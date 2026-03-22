"""
cli-anything-bloomberg — Bloomberg 金融数据 CLI
支持 BLPAPI（本地终端）和 HTTP MCP 双模式。
"""
import json
import sys
import os
import functools
from datetime import datetime, timedelta
from typing import Optional

import click

try:
    import blpapi
    _BLPAPI_AVAILABLE = True
except ImportError:
    _BLPAPI_AVAILABLE = False

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

_VERSION = "1.0.0"
_DEFAULT_MCP_URL = "https://bloomberg-mcp.agentputer.com/api/v1"


def _get_mode():
    """判断当前可用的连接模式。"""
    if _BLPAPI_AVAILABLE:
        return "blpapi"
    api_key = os.environ.get("BLOOMBERG_API_KEY")
    if api_key and _REQUESTS_AVAILABLE:
        return "http"
    return None


def _setup(token: Optional[str] = None):
    """初始化连接（BLPAPI 模式无需 token）。"""
    mode = _get_mode()
    if mode == "blpapi":
        return mode
    if mode == "http":
        return mode
    if token and _REQUESTS_AVAILABLE:
        return "http"
    return None


def _token(ctx) -> Optional[str]:
    """获取 API Key（仅 HTTP 模式需要）。"""
    return ctx.obj.get("token") or os.environ.get("BLOOMBERG_API_KEY")


def _base_url(ctx) -> str:
    """获取 MCP 服务端点 URL。"""
    return ctx.obj.get("base_url") or os.environ.get("BLOOMBERG_MCP_URL") or _DEFAULT_MCP_URL


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


def _bloomberg_err(fn):
    """统一错误处理装饰器。"""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except click.ClickException:
            raise
        except Exception as e:
            raise click.ClickException(f"Bloomberg 错误: {str(e)}")
    return wrapper


def _http_request(ctx, endpoint: str, params: dict = None, method: str = "GET") -> dict:
    """发送 HTTP 请求到 Bloomberg MCP 服务。"""
    if not _REQUESTS_AVAILABLE:
        raise click.ClickException("requests 库未安装，请运行: pip install requests")
    token = _token(ctx)
    if not token:
        raise click.ClickException(
            "未提供 Bloomberg API Key。\n"
            "方式1: --key YOUR_KEY\n"
            "方式2: export BLOOMBERG_API_KEY=YOUR_KEY"
        )
    base = _base_url(ctx)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{base}/{endpoint.lstrip('/')}"
    try:
        if method == "GET":
            resp = _requests.get(url, headers=headers, params=params, timeout=30)
        else:
            resp = _requests.post(url, headers=headers, json=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except _requests.exceptions.ConnectionError:
        raise click.ClickException(
            f"无法连接到 Bloomberg MCP 服务: {base}\n"
            "请检查 BLOOMBERG_MCP_URL 环境变量或确认服务可用。"
        )
    except _requests.exceptions.HTTPError as e:
        raise click.ClickException(f"HTTP 错误: {e.response.status_code} - {e.response.text[:200]}")


def _blpapi_session():
    """创建并启动 BLPAPI 会话。"""
    opts = blpapi.SessionOptions()
    opts.setServerHost("localhost")
    opts.setServerPort(8194)
    session = blpapi.Session(opts)
    if not session.start():
        raise click.ClickException(
            "无法连接到 Bloomberg Terminal。\n"
            "请确认: 1) Bloomberg Terminal 正在运行  2) BLPAPI 服务已启用"
        )
    return session


def _blpapi_reference(session, securities: list, fields: list) -> list:
    """通过 BLPAPI 获取参考数据。"""
    if not session.openService("//blp/refdata"):
        raise click.ClickException("无法打开 //blp/refdata 服务")
    svc = session.getService("//blp/refdata")
    req = svc.createRequest("ReferenceDataRequest")
    for sec in securities:
        req.getElement("securities").appendValue(sec)
    for fld in fields:
        req.getElement("fields").appendValue(fld)
    session.sendRequest(req)
    results = []
    while True:
        ev = session.nextEvent(5000)
        for msg in ev:
            if msg.hasElement("securityData"):
                sec_data = msg.getElement("securityData")
                for i in range(sec_data.numValues()):
                    sec = sec_data.getValueAsElement(i)
                    security = sec.getElementAsString("security")
                    field_data = sec.getElement("fieldData")
                    row = {"security": security}
                    for fld in fields:
                        try:
                            row[fld] = field_data.getElementAsFloat(fld)
                        except Exception:
                            try:
                                row[fld] = field_data.getElementAsString(fld)
                            except Exception:
                                row[fld] = None
                    results.append(row)
        if ev.eventType() == blpapi.Event.RESPONSE:
            break
    return results


def _blpapi_historical(session, security: str, fields: list, start: str, end: str, period: str) -> list:
    """通过 BLPAPI 获取历史数据。"""
    if not session.openService("//blp/refdata"):
        raise click.ClickException("无法打开 //blp/refdata 服务")
    svc = session.getService("//blp/refdata")
    req = svc.createRequest("HistoricalDataRequest")
    req.getElement("securities").appendValue(security)
    for fld in fields:
        req.getElement("fields").appendValue(fld)
    req.set("startDate", start.replace("-", ""))
    req.set("endDate", end.replace("-", ""))
    period_map = {"DAILY": "DAILY", "WEEKLY": "WEEKLY", "MONTHLY": "MONTHLY"}
    req.set("periodicitySelection", period_map.get(period.upper(), "DAILY"))
    session.sendRequest(req)
    results = []
    while True:
        ev = session.nextEvent(5000)
        for msg in ev:
            if msg.hasElement("securityData"):
                sec_data = msg.getElement("securityData")
                fd_array = sec_data.getElement("fieldData")
                for i in range(fd_array.numValues()):
                    fd = fd_array.getValueAsElement(i)
                    row = {"date": str(fd.getElementAsDatetime("date"))}
                    for fld in fields:
                        try:
                            row[fld] = fd.getElementAsFloat(fld)
                        except Exception:
                            row[fld] = None
                    results.append(row)
        if ev.eventType() == blpapi.Event.RESPONSE:
            break
    return results


# ── CLI 入口 ─────────────────────────────────────────────────────────────────

@click.group()
@click.option("--key", envvar="BLOOMBERG_API_KEY", default=None, help="Bloomberg API Key（HTTP MCP 模式）")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.option("--mcp-url", envvar="BLOOMBERG_MCP_URL", default=None, help="Bloomberg MCP 服务 URL")
@click.pass_context
def cli(ctx, key, as_json, mcp_url):
    """cli-anything-bloomberg — Bloomberg 金融数据 CLI\n
    支持 BLPAPI（本地 Terminal）和 HTTP MCP 双模式。
    获取参考数据、历史行情、实时行情、证券搜索等。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json
    ctx.obj["base_url"] = mcp_url


# ── 标准命令 ─────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
@_bloomberg_err
def detect(ctx):
    """检测 Bloomberg 连接状态。"""
    as_json = ctx.obj["json"]
    mode = _get_mode()

    if mode == "blpapi":
        try:
            session = _blpapi_session()
            session.stop()
            result = {"status": "ok", "mode": "blpapi", "message": "Bloomberg Terminal 连接正常"}
        except Exception as e:
            result = {"status": "error", "mode": "blpapi", "message": f"BLPAPI 可用但连接失败: {str(e)}"}
    elif mode == "http":
        try:
            resp = _http_request(ctx, "/status")
            result = {"status": "ok", "mode": "http", "endpoint": _base_url(ctx), "message": "MCP 服务连接正常"}
        except Exception:
            result = {"status": "partial", "mode": "http", "endpoint": _base_url(ctx),
                      "message": "API Key 已配置，但 MCP 服务暂不可达。请检查端点 URL。"}
    else:
        result = {
            "status": "not_configured",
            "blpapi_installed": _BLPAPI_AVAILABLE,
            "api_key_set": bool(os.environ.get("BLOOMBERG_API_KEY")),
            "message": "未检测到可用连接。",
            "fix": [
                "方式1 (本地终端): pip install blpapi 并启动 Bloomberg Terminal",
                "方式2 (HTTP MCP): export BLOOMBERG_API_KEY=your_key"
            ]
        }

    if as_json:
        _out(result, True)
    else:
        status_icon = {"ok": "✅", "partial": "⚠️", "error": "❌"}.get(result["status"], "❌")
        click.echo(f"{status_icon} Bloomberg {result.get('mode', 'N/A')}  {result['message']}")
        if result["status"] == "not_configured":
            for f in result.get("fix", []):
                click.echo(f"  → {f}")
    if result["status"] in ("error", "not_configured"):
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {
        "cli_version": _VERSION,
        "blpapi_available": _BLPAPI_AVAILABLE,
        "mode": _get_mode() or "none",
    }
    if _BLPAPI_AVAILABLE:
        try:
            result["blpapi_version"] = blpapi.VERSION_MAJOR * 10000 + blpapi.VERSION_MINOR * 100 + blpapi.VERSION_PATCH
        except Exception:
            result["blpapi_version"] = "unknown"
    _out(result, as_json) if as_json else click.echo(
        f"cli-anything-bloomberg v{_VERSION}  mode={result['mode']}  blpapi={'✓' if _BLPAPI_AVAILABLE else '✗'}"
    )


@cli.command()
@click.pass_context
def schema(ctx):
    """输出 JSON Schema（Agent 发现用，无需认证）。"""
    info = {
        "name": "cli-anything-bloomberg",
        "version": _VERSION,
        "description": "Bloomberg 金融数据 CLI - 参考数据、历史行情、实时行情、证券搜索",
        "requires_token": False,
        "token_env": "BLOOMBERG_API_KEY",
        "token_hint": "HTTP MCP 模式需要 API Key; BLPAPI 模式需要本地 Bloomberg Terminal",
        "modes": ["blpapi (本地 Terminal)", "http (MCP 远程)"],
        "commands": [
            {"cmd": "detect", "args": [], "desc": "检测连接状态"},
            {"cmd": "version", "args": [], "desc": "版本信息"},
            {"cmd": "reference", "args": [
                {"name": "--securities", "type": "str", "required": True, "example": "AAPL US Equity"},
                {"name": "--fields", "type": "str", "required": True, "example": "PX_LAST,PE_RATIO"}
            ], "desc": "获取参考数据"},
            {"cmd": "historical", "args": [
                {"name": "--security", "type": "str", "required": True},
                {"name": "--fields", "type": "str", "required": True},
                {"name": "--start", "type": "str", "required": True, "format": "YYYY-MM-DD"},
                {"name": "--end", "type": "str"},
                {"name": "--period", "type": "str", "choices": ["DAILY", "WEEKLY", "MONTHLY"]}
            ], "desc": "获取历史数据"},
            {"cmd": "market-data", "args": [
                {"name": "--securities", "type": "str", "required": True, "multiple": True}
            ], "desc": "实时行情快照"},
            {"cmd": "search", "args": [
                {"name": "--query", "type": "str", "required": True},
                {"name": "--max-results", "type": "int", "default": 10}
            ], "desc": "证券搜索"},
            {"cmd": "field-search", "args": [
                {"name": "--query", "type": "str", "required": True}
            ], "desc": "字段搜索"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-bloomberg --json reference --securities 'AAPL US Equity' --fields PX_LAST,PE_RATIO",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── 业务命令 ─────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--securities", required=True, help="证券代码，逗号分隔 (如 'AAPL US Equity,MSFT US Equity')")
@click.option("--fields", required=True, help="字段名，逗号分隔 (如 PX_LAST,PE_RATIO,MARKET_CAP)")
@click.pass_context
@_bloomberg_err
def reference(ctx, securities, fields):
    """获取参考数据（最新快照）。"""
    as_json = ctx.obj["json"]
    sec_list = [s.strip() for s in securities.split(",")]
    fld_list = [f.strip() for f in fields.split(",")]
    mode = _setup(_token(ctx))

    if mode == "blpapi":
        session = _blpapi_session()
        try:
            results = _blpapi_reference(session, sec_list, fld_list)
        finally:
            session.stop()
    elif mode == "http":
        resp = _http_request(ctx, "/reference", {
            "securities": sec_list, "fields": fld_list
        }, method="POST")
        results = resp.get("data", resp)
    else:
        raise click.ClickException(
            "未配置 Bloomberg 连接。\n"
            "运行 `cli-anything-bloomberg detect` 查看可用选项。"
        )

    if as_json:
        _out({"data": results, "count": len(results), "fields": fld_list}, True)
    else:
        header = f"{'SECURITY':<25}" + "".join(f" {f:<15}" for f in fld_list)
        click.echo(header)
        click.echo("─" * len(header))
        for row in results:
            line = f"{row.get('security', 'N/A'):<25}"
            for f in fld_list:
                val = row.get(f, "N/A")
                line += f" {str(val):<15}"
            click.echo(line)


@cli.command()
@click.option("--security", required=True, help="证券代码 (如 'AAPL US Equity')")
@click.option("--fields", required=True, help="字段名，逗号分隔 (如 PX_LAST,VOLUME)")
@click.option("--start", required=True, help="开始日期 (YYYY-MM-DD)")
@click.option("--end", default=None, help="结束日期 (YYYY-MM-DD)，默认今天")
@click.option("--period", default="DAILY", type=click.Choice(["DAILY", "WEEKLY", "MONTHLY"], case_sensitive=False),
              help="数据周期")
@click.pass_context
@_bloomberg_err
def historical(ctx, security, fields, start, end, period):
    """获取历史数据。"""
    as_json = ctx.obj["json"]
    if not end:
        end = datetime.now().strftime("%Y-%m-%d")
    fld_list = [f.strip() for f in fields.split(",")]
    mode = _setup(_token(ctx))

    if mode == "blpapi":
        session = _blpapi_session()
        try:
            results = _blpapi_historical(session, security, fld_list, start, end, period)
        finally:
            session.stop()
    elif mode == "http":
        resp = _http_request(ctx, "/historical", {
            "security": security, "fields": fld_list,
            "start_date": start, "end_date": end, "period": period.upper()
        }, method="POST")
        results = resp.get("data", resp)
    else:
        raise click.ClickException(
            "未配置 Bloomberg 连接。运行 `cli-anything-bloomberg detect` 查看可用选项。"
        )

    if as_json:
        _out({"security": security, "period": period, "data": results, "count": len(results)}, True)
    else:
        header = f"{'DATE':<12}" + "".join(f" {f:<15}" for f in fld_list)
        click.echo(f"证券: {security}  周期: {period}  {start} → {end}")
        click.echo(header)
        click.echo("─" * len(header))
        for row in results:
            line = f"{row.get('date', ''):<12}"
            for f in fld_list:
                val = row.get(f, "N/A")
                line += f" {str(val):<15}"
            click.echo(line)


@cli.command("market-data")
@click.option("--securities", required=True, multiple=True, help="证券代码（可多次指定）")
@click.pass_context
@_bloomberg_err
def market_data(ctx, securities):
    """获取实时行情快照。"""
    as_json = ctx.obj["json"]
    sec_list = []
    for s in securities:
        sec_list.extend([x.strip() for x in s.split(",")])

    default_fields = ["LAST_PRICE", "BID", "ASK", "VOLUME", "CHG_PCT_1D"]
    mode = _setup(_token(ctx))

    if mode == "blpapi":
        session = _blpapi_session()
        try:
            results = _blpapi_reference(session, sec_list, default_fields)
        finally:
            session.stop()
    elif mode == "http":
        resp = _http_request(ctx, "/market-data", {
            "securities": sec_list, "fields": default_fields
        }, method="POST")
        results = resp.get("data", resp)
    else:
        raise click.ClickException(
            "未配置 Bloomberg 连接。运行 `cli-anything-bloomberg detect` 查看可用选项。"
        )

    if as_json:
        _out({"data": results, "count": len(results)}, True)
    else:
        click.echo(f"{'SECURITY':<25} {'LAST':>10} {'BID':>10} {'ASK':>10} {'VOLUME':>12} {'CHG%':>8}")
        click.echo("─" * 80)
        for row in results:
            click.echo(
                f"{row.get('security', 'N/A'):<25} "
                f"{str(row.get('LAST_PRICE', 'N/A')):>10} "
                f"{str(row.get('BID', 'N/A')):>10} "
                f"{str(row.get('ASK', 'N/A')):>10} "
                f"{str(row.get('VOLUME', 'N/A')):>12} "
                f"{str(row.get('CHG_PCT_1D', 'N/A')):>8}"
            )


@cli.command()
@click.option("--query", required=True, help="搜索关键词 (如 'Apple', 'tech')")
@click.option("--max-results", default=10, type=int, help="最大返回数量")
@click.pass_context
@_bloomberg_err
def search(ctx, query, max_results):
    """搜索证券。"""
    as_json = ctx.obj["json"]
    mode = _setup(_token(ctx))

    if mode == "blpapi":
        session = _blpapi_session()
        try:
            if not session.openService("//blp/instruments"):
                raise click.ClickException("无法打开 //blp/instruments 服务")
            svc = session.getService("//blp/instruments")
            req = svc.createRequest("instrumentListRequest")
            req.set("query", query)
            req.set("maxResults", max_results)
            session.sendRequest(req)
            results = []
            while True:
                ev = session.nextEvent(5000)
                for msg in ev:
                    if msg.hasElement("results"):
                        res_elem = msg.getElement("results")
                        for i in range(res_elem.numValues()):
                            item = res_elem.getValueAsElement(i)
                            results.append({
                                "security": item.getElementAsString("security"),
                                "description": item.getElementAsString("description") if item.hasElement("description") else "",
                            })
                if ev.eventType() == blpapi.Event.RESPONSE:
                    break
        finally:
            session.stop()
    elif mode == "http":
        resp = _http_request(ctx, "/search", {"query": query, "max_results": max_results})
        results = resp.get("data", resp)
    else:
        raise click.ClickException(
            "未配置 Bloomberg 连接。运行 `cli-anything-bloomberg detect` 查看可用选项。"
        )

    if as_json:
        _out({"query": query, "results": results, "count": len(results)}, True)
    else:
        click.echo(f"搜索: '{query}'  结果: {len(results)} 条")
        click.echo(f"{'SECURITY':<30} DESCRIPTION")
        click.echo("─" * 70)
        for r in results:
            click.echo(f"{r.get('security', ''):<30} {r.get('description', '')}")


@cli.command("field-search")
@click.option("--query", required=True, help="字段搜索关键词 (如 'price', 'volume')")
@click.pass_context
@_bloomberg_err
def field_search(ctx, query):
    """搜索可用字段。"""
    as_json = ctx.obj["json"]
    mode = _setup(_token(ctx))

    if mode == "blpapi":
        session = _blpapi_session()
        try:
            if not session.openService("//blp/apiflds"):
                raise click.ClickException("无法打开 //blp/apiflds 服务")
            svc = session.getService("//blp/apiflds")
            req = svc.createRequest("FieldSearchRequest")
            req.set("searchSpec", query)
            session.sendRequest(req)
            results = []
            while True:
                ev = session.nextEvent(5000)
                for msg in ev:
                    if msg.hasElement("fieldData"):
                        fd = msg.getElement("fieldData")
                        for i in range(fd.numValues()):
                            item = fd.getValueAsElement(i)
                            results.append({
                                "id": item.getElementAsString("id") if item.hasElement("id") else "",
                                "mnemonic": item.getElementAsString("mnemonic") if item.hasElement("mnemonic") else "",
                                "description": item.getElementAsString("description") if item.hasElement("description") else "",
                            })
                if ev.eventType() == blpapi.Event.RESPONSE:
                    break
        finally:
            session.stop()
    elif mode == "http":
        resp = _http_request(ctx, "/field-search", {"query": query})
        results = resp.get("data", resp)
    else:
        raise click.ClickException(
            "未配置 Bloomberg 连接。运行 `cli-anything-bloomberg detect` 查看可用选项。"
        )

    if as_json:
        _out({"query": query, "fields": results, "count": len(results)}, True)
    else:
        click.echo(f"字段搜索: '{query}'  结果: {len(results)} 条")
        click.echo(f"{'MNEMONIC':<20} {'ID':<10} DESCRIPTION")
        click.echo("─" * 70)
        for r in results:
            click.echo(f"{r.get('mnemonic', ''):<20} {r.get('id', ''):<10} {r.get('description', '')}")


if __name__ == "__main__":
    cli()
