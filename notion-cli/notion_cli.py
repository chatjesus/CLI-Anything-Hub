"""
cli-anything-notion — Notion REST API CLI
Wraps Notion API v1 for AI Agent use.
"""
import json
import sys
import os
import urllib.request
import urllib.error
from typing import Optional

import click

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


# ─── helpers ─────────────────────────────────────────────────────────────────

def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("NOTION_TOKEN") or os.environ.get("NOTION_API_KEY")
    if not t:
        raise click.ClickException(
            "未提供 Notion token。\n"
            "方式1: --token <Integration_Token>\n"
            "方式2: export NOTION_TOKEN=secret_xxxx\n"
            "获取: https://www.notion.so/my-integrations"
        )
    return t


def _request(method: str, path: str, token: str, body: Optional[dict] = None, timeout: int = 30) -> dict:
    url = NOTION_API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=_headers(token), method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            raise click.ClickException(f"Notion API 错误 {e.code}: {err.get('message', body_text)}")
        except (json.JSONDecodeError, KeyError):
            raise click.ClickException(f"Notion API 错误 {e.code}: {body_text[:200]}")
    except urllib.error.URLError as e:
        raise click.ClickException(f"网络错误: {e.reason}")


def _get(path: str, token: str) -> dict:
    return _request("GET", path, token)


def _post(path: str, token: str, body: dict) -> dict:
    return _request("POST", path, token, body)


def _patch(path: str, token: str, body: dict) -> dict:
    return _request("PATCH", path, token, body)


def _delete(path: str, token: str) -> dict:
    return _request("DELETE", path, token)


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        if isinstance(data, str):
            click.echo(data)
        elif isinstance(data, list):
            for item in data:
                click.echo(item if isinstance(item, str) else json.dumps(item, ensure_ascii=False))
        else:
            click.echo(str(data))


def _rich_text_content(rt_list: list) -> str:
    """从 rich_text 数组中提取纯文本"""
    return "".join(rt.get("plain_text", "") for rt in rt_list)


def _page_title(page: dict) -> str:
    props = page.get("properties", {})
    for prop in props.values():
        if prop.get("type") == "title":
            return _rich_text_content(prop.get("title", []))
    return "（无标题）"


def _db_title(db: dict) -> str:
    return _rich_text_content(db.get("title", []))


# ─── root ─────────────────────────────────────────────────────────────────────

@click.group()
@click.option("--token", envvar="NOTION_TOKEN", default=None,
              help="Notion Integration Token（或设置 NOTION_TOKEN 环境变量）")
@click.option("--json", "as_json", is_flag=True, help="以 JSON 格式输出（Agent 友好）")
@click.pass_context
def cli(ctx, token, as_json):
    """cli-anything-notion — Notion REST API CLI\n
    管理 Pages、Blocks、Databases、Comments。
    需要 Notion Integration Token（在 notion.so/my-integrations 创建）。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json


# ─── detect ───────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def detect(ctx):
    """检测 Notion API 可用性并验证 token。"""
    as_json = ctx.obj["json"]
    try:
        t = _token(ctx)
        data = _get("/users/me", t)
        result = {
            "status": "ok",
            "bot_id": data.get("id"),
            "bot_name": data.get("name"),
            "workspace_name": data.get("bot", {}).get("workspace_name"),
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Notion API OK  bot={result['bot_name']}  workspace={result['workspace_name']}")
    except click.ClickException as e:
        result = {"status": "error", "error": e.format_message()}
        _out(result, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


# ─── version ──────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def version(ctx):
    """显示 Notion API 版本信息。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get("/users/me", t)
    result = {
        "api_version": NOTION_VERSION,
        "bot_id": data.get("id"),
        "bot_name": data.get("name"),
        "workspace": data.get("bot", {}).get("workspace_name"),
    }
    _out(result, as_json) if as_json else click.echo(
        f"Notion API {NOTION_VERSION}  bot={result['bot_name']}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# SEARCH
# ══════════════════════════════════════════════════════════════════════════════

@cli.command()
@click.argument("query")
@click.option("--type", "filter_type", default=None,
              type=click.Choice(["page", "database"]), help="筛选类型")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
def search(ctx, query, filter_type, limit):
    """全局搜索 Pages 和 Databases。\n
    示例: notion-cli search "Meeting Notes"
    """
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {"query": query, "page_size": min(limit, 100)}
    if filter_type:
        body["filter"] = {"value": filter_type, "property": "object"}
    data = _post("/search", t, body)
    results = data.get("results", [])
    items = []
    for item in results:
        obj_type = item.get("object")
        if obj_type == "page":
            items.append({
                "type": "page",
                "id": item["id"],
                "title": _page_title(item),
                "url": item.get("url"),
                "last_edited": item.get("last_edited_time", "")[:10],
            })
        elif obj_type == "database":
            items.append({
                "type": "database",
                "id": item["id"],
                "title": _db_title(item),
                "url": item.get("url"),
                "last_edited": item.get("last_edited_time", "")[:10],
            })
    if as_json:
        _out({"results": items, "count": len(items)}, True)
    else:
        if not items:
            click.echo("（无结果）")
            return
        click.echo(f"{'TYPE':<12} {'TITLE':<45} LAST EDITED")
        click.echo("─" * 75)
        for item in items:
            click.echo(f"{item['type']:<12} {item['title'][:44]:<45} {item['last_edited']}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def page():
    """Page 管理（get / create / update / archive / append-text）。"""


@page.command(name="get")
@click.argument("page_id")
@click.pass_context
def page_get(ctx, page_id):
    """获取 Page 详情。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/pages/{page_id}", t)
    if as_json:
        _out(data, True)
    else:
        click.echo(f"ID:         {data['id']}")
        click.echo(f"Title:      {_page_title(data)}")
        click.echo(f"URL:        {data.get('url')}")
        click.echo(f"Created:    {data.get('created_time', '')[:19]}")
        click.echo(f"Edited:     {data.get('last_edited_time', '')[:19]}")
        click.echo(f"Archived:   {data.get('archived', False)}")


@page.command(name="create")
@click.option("--parent-page", default=None, help="父 Page ID（page_id）")
@click.option("--parent-db", default=None, help="父 Database ID（db_id）")
@click.option("--title", "-t", required=True, help="页面标题")
@click.option("--content", "-c", default=None, help="初始内容（纯文本）")
@click.pass_context
def page_create(ctx, parent_page, parent_db, title, content):
    """创建新 Page。需要指定 --parent-page 或 --parent-db。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    if not parent_page and not parent_db:
        raise click.UsageError("必须指定 --parent-page 或 --parent-db")
    if parent_page:
        parent = {"type": "page_id", "page_id": parent_page}
    else:
        parent = {"type": "database_id", "database_id": parent_db}
    properties = {
        "title": {
            "title": [{"type": "text", "text": {"content": title}}]
        }
    }
    children = []
    if content:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": content}}]
            }
        })
    body = {"parent": parent, "properties": properties}
    if children:
        body["children"] = children
    data = _post("/pages", t, body)
    result = {"id": data["id"], "title": title, "url": data.get("url")}
    _out(result, as_json) if as_json else click.echo(f"✅ Page created: {data.get('url')}")


@page.command(name="update-title")
@click.argument("page_id")
@click.argument("new_title")
@click.pass_context
def page_update_title(ctx, page_id, new_title):
    """更新 Page 标题。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body = {
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": new_title}}]
            }
        }
    }
    data = _patch(f"/pages/{page_id}", t, body)
    result = {"id": data["id"], "title": new_title}
    _out(result, as_json) if as_json else click.echo(f"✅ Title updated: {new_title}")


@page.command(name="archive")
@click.argument("page_id")
@click.option("--restore", is_flag=True, help="取消归档（恢复）")
@click.pass_context
def page_archive(ctx, page_id, restore):
    """归档（软删除）或恢复 Page。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body = {"archived": not restore}
    data = _patch(f"/pages/{page_id}", t, body)
    action = "restored" if restore else "archived"
    result = {"id": data["id"], "archived": data.get("archived"), "action": action}
    _out(result, as_json) if as_json else click.echo(f"✅ Page {action}")


@page.command(name="append-text")
@click.argument("page_id")
@click.argument("text")
@click.option("--type", "block_type", default="paragraph",
              type=click.Choice(["paragraph", "heading_1", "heading_2", "heading_3",
                                 "bulleted_list_item", "numbered_list_item", "to_do", "quote", "callout"]),
              help="Block 类型")
@click.pass_context
def page_append_text(ctx, page_id, text, block_type):
    """向 Page 末尾追加文本 Block。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    rich_text = [{"type": "text", "text": {"content": text}}]
    block = {"object": "block", "type": block_type, block_type: {"rich_text": rich_text}}
    if block_type == "to_do":
        block[block_type]["checked"] = False
    body = {"children": [block]}
    data = _patch(f"/blocks/{page_id}/children", t, body)
    added = data.get("results", [{}])
    result = {"added_blocks": len(added), "block_type": block_type}
    _out(result, as_json) if as_json else click.echo(f"✅ Appended {block_type}: {text[:50]}")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def block():
    """Block 管理（children / get / update / delete）。"""


@block.command(name="children")
@click.argument("block_id")
@click.option("--limit", default=50, show_default=True, type=int)
@click.pass_context
def block_children(ctx, block_id, limit):
    """列出 Block 的子 Blocks（即 Page 正文内容）。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/blocks/{block_id}/children?page_size={min(limit, 100)}", t)
    blocks = data.get("results", [])
    items = []
    for b in blocks:
        btype = b.get("type", "unknown")
        content = ""
        if btype in b:
            rt = b[btype].get("rich_text", [])
            content = _rich_text_content(rt)
        items.append({"id": b["id"], "type": btype, "content": content[:80]})
    if as_json:
        _out({"blocks": items, "count": len(items)}, True)
    else:
        click.echo(f"{'TYPE':<25} {'CONTENT'}")
        click.echo("─" * 80)
        for item in items:
            click.echo(f"{item['type']:<25} {item['content']}")


@block.command(name="get")
@click.argument("block_id")
@click.pass_context
def block_get(ctx, block_id):
    """获取 Block 详情。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/blocks/{block_id}", t)
    if as_json:
        _out(data, True)
    else:
        btype = data.get("type", "unknown")
        content = ""
        if btype in data:
            rt = data[btype].get("rich_text", [])
            content = _rich_text_content(rt)
        click.echo(f"ID:       {data['id']}")
        click.echo(f"Type:     {btype}")
        click.echo(f"Content:  {content}")


@block.command(name="delete")
@click.argument("block_id")
@click.pass_context
def block_delete(ctx, block_id):
    """删除 Block（归档，不可撤销）。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _delete(f"/blocks/{block_id}", t)
    result = {"id": block_id, "archived": data.get("archived", True)}
    _out(result, as_json) if as_json else click.echo(f"🗑  Block deleted: {block_id}")


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def database():
    """Database 管理（get / query / create-page）。"""


@database.command(name="get")
@click.argument("db_id")
@click.pass_context
def database_get(ctx, db_id):
    """获取 Database Schema 详情。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/databases/{db_id}", t)
    if as_json:
        _out(data, True)
    else:
        click.echo(f"ID:     {data['id']}")
        click.echo(f"Title:  {_db_title(data)}")
        click.echo(f"URL:    {data.get('url')}")
        click.echo("\n── Properties ──")
        for name, prop in data.get("properties", {}).items():
            click.echo(f"  {name:<30} {prop.get('type', '?')}")


@database.command(name="query")
@click.argument("db_id")
@click.option("--filter-prop", default=None, help="筛选属性名")
@click.option("--filter-value", default=None, help="筛选值（文字匹配）")
@click.option("--sort-prop", default=None, help="排序属性名")
@click.option("--sort-dir", default="descending", type=click.Choice(["ascending", "descending"]))
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def database_query(ctx, db_id, filter_prop, filter_value, sort_prop, sort_dir, limit):
    """查询 Database 条目。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {"page_size": min(limit, 100)}
    if filter_prop and filter_value:
        body["filter"] = {
            "property": filter_prop,
            "rich_text": {"contains": filter_value}
        }
    if sort_prop:
        body["sorts"] = [{"property": sort_prop, "direction": sort_dir}]
    data = _post(f"/databases/{db_id}/query", t, body)
    pages = data.get("results", [])
    items = [{
        "id": p["id"],
        "title": _page_title(p),
        "url": p.get("url"),
        "created": p.get("created_time", "")[:10],
        "edited": p.get("last_edited_time", "")[:10],
    } for p in pages]
    if as_json:
        _out({"results": items, "count": len(items), "has_more": data.get("has_more", False)}, True)
    else:
        click.echo(f"{'TITLE':<50} CREATED    EDITED")
        click.echo("─" * 80)
        for item in items:
            click.echo(f"{item['title'][:49]:<50} {item['created']}  {item['edited']}")
        if data.get("has_more"):
            click.echo("  … (还有更多结果，增加 --limit 查看)")


@database.command(name="create-page")
@click.argument("db_id")
@click.option("--title", "-t", required=True, help="条目标题")
@click.option("--prop", "-p", "props", multiple=True,
              help="额外属性（格式: PropName=Value，可重复）")
@click.pass_context
def database_create_page(ctx, db_id, title, props):
    """在 Database 中创建新条目（Page）。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    properties: dict = {
        "Name": {
            "title": [{"type": "text", "text": {"content": title}}]
        }
    }
    # Additional properties as rich_text
    for prop in props:
        if "=" in prop:
            k, v = prop.split("=", 1)
            properties[k] = {
                "rich_text": [{"type": "text", "text": {"content": v}}]
            }
    body = {
        "parent": {"database_id": db_id},
        "properties": properties,
    }
    data = _post("/pages", t, body)
    result = {"id": data["id"], "title": title, "url": data.get("url")}
    _out(result, as_json) if as_json else click.echo(f"✅ Created: {data.get('url')}")


# ══════════════════════════════════════════════════════════════════════════════
# USERS
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def users():
    """用户列表（list / me）。"""


@users.command(name="list")
@click.pass_context
def users_list(ctx):
    """列出工作空间所有成员。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get("/users", t)
    members = data.get("results", [])
    items = [{
        "id": u["id"],
        "name": u.get("name"),
        "type": u.get("type"),
        "email": u.get("person", {}).get("email") or u.get("bot", {}).get("owner", {}).get("user", {}).get("person", {}).get("email"),
    } for u in members]
    if as_json:
        _out({"users": items, "count": len(items)}, True)
    else:
        click.echo(f"{'NAME':<30} {'TYPE':<12} EMAIL")
        click.echo("─" * 70)
        for item in items:
            click.echo(f"{(item['name'] or ''):<30} {(item['type'] or ''):<12} {item['email'] or ''}")


@users.command(name="me")
@click.pass_context
def users_me(ctx):
    """显示当前集成 Bot 的信息。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get("/users/me", t)
    if as_json:
        _out(data, True)
    else:
        click.echo(f"ID:        {data.get('id')}")
        click.echo(f"Name:      {data.get('name')}")
        click.echo(f"Type:      {data.get('type')}")
        click.echo(f"Workspace: {data.get('bot', {}).get('workspace_name')}")


if __name__ == "__main__":
    cli()
