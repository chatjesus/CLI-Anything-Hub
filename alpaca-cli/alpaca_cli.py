"""
cli-anything-alpaca — Alpaca Trading API CLI
Wraps Alpaca REST API for AI Agent use.
"""
import json
import sys
import os
import functools
from typing import Optional

import click

try:
    import requests
    _HTTP_AVAILABLE = True
except ImportError:
    _HTTP_AVAILABLE = False

_PAPER_BASE = "https://paper-api.alpaca.markets"
_LIVE_BASE = "https://api.alpaca.markets"
_DATA_BASE = "https://data.alpaca.markets"


def _setup(api_key: str, secret_key: str):
    if not _HTTP_AVAILABLE:
        raise click.ClickException("requests 未安装，请运行: pip install requests")
    return api_key, secret_key


def _token(ctx) -> tuple:
    api_key = ctx.obj.get("api_key") or os.environ.get("ALPACA_API_KEY")
    secret_key = ctx.obj.get("secret_key") or os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        raise click.ClickException(
            "未提供 Alpaca API 凭证。\n"
            "方式1: --key YOUR_API_KEY --secret YOUR_SECRET_KEY\n"
            "方式2: export ALPACA_API_KEY=xxx && export ALPACA_SECRET_KEY=xxx\n"
            "获取: https://app.alpaca.markets/paper/dashboard/overview"
        )
    return api_key, secret_key


def _base(ctx) -> str:
    if ctx.obj.get("live"):
        return _LIVE_BASE
    return _PAPER_BASE


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if isinstance(data, dict):
            click.echo(str(data))
        else:
            click.echo(str(data))


def _err(fn):
    """统一捕获 Alpaca API 错误。"""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"Alpaca 请求错误: {e}")
        except KeyError as e:
            raise click.ClickException(f"Alpaca 响应解析错误: 缺少字段 {e}")
    return wrapper


def _headers(api_key: str, secret_key: str) -> dict:
    return {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _get(base: str, endpoint: str, api_key: str, secret_key: str, **params) -> dict:
    """发送 GET 请求到 Alpaca API。"""
    url = f"{base}/{endpoint.lstrip('/')}"
    resp = requests.get(url, headers=_headers(api_key, secret_key), params=params, timeout=30)
    if resp.status_code == 401:
        raise click.ClickException("认证失败: API Key 或 Secret Key 无效")
    if resp.status_code == 403:
        raise click.ClickException("权限不足: 请检查 API Key 权限设置")
    if resp.status_code == 404:
        raise click.ClickException(f"未找到: {endpoint}")
    if resp.status_code != 200:
        raise click.ClickException(f"Alpaca API 错误 ({resp.status_code}): {resp.text[:300]}")
    return resp.json()


def _post(base: str, endpoint: str, api_key: str, secret_key: str, payload: dict) -> dict:
    """发送 POST 请求到 Alpaca API。"""
    url = f"{base}/{endpoint.lstrip('/')}"
    resp = requests.post(url, headers=_headers(api_key, secret_key), json=payload, timeout=30)
    if resp.status_code == 401:
        raise click.ClickException("认证失败: API Key 或 Secret Key 无效")
    if resp.status_code == 403:
        raise click.ClickException("权限不足: 请检查 API Key 权限设置")
    if resp.status_code not in (200, 201):
        raise click.ClickException(f"Alpaca API 错误 ({resp.status_code}): {resp.text[:300]}")
    return resp.json()


def _delete(base: str, endpoint: str, api_key: str, secret_key: str) -> Optional[dict]:
    """发送 DELETE 请求到 Alpaca API。"""
    url = f"{base}/{endpoint.lstrip('/')}"
    resp = requests.delete(url, headers=_headers(api_key, secret_key), timeout=30)
    if resp.status_code == 401:
        raise click.ClickException("认证失败: API Key 或 Secret Key 无效")
    if resp.status_code not in (200, 204, 207):
        raise click.ClickException(f"Alpaca API 错误 ({resp.status_code}): {resp.text[:300]}")
    if resp.status_code == 204:
        return {"status": "deleted"}
    return resp.json()


@click.group()
@click.option("--key", envvar="ALPACA_API_KEY", default=None, help="Alpaca API Key")
@click.option("--secret", envvar="ALPACA_SECRET_KEY", default=None, help="Alpaca Secret Key")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.option("--paper/--live", default=True, show_default=True, help="使用模拟盘(paper)或实盘(live)")
@click.pass_context
def cli(ctx, key, secret, as_json, paper):
    """cli-anything-alpaca — Alpaca 交易 CLI\n
    查询账户、持仓、下单、行情数据等。\n
    默认使用 Paper Trading（模拟盘），加 --live 切换实盘。
    """
    ctx.ensure_object(dict)
    ctx.obj["api_key"] = key
    ctx.obj["secret_key"] = secret
    ctx.obj["json"] = as_json
    ctx.obj["live"] = not paper


@cli.command()
@click.pass_context
@_err
def detect(ctx):
    """检测 Alpaca API 凭证有效性。"""
    as_json = ctx.obj["json"]
    if not _HTTP_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install requests"}
        _out(result, as_json) if as_json else click.echo("❌ requests 未安装")
        sys.exit(1)
    try:
        api_key, secret_key = _token(ctx)
        _setup(api_key, secret_key)
        base = _base(ctx)
        data = _get(base, "/v2/account", api_key, secret_key)
        mode = "live" if ctx.obj.get("live") else "paper"
        result = {
            "status": "ok",
            "account_id": data.get("id"),
            "account_number": data.get("account_number"),
            "status_detail": data.get("status"),
            "equity": data.get("equity"),
            "buying_power": data.get("buying_power"),
            "mode": mode,
            "api": "Alpaca Markets",
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Alpaca OK  account={result['account_number']}  mode={mode}  equity=${result['equity']}")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    mode = "live" if ctx.obj.get("live") else "paper"
    result = {
        "cli": "cli-anything-alpaca",
        "version": "1.0.0",
        "api": "Alpaca Markets Trading API",
        "mode": mode,
        "paper_url": _PAPER_BASE,
        "live_url": _LIVE_BASE,
        "data_url": _DATA_BASE,
    }
    _out(result, as_json) if as_json else click.echo(f"cli-anything-alpaca v1.0.0  api=Alpaca  mode={mode}")


# ── ACCOUNT ──────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
@_err
def account(ctx):
    """获取账户详情。"""
    api_key, secret_key = _token(ctx)
    _setup(api_key, secret_key)
    base = _base(ctx)
    as_json = ctx.obj["json"]
    data = _get(base, "/v2/account", api_key, secret_key)
    result = {
        "id": data.get("id"),
        "account_number": data.get("account_number"),
        "status": data.get("status"),
        "equity": data.get("equity"),
        "buying_power": data.get("buying_power"),
        "cash": data.get("cash"),
        "portfolio_value": data.get("portfolio_value"),
        "pattern_day_trader": data.get("pattern_day_trader"),
        "daytrade_count": data.get("daytrade_count"),
        "last_equity": data.get("last_equity"),
        "long_market_value": data.get("long_market_value"),
        "short_market_value": data.get("short_market_value"),
    }
    if as_json:
        _out(result, True)
    else:
        mode = "LIVE" if ctx.obj.get("live") else "PAPER"
        click.echo(f"📊 Alpaca 账户 [{mode}]")
        click.echo("─" * 45)
        for k, v in result.items():
            if v is not None:
                click.echo(f"  {k:<25} {v}")


# ── POSITIONS ────────────────────────────────────────────────────────────────

@cli.group()
def positions():
    """持仓管理（list / get）。"""


@positions.command(name="list")
@click.pass_context
@_err
def positions_list(ctx):
    """列出所有持仓。"""
    api_key, secret_key = _token(ctx)
    _setup(api_key, secret_key)
    base = _base(ctx)
    as_json = ctx.obj["json"]
    data = _get(base, "/v2/positions", api_key, secret_key)
    rows = []
    for p in data:
        rows.append({
            "symbol": p.get("symbol"),
            "qty": p.get("qty"),
            "side": p.get("side"),
            "market_value": p.get("market_value"),
            "cost_basis": p.get("cost_basis"),
            "unrealized_pl": p.get("unrealized_pl"),
            "unrealized_plpc": p.get("unrealized_plpc"),
            "current_price": p.get("current_price"),
            "avg_entry_price": p.get("avg_entry_price"),
        })
    if as_json:
        _out({"positions": rows, "count": len(rows)}, True)
    else:
        click.echo(f"{'SYMBOL':<8} {'QTY':<8} {'PRICE':<12} {'MKT VAL':<14} {'P/L':<14} P/L%")
        click.echo("─" * 75)
        for r in rows:
            click.echo(
                f"{r['symbol']:<8} {r['qty']:<8} ${r['current_price'] or '?':<11} "
                f"${r['market_value'] or '?':<13} ${r['unrealized_pl'] or '?':<13} "
                f"{r['unrealized_plpc'] or 'N/A'}"
            )
        click.echo(f"\n共 {len(rows)} 个持仓")


@positions.command(name="get")
@click.option("--symbol", required=True, help="股票代码")
@click.pass_context
@_err
def positions_get(ctx, symbol):
    """获取指定股票持仓。"""
    api_key, secret_key = _token(ctx)
    _setup(api_key, secret_key)
    base = _base(ctx)
    as_json = ctx.obj["json"]
    data = _get(base, f"/v2/positions/{symbol.upper()}", api_key, secret_key)
    result = {
        "symbol": data.get("symbol"),
        "qty": data.get("qty"),
        "side": data.get("side"),
        "market_value": data.get("market_value"),
        "cost_basis": data.get("cost_basis"),
        "unrealized_pl": data.get("unrealized_pl"),
        "unrealized_plpc": data.get("unrealized_plpc"),
        "current_price": data.get("current_price"),
        "avg_entry_price": data.get("avg_entry_price"),
        "lastday_price": data.get("lastday_price"),
        "change_today": data.get("change_today"),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"📊 持仓: {result['symbol']}")
        click.echo("─" * 40)
        for k, v in result.items():
            if v is not None:
                click.echo(f"  {k:<25} {v}")


# ── ORDERS ───────────────────────────────────────────────────────────────────

@cli.group()
def order():
    """订单管理（submit / list / cancel）。"""


@order.command(name="submit")
@click.option("--symbol", required=True, help="股票代码")
@click.option("--qty", required=True, type=float, help="数量")
@click.option("--side", required=True, type=click.Choice(["buy", "sell"]), help="买/卖方向")
@click.option("--type", "order_type", default="market", type=click.Choice(["market", "limit", "stop", "stop_limit", "trailing_stop"]), show_default=True)
@click.option("--time-in-force", "tif", default="day", type=click.Choice(["day", "gtc", "opg", "cls", "ioc", "fok"]), show_default=True)
@click.option("--limit-price", default=None, type=float, help="限价单价格")
@click.option("--stop-price", default=None, type=float, help="止损价格")
@click.pass_context
@_err
def order_submit(ctx, symbol, qty, side, order_type, tif, limit_price, stop_price):
    """提交订单。"""
    api_key, secret_key = _token(ctx)
    _setup(api_key, secret_key)
    base = _base(ctx)
    as_json = ctx.obj["json"]
    mode = "LIVE" if ctx.obj.get("live") else "PAPER"

    if ctx.obj.get("live"):
        click.echo(f"⚠️  警告: 正在使用实盘 (LIVE) 模式！此操作将影响真实资金！", err=True)

    payload = {
        "symbol": symbol.upper(),
        "qty": str(qty),
        "side": side,
        "type": order_type,
        "time_in_force": tif,
    }
    if limit_price and order_type in ("limit", "stop_limit"):
        payload["limit_price"] = str(limit_price)
    if stop_price and order_type in ("stop", "stop_limit"):
        payload["stop_price"] = str(stop_price)

    data = _post(base, "/v2/orders", api_key, secret_key, payload)
    result = {
        "id": data.get("id"),
        "symbol": data.get("symbol"),
        "side": data.get("side"),
        "qty": data.get("qty"),
        "type": data.get("type"),
        "time_in_force": data.get("time_in_force"),
        "status": data.get("status"),
        "limit_price": data.get("limit_price"),
        "stop_price": data.get("stop_price"),
        "submitted_at": data.get("submitted_at"),
        "mode": mode,
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"✅ [{mode}] 订单已提交: {result['id']}")
        click.echo(f"   {side.upper()} {qty}x {symbol.upper()} ({order_type})  status={result['status']}")


@order.command(name="list")
@click.option("--status", default="open", type=click.Choice(["open", "closed", "all"]), show_default=True)
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
@_err
def order_list(ctx, status, limit):
    """列出订单。"""
    api_key, secret_key = _token(ctx)
    _setup(api_key, secret_key)
    base = _base(ctx)
    as_json = ctx.obj["json"]
    data = _get(base, "/v2/orders", api_key, secret_key, status=status, limit=min(limit, 500))
    rows = []
    for o in data:
        rows.append({
            "id": o.get("id"),
            "symbol": o.get("symbol"),
            "side": o.get("side"),
            "qty": o.get("qty"),
            "type": o.get("type"),
            "status": o.get("status"),
            "filled_qty": o.get("filled_qty"),
            "limit_price": o.get("limit_price"),
            "submitted_at": o.get("submitted_at"),
        })
    if as_json:
        _out({"orders": rows, "count": len(rows), "filter_status": status}, True)
    else:
        click.echo(f"{'SYMBOL':<8} {'SIDE':<6} {'QTY':<8} {'TYPE':<10} {'STATUS':<14} SUBMITTED")
        click.echo("─" * 75)
        for r in rows:
            click.echo(
                f"{r['symbol']:<8} {(r['side'] or ''):<6} {r['qty']:<8} "
                f"{(r['type'] or ''):<10} {(r['status'] or ''):<14} {(r['submitted_at'] or '')[:19]}"
            )
        click.echo(f"\n共 {len(rows)} 条 (filter={status})")


@order.command(name="cancel")
@click.option("--order-id", default=None, help="要取消的订单 ID")
@click.option("--all", "cancel_all", is_flag=True, help="取消所有未成交订单")
@click.pass_context
@_err
def order_cancel(ctx, order_id, cancel_all):
    """取消订单。"""
    api_key, secret_key = _token(ctx)
    _setup(api_key, secret_key)
    base = _base(ctx)
    as_json = ctx.obj["json"]

    if not order_id and not cancel_all:
        raise click.ClickException("请指定 --order-id 或 --all")

    if cancel_all:
        data = _delete(base, "/v2/orders", api_key, secret_key)
        if isinstance(data, list):
            result = {"cancelled": len(data), "orders": data}
        else:
            result = {"cancelled": "all", "status": "ok"}
        _out(result, as_json) if as_json else click.echo(f"✅ 已取消所有未成交订单")
    else:
        data = _delete(base, f"/v2/orders/{order_id}", api_key, secret_key)
        result = {"order_id": order_id, "status": "cancelled"}
        _out(result, as_json) if as_json else click.echo(f"✅ 已取消订单: {order_id}")


# ── BARS ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--symbol", required=True, help="股票代码")
@click.option("--timeframe", default="1Day", type=click.Choice(["1Min", "5Min", "15Min", "1Hour", "1Day"]), show_default=True)
@click.option("--start", default=None, help="起始时间 (RFC3339 或 YYYY-MM-DD)")
@click.option("--end", default=None, help="截止时间 (RFC3339 或 YYYY-MM-DD)")
@click.option("--limit", default=50, show_default=True, type=int)
@click.pass_context
@_err
def bars(ctx, symbol, timeframe, start, end, limit):
    """获取 K 线/OHLCV 数据。"""
    api_key, secret_key = _token(ctx)
    _setup(api_key, secret_key)
    as_json = ctx.obj["json"]
    params = {"timeframe": timeframe, "limit": min(limit, 10000)}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    data = _get(_DATA_BASE, f"/v2/stocks/{symbol.upper()}/bars", api_key, secret_key, **params)
    bar_list = data.get("bars", [])
    rows = [
        {
            "timestamp": b.get("t"),
            "open": b.get("o"),
            "high": b.get("h"),
            "low": b.get("l"),
            "close": b.get("c"),
            "volume": b.get("v"),
            "vwap": b.get("vw"),
        }
        for b in bar_list
    ]
    if as_json:
        _out({"symbol": symbol.upper(), "timeframe": timeframe, "count": len(rows), "bars": rows}, True)
    else:
        click.echo(f"📊 {symbol.upper()} K线 ({timeframe})")
        click.echo(f"{'TIME':<22} {'OPEN':>10} {'HIGH':>10} {'LOW':>10} {'CLOSE':>10} {'VOL':>12}")
        click.echo("─" * 80)
        for r in rows:
            click.echo(
                f"{(r['timestamp'] or '')[:19]:<22} "
                f"{r['open']:>10} {r['high']:>10} {r['low']:>10} {r['close']:>10} "
                f"{r['volume']:>12}"
            )
        click.echo(f"\n共 {len(rows)} 根K线")


# ── SNAPSHOT ─────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--symbol", required=True, help="股票代码")
@click.pass_context
@_err
def snapshot(ctx, symbol):
    """获取股票快照（最新报价、成交、K线）。"""
    api_key, secret_key = _token(ctx)
    _setup(api_key, secret_key)
    as_json = ctx.obj["json"]
    data = _get(_DATA_BASE, f"/v2/stocks/{symbol.upper()}/snapshot", api_key, secret_key)
    latest_trade = data.get("latestTrade", {})
    latest_quote = data.get("latestQuote", {})
    minute_bar = data.get("minuteBar", {})
    daily_bar = data.get("dailyBar", {})
    prev_daily_bar = data.get("prevDailyBar", {})
    result = {
        "symbol": symbol.upper(),
        "latest_trade": {
            "price": latest_trade.get("p"),
            "size": latest_trade.get("s"),
            "timestamp": latest_trade.get("t"),
        },
        "latest_quote": {
            "bid": latest_quote.get("bp"),
            "ask": latest_quote.get("ap"),
            "bid_size": latest_quote.get("bs"),
            "ask_size": latest_quote.get("as"),
        },
        "minute_bar": {
            "open": minute_bar.get("o"),
            "high": minute_bar.get("h"),
            "low": minute_bar.get("l"),
            "close": minute_bar.get("c"),
            "volume": minute_bar.get("v"),
        },
        "daily_bar": {
            "open": daily_bar.get("o"),
            "high": daily_bar.get("h"),
            "low": daily_bar.get("l"),
            "close": daily_bar.get("c"),
            "volume": daily_bar.get("v"),
        },
        "prev_daily_bar": {
            "open": prev_daily_bar.get("o"),
            "high": prev_daily_bar.get("h"),
            "low": prev_daily_bar.get("l"),
            "close": prev_daily_bar.get("c"),
            "volume": prev_daily_bar.get("v"),
        },
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"📊 快照: {symbol.upper()}")
        click.echo("─" * 50)
        click.echo(f"  最新成交:  ${latest_trade.get('p', 'N/A')}  x{latest_trade.get('s', '?')}")
        click.echo(f"  买一/卖一: ${latest_quote.get('bp', '?')} / ${latest_quote.get('ap', '?')}")
        click.echo(f"  今日 OHLC: {daily_bar.get('o')} / {daily_bar.get('h')} / {daily_bar.get('l')} / {daily_bar.get('c')}")
        click.echo(f"  今日成交量: {daily_bar.get('v', 'N/A')}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-alpaca",
        "version": "1.0.0",
        "description": "Alpaca Trading API CLI - account, positions, orders, bars, snapshots for stock trading",
        "requires_token": True,
        "token_env": ["ALPACA_API_KEY", "ALPACA_SECRET_KEY"],
        "token_hint": "Get keys at https://app.alpaca.markets/paper/dashboard/overview",
        "modes": {"paper": "https://paper-api.alpaca.markets (default)", "live": "https://api.alpaca.markets (use --live flag)"},
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Verify API credentials and show account"},
            {"cmd": "version", "args": [], "desc": "Show CLI version info"},
            {"cmd": "account", "args": [], "desc": "Get account details (equity, buying power, cash)"},
            {"cmd": "positions list", "args": [], "desc": "List all positions"},
            {"cmd": "positions get", "args": [{"name": "--symbol", "type": "str", "required": True}], "desc": "Get position for a symbol"},
            {"cmd": "order submit", "args": [
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--qty", "type": "float", "required": True},
                {"name": "--side", "type": "str", "required": True, "choices": ["buy", "sell"]},
                {"name": "--type", "type": "str", "default": "market", "choices": ["market", "limit", "stop", "stop_limit", "trailing_stop"]},
                {"name": "--time-in-force", "type": "str", "default": "day", "choices": ["day", "gtc", "opg", "cls", "ioc", "fok"]},
                {"name": "--limit-price", "type": "float"},
                {"name": "--stop-price", "type": "float"},
            ], "desc": "Submit an order"},
            {"cmd": "order list", "args": [
                {"name": "--status", "type": "str", "default": "open", "choices": ["open", "closed", "all"]},
                {"name": "--limit", "type": "int", "default": 20},
            ], "desc": "List orders"},
            {"cmd": "order cancel", "args": [
                {"name": "--order-id", "type": "str"},
                {"name": "--all", "type": "flag"},
            ], "desc": "Cancel order(s)"},
            {"cmd": "bars", "args": [
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--timeframe", "type": "str", "default": "1Day", "choices": ["1Min", "5Min", "15Min", "1Hour", "1Day"]},
                {"name": "--start", "type": "str"},
                {"name": "--end", "type": "str"},
                {"name": "--limit", "type": "int", "default": 50},
            ], "desc": "Get OHLCV bars/candles"},
            {"cmd": "snapshot", "args": [{"name": "--symbol", "type": "str", "required": True}], "desc": "Get stock snapshot (trade, quote, bars)"},
        ],
        "global_flags": ["--paper (default)", "--live"],
        "json_flag": "--json",
        "example": "cli-anything-alpaca --json account",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
