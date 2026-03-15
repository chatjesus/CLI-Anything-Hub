"""
cli-anything-discord — Discord Bot API CLI
Wraps Discord REST API via requests (no heavy library needed) for AI Agent use.
"""
import json
import sys
import os
import urllib.request
import urllib.error
from typing import Optional

import click

DISCORD_API = "https://discord.com/api/v10"


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "cli-anything-discord/1.0.0",
    }


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("DISCORD_BOT_TOKEN") or os.environ.get("DISCORD_TOKEN")
    if not t:
        raise click.ClickException(
            "未提供 Discord Bot token。\n"
            "方式1: --token <bot_token>\n"
            "方式2: export DISCORD_BOT_TOKEN=<token>\n"
            "获取: https://discord.com/developers/applications → Bot → Token"
        )
    return t


def _request(method: str, path: str, token: str, body: Optional[dict] = None, timeout: int = 30) -> dict:
    url = DISCORD_API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=_headers(token), method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            raise click.ClickException(f"Discord API {e.code}: {err.get('message', body_text[:200])}")
        except (json.JSONDecodeError, KeyError):
            raise click.ClickException(f"Discord API {e.code}: {body_text[:200]}")
    except urllib.error.URLError as e:
        raise click.ClickException(f"网络错误: {e.reason}")


def _get(path: str, t: str) -> dict:
    return _request("GET", path, t)


def _post(path: str, t: str, body: dict) -> dict:
    return _request("POST", path, t, body)


def _patch(path: str, t: str, body: dict) -> dict:
    return _request("PATCH", path, t, body)


def _delete(path: str, t: str) -> dict:
    return _request("DELETE", path, t)


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        click.echo(str(data) if not isinstance(data, str) else data)


@click.group()
@click.option("--token", envvar="DISCORD_BOT_TOKEN", default=None, help="Discord Bot Token")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, token, as_json):
    """cli-anything-discord — Discord Bot API CLI\n
    发消息、管理服务器频道、角色、成员、Webhook 等。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
def detect(ctx):
    """检测 Discord Bot Token 有效性。"""
    as_json = ctx.obj["json"]
    try:
        t = _token(ctx)
        data = _get("/users/@me", t)
        result = {"status": "ok", "id": data["id"], "username": data["username"], "bot": data.get("bot", True)}
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Discord Bot OK  username={data['username']}#{data.get('discriminator','0')}")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示 Bot 信息。"""
    t = _token(ctx)
    data = _get("/users/@me", t)
    as_json = ctx.obj["json"]
    _out(data, as_json) if as_json else click.echo(f"Bot: {data['username']}  ID: {data['id']}")


# ── GUILDS ───────────────────────────────────────────────────────────────────

@cli.group()
def guild():
    """服务器（Guild）管理（list / info / channels / members / roles）。"""


@guild.command(name="list")
@click.pass_context
def guild_list(ctx):
    """列出 Bot 加入的所有服务器。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get("/users/@me/guilds", t)
    guilds = [{"id": g["id"], "name": g["name"], "owner": g.get("owner", False), "permissions": g.get("permissions")} for g in data]
    if as_json:
        _out({"guilds": guilds, "count": len(guilds)}, True)
    else:
        click.echo(f"{'ID':<22} {'NAME':<35} OWNER")
        click.echo("─" * 65)
        for g in guilds:
            click.echo(f"{g['id']:<22} {g['name']:<35} {g['owner']}")


@guild.command(name="info")
@click.argument("guild_id")
@click.pass_context
def guild_info(ctx, guild_id):
    """获取服务器详情。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/guilds/{guild_id}?with_counts=true", t)
    result = {"id": data["id"], "name": data["name"], "description": data.get("description"), "member_count": data.get("approximate_member_count"), "online_count": data.get("approximate_presence_count"), "owner_id": data.get("owner_id")}
    _out(result, as_json) if as_json else click.echo("\n".join(f"  {k:<20} {v}" for k, v in result.items() if v is not None))


@guild.command(name="channels")
@click.argument("guild_id")
@click.pass_context
def guild_channels(ctx, guild_id):
    """列出服务器所有频道。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/guilds/{guild_id}/channels", t)
    TYPES = {0: "text", 2: "voice", 4: "category", 5: "announcement", 13: "stage", 15: "forum"}
    channels = [{"id": c["id"], "name": c["name"], "type": TYPES.get(c["type"], str(c["type"])), "position": c.get("position", 0)} for c in sorted(data, key=lambda x: x.get("position", 0))]
    if as_json:
        _out({"channels": channels, "count": len(channels)}, True)
    else:
        click.echo(f"{'ID':<22} {'TYPE':<14} NAME")
        click.echo("─" * 60)
        for c in channels:
            click.echo(f"{c['id']:<22} {c['type']:<14} {c['name']}")


@guild.command(name="members")
@click.argument("guild_id")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def guild_members(ctx, guild_id, limit):
    """列出服务器成员。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/guilds/{guild_id}/members?limit={min(limit, 1000)}", t)
    members = [{"id": m["user"]["id"], "username": m["user"]["username"], "nick": m.get("nick"), "roles": m.get("roles", [])} for m in data]
    if as_json:
        _out({"members": members, "count": len(members)}, True)
    else:
        click.echo(f"{'ID':<22} {'USERNAME':<25} NICK")
        click.echo("─" * 60)
        for m in members:
            click.echo(f"{m['id']:<22} {m['username']:<25} {m['nick'] or ''}")


@guild.command(name="roles")
@click.argument("guild_id")
@click.pass_context
def guild_roles(ctx, guild_id):
    """列出服务器角色。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/guilds/{guild_id}/roles", t)
    roles = [{"id": r["id"], "name": r["name"], "color": hex(r.get("color", 0)), "managed": r.get("managed", False), "position": r.get("position", 0)} for r in sorted(data, key=lambda x: x.get("position", 0), reverse=True)]
    if as_json:
        _out({"roles": roles, "count": len(roles)}, True)
    else:
        click.echo(f"{'ID':<22} {'COLOR':<10} NAME")
        click.echo("─" * 50)
        for r in roles:
            click.echo(f"{r['id']:<22} {r['color']:<10} {r['name']}")


# ── MESSAGES ─────────────────────────────────────────────────────────────────

@cli.group()
def message():
    """消息管理（send / delete / history / react / pin）。"""


@message.command(name="send")
@click.argument("channel_id")
@click.argument("content")
@click.option("--tts", is_flag=True, help="Text-to-speech")
@click.option("--reply-to", default=None, help="回复的消息 ID")
@click.pass_context
def message_send(ctx, channel_id, content, tts, reply_to):
    """发送消息到频道。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {"content": content, "tts": tts}
    if reply_to:
        body["message_reference"] = {"message_id": reply_to}
    data = _post(f"/channels/{channel_id}/messages", t, body)
    result = {"id": data["id"], "channel_id": channel_id, "content": content[:50]}
    _out(result, as_json) if as_json else click.echo(f"✅ Sent  id={data['id']}")


@message.command(name="delete")
@click.argument("channel_id")
@click.argument("message_id")
@click.pass_context
def message_delete(ctx, channel_id, message_id):
    """删除消息。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    _delete(f"/channels/{channel_id}/messages/{message_id}", t)
    result = {"channel_id": channel_id, "message_id": message_id, "status": "deleted"}
    _out(result, as_json) if as_json else click.echo(f"🗑  Deleted message {message_id}")


@message.command(name="history")
@click.argument("channel_id")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def message_history(ctx, channel_id, limit):
    """获取频道消息历史。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/channels/{channel_id}/messages?limit={min(limit, 100)}", t)
    msgs = [{"id": m["id"], "author": m["author"]["username"], "content": m.get("content", "")[:100], "timestamp": m.get("timestamp", "")[:19]} for m in data]
    if as_json:
        _out({"messages": msgs, "count": len(msgs)}, True)
    else:
        for m in msgs:
            click.echo(f"[{m['timestamp']}] @{m['author']}: {m['content'][:70]}")


@message.command(name="react")
@click.argument("channel_id")
@click.argument("message_id")
@click.argument("emoji")
@click.pass_context
def message_react(ctx, channel_id, message_id, emoji):
    """为消息添加表情反应。emoji 可以是 Unicode 或 name:id 格式。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    from urllib.parse import quote
    encoded = quote(emoji)
    _request("PUT", f"/channels/{channel_id}/messages/{message_id}/reactions/{encoded}/@me", t)
    result = {"channel_id": channel_id, "message_id": message_id, "emoji": emoji}
    _out(result, as_json) if as_json else click.echo(f"✅ Reacted {emoji} to {message_id}")


# ── WEBHOOKS ─────────────────────────────────────────────────────────────────

@cli.group()
def webhook():
    """Webhook 管理（list / create / send / delete）。"""


@webhook.command(name="send")
@click.argument("webhook_url")
@click.argument("content")
@click.option("--username", default=None)
@click.option("--avatar-url", default=None)
@click.pass_context
def webhook_send(ctx, webhook_url, content, username, avatar_url):
    """通过 Webhook URL 发送消息（不需要 Bot Token）。"""
    as_json = ctx.obj["json"]
    body: dict = {"content": content}
    if username:
        body["username"] = username
    if avatar_url:
        body["avatar_url"] = avatar_url
    data = json.dumps(body).encode()
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = {"status": "sent", "webhook": webhook_url[:40] + "..."}
            _out(result, as_json) if as_json else click.echo("✅ Webhook message sent")
    except urllib.error.HTTPError as e:
        raise click.ClickException(f"Webhook 失败 {e.code}: {e.read().decode()[:100]}")


@webhook.command(name="list")
@click.argument("channel_id")
@click.pass_context
def webhook_list(ctx, channel_id):
    """列出频道的 Webhooks。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _get(f"/channels/{channel_id}/webhooks", t)
    hooks = [{"id": w["id"], "name": w["name"], "url": f"https://discord.com/api/webhooks/{w['id']}/{w.get('token','')}"} for w in data]
    if as_json:
        _out({"webhooks": hooks, "count": len(hooks)}, True)
    else:
        for h in hooks:
            click.echo(f"{h['id']}  {h['name']}")


@webhook.command(name="create")
@click.argument("channel_id")
@click.argument("name")
@click.pass_context
def webhook_create(ctx, channel_id, name):
    """创建 Webhook。"""
    t = _token(ctx)
    as_json = ctx.obj["json"]
    data = _post(f"/channels/{channel_id}/webhooks", t, {"name": name})
    result = {"id": data["id"], "name": data["name"], "token": data.get("token", "")}
    _out(result, as_json) if as_json else click.echo(f"✅ Webhook created: {data['name']} ({data['id']})")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 Token）。"""
    info = {
        "name": "cli-anything-discord",
        "version": "1.0.0",
        "description": "Discord Bot API CLI - manage guilds, channels, members, webhooks, messages",
        "requires_token": True,
        "token_env": "DISCORD_BOT_TOKEN",
        "token_hint": "Bot token from https://discord.com/developers/applications",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Check Discord Bot token validity"},
            {"cmd": "version", "args": [], "desc": "Show Bot info"},
            {"cmd": "guild list", "args": [], "desc": "List all guilds (servers) the Bot joined"},
            {"cmd": "guild info", "args": [{"name": "GUILD_ID", "type": "str"}], "desc": "Get guild details"},
            {"cmd": "guild channels", "args": [{"name": "GUILD_ID", "type": "str"}], "desc": "List guild channels"},
            {"cmd": "guild members", "args": [{"name": "GUILD_ID", "type": "str"}, {"name": "--limit", "type": "int", "default": 20}], "desc": "List guild members"},
            {"cmd": "guild roles", "args": [{"name": "GUILD_ID", "type": "str"}], "desc": "List guild roles"},
            {"cmd": "message send", "args": [{"name": "CHANNEL_ID", "type": "str"}, {"name": "CONTENT", "type": "str"}, {"name": "--reply-to", "type": "str"}], "desc": "Send message to channel"},
            {"cmd": "message delete", "args": [{"name": "CHANNEL_ID", "type": "str"}, {"name": "MESSAGE_ID", "type": "str"}], "desc": "Delete a message"},
            {"cmd": "message history", "args": [{"name": "CHANNEL_ID", "type": "str"}, {"name": "--limit", "type": "int", "default": 20}], "desc": "Get channel message history"},
            {"cmd": "message react", "args": [{"name": "CHANNEL_ID", "type": "str"}, {"name": "MESSAGE_ID", "type": "str"}, {"name": "EMOJI", "type": "str"}], "desc": "Add reaction to message"},
            {"cmd": "webhook send", "args": [{"name": "WEBHOOK_URL", "type": "str"}, {"name": "CONTENT", "type": "str"}, {"name": "--username", "type": "str"}], "desc": "Send message via webhook (no Bot token needed)"},
            {"cmd": "webhook list", "args": [{"name": "CHANNEL_ID", "type": "str"}], "desc": "List channel webhooks"},
            {"cmd": "webhook create", "args": [{"name": "CHANNEL_ID", "type": "str"}, {"name": "NAME", "type": "str"}], "desc": "Create a webhook"},
        ],
        "json_flag": "--json",
        "example": "discord-cli --json message send 123456789 'Hello from Agent'",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
