"""
cli-anything-alphavantage — Alpha Vantage 金融数据 API CLI
通过 Alpha Vantage API 查询行情、时间序列、基本面、外汇和加密货币数据。
"""
import json
import sys
import os
import functools
from typing import Optional

import click
import requests

_BASE_URL = "https://www.alphavantage.co/query"
_VERSION = "1.0.0"


def _setup(token: str) -> dict:
    """返回通用请求参数（含 API Key）。"""
    return {"apikey": token}


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not t:
        raise click.ClickException(
            "未提供 Alpha Vantage API Key。\n"
            "方式1: --key YOUR_API_KEY\n"
            "方式2: export ALPHA_VANTAGE_API_KEY=your_key\n"
            "获取: https://www.alphavantage.co/support/#api-key"
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


def _av_request(params: dict, timeout: int = 15) -> dict:
    """发送 Alpha Vantage API 请求并返回 JSON。"""
    resp = requests.get(_BASE_URL, params=params, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    if "Error Message" in data:
        raise click.ClickException(f"Alpha Vantage 错误: {data['Error Message']}")
    if "Note" in data:
        raise click.ClickException(f"Alpha Vantage 限流: {data['Note']}")
    return data


@click.group()
@click.option("--key", envvar="ALPHA_VANTAGE_API_KEY", default=None, help="Alpha Vantage API Key")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-alphavantage — Alpha Vantage 金融数据 CLI\n
    查询行情、时间序列、基本面、外汇和加密货币。支持 --json 结构化输出。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
@_err
def detect(ctx):
    """检测 Alpha Vantage API Key 有效性。"""
    as_json = ctx.obj["json"]
    try:
        t = _token(ctx)
        params = {**_setup(t), "function": "GLOBAL_QUOTE", "symbol": "AAPL"}
        data = _av_request(params)
        gq = data.get("Global Quote", {})
        result = {
            "status": "ok",
            "api_base": _BASE_URL,
            "test_symbol": "AAPL",
            "test_price": gq.get("05. price", "N/A"),
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Alpha Vantage API 正常  AAPL={gq.get('05. price', 'N/A')}")
    except click.ClickException:
        raise
    except Exception as e:
        result = {"status": "error", "error": str(e)}
        _out(result, as_json) if as_json else click.echo(f"❌ Alpha Vantage API 连接失败: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {"cli": "cli-anything-alphavantage", "version": _VERSION, "api_base": _BASE_URL}
    _out(result, as_json) if as_json else click.echo(f"cli-anything-alphavantage v{_VERSION}  api={_BASE_URL}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-alphavantage",
        "version": _VERSION,
        "description": "Alpha Vantage 金融数据 API CLI - 行情、时间序列、基本面、外汇、加密货币",
        "requires_token": True,
        "token_env": "ALPHA_VANTAGE_API_KEY",
        "token_hint": "从 https://www.alphavantage.co/support/#api-key 免费获取",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Test API key validity"},
            {"cmd": "version", "args": [], "desc": "Show version info"},
            {"cmd": "quote", "args": [
                {"name": "--symbol", "type": "str", "required": True},
            ], "desc": "Get real-time quote"},
            {"cmd": "timeseries daily", "args": [
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--outputsize", "type": "str", "default": "compact", "choices": ["compact", "full"]},
            ], "desc": "Daily time series"},
            {"cmd": "timeseries intraday", "args": [
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--interval", "type": "str", "default": "5min", "choices": ["1min", "5min", "15min", "30min", "60min"]},
            ], "desc": "Intraday time series"},
            {"cmd": "search", "args": [
                {"name": "--keywords", "type": "str", "required": True},
            ], "desc": "Symbol search"},
            {"cmd": "fundamentals income", "args": [
                {"name": "--symbol", "type": "str", "required": True},
            ], "desc": "Income statement"},
            {"cmd": "fundamentals balance", "args": [
                {"name": "--symbol", "type": "str", "required": True},
            ], "desc": "Balance sheet"},
            {"cmd": "fundamentals earnings", "args": [
                {"name": "--symbol", "type": "str", "required": True},
            ], "desc": "Earnings data"},
            {"cmd": "forex rate", "args": [
                {"name": "--from-currency", "type": "str", "required": True},
                {"name": "--to-currency", "type": "str", "required": True},
            ], "desc": "Forex exchange rate"},
            {"cmd": "crypto daily", "args": [
                {"name": "--symbol", "type": "str", "required": True},
                {"name": "--market", "type": "str", "default": "USD"},
            ], "desc": "Crypto daily prices"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-alphavantage --key xxx --json quote --symbol AAPL",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── QUOTE ──────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--symbol", required=True, help="股票代码 (如 AAPL, MSFT)")
@click.pass_context
@_err
def quote(ctx, symbol):
    """获取实时行情报价。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {**_setup(t), "function": "GLOBAL_QUOTE", "symbol": symbol.upper()}
    data = _av_request(params)
    gq = data.get("Global Quote", {})
    result = {
        "symbol": gq.get("01. symbol", symbol),
        "open": gq.get("02. open"),
        "high": gq.get("03. high"),
        "low": gq.get("04. low"),
        "price": gq.get("05. price"),
        "volume": gq.get("06. volume"),
        "latest_trading_day": gq.get("07. latest trading day"),
        "previous_close": gq.get("08. previous close"),
        "change": gq.get("09. change"),
        "change_percent": gq.get("10. change percent"),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"📈 {result['symbol']}  价格: {result['price']}  涨跌: {result['change']} ({result['change_percent']})")
        click.echo(f"  开盘: {result['open']}  最高: {result['high']}  最低: {result['low']}  成交量: {result['volume']}")


# ── TIMESERIES ─────────────────────────────────────────────────────────────

@cli.group()
def timeseries():
    """时间序列数据（daily / intraday）。"""


@timeseries.command(name="daily")
@click.option("--symbol", required=True, help="股票代码")
@click.option("--outputsize", default="compact", type=click.Choice(["compact", "full"]), show_default=True, help="compact=最近100条, full=全量")
@click.pass_context
@_err
def ts_daily(ctx, symbol, outputsize):
    """获取日线时间序列。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {**_setup(t), "function": "TIME_SERIES_DAILY", "symbol": symbol.upper(), "outputsize": outputsize}
    data = _av_request(params)
    meta = data.get("Meta Data", {})
    ts = data.get("Time Series (Daily)", {})
    entries = []
    for date, vals in sorted(ts.items(), reverse=True)[:20]:
        entries.append({
            "date": date,
            "open": vals.get("1. open"),
            "high": vals.get("2. high"),
            "low": vals.get("3. low"),
            "close": vals.get("4. close"),
            "volume": vals.get("5. volume"),
        })
    if as_json:
        _out({"symbol": meta.get("2. Symbol", symbol), "entries": entries, "count": len(entries)}, True)
    else:
        click.echo(f"📊 {symbol.upper()} 日线 (最近 {len(entries)} 条)")
        click.echo(f"{'DATE':<12} {'OPEN':>10} {'HIGH':>10} {'LOW':>10} {'CLOSE':>10} {'VOLUME':>12}")
        click.echo("─" * 70)
        for e in entries:
            click.echo(f"{e['date']:<12} {e['open']:>10} {e['high']:>10} {e['low']:>10} {e['close']:>10} {e['volume']:>12}")


@timeseries.command(name="intraday")
@click.option("--symbol", required=True, help="股票代码")
@click.option("--interval", default="5min", type=click.Choice(["1min", "5min", "15min", "30min", "60min"]), show_default=True)
@click.pass_context
@_err
def ts_intraday(ctx, symbol, interval):
    """获取分钟级时间序列。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {**_setup(t), "function": "TIME_SERIES_INTRADAY", "symbol": symbol.upper(), "interval": interval}
    data = _av_request(params)
    meta = data.get("Meta Data", {})
    ts_key = f"Time Series ({interval})"
    ts = data.get(ts_key, {})
    entries = []
    for dt, vals in sorted(ts.items(), reverse=True)[:20]:
        entries.append({
            "datetime": dt,
            "open": vals.get("1. open"),
            "high": vals.get("2. high"),
            "low": vals.get("3. low"),
            "close": vals.get("4. close"),
            "volume": vals.get("5. volume"),
        })
    if as_json:
        _out({"symbol": meta.get("2. Symbol", symbol), "interval": interval, "entries": entries, "count": len(entries)}, True)
    else:
        click.echo(f"📊 {symbol.upper()} 分时 ({interval}, 最近 {len(entries)} 条)")
        click.echo(f"{'DATETIME':<20} {'OPEN':>10} {'HIGH':>10} {'LOW':>10} {'CLOSE':>10} {'VOL':>10}")
        click.echo("─" * 75)
        for e in entries:
            click.echo(f"{e['datetime']:<20} {e['open']:>10} {e['high']:>10} {e['low']:>10} {e['close']:>10} {e['volume']:>10}")


# ── SEARCH ─────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--keywords", required=True, help="搜索关键词")
@click.pass_context
@_err
def search(ctx, keywords):
    """按关键词搜索股票代码。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {**_setup(t), "function": "SYMBOL_SEARCH", "keywords": keywords}
    data = _av_request(params)
    matches = data.get("bestMatches", [])
    results = []
    for m in matches:
        results.append({
            "symbol": m.get("1. symbol", ""),
            "name": m.get("2. name", ""),
            "type": m.get("3. type", ""),
            "region": m.get("4. region", ""),
            "currency": m.get("8. currency", ""),
            "match_score": m.get("9. matchScore", ""),
        })
    if as_json:
        _out({"results": results, "count": len(results), "keywords": keywords}, True)
    else:
        click.echo(f"搜索 '{keywords}' — 找到 {len(results)} 条结果")
        click.echo(f"{'SYMBOL':<10} {'TYPE':<8} {'REGION':<12} NAME")
        click.echo("─" * 65)
        for r in results:
            click.echo(f"{r['symbol']:<10} {r['type']:<8} {r['region']:<12} {r['name'][:40]}")


# ── FUNDAMENTALS ───────────────────────────────────────────────────────────

@cli.group()
def fundamentals():
    """基本面数据（income / balance / earnings）。"""


@fundamentals.command(name="income")
@click.option("--symbol", required=True, help="股票代码")
@click.pass_context
@_err
def fund_income(ctx, symbol):
    """获取利润表。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {**_setup(t), "function": "INCOME_STATEMENT", "symbol": symbol.upper()}
    data = _av_request(params)
    annual = data.get("annualReports", [])
    entries = []
    for r in annual[:5]:
        entries.append({
            "fiscal_date": r.get("fiscalDateEnding", ""),
            "total_revenue": r.get("totalRevenue", ""),
            "gross_profit": r.get("grossProfit", ""),
            "operating_income": r.get("operatingIncome", ""),
            "net_income": r.get("netIncome", ""),
            "ebitda": r.get("ebitda", ""),
        })
    if as_json:
        _out({"symbol": symbol.upper(), "annual_reports": entries, "count": len(entries)}, True)
    else:
        click.echo(f"📋 {symbol.upper()} 利润表 (年度)")
        click.echo(f"{'FISCAL_DATE':<14} {'REVENUE':>15} {'GROSS_PROFIT':>15} {'NET_INCOME':>15}")
        click.echo("─" * 65)
        for e in entries:
            click.echo(f"{e['fiscal_date']:<14} {e['total_revenue']:>15} {e['gross_profit']:>15} {e['net_income']:>15}")


@fundamentals.command(name="balance")
@click.option("--symbol", required=True, help="股票代码")
@click.pass_context
@_err
def fund_balance(ctx, symbol):
    """获取资产负债表。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {**_setup(t), "function": "BALANCE_SHEET", "symbol": symbol.upper()}
    data = _av_request(params)
    annual = data.get("annualReports", [])
    entries = []
    for r in annual[:5]:
        entries.append({
            "fiscal_date": r.get("fiscalDateEnding", ""),
            "total_assets": r.get("totalAssets", ""),
            "total_liabilities": r.get("totalLiabilities", ""),
            "total_equity": r.get("totalShareholderEquity", ""),
            "cash": r.get("cashAndCashEquivalentsAtCarryingValue", ""),
            "total_debt": r.get("shortLongTermDebtTotal", ""),
        })
    if as_json:
        _out({"symbol": symbol.upper(), "annual_reports": entries, "count": len(entries)}, True)
    else:
        click.echo(f"📋 {symbol.upper()} 资产负债表 (年度)")
        click.echo(f"{'FISCAL_DATE':<14} {'ASSETS':>15} {'LIABILITIES':>15} {'EQUITY':>15} {'CASH':>15}")
        click.echo("─" * 80)
        for e in entries:
            click.echo(f"{e['fiscal_date']:<14} {e['total_assets']:>15} {e['total_liabilities']:>15} {e['total_equity']:>15} {e['cash']:>15}")


@fundamentals.command(name="earnings")
@click.option("--symbol", required=True, help="股票代码")
@click.pass_context
@_err
def fund_earnings(ctx, symbol):
    """获取盈利数据。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {**_setup(t), "function": "EARNINGS", "symbol": symbol.upper()}
    data = _av_request(params)
    annual = data.get("annualEarnings", [])
    quarterly = data.get("quarterlyEarnings", [])
    annual_data = []
    for r in annual[:5]:
        annual_data.append({
            "fiscal_date": r.get("fiscalDateEnding", ""),
            "reported_eps": r.get("reportedEPS", ""),
        })
    quarterly_data = []
    for r in quarterly[:8]:
        quarterly_data.append({
            "fiscal_date": r.get("fiscalDateEnding", ""),
            "reported_date": r.get("reportedDate", ""),
            "reported_eps": r.get("reportedEPS", ""),
            "estimated_eps": r.get("estimatedEPS", ""),
            "surprise": r.get("surprise", ""),
            "surprise_pct": r.get("surprisePercentage", ""),
        })
    if as_json:
        _out({"symbol": symbol.upper(), "annual": annual_data, "quarterly": quarterly_data}, True)
    else:
        click.echo(f"📋 {symbol.upper()} 盈利数据")
        click.echo(f"\n年度 EPS:")
        for e in annual_data:
            click.echo(f"  {e['fiscal_date']}  EPS: {e['reported_eps']}")
        click.echo(f"\n季度 EPS (最近 {len(quarterly_data)} 期):")
        click.echo(f"  {'DATE':<12} {'REPORTED':>10} {'ESTIMATED':>10} {'SURPRISE':>10}")
        click.echo("  " + "─" * 50)
        for e in quarterly_data:
            click.echo(f"  {e['fiscal_date']:<12} {e['reported_eps']:>10} {e['estimated_eps']:>10} {e['surprise']:>10}")


# ── FOREX ──────────────────────────────────────────────────────────────────

@cli.group()
def forex():
    """外汇数据（rate）。"""


@forex.command(name="rate")
@click.option("--from-currency", required=True, help="源货币 (如 USD)")
@click.option("--to-currency", required=True, help="目标货币 (如 CNY)")
@click.pass_context
@_err
def forex_rate(ctx, from_currency, to_currency):
    """获取外汇实时汇率。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {
        **_setup(t),
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
    }
    data = _av_request(params)
    rate_data = data.get("Realtime Currency Exchange Rate", {})
    result = {
        "from_currency": rate_data.get("1. From_Currency Code", from_currency),
        "from_name": rate_data.get("2. From_Currency Name", ""),
        "to_currency": rate_data.get("3. To_Currency Code", to_currency),
        "to_name": rate_data.get("4. To_Currency Name", ""),
        "exchange_rate": rate_data.get("5. Exchange Rate", ""),
        "last_refreshed": rate_data.get("6. Last Refreshed", ""),
        "bid_price": rate_data.get("8. Bid Price", ""),
        "ask_price": rate_data.get("9. Ask Price", ""),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"💱 {result['from_currency']}/{result['to_currency']} = {result['exchange_rate']}")
        click.echo(f"  {result['from_name']} → {result['to_name']}")
        click.echo(f"  买入: {result['bid_price']}  卖出: {result['ask_price']}  更新: {result['last_refreshed']}")


# ── CRYPTO ─────────────────────────────────────────────────────────────────

@cli.group()
def crypto():
    """加密货币数据（daily）。"""


@crypto.command(name="daily")
@click.option("--symbol", required=True, help="加密货币代码 (如 BTC, ETH)")
@click.option("--market", default="USD", show_default=True, help="目标市场货币")
@click.pass_context
@_err
def crypto_daily(ctx, symbol, market):
    """获取加密货币日线数据。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    params = {
        **_setup(t),
        "function": "DIGITAL_CURRENCY_DAILY",
        "symbol": symbol.upper(),
        "market": market.upper(),
    }
    data = _av_request(params)
    meta = data.get("Meta Data", {})
    ts = data.get("Time Series (Digital Currency Daily)", {})
    entries = []
    mkt = market.upper()
    for date, vals in sorted(ts.items(), reverse=True)[:20]:
        entries.append({
            "date": date,
            "open": vals.get(f"1a. open ({mkt})", vals.get("1. open", "")),
            "high": vals.get(f"2a. high ({mkt})", vals.get("2. high", "")),
            "low": vals.get(f"3a. low ({mkt})", vals.get("3. low", "")),
            "close": vals.get(f"4a. close ({mkt})", vals.get("4. close", "")),
            "volume": vals.get("5. volume", ""),
            "market_cap": vals.get("6. market cap (USD)", ""),
        })
    if as_json:
        _out({"symbol": symbol.upper(), "market": mkt, "entries": entries, "count": len(entries)}, True)
    else:
        click.echo(f"🪙 {symbol.upper()}/{mkt} 日线 (最近 {len(entries)} 条)")
        click.echo(f"{'DATE':<12} {'OPEN':>12} {'HIGH':>12} {'LOW':>12} {'CLOSE':>12} {'VOLUME':>14}")
        click.echo("─" * 80)
        for e in entries:
            click.echo(f"{e['date']:<12} {e['open']:>12} {e['high']:>12} {e['low']:>12} {e['close']:>12} {e['volume']:>14}")


if __name__ == "__main__":
    cli()
