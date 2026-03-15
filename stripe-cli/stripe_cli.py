"""
cli-anything-stripe — Stripe Payment API CLI
Wraps Stripe Python SDK for AI Agent use.
"""
import json
import sys
import os
from typing import Optional

import click

try:
    import stripe as stripe_sdk
    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False


def _setup(token: str):
    if not _SDK_AVAILABLE:
        raise click.ClickException("stripe SDK 未安装，请运行: pip install stripe")
    stripe_sdk.api_key = token


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("STRIPE_SECRET_KEY") or os.environ.get("STRIPE_API_KEY")
    if not t:
        raise click.ClickException(
            "未提供 Stripe Secret Key。\n"
            "方式1: --key sk_live_xxx 或 sk_test_xxx\n"
            "方式2: export STRIPE_SECRET_KEY=sk_test_xxx\n"
            "获取: https://dashboard.stripe.com/apikeys"
        )
    return t


def _out(data, as_json: bool):
    if as_json:
        if hasattr(data, "to_dict"):
            data = data.to_dict()
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if hasattr(data, "get"):
            click.echo(str(dict(data)) if not isinstance(data, dict) else str(data))
        else:
            click.echo(str(data))


def _stripe_err(fn):
    """Decorator to catch Stripe errors."""
    import functools
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if _SDK_AVAILABLE:
                try:
                    from stripe.error import StripeError
                    if isinstance(e, StripeError):
                        raise click.ClickException(f"Stripe 错误: {e.user_message or str(e)}")
                except ImportError:
                    pass
            raise
    return wrapper


@click.group()
@click.option("--key", envvar="STRIPE_SECRET_KEY", default=None, help="Stripe Secret Key (sk_live_... 或 sk_test_...)")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-stripe — Stripe 支付 API CLI\n
    管理客户、支付、订阅、发票、退款、优惠券等。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
def detect(ctx):
    """检测 Stripe API Key 有效性。"""
    as_json = ctx.obj["json"]
    if not _SDK_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install stripe"}
        _out(result, as_json) if as_json else click.echo("❌ stripe SDK 未安装")
        sys.exit(1)
    try:
        t = _token(ctx)
        _setup(t)
        account = stripe_sdk.Account.retrieve()
        result = {
            "status": "ok",
            "account_id": account.get("id"),
            "email": account.get("email"),
            "country": account.get("country"),
            "livemode": account.get("charges_enabled"),
            "key_mode": "live" if t.startswith("sk_live") else "test",
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Stripe OK  account={result['account_id']}  mode={result['key_mode']}")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示 Stripe SDK 版本信息。"""
    if not _SDK_AVAILABLE:
        raise click.ClickException("stripe SDK 未安装")
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    account = stripe_sdk.Account.retrieve()
    result = {"stripe_sdk_version": stripe_sdk.VERSION, "account_id": account.get("id"), "country": account.get("country")}
    _out(result, as_json) if as_json else click.echo(f"Stripe SDK {stripe_sdk.VERSION}  account={result['account_id']}")


# ── CUSTOMERS ─────────────────────────────────────────────────────────────────

@cli.group()
def customer():
    """客户管理（list / get / create / update / delete）。"""


@customer.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.option("--email", default=None, help="按 email 筛选")
@click.pass_context
def customer_list(ctx, limit, email):
    """列出客户。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs = {"limit": min(limit, 100)}
    if email:
        kwargs["email"] = email
    customers = stripe_sdk.Customer.list(**kwargs)
    data = [{"id": c.id, "email": c.email, "name": c.name, "created": c.created, "balance": c.balance} for c in customers.auto_paging_iter() if len(data := []) or True]
    # Re-do cleanly
    data = []
    for c in stripe_sdk.Customer.list(**kwargs).auto_paging_iter():
        data.append({"id": c.id, "email": c.email or "", "name": c.name or "", "created": c.created})
        if len(data) >= limit:
            break
    if as_json:
        _out({"customers": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':<22} {'EMAIL':<35} NAME")
        click.echo("─" * 75)
        for d in data:
            click.echo(f"{d['id']:<22} {d['email']:<35} {d['name']}")


@customer.command(name="get")
@click.argument("customer_id")
@click.pass_context
def customer_get(ctx, customer_id):
    """获取客户详情。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    c = stripe_sdk.Customer.retrieve(customer_id)
    result = {"id": c.id, "email": c.email, "name": c.name, "phone": c.phone, "created": c.created, "balance": c.balance, "currency": c.currency, "subscriptions": c.subscriptions.total_count if c.subscriptions else 0}
    _out(result, as_json) if as_json else click.echo("\n".join(f"  {k:<20} {v}" for k, v in result.items() if v is not None))


@customer.command(name="create")
@click.option("--email", required=True)
@click.option("--name", default=None)
@click.option("--phone", default=None)
@click.option("--description", default=None)
@click.pass_context
def customer_create(ctx, email, name, phone, description):
    """创建客户。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs = {"email": email}
    if name: kwargs["name"] = name
    if phone: kwargs["phone"] = phone
    if description: kwargs["description"] = description
    c = stripe_sdk.Customer.create(**kwargs)
    result = {"id": c.id, "email": c.email, "name": c.name}
    _out(result, as_json) if as_json else click.echo(f"✅ Customer: {c.id}  {c.email}")


@customer.command(name="delete")
@click.argument("customer_id")
@click.option("--yes", is_flag=True)
@click.pass_context
def customer_delete(ctx, customer_id, yes):
    """删除客户。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    if not yes:
        click.confirm(f"确认删除客户 {customer_id}？", abort=True)
    result = stripe_sdk.Customer.delete(customer_id)
    _out({"deleted": result.deleted, "id": customer_id}, as_json) if as_json else click.echo(f"🗑  Deleted: {customer_id}")


# ── PAYMENTS ─────────────────────────────────────────────────────────────────

@cli.group()
def payment():
    """支付意图（list / get / create / confirm / cancel）。"""


@payment.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.option("--customer", default=None, help="按客户 ID 筛选")
@click.pass_context
def payment_list(ctx, limit, customer):
    """列出 PaymentIntents。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs = {"limit": min(limit, 100)}
    if customer:
        kwargs["customer"] = customer
    pis = stripe_sdk.PaymentIntent.list(**kwargs)
    data = []
    for pi in pis.auto_paging_iter():
        data.append({"id": pi.id, "amount": pi.amount, "currency": pi.currency, "status": pi.status, "customer": pi.customer})
        if len(data) >= limit:
            break
    if as_json:
        _out({"payments": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':<30} {'AMOUNT':>10}  {'CURRENCY':<8} STATUS")
        click.echo("─" * 70)
        for d in data:
            click.echo(f"{d['id']:<30} {d['amount']:>10}  {d['currency']:<8} {d['status']}")


@payment.command(name="create")
@click.option("--amount", required=True, type=int, help="金额（最小单位，如分）")
@click.option("--currency", default="usd", show_default=True)
@click.option("--customer", default=None, help="客户 ID")
@click.option("--description", default=None)
@click.option("--auto-confirm", is_flag=True, help="自动确认（需要 payment_method）")
@click.option("--payment-method", default=None, help="支付方式 ID（pm_xxx）")
@click.pass_context
def payment_create(ctx, amount, currency, customer, description, auto_confirm, payment_method):
    """创建 PaymentIntent。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs: dict = {"amount": amount, "currency": currency, "automatic_payment_methods": {"enabled": True}}
    if customer: kwargs["customer"] = customer
    if description: kwargs["description"] = description
    if auto_confirm and payment_method:
        kwargs["payment_method"] = payment_method
        kwargs["confirm"] = True
    pi = stripe_sdk.PaymentIntent.create(**kwargs)
    result = {"id": pi.id, "client_secret": pi.client_secret, "status": pi.status, "amount": pi.amount, "currency": pi.currency}
    _out(result, as_json) if as_json else click.echo(f"✅ PaymentIntent: {pi.id}  status={pi.status}  {pi.amount} {pi.currency}")


# ── SUBSCRIPTIONS ─────────────────────────────────────────────────────────────

@cli.group()
def subscription():
    """订阅管理（list / get / cancel）。"""


@subscription.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.option("--customer", default=None)
@click.option("--status", default=None, type=click.Choice(["active", "past_due", "canceled", "trialing", "all"]))
@click.pass_context
def subscription_list(ctx, limit, customer, status):
    """列出订阅。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs: dict = {"limit": min(limit, 100)}
    if customer: kwargs["customer"] = customer
    if status and status != "all": kwargs["status"] = status
    subs = stripe_sdk.Subscription.list(**kwargs)
    data = []
    for s in subs.auto_paging_iter():
        data.append({"id": s.id, "customer": s.customer, "status": s.status, "current_period_end": s.current_period_end, "items": len(s.items.data)})
        if len(data) >= limit:
            break
    if as_json:
        _out({"subscriptions": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':<30} {'STATUS':<12} {'CUSTOMER':<25} PERIOD END")
        click.echo("─" * 90)
        for d in data:
            import datetime
            end = datetime.datetime.fromtimestamp(d["current_period_end"]).strftime("%Y-%m-%d") if d["current_period_end"] else ""
            click.echo(f"{d['id']:<30} {d['status']:<12} {(d['customer'] or ''):<25} {end}")


@subscription.command(name="cancel")
@click.argument("subscription_id")
@click.option("--at-period-end", is_flag=True, help="在当前周期结束时取消（非立即）")
@click.pass_context
def subscription_cancel(ctx, subscription_id, at_period_end):
    """取消订阅。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    if at_period_end:
        sub = stripe_sdk.Subscription.modify(subscription_id, cancel_at_period_end=True)
    else:
        sub = stripe_sdk.Subscription.delete(subscription_id)
    result = {"id": sub.id, "status": sub.status, "cancel_at_period_end": sub.cancel_at_period_end}
    _out(result, as_json) if as_json else click.echo(f"✅ Subscription {subscription_id} cancel_at_period_end={sub.cancel_at_period_end}")


# ── REFUNDS ───────────────────────────────────────────────────────────────────

@cli.group()
def refund():
    """退款管理（list / create）。"""


@refund.command(name="create")
@click.argument("payment_intent_id")
@click.option("--amount", default=None, type=int, help="退款金额（不填=全额退款）")
@click.option("--reason", default=None, type=click.Choice(["duplicate", "fraudulent", "requested_by_customer"]))
@click.pass_context
def refund_create(ctx, payment_intent_id, amount, reason):
    """创建退款。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs: dict = {"payment_intent": payment_intent_id}
    if amount: kwargs["amount"] = amount
    if reason: kwargs["reason"] = reason
    r = stripe_sdk.Refund.create(**kwargs)
    result = {"id": r.id, "amount": r.amount, "currency": r.currency, "status": r.status}
    _out(result, as_json) if as_json else click.echo(f"✅ Refund: {r.id}  {r.amount} {r.currency}  status={r.status}")


@refund.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.option("--payment-intent", default=None)
@click.pass_context
def refund_list(ctx, limit, payment_intent):
    """列出退款记录。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs: dict = {"limit": min(limit, 100)}
    if payment_intent: kwargs["payment_intent"] = payment_intent
    refunds = stripe_sdk.Refund.list(**kwargs)
    data = []
    for r in refunds.auto_paging_iter():
        data.append({"id": r.id, "amount": r.amount, "currency": r.currency, "status": r.status, "payment_intent": r.payment_intent})
        if len(data) >= limit: break
    if as_json:
        _out({"refunds": data, "count": len(data)}, True)
    else:
        for d in data:
            click.echo(f"{d['id']}  {d['amount']} {d['currency']}  {d['status']}")


# ── PRODUCTS & PRICES ─────────────────────────────────────────────────────────

@cli.group()
def product():
    """产品管理（list / create / get）。"""


@product.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.option("--active", "active_only", is_flag=True, default=False)
@click.pass_context
def product_list(ctx, limit, active_only):
    """列出产品。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs: dict = {"limit": min(limit, 100)}
    if active_only: kwargs["active"] = True
    products = stripe_sdk.Product.list(**kwargs)
    data = []
    for p in products.auto_paging_iter():
        data.append({"id": p.id, "name": p.name, "active": p.active, "description": (p.description or "")[:60]})
        if len(data) >= limit: break
    if as_json:
        _out({"products": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':<22} {'ACTIVE':<8} NAME")
        click.echo("─" * 70)
        for d in data:
            click.echo(f"{d['id']:<22} {str(d['active']):<8} {d['name']}")


@product.command(name="create")
@click.option("--name", required=True)
@click.option("--description", default=None)
@click.option("--price", default=None, type=int, help="一次性价格（最小单位）")
@click.option("--currency", default="usd")
@click.pass_context
def product_create(ctx, name, description, price, currency):
    """创建产品（可附带一次性价格）。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    kwargs: dict = {"name": name}
    if description: kwargs["description"] = description
    p = stripe_sdk.Product.create(**kwargs)
    result = {"id": p.id, "name": p.name}
    if price:
        price_obj = stripe_sdk.Price.create(unit_amount=price, currency=currency, product=p.id)
        result["price_id"] = price_obj.id
        result["price_amount"] = price
    _out(result, as_json) if as_json else click.echo(f"✅ Product: {p.id}  {p.name}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-stripe",
        "version": "1.0.0",
        "description": "Stripe Payment API CLI - customers, payments, subscriptions, refunds, products via Stripe SDK",
        "requires_token": True,
        "token_env": "STRIPE_SECRET_KEY",
        "token_hint": "sk_test_... or sk_live_... from https://dashboard.stripe.com/apikeys",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Verify API key and show account info"},
            {"cmd": "version", "args": [], "desc": "Show Stripe SDK version and account"},
            {"cmd": "customer list", "args": [{"name": "--limit", "type": "int", "default": 10}, {"name": "--email", "type": "str"}], "desc": "List customers"},
            {"cmd": "customer get", "args": [{"name": "CUSTOMER_ID", "type": "str"}], "desc": "Get customer details"},
            {"cmd": "customer create", "args": [{"name": "--email", "type": "str", "required": True}, {"name": "--name", "type": "str"}, {"name": "--phone", "type": "str"}], "desc": "Create customer"},
            {"cmd": "customer delete", "args": [{"name": "CUSTOMER_ID", "type": "str"}, {"name": "--yes", "type": "flag"}], "desc": "Delete customer"},
            {"cmd": "payment list", "args": [{"name": "--limit", "type": "int", "default": 10}, {"name": "--customer", "type": "str"}], "desc": "List PaymentIntents"},
            {"cmd": "payment create", "args": [{"name": "--amount", "type": "int", "required": True}, {"name": "--currency", "type": "str", "default": "usd"}, {"name": "--customer", "type": "str"}], "desc": "Create PaymentIntent"},
            {"cmd": "subscription list", "args": [{"name": "--limit", "type": "int", "default": 10}, {"name": "--customer", "type": "str"}, {"name": "--status", "type": "str"}], "desc": "List subscriptions"},
            {"cmd": "subscription cancel", "args": [{"name": "SUBSCRIPTION_ID", "type": "str"}, {"name": "--at-period-end", "type": "flag"}], "desc": "Cancel subscription"},
            {"cmd": "refund create", "args": [{"name": "PAYMENT_INTENT_ID", "type": "str"}, {"name": "--amount", "type": "int"}, {"name": "--reason", "type": "str"}], "desc": "Create refund"},
            {"cmd": "refund list", "args": [{"name": "--limit", "type": "int", "default": 10}, {"name": "--payment-intent", "type": "str"}], "desc": "List refunds"},
            {"cmd": "product list", "args": [{"name": "--limit", "type": "int", "default": 10}, {"name": "--active", "type": "flag"}], "desc": "List products"},
            {"cmd": "product create", "args": [{"name": "--name", "type": "str", "required": True}, {"name": "--price", "type": "int"}, {"name": "--currency", "type": "str", "default": "usd"}], "desc": "Create product with optional price"},
        ],
        "json_flag": "--json",
        "example": "stripe-cli --key sk_test_xxx --json customer list --limit 5",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
