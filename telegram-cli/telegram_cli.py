"""
cli-anything-telegram — Telegram Bot API CLI
Pure REST, no external dependencies beyond click. AI Agent ready.
"""
import json
import sys
import os
import urllib.request
import urllib.error
import urllib.parse
from typing import Optional

import click

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
    if not t:
        raise click.ClickException(
            "未提供 Telegram Bot token。\n"
            "方式1: --token <bot_token>\n"
            "方式2: export TELEGRAM_BOT_TOKEN=<token>\n"
            "获取: 在 Telegram 与 @BotFather 对话，/newbot"
        )
    return t


def _call(token: str, method: str, body: Optional[dict] = None, timeout: int = 30) -> dict:
    url = TELEGRAM_API.format(token=token, method=method)
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"} if data else {}, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode())
            if not result.get("ok"):
                raise click.ClickException(f"Telegram API 错误: {result.get('description', 'unknown')}")
            return result.get("result", {})
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            raise click.ClickException(f"Telegram API {e.code}: {err.get('description', body_text[:200])}")
        except (json.JSONDecodeError, KeyError):
            raise click.ClickException(f"Telegram API {e.code}: {body_text[:200]}")
    except urllib.error.URLError as e:
        raise click.ClickException(f"网络错误: {e.reason}")


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        click.echo(str(data) if not isinstance(data, str) else data)


def _format_user(u: dict) -> str:
    if not u:
        return "unknown"
    name = u.get("first_name", "")
    if u.get("last_name"):
        name += " " + u["last_name"]
    if u.get("username"):
        name += f" (@{u['username']})"
    return name


@click.group()
@click.option("--token", envvar="TELEGRAM_BOT_TOKEN", default=None, help="Telegram Bot Token")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, token, as_json):
    """cli-anything-telegram — Telegram Bot API CLI\n
    发消息/文件/通知、管理群组、获取更新。纯 REST，无需额外依赖。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
def detect(ctx):
    """检测 Bot Token 有效性。"""
    as_json = ctx.obj["json"]
    try:
        t = _token(ctx)
        data = _call(t, "getMe")
        result = {
            "status": "ok",
            "id": data["id"],
            "username": data.get("username"),
            "first_name": data.get("first_name"),
            "can_join_groups": data.get("can_join_groups"),
            "supports_inline": data.get("supports_inline_queries"),
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Telegram Bot OK  @{data.get('username')}  id={data['id']}")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示 Bot 信息。"""
    t = _token(ctx)
    data = _call(t, "getMe")
    as_json = ctx.obj["json"]
    _out(data, as_json) if as_json else click.echo(f"@{data.get('username')}  id={data['id']}  name={data.get('first_name')}")


# ── SEND ─────────────────────────────────────────────────────────────────────

@cli.group()
def send():
    """发送内容（text / photo / document / location / poll）。"""


@send.command(name="text")
@click.argument("chat_id")
@click.argument("text")
@click.option("--parse-mode", default="HTML", type=click.Choice(["HTML", "Markdown", "MarkdownV2", ""], case_sensitive=False))
@click.option("--reply-to", default=None, type=int, help="回复的消息 ID")
@click.option("--silent", is_flag=True, help="静默发送（不通知）")
@click.option("--protect", is_flag=True, help="禁止转发/截图")
@click.pass_context
def send_text(ctx, chat_id, text, parse_mode, reply_to, silent, protect):
    """发送文本消息。\n
    CHAT_ID 可以是 @username、群组/频道 ID（如 -100123456789）、用户 ID
    """
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {"chat_id": chat_id, "text": text}
    if parse_mode:
        body["parse_mode"] = parse_mode
    if reply_to:
        body["reply_to_message_id"] = reply_to
    if silent:
        body["disable_notification"] = True
    if protect:
        body["protect_content"] = True
    data = _call(t, "sendMessage", body)
    result = {"message_id": data["message_id"], "chat_id": chat_id, "date": data.get("date")}
    _out(result, as_json) if as_json else click.echo(f"✅ Sent  message_id={data['message_id']}")


@send.command(name="photo")
@click.argument("chat_id")
@click.argument("photo")
@click.option("--caption", default=None)
@click.option("--parse-mode", default="HTML")
@click.pass_context
def send_photo(ctx, chat_id, photo, caption, parse_mode):
    """发送图片（URL 或 file_id）。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {"chat_id": chat_id, "photo": photo}
    if caption:
        body["caption"] = caption
        body["parse_mode"] = parse_mode
    data = _call(t, "sendPhoto", body)
    result = {"message_id": data["message_id"], "chat_id": chat_id}
    _out(result, as_json) if as_json else click.echo(f"✅ Photo sent  message_id={data['message_id']}")


@send.command(name="document")
@click.argument("chat_id")
@click.argument("document")
@click.option("--caption", default=None)
@click.pass_context
def send_document(ctx, chat_id, document, caption):
    """发送文件（URL 或 file_id）。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {"chat_id": chat_id, "document": document}
    if caption:
        body["caption"] = caption
    data = _call(t, "sendDocument", body)
    result = {"message_id": data["message_id"], "chat_id": chat_id}
    _out(result, as_json) if as_json else click.echo(f"✅ Document sent  message_id={data['message_id']}")


@send.command(name="location")
@click.argument("chat_id")
@click.argument("latitude", type=float)
@click.argument("longitude", type=float)
@click.pass_context
def send_location(ctx, chat_id, latitude, longitude):
    """发送位置信息。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _call(t, "sendLocation", {"chat_id": chat_id, "latitude": latitude, "longitude": longitude})
    result = {"message_id": data["message_id"], "lat": latitude, "lon": longitude}
    _out(result, as_json) if as_json else click.echo(f"✅ Location sent  message_id={data['message_id']}")


@send.command(name="poll")
@click.argument("chat_id")
@click.argument("question")
@click.option("--option", "-o", "options", multiple=True, required=True, help="投票选项（可重复，最少2个）")
@click.option("--anonymous/--not-anonymous", default=True, show_default=True)
@click.option("--allows-multiple-answers", is_flag=True)
@click.pass_context
def send_poll(ctx, chat_id, question, options, anonymous, allows_multiple_answers):
    """发送投票。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    if len(options) < 2:
        raise click.UsageError("至少需要 2 个选项: --option A --option B")
    body = {
        "chat_id": chat_id,
        "question": question,
        "options": list(options),
        "is_anonymous": anonymous,
        "allows_multiple_answers": allows_multiple_answers,
    }
    data = _call(t, "sendPoll", body)
    result = {"message_id": data["message_id"], "poll_id": data.get("poll", {}).get("id")}
    _out(result, as_json) if as_json else click.echo(f"✅ Poll sent  message_id={data['message_id']}")


# ── CHAT ─────────────────────────────────────────────────────────────────────

@cli.group()
def chat():
    """聊天/群组管理（info / members / pin / unpin / kick / leave）。"""


@chat.command(name="info")
@click.argument("chat_id")
@click.pass_context
def chat_info(ctx, chat_id):
    """获取聊天/群组信息。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _call(t, "getChat", {"chat_id": chat_id})
    result = {
        "id": data["id"],
        "type": data.get("type"),
        "title": data.get("title") or data.get("first_name"),
        "username": data.get("username"),
        "description": data.get("description"),
        "member_count": data.get("approximate_member_count"),
    }
    _out(result, as_json) if as_json else click.echo("\n".join(f"  {k:<18} {v}" for k, v in result.items() if v is not None))


@chat.command(name="members")
@click.argument("chat_id")
@click.pass_context
def chat_members(ctx, chat_id):
    """获取群组成员数量。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    count = _call(t, "getChatMemberCount", {"chat_id": chat_id})
    result = {"chat_id": chat_id, "member_count": count}
    _out(result, as_json) if as_json else click.echo(f"Members: {count}")


@chat.command(name="pin")
@click.argument("chat_id")
@click.argument("message_id", type=int)
@click.option("--silent", is_flag=True)
@click.pass_context
def chat_pin(ctx, chat_id, message_id, silent):
    """置顶消息。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    _call(t, "pinChatMessage", {"chat_id": chat_id, "message_id": message_id, "disable_notification": silent})
    result = {"chat_id": chat_id, "message_id": message_id, "status": "pinned"}
    _out(result, as_json) if as_json else click.echo(f"✅ Pinned message {message_id}")


@chat.command(name="kick")
@click.argument("chat_id")
@click.argument("user_id", type=int)
@click.pass_context
def chat_kick(ctx, chat_id, user_id):
    """踢出成员（ban + unban）。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    _call(t, "banChatMember", {"chat_id": chat_id, "user_id": user_id})
    import time
    _call(t, "unbanChatMember", {"chat_id": chat_id, "user_id": user_id, "only_if_banned": True})
    result = {"chat_id": chat_id, "user_id": user_id, "status": "kicked"}
    _out(result, as_json) if as_json else click.echo(f"✅ Kicked user {user_id}")


# ── UPDATES ──────────────────────────────────────────────────────────────────

@cli.group()
def updates():
    """消息更新（poll / get）。"""


@updates.command(name="get")
@click.option("--offset", default=None, type=int, help="获取此 offset 之后的更新")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
def updates_get(ctx, offset, limit):
    """获取最新更新（长轮询一次）。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {"limit": min(limit, 100)}
    if offset is not None:
        body["offset"] = offset
    data = _call(t, "getUpdates", body)
    items = []
    for u in data:
        msg = u.get("message") or u.get("channel_post") or {}
        items.append({
            "update_id": u["update_id"],
            "chat_id": msg.get("chat", {}).get("id"),
            "from": _format_user(msg.get("from", {})),
            "text": msg.get("text", "")[:100],
            "date": msg.get("date"),
        })
    if as_json:
        _out({"updates": items, "count": len(items)}, True)
    else:
        for item in items:
            click.echo(f"[{item['update_id']}] {item['from']}: {item['text'][:60]}")


# ── BOT ───────────────────────────────────────────────────────────────────────

@cli.group()
def bot():
    """Bot 管理（commands / set-commands / webhook-set / webhook-del）。"""


@bot.command(name="commands")
@click.pass_context
def bot_commands(ctx):
    """列出 Bot 当前命令列表。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _call(t, "getMyCommands")
    if as_json:
        _out({"commands": data}, True)
    else:
        for cmd in data:
            click.echo(f"/{cmd['command']:<20} {cmd['description']}")


@bot.command(name="set-commands")
@click.option("--cmd", "-c", "cmds", multiple=True, help="命令（格式: command:description，可重复）")
@click.pass_context
def bot_set_commands(ctx, cmds):
    """设置 Bot 命令列表。\n
    示例: telegram-cli bot set-commands -c start:启动 -c help:帮助
    """
    t = _token(ctx)
    as_json = ctx.obj["json"]
    commands = []
    for cmd in cmds:
        if ":" in cmd:
            command, description = cmd.split(":", 1)
            commands.append({"command": command.strip("/"), "description": description})
    _call(t, "setMyCommands", {"commands": commands})
    result = {"commands_set": len(commands)}
    _out(result, as_json) if as_json else click.echo(f"✅ Set {len(commands)} commands")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 Token）。"""
    info = {
        "name": "cli-anything-telegram",
        "version": "1.0.0",
        "description": "Telegram Bot API CLI - send messages, photos, polls, manage groups, pure REST no extra deps",
        "requires_token": True,
        "token_env": "TELEGRAM_BOT_TOKEN",
        "token_hint": "Talk to @BotFather on Telegram, use /newbot",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Validate Bot token and get Bot info"},
            {"cmd": "version", "args": [], "desc": "Show Bot username and ID"},
            {"cmd": "send text", "args": [{"name": "CHAT_ID", "type": "str"}, {"name": "TEXT", "type": "str"}, {"name": "--parse-mode", "type": "str", "default": "HTML"}, {"name": "--reply-to", "type": "int"}, {"name": "--silent", "type": "flag"}], "desc": "Send text message (HTML/Markdown supported)"},
            {"cmd": "send photo", "args": [{"name": "CHAT_ID", "type": "str"}, {"name": "PHOTO", "type": "str"}, {"name": "--caption", "type": "str"}], "desc": "Send photo (URL or file_id)"},
            {"cmd": "send document", "args": [{"name": "CHAT_ID", "type": "str"}, {"name": "DOCUMENT", "type": "str"}, {"name": "--caption", "type": "str"}], "desc": "Send document (URL or file_id)"},
            {"cmd": "send location", "args": [{"name": "CHAT_ID", "type": "str"}, {"name": "LATITUDE", "type": "float"}, {"name": "LONGITUDE", "type": "float"}], "desc": "Send location coordinates"},
            {"cmd": "send poll", "args": [{"name": "CHAT_ID", "type": "str"}, {"name": "QUESTION", "type": "str"}, {"name": "--option", "type": "str", "multiple": True}], "desc": "Create a poll (>=2 options required)"},
            {"cmd": "chat info", "args": [{"name": "CHAT_ID", "type": "str"}], "desc": "Get chat/group info"},
            {"cmd": "chat members", "args": [{"name": "CHAT_ID", "type": "str"}], "desc": "Get member count"},
            {"cmd": "chat pin", "args": [{"name": "CHAT_ID", "type": "str"}, {"name": "MESSAGE_ID", "type": "int"}], "desc": "Pin a message"},
            {"cmd": "chat kick", "args": [{"name": "CHAT_ID", "type": "str"}, {"name": "USER_ID", "type": "int"}], "desc": "Kick (ban+unban) a member"},
            {"cmd": "updates get", "args": [{"name": "--offset", "type": "int"}, {"name": "--limit", "type": "int", "default": 10}], "desc": "Get latest updates (one long-poll)"},
            {"cmd": "bot commands", "args": [], "desc": "List Bot command menu"},
            {"cmd": "bot set-commands", "args": [{"name": "--cmd", "type": "str", "multiple": True}], "desc": "Set Bot command menu (format cmd:description)"},
        ],
        "json_flag": "--json",
        "example": "telegram-cli --json send text @mychannel 'Hello from Agent'",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
