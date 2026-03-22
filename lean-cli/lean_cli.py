"""
cli-anything-lean — QuantConnect / Lean 量化平台 CLI
管理项目、回测、实盘和数据。
"""
import json
import sys
import os
import functools
from typing import Optional

import click

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

_VERSION = "1.0.0"
_DEFAULT_BASE_URL = "https://www.quantconnect.com/api/v2"


def _setup(token: str):
    """验证依赖可用。"""
    if not _REQUESTS_AVAILABLE:
        raise click.ClickException("requests 库未安装，请运行: pip install requests")
    return token


def _token(ctx) -> tuple:
    """获取 User ID 和 API Key。返回 (user_id, api_key)。"""
    user_id = ctx.obj.get("user_id") or os.environ.get("QUANTCONNECT_USER_ID")
    api_key = ctx.obj.get("token") or os.environ.get("QUANTCONNECT_API_KEY")
    if not user_id or not api_key:
        raise click.ClickException(
            "未提供 QuantConnect 凭证。\n"
            "方式1: --key API_KEY --user-id USER_ID\n"
            "方式2: export QUANTCONNECT_API_KEY=xxx && export QUANTCONNECT_USER_ID=xxx\n"
            "获取: https://www.quantconnect.com/account"
        )
    return user_id, api_key


def _base_url(ctx) -> str:
    """获取 API 基础 URL。"""
    return ctx.obj.get("base_url") or os.environ.get("QUANTCONNECT_BASE_URL") or _DEFAULT_BASE_URL


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


def _lean_err(fn):
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
            raise click.ClickException(f"QuantConnect API 错误 ({status}): {body}")
        except _requests.exceptions.ConnectionError:
            raise click.ClickException("无法连接到 QuantConnect API，请检查网络。")
        except Exception as e:
            raise click.ClickException(f"QuantConnect 错误: {str(e)}")
    return wrapper


def _api(ctx, method: str, endpoint: str, params: dict = None, body: dict = None) -> dict:
    """发送 API 请求（Basic Auth）。"""
    if not _REQUESTS_AVAILABLE:
        raise click.ClickException("requests 库未安装，请运行: pip install requests")
    user_id, api_key = _token(ctx)
    base = _base_url(ctx)
    url = f"{base}/{endpoint.lstrip('/')}"
    auth = (user_id, api_key)
    headers = {"Content-Type": "application/json"}

    if method.upper() == "GET":
        resp = _requests.get(url, auth=auth, headers=headers, params=params, timeout=30)
    elif method.upper() == "POST":
        resp = _requests.post(url, auth=auth, headers=headers, json=body or {}, timeout=30)
    elif method.upper() == "DELETE":
        resp = _requests.delete(url, auth=auth, headers=headers, json=body or {}, timeout=30)
    else:
        resp = _requests.request(method, url, auth=auth, headers=headers, json=body, params=params, timeout=30)

    resp.raise_for_status()
    data = resp.json()
    if not data.get("success", True):
        errors = data.get("errors", [])
        msg = "; ".join(errors) if errors else "未知错误"
        raise click.ClickException(f"QuantConnect 返回错误: {msg}")
    return data


# ── CLI 入口 ─────────────────────────────────────────────────────────────────

@click.group()
@click.option("--key", envvar="QUANTCONNECT_API_KEY", default=None, help="QuantConnect API Key")
@click.option("--user-id", envvar="QUANTCONNECT_USER_ID", default=None, help="QuantConnect User ID")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.option("--base-url", envvar="QUANTCONNECT_BASE_URL", default=None, help="API 基础 URL")
@click.pass_context
def cli(ctx, key, user_id, as_json, base_url):
    """cli-anything-lean — QuantConnect / Lean 量化平台 CLI\n
    管理项目、回测、实盘交易和数据。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["user_id"] = user_id
    ctx.obj["json"] = as_json
    ctx.obj["base_url"] = base_url


# ── 标准命令 ─────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
@_lean_err
def detect(ctx):
    """检测 QuantConnect API 凭证有效性。"""
    as_json = ctx.obj["json"]
    if not _REQUESTS_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install requests"}
        _out(result, as_json) if as_json else click.echo("❌ requests 库未安装")
        sys.exit(1)
    try:
        user_id, api_key = _token(ctx)
        _setup(api_key)
        resp = _api(ctx, "GET", "/authenticate")
        result = {
            "status": "ok",
            "user_id": user_id,
            "authenticated": resp.get("success", False),
            "endpoint": _base_url(ctx),
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ QuantConnect OK  user_id={user_id}  endpoint={result['endpoint']}")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {"cli_version": _VERSION, "requests_available": _REQUESTS_AVAILABLE}
    _out(result, as_json) if as_json else click.echo(f"cli-anything-lean v{_VERSION}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出 JSON Schema（Agent 发现用，无需认证）。"""
    info = {
        "name": "cli-anything-lean",
        "version": _VERSION,
        "description": "QuantConnect / Lean 量化平台 CLI - 项目、回测、实盘、数据管理",
        "requires_token": True,
        "token_env": ["QUANTCONNECT_API_KEY", "QUANTCONNECT_USER_ID"],
        "token_hint": "从 https://www.quantconnect.com/account 获取 User ID 和 API Key",
        "auth_method": "Basic Auth (user_id:api_key)",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "检测 API 凭证"},
            {"cmd": "version", "args": [], "desc": "版本信息"},
            {"cmd": "project list", "args": [], "desc": "列出项目"},
            {"cmd": "project create", "args": [
                {"name": "--name", "type": "str", "required": True},
                {"name": "--language", "type": "str", "choices": ["python", "csharp"], "default": "python"}
            ], "desc": "创建项目"},
            {"cmd": "project get", "args": [
                {"name": "--project-id", "type": "int", "required": True}
            ], "desc": "获取项目详情"},
            {"cmd": "backtest run", "args": [
                {"name": "--project-id", "type": "int", "required": True}
            ], "desc": "运行回测"},
            {"cmd": "backtest list", "args": [
                {"name": "--project-id", "type": "int", "required": True}
            ], "desc": "列出回测"},
            {"cmd": "backtest results", "args": [
                {"name": "--project-id", "type": "int", "required": True},
                {"name": "--backtest-id", "type": "str", "required": True}
            ], "desc": "获取回测结果"},
            {"cmd": "live list", "args": [], "desc": "列出实盘算法"},
            {"cmd": "live start", "args": [
                {"name": "--project-id", "type": "int", "required": True},
                {"name": "--brokerage", "type": "str", "choices": ["alpaca", "ib", "coinbase"]}
            ], "desc": "启动实盘交易"},
            {"cmd": "live stop", "args": [
                {"name": "--project-id", "type": "int", "required": True}
            ], "desc": "停止实盘算法"},
            {"cmd": "data list", "args": [], "desc": "列出可用数据库"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-lean --json project list",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── 项目管理 ─────────────────────────────────────────────────────────────────

@cli.group()
def project():
    """项目管理（list / create / get）。"""


@project.command(name="list")
@click.pass_context
@_lean_err
def project_list(ctx):
    """列出所有项目。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    resp = _api(ctx, "GET", "/projects/read")
    projects = resp.get("projects", [])

    if as_json:
        _out({"projects": projects, "count": len(projects)}, True)
    else:
        click.echo(f"{'ID':<10} {'LANGUAGE':<10} {'NAME':<40} MODIFIED")
        click.echo("─" * 80)
        for p in projects:
            click.echo(
                f"{p.get('projectId', '?'):<10} "
                f"{p.get('language', '?'):<10} "
                f"{p.get('name', '?'):<40} "
                f"{p.get('modified', '')}"
            )


@project.command(name="create")
@click.option("--name", required=True, help="项目名称")
@click.option("--language", default="python", type=click.Choice(["python", "csharp"], case_sensitive=False),
              help="编程语言")
@click.pass_context
@_lean_err
def project_create(ctx, name, language):
    """创建新项目。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    lang_map = {"python": "Py", "csharp": "C#"}
    resp = _api(ctx, "POST", "/projects/create", body={
        "name": name,
        "language": lang_map.get(language.lower(), "Py"),
    })
    proj = resp.get("projects", [{}])[0] if resp.get("projects") else resp

    if as_json:
        _out(proj, True)
    else:
        click.echo(f"✅ 项目已创建: {proj.get('projectId', 'N/A')}  {proj.get('name', name)}  ({language})")


@project.command(name="get")
@click.option("--project-id", required=True, type=int, help="项目 ID")
@click.pass_context
@_lean_err
def project_get(ctx, project_id):
    """获取项目详情。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    resp = _api(ctx, "GET", "/projects/read", params={"projectId": project_id})
    proj = resp.get("projects", [{}])[0] if resp.get("projects") else resp

    if as_json:
        _out(proj, True)
    else:
        click.echo(f"项目详情: #{project_id}")
        click.echo("─" * 50)
        for k in ["projectId", "name", "language", "created", "modified", "description"]:
            val = proj.get(k)
            if val is not None:
                click.echo(f"  {k:<15} {val}")
        files = proj.get("files", [])
        if files:
            click.echo(f"\n  文件 ({len(files)}):")
            for f in files:
                click.echo(f"    {f.get('name', '?')}")


# ── 回测管理 ─────────────────────────────────────────────────────────────────

@cli.group()
def backtest():
    """回测管理（run / list / results）。"""


@backtest.command(name="run")
@click.option("--project-id", required=True, type=int, help="项目 ID")
@click.pass_context
@_lean_err
def backtest_run(ctx, project_id):
    """运行回测。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    resp = _api(ctx, "POST", "/backtests/create", body={"projectId": project_id, "compileId": ""})
    bt = resp.get("backtest", resp)

    if as_json:
        _out(bt, True)
    else:
        click.echo(f"✅ 回测已启动")
        click.echo(f"  回测 ID: {bt.get('backtestId', 'N/A')}")
        click.echo(f"  项目 ID: {project_id}")
        click.echo(f"  状态: {bt.get('status', 'N/A')}")
        click.echo(f"  名称: {bt.get('name', 'N/A')}")


@backtest.command(name="list")
@click.option("--project-id", required=True, type=int, help="项目 ID")
@click.pass_context
@_lean_err
def backtest_list(ctx, project_id):
    """列出项目的回测记录。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    resp = _api(ctx, "GET", "/backtests/read", params={"projectId": project_id})
    backtests = resp.get("backtests", [])

    if as_json:
        _out({"backtests": backtests, "count": len(backtests), "project_id": project_id}, True)
    else:
        click.echo(f"项目 #{project_id} 的回测记录:")
        click.echo(f"{'ID':<40} {'STATUS':<12} {'NAME':<30}")
        click.echo("─" * 85)
        for bt in backtests:
            click.echo(
                f"{bt.get('backtestId', '?'):<40} "
                f"{bt.get('status', '?'):<12} "
                f"{bt.get('name', '?'):<30}"
            )


@backtest.command(name="results")
@click.option("--project-id", required=True, type=int, help="项目 ID")
@click.option("--backtest-id", required=True, help="回测 ID")
@click.pass_context
@_lean_err
def backtest_results(ctx, project_id, backtest_id):
    """获取回测结果。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    resp = _api(ctx, "GET", "/backtests/read", params={
        "projectId": project_id, "backtestId": backtest_id
    })
    bt = resp.get("backtest", resp)

    if as_json:
        _out(bt, True)
    else:
        click.echo(f"回测结果: {backtest_id}")
        click.echo("═" * 60)
        click.echo(f"  名称: {bt.get('name', 'N/A')}")
        click.echo(f"  状态: {bt.get('status', 'N/A')}")
        click.echo(f"  创建: {bt.get('created', 'N/A')}")
        stats = bt.get("statistics", {})
        if stats:
            click.echo("\n  统计数据:")
            for k, v in stats.items():
                click.echo(f"    {k:<30} {v}")
        runtime = bt.get("runtimeStatistics", {})
        if runtime:
            click.echo("\n  运行时统计:")
            for k, v in runtime.items():
                click.echo(f"    {k:<30} {v}")


# ── 实盘管理 ─────────────────────────────────────────────────────────────────

@cli.group()
def live():
    """实盘算法管理（list / start / stop）。"""


@live.command(name="list")
@click.pass_context
@_lean_err
def live_list(ctx):
    """列出实盘算法。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    resp = _api(ctx, "GET", "/live/read")
    algorithms = resp.get("live", [])

    if as_json:
        _out({"algorithms": algorithms, "count": len(algorithms)}, True)
    else:
        if not algorithms:
            click.echo("暂无运行中的实盘算法。")
            return
        click.echo(f"{'PROJECT':<10} {'DEPLOY ID':<40} {'STATUS':<12} BROKERAGE")
        click.echo("─" * 80)
        for algo in algorithms:
            click.echo(
                f"{algo.get('projectId', '?'):<10} "
                f"{algo.get('deployId', '?'):<40} "
                f"{algo.get('status', '?'):<12} "
                f"{algo.get('brokerage', 'N/A')}"
            )


@live.command(name="start")
@click.option("--project-id", required=True, type=int, help="项目 ID")
@click.option("--brokerage", required=True,
              type=click.Choice(["alpaca", "ib", "coinbase"], case_sensitive=False),
              help="券商: alpaca / ib / coinbase")
@click.pass_context
@_lean_err
def live_start(ctx, project_id, brokerage):
    """启动实盘交易。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])

    brokerage_map = {
        "alpaca": "AlpacaBrokerage",
        "ib": "InteractiveBrokersBrokerage",
        "coinbase": "CoinbaseBrokerage",
    }
    brokerage_id = brokerage_map.get(brokerage.lower(), brokerage)

    resp = _api(ctx, "POST", "/live/create", body={
        "projectId": project_id,
        "compileId": "",
        "serverType": "L-MICRO",
        "baseLiveAlgorithmSettings": {
            "id": brokerage_id,
            "environment": "live",
        },
        "versionId": "-1",
    })
    deploy = resp.get("live", resp)

    if as_json:
        _out(deploy, True)
    else:
        click.echo(f"✅ 实盘已启动")
        click.echo(f"  项目 ID: {project_id}")
        click.echo(f"  部署 ID: {deploy.get('deployId', 'N/A')}")
        click.echo(f"  券商: {brokerage}")
        click.echo(f"  状态: {deploy.get('status', 'N/A')}")


@live.command(name="stop")
@click.option("--project-id", required=True, type=int, help="项目 ID")
@click.pass_context
@_lean_err
def live_stop(ctx, project_id):
    """停止实盘算法。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    resp = _api(ctx, "POST", "/live/update/stop", body={"projectId": project_id})

    if as_json:
        _out({"status": "stopped", "project_id": project_id}, True)
    else:
        click.echo(f"✅ 实盘已停止  项目 ID: {project_id}")


# ── 数据管理 ─────────────────────────────────────────────────────────────────

@cli.group()
def data():
    """数据管理（list）。"""


@data.command(name="list")
@click.pass_context
@_lean_err
def data_list(ctx):
    """列出可用数据库。"""
    as_json = ctx.obj["json"]
    _setup(_token(ctx)[1])
    resp = _api(ctx, "GET", "/data/read")
    datasets = resp.get("data", resp.get("datasets", []))

    if as_json:
        _out({"datasets": datasets}, True)
    else:
        if isinstance(datasets, list):
            click.echo("可用数据库:")
            click.echo("─" * 60)
            for ds in datasets:
                if isinstance(ds, dict):
                    click.echo(f"  {ds.get('name', '?'):<30} {ds.get('description', '')}")
                else:
                    click.echo(f"  {ds}")
        elif isinstance(datasets, dict):
            click.echo("可用数据库:")
            click.echo("─" * 60)
            for k, v in datasets.items():
                click.echo(f"  {k:<30} {v if isinstance(v, str) else ''}")


if __name__ == "__main__":
    cli()
