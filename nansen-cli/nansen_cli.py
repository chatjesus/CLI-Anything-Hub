"""
cli-anything-nansen — Nansen On-Chain Analytics API CLI
通过 Nansen REST API 查询聪明钱流向、代币分析、钱包画像和 DEX 交易。
"""
import json
import sys
import os
import functools
from typing import Optional

import click
import requests

_BASE = "https://api.nansen.ai/v1"
_VERSION = "1.0.0"


def _setup(token: str) -> dict:
    """返回带认证头的 headers。"""
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("NANSEN_API_KEY")
    if not t:
        raise click.ClickException(
            "未提供 Nansen API Key。\n"
            "方式1: --key your_api_key\n"
            "方式2: export NANSEN_API_KEY=your_key\n"
            "获取: https://app.nansen.ai/settings/api"
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


def _api_err(fn):
    """统一捕获 API 异常。"""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            resp = e.response
            detail = ""
            if resp is not None:
                try:
                    detail = resp.json().get("error", resp.text[:200])
                except Exception:
                    detail = resp.text[:200]
            raise click.ClickException(f"Nansen API 错误 ({resp.status_code if resp is not None else '?'}): {detail}")
        except requests.exceptions.ConnectionError:
            raise click.ClickException("无法连接 Nansen API，请检查网络。")
        except requests.exceptions.Timeout:
            raise click.ClickException("Nansen API 请求超时。")
    return wrapper


def _get(headers, path, params=None):
    r = requests.get(f"{_BASE}{path}", headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _post(headers, path, payload=None):
    r = requests.post(f"{_BASE}{path}", headers=headers, json=payload or {}, timeout=30)
    r.raise_for_status()
    return r.json()


@click.group()
@click.option("--key", envvar="NANSEN_API_KEY", default=None, help="Nansen API Key")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-nansen — Nansen 链上数据分析 CLI\n
    聪明钱流向、代币分析、钱包画像、DEX 交易、标签搜索。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
@_api_err
def detect(ctx):
    """检测 Nansen API Key 有效性。"""
    as_json = ctx.obj["json"]
    try:
        t = _token(ctx)
        headers = _setup(t)
        data = _get(headers, "/me")
        result = {
            "status": "ok",
            "user": data.get("username", data.get("email", "")),
            "plan": data.get("plan", data.get("tier", "")),
            "api_key_prefix": t[:8] + "...",
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Nansen OK  user={result['user']}  plan={result['plan']}")
    except click.ClickException:
        raise
    except Exception as e:
        err = {"status": "error", "error": str(e)}
        _out(err, as_json) if as_json else click.echo(f"❌ {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {"cli": "cli-anything-nansen", "version": _VERSION, "api_base": _BASE}
    _out(result, as_json) if as_json else click.echo(f"cli-anything-nansen v{_VERSION}  api={_BASE}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-nansen",
        "version": _VERSION,
        "description": "Nansen On-Chain Analytics API CLI - smart money, token analysis, wallet profiling, DEX trades, labels",
        "requires_token": True,
        "token_env": "NANSEN_API_KEY",
        "token_hint": "API key from https://app.nansen.ai/settings/api",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Verify API key validity"},
            {"cmd": "version", "args": [], "desc": "Show CLI version"},
            {"cmd": "smart-money", "args": [{"name": "--chain", "type": "str", "default": "ethereum"}, {"name": "--timeframe", "type": "str", "default": "24h"}], "desc": "Get smart money flows"},
            {"cmd": "token analysis", "args": [{"name": "--address", "type": "str", "required": True}, {"name": "--chain", "type": "str", "default": "ethereum"}], "desc": "Analyze token"},
            {"cmd": "token holders", "args": [{"name": "--address", "type": "str", "required": True}, {"name": "--chain", "type": "str", "default": "ethereum"}, {"name": "--limit", "type": "int", "default": 20}], "desc": "Top token holders"},
            {"cmd": "wallet profile", "args": [{"name": "--address", "type": "str", "required": True}, {"name": "--chain", "type": "str", "default": "ethereum"}], "desc": "Wallet profiling"},
            {"cmd": "dex trades", "args": [{"name": "--chain", "type": "str", "default": "ethereum"}, {"name": "--pair", "type": "str"}, {"name": "--limit", "type": "int", "default": 50}], "desc": "Recent DEX trades"},
            {"cmd": "labels search", "args": [{"name": "--query", "type": "str", "required": True}], "desc": "Search wallet labels"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-nansen --key xxx --json smart-money --chain ethereum --timeframe 24h",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── SMART MONEY ──────────────────────────────────────────────────────────────

@cli.command(name="smart-money")
@click.option("--chain", default="ethereum", show_default=True, type=click.Choice(["ethereum", "solana", "base", "polygon", "arbitrum", "bnb", "optimism", "avalanche"], case_sensitive=False), help="区块链")
@click.option("--timeframe", default="24h", show_default=True, type=click.Choice(["1h", "24h", "7d", "30d"], case_sensitive=False), help="时间范围")
@click.pass_context
@_api_err
def smart_money(ctx, chain, timeframe):
    """查询聪明钱资金流向。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _get(headers, "/smart-money", params={"chain": chain, "timeframe": timeframe})
    flows = data if isinstance(data, list) else data.get("data", data.get("flows", []))
    result = {"chain": chain, "timeframe": timeframe, "count": len(flows) if isinstance(flows, list) else 0, "flows": flows}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"🧠 聪明钱流向  chain={chain}  timeframe={timeframe}")
        if isinstance(flows, list):
            for f in flows[:20]:
                token = f.get("token", f.get("symbol", ""))
                amount = f.get("amount", f.get("value", ""))
                direction = f.get("direction", f.get("type", ""))
                click.echo(f"  {direction:<8} {token:<12} {amount}")
        else:
            click.echo(f"  {flows}")


# ── TOKEN ────────────────────────────────────────────────────────────────────

@cli.group()
def token():
    """代币分析（analysis / holders）。"""


@token.command(name="analysis")
@click.option("--address", required=True, help="代币合约地址")
@click.option("--chain", default="ethereum", show_default=True, type=click.Choice(["ethereum", "solana", "base", "polygon", "arbitrum", "bnb"], case_sensitive=False))
@click.pass_context
@_api_err
def token_analysis(ctx, address, chain):
    """分析代币详情。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _get(headers, "/token/analysis", params={"address": address, "chain": chain})
    result = {
        "address": address,
        "chain": chain,
        "name": data.get("name", ""),
        "symbol": data.get("symbol", ""),
        "price": data.get("price", ""),
        "market_cap": data.get("market_cap", ""),
        "holders_count": data.get("holders_count", ""),
        "smart_money_holdings": data.get("smart_money_holdings", ""),
        "whale_concentration": data.get("whale_concentration", ""),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"🪙 {result['name']} ({result['symbol']})  chain={chain}")
        click.echo(f"   价格: {result['price']}")
        click.echo(f"   市值: {result['market_cap']}")
        click.echo(f"   持有人: {result['holders_count']}")
        click.echo(f"   聪明钱持仓: {result['smart_money_holdings']}")


@token.command(name="holders")
@click.option("--address", required=True, help="代币合约地址")
@click.option("--chain", default="ethereum", show_default=True, type=click.Choice(["ethereum", "solana", "base", "polygon", "arbitrum", "bnb"], case_sensitive=False))
@click.option("--limit", default=20, show_default=True, type=int, help="返回数量")
@click.pass_context
@_api_err
def token_holders(ctx, address, chain, limit):
    """查询代币 Top 持有人。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _get(headers, "/token/holders", params={"address": address, "chain": chain, "limit": limit})
    holders = data if isinstance(data, list) else data.get("holders", data.get("data", []))
    result = {"address": address, "chain": chain, "count": len(holders) if isinstance(holders, list) else 0, "holders": holders}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"👥 Top 持有人  token={address[:10]}...  chain={chain}")
        if isinstance(holders, list):
            click.echo(f"  {'#':<4} {'ADDRESS':<44} {'BALANCE':>14} LABEL")
            click.echo("  " + "─" * 80)
            for i, h in enumerate(holders[:limit], 1):
                addr = h.get("address", "")
                bal = h.get("balance", h.get("amount", ""))
                label = h.get("label", h.get("name", ""))
                click.echo(f"  {i:<4} {addr:<44} {str(bal):>14} {label}")


# ── WALLET ───────────────────────────────────────────────────────────────────

@cli.group()
def wallet():
    """钱包画像（profile）。"""


@wallet.command(name="profile")
@click.option("--address", required=True, help="钱包地址")
@click.option("--chain", default="ethereum", show_default=True, type=click.Choice(["ethereum", "solana", "base", "polygon", "arbitrum", "bnb"], case_sensitive=False))
@click.pass_context
@_api_err
def wallet_profile(ctx, address, chain):
    """查看钱包画像。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _get(headers, "/wallet/profile", params={"address": address, "chain": chain})
    result = {
        "address": address,
        "chain": chain,
        "labels": data.get("labels", []),
        "portfolio_value": data.get("portfolio_value", ""),
        "first_seen": data.get("first_seen", ""),
        "transaction_count": data.get("transaction_count", ""),
        "tokens_held": data.get("tokens_held", []),
        "nft_count": data.get("nft_count", ""),
        "risk_score": data.get("risk_score", ""),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"👛 钱包画像  {address}")
        click.echo(f"   标签: {', '.join(result['labels']) if result['labels'] else '无'}")
        click.echo(f"   资产总值: {result['portfolio_value']}")
        click.echo(f"   交易数: {result['transaction_count']}")
        click.echo(f"   首次活跃: {result['first_seen']}")


# ── DEX ──────────────────────────────────────────────────────────────────────

@cli.group()
def dex():
    """DEX 交易（trades）。"""


@dex.command(name="trades")
@click.option("--chain", default="ethereum", show_default=True, type=click.Choice(["ethereum", "solana", "base", "polygon", "arbitrum", "bnb"], case_sensitive=False))
@click.option("--pair", default=None, help="交易对，例如 ETH/USDC")
@click.option("--limit", default=50, show_default=True, type=int)
@click.pass_context
@_api_err
def dex_trades(ctx, chain, pair, limit):
    """查询近期 DEX 交易。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    params = {"chain": chain, "limit": limit}
    if pair:
        params["pair"] = pair
    data = _get(headers, "/dex/trades", params=params)
    trades = data if isinstance(data, list) else data.get("trades", data.get("data", []))
    result = {"chain": chain, "pair": pair, "count": len(trades) if isinstance(trades, list) else 0, "trades": trades}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"📈 DEX 交易  chain={chain}  pair={pair or 'all'}")
        if isinstance(trades, list):
            for t in trades[:20]:
                ts = t.get("timestamp", t.get("time", ""))
                side = t.get("side", t.get("type", ""))
                token_in = t.get("token_in", t.get("from_token", ""))
                token_out = t.get("token_out", t.get("to_token", ""))
                amount = t.get("amount", t.get("value", ""))
                click.echo(f"  {ts}  {side:<6} {token_in} → {token_out}  {amount}")


# ── LABELS ───────────────────────────────────────────────────────────────────

@cli.group()
def labels():
    """标签搜索（search）。"""


@labels.command(name="search")
@click.option("--query", "query_str", required=True, help="搜索关键词")
@click.pass_context
@_api_err
def labels_search(ctx, query_str):
    """搜索钱包标签。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _get(headers, "/labels/search", params={"query": query_str})
    labels_list = data if isinstance(data, list) else data.get("labels", data.get("data", []))
    result = {"query": query_str, "count": len(labels_list) if isinstance(labels_list, list) else 0, "labels": labels_list}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"🏷️  标签搜索: \"{query_str}\"")
        if isinstance(labels_list, list):
            for lb in labels_list[:30]:
                addr = lb.get("address", "")
                name = lb.get("label", lb.get("name", ""))
                entity = lb.get("entity", lb.get("category", ""))
                click.echo(f"  {addr:<44} {name:<20} {entity}")


if __name__ == "__main__":
    cli()
