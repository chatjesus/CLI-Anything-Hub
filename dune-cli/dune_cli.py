"""
cli-anything-dune — Dune Analytics API CLI
通过 Dune Analytics REST API 执行链上查询、获取结果和搜索数据集。
"""
import json
import sys
import os
import functools
from typing import Optional

import click
import requests

_BASE = "https://api.dune.com/api/v1"
_VERSION = "1.0.0"


def _setup(token: str) -> dict:
    """返回带认证头的 headers。"""
    return {"X-Dune-Api-Key": token, "Content-Type": "application/json"}


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("DUNE_API_KEY")
    if not t:
        raise click.ClickException(
            "未提供 Dune API Key。\n"
            "方式1: --key your_api_key\n"
            "方式2: export DUNE_API_KEY=your_key\n"
            "获取: https://dune.com/settings/api"
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
            raise click.ClickException(f"Dune API 错误 ({resp.status_code if resp is not None else '?'}): {detail}")
        except requests.exceptions.ConnectionError:
            raise click.ClickException("无法连接 Dune API，请检查网络。")
        except requests.exceptions.Timeout:
            raise click.ClickException("Dune API 请求超时。")
    return wrapper


def _get(headers, path, params=None):
    r = requests.get(f"{_BASE}{path}", headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _post(headers, path, payload=None):
    r = requests.post(f"{_BASE}{path}", headers=headers, json=payload or {}, timeout=60)
    r.raise_for_status()
    return r.json()


@click.group()
@click.option("--key", envvar="DUNE_API_KEY", default=None, help="Dune Analytics API Key")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-dune — Dune Analytics 链上数据查询 CLI\n
    执行 SQL 查询、获取结果、搜索数据集。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
@_api_err
def detect(ctx):
    """检测 Dune API Key 有效性。"""
    as_json = ctx.obj["json"]
    try:
        t = _token(ctx)
        headers = _setup(t)
        data = _get(headers, "/auth/session")
        result = {
            "status": "ok",
            "username": data.get("username", ""),
            "plan": data.get("plan", ""),
            "api_key_prefix": t[:8] + "...",
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Dune OK  user={result['username']}  plan={result['plan']}")
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
    result = {"cli": "cli-anything-dune", "version": _VERSION, "api_base": _BASE}
    _out(result, as_json) if as_json else click.echo(f"cli-anything-dune v{_VERSION}  api={_BASE}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-dune",
        "version": _VERSION,
        "description": "Dune Analytics API CLI - execute on-chain SQL queries, get results, search datasets",
        "requires_token": True,
        "token_env": "DUNE_API_KEY",
        "token_hint": "API key from https://dune.com/settings/api",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Verify API key validity"},
            {"cmd": "version", "args": [], "desc": "Show CLI version"},
            {"cmd": "query execute", "args": [{"name": "--query-id", "type": "int", "required": True}], "desc": "Execute a Dune query"},
            {"cmd": "query status", "args": [{"name": "--execution-id", "type": "str", "required": True}], "desc": "Check execution status"},
            {"cmd": "query results", "args": [{"name": "--execution-id", "type": "str", "required": True}, {"name": "--limit", "type": "int", "default": 100}], "desc": "Get query results"},
            {"cmd": "query get", "args": [{"name": "--query-id", "type": "int", "required": True}], "desc": "Get query metadata"},
            {"cmd": "dataset search", "args": [{"name": "--keyword", "type": "str"}, {"name": "--contract-address", "type": "str"}, {"name": "--chain", "type": "str"}], "desc": "Search datasets"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-dune --key xxx --json query execute --query-id 1234",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ── QUERY ────────────────────────────────────────────────────────────────────

@cli.group()
def query():
    """查询管理（execute / status / results / get）。"""


@query.command(name="execute")
@click.option("--query-id", required=True, type=int, help="Dune 查询 ID")
@click.pass_context
@_api_err
def query_execute(ctx, query_id):
    """执行一个 Dune 查询。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _post(headers, f"/query/{query_id}/execute")
    result = {
        "execution_id": data.get("execution_id"),
        "state": data.get("state"),
        "query_id": query_id,
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"🚀 查询已提交  execution_id={result['execution_id']}  state={result['state']}")


@query.command(name="status")
@click.option("--execution-id", required=True, help="执行 ID")
@click.pass_context
@_api_err
def query_status(ctx, execution_id):
    """查看查询执行状态。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _get(headers, f"/execution/{execution_id}/status")
    result = {
        "execution_id": execution_id,
        "state": data.get("state"),
        "submitted_at": data.get("submitted_at"),
        "execution_started_at": data.get("execution_started_at"),
        "execution_ended_at": data.get("execution_ended_at"),
        "queue_position": data.get("queue_position"),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"📊 state={result['state']}  execution_id={execution_id}")
        if result["queue_position"]:
            click.echo(f"   队列位置: {result['queue_position']}")


@query.command(name="results")
@click.option("--execution-id", required=True, help="执行 ID")
@click.option("--limit", default=100, show_default=True, type=int, help="返回行数上限")
@click.pass_context
@_api_err
def query_results(ctx, execution_id, limit):
    """获取查询结果。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _get(headers, f"/execution/{execution_id}/results", params={"limit": limit})
    result_data = data.get("result", {})
    rows = result_data.get("rows", [])
    metadata = result_data.get("metadata", {})
    result = {
        "execution_id": execution_id,
        "state": data.get("state"),
        "row_count": len(rows),
        "columns": metadata.get("column_names", []),
        "rows": rows[:limit],
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"📊 结果 execution_id={execution_id}  rows={len(rows)}")
        cols = metadata.get("column_names", [])
        if cols:
            click.echo("  " + " | ".join(cols))
            click.echo("  " + "─" * (len(" | ".join(cols))))
        for row in rows[:20]:
            click.echo("  " + " | ".join(str(row.get(c, "")) for c in cols))
        if len(rows) > 20:
            click.echo(f"  ... 共 {len(rows)} 行（显示前 20 行）")


@query.command(name="get")
@click.option("--query-id", required=True, type=int, help="Dune 查询 ID")
@click.pass_context
@_api_err
def query_get(ctx, query_id):
    """获取查询元数据。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    data = _get(headers, f"/query/{query_id}")
    result = {
        "query_id": data.get("query_id"),
        "name": data.get("name"),
        "description": data.get("description", ""),
        "owner": data.get("owner", ""),
        "parameters": data.get("parameters", []),
        "is_archived": data.get("is_archived", False),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"📋 Query #{query_id}: {result['name']}")
        click.echo(f"   Owner: {result['owner']}")
        if result["description"]:
            click.echo(f"   Desc: {result['description'][:100]}")


# ── DATASET ──────────────────────────────────────────────────────────────────

@cli.group()
def dataset():
    """数据集搜索（search）。"""


@dataset.command(name="search")
@click.option("--keyword", default=None, help="搜索关键词")
@click.option("--contract-address", default=None, help="合约地址")
@click.option("--chain", default=None, type=click.Choice(["ethereum", "polygon", "arbitrum", "optimism", "bnb", "avalanche", "base", "solana"], case_sensitive=False), help="区块链")
@click.pass_context
@_api_err
def dataset_search(ctx, keyword, contract_address, chain):
    """搜索 Dune 数据集。"""
    t = _token(ctx)
    headers = _setup(t)
    as_json = ctx.obj["json"]
    params = {}
    if keyword:
        params["query"] = keyword
    if contract_address:
        params["contract_address"] = contract_address
    if chain:
        params["chain"] = chain
    data = _get(headers, "/datasets", params=params)
    datasets = data if isinstance(data, list) else data.get("datasets", data.get("results", []))
    result = {"count": len(datasets), "datasets": datasets[:50]}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"🔍 找到 {len(datasets)} 个数据集")
        for ds in datasets[:20]:
            name = ds.get("name", ds.get("title", ""))
            desc = ds.get("description", "")[:60]
            click.echo(f"  • {name}  {desc}")


if __name__ == "__main__":
    cli()
