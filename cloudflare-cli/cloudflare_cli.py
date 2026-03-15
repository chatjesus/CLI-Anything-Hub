"""cli-anything-cloudflare -- Cloudflare REST API CLI"""
import json, os, sys, urllib.request, urllib.parse, urllib.error
import click

BASE = "https://api.cloudflare.com/client/v4"

def _err(msg):
    click.echo(json.dumps({"error": msg}), err=True)
    sys.exit(1)

def _req(ctx, method, path, body=None, params=None):
    token = ctx.obj.get("token") or _err("CLOUDFLARE_API_TOKEN not set")
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{BASE}{path}{qs}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
            if not resp.get("success", True):
                _err(str(resp.get("errors", "unknown error")))
            return resp.get("result", resp)
    except urllib.error.HTTPError as e:
        _err(f"HTTP {e.code}: {e.read().decode()}")

def _out(ctx, data):
    if ctx.obj.get("json"):
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        if isinstance(data, list):
            for item in data:
                parts = []
                for k in ("id", "name", "type", "content", "status", "zone_name", "script", "title"):
                    v = item.get(k)
                    if v:
                        parts.append(f"{k}={str(v)[:60]}")
                click.echo("  ".join(parts))
        else:
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))

@click.group()
@click.option("--token", envvar="CLOUDFLARE_API_TOKEN", default=None)
@click.option("--json", "as_json", is_flag=True)
@click.pass_context
def cli(ctx, token, as_json):
    """cli-anything-cloudflare -- DNS, Workers, R2, Zones via Cloudflare API"""
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json

@cli.command()
@click.pass_context
def detect(ctx):
    """Check Cloudflare credentials."""
    r = _req(ctx, "GET", "/user/tokens/verify")
    _out(ctx, {"status": "ok", "token_status": r.get("status"), "id": r.get("id")})

@cli.command()
@click.pass_context
def schema(ctx):
    """Output capability schema (no token needed)."""
    info = {
        "name": "cli-anything-cloudflare", "version": "1.0.0",
        "description": "Cloudflare REST API CLI - zones, DNS records, Workers, R2 buckets, firewall",
        "requires_token": True,
        "token_env": "CLOUDFLARE_API_TOKEN",
        "token_hint": "Create at dash.cloudflare.com > My Profile > API Tokens",
        "commands": [
            {"cmd": "detect", "desc": "Verify token"},
            {"cmd": "zones list", "args": ["--name STR"], "desc": "List zones"},
            {"cmd": "dns list", "args": ["ZONE_ID", "--type A|CNAME|TXT", "--name STR"], "desc": "List DNS records"},
            {"cmd": "dns add", "args": ["ZONE_ID", "--type STR", "--name STR", "--content STR", "--ttl INT"], "desc": "Add DNS record"},
            {"cmd": "dns delete", "args": ["ZONE_ID", "RECORD_ID"], "desc": "Delete DNS record"},
            {"cmd": "workers list", "args": ["ACCOUNT_ID"], "desc": "List Workers scripts"},
            {"cmd": "r2 list", "args": ["ACCOUNT_ID"], "desc": "List R2 buckets"},
        ],
        "json_flag": "--json",
        "example": "cloudflare-cli --json dns list ZONE_ID --type A",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))

@cli.group()
def zones():
    """Manage Cloudflare zones."""

@zones.command("list")
@click.option("--name", default=None, help="Filter by domain name")
@click.option("--limit", default=20)
@click.pass_context
def zones_list(ctx, name, limit):
    """List all zones."""
    params = {"per_page": limit}
    if name:
        params["name"] = name
    r = _req(ctx, "GET", "/zones", params=params)
    _out(ctx, r)

@cli.group()
def dns():
    """Manage DNS records."""

@dns.command("list")
@click.argument("zone_id")
@click.option("--type", "rec_type", default=None, help="A, CNAME, TXT, MX, etc.")
@click.option("--name", default=None)
@click.option("--limit", default=100)
@click.pass_context
def dns_list(ctx, zone_id, rec_type, name, limit):
    """List DNS records for a zone."""
    params = {"per_page": limit}
    if rec_type:
        params["type"] = rec_type
    if name:
        params["name"] = name
    r = _req(ctx, "GET", f"/zones/{zone_id}/dns_records", params=params)
    _out(ctx, r)

@dns.command("add")
@click.argument("zone_id")
@click.option("--type", "rec_type", required=True, help="A, CNAME, TXT, MX, AAAA")
@click.option("--name", required=True, help="DNS name, e.g. subdomain.example.com")
@click.option("--content", required=True, help="Record content / IP")
@click.option("--ttl", default=1, help="TTL in seconds (1 = auto)")
@click.option("--proxied", is_flag=True, default=False, help="Enable Cloudflare proxy")
@click.pass_context
def dns_add(ctx, zone_id, rec_type, name, content, ttl, proxied):
    """Add a DNS record."""
    body = {"type": rec_type, "name": name, "content": content, "ttl": ttl, "proxied": proxied}
    r = _req(ctx, "POST", f"/zones/{zone_id}/dns_records", body)
    _out(ctx, {"status": "ok", "id": r.get("id"), "name": r.get("name"), "type": r.get("type"), "content": r.get("content")})

@dns.command("delete")
@click.argument("zone_id")
@click.argument("record_id")
@click.pass_context
def dns_delete(ctx, zone_id, record_id):
    """Delete a DNS record."""
    r = _req(ctx, "DELETE", f"/zones/{zone_id}/dns_records/{record_id}")
    _out(ctx, {"status": "ok", "deleted_id": record_id})

@cli.group()
def workers():
    """Manage Cloudflare Workers."""

@workers.command("list")
@click.argument("account_id", envvar="CLOUDFLARE_ACCOUNT_ID")
@click.pass_context
def workers_list(ctx, account_id):
    """List Workers scripts."""
    r = _req(ctx, "GET", f"/accounts/{account_id}/workers/scripts")
    _out(ctx, r)

@cli.group()
def r2():
    """Manage R2 buckets."""

@r2.command("list")
@click.argument("account_id", envvar="CLOUDFLARE_ACCOUNT_ID")
@click.pass_context
def r2_list(ctx, account_id):
    """List R2 buckets."""
    r = _req(ctx, "GET", f"/accounts/{account_id}/r2/buckets")
    _out(ctx, r.get("buckets", r))

if __name__ == "__main__":
    cli()
