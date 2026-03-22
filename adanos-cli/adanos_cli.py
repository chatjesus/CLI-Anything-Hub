"""
cli-anything-adanos — Adanos 多源情绪分析平台 CLI
聚合 News + Polymarket + X/Twitter + Reddit 的情绪数据。
"""
import json
import sys
import os
import functools
from datetime import datetime, timedelta
from typing import Optional

import click

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

_VERSION = "1.0.0"
_DEFAULT_BASE_URL = "https://api.adanos.ai/v1"


def _setup(token: str):
    """验证依赖可用。"""
    if not _REQUESTS_AVAILABLE:
        raise click.ClickException("requests 库未安装，请运行: pip install requests")
    return token


def _token(ctx) -> str:
    """获取 API Key。"""
    t = ctx.obj.get("token") or os.environ.get("ADANOS_API_KEY")
    if not t:
        raise click.ClickException(
            "未提供 Adanos API Key。\n"
            "方式1: --key YOUR_KEY\n"
            "方式2: export ADANOS_API_KEY=YOUR_KEY\n"
            "获取: https://app.adanos.ai/settings/api"
        )
    return t


def _base_url(ctx) -> str:
    """获取 API 基础 URL。"""
    return ctx.obj.get("base_url") or os.environ.get("ADANOS_BASE_URL") or _DEFAULT_BASE_URL


def _out(data, as_json: bool):
    """统一输出：JSON 或人类可读。"""
    if as_json:
        if hasattr(data, "to_dict"):
            data = data.to_dict()
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if isinstance(data, dict):
            click.echo(str(data))
        elif isinstance(data, list):
            for item in data:
                click.echo(str(item))
        else:
            click.echo(str(data))


def _adanos_err(fn):
    """统一错误处理装饰器。"""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except click.ClickException:
            raise
        except _requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "unknown"
            body = e.response.text[:300] if e.response is not None else ""
            raise click.ClickException(f"Adanos API 错误 ({status}): {body}")
        except _requests.exceptions.ConnectionError:
            raise click.ClickException("无法连接到 Adanos API，请检查网络或 base URL。")
        except Exception as e:
            raise click.ClickException(f"Adanos 错误: {str(e)}")
    return wrapper


def _api(ctx, method: str, endpoint: str, params: dict = None, body: dict = None) -> dict:
    """发送 API 请求。"""
    if not _REQUESTS_AVAILABLE:
        raise click.ClickException("requests 库未安装，请运行: pip install requests")
    token = _token(ctx)
    base = _base_url(ctx)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{base}/{endpoint.lstrip('/')}"

    if method.upper() == "GET":
        resp = _requests.get(url, headers=headers, params=params, timeout=30)
    elif method.upper() == "POST":
        resp = _requests.post(url, headers=headers, json=body or params, timeout=30)
    elif method.upper() == "DELETE":
        resp = _requests.delete(url, headers=headers, json=body or params, timeout=30)
    else:
        resp = _requests.request(method, url, headers=headers, json=body, params=params, timeout=30)

    resp.raise_for_status()
    if resp.status_code == 204:
        return {"status": "ok"}
    return resp.json()


# ── CLI 入口 ─────────────────────────────────────────────────────────────────

@click.group()
@click.option("--key", envvar="ADANOS_API_KEY", default=None, help="Adanos API Key")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.option("--base-url", envvar="ADANOS_BASE_URL", default=None, help="API 基础 URL")
@click.pass_context
def cli(ctx, key, as_json, base_url):
    """cli-anything-adanos — 多源情绪分析平台 CLI\n
    聚合 News、Polymarket、X/Twitter、Reddit 的情绪数据。
    支持情绪查询、每日简报、监控列表、告警、预测市场关联分析。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json
    ctx.obj["base_url"] = base_url


# ── 标准命令 ─────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
@_adanos_err
def detect(ctx):
    """检测 Adanos API 连接状态。"""
    as_json = ctx.obj["json"]
    if not _REQUESTS_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install requests"}
        _out(result, as_json) if as_json else click.echo("❌ requests 库未安装")
        sys.exit(1)
    try:
        token = _token(ctx)
        _setup(token)
        resp = _api(ctx, "GET", "/status")
        result = {
            "status": "ok",
            "endpoint": _base_url(ctx),
            "user": resp.get("user", "N/A"),
            "plan": resp.get("plan", "N/A"),
            "rate_limit": resp.get("rate_limit", "N/A"),
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Adanos OK  endpoint={result['endpoint']}  user={result['user']}")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {"cli_version": _VERSION, "requests_available": _REQUESTS_AVAILABLE}
    _out(result, as_json) if as_json else click.echo(f"cli-anything-adanos v{_VERSION}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出 JSON Schema（Agent 发现用，无需认证）。"""
    info = {
        "name": "cli-anything-adanos",
        "version": _VERSION,
        "description": "Adanos 多源情绪分析平台 CLI - News/Polymarket/X/Reddit 聚合分析",
        "requires_token": True,
        "token_env": "ADANOS_API_KEY",
        "token_hint": "从 https://app.adanos.ai/settings/api 获取",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "检测 API 连接"},
            {"cmd": "version", "args": [], "desc": "版本信息"},
            {"cmd": "sentiment", "args": [
                {"name": "--query", "type": "str", "required": True, "example": "AAPL"},
                {"name": "--sources", "type": "str", "default": "news,polymarket,x,reddit"}
            ], "desc": "查询情绪分析"},
            {"cmd": "briefing daily", "args": [
                {"name": "--date", "type": "str", "format": "YYYY-MM-DD"}
            ], "desc": "每日市场简报"},
            {"cmd": "briefing weekly", "args": [], "desc": "每周市场摘要"},
            {"cmd": "watchlist list", "args": [], "desc": "列出监控列表"},
            {"cmd": "watchlist add", "args": [
                {"name": "--name", "type": "str", "required": True},
                {"name": "--ticker", "type": "str", "required": True}
            ], "desc": "添加到监控列表"},
            {"cmd": "watchlist remove", "args": [
                {"name": "--name", "type": "str", "required": True},
                {"name": "--ticker", "type": "str", "required": True}
            ], "desc": "从监控列表移除"},
            {"cmd": "alerts list", "args": [], "desc": "列出活跃告警"},
            {"cmd": "alerts create", "args": [
                {"name": "--ticker", "type": "str", "required": True},
                {"name": "--threshold", "type": "float", "required": True},
                {"name": "--direction", "type": "str", "choices": ["above", "below"]}
            ], "desc": "创建情绪告警"},
            {"cmd": "predict", "args": [
                {"name": "--ticker", "type": "str", "required": True},
                {"name": "--market", "type": "str", "default": "polymarket"}
            ], "desc": "预测市场关联分析"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-adanos --json sentiment --query AAPL --sources news,x",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── 情绪分析 ─────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--query", required=True, help="查询主题或股票代码 (如 AAPL, Bitcoin)")
@click.option("--sources", default="news,polymarket,x,reddit",
              help="数据源，逗号分隔 (news,polymarket,x,reddit)")
@click.pass_context
@_adanos_err
def sentiment(ctx, query, sources):
    """获取多源情绪分析。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    source_list = [s.strip() for s in sources.split(",")]
    resp = _api(ctx, "POST", "/sentiment", body={"query": query, "sources": source_list})
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        click.echo(f"情绪分析: {query}")
        click.echo("─" * 60)
        overall = data.get("overall", {})
        click.echo(f"  综合评分: {overall.get('score', 'N/A')}  信号: {overall.get('signal', 'N/A')}")
        click.echo(f"  置信度: {overall.get('confidence', 'N/A')}  样本量: {overall.get('sample_size', 'N/A')}")
        click.echo()
        for src in data.get("sources", []):
            click.echo(f"  [{src.get('source', '?')}]  评分: {src.get('score', 'N/A')}  "
                       f"正面: {src.get('positive', 0)}  负面: {src.get('negative', 0)}  "
                       f"中性: {src.get('neutral', 0)}")


# ── 简报 ─────────────────────────────────────────────────────────────────────

@cli.group()
def briefing():
    """市场简报（daily / weekly）。"""


@briefing.command(name="daily")
@click.option("--date", default=None, help="日期 (YYYY-MM-DD)，默认今天")
@click.pass_context
@_adanos_err
def briefing_daily(ctx, date):
    """获取每日市场简报。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    resp = _api(ctx, "GET", "/briefing/daily", params={"date": date})
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        click.echo(f"每日简报: {date}")
        click.echo("═" * 60)
        click.echo(f"市场情绪: {data.get('market_sentiment', 'N/A')}")
        click.echo()
        for section in data.get("sections", []):
            click.echo(f"▸ {section.get('title', '未知')}")
            click.echo(f"  {section.get('summary', '')}")
            click.echo()
        top_movers = data.get("top_movers", [])
        if top_movers:
            click.echo("热门标的:")
            for m in top_movers:
                click.echo(f"  {m.get('ticker', '?'):<8} 情绪: {m.get('sentiment', 'N/A'):<8} "
                           f"变化: {m.get('change', 'N/A')}")


@briefing.command(name="weekly")
@click.pass_context
@_adanos_err
def briefing_weekly(ctx):
    """获取每周市场摘要。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    resp = _api(ctx, "GET", "/briefing/weekly")
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        click.echo("每周市场摘要")
        click.echo("═" * 60)
        click.echo(f"周期: {data.get('week_start', '?')} → {data.get('week_end', '?')}")
        click.echo(f"整体情绪: {data.get('overall_sentiment', 'N/A')}")
        click.echo()
        for highlight in data.get("highlights", []):
            click.echo(f"  • {highlight}")


# ── 监控列表 ─────────────────────────────────────────────────────────────────

@cli.group()
def watchlist():
    """监控列表管理（list / add / remove）。"""


@watchlist.command(name="list")
@click.pass_context
@_adanos_err
def watchlist_list(ctx):
    """列出所有监控列表。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    resp = _api(ctx, "GET", "/watchlists")
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        watchlists = data if isinstance(data, list) else data.get("watchlists", [])
        if not watchlists:
            click.echo("暂无监控列表。")
            return
        for wl in watchlists:
            tickers = ", ".join(wl.get("tickers", []))
            click.echo(f"  [{wl.get('name', '?')}]  {tickers or '(空)'}")


@watchlist.command(name="add")
@click.option("--name", required=True, help="监控列表名称")
@click.option("--ticker", required=True, help="要添加的标的代码")
@click.pass_context
@_adanos_err
def watchlist_add(ctx, name, ticker):
    """添加标的到监控列表。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    resp = _api(ctx, "POST", "/watchlists/add", body={"name": name, "ticker": ticker})
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        click.echo(f"✅ 已添加 {ticker} 到 [{name}]")


@watchlist.command(name="remove")
@click.option("--name", required=True, help="监控列表名称")
@click.option("--ticker", required=True, help="要移除的标的代码")
@click.pass_context
@_adanos_err
def watchlist_remove(ctx, name, ticker):
    """从监控列表移除标的。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    resp = _api(ctx, "POST", "/watchlists/remove", body={"name": name, "ticker": ticker})
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        click.echo(f"✅ 已从 [{name}] 移除 {ticker}")


# ── 告警 ─────────────────────────────────────────────────────────────────────

@cli.group()
def alerts():
    """情绪告警管理（list / create）。"""


@alerts.command(name="list")
@click.pass_context
@_adanos_err
def alerts_list(ctx):
    """列出活跃告警。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    resp = _api(ctx, "GET", "/alerts")
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        alert_list = data if isinstance(data, list) else data.get("alerts", [])
        if not alert_list:
            click.echo("暂无活跃告警。")
            return
        click.echo(f"{'TICKER':<10} {'DIRECTION':<10} {'THRESHOLD':>10} {'STATUS':<10} CREATED")
        click.echo("─" * 65)
        for a in alert_list:
            click.echo(
                f"{a.get('ticker', '?'):<10} "
                f"{a.get('direction', '?'):<10} "
                f"{str(a.get('threshold', '?')):>10} "
                f"{a.get('status', '?'):<10} "
                f"{a.get('created_at', '')}"
            )


@alerts.command(name="create")
@click.option("--ticker", required=True, help="标的代码")
@click.option("--threshold", required=True, type=float, help="情绪阈值 (-1.0 到 1.0)")
@click.option("--direction", required=True, type=click.Choice(["above", "below"]),
              help="触发方向: above=高于阈值, below=低于阈值")
@click.pass_context
@_adanos_err
def alerts_create(ctx, ticker, threshold, direction):
    """创建情绪告警。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    resp = _api(ctx, "POST", "/alerts", body={
        "ticker": ticker,
        "threshold": threshold,
        "direction": direction,
    })
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        alert_id = data.get("id", "N/A")
        click.echo(f"✅ 告警已创建: {alert_id}  {ticker} {direction} {threshold}")


# ── 预测市场关联 ─────────────────────────────────────────────────────────────

@cli.command()
@click.option("--ticker", required=True, help="标的代码")
@click.option("--market", default="polymarket", help="预测市场 (默认: polymarket)")
@click.pass_context
@_adanos_err
def predict(ctx, ticker, market):
    """获取预测市场关联分析。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx))
    resp = _api(ctx, "GET", "/predict", params={"ticker": ticker, "market": market})
    data = resp.get("data", resp)

    if as_json:
        _out(data, True)
    else:
        click.echo(f"预测市场关联: {ticker} ↔ {market}")
        click.echo("─" * 60)
        click.echo(f"  关联度: {data.get('correlation', 'N/A')}")
        click.echo(f"  预测方向: {data.get('predicted_direction', 'N/A')}")
        click.echo(f"  置信度: {data.get('confidence', 'N/A')}")
        click.echo()
        contracts = data.get("related_contracts", [])
        if contracts:
            click.echo("  相关合约:")
            for c in contracts:
                click.echo(f"    • {c.get('title', '?')}  概率: {c.get('probability', 'N/A')}")


if __name__ == "__main__":
    cli()
