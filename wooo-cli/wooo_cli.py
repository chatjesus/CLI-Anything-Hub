"""
cli-anything-wooo — All-in-One Crypto CLI (CEX + DEX + DeFi)
聚合多个交易所和 DeFi 协议，统一操作入口。
"""
import json
import sys
import os
import functools
from pathlib import Path
from typing import Optional

import click
import requests

_VERSION = "1.0.0"
_CONFIG_DIR = Path.home() / ".wooo"
_CONFIG_FILE = _CONFIG_DIR / "config.json"

# ── CEX API ENDPOINTS ─────────────────────────────────────────────────────────

_CEX_ENDPOINTS = {
    "okx": {
        "base": "https://www.okx.com",
        "balance": "/api/v5/account/balance",
        "order": "/api/v5/trade/order",
        "positions": "/api/v5/account/positions",
    },
    "binance": {
        "base": "https://api.binance.com",
        "balance": "/api/v3/account",
        "order": "/api/v3/order",
        "positions": "/fapi/v2/positionRisk",
    },
    "bybit": {
        "base": "https://api.bybit.com",
        "balance": "/v5/account/wallet-balance",
        "order": "/v5/order/create",
        "positions": "/v5/position/list",
    },
}

_DEX_ENDPOINTS = {
    "uniswap": "https://api.uniswap.org/v2",
    "curve": "https://api.curve.fi/v1",
    "jupiter": "https://quote-api.jup.ag/v6",
}

_DEFI_ENDPOINTS = {
    "aave": "https://aave-api-v2.aave.com",
    "lido": "https://stake.lido.fi/api",
    "compound": "https://api.compound.finance/api/v2",
}


def _load_config() -> dict:
    """从 ~/.wooo/config.json 加载配置。"""
    if _CONFIG_FILE.exists():
        try:
            return json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_config(config: dict):
    """保存配置到 ~/.wooo/config.json。"""
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def _setup(token: str = None):
    """加载配置，合并环境变量和 CLI 参数。"""
    config = _load_config()
    if token:
        config["wooo_api_key"] = token
    for ex in ("okx", "binance", "bybit"):
        env_key = f"{ex.upper()}_API_KEY"
        env_secret = f"{ex.upper()}_API_SECRET"
        env_pass = f"{ex.upper()}_PASSPHRASE"
        if os.environ.get(env_key):
            config.setdefault("exchanges", {}).setdefault(ex, {})["api_key"] = os.environ[env_key]
        if os.environ.get(env_secret):
            config.setdefault("exchanges", {}).setdefault(ex, {})["api_secret"] = os.environ[env_secret]
        if os.environ.get(env_pass):
            config.setdefault("exchanges", {}).setdefault(ex, {})["passphrase"] = os.environ[env_pass]
    return config


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("WOOO_API_KEY")
    if not t:
        config = _load_config()
        t = config.get("wooo_api_key", "")
    return t


def _exchange_creds(config: dict, exchange: str) -> dict:
    """获取指定交易所的凭证。"""
    ex_config = config.get("exchanges", {}).get(exchange, {})
    api_key = ex_config.get("api_key") or os.environ.get(f"{exchange.upper()}_API_KEY")
    api_secret = ex_config.get("api_secret") or os.environ.get(f"{exchange.upper()}_API_SECRET")
    passphrase = ex_config.get("passphrase") or os.environ.get(f"{exchange.upper()}_PASSPHRASE")
    if not api_key:
        raise click.ClickException(
            f"未提供 {exchange.upper()} API Key。\n"
            f"方式1: export {exchange.upper()}_API_KEY=xxx\n"
            f"方式2: 在 ~/.wooo/config.json 中配置"
        )
    return {"api_key": api_key, "api_secret": api_secret or "", "passphrase": passphrase or ""}


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if isinstance(data, dict):
            click.echo(str(data))
        else:
            click.echo(str(data))


def _wooo_err(fn):
    """捕获 API 请求异常。"""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            resp = e.response
            detail = ""
            if resp is not None:
                try:
                    body = resp.json()
                    detail = body.get("error", body.get("msg", body.get("message", resp.text[:300])))
                except Exception:
                    detail = resp.text[:300]
            raise click.ClickException(f"API 错误 ({resp.status_code if resp is not None else '?'}): {detail}")
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"网络错误: {e}")
    return wrapper


def _cex_headers(exchange: str, creds: dict) -> dict:
    """构建 CEX API headers。"""
    if exchange == "okx":
        return {
            "OK-ACCESS-KEY": creds["api_key"],
            "OK-ACCESS-PASSPHRASE": creds["passphrase"],
            "Content-Type": "application/json",
        }
    elif exchange == "binance":
        return {"X-MBX-APIKEY": creds["api_key"], "Content-Type": "application/json"}
    elif exchange == "bybit":
        return {"X-BAPI-API-KEY": creds["api_key"], "Content-Type": "application/json"}
    return {"Content-Type": "application/json"}


# ── CLI ROOT ──────────────────────────────────────────────────────────────────

@click.group()
@click.option("--key", envvar="WOOO_API_KEY", default=None, help="Wooo API Key（通用）")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-wooo — 全能加密货币 CLI\n
    聚合 CEX (OKX/Binance/Bybit) + DEX (Uniswap/Curve/Jupiter) + DeFi (Aave/Lido/Compound) + Hyperliquid。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json
    ctx.obj["config"] = _setup(key)


# ── DETECT ────────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def detect(ctx):
    """检测连接和配置状态。"""
    as_json = ctx.obj["json"]
    config = ctx.obj["config"]
    exchanges_status = {}
    for ex in ("okx", "binance", "bybit"):
        ex_conf = config.get("exchanges", {}).get(ex, {})
        has_key = bool(ex_conf.get("api_key") or os.environ.get(f"{ex.upper()}_API_KEY"))
        if has_key:
            try:
                ep = _CEX_ENDPOINTS[ex]
                creds = _exchange_creds(config, ex)
                headers = _cex_headers(ex, creds)
                r = requests.get(f"{ep['base']}{ep['balance']}", headers=headers, timeout=10)
                exchanges_status[ex] = {"configured": True, "reachable": r.status_code != 403, "status_code": r.status_code}
            except Exception as e:
                exchanges_status[ex] = {"configured": True, "reachable": False, "error": str(e)[:100]}
        else:
            exchanges_status[ex] = {"configured": False}

    has_config = _CONFIG_FILE.exists()
    result = {
        "status": "ok",
        "config_file": str(_CONFIG_FILE),
        "config_exists": has_config,
        "exchanges": exchanges_status,
        "dex_endpoints": {k: True for k in _DEX_ENDPOINTS},
        "defi_endpoints": {k: True for k in _DEFI_ENDPOINTS},
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"✅ Wooo CLI 状态:")
        click.echo(f"  配置文件: {_CONFIG_FILE} ({'存在' if has_config else '不存在'})")
        for ex, st in exchanges_status.items():
            if st["configured"]:
                icon = "✅" if st.get("reachable") else "⚠️"
                click.echo(f"  {ex.upper()}: {icon} 已配置 {'可连接' if st.get('reachable') else '不可达'}")
            else:
                click.echo(f"  {ex.upper()}: ❌ 未配置")
        click.echo(f"  DEX: {', '.join(_DEX_ENDPOINTS.keys())}")
        click.echo(f"  DeFi: {', '.join(_DEFI_ENDPOINTS.keys())}")


# ── VERSION ───────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {
        "cli": "cli-anything-wooo",
        "version": _VERSION,
        "supported_cex": list(_CEX_ENDPOINTS.keys()),
        "supported_dex": list(_DEX_ENDPOINTS.keys()),
        "supported_defi": list(_DEFI_ENDPOINTS.keys()),
    }
    _out(result, as_json) if as_json else click.echo(
        f"cli-anything-wooo v{_VERSION}\n"
        f"  CEX: {', '.join(result['supported_cex'])}\n"
        f"  DEX: {', '.join(result['supported_dex'])}\n"
        f"  DeFi: {', '.join(result['supported_defi'])}"
    )


# ── SCHEMA ────────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（无需 API Key）。"""
    info = {
        "name": "cli-anything-wooo",
        "version": _VERSION,
        "description": "All-in-One Crypto CLI - CEX (OKX/Binance/Bybit) + DEX (Uniswap/Curve/Jupiter) + DeFi (Aave/Lido/Compound) + Hyperliquid",
        "requires_token": True,
        "token_env": "WOOO_API_KEY",
        "additional_env": ["OKX_API_KEY", "BINANCE_API_KEY", "BYBIT_API_KEY"],
        "config_file": "~/.wooo/config.json",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Check connectivity and config status"},
            {"cmd": "version", "args": [], "desc": "Show CLI version and supported platforms"},
            {"cmd": "cex balance", "args": [
                {"name": "--exchange", "type": "str", "required": True, "choices": ["okx", "binance", "bybit"]},
            ], "desc": "Get CEX balance"},
            {"cmd": "cex order", "args": [
                {"name": "--exchange", "type": "str", "required": True, "choices": ["okx", "binance", "bybit"]},
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--side", "type": "str", "required": True, "choices": ["buy", "sell"]},
                {"name": "--amount", "type": "float", "required": True},
                {"name": "--type", "type": "str", "default": "limit", "choices": ["limit", "market"]},
                {"name": "--price", "type": "float"},
            ], "desc": "Place CEX order"},
            {"cmd": "cex positions", "args": [
                {"name": "--exchange", "type": "str", "required": True, "choices": ["okx", "binance", "bybit"]},
            ], "desc": "List CEX positions"},
            {"cmd": "dex swap", "args": [
                {"name": "--dex", "type": "str", "required": True, "choices": ["uniswap", "curve", "jupiter"]},
                {"name": "--from", "type": "str", "required": True},
                {"name": "--to", "type": "str", "required": True},
                {"name": "--amount", "type": "float", "required": True},
                {"name": "--slippage", "type": "float", "default": 0.5},
            ], "desc": "DEX swap"},
            {"cmd": "dex quote", "args": [
                {"name": "--dex", "type": "str", "required": True},
                {"name": "--from", "type": "str", "required": True},
                {"name": "--to", "type": "str", "required": True},
                {"name": "--amount", "type": "float", "required": True},
            ], "desc": "Get DEX quote"},
            {"cmd": "defi supply", "args": [
                {"name": "--protocol", "type": "str", "required": True, "choices": ["aave", "lido", "compound"]},
                {"name": "--asset", "type": "str", "required": True},
                {"name": "--amount", "type": "float", "required": True},
            ], "desc": "Supply to DeFi protocol"},
            {"cmd": "defi positions", "args": [
                {"name": "--protocol", "type": "str", "required": True, "choices": ["aave", "lido", "compound"]},
            ], "desc": "List DeFi positions"},
            {"cmd": "hyperliquid positions", "args": [], "desc": "Hyperliquid perp positions"},
            {"cmd": "hyperliquid order", "args": [
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--side", "type": "str", "required": True, "choices": ["buy", "sell"]},
                {"name": "--size", "type": "float", "required": True},
                {"name": "--price", "type": "float"},
            ], "desc": "Hyperliquid order"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-wooo --json cex balance --exchange okx",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── CEX GROUP ─────────────────────────────────────────────────────────────────

@cli.group()
def cex():
    """中心化交易所操作（balance / order / positions）。"""


@cex.command(name="balance")
@click.option("--exchange", required=True, type=click.Choice(["okx", "binance", "bybit"]), help="交易所")
@click.pass_context
@_wooo_err
def cex_balance(ctx, exchange):
    """查询 CEX 账户余额。"""
    config = ctx.obj["config"]
    as_json = ctx.obj["json"]
    creds = _exchange_creds(config, exchange)
    ep = _CEX_ENDPOINTS[exchange]
    headers = _cex_headers(exchange, creds)

    r = requests.get(f"{ep['base']}{ep['balance']}", headers=headers, timeout=15)
    r.raise_for_status()
    resp = r.json()

    balances = []
    if exchange == "okx":
        for detail in resp.get("data", [{}])[0].get("details", []):
            if float(detail.get("eq", 0)) > 0:
                balances.append({
                    "currency": detail.get("ccy", ""),
                    "available": detail.get("availBal", "0"),
                    "frozen": detail.get("frozenBal", "0"),
                    "equity": detail.get("eq", "0"),
                })
    elif exchange == "binance":
        for b in resp.get("balances", []):
            free = float(b.get("free", 0))
            locked = float(b.get("locked", 0))
            if free + locked > 0:
                balances.append({
                    "currency": b.get("asset", ""),
                    "available": b.get("free", "0"),
                    "frozen": b.get("locked", "0"),
                    "equity": str(free + locked),
                })
    elif exchange == "bybit":
        for coin in resp.get("result", {}).get("list", [{}])[0].get("coin", []):
            if float(coin.get("equity", 0)) > 0:
                balances.append({
                    "currency": coin.get("coin", ""),
                    "available": coin.get("availableToWithdraw", "0"),
                    "frozen": coin.get("locked", "0"),
                    "equity": coin.get("equity", "0"),
                })

    result = {"exchange": exchange, "balances": balances, "count": len(balances)}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"{exchange.upper()} 余额:")
        click.echo(f"{'CURRENCY':<10} {'AVAILABLE':>16} {'FROZEN':>16} {'EQUITY':>16}")
        click.echo("─" * 62)
        for b in balances:
            click.echo(f"{b['currency']:<10} {b['available']:>16} {b['frozen']:>16} {b['equity']:>16}")


@cex.command(name="order")
@click.option("--exchange", required=True, type=click.Choice(["okx", "binance", "bybit"]), help="交易所")
@click.option("--symbol", required=True, help="交易对 (如 BTC-USDT)")
@click.option("--side", required=True, type=click.Choice(["buy", "sell"]), help="买/卖方向")
@click.option("--amount", required=True, type=float, help="数量")
@click.option("--type", "order_type", default="limit", show_default=True, type=click.Choice(["limit", "market"]), help="订单类型")
@click.option("--price", default=None, type=float, help="限价单价格")
@click.pass_context
@_wooo_err
def cex_order(ctx, exchange, symbol, side, amount, order_type, price):
    """在 CEX 下单。"""
    config = ctx.obj["config"]
    as_json = ctx.obj["json"]
    creds = _exchange_creds(config, exchange)
    ep = _CEX_ENDPOINTS[exchange]
    headers = _cex_headers(exchange, creds)

    if order_type == "limit" and price is None:
        raise click.ClickException("限价单需要指定 --price")

    if exchange == "okx":
        payload = {
            "instId": symbol,
            "tdMode": "cash",
            "side": side,
            "ordType": order_type,
            "sz": str(amount),
        }
        if price:
            payload["px"] = str(price)
    elif exchange == "binance":
        payload = {
            "symbol": symbol.replace("-", ""),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": str(amount),
        }
        if price:
            payload["price"] = str(price)
            payload["timeInForce"] = "GTC"
    elif exchange == "bybit":
        payload = {
            "category": "spot",
            "symbol": symbol.replace("-", ""),
            "side": side.capitalize(),
            "orderType": order_type.capitalize(),
            "qty": str(amount),
        }
        if price:
            payload["price"] = str(price)
    else:
        raise click.ClickException(f"不支持的交易所: {exchange}")

    r = requests.post(f"{ep['base']}{ep['order']}", headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    resp = r.json()

    order_id = ""
    if exchange == "okx":
        order_id = resp.get("data", [{}])[0].get("ordId", "")
    elif exchange == "binance":
        order_id = resp.get("orderId", "")
    elif exchange == "bybit":
        order_id = resp.get("result", {}).get("orderId", "")

    result = {
        "exchange": exchange,
        "order_id": str(order_id),
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "amount": amount,
        "price": price,
        "status": "submitted",
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"✅ 下单成功  {exchange.upper()}  {side} {amount} {symbol} @ {price or 'market'}  order_id={order_id}")


@cex.command(name="positions")
@click.option("--exchange", required=True, type=click.Choice(["okx", "binance", "bybit"]), help="交易所")
@click.pass_context
@_wooo_err
def cex_positions(ctx, exchange):
    """查询 CEX 持仓。"""
    config = ctx.obj["config"]
    as_json = ctx.obj["json"]
    creds = _exchange_creds(config, exchange)
    ep = _CEX_ENDPOINTS[exchange]
    headers = _cex_headers(exchange, creds)

    r = requests.get(f"{ep['base']}{ep['positions']}", headers=headers, timeout=15)
    r.raise_for_status()
    resp = r.json()

    positions = []
    if exchange == "okx":
        for p in resp.get("data", []):
            if float(p.get("pos", 0)) != 0:
                positions.append({
                    "symbol": p.get("instId", ""),
                    "side": p.get("posSide", ""),
                    "size": p.get("pos", "0"),
                    "avg_price": p.get("avgPx", "0"),
                    "unrealized_pnl": p.get("upl", "0"),
                    "leverage": p.get("lever", ""),
                })
    elif exchange == "binance":
        for p in resp if isinstance(resp, list) else resp.get("data", []):
            if float(p.get("positionAmt", 0)) != 0:
                positions.append({
                    "symbol": p.get("symbol", ""),
                    "side": "long" if float(p.get("positionAmt", 0)) > 0 else "short",
                    "size": p.get("positionAmt", "0"),
                    "avg_price": p.get("entryPrice", "0"),
                    "unrealized_pnl": p.get("unRealizedProfit", "0"),
                    "leverage": p.get("leverage", ""),
                })
    elif exchange == "bybit":
        for p in resp.get("result", {}).get("list", []):
            if float(p.get("size", 0)) != 0:
                positions.append({
                    "symbol": p.get("symbol", ""),
                    "side": p.get("side", ""),
                    "size": p.get("size", "0"),
                    "avg_price": p.get("avgPrice", "0"),
                    "unrealized_pnl": p.get("unrealisedPnl", "0"),
                    "leverage": p.get("leverage", ""),
                })

    result = {"exchange": exchange, "positions": positions, "count": len(positions)}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"{exchange.upper()} 持仓:")
        click.echo(f"{'SYMBOL':<16} {'SIDE':<8} {'SIZE':>12} {'AVG_PRICE':>14} {'UPL':>14} LEV")
        click.echo("─" * 80)
        for p in positions:
            click.echo(f"{p['symbol']:<16} {p['side']:<8} {p['size']:>12} {p['avg_price']:>14} {p['unrealized_pnl']:>14} {p['leverage']}")


# ── DEX GROUP ─────────────────────────────────────────────────────────────────

@cli.group()
def dex():
    """去中心化交易所操作（swap / quote）。"""


@dex.command(name="quote")
@click.option("--dex", "dex_name", required=True, type=click.Choice(["uniswap", "curve", "jupiter"]), help="DEX 协议")
@click.option("--from", "from_token", required=True, help="输入代币 (如 ETH)")
@click.option("--to", "to_token", required=True, help="输出代币 (如 USDC)")
@click.option("--amount", required=True, type=float, help="输入数量")
@click.pass_context
@_wooo_err
def dex_quote(ctx, dex_name, from_token, to_token, amount):
    """获取 DEX 报价。"""
    as_json = ctx.obj["json"]
    base = _DEX_ENDPOINTS[dex_name]

    if dex_name == "jupiter":
        params = {
            "inputMint": from_token,
            "outputMint": to_token,
            "amount": int(amount * 1e6),
            "slippageBps": 50,
        }
        r = requests.get(f"{base}/quote", params=params, timeout=15)
    else:
        params = {
            "tokenIn": from_token,
            "tokenOut": to_token,
            "amount": str(amount),
        }
        r = requests.get(f"{base}/quote", params=params, timeout=15)

    r.raise_for_status()
    resp = r.json()

    result = {
        "dex": dex_name,
        "from": from_token,
        "to": to_token,
        "input_amount": amount,
        "output_amount": resp.get("outAmount", resp.get("amountOut", resp.get("expectedOutput", "0"))),
        "price_impact": resp.get("priceImpactPct", resp.get("priceImpact", "0")),
        "route": resp.get("routePlan", resp.get("route", [])),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"DEX 报价 ({dex_name}):")
        click.echo(f"  {amount} {from_token} → {result['output_amount']} {to_token}")
        click.echo(f"  价格影响: {result['price_impact']}%")


@dex.command(name="swap")
@click.option("--dex", "dex_name", required=True, type=click.Choice(["uniswap", "curve", "jupiter"]), help="DEX 协议")
@click.option("--from", "from_token", required=True, help="输入代币")
@click.option("--to", "to_token", required=True, help="输出代币")
@click.option("--amount", required=True, type=float, help="输入数量")
@click.option("--slippage", default=0.5, show_default=True, type=float, help="滑点容忍度 (%)")
@click.pass_context
@_wooo_err
def dex_swap(ctx, dex_name, from_token, to_token, amount, slippage):
    """执行 DEX 交换。"""
    as_json = ctx.obj["json"]
    base = _DEX_ENDPOINTS[dex_name]

    payload = {
        "tokenIn": from_token,
        "tokenOut": to_token,
        "amount": str(amount),
        "slippage": slippage,
    }

    if dex_name == "jupiter":
        params = {
            "inputMint": from_token,
            "outputMint": to_token,
            "amount": int(amount * 1e6),
            "slippageBps": int(slippage * 100),
        }
        r = requests.get(f"{base}/quote", params=params, timeout=15)
        r.raise_for_status()
        quote = r.json()
        r2 = requests.post(f"{base}/swap", json={"quoteResponse": quote, "userPublicKey": ""}, timeout=15)
        r2.raise_for_status()
        resp = r2.json()
    else:
        r = requests.post(f"{base}/swap", json=payload, timeout=15)
        r.raise_for_status()
        resp = r.json()

    result = {
        "dex": dex_name,
        "from": from_token,
        "to": to_token,
        "input_amount": amount,
        "slippage": slippage,
        "tx_hash": resp.get("txHash", resp.get("hash", resp.get("swapTransaction", "pending"))),
        "status": resp.get("status", "submitted"),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"✅ DEX Swap ({dex_name}):")
        click.echo(f"  {amount} {from_token} → {to_token}")
        click.echo(f"  滑点: {slippage}%")
        click.echo(f"  TX: {result['tx_hash']}")


# ── DEFI GROUP ────────────────────────────────────────────────────────────────

@cli.group()
def defi():
    """DeFi 协议操作（supply / positions）。"""


@defi.command(name="supply")
@click.option("--protocol", required=True, type=click.Choice(["aave", "lido", "compound"]), help="DeFi 协议")
@click.option("--asset", required=True, help="资产 (如 ETH, USDC)")
@click.option("--amount", required=True, type=float, help="数量")
@click.pass_context
@_wooo_err
def defi_supply(ctx, protocol, asset, amount):
    """向 DeFi 协议存入资产。"""
    as_json = ctx.obj["json"]
    base = _DEFI_ENDPOINTS[protocol]

    payload = {"asset": asset, "amount": str(amount)}

    if protocol == "lido":
        r = requests.post(f"{base}/submit", json=payload, timeout=15)
    elif protocol == "aave":
        r = requests.post(f"{base}/deposit", json=payload, timeout=15)
    else:
        r = requests.post(f"{base}/supply", json=payload, timeout=15)

    r.raise_for_status()
    resp = r.json()

    result = {
        "protocol": protocol,
        "asset": asset,
        "amount": amount,
        "tx_hash": resp.get("txHash", resp.get("hash", "pending")),
        "apy": resp.get("apy", resp.get("rate", "N/A")),
        "status": resp.get("status", "submitted"),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"✅ DeFi Supply ({protocol}):")
        click.echo(f"  资产: {amount} {asset}")
        click.echo(f"  APY: {result['apy']}")
        click.echo(f"  TX: {result['tx_hash']}")


@defi.command(name="positions")
@click.option("--protocol", required=True, type=click.Choice(["aave", "lido", "compound"]), help="DeFi 协议")
@click.pass_context
@_wooo_err
def defi_positions(ctx, protocol):
    """查询 DeFi 持仓。"""
    as_json = ctx.obj["json"]
    base = _DEFI_ENDPOINTS[protocol]

    r = requests.get(f"{base}/positions", timeout=15)
    r.raise_for_status()
    resp = r.json()

    positions_data = resp.get("data", resp.get("positions", resp)) if isinstance(resp, dict) else resp
    positions = []
    for p in (positions_data if isinstance(positions_data, list) else []):
        positions.append({
            "asset": p.get("asset", p.get("symbol", "")),
            "amount": p.get("amount", p.get("balance", "0")),
            "apy": p.get("apy", p.get("rate", "0")),
            "value_usd": p.get("value_usd", p.get("balanceUSD", "0")),
            "type": p.get("type", "supply"),
        })

    result = {"protocol": protocol, "positions": positions, "count": len(positions)}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"{protocol.upper()} 持仓:")
        click.echo(f"{'ASSET':<10} {'AMOUNT':>16} {'APY':>10} {'VALUE (USD)':>16} TYPE")
        click.echo("─" * 70)
        for p in positions:
            click.echo(f"{p['asset']:<10} {p['amount']:>16} {p['apy']:>10} {p['value_usd']:>16} {p['type']}")


# ── HYPERLIQUID GROUP ─────────────────────────────────────────────────────────

_HYPERLIQUID_BASE = "https://api.hyperliquid.xyz"


@cli.group()
def hyperliquid():
    """Hyperliquid 永续合约操作（positions / order）。"""


@hyperliquid.command(name="positions")
@click.pass_context
@_wooo_err
def hl_positions(ctx):
    """查询 Hyperliquid 永续合约持仓。"""
    as_json = ctx.obj["json"]
    config = ctx.obj["config"]
    wallet = config.get("hyperliquid", {}).get("wallet") or os.environ.get("HYPERLIQUID_WALLET", "")
    if not wallet:
        raise click.ClickException(
            "未提供 Hyperliquid 钱包地址。\n"
            "方式1: export HYPERLIQUID_WALLET=0x...\n"
            "方式2: 在 ~/.wooo/config.json 中配置 hyperliquid.wallet"
        )

    r = requests.post(f"{_HYPERLIQUID_BASE}/info", json={"type": "clearinghouseState", "user": wallet}, timeout=15)
    r.raise_for_status()
    resp = r.json()

    positions = []
    for p in resp.get("assetPositions", []):
        pos = p.get("position", {})
        if float(pos.get("szi", 0)) != 0:
            positions.append({
                "symbol": pos.get("coin", ""),
                "size": pos.get("szi", "0"),
                "entry_price": pos.get("entryPx", "0"),
                "unrealized_pnl": pos.get("unrealizedPnl", "0"),
                "leverage": pos.get("leverage", {}).get("value", ""),
                "liquidation_price": pos.get("liquidationPx", ""),
            })

    result = {"platform": "hyperliquid", "wallet": wallet[:10] + "...", "positions": positions, "count": len(positions)}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"Hyperliquid 持仓 ({wallet[:10]}...):")
        click.echo(f"{'SYMBOL':<10} {'SIZE':>12} {'ENTRY':>14} {'UPL':>14} {'LIQ':>14} LEV")
        click.echo("─" * 80)
        for p in positions:
            click.echo(f"{p['symbol']:<10} {p['size']:>12} {p['entry_price']:>14} {p['unrealized_pnl']:>14} {p['liquidation_price']:>14} {p['leverage']}")


@hyperliquid.command(name="order")
@click.option("--symbol", required=True, help="交易对 (如 BTC)")
@click.option("--side", required=True, type=click.Choice(["buy", "sell"]), help="方向")
@click.option("--size", required=True, type=float, help="合约数量")
@click.option("--price", default=None, type=float, help="限价（不填则为市价）")
@click.pass_context
@_wooo_err
def hl_order(ctx, symbol, side, size, price):
    """在 Hyperliquid 下永续合约订单。"""
    as_json = ctx.obj["json"]
    config = ctx.obj["config"]
    wallet = config.get("hyperliquid", {}).get("wallet") or os.environ.get("HYPERLIQUID_WALLET", "")
    if not wallet:
        raise click.ClickException("未提供 Hyperliquid 钱包地址")

    is_buy = side == "buy"
    order_type = {"limit": {"tif": "Gtc"}} if price else {"market": {}}
    payload = {
        "type": "order",
        "orders": [{
            "a": 0,
            "b": is_buy,
            "p": str(price) if price else "0",
            "s": str(size),
            "r": False,
            "t": order_type,
        }],
        "grouping": "na",
    }

    r = requests.post(f"{_HYPERLIQUID_BASE}/exchange", json={"action": payload, "nonce": 0, "signature": ""}, timeout=15)
    r.raise_for_status()
    resp = r.json()

    result = {
        "platform": "hyperliquid",
        "symbol": symbol,
        "side": side,
        "size": size,
        "price": price or "market",
        "status": resp.get("status", "submitted"),
        "response": resp,
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"✅ Hyperliquid 下单:")
        click.echo(f"  {side.upper()} {size} {symbol} @ {price or 'market'}")
        click.echo(f"  状态: {result['status']}")


if __name__ == "__main__":
    cli()
