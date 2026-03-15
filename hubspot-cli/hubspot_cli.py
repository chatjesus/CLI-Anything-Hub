"""cli-anything-hubspot -- HubSpot CRM REST API CLI"""
import json, os, sys, urllib.request, urllib.parse, urllib.error
import click

BASE = "https://api.hubapi.com"

def _err(msg):
    click.echo(json.dumps({"error": msg}), err=True)
    sys.exit(1)

def _req(ctx, method, path, body=None, params=None):
    token = ctx.obj.get("token") or _err("HUBSPOT_API_KEY not set")
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{BASE}{path}{qs}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        _err(f"HTTP {e.code}: {e.read().decode()}")

def _out(ctx, data):
    if ctx.obj.get("json"):
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        results = data.get("results", data) if isinstance(data, dict) else data
        if isinstance(results, list):
            for item in results:
                props = item.get("properties", item)
                parts = []
                for k in ("id", "email", "firstname", "lastname", "dealname", "amount", "name", "domain"):
                    v = props.get(k) or item.get(k)
                    if v:
                        parts.append(f"{k}={v}")
                click.echo("  ".join(parts) if parts else str(item))
        else:
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))

@click.group()
@click.option("--token", envvar="HUBSPOT_API_KEY", default=None)
@click.option("--json", "as_json", is_flag=True)
@click.pass_context
def cli(ctx, token, as_json):
    """cli-anything-hubspot -- HubSpot CRM API (contacts, deals, companies)"""
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json

@cli.command()
@click.pass_context
def detect(ctx):
    """Check HubSpot API connectivity."""
    r = _req(ctx, "GET", "/crm/v3/objects/contacts", params={"limit": 1})
    _out(ctx, {"status": "ok", "total_contacts": r.get("total", "unknown")})

@cli.command()
@click.pass_context
def schema(ctx):
    """Output capability schema (no token needed)."""
    info = {
        "name": "cli-anything-hubspot", "version": "1.0.0",
        "description": "HubSpot CRM CLI - contacts, deals, companies, pipelines",
        "requires_token": True,
        "token_env": "HUBSPOT_API_KEY",
        "token_hint": "Private App token from HubSpot > Settings > Integrations > Private Apps",
        "commands": [
            {"cmd": "detect", "desc": "Check connectivity"},
            {"cmd": "contacts list", "args": ["--limit INT", "--props STR"], "desc": "List contacts"},
            {"cmd": "contacts search", "args": ["--email STR", "--query STR"], "desc": "Search contacts"},
            {"cmd": "contacts create", "args": ["--email STR", "--first STR", "--last STR"], "desc": "Create contact"},
            {"cmd": "deals list", "args": ["--limit INT"], "desc": "List deals"},
            {"cmd": "deals create", "args": ["--name STR", "--amount FLOAT", "--stage STR"], "desc": "Create deal"},
            {"cmd": "companies list", "args": ["--limit INT"], "desc": "List companies"},
            {"cmd": "companies search", "args": ["--domain STR"], "desc": "Search by domain"},
        ],
        "json_flag": "--json",
        "example": "hubspot-cli --json contacts search --email john@example.com",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))

@cli.group()
def contacts():
    """Manage HubSpot contacts."""

@contacts.command("list")
@click.option("--limit", default=20)
@click.option("--props", default="email,firstname,lastname,company", show_default=True)
@click.pass_context
def contacts_list(ctx, limit, props):
    """List contacts."""
    r = _req(ctx, "GET", "/crm/v3/objects/contacts", params={"limit": limit, "properties": props})
    _out(ctx, r)

@contacts.command("search")
@click.option("--email", default=None)
@click.option("--query", default=None, help="Free-text search")
@click.pass_context
def contacts_search(ctx, email, query):
    """Search contacts."""
    filters = []
    if email:
        filters.append({"propertyName": "email", "operator": "EQ", "value": email})
    body = {
        "filterGroups": [{"filters": filters}] if filters else [],
        "query": query or "",
        "properties": ["email", "firstname", "lastname", "phone", "company"],
        "limit": 10,
    }
    r = _req(ctx, "POST", "/crm/v3/objects/contacts/search", body)
    _out(ctx, r)

@contacts.command("create")
@click.option("--email", required=True)
@click.option("--first", default="")
@click.option("--last", default="")
@click.option("--phone", default="")
@click.pass_context
def contacts_create(ctx, email, first, last, phone):
    """Create a contact."""
    body = {"properties": {"email": email, "firstname": first, "lastname": last, "phone": phone}}
    r = _req(ctx, "POST", "/crm/v3/objects/contacts", body)
    _out(ctx, {"status": "ok", "id": r.get("id"), "email": r.get("properties", {}).get("email")})

@cli.group()
def deals():
    """Manage HubSpot deals."""

@deals.command("list")
@click.option("--limit", default=20)
@click.option("--props", default="dealname,amount,dealstage,closedate", show_default=True)
@click.pass_context
def deals_list(ctx, limit, props):
    """List deals."""
    r = _req(ctx, "GET", "/crm/v3/objects/deals", params={"limit": limit, "properties": props})
    _out(ctx, r)

@deals.command("create")
@click.option("--name", required=True, help="Deal name")
@click.option("--amount", default="0")
@click.option("--stage", default="appointmentscheduled", help="Pipeline stage ID")
@click.option("--pipeline", default="default")
@click.pass_context
def deals_create(ctx, name, amount, stage, pipeline):
    """Create a deal."""
    body = {"properties": {"dealname": name, "amount": amount, "dealstage": stage, "pipeline": pipeline}}
    r = _req(ctx, "POST", "/crm/v3/objects/deals", body)
    _out(ctx, {"status": "ok", "id": r.get("id"), "name": r.get("properties", {}).get("dealname")})

@cli.group()
def companies():
    """Manage HubSpot companies."""

@companies.command("list")
@click.option("--limit", default=20)
@click.pass_context
def companies_list(ctx, limit):
    """List companies."""
    r = _req(ctx, "GET", "/crm/v3/objects/companies", params={"limit": limit, "properties": "name,domain,industry"})
    _out(ctx, r)

@companies.command("search")
@click.option("--domain", required=True)
@click.pass_context
def companies_search(ctx, domain):
    """Search company by domain."""
    body = {
        "filterGroups": [{"filters": [{"propertyName": "domain", "operator": "EQ", "value": domain}]}],
        "properties": ["name", "domain", "industry", "numberofemployees"],
        "limit": 5,
    }
    r = _req(ctx, "POST", "/crm/v3/objects/companies/search", body)
    _out(ctx, r)

if __name__ == "__main__":
    cli()
