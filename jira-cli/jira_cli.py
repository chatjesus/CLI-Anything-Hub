"""cli-anything-jira -- Atlassian Jira REST API CLI"""
import json, os, sys, urllib.request, urllib.parse, urllib.error, base64
import click

def _err(msg):
    click.echo(json.dumps({"error": msg}), err=True)
    sys.exit(1)

def _req(ctx, method, path, body=None, params=None):
    url_base = ctx.obj.get("url") or _err("JIRA_URL not set (e.g. https://myorg.atlassian.net)")
    user = ctx.obj.get("user") or _err("JIRA_USER not set (your Atlassian email)")
    token = ctx.obj.get("token") or _err("JIRA_TOKEN not set")
    url_base = url_base.rstrip("/")
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{url_base}/rest/api/3{path}{qs}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    cred = base64.b64encode(f"{user}:{token}".encode()).decode()
    req.add_header("Authorization", f"Basic {cred}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            content = r.read()
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        _err(f"HTTP {e.code}: {e.read().decode()}")

def _out(ctx, data):
    if ctx.obj.get("json"):
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        issues = data.get("issues", data if isinstance(data, list) else None)
        if issues:
            for i in issues:
                key = i.get("key", "")
                fields = i.get("fields", {})
                summary = fields.get("summary", "")
                status = fields.get("status", {}).get("name", "")
                assignee = (fields.get("assignee") or {}).get("displayName", "unassigned")
                click.echo(f"  {key:<12} [{status:<12}] {summary[:50]}  ({assignee})")
        else:
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))

@click.group()
@click.option("--url", envvar="JIRA_URL", default=None, help="https://myorg.atlassian.net")
@click.option("--user", envvar="JIRA_USER", default=None, help="your-email@company.com")
@click.option("--token", envvar="JIRA_TOKEN", default=None, help="API token from id.atlassian.com")
@click.option("--json", "as_json", is_flag=True)
@click.pass_context
def cli(ctx, url, user, token, as_json):
    """cli-anything-jira -- Jira REST API (issues, sprints, JQL)"""
    ctx.ensure_object(dict)
    ctx.obj["url"] = url
    ctx.obj["user"] = user
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json

@cli.command()
@click.pass_context
def detect(ctx):
    """Check Jira connectivity."""
    r = _req(ctx, "GET", "/myself")
    _out(ctx, {"status": "ok", "user": r.get("displayName"), "email": r.get("emailAddress"), "account_id": r.get("accountId")})

@cli.command()
@click.pass_context
def schema(ctx):
    """Output capability schema (no credentials needed)."""
    info = {
        "name": "cli-anything-jira", "version": "1.0.0",
        "description": "Jira REST API CLI - issues, JQL search, projects, sprints, transitions",
        "requires_token": True,
        "env_vars": {
            "JIRA_URL": "https://myorg.atlassian.net",
            "JIRA_USER": "your-email@company.com",
            "JIRA_TOKEN": "API token from id.atlassian.com/manage-profile/security/api-tokens",
        },
        "commands": [
            {"cmd": "detect", "desc": "Check connectivity"},
            {"cmd": "issues search", "args": ["--jql STR", "--limit INT", "--fields STR"], "desc": "JQL search"},
            {"cmd": "issues get", "args": ["ISSUE_KEY"], "desc": "Get issue detail"},
            {"cmd": "issues create", "args": ["--project STR", "--type STR", "--summary STR", "--desc STR"], "desc": "Create issue"},
            {"cmd": "issues transition", "args": ["ISSUE_KEY", "--to STR"], "desc": "Move issue to status"},
            {"cmd": "issues comment", "args": ["ISSUE_KEY", "--body STR"], "desc": "Add comment"},
            {"cmd": "projects list", "args": [], "desc": "List all projects"},
        ],
        "json_flag": "--json",
        "example": "jira-cli --json issues search --jql 'project=MYPROJ AND status=\"In Progress\"'",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))

@cli.group()
def issues():
    """Manage Jira issues."""

@issues.command("search")
@click.option("--jql", default="ORDER BY created DESC", show_default=True)
@click.option("--limit", default=20)
@click.option("--fields", default="summary,status,assignee,priority,issuetype", show_default=True)
@click.pass_context
def issues_search(ctx, jql, limit, fields):
    """Search issues via JQL."""
    r = _req(ctx, "GET", "/search", params={"jql": jql, "maxResults": limit, "fields": fields})
    _out(ctx, r)

@issues.command("get")
@click.argument("issue_key")
@click.pass_context
def issues_get(ctx, issue_key):
    """Get an issue by key (e.g. PROJ-123)."""
    r = _req(ctx, "GET", f"/issue/{issue_key}")
    if ctx.obj.get("json"):
        _out(ctx, r)
    else:
        f = r.get("fields", {})
        click.echo(f"  Key:     {r.get('key')}")
        click.echo(f"  Summary: {f.get('summary')}")
        click.echo(f"  Status:  {f.get('status', {}).get('name')}")
        click.echo(f"  Type:    {f.get('issuetype', {}).get('name')}")
        click.echo(f"  Priority:{f.get('priority', {}).get('name')}")
        click.echo(f"  Assignee:{(f.get('assignee') or {}).get('displayName', 'unassigned')}")
        click.echo(f"  Created: {f.get('created', '')[:10]}")

@issues.command("create")
@click.option("--project", required=True, help="Project key, e.g. MYPROJ")
@click.option("--type", "issue_type", default="Task", show_default=True)
@click.option("--summary", required=True)
@click.option("--desc", default="", help="Issue description")
@click.option("--priority", default="Medium")
@click.pass_context
def issues_create(ctx, project, issue_type, summary, desc, priority):
    """Create a new issue."""
    body = {
        "fields": {
            "project": {"key": project},
            "issuetype": {"name": issue_type},
            "summary": summary,
            "priority": {"name": priority},
            "description": {"version": 1, "type": "doc", "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": desc}]}
            ]} if desc else None,
        }
    }
    body["fields"] = {k: v for k, v in body["fields"].items() if v}
    r = _req(ctx, "POST", "/issue", body)
    _out(ctx, {"status": "ok", "key": r.get("key"), "id": r.get("id"), "url": r.get("self")})

@issues.command("transition")
@click.argument("issue_key")
@click.option("--to", required=True, help="Target status name or transition ID")
@click.pass_context
def issues_transition(ctx, issue_key, to):
    """Transition an issue to a new status."""
    trans = _req(ctx, "GET", f"/issue/{issue_key}/transitions")
    target = None
    for t in trans.get("transitions", []):
        if t.get("name", "").lower() == to.lower() or t.get("id") == to:
            target = t["id"]
            break
    if not target:
        names = [t["name"] for t in trans.get("transitions", [])]
        _err(f"Transition '{to}' not found. Available: {names}")
    _req(ctx, "POST", f"/issue/{issue_key}/transitions", {"transition": {"id": target}})
    _out(ctx, {"status": "ok", "issue": issue_key, "transitioned_to": to})

@issues.command("comment")
@click.argument("issue_key")
@click.option("--body", required=True)
@click.pass_context
def issues_comment(ctx, issue_key, body):
    """Add a comment to an issue."""
    payload = {"body": {"version": 1, "type": "doc", "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": body}]}
    ]}}
    r = _req(ctx, "POST", f"/issue/{issue_key}/comment", payload)
    _out(ctx, {"status": "ok", "comment_id": r.get("id")})

@cli.group()
def projects():
    """List and manage projects."""

@projects.command("list")
@click.option("--limit", default=50)
@click.pass_context
def projects_list(ctx, limit):
    """List all Jira projects."""
    r = _req(ctx, "GET", "/project/search", params={"maxResults": limit})
    if ctx.obj.get("json"):
        _out(ctx, r)
    else:
        for p in r.get("values", []):
            click.echo(f"  {p.get('key'):<12} {p.get('name')}")

if __name__ == "__main__":
    cli()
