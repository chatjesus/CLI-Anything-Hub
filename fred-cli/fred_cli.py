"""
cli-anything-fred — FRED (Federal Reserve Economic Data) API CLI
Wraps FRED REST API for AI Agent use.
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

_BASE = "https://api.stlouisfed.org/fred"


def _setup(token: str):
    if not _HTTP_AVAILABLE:
        raise click.ClickException("requests 未安装，请运行: pip install requests")
    return token


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("FRED_API_KEY")
    if not t:
        raise click.ClickException(
            "未提供 FRED API Key。\n"
            "方式1: --key YOUR_KEY\n"
            "方式2: export FRED_API_KEY=YOUR_KEY\n"
            "获取: https://fred.stlouisfed.org/docs/api/api_key.html"
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


def _err(fn):
    """统一捕获 FRED API 错误。"""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"FRED 请求错误: {e}")
        except KeyError as e:
            raise click.ClickException(f"FRED 响应解析错误: 缺少字段 {e}")
    return wrapper


def _get(endpoint: str, token: str, **params) -> dict:
    """发送 GET 请求到 FRED API。"""
    params["api_key"] = token
    params["file_type"] = "json"
    url = f"{_BASE}/{endpoint}"
    resp = requests.get(url, params=params, timeout=30)
    if resp.status_code != 200:
        error_msg = resp.json().get("error_message", resp.text) if resp.text else f"HTTP {resp.status_code}"
        raise click.ClickException(f"FRED API 错误 ({resp.status_code}): {error_msg}")
    return resp.json()


@click.group()
@click.option("--key", envvar="FRED_API_KEY", default=None, help="FRED API Key")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, key, as_json):
    """cli-anything-fred — FRED 联邦储备经济数据 CLI\n
    查询经济数据序列、分类、发布等。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = key
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
@_err
def detect(ctx):
    """检测 FRED API Key 有效性。"""
    as_json = ctx.obj["json"]
    if not _HTTP_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install requests"}
        _out(result, as_json) if as_json else click.echo("❌ requests 未安装")
        sys.exit(1)
    try:
        t = _token(ctx)
        _setup(t)
        data = _get("series/search", t, search_text="GDP", limit=1)
        count = data.get("count", 0)
        result = {
            "status": "ok",
            "search_test": "GDP",
            "results_found": count,
            "api": "FRED (Federal Reserve Economic Data)",
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ FRED OK  搜索 GDP 返回 {count} 条结果")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示版本信息。"""
    as_json = ctx.obj["json"]
    result = {
        "cli": "cli-anything-fred",
        "version": "1.0.0",
        "api": "FRED (Federal Reserve Economic Data)",
        "base_url": _BASE,
    }
    _out(result, as_json) if as_json else click.echo("cli-anything-fred v1.0.0  api=FRED")


# ── SERIES ───────────────────────────────────────────────────────────────────

@cli.group()
def series():
    """经济数据序列（get / observations / search）。"""


@series.command(name="get")
@click.option("--series-id", required=True, help="序列 ID（如 GDP, UNRATE, CPIAUCSL）")
@click.pass_context
@_err
def series_get(ctx, series_id):
    """获取序列基本信息。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    data = _get("series", t, series_id=series_id)
    serieses = data.get("seriess", [])
    if not serieses:
        raise click.ClickException(f"未找到序列: {series_id}")
    s = serieses[0]
    result = {
        "id": s.get("id"),
        "title": s.get("title"),
        "frequency": s.get("frequency"),
        "units": s.get("units"),
        "seasonal_adjustment": s.get("seasonal_adjustment"),
        "last_updated": s.get("last_updated"),
        "observation_start": s.get("observation_start"),
        "observation_end": s.get("observation_end"),
        "notes": (s.get("notes") or "")[:200],
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"  序列 ID:    {result['id']}")
        click.echo(f"  标题:       {result['title']}")
        click.echo(f"  频率:       {result['frequency']}")
        click.echo(f"  单位:       {result['units']}")
        click.echo(f"  季节调整:   {result['seasonal_adjustment']}")
        click.echo(f"  最后更新:   {result['last_updated']}")
        click.echo(f"  观测范围:   {result['observation_start']} ~ {result['observation_end']}")


@series.command(name="observations")
@click.option("--series-id", required=True, help="序列 ID")
@click.option("--start", "observation_start", default=None, help="起始日期 YYYY-MM-DD")
@click.option("--end", "observation_end", default=None, help="截止日期 YYYY-MM-DD")
@click.option("--sort-order", default="asc", type=click.Choice(["asc", "desc"]), help="排序")
@click.option("--limit", default=100, show_default=True, type=int, help="返回条数")
@click.pass_context
@_err
def series_observations(ctx, series_id, observation_start, observation_end, sort_order, limit):
    """获取序列观测数据（时间序列数据点）。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    params = {"series_id": series_id, "sort_order": sort_order, "limit": min(limit, 100000)}
    if observation_start:
        params["observation_start"] = observation_start
    if observation_end:
        params["observation_end"] = observation_end
    data = _get("series/observations", t, **params)
    observations = data.get("observations", [])
    rows = [{"date": o["date"], "value": o["value"]} for o in observations]
    if as_json:
        _out({"series_id": series_id, "count": len(rows), "observations": rows}, True)
    else:
        click.echo(f"{'DATE':<14} VALUE")
        click.echo("─" * 30)
        for r in rows:
            click.echo(f"{r['date']:<14} {r['value']}")
        click.echo(f"\n共 {len(rows)} 条")


@series.command(name="search")
@click.option("--text", required=True, help="搜索关键词")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
@_err
def series_search(ctx, text, limit):
    """搜索经济数据序列。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    data = _get("series/search", t, search_text=text, limit=min(limit, 1000))
    serieses = data.get("seriess", [])
    rows = [
        {
            "id": s.get("id"),
            "title": s.get("title"),
            "frequency": s.get("frequency_short"),
            "units": s.get("units_short"),
            "popularity": s.get("popularity"),
        }
        for s in serieses
    ]
    if as_json:
        _out({"query": text, "count": len(rows), "total": data.get("count", 0), "series": rows}, True)
    else:
        click.echo(f"{'ID':<18} {'FREQ':<6} {'POP':>4}  TITLE")
        click.echo("─" * 80)
        for r in rows:
            click.echo(f"{r['id']:<18} {(r['frequency'] or ''):<6} {r['popularity'] or 0:>4}  {r['title']}")
        click.echo(f"\n显示 {len(rows)} / {data.get('count', 0)} 条")


# ── CATEGORY ─────────────────────────────────────────────────────────────────

@cli.group()
def category():
    """分类目录（list）。"""


@category.command(name="list")
@click.option("--category-id", default=0, show_default=True, type=int, help="分类 ID（0=根目录）")
@click.pass_context
@_err
def category_list(ctx, category_id):
    """列出子分类。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    if category_id == 0:
        data = _get("category", t, category_id=0)
        cats = data.get("categories", [])
        children = _get("category/children", t, category_id=0).get("categories", [])
        cats = children if children else cats
    else:
        data = _get("category/children", t, category_id=category_id)
        cats = data.get("categories", [])
    rows = [{"id": c.get("id"), "name": c.get("name"), "parent_id": c.get("parent_id")} for c in cats]
    if as_json:
        _out({"parent_category_id": category_id, "categories": rows, "count": len(rows)}, True)
    else:
        click.echo(f"{'ID':>8}  {'PARENT':>8}  NAME")
        click.echo("─" * 60)
        for r in rows:
            click.echo(f"{r['id']:>8}  {r['parent_id'] or 0:>8}  {r['name']}")


# ── RELEASES ─────────────────────────────────────────────────────────────────

@cli.group()
def releases():
    """发布信息（list）。"""


@releases.command(name="list")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
@_err
def releases_list(ctx, limit):
    """列出所有数据发布。"""
    t = _token(ctx)
    _setup(t)
    as_json = ctx.obj["json"]
    data = _get("releases", t, limit=min(limit, 1000))
    rels = data.get("releases", [])
    rows = [
        {
            "id": r.get("id"),
            "name": r.get("name"),
            "link": r.get("link"),
            "press_release": r.get("press_release"),
        }
        for r in rels
    ]
    if as_json:
        _out({"releases": rows, "count": len(rows)}, True)
    else:
        click.echo(f"{'ID':>6}  NAME")
        click.echo("─" * 70)
        for r in rows:
            click.echo(f"{r['id']:>6}  {r['name']}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 API Key）。"""
    info = {
        "name": "cli-anything-fred",
        "version": "1.0.0",
        "description": "FRED (Federal Reserve Economic Data) CLI - series, observations, categories, releases",
        "requires_token": True,
        "token_env": "FRED_API_KEY",
        "token_hint": "Get your key at https://fred.stlouisfed.org/docs/api/api_key.html",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Verify API key validity"},
            {"cmd": "version", "args": [], "desc": "Show CLI version info"},
            {"cmd": "series get", "args": [{"name": "--series-id", "type": "str", "required": True}], "desc": "Get series metadata"},
            {"cmd": "series observations", "args": [
                {"name": "--series-id", "type": "str", "required": True},
                {"name": "--start", "type": "str", "desc": "YYYY-MM-DD"},
                {"name": "--end", "type": "str", "desc": "YYYY-MM-DD"},
                {"name": "--sort-order", "type": "str", "default": "asc", "choices": ["asc", "desc"]},
                {"name": "--limit", "type": "int", "default": 100},
            ], "desc": "Get time series data points"},
            {"cmd": "series search", "args": [
                {"name": "--text", "type": "str", "required": True},
                {"name": "--limit", "type": "int", "default": 10},
            ], "desc": "Search for series by keyword"},
            {"cmd": "category list", "args": [{"name": "--category-id", "type": "int", "default": 0}], "desc": "List child categories"},
            {"cmd": "releases list", "args": [{"name": "--limit", "type": "int", "default": 20}], "desc": "List data releases"},
        ],
        "json_flag": "--json",
        "example": "cli-anything-fred --json series get --series-id GDP",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
