#!/usr/bin/env python3
"""
飞书（Lark）CLI — 基于飞书开放平台 REST API
覆盖：认证 / 消息 / 文档 / 日历 / 用户 / 群组

依赖：pip install click requests
凭证：需在飞书开放平台创建企业自建应用，获取 app_id + app_secret
      https://open.feishu.cn/app → 创建应用 → 凭证与基础信息
"""

import os
import sys
import json
import time
import click
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timezone

# ── 配置文件路径 ────────────────────────────────────────────────
CONFIG_PATH = Path.home() / ".feishu_cli.json"
BASE_URL = "https://open.feishu.cn/open-apis"

# ── 工具函数 ────────────────────────────────────────────────────

def _load_config() -> Dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def _save_config(cfg: Dict):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def _get_tenant_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token（机器人身份，企业级权限）。"""
    r = requests.post(f"{BASE_URL}/auth/v3/tenant_access_token/internal", json={
        "app_id": app_id, "app_secret": app_secret
    }, timeout=10)
    data = r.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取 token 失败: {data.get('msg')} (code={data.get('code')})\n"
                           f"请检查 app_id/app_secret 是否正确")
    return data["tenant_access_token"]


def _api(method: str, path: str, token: str = None, **kwargs) -> Dict:
    """通用 API 请求，自动附带 token 和错误处理。"""
    cfg = _load_config()
    if not token:
        token = cfg.get("token") or _refresh_token()
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    headers["Content-Type"] = "application/json; charset=utf-8"
    url = f"{BASE_URL}{path}"
    r = requests.request(method, url, headers=headers, timeout=15, **kwargs)
    data = r.json()
    if data.get("code") != 0:
        raise RuntimeError(f"API 错误 [{path}]: {data.get('msg')} (code={data.get('code')})")
    return data


def _refresh_token() -> str:
    cfg = _load_config()
    if not cfg.get("app_id") or not cfg.get("app_secret"):
        raise RuntimeError("未配置飞书凭证，请先运行: feishu-cli config setup")
    token = _get_tenant_token(cfg["app_id"], cfg["app_secret"])
    cfg["token"] = token
    cfg["token_time"] = time.time()
    _save_config(cfg)
    return token


def _out(data: Any, message: str, uj: bool):
    if uj:
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        if message:
            click.echo(message)
        if isinstance(data, dict):
            _print_dict(data)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                click.echo(f"  [{i}]")
                if isinstance(item, dict):
                    _print_dict(item, indent=2)
                else:
                    click.echo(f"    {item}")
        elif data is not None:
            click.echo(f"  {data}")


def _print_dict(d: dict, indent: int = 0):
    pad = " " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            click.echo(f"{pad}  {k}:")
            _print_dict(v, indent + 2)
        elif isinstance(v, list):
            click.echo(f"{pad}  {k}: [{len(v)} 项]")
        else:
            click.echo(f"{pad}  {k}: {v}")


# ════════════════════════════════════════════════════════════════
# CLI 入口
# ════════════════════════════════════════════════════════════════
@click.group()
@click.option("--json", "use_json", is_flag=True, help="JSON 格式输出")
@click.pass_context
def cli(ctx, use_json):
    """飞书 CLI — 通过开放平台 API 自动化操控飞书"""
    ctx.ensure_object(dict)
    ctx.obj["json"] = use_json


# ── 配置 ────────────────────────────────────────────────────────
@cli.group()
def config():
    """配置管理（凭证、token）。"""


@config.command("setup")
@click.option("--app-id",     prompt="飞书 App ID",     help="开放平台应用的 app_id")
@click.option("--app-secret", prompt="飞书 App Secret", hide_input=True, help="app_secret")
@click.pass_context
def config_setup(ctx, app_id, app_secret):
    """交互式配置 app_id 和 app_secret，并验证连接。"""
    uj = ctx.obj["json"]
    try:
        token = _get_tenant_token(app_id, app_secret)
        cfg = {"app_id": app_id, "app_secret": app_secret,
               "token": token, "token_time": time.time()}
        _save_config(cfg)
        _out({"status": "ok", "app_id": app_id, "config_path": str(CONFIG_PATH)},
             f"✓ 配置成功，token 已缓存\n  配置文件: {CONFIG_PATH}", uj)
    except Exception as e:
        click.echo(f"✗ 配置失败: {e}", err=True); sys.exit(1)


@config.command("show")
@click.pass_context
def config_show(ctx):
    """显示当前配置（隐藏 secret）。"""
    uj = ctx.obj["json"]
    cfg = _load_config()
    safe = {k: ("***" if "secret" in k.lower() else v)
            for k, v in cfg.items() if k != "token"}
    safe["token"] = cfg.get("token", "")[:20] + "..." if cfg.get("token") else "未配置"
    safe["config_path"] = str(CONFIG_PATH)
    _out(safe, "当前配置", uj)


@config.command("refresh")
@click.pass_context
def config_refresh(ctx):
    """强制刷新 tenant_access_token。"""
    uj = ctx.obj["json"]
    try:
        token = _refresh_token()
        _out({"token_prefix": token[:20] + "...", "refreshed_at": datetime.now().isoformat()},
             "✓ token 已刷新", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


# ── 消息 ────────────────────────────────────────────────────────
@cli.group()
def msg():
    """消息管理（发送/查询/撤回）。"""


@msg.command("send")
@click.option("--to",      required=True, help="接收方：用户 open_id / chat_id（群组）")
@click.option("--text",    "-t", default=None, help="纯文本内容")
@click.option("--card",    "-c", default=None, help="卡片消息 JSON 字符串")
@click.option("--file",    "-f", default=None, help="从文件读取消息内容")
@click.option("--receive-type", default="open_id",
              type=click.Choice(["open_id", "user_id", "email", "chat_id"]),
              help="接收方 ID 类型")
@click.pass_context
def msg_send(ctx, to, text, card, file, receive_type):
    """发送消息（文本/富文本/卡片）。"""
    uj = ctx.obj["json"]
    try:
        if file:
            content_raw = Path(file).read_text(encoding="utf-8")
            try:
                content = json.loads(content_raw)
                msg_type = "interactive"
                content_str = content_raw
            except Exception:
                text = content_raw
        if card:
            msg_type = "interactive"
            content_str = card
        elif text:
            msg_type = "text"
            content_str = json.dumps({"text": text}, ensure_ascii=False)
        else:
            click.echo("✗ 请提供 --text 或 --card 或 --file", err=True); sys.exit(1)

        data = _api("POST", "/im/v1/messages", params={"receive_id_type": receive_type},
                    json={"receive_id": to, "msg_type": msg_type, "content": content_str})
        msg_data = data.get("data", {}).get("message_id", "")
        _out({"message_id": msg_data, "to": to, "type": msg_type},
             f"✓ 消息已发送  message_id: {msg_data}", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@msg.command("send-card")
@click.option("--to",    required=True, help="chat_id 或 open_id")
@click.option("--title", required=True, help="卡片标题")
@click.option("--body",  required=True, help="卡片正文内容")
@click.option("--color", default="blue",
              type=click.Choice(["blue","green","red","yellow","purple","grey"]),
              help="标题栏颜色")
@click.option("--btn-text",  default=None, help="按钮文字")
@click.option("--btn-url",   default=None, help="按钮跳转链接")
@click.option("--receive-type", default="chat_id",
              type=click.Choice(["open_id","chat_id"]))
@click.pass_context
def msg_send_card(ctx, to, title, body, color, btn_text, btn_url, receive_type):
    """发送格式化卡片消息（支持标题/正文/按钮）。"""
    uj = ctx.obj["json"]
    try:
        elements = [{"tag": "div", "text": {"tag": "lark_md", "content": body}}]
        if btn_text and btn_url:
            elements.append({
                "tag": "action",
                "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": btn_text},
                             "url": btn_url, "type": "primary"}]
            })
        card = {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": title},
                       "template": color},
            "elements": elements
        }
        content_str = json.dumps(card, ensure_ascii=False)
        data = _api("POST", "/im/v1/messages", params={"receive_id_type": receive_type},
                    json={"receive_id": to, "msg_type": "interactive", "content": content_str})
        mid = data.get("data", {}).get("message_id", "")
        _out({"message_id": mid, "to": to, "title": title}, f"✓ 卡片消息已发送  {mid}", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@msg.command("list")
@click.option("--chat-id", required=True, help="群组 chat_id")
@click.option("--limit", default=20, help="条数限制")
@click.pass_context
def msg_list(ctx, chat_id, limit):
    """列出群组消息历史。"""
    uj = ctx.obj["json"]
    try:
        data = _api("GET", f"/im/v1/messages",
                    params={"container_id_type": "chat", "container_id": chat_id,
                            "page_size": limit, "sort_type": "ByCreateTimeDesc"})
        items = data.get("data", {}).get("items", [])
        result = [{"id": m.get("message_id"), "type": m.get("msg_type"),
                   "sender": m.get("sender", {}).get("id"),
                   "time": datetime.fromtimestamp(int(m.get("create_time", 0)) / 1000).strftime("%Y-%m-%d %H:%M"),
                   "content": m.get("body", {}).get("content", "")[:60]}
                  for m in items]
        _out(result, f"群组消息（最近 {len(result)} 条）", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@msg.command("recall")
@click.argument("message_id")
@click.pass_context
def msg_recall(ctx, message_id):
    """撤回消息。"""
    uj = ctx.obj["json"]
    try:
        _api("DELETE", f"/im/v1/messages/{message_id}")
        _out({"message_id": message_id, "status": "recalled"}, f"✓ 消息已撤回 {message_id}", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


# ── 群组 ────────────────────────────────────────────────────────
@cli.group()
def chat():
    """群组管理（列表/成员/创建）。"""


@chat.command("list")
@click.pass_context
def chat_list(ctx):
    """列出机器人所在的所有群组。"""
    uj = ctx.obj["json"]
    try:
        data = _api("GET", "/im/v1/chats", params={"page_size": 100})
        items = data.get("data", {}).get("items", [])
        result = [{"chat_id": c.get("chat_id"), "name": c.get("name"),
                   "type": c.get("chat_type"), "members": c.get("member_count")}
                  for c in items]
        _out(result, f"共 {len(result)} 个群组", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@chat.command("members")
@click.argument("chat_id")
@click.pass_context
def chat_members(ctx, chat_id):
    """查看群组成员。"""
    uj = ctx.obj["json"]
    try:
        data = _api("GET", f"/im/v1/chats/{chat_id}/members", params={"page_size": 100})
        items = data.get("data", {}).get("items", [])
        result = [{"open_id": m.get("member_id"), "name": m.get("name")} for m in items]
        _out(result, f"共 {len(result)} 名成员", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


# ── 文档 ────────────────────────────────────────────────────────
@cli.group()
def doc():
    """飞书文档（Wiki/Docs）管理。"""


@doc.command("create")
@click.option("--title",   required=True, help="文档标题")
@click.option("--content", "-c", default="", help="初始内容（Markdown）")
@click.pass_context
def doc_create(ctx, title, content):
    """创建新的飞书文档。"""
    uj = ctx.obj["json"]
    try:
        # 使用飞书文档 v1 API 创建空白文档
        data = _api("POST", "/docx/v1/documents",
                    json={"title": title})
        doc_info = data.get("data", {}).get("document", {})
        doc_id   = doc_info.get("document_id", "")
        # 写入初始内容
        if content:
            _api("POST", f"/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
                 json={"children": [{"block_type": 2,  # paragraph
                                     "paragraph": {"elements": [
                                         {"type": "text_run",
                                          "text_run": {"content": content}}
                                     ]}}],
                       "index": 0})
        url = f"https://bytedance.feishu.cn/docx/{doc_id}"
        _out({"document_id": doc_id, "title": title, "url": url},
             f"✓ 文档已创建\n  ID: {doc_id}\n  链接: {url}", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@doc.command("list")
@click.option("--folder-token", default=None, help="文件夹 token（不填则列出根目录）")
@click.pass_context
def doc_list(ctx, folder_token):
    """列出云空间文件列表。"""
    uj = ctx.obj["json"]
    try:
        params = {"page_size": 50}
        if folder_token:
            params["folder_token"] = folder_token
        data = _api("GET", "/drive/v1/files", params=params)
        items = data.get("data", {}).get("files", [])
        result = [{"name": f.get("name"), "type": f.get("type"),
                   "token": f.get("token"),
                   "modified": f.get("modified_time", ""),
                   "url": f.get("url", "")}
                  for f in items]
        _out(result, f"云空间共 {len(result)} 个文件", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@doc.command("get")
@click.argument("document_id")
@click.option("--format", "fmt", default="text",
              type=click.Choice(["text", "json", "markdown"]))
@click.pass_context
def doc_get(ctx, document_id, fmt):
    """读取文档内容。"""
    uj = ctx.obj["json"]
    try:
        data = _api("GET", f"/docx/v1/documents/{document_id}/raw_content")
        content = data.get("data", {}).get("content", "")
        if fmt == "json" or uj:
            _out({"document_id": document_id, "content": content}, "", uj)
        else:
            click.echo(content)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


# ── 日历 ────────────────────────────────────────────────────────
@cli.group()
def cal():
    """日历管理（日程 CRUD）。"""


@cal.command("list")
@click.option("--start", default=None, help="开始时间 YYYY-MM-DD，默认今天")
@click.option("--end",   default=None, help="结束时间 YYYY-MM-DD，默认 7 天后")
@click.pass_context
def cal_list(ctx, start, end):
    """列出日程。"""
    uj = ctx.obj["json"]
    try:
        now = datetime.now()
        start_ts = int(datetime.strptime(start, "%Y-%m-%d").timestamp()) if start \
                   else int(now.replace(hour=0, minute=0, second=0).timestamp())
        end_ts = int(datetime.strptime(end, "%Y-%m-%d").timestamp()) if end \
                 else start_ts + 7 * 86400
        # 先获取主日历 ID
        cal_data = _api("GET", "/calendar/v4/calendars/primary")
        cal_id = cal_data.get("data", {}).get("calendar", {}).get("calendar_id", "primary")
        data = _api("GET", f"/calendar/v4/calendars/{cal_id}/events",
                    params={"start_time": str(start_ts), "end_time": str(end_ts),
                            "page_size": 50})
        items = data.get("data", {}).get("items", [])
        result = [{"summary": e.get("summary"), "event_id": e.get("event_id"),
                   "start": e.get("start_time", {}).get("timestamp", ""),
                   "end":   e.get("end_time",   {}).get("timestamp", ""),
                   "status": e.get("status")}
                  for e in items]
        # 转换时间戳
        for r in result:
            for k in ("start", "end"):
                if r[k]:
                    r[k] = datetime.fromtimestamp(int(r[k])).strftime("%Y-%m-%d %H:%M")
        _out(result, f"日程共 {len(result)} 条", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@cal.command("add")
@click.option("--title",    required=True, help="日程标题")
@click.option("--start",    required=True, help="开始时间 YYYY-MM-DD HH:MM")
@click.option("--end",      required=True, help="结束时间 YYYY-MM-DD HH:MM")
@click.option("--desc",     default="",   help="日程描述")
@click.option("--location", default="",   help="地点")
@click.option("--attendee", "-a", multiple=True, help="参与者 open_id（可多次）")
@click.pass_context
def cal_add(ctx, title, start, end, desc, location, attendee):
    """创建日程。"""
    uj = ctx.obj["json"]
    try:
        start_ts = str(int(datetime.strptime(start, "%Y-%m-%d %H:%M").timestamp()))
        end_ts   = str(int(datetime.strptime(end,   "%Y-%m-%d %H:%M").timestamp()))
        cal_data = _api("GET", "/calendar/v4/calendars/primary")
        cal_id = cal_data.get("data", {}).get("calendar", {}).get("calendar_id", "primary")
        body = {"summary": title, "description": desc,
                "start_time": {"timestamp": start_ts, "timezone": "Asia/Shanghai"},
                "end_time":   {"timestamp": end_ts,   "timezone": "Asia/Shanghai"}}
        if location:
            body["location"] = {"name": location}
        if attendee:
            body["attendees"] = [{"type": "user", "user_id": a} for a in attendee]
        data = _api("POST", f"/calendar/v4/calendars/{cal_id}/events", json=body)
        event = data.get("data", {}).get("event", {})
        _out({"event_id": event.get("event_id"), "title": title,
              "start": start, "end": end},
             f"✓ 日程已创建: {title}  [{start} → {end}]", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@cal.command("delete")
@click.argument("event_id")
@click.pass_context
def cal_delete(ctx, event_id):
    """删除日程。"""
    uj = ctx.obj["json"]
    try:
        cal_data = _api("GET", "/calendar/v4/calendars/primary")
        cal_id = cal_data.get("data", {}).get("calendar", {}).get("calendar_id", "primary")
        _api("DELETE", f"/calendar/v4/calendars/{cal_id}/events/{event_id}")
        _out({"event_id": event_id, "status": "deleted"}, f"✓ 日程已删除 {event_id}", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


# ── 用户 ────────────────────────────────────────────────────────
@cli.group()
def user():
    """用户信息查询。"""


@user.command("me")
@click.pass_context
def user_me(ctx):
    """查看当前 Bot 身份信息。"""
    uj = ctx.obj["json"]
    try:
        data = _api("GET", "/bot/v3/info")
        bot = data.get("data", {}).get("bot", {})
        _out({"name": bot.get("app_name"), "open_id": bot.get("open_id"),
              "avatar": bot.get("avatar_url")},
             f"Bot 信息: {bot.get('app_name')}", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@user.command("get")
@click.argument("user_id")
@click.option("--id-type", default="open_id",
              type=click.Choice(["open_id","user_id","email","mobile"]))
@click.pass_context
def user_get(ctx, user_id, id_type):
    """根据 ID 查询用户信息。"""
    uj = ctx.obj["json"]
    try:
        data = _api("GET", "/contact/v3/users", params={"user_ids": user_id,
                                                         "user_id_type": id_type})
        items = data.get("data", {}).get("items", [])
        if not items:
            click.echo("未找到用户"); return
        u = items[0]
        _out({"name": u.get("name"), "open_id": u.get("open_id"),
              "email": u.get("email"), "mobile": u.get("mobile"),
              "department": u.get("department_ids", [])},
             f"用户: {u.get('name')}", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


@user.command("search")
@click.argument("keyword")
@click.pass_context
def user_search(ctx, keyword):
    """搜索用户（按名字/邮箱）。"""
    uj = ctx.obj["json"]
    try:
        data = _api("GET", "/search/v1/user", params={"query": keyword, "page_size": 20})
        items = data.get("data", {}).get("users", [])
        result = [{"name": u.get("name"), "open_id": u.get("open_id"),
                   "department": u.get("department_path", "")} for u in items]
        _out(result, f"找到 {len(result)} 名用户", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


# ── 通知快捷命令 ────────────────────────────────────────────────
@cli.command("notify")
@click.option("--to",      required=True, help="chat_id 或 open_id")
@click.option("--title",   required=True, help="通知标题")
@click.option("--content", "-c", required=True, help="通知内容（支持 Markdown）")
@click.option("--level",   default="info",
              type=click.Choice(["info","success","warning","error"]),
              help="通知级别（影响卡片颜色）")
@click.option("--receive-type", default="chat_id",
              type=click.Choice(["open_id","chat_id"]))
@click.pass_context
def notify(ctx, to, title, content, level, receive_type):
    """一键发送格式化通知卡片（最常用快捷命令）。"""
    uj = ctx.obj["json"]
    color_map = {"info": "blue", "success": "green", "warning": "yellow", "error": "red"}
    emoji_map = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "🚨"}
    try:
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text",
                          "content": f"{emoji_map[level]} {title}"},
                "template": color_map[level]
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": content}},
                {"tag": "note", "elements": [
                    {"tag": "plain_text",
                     "content": f"发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
                ]}
            ]
        }
        data = _api("POST", "/im/v1/messages",
                    params={"receive_id_type": receive_type},
                    json={"receive_id": to, "msg_type": "interactive",
                          "content": json.dumps(card, ensure_ascii=False)})
        mid = data.get("data", {}).get("message_id", "")
        _out({"message_id": mid, "level": level, "title": title},
             f"✓ 通知已发送  [{level.upper()}] {title}", uj)
    except Exception as e:
        click.echo(f"✗ {e}", err=True); sys.exit(1)


if __name__ == "__main__":
    cli(obj={})
