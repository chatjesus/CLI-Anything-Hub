"""
cli-anything-kalshi — Kalshi 预测市场交易 API CLI
通过 Kalshi Trading API v2 查询市场、下单、管理仓位和投资组合。
"""
import json
import sys
import os
import functools
from typing import Optional

import click
import requests

_BASE_URL = "https://trading-api.kalshi.com/trade-api/v2"
_VERSION = "1.0.0"


def _setup(token: str) -> dict:
    """返回带认证的 headers。"""
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("KALSHI_API_KEY")
    if t:
        return t
    email = os.environ.get("KALSHI_EMAIL")
    password = os.environ.get("KALSHI_PASSWORD")
    if email and password:
        try:
            resp = requests.post(
                f"{_BASE_URL}/login",
                json={"email": email, "password": password},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("token", data.get("access_token", ""))
        except Exception as e:
            raise click.ClickException(f"Kalshi 登录失败: {e}")
    raise click.ClickException(
        "未提供 Kalshi 认证信息。\n"
        "方式1: --key YOUR_API_TOKEN\n"
        "方式2: export KALSHI_API_KEY=your_token\n"
        "方式3: export KALSHI_EMAIL=xxx && export KALSHI_PASSWORD=xxx\n"
        "获取: https://kalshi.com/sign-up"
    )


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if isinstance(data, dict):
            click.echo(str(data))
        elif isinstance(data, list):
            for item in data:
                click.echo(str(item))
        else:
            click.echo(str(data))


def _err(fn):
    """捕获 requests 异常的装饰器。"""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"API 请求错误: {e}")
        except json.JSONDecodeError as e:
            raise click.ClickException(f"JSON 解析错误: {e}")
    return wrapper


@click.group()
@click.option("--key", envvar="KALSHI_API_KEY", default=None, help="Kalshi API Token")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-kalshi — Kalshi 预测市场交易 CLI\n
    查询市场、下单、管理仓位和投资组合。支持 --json 结构化输出。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
@_err
def detect(ctx):
    """检测 Kalshi API 连通性。"""
    as_json = ctx.obj["json"]
    try:
        resp = requests.get(f"{_BASE_URL}/exchange/status", timeout=10)
        resp.raise_for_status()
        status_data = resp.json()
        result = {
            "status": "ok",
            "base_url": _BASE_URL,
            "http_status": resp.status_code,
            "exchange_active": status_data.get("exchange_active", status_data.get("trading_active")),
        }
        has_key = bool(ctx.obj.get("token") or os.environ.get("KALSHI_API_KEY")
                       or (os.environ.get("KALSHI_EMAIL") and os.environ.get("KALSHI_PASSWORD")))
        result["auth"] = "configured" if has_key else "not_configured"
        if as_json:
            _out(result, True)
        else:
            auth_status = "✅" if has_key else "⚠️  未配置"
            click.echo(f"✅ Kalshi API 连通正常  auth={auth_status}")
    except Exception as e:
        result = {"status": "error", "error": str(e)}
        _out(result, as_json) if as_json else click.echo(f"❌ Kalshi API 连接失败: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {"cli": "cli-anything-kalshi", "version": _VERSION, "api_base": _BASE_URL}
    _out(result, as_json) if as_json else click.echo(f"cli-anything-kalshi v{_VERSION}  api={_BASE_URL}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-kalshi",
        "version": _VERSION,
        "description": "Kalshi 预测市场交易 API CLI - 查询市场、下单、管理仓位和投资组合",
        "requires_token": True,
        "token_env": "KALSHI_API_KEY",
        "token_hint": "Kalshi API token 或通过 KALSHI_EMAIL + KALSHI_PASSWORD 登录",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Check API connectivity"},
            {"cmd": "version", "args": [], "desc": "Show version info"},
            {"cmd": "market list", "args": [
                {"name": "--limit", "type": "int", "default": 10},
                {"name": "--status", "type": "str", "choices": ["active", "closed"]},
            ], "desc": "List events/markets"},
            {"cmd": "market get", "args": [
                {"name": "TICKER", "type": "str", "required": True},
            ], "desc": "Get market by ticker"},
            {"cmd": "market search", "args": [
                {"name": "--query", "type": "str", "required": True},
                {"name": "--limit", "type": "int", "default": 10},
            ], "desc": "Search markets by query"},
            {"cmd": "orderbook", "args": [
                {"name": "TICKER", "type": "str", "required": True},
                {"name": "--depth", "type": "int", "default": 10},
            ], "desc": "Get orderbook for a ticker"},
            {"cmd": "order place", "args": [
                {"name": "--ticker", "type": "str", "required": True},
                {"name": "--side", "type": "str", "required": True, "choices": ["yes", "no"]},
                {"name": "--qty", "type": "int", "required": True},
                {"name": "--price", "type": "int", "required": True},
            ], "desc": "Place order"},
            {"cmd": "order list", "args": [
                {"name": "--limit", "type": "int", "default": 10},
                {"name": "--ticker", "type": "str"},
            ], "desc": "List user orders"},
            {"cmd": "position list", "args": [
                {"name": "--limit", "type": "int", "default": 10},
            ], "desc": "List user positions"},
            {"cmd": "portfolio", "args": [], "desc": "Portfolio summary"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-kalshi --key xxx --json market list --limit 5",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── MARKET ──────────────────────────────────────────────────────────────────

@cli.group()
def market():
    """市场查询（list / get / search）。"""


@market.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int, help="返回数量")
@click.option("--status", default=None, type=click.Choice(["active", "closed"]), help="按状态筛选")
@click.pass_context
@_err
def market_list(ctx, limit, status):
    """列出市场/事件。"""
    as_json = ctx.obj["json"]
    params = {"limit": min(limit, 100)}
    if status:
        params["status"] = status
    resp = requests.get(f"{_BASE_URL}/events", params=params, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    events = raw.get("events", raw.get("data", []))
    data = []
    for e in events[:limit]:
        data.append({
            "event_ticker": e.get("event_ticker", ""),
            "title": e.get("title", ""),
            "category": e.get("category", ""),
            "status": e.get("status", ""),
            "markets_count": len(e.get("markets", [])),
        })
    if as_json:
        _out({"events": data, "count": len(data)}, True)
    else:
        click.echo(f"{'TICKER':<25} {'STATUS':<10} {'CAT':<15} TITLE")
        click.echo("─" * 85)
        for d in data:
            click.echo(f"{d['event_ticker']:<25} {d['status']:<10} {d['category']:<15} {d['title'][:40]}")


@market.command(name="get")
@click.argument("ticker")
@click.pass_context
@_err
def market_get(ctx, ticker):
    """获取市场详情（按 ticker）。"""
    as_json = ctx.obj["json"]
    resp = requests.get(f"{_BASE_URL}/markets/{ticker}", timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    m = raw.get("market", raw)
    result = {
        "ticker": m.get("ticker", ""),
        "event_ticker": m.get("event_ticker", ""),
        "title": m.get("title", m.get("subtitle", "")),
        "status": m.get("status", ""),
        "yes_bid": m.get("yes_bid", ""),
        "yes_ask": m.get("yes_ask", ""),
        "no_bid": m.get("no_bid", ""),
        "no_ask": m.get("no_ask", ""),
        "volume": m.get("volume", 0),
        "open_interest": m.get("open_interest", 0),
        "close_time": m.get("close_time", ""),
        "result": m.get("result", ""),
    }
    if as_json:
        _out(result, True)
    else:
        for k, v in result.items():
            if v is not None and v != "" and v != 0:
                click.echo(f"  {k:<20} {v}")


@market.command(name="search")
@click.option("--query", required=True, help="搜索关键词")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
@_err
def market_search(ctx, query, limit):
    """按关键词搜索市场。"""
    as_json = ctx.obj["json"]
    params = {"limit": min(limit, 100), "status": "active"}
    resp = requests.get(f"{_BASE_URL}/events", params=params, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    events = raw.get("events", raw.get("data", []))
    kw_lower = query.lower()
    filtered = [
        e for e in events
        if kw_lower in (e.get("title", "") + e.get("category", "")).lower()
    ][:limit]
    data = []
    for e in filtered:
        data.append({
            "event_ticker": e.get("event_ticker", ""),
            "title": e.get("title", ""),
            "category": e.get("category", ""),
            "status": e.get("status", ""),
        })
    if as_json:
        _out({"results": data, "count": len(data), "query": query}, True)
    else:
        click.echo(f"搜索 '{query}' — 找到 {len(data)} 条结果")
        click.echo("─" * 60)
        for d in data:
            click.echo(f"  [{d['event_ticker']}] {d['title'][:60]}")


# ── ORDERBOOK ──────────────────────────────────────────────────────────────

@cli.command()
@click.argument("ticker")
@click.option("--depth", default=10, show_default=True, type=int, help="深度")
@click.pass_context
@_err
def orderbook(ctx, ticker, depth):
    """获取某个 ticker 的订单簿。"""
    as_json = ctx.obj["json"]
    params = {"depth": depth}
    resp = requests.get(f"{_BASE_URL}/orderbooks/{ticker}", params=params, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    ob = raw.get("orderbook", raw)
    result = {
        "ticker": ticker,
        "yes": ob.get("yes", []),
        "no": ob.get("no", []),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"订单簿: {ticker}")
        click.echo(f"\n  YES 方向:")
        for level in (result["yes"] or [])[:depth]:
            if isinstance(level, list) and len(level) >= 2:
                click.echo(f"    价格: {level[0]}  数量: {level[1]}")
            elif isinstance(level, dict):
                click.echo(f"    价格: {level.get('price', '')}  数量: {level.get('quantity', level.get('size', ''))}")
        click.echo(f"\n  NO 方向:")
        for level in (result["no"] or [])[:depth]:
            if isinstance(level, list) and len(level) >= 2:
                click.echo(f"    价格: {level[0]}  数量: {level[1]}")
            elif isinstance(level, dict):
                click.echo(f"    价格: {level.get('price', '')}  数量: {level.get('quantity', level.get('size', ''))}")


# ── ORDER ──────────────────────────────────────────────────────────────────

@cli.group()
def order():
    """订单管理（place / list）。"""


@order.command(name="place")
@click.option("--ticker", required=True, help="市场 ticker")
@click.option("--side", required=True, type=click.Choice(["yes", "no"]), help="Yes 或 No")
@click.option("--qty", required=True, type=int, help="合约数量")
@click.option("--price", required=True, type=int, help="价格（1-99 美分）")
@click.pass_context
@_err
def order_place(ctx, ticker, side, qty, price):
    """下单。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    if price < 1 or price > 99:
        raise click.ClickException("价格必须在 1 到 99 之间（美分）")
    payload = {
        "ticker": ticker,
        "side": side,
        "count": qty,
        "type": "limit",
        "yes_price": price if side == "yes" else None,
        "no_price": price if side == "no" else None,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    resp = requests.post(f"{_BASE_URL}/portfolio/orders", json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    result = resp.json()
    order_data = result.get("order", result)
    if as_json:
        _out(order_data, True)
    else:
        oid = order_data.get("order_id", order_data.get("id", "unknown"))
        click.echo(f"✅ 订单已提交  order_id={oid}  {side} {qty}x @ {price}¢  ticker={ticker}")


@order.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.option("--ticker", default=None, help="按 ticker 筛选")
@click.pass_context
@_err
def order_list(ctx, limit, ticker):
    """列出用户订单。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    params = {"limit": min(limit, 100)}
    if ticker:
        params["ticker"] = ticker
    resp = requests.get(f"{_BASE_URL}/portfolio/orders", params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    orders = raw.get("orders", raw.get("data", []))
    data = []
    for o in orders[:limit]:
        data.append({
            "order_id": o.get("order_id", o.get("id", "")),
            "ticker": o.get("ticker", ""),
            "side": o.get("side", ""),
            "type": o.get("type", ""),
            "price": o.get("yes_price", o.get("no_price", "")),
            "count": o.get("remaining_count", o.get("count", "")),
            "status": o.get("status", ""),
        })
    if as_json:
        _out({"orders": data, "count": len(data)}, True)
    else:
        if not data:
            click.echo("暂无订单")
            return
        click.echo(f"{'ORDER_ID':<20} {'TICKER':<18} {'SIDE':<6} {'PRICE':>6} {'QTY':>5} STATUS")
        click.echo("─" * 75)
        for d in data:
            click.echo(f"{str(d['order_id'])[:18]:<20} {d['ticker']:<18} {d['side']:<6} {str(d['price']):>6} {str(d['count']):>5} {d['status']}")


# ── POSITION ───────────────────────────────────────────────────────────────

@cli.group()
def position():
    """仓位管理（list）。"""


@position.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
@_err
def position_list(ctx, limit):
    """列出持仓。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    params = {"limit": min(limit, 100)}
    resp = requests.get(f"{_BASE_URL}/portfolio/positions", params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    positions = raw.get("market_positions", raw.get("positions", raw.get("data", [])))
    data = []
    for p in positions[:limit]:
        data.append({
            "ticker": p.get("ticker", p.get("market_ticker", "")),
            "position": p.get("position", 0),
            "market_exposure": p.get("market_exposure", 0),
            "realized_pnl": p.get("realized_pnl", 0),
            "total_traded": p.get("total_traded", 0),
        })
    if as_json:
        _out({"positions": data, "count": len(data)}, True)
    else:
        if not data:
            click.echo("暂无持仓")
            return
        click.echo(f"{'TICKER':<20} {'POSITION':>10} {'EXPOSURE':>10} {'PNL':>10}")
        click.echo("─" * 55)
        for d in data:
            click.echo(f"{d['ticker']:<20} {d['position']:>10} {d['market_exposure']:>10} {d['realized_pnl']:>10}")


# ── PORTFOLIO ──────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
@_err
def portfolio(ctx):
    """投资组合摘要。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    resp = requests.get(f"{_BASE_URL}/portfolio/balance", headers=headers, timeout=15)
    resp.raise_for_status()
    balance_data = resp.json()
    result = {
        "balance": balance_data.get("balance", 0),
        "payout": balance_data.get("payout", 0),
    }
    try:
        pos_resp = requests.get(
            f"{_BASE_URL}/portfolio/positions",
            params={"limit": 100},
            headers=headers,
            timeout=15,
        )
        pos_resp.raise_for_status()
        pos_raw = pos_resp.json()
        positions = pos_raw.get("market_positions", pos_raw.get("positions", []))
        result["open_positions"] = len(positions)
        total_exposure = sum(p.get("market_exposure", 0) for p in positions)
        result["total_exposure"] = total_exposure
    except Exception:
        result["open_positions"] = "unknown"
        result["total_exposure"] = "unknown"
    if as_json:
        _out(result, True)
    else:
        click.echo("📊 投资组合摘要")
        click.echo("─" * 40)
        click.echo(f"  余额:         ${result['balance'] / 100:.2f}" if isinstance(result['balance'], (int, float)) else f"  余额:         {result['balance']}")
        click.echo(f"  持仓数:       {result['open_positions']}")
        click.echo(f"  总敞口:       {result['total_exposure']}")


if __name__ == "__main__":
    cli()
