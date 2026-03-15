"""cli-anything-vercel -- Vercel REST API CLI"""
import json, os, sys, urllib.request, urllib.parse, urllib.error
import click

BASE = "https://api.vercel.com"

def _err(msg):
    click.echo(json.dumps({"error": msg}), err=True)
    sys.exit(1)

def _req(ctx, method, path, body=None, params=None):
    token = ctx.obj.get("token") or _err("VERCEL_TOKEN not set")
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{BASE}{path}{qs}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
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
        if isinstance(data, list):
            for item in data:
                parts = []
                for k in ("uid", "id", "name", "url", "state", "readyState", "target", "key", "value"):
                    v = item.get(k)
                    if v:
                        parts.append(f"{k}={str(v)[:50]}")
                click.echo("  ".join(parts))
        elif isinstance(data, dict) and ("deployments" in data or "projects" in data or "domains" in data or "envs" in data):
            items = list(data.values())[0]
            _out(ctx, items)
        else:
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))

@click.group()
@click.option("--token", envvar="VERCEL_TOKEN", default=None)
@click.option("--team", envvar="VERCEL_TEAM_ID", default=None, help="Team slug or ID")
@click.option("--json", "as_json", is_flag=True)
@click.pass_context
def cli(ctx, token, team, as_json):
    """cli-anything-vercel -- Deploy, manage domains, env vars via Vercel REST API"""
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["team"] = team
    ctx.obj["json"] = as_json

def _team_params(ctx):
    t = ctx.obj.get("team")
    return {"teamId": t} if t else {}

@cli.command()
@click.pass_context
def detect(ctx):
    """Check Vercel credentials."""
    r = _req(ctx, "GET", "/v2/user")
    u = r.get("user", r)
    _out(ctx, {"status": "ok", "username": u.get("username"), "email": u.get("email"), "name": u.get("name")})

@cli.command()
@click.pass_context
def schema(ctx):
    """Output capability schema (no token needed)."""
    info = {
        "name": "cli-anything-vercel", "version": "1.0.0",
        "description": "Vercel REST API CLI - deployments, projects, domains, env vars",
        "requires_token": True,
        "token_env": "VERCEL_TOKEN",
        "token_hint": "Create at vercel.com/account/tokens",
        "commands": [
            {"cmd": "detect", "desc": "Check credentials"},
            {"cmd": "deployments list", "args": ["--project STR", "--limit INT"], "desc": "List deployments"},
            {"cmd": "deployments get", "args": ["DEPLOY_ID"], "desc": "Get deployment detail"},
            {"cmd": "deployments cancel", "args": ["DEPLOY_ID"], "desc": "Cancel a deployment"},
            {"cmd": "projects list", "args": ["--limit INT"], "desc": "List projects"},
            {"cmd": "domains list", "args": ["--project STR"], "desc": "List domains"},
            {"cmd": "env list", "args": ["PROJECT_NAME"], "desc": "List environment variables"},
            {"cmd": "env add", "args": ["PROJECT_NAME", "--key STR", "--value STR", "--target production|preview|development"], "desc": "Add env var"},
        ],
        "json_flag": "--json",
        "example": "vercel-cli --json deployments list --project my-app --limit 5",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))

@cli.group()
def deployments():
    """Manage Vercel deployments."""

@deployments.command("list")
@click.option("--project", default=None, help="Project name or ID")
@click.option("--limit", default=20)
@click.pass_context
def deployments_list(ctx, project, limit):
    """List deployments."""
    params = {**_team_params(ctx), "limit": limit}
    if project:
        params["projectId"] = project
    r = _req(ctx, "GET", "/v6/deployments", params=params)
    _out(ctx, r.get("deployments", r))

@deployments.command("get")
@click.argument("deploy_id")
@click.pass_context
def deployments_get(ctx, deploy_id):
    """Get deployment details."""
    r = _req(ctx, "GET", f"/v13/deployments/{deploy_id}")
    if ctx.obj.get("json"):
        _out(ctx, r)
    else:
        click.echo(f"  ID:      {r.get('id')}")
        click.echo(f"  URL:     {r.get('url')}")
        click.echo(f"  State:   {r.get('readyState')}")
        click.echo(f"  Created: {r.get('createdAt')}")

@deployments.command("cancel")
@click.argument("deploy_id")
@click.pass_context
def deployments_cancel(ctx, deploy_id):
    """Cancel a running deployment."""
    r = _req(ctx, "PATCH", f"/v12/deployments/{deploy_id}/cancel")
    _out(ctx, {"status": "ok", "uid": r.get("uid"), "state": r.get("readyState")})

@cli.group()
def projects():
    """Manage Vercel projects."""

@projects.command("list")
@click.option("--limit", default=20)
@click.pass_context
def projects_list(ctx, limit):
    """List all projects."""
    params = {**_team_params(ctx), "limit": limit}
    r = _req(ctx, "GET", "/v9/projects", params=params)
    _out(ctx, r.get("projects", r))

@cli.group()
def domains():
    """Manage Vercel domains."""

@domains.command("list")
@click.option("--project", default=None)
@click.pass_context
def domains_list(ctx, project):
    """List domains."""
    if project:
        params = {**_team_params(ctx)}
        r = _req(ctx, "GET", f"/v9/projects/{project}/domains", params=params)
    else:
        r = _req(ctx, "GET", "/v5/domains", params=_team_params(ctx))
    _out(ctx, r.get("domains", r))

@cli.group()
def env():
    """Manage environment variables."""

@env.command("list")
@click.argument("project")
@click.pass_context
def env_list(ctx, project):
    """List env vars for a project."""
    r = _req(ctx, "GET", f"/v9/projects/{project}/env", params=_team_params(ctx))
    _out(ctx, r.get("envs", r))

@env.command("add")
@click.argument("project")
@click.option("--key", required=True)
@click.option("--value", required=True)
@click.option("--target", default="production,preview,development", show_default=True)
@click.pass_context
def env_add(ctx, project, key, value, target):
    """Add an environment variable."""
    targets = [t.strip() for t in target.split(",")]
    body = {"key": key, "value": value, "target": targets, "type": "encrypted"}
    r = _req(ctx, "POST", f"/v10/projects/{project}/env", body)
    _out(ctx, {"status": "ok", "key": r.get("key"), "id": r.get("id")})

if __name__ == "__main__":
    cli()
