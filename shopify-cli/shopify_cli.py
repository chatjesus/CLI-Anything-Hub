"""cli-anything-shopify -- Shopify Admin REST API CLI"""
import json, os, sys, urllib.request, urllib.error
import click

def _err(msg):
    click.echo(json.dumps({"error": msg}), err=True)
    sys.exit(1)

def _req(ctx, method, path, body=None):
    shop = ctx.obj.get("shop") or _err("SHOPIFY_SHOP not set (e.g. mystore.myshopify.com)")
    token = ctx.obj.get("token") or _err("SHOPIFY_ACCESS_TOKEN not set")
    url = f"https://{shop}/admin/api/2024-04{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-Shopify-Access-Token", token)
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
        if isinstance(data, dict) and len(data) == 1:
            data = list(data.values())[0]
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    parts = []
                    for k in ("id","title","name","email","handle","status","financial_status"):
                        if k in item:
                            parts.append(f"{k}={item[k]}")
                    click.echo("  ".join(parts) if parts else str(item))
                else:
                    click.echo(str(item))
        else:
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))

@click.group()
@click.option("--shop", envvar="SHOPIFY_SHOP", default=None, help="mystore.myshopify.com")
@click.option("--token", envvar="SHOPIFY_ACCESS_TOKEN", default=None)
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@click.pass_context
def cli(ctx, shop, token, as_json):
    """cli-anything-shopify -- Shopify Admin REST API"""
    ctx.ensure_object(dict)
    ctx.obj["shop"] = shop
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json

@cli.command()
@click.pass_context
def detect(ctx):
    """Check Shopify connectivity."""
    r = _req(ctx, "GET", "/shop.json")
    s = r.get("shop", {})
    _out(ctx, {"status": "ok", "shop": s.get("name"), "domain": s.get("domain"), "plan": s.get("plan_name")})

@cli.command()
@click.pass_context
def schema(ctx):
    """Output capability schema (no token needed)."""
    info = {
        "name": "cli-anything-shopify", "version": "1.0.0",
        "description": "Shopify Admin REST API CLI - products, orders, customers, inventory",
        "requires_token": True,
        "token_env": "SHOPIFY_ACCESS_TOKEN",
        "shop_env": "SHOPIFY_SHOP",
        "token_hint": "Admin API access token from Shopify Partners or Custom App",
        "commands": [
            {"cmd": "detect", "desc": "Check connectivity"},
            {"cmd": "products list", "args": ["--limit INT", "--status active|draft|archived"], "desc": "List products"},
            {"cmd": "products get", "args": ["PRODUCT_ID"], "desc": "Get product detail"},
            {"cmd": "products create", "args": ["--title STR", "--price FLOAT", "--sku STR"], "desc": "Create product"},
            {"cmd": "orders list", "args": ["--limit INT", "--status open|closed|any"], "desc": "List orders"},
            {"cmd": "orders get", "args": ["ORDER_ID"], "desc": "Get order detail"},
            {"cmd": "customers list", "args": ["--limit INT", "--query STR"], "desc": "List customers"},
            {"cmd": "inventory list", "args": ["--location-id STR"], "desc": "List inventory levels"},
        ],
        "json_flag": "--json",
        "example": "shopify-cli --json products list --limit 10",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))

@cli.group()
def products():
    """Manage Shopify products."""

@products.command("list")
@click.option("--limit", default=20, show_default=True)
@click.option("--status", default="any")
@click.pass_context
def products_list(ctx, limit, status):
    """List products."""
    r = _req(ctx, "GET", f"/products.json?limit={limit}&status={status}")
    _out(ctx, r)

@products.command("get")
@click.argument("product_id")
@click.pass_context
def products_get(ctx, product_id):
    """Get a product by ID."""
    r = _req(ctx, "GET", f"/products/{product_id}.json")
    _out(ctx, r)

@products.command("create")
@click.option("--title", required=True)
@click.option("--price", default="0.00")
@click.option("--sku", default="")
@click.option("--vendor", default="")
@click.pass_context
def products_create(ctx, title, price, sku, vendor):
    """Create a new product."""
    body = {"product": {"title": title, "vendor": vendor,
                        "variants": [{"price": price, "sku": sku}]}}
    r = _req(ctx, "POST", "/products.json", body)
    _out(ctx, r)

@products.command("update")
@click.argument("product_id")
@click.option("--title", default=None)
@click.option("--status", default=None)
@click.pass_context
def products_update(ctx, product_id, title, status):
    """Update a product."""
    body = {"product": {k: v for k, v in {"title": title, "status": status}.items() if v}}
    r = _req(ctx, "PUT", f"/products/{product_id}.json", body)
    _out(ctx, r)

@cli.group()
def orders():
    """Manage Shopify orders."""

@orders.command("list")
@click.option("--limit", default=20, show_default=True)
@click.option("--status", default="any")
@click.pass_context
def orders_list(ctx, limit, status):
    """List orders."""
    r = _req(ctx, "GET", f"/orders.json?limit={limit}&status={status}")
    _out(ctx, r)

@orders.command("get")
@click.argument("order_id")
@click.pass_context
def orders_get(ctx, order_id):
    """Get an order by ID."""
    r = _req(ctx, "GET", f"/orders/{order_id}.json")
    _out(ctx, r)

@cli.group()
def customers():
    """Manage Shopify customers."""

@customers.command("list")
@click.option("--limit", default=20, show_default=True)
@click.option("--query", default=None, help="Search query")
@click.pass_context
def customers_list(ctx, limit, query):
    """List customers."""
    qs = f"?limit={limit}" + (f"&query={query}" if query else "")
    r = _req(ctx, "GET", f"/customers.json{qs}")
    _out(ctx, r)

@customers.command("get")
@click.argument("customer_id")
@click.pass_context
def customers_get(ctx, customer_id):
    """Get a customer by ID."""
    r = _req(ctx, "GET", f"/customers/{customer_id}.json")
    _out(ctx, r)

@cli.group()
def inventory():
    """Manage inventory levels."""

@inventory.command("list")
@click.option("--location-id", envvar="SHOPIFY_LOCATION_ID", default=None)
@click.option("--limit", default=50)
@click.pass_context
def inventory_list(ctx, location_id, limit):
    """List inventory levels."""
    qs = f"?limit={limit}" + (f"&location_ids={location_id}" if location_id else "")
    r = _req(ctx, "GET", f"/inventory_levels.json{qs}")
    _out(ctx, r)

if __name__ == "__main__":
    cli()
