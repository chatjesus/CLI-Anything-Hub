"""
cli-anything-polymarket — Polymarket 预测市场 API CLI
通过 CLOB API 查询市场、下单、管理仓位。
"""
import json
import sys
import os
import functools
from typing import Optional

import click
import requests

_BASE_URL = "https://clob.polymarket.com"
_VERSION = "1.0.0"


def _setup(token: str) -> dict:
    """返回带认证的 headers。"""
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("POLYMARKET_API_KEY")
    if not t:
        raise click.ClickException(
            "未提供 Polymarket API Key。\n"
            "方式1: --key YOUR_API_KEY\n"
            "方式2: export POLYMARKET_API_KEY=your_key\n"
            "获取: https://docs.polymarket.com/"
        )
    return t


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
@click.option("--key", envvar="POLYMARKET_API_KEY", default=None, help="Polymarket API Key")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-polymarket — Polymarket 预测市场 CLI\n
    查询市场、下单、管理仓位。支持 --json 结构化输出。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
@_err
def detect(ctx):
    """检测 Polymarket API 连通性。"""
    as_json = ctx.obj["json"]
    try:
        resp = requests.get(f"{_BASE_URL}/markets", params={"limit": 1}, timeout=10)
        resp.raise_for_status()
        result = {"status": "ok", "base_url": _BASE_URL, "http_status": resp.status_code}
        has_key = bool(ctx.obj.get("token") or os.environ.get("POLYMARKET_API_KEY"))
        result["auth"] = "configured" if has_key else "not_configured"
        if as_json:
            _out(result, True)
        else:
            auth_status = "✅" if has_key else "⚠️  未配置"
            click.echo(f"✅ Polymarket CLOB API 连通正常  auth={auth_status}")
    except Exception as e:
        result = {"status": "error", "error": str(e)}
        _out(result, as_json) if as_json else click.echo(f"❌ Polymarket API 连接失败: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {"cli": "cli-anything-polymarket", "version": _VERSION, "api_base": _BASE_URL}
    _out(result, as_json) if as_json else click.echo(f"cli-anything-polymarket v{_VERSION}  api={_BASE_URL}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-polymarket",
        "version": _VERSION,
        "description": "Polymarket 预测市场 CLOB API CLI - 查询市场、下单、管理仓位",
        "requires_token": True,
        "token_env": "POLYMARKET_API_KEY",
        "token_hint": "从 Polymarket 获取 API Key",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Check API connectivity"},
            {"cmd": "version", "args": [], "desc": "Show version info"},
            {"cmd": "market list", "args": [
                {"name": "--limit", "type": "int", "default": 10},
                {"name": "--category", "type": "str"},
            ], "desc": "List active markets"},
            {"cmd": "market get", "args": [
                {"name": "CONDITION_ID", "type": "str", "required": True},
            ], "desc": "Get market by condition_id"},
            {"cmd": "market search", "args": [
                {"name": "--keyword", "type": "str", "required": True},
                {"name": "--limit", "type": "int", "default": 10},
            ], "desc": "Search markets by keyword"},
            {"cmd": "order place", "args": [
                {"name": "--market", "type": "str", "required": True},
                {"name": "--side", "type": "str", "required": True, "choices": ["buy", "sell"]},
                {"name": "--amount", "type": "float", "required": True},
                {"name": "--price", "type": "float", "required": True},
            ], "desc": "Place order"},
            {"cmd": "order cancel", "args": [
                {"name": "ORDER_ID", "type": "str", "required": True},
            ], "desc": "Cancel order by ID"},
            {"cmd": "position list", "args": [], "desc": "List open positions"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-polymarket --key xxx --json market list --limit 5",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── MARKET ──────────────────────────────────────────────────────────────────

@cli.group()
def market():
    """市场查询（list / get / search）。"""


@market.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int, help="返回数量")
@click.option("--category", default=None, help="按分类筛选")
@click.pass_context
@_err
def market_list(ctx, limit, category):
    """列出活跃市场。"""
    as_json = ctx.obj["json"]
    params = {"limit": min(limit, 100)}
    if category:
        params["tag"] = category
    resp = requests.get(f"{_BASE_URL}/markets", params=params, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    markets = raw if isinstance(raw, list) else raw.get("data", raw.get("markets", []))
    data = []
    for m in markets[:limit]:
        data.append({
            "condition_id": m.get("condition_id", ""),
            "question": m.get("question", ""),
            "market_slug": m.get("market_slug", ""),
            "active": m.get("active", False),
            "end_date_iso": m.get("end_date_iso", ""),
        })
    if as_json:
        _out({"markets": data, "count": len(data)}, True)
    else:
        click.echo(f"{'CONDITION_ID':<20} {'ACTIVE':<8} QUESTION")
        click.echo("─" * 80)
        for d in data:
            cid = d["condition_id"][:18] if d["condition_id"] else ""
            click.echo(f"{cid:<20} {str(d['active']):<8} {d['question'][:60]}")


@market.command(name="get")
@click.argument("condition_id")
@click.pass_context
@_err
def market_get(ctx, condition_id):
    """获取市场详情（按 condition_id）。"""
    as_json = ctx.obj["json"]
    resp = requests.get(f"{_BASE_URL}/markets/{condition_id}", timeout=15)
    resp.raise_for_status()
    m = resp.json()
    result = {
        "condition_id": m.get("condition_id", ""),
        "question": m.get("question", ""),
        "description": m.get("description", ""),
        "market_slug": m.get("market_slug", ""),
        "active": m.get("active", False),
        "end_date_iso": m.get("end_date_iso", ""),
        "tokens": m.get("tokens", []),
        "minimum_order_size": m.get("minimum_order_size"),
        "minimum_tick_size": m.get("minimum_tick_size"),
    }
    if as_json:
        _out(result, True)
    else:
        for k, v in result.items():
            if v is not None and v != "" and v != []:
                click.echo(f"  {k:<25} {v}")


@market.command(name="search")
@click.option("--keyword", required=True, help="搜索关键词")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
@_err
def market_search(ctx, keyword, limit):
    """按关键词搜索市场。"""
    as_json = ctx.obj["json"]
    params = {"limit": min(limit, 100)}
    resp = requests.get(f"{_BASE_URL}/markets", params=params, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    markets = raw if isinstance(raw, list) else raw.get("data", raw.get("markets", []))
    kw_lower = keyword.lower()
    filtered = [
        m for m in markets
        if kw_lower in (m.get("question", "") + m.get("description", "")).lower()
    ][:limit]
    data = []
    for m in filtered:
        data.append({
            "condition_id": m.get("condition_id", ""),
            "question": m.get("question", ""),
            "active": m.get("active", False),
        })
    if as_json:
        _out({"results": data, "count": len(data), "keyword": keyword}, True)
    else:
        click.echo(f"搜索 '{keyword}' — 找到 {len(data)} 条结果")
        click.echo("─" * 60)
        for d in data:
            click.echo(f"  [{d['condition_id'][:12]}] {d['question'][:70]}")


# ── ORDER ───────────────────────────────────────────────────────────────────

@cli.group()
def order():
    """订单管理（place / cancel）。"""


@order.command(name="place")
@click.option("--market", "market_id", required=True, help="市场 condition_id 或 token_id")
@click.option("--side", required=True, type=click.Choice(["buy", "sell"]), help="买入或卖出")
@click.option("--amount", required=True, type=float, help="数量")
@click.option("--price", required=True, type=float, help="价格 (0-1)")
@click.pass_context
@_err
def order_place(ctx, market_id, side, amount, price):
    """下单。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    if price < 0 or price > 1:
        raise click.ClickException("价格必须在 0 到 1 之间")
    payload = {
        "tokenID": market_id,
        "side": side.upper(),
        "size": amount,
        "price": price,
        "type": "GTC",
    }
    resp = requests.post(f"{_BASE_URL}/orders", json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    result = resp.json()
    if as_json:
        _out(result, True)
    else:
        order_id = result.get("orderID", result.get("id", "unknown"))
        click.echo(f"✅ 订单已提交  order_id={order_id}  {side} {amount} @ {price}")


@order.command(name="cancel")
@click.argument("order_id")
@click.pass_context
@_err
def order_cancel(ctx, order_id):
    """取消订单。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    resp = requests.delete(f"{_BASE_URL}/orders/{order_id}", headers=headers, timeout=15)
    resp.raise_for_status()
    result = {"status": "cancelled", "order_id": order_id}
    try:
        result = resp.json()
    except Exception:
        pass
    if as_json:
        _out(result, True)
    else:
        click.echo(f"🗑  订单已取消: {order_id}")


# ── POSITION ────────────────────────────────────────────────────────────────

@cli.group()
def position():
    """仓位管理（list）。"""


@position.command(name="list")
@click.pass_context
@_err
def position_list(ctx):
    """列出持仓。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    resp = requests.get(f"{_BASE_URL}/positions", headers=headers, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
    positions = raw if isinstance(raw, list) else raw.get("positions", raw.get("data", []))
    data = []
    for p in positions:
        data.append({
            "asset_id": p.get("asset_id", p.get("tokenID", "")),
            "size": p.get("size", 0),
            "avg_price": p.get("avg_price", 0),
            "market": p.get("market", p.get("question", "")),
        })
    if as_json:
        _out({"positions": data, "count": len(data)}, True)
    else:
        if not data:
            click.echo("暂无持仓")
            return
        click.echo(f"{'ASSET_ID':<20} {'SIZE':>10} {'AVG_PRICE':>10} MARKET")
        click.echo("─" * 70)
        for d in data:
            click.echo(f"{str(d['asset_id'])[:18]:<20} {d['size']:>10} {d['avg_price']:>10} {str(d['market'])[:30]}")


if __name__ == "__main__":
    cli()
