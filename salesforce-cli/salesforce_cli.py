"""cli-anything-salesforce -- Salesforce REST API CLI"""
import json, os, sys, urllib.request, urllib.parse, urllib.error
import click

def _err(msg):
    click.echo(json.dumps({"error": msg}), err=True)
    sys.exit(1)

def _login(ctx):
    """Obtain access token via username-password OAuth2 flow."""
    if ctx.obj.get("_access_token"):
        return ctx.obj["_access_token"], ctx.obj["_instance_url"]
    
    token = ctx.obj.get("token")
    if token:
        instance = ctx.obj.get("instance") or _err("SALESFORCE_INSTANCE not set (e.g. https://myorg.my.salesforce.com)")
        ctx.obj["_access_token"] = token
        ctx.obj["_instance_url"] = instance
        return token, instance
    
    username = ctx.obj.get("username") or _err("SALESFORCE_USERNAME not set")
    password = ctx.obj.get("password") or _err("SALESFORCE_PASSWORD not set")
    sec_token = ctx.obj.get("security_token", "")
    client_id = ctx.obj.get("client_id") or "3MVG9n_HvETGhr3A7gzxJbHe0QkD0YJXJ27lLVEr0ixJg3m4QWQJgzWzFefMqmjUYOGYTJLpVRPcqMPBWJanH"
    client_secret = ctx.obj.get("client_secret", "")
    
    login_url = "https://login.salesforce.com/services/oauth2/token"
    form = urllib.parse.urlencode({
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password + sec_token,
    }).encode()
    req = urllib.request.Request(login_url, data=form, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            ctx.obj["_access_token"] = data["access_token"]
            ctx.obj["_instance_url"] = data["instance_url"]
            return data["access_token"], data["instance_url"]
    except urllib.error.HTTPError as e:
        _err(f"Login failed HTTP {e.code}: {e.read().decode()}")

def _req(ctx, method, path, body=None, params=None):
    access_token, instance_url = _login(ctx)
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{instance_url}{path}{qs}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {access_token}")
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
        records = data.get("records", data) if isinstance(data, dict) else data
        if isinstance(records, list):
            for rec in records:
                parts = []
                for k in ("Id", "Name", "Email", "FirstName", "LastName", "StageName", "Amount", "Status", "Subject"):
                    v = rec.get(k)
                    if v:
                        parts.append(f"{k}={str(v)[:40]}")
                click.echo("  ".join(parts) if parts else str(rec))
        else:
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))

@click.group()
@click.option("--username", envvar="SALESFORCE_USERNAME", default=None)
@click.option("--password", envvar="SALESFORCE_PASSWORD", default=None)
@click.option("--token", envvar="SALESFORCE_ACCESS_TOKEN", default=None, help="Pre-obtained access token")
@click.option("--instance", envvar="SALESFORCE_INSTANCE", default=None, help="https://myorg.my.salesforce.com")
@click.option("--security-token", envvar="SALESFORCE_SECURITY_TOKEN", default="")
@click.option("--client-id", envvar="SALESFORCE_CLIENT_ID", default=None)
@click.option("--client-secret", envvar="SALESFORCE_CLIENT_SECRET", default="")
@click.option("--json", "as_json", is_flag=True)
@click.pass_context
def cli(ctx, username, password, token, instance, security_token, client_id, client_secret, as_json):
    """cli-anything-salesforce -- SOQL, records, leads, opportunities"""
    ctx.ensure_object(dict)
    ctx.obj.update({"username": username, "password": password, "token": token,
                    "instance": instance, "security_token": security_token,
                    "client_id": client_id, "client_secret": client_secret, "json": as_json})

@cli.command()
@click.pass_context
def detect(ctx):
    """Check Salesforce connectivity."""
    r = _req(ctx, "GET", "/services/data/v59.0/")
    _out(ctx, {"status": "ok", "api_version": r.get("label"), "instance": ctx.obj.get("_instance_url")})

@cli.command()
@click.pass_context
def schema(ctx):
    """Output capability schema (no credentials needed)."""
    info = {
        "name": "cli-anything-salesforce", "version": "1.0.0",
        "description": "Salesforce REST API CLI - SOQL queries, records, leads, contacts, opportunities",
        "requires_token": True,
        "env_vars": {
            "SALESFORCE_USERNAME": "your-email@company.com",
            "SALESFORCE_PASSWORD": "your-password",
            "SALESFORCE_SECURITY_TOKEN": "your-security-token",
            "SALESFORCE_ACCESS_TOKEN": "or pre-obtained access token + SALESFORCE_INSTANCE",
        },
        "commands": [
            {"cmd": "detect", "desc": "Check connectivity"},
            {"cmd": "query", "args": ["SOQL_STRING"], "desc": "Execute SOQL query"},
            {"cmd": "objects list", "args": [], "desc": "List all available sObjects"},
            {"cmd": "record get", "args": ["OBJECT", "RECORD_ID"], "desc": "Get a record"},
            {"cmd": "record create", "args": ["OBJECT", "--data JSON"], "desc": "Create a record"},
            {"cmd": "record update", "args": ["OBJECT", "RECORD_ID", "--data JSON"], "desc": "Update a record"},
            {"cmd": "record delete", "args": ["OBJECT", "RECORD_ID"], "desc": "Delete a record"},
        ],
        "json_flag": "--json",
        "example": "salesforce-cli --json query \"SELECT Id,Name,Email FROM Contact LIMIT 10\"",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))

@cli.command("query")
@click.argument("soql")
@click.pass_context
def query(ctx, soql):
    """Execute a SOQL query."""
    r = _req(ctx, "GET", "/services/data/v59.0/query", params={"q": soql})
    _out(ctx, r)

@cli.group()
def objects():
    """Explore Salesforce object types."""

@objects.command("list")
@click.pass_context
def objects_list(ctx):
    """List all sObjects."""
    r = _req(ctx, "GET", "/services/data/v59.0/sobjects")
    if ctx.obj.get("json"):
        click.echo(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        for obj in r.get("sobjects", []):
            if obj.get("queryable"):
                click.echo(f"  {obj.get('name'):<40} {obj.get('label')}")

@cli.group()
def record():
    """CRUD operations on Salesforce records."""

@record.command("get")
@click.argument("sobject")
@click.argument("record_id")
@click.pass_context
def record_get(ctx, sobject, record_id):
    """Get a Salesforce record."""
    r = _req(ctx, "GET", f"/services/data/v59.0/sobjects/{sobject}/{record_id}")
    _out(ctx, r)

@record.command("create")
@click.argument("sobject")
@click.option("--data", required=True, help='JSON string: \'{"Name":"Acme","Email":"a@b.com"}\'')
@click.pass_context
def record_create(ctx, sobject, data):
    """Create a record."""
    try:
        body = json.loads(data)
    except json.JSONDecodeError as e:
        _err(f"Invalid JSON: {e}")
    r = _req(ctx, "POST", f"/services/data/v59.0/sobjects/{sobject}", body)
    _out(ctx, {"status": "ok", "id": r.get("id"), "success": r.get("success")})

@record.command("update")
@click.argument("sobject")
@click.argument("record_id")
@click.option("--data", required=True, help='JSON string: \'{"Name":"New Name"}\'')
@click.pass_context
def record_update(ctx, sobject, record_id, data):
    """Update a record."""
    try:
        body = json.loads(data)
    except json.JSONDecodeError as e:
        _err(f"Invalid JSON: {e}")
    _req(ctx, "PATCH", f"/services/data/v59.0/sobjects/{sobject}/{record_id}", body)
    _out(ctx, {"status": "ok", "updated": record_id})

@record.command("delete")
@click.argument("sobject")
@click.argument("record_id")
@click.pass_context
def record_delete(ctx, sobject, record_id):
    """Delete a record."""
    _req(ctx, "DELETE", f"/services/data/v59.0/sobjects/{sobject}/{record_id}")
    _out(ctx, {"status": "ok", "deleted": record_id})

if __name__ == "__main__":
    cli()
