"""
cli-anything-robinhood — Robinhood Trading API CLI
Wraps unofficial Robinhood REST API for AI Agent use.
"""
import json
import sys
import os
import functools
from typing import Optional
from datetime import datetime, timedelta

import click

try:
    import requests
    _HTTP_AVAILABLE = True
except ImportError:
    _HTTP_AVAILABLE = False

_BASE = "https://api.robinhood.com"


def _setup(token: str):
    if not _HTTP_AVAILABLE:
        raise click.ClickException("requests 未安装，请运行: pip install requests")
    return token


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("ROBINHOOD_TOKEN")
    if not t:
        raise click.ClickException(
            "未提供 Robinhood Token。\n"
            "方式1: --key YOUR_BEARER_TOKEN\n"
            "方式2: export ROBINHOOD_TOKEN=YOUR_BEARER_TOKEN\n"
            "说明: 需要通过 Robinhood OAuth 流程获取 Bearer Token"
        )
    return t


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if isinstance(data, dict):
            click.echo(str(data))
        else:
            click.echo(str(data))


def _err(fn):
    """统一捕获 Robinhood API 错误。"""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"Robinhood 请求错误: {e}")
        except KeyError as e:
            raise click.ClickException(f"Robinhood 响应解析错误: 缺少字段 {e}")
    return wrapper


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _get(endpoint: str, token: str, **params) -> dict:
    """发送 GET 请求到 Robinhood API。"""
    url = f"{_BASE}/{endpoint.lstrip('/')}"
    resp = requests.get(url, headers=_headers(token), params=params, timeout=30)
    if resp.status_code == 401:
        raise click.ClickException("认证失败: Token 无效或已过期，请重新获取 Bearer Token")
    if resp.status_code != 200:
        raise click.ClickException(f"Robinhood API 错误 ({resp.status_code}): {resp.text[:300]}")
    return resp.json()


def _post(endpoint: str, token: str, payload: dict) -> dict:
    """发送 POST 请求到 Robinhood API。"""
    url = f"{_BASE}/{endpoint.lstrip('/')}"
    resp = requests.post(url, headers=_headers(token), json=payload, timeout=30)
    if resp.status_code == 401:
        raise click.ClickException("认证失败: Token 无效或已过期")
    if resp.status_code not in (200, 201):
        raise click.ClickException(f"Robinhood API 错误 ({resp.status_code}): {resp.text[:300]}")
    return resp.json()


@click.group()
@click.option("--key", envvar="ROBINHOOD_TOKEN", default=None, help="Robinhood OAuth Bearer Token")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-robinhood — Robinhood 交易 CLI\n
    查询持仓、报价、下单、历史等。\n
    ⚠️  使用非官方 API，请谨慎操作真实资金。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
@_err
def detect(ctx):
    """检测 Robinhood Token 有效性。"""
    as_json = ctx.obj["json"]
    if not _HTTP_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install requests"}
        _out(result, as_json) if as_json else click.echo("❌ requests 未安装")
        sys.exit(1)
    try:
        t = _token(ctx)
        _setup(t)
        data = _get("/user/", t)
        result = {
            "status": "ok",
            "username": data.get("username"),
            "email": data.get("email"),
            "id": data.get("id"),
            "api": "Robinhood (unofficial)",
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Robinhood OK  user={result['username']}  email={result['email']}")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {
        "cli": "cli-anything-robinhood",
        "version": "1.0.0",
        "api": "Robinhood (unofficial REST API)",
        "base_url": _BASE,
        "warning": "Unofficial API - use at your own risk",
    }
    _out(result, as_json) if as_json else click.echo("cli-anything-robinhood v1.0.0  api=Robinhood (unofficial)")


# ── PORTFOLIO ────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
@_err
def portfolio(ctx):
    """获取投资组合摘要。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    data = _get("/portfolios/", t)
    results = data.get("results", [])
    if not results:
        raise click.ClickException("未找到投资组合数据")
    p = results[0]
    result = {
        "equity": p.get("equity"),
        "extended_hours_equity": p.get("extended_hours_equity"),
        "market_value": p.get("market_value"),
        "excess_margin": p.get("excess_margin"),
        "last_core_equity": p.get("last_core_equity"),
        "withdrawable_amount": p.get("withdrawable_amount"),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo("📊 投资组合摘要")
        click.echo("─" * 40)
        for k, v in result.items():
            if v is not None:
                click.echo(f"  {k:<30} ${v}")


# ── POSITIONS ────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
@_err
def positions(ctx):
    """列出当前持仓（仅非零）。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    data = _get("/positions/", t, nonzero="true")
    results = data.get("results", [])
    rows = []
    for pos in results:
        instrument_url = pos.get("instrument", "")
        rows.append({
            "instrument": instrument_url,
            "quantity": pos.get("quantity"),
            "average_buy_price": pos.get("average_buy_price"),
            "equity": pos.get("equity"),
            "percent_change": pos.get("percent_change"),
            "equity_change": pos.get("equity_change"),
        })
    if as_json:
        _out({"positions": rows, "count": len(rows)}, True)
    else:
        click.echo(f"{'QTY':<10} {'AVG PRICE':<14} {'EQUITY':<14} CHG")
        click.echo("─" * 55)
        for r in rows:
            click.echo(f"{r['quantity']:<10} ${r['average_buy_price'] or '?':<13} ${r['equity'] or '?':<13} {r['percent_change'] or 'N/A'}")
        click.echo(f"\n共 {len(rows)} 个持仓")


# ── QUOTE ────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--symbols", required=True, help="股票代码，逗号分隔（如 AAPL,TSLA,MSFT）")
@click.pass_context
@_err
def quote(ctx, symbols):
    """获取股票报价。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    data = _get("/quotes/", t, symbols=symbols.upper())
    results = data.get("results", [])
    rows = []
    for q in results:
        if q is None:
            continue
        rows.append({
            "symbol": q.get("symbol"),
            "last_trade_price": q.get("last_trade_price"),
            "bid_price": q.get("bid_price"),
            "ask_price": q.get("ask_price"),
            "previous_close": q.get("previous_close"),
            "updated_at": q.get("updated_at"),
        })
    if as_json:
        _out({"quotes": rows, "count": len(rows)}, True)
    else:
        click.echo(f"{'SYMBOL':<8} {'LAST':<12} {'BID':<12} {'ASK':<12} PREV CLOSE")
        click.echo("─" * 60)
        for r in rows:
            click.echo(f"{r['symbol']:<8} ${r['last_trade_price'] or '?':<11} ${r['bid_price'] or '?':<11} ${r['ask_price'] or '?':<11} ${r['previous_close'] or '?'}")


# ── ORDERS ───────────────────────────────────────────────────────────────────

@cli.group()
def order():
    """订单管理（list / buy / sell）。\n
    ⚠️  交易命令涉及真实资金，请谨慎操作！
    """


@order.command(name="list")
@click.option("--days", default=7, show_default=True, type=int, help="最近几天的订单")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
@_err
def order_list(ctx, days, limit):
    """列出最近订单。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    since = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
    data = _get("/orders/", t, **{"updated_at[gte]": since})
    results = data.get("results", [])[:limit]
    rows = []
    for o in results:
        rows.append({
            "id": o.get("id"),
            "side": o.get("side"),
            "type": o.get("type"),
            "quantity": o.get("quantity"),
            "price": o.get("price"),
            "state": o.get("state"),
            "created_at": o.get("created_at"),
        })
    if as_json:
        _out({"orders": rows, "count": len(rows)}, True)
    else:
        click.echo(f"{'SIDE':<6} {'TYPE':<8} {'QTY':<8} {'PRICE':<12} {'STATE':<12} CREATED")
        click.echo("─" * 70)
        for r in rows:
            click.echo(f"{(r['side'] or ''):<6} {(r['type'] or ''):<8} {r['quantity']:<8} ${r['price'] or '?':<11} {(r['state'] or ''):<12} {(r['created_at'] or '')[:16]}")


def _place_order(ctx, symbol, qty, side, order_type, price, dry_run):
    """内部下单逻辑。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]

    click.echo(f"⚠️  警告: 即将提交 {side.upper()} 订单", err=True)
    click.echo(f"   股票: {symbol}  数量: {qty}  类型: {order_type}  价格: {price or 'market'}", err=True)
    click.echo("   ⚠️  此操作使用非官方 API，可能影响您的真实资金！", err=True)

    if dry_run:
        result = {
            "dry_run": True,
            "side": side,
            "symbol": symbol,
            "quantity": qty,
            "type": order_type,
            "price": price,
            "message": "模拟运行 - 未实际提交订单",
        }
        _out(result, as_json) if as_json else click.echo(f"🧪 DRY RUN: {side} {qty}x {symbol} ({order_type}) — 未实际下单")
        return

    instrument_data = _get(f"/instruments/", t, symbol=symbol.upper())
    instruments = instrument_data.get("results", [])
    if not instruments:
        raise click.ClickException(f"未找到股票: {symbol}")
    instrument_url = instruments[0]["url"]

    payload = {
        "account": _get("/accounts/", t)["results"][0]["url"],
        "instrument": instrument_url,
        "symbol": symbol.upper(),
        "quantity": qty,
        "side": side,
        "type": order_type,
        "time_in_force": "gfd",
        "trigger": "immediate",
    }
    if order_type == "limit" and price:
        payload["price"] = price
    elif order_type == "market":
        payload["price"] = None

    result = _post("/orders/", t, payload)
    out = {
        "id": result.get("id"),
        "side": result.get("side"),
        "symbol": symbol,
        "quantity": result.get("quantity"),
        "type": result.get("type"),
        "state": result.get("state"),
        "price": result.get("price"),
    }
    _out(out, as_json) if as_json else click.echo(f"✅ 订单已提交: {out['id']}  {side} {qty}x {symbol}  state={out['state']}")


@order.command(name="buy")
@click.option("--symbol", required=True, help="股票代码")
@click.option("--qty", required=True, type=float, help="数量")
@click.option("--type", "order_type", default="market", type=click.Choice(["market", "limit"]), show_default=True)
@click.option("--price", default=None, type=float, help="限价单价格")
@click.option("--dry-run", is_flag=True, help="模拟运行，不实际下单")
@click.pass_context
@_err
def order_buy(ctx, symbol, qty, order_type, price, dry_run):
    """买入股票。\n
    ⚠️  此操作可能影响您的真实资金！建议先使用 --dry-run 测试。
    """
    _place_order(ctx, symbol, qty, "buy", order_type, price, dry_run)


@order.command(name="sell")
@click.option("--symbol", required=True, help="股票代码")
@click.option("--qty", required=True, type=float, help="数量")
@click.option("--type", "order_type", default="market", type=click.Choice(["market", "limit"]), show_default=True)
@click.option("--price", default=None, type=float, help="限价单价格")
@click.option("--dry-run", is_flag=True, help="模拟运行，不实际下单")
@click.pass_context
@_err
def order_sell(ctx, symbol, qty, order_type, price, dry_run):
    """卖出股票。\n
    ⚠️  此操作可能影响您的真实资金！建议先使用 --dry-run 测试。
    """
    _place_order(ctx, symbol, qty, "sell", order_type, price, dry_run)


# ── HISTORY ──────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--span", default="week", type=click.Choice(["day", "week", "month", "3month", "year", "all"]), show_default=True)
@click.pass_context
@_err
def history(ctx, span):
    """获取账户历史走势。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    interval_map = {"day": "5minute", "week": "10minute", "month": "day", "3month": "day", "year": "week", "all": "week"}
    interval = interval_map.get(span, "day")
    data = _get("/portfolios/historicals/aggregate/", t, span=span, interval=interval)
    equities = data.get("equity_historicals", [])
    rows = [
        {
            "begins_at": e.get("begins_at"),
            "open_equity": e.get("open_equity"),
            "close_equity": e.get("close_equity"),
            "adjusted_open_equity": e.get("adjusted_open_equity"),
            "adjusted_close_equity": e.get("adjusted_close_equity"),
        }
        for e in equities
    ]
    if as_json:
        _out({"span": span, "interval": interval, "data_points": len(rows), "history": rows}, True)
    else:
        click.echo(f"📈 账户历史 (span={span}, interval={interval})")
        click.echo(f"{'TIME':<28} {'OPEN':<14} CLOSE")
        click.echo("─" * 60)
        for r in rows[-20:]:
            click.echo(f"{(r['begins_at'] or ''):<28} ${r['open_equity'] or '?':<13} ${r['close_equity'] or '?'}")
        if len(rows) > 20:
            click.echo(f"... 显示最近 20 / {len(rows)} 条")


# ── WATCHLIST ────────────────────────────────────────────────────────────────

@cli.group()
def watchlist():
    """自选列表（list）。"""


@watchlist.command(name="list")
@click.pass_context
@_err
def watchlist_list(ctx):
    """列出所有自选列表。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    data = _get("/watchlists/", t)
    results = data.get("results", [])
    rows = [{"name": w.get("name"), "url": w.get("url")} for w in results]
    if as_json:
        _out({"watchlists": rows, "count": len(rows)}, True)
    else:
        click.echo("📋 自选列表")
        click.echo("─" * 40)
        for r in rows:
            click.echo(f"  {r['name']}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-robinhood",
        "version": "1.0.0",
        "description": "Robinhood Trading CLI (unofficial API) - portfolio, positions, quotes, orders, history",
        "requires_token": True,
        "token_env": "ROBINHOOD_TOKEN",
        "token_hint": "OAuth Bearer Token from Robinhood authentication flow",
        "warning": "Uses unofficial Robinhood API. Use at your own risk with real money.",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Verify token and show user info"},
            {"cmd": "version", "args": [], "desc": "Show CLI version info"},
            {"cmd": "portfolio", "args": [], "desc": "Get portfolio summary"},
            {"cmd": "positions", "args": [], "desc": "List non-zero positions"},
            {"cmd": "quote", "args": [{"name": "--symbols", "type": "str", "required": True, "desc": "Comma-separated symbols"}], "desc": "Get stock quotes"},
            {"cmd": "order list", "args": [
                {"name": "--days", "type": "int", "default": 7},
                {"name": "--limit", "type": "int", "default": 20},
            ], "desc": "List recent orders"},
            {"cmd": "order buy", "args": [
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--qty", "type": "float", "required": True},
                {"name": "--type", "type": "str", "default": "market", "choices": ["market", "limit"]},
                {"name": "--price", "type": "float"},
                {"name": "--dry-run", "type": "flag"},
            ], "desc": "Place buy order (⚠️ real money)"},
            {"cmd": "order sell", "args": [
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--qty", "type": "float", "required": True},
                {"name": "--type", "type": "str", "default": "market", "choices": ["market", "limit"]},
                {"name": "--price", "type": "float"},
                {"name": "--dry-run", "type": "flag"},
            ], "desc": "Place sell order (⚠️ real money)"},
            {"cmd": "history", "args": [{"name": "--span", "type": "str", "default": "week", "choices": ["day", "week", "month", "3month", "year", "all"]}], "desc": "Account equity history"},
            {"cmd": "watchlist list", "args": [], "desc": "List watchlists"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-robinhood --json quote --symbols AAPL,TSLA",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
