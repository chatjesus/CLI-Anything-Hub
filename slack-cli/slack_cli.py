"""
cli-anything-slack — Slack Web API CLI
Wraps Slack Web API via slack-sdk for AI Agent use.
"""
import json
import sys
import os
from typing import Optional

import click

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False


def _client(token: str):
    if not _SDK_AVAILABLE:
        raise click.ClickException("slack-sdk 未安装，请运行: pip install slack-sdk")
    return WebClient(token=token)


def _token(ctx) -> str:
    t = ctx.obj.get("token") or os.environ.get("SLACK_BOT_TOKEN") or os.environ.get("SLACK_TOKEN")
    if not t:
        raise click.ClickException(
            "未提供 Slack token。\n"
            "方式1: --token xoxb-xxx\n"
            "方式2: export SLACK_BOT_TOKEN=xoxb-xxx\n"
            "获取: https://api.slack.com/apps → OAuth & Permissions"
        )
    return t


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        click.echo(str(data) if not isinstance(data, str) else data)


def _api(ctx, method, **kwargs):
    try:
        c = _client(_token(ctx))
        return getattr(c, method)(**kwargs)
    except SlackApiError as e:
        raise click.ClickException(f"Slack API 错误: {e.response['error']}")


@click.group()
@click.option("--token", envvar="SLACK_BOT_TOKEN", default=None, help="Slack Bot Token (xoxb-...)")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出")
@click.pass_context
def cli(ctx, token, as_json):
    """cli-anything-slack — Slack Web API CLI\n
    发消息、管理频道、上传文件、查询用户等。需要 Slack Bot Token。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
def detect(ctx):
    """检测 Slack API 连通性并验证 token。"""
    as_json = ctx.obj["json"]
    if not _SDK_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install slack-sdk"}
        _out(result, as_json) if as_json else click.echo("❌ slack-sdk 未安装")
        sys.exit(1)
    try:
        resp = _api(ctx, "auth_test")
        result = {
            "status": "ok",
            "team": resp["team"],
            "user": resp["user"],
            "bot_id": resp.get("bot_id"),
            "url": resp.get("url"),
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Slack OK  team={result['team']}  user={result['user']}")
    except click.ClickException as e:
        result = {"status": "error", "error": e.format_message()}
        _out(result, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """显示 Slack API 版本及 Bot 信息。"""
    resp = _api(ctx, "auth_test")
    as_json = ctx.obj["json"]
    result = {"team": resp["team"], "team_id": resp["team_id"], "user": resp["user"], "bot_id": resp.get("bot_id")}
    _out(result, as_json) if as_json else click.echo(f"Slack API  team={result['team']}  user={result['user']}")


# ── CHANNELS ────────────────────────────────────────────────────────────────

@cli.group()
def channel():
    """频道管理（list / info / join / leave / create / archive）。"""


@channel.command(name="list")
@click.option("--limit", default=50, show_default=True, type=int)
@click.option("--types", default="public_channel,private_channel", help="频道类型")
@click.pass_context
def channel_list(ctx, limit, types):
    """列出所有频道。"""
    as_json = ctx.obj["json"]
    resp = _api(ctx, "conversations_list", limit=limit, types=types)
    channels = resp["channels"]
    data = [{"id": c["id"], "name": c["name"], "members": c.get("num_members", 0), "topic": c.get("topic", {}).get("value", "")[:60]} for c in channels]
    if as_json:
        _out({"channels": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':<14} {'NAME':<32} {'MEMBERS':>8}  TOPIC")
        click.echo("─" * 80)
        for d in data:
            click.echo(f"{d['id']:<14} {d['name']:<32} {d['members']:>8}  {d['topic'][:30]}")


@channel.command(name="info")
@click.argument("channel_id")
@click.pass_context
def channel_info(ctx, channel_id):
    """获取频道详情。"""
    as_json = ctx.obj["json"]
    resp = _api(ctx, "conversations_info", channel=channel_id)
    c = resp["channel"]
    result = {"id": c["id"], "name": c["name"], "topic": c.get("topic", {}).get("value"), "purpose": c.get("purpose", {}).get("value"), "members": c.get("num_members")}
    _out(result, as_json) if as_json else click.echo("\n".join(f"  {k:<12} {v}" for k, v in result.items() if v))


@channel.command(name="create")
@click.argument("name")
@click.option("--private", is_flag=True)
@click.pass_context
def channel_create(ctx, name, private):
    """创建频道。"""
    as_json = ctx.obj["json"]
    resp = _api(ctx, "conversations_create", name=name, is_private=private)
    c = resp["channel"]
    result = {"id": c["id"], "name": c["name"]}
    _out(result, as_json) if as_json else click.echo(f"✅ Created: #{c['name']} ({c['id']})")


@channel.command(name="archive")
@click.argument("channel_id")
@click.pass_context
def channel_archive(ctx, channel_id):
    """归档频道。"""
    as_json = ctx.obj["json"]
    _api(ctx, "conversations_archive", channel=channel_id)
    result = {"channel": channel_id, "status": "archived"}
    _out(result, as_json) if as_json else click.echo(f"✅ Archived: {channel_id}")


# ── MESSAGES ─────────────────────────────────────────────────────────────────

@cli.group()
def message():
    """消息管理（send / reply / delete / history / search / react）。"""


@message.command(name="send")
@click.argument("channel")
@click.argument("text")
@click.option("--thread-ts", default=None, help="回复到指定 thread")
@click.option("--username", default=None, help="覆盖 Bot 显示名")
@click.option("--emoji-icon", default=None, help="覆盖 Bot 图标 emoji（如 :robot_face:）")
@click.pass_context
def message_send(ctx, channel, text, thread_ts, username, emoji_icon):
    """发送消息到频道或 DM。\n
    CHANNEL 可以是 #channel-name 或 用户ID（U123456）
    """
    as_json = ctx.obj["json"]
    kwargs = {"channel": channel, "text": text}
    if thread_ts:
        kwargs["thread_ts"] = thread_ts
    if username:
        kwargs["username"] = username
    if emoji_icon:
        kwargs["icon_emoji"] = emoji_icon
    resp = _api(ctx, "chat_postMessage", **kwargs)
    result = {"ts": resp["ts"], "channel": resp["channel"]}
    _out(result, as_json) if as_json else click.echo(f"✅ Sent  ts={resp['ts']}")


@message.command(name="delete")
@click.argument("channel")
@click.argument("ts")
@click.pass_context
def message_delete(ctx, channel, ts):
    """删除消息（需要 chat:write 权限）。"""
    as_json = ctx.obj["json"]
    _api(ctx, "chat_delete", channel=channel, ts=ts)
    result = {"channel": channel, "ts": ts, "status": "deleted"}
    _out(result, as_json) if as_json else click.echo(f"🗑  Deleted ts={ts}")


@message.command(name="history")
@click.argument("channel")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def message_history(ctx, channel, limit):
    """获取频道消息历史。"""
    as_json = ctx.obj["json"]
    resp = _api(ctx, "conversations_history", channel=channel, limit=limit)
    messages = resp["messages"]
    data = [{"ts": m["ts"], "user": m.get("user", "bot"), "text": m.get("text", "")[:100], "type": m.get("subtype", "message")} for m in messages]
    if as_json:
        _out({"messages": data, "count": len(data)}, True)
    else:
        for d in data:
            click.echo(f"[{d['ts']}] {d['user']}: {d['text'][:80]}")


@message.command(name="react")
@click.argument("channel")
@click.argument("ts")
@click.argument("emoji")
@click.pass_context
def message_react(ctx, channel, ts, emoji):
    """为消息添加 emoji 反应。"""
    as_json = ctx.obj["json"]
    name = emoji.strip(":")
    _api(ctx, "reactions_add", channel=channel, timestamp=ts, name=name)
    result = {"channel": channel, "ts": ts, "emoji": name}
    _out(result, as_json) if as_json else click.echo(f"✅ Reacted :{name}: to {ts}")


@message.command(name="search")
@click.argument("query")
@click.option("--count", default=10, show_default=True, type=int)
@click.pass_context
def message_search(ctx, query, count):
    """全局搜索消息（需要 search:read 权限）。"""
    as_json = ctx.obj["json"]
    resp = _api(ctx, "search_messages", query=query, count=count)
    matches = resp.get("messages", {}).get("matches", [])
    data = [{"channel": m.get("channel", {}).get("name", "?"), "user": m.get("username", "?"), "text": m.get("text", "")[:100], "ts": m.get("ts")} for m in matches]
    if as_json:
        _out({"results": data, "count": len(data)}, True)
    else:
        for d in data:
            click.echo(f"#{d['channel']} @{d['user']}: {d['text'][:70]}")


# ── FILES ─────────────────────────────────────────────────────────────────────

@cli.group()
def file():
    """文件管理（upload / list / delete）。"""


@file.command(name="upload")
@click.argument("filepath")
@click.option("--channel", "-c", default=None, help="发送到的频道")
@click.option("--title", default=None, help="文件标题")
@click.option("--message", "-m", default=None, help="附带消息")
@click.pass_context
def file_upload(ctx, filepath, channel, title, message):
    """上传文件。"""
    as_json = ctx.obj["json"]
    kwargs = {"file": filepath}
    if channel:
        kwargs["channels"] = channel
    if title:
        kwargs["title"] = title
    if message:
        kwargs["initial_comment"] = message
    resp = _api(ctx, "files_upload", **kwargs)
    f = resp["file"]
    result = {"id": f["id"], "name": f["name"], "url": f.get("permalink")}
    _out(result, as_json) if as_json else click.echo(f"✅ Uploaded: {f['name']} ({f['id']})")


@file.command(name="list")
@click.option("--channel", default=None, help="按频道筛选")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def file_list(ctx, channel, limit):
    """列出文件。"""
    as_json = ctx.obj["json"]
    kwargs = {"count": limit}
    if channel:
        kwargs["channel"] = channel
    resp = _api(ctx, "files_list", **kwargs)
    files = resp.get("files", [])
    data = [{"id": f["id"], "name": f["name"], "size": f.get("size", 0), "created": f.get("created")} for f in files]
    if as_json:
        _out({"files": data, "count": len(data)}, True)
    else:
        for d in data:
            click.echo(f"{d['id']}  {d['name']}  {d['size']} bytes")


# ── USERS ─────────────────────────────────────────────────────────────────────

@cli.group()
def user():
    """用户管理（list / info / lookup）。"""


@user.command(name="list")
@click.option("--limit", default=50, show_default=True, type=int)
@click.pass_context
def user_list(ctx, limit):
    """列出工作空间成员。"""
    as_json = ctx.obj["json"]
    resp = _api(ctx, "users_list", limit=limit)
    members = [m for m in resp["members"] if not m.get("deleted") and not m.get("is_bot")]
    data = [{"id": m["id"], "name": m["name"], "real_name": m.get("real_name", ""), "email": m.get("profile", {}).get("email", "")} for m in members]
    if as_json:
        _out({"users": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':<14} {'NAME':<22} REAL NAME")
        click.echo("─" * 60)
        for d in data:
            click.echo(f"{d['id']:<14} {d['name']:<22} {d['real_name']}")


@user.command(name="lookup")
@click.argument("email")
@click.pass_context
def user_lookup(ctx, email):
    """通过 email 查找用户 ID。"""
    as_json = ctx.obj["json"]
    resp = _api(ctx, "users_lookupByEmail", email=email)
    u = resp["user"]
    result = {"id": u["id"], "name": u["name"], "real_name": u.get("real_name")}
    _out(result, as_json) if as_json else click.echo(f"{u['id']}  {u['name']}  {u.get('real_name', '')}")


@cli.command()
@click.pass_context
def schema(ctx):
    """输出所有可用命令的 JSON Schema（Agent 发现能力用，无需 Token）。"""
    info = {
        "name": "cli-anything-slack",
        "version": "1.0.0",
        "description": "Slack Web API CLI - send messages, manage channels, upload files, search",
        "requires_token": True,
        "token_env": "SLACK_BOT_TOKEN",
        "token_hint": "xoxb-... from https://api.slack.com/apps",
        "commands": [
            {"cmd": "detect", "args": [], "desc": "Check Slack API connectivity and verify token"},
            {"cmd": "version", "args": [], "desc": "Show Bot info"},
            {"cmd": "channel list", "args": [{"name": "--limit", "type": "int", "default": 50}], "desc": "List all channels"},
            {"cmd": "channel info", "args": [{"name": "CHANNEL_ID", "type": "str"}], "desc": "Get channel details"},
            {"cmd": "channel create", "args": [{"name": "NAME", "type": "str"}, {"name": "--private", "type": "flag"}], "desc": "Create a channel"},
            {"cmd": "channel archive", "args": [{"name": "CHANNEL_ID", "type": "str"}], "desc": "Archive a channel"},
            {"cmd": "message send", "args": [{"name": "CHANNEL", "type": "str"}, {"name": "TEXT", "type": "str"}, {"name": "--thread-ts", "type": "str"}, {"name": "--silent", "type": "flag"}], "desc": "Send message to channel or DM"},
            {"cmd": "message delete", "args": [{"name": "CHANNEL", "type": "str"}, {"name": "TS", "type": "str"}], "desc": "Delete a message"},
            {"cmd": "message history", "args": [{"name": "CHANNEL", "type": "str"}, {"name": "--limit", "type": "int", "default": 20}], "desc": "Get message history"},
            {"cmd": "message react", "args": [{"name": "CHANNEL", "type": "str"}, {"name": "TS", "type": "str"}, {"name": "EMOJI", "type": "str"}], "desc": "React to a message with emoji"},
            {"cmd": "message search", "args": [{"name": "QUERY", "type": "str"}, {"name": "--count", "type": "int", "default": 10}], "desc": "Search messages globally"},
            {"cmd": "file upload", "args": [{"name": "FILEPATH", "type": "str"}, {"name": "--channel", "type": "str"}, {"name": "--title", "type": "str"}], "desc": "Upload file"},
            {"cmd": "file list", "args": [{"name": "--channel", "type": "str"}, {"name": "--limit", "type": "int", "default": 20}], "desc": "List files"},
            {"cmd": "user list", "args": [{"name": "--limit", "type": "int", "default": 50}], "desc": "List workspace members"},
            {"cmd": "user lookup", "args": [{"name": "EMAIL", "type": "str"}], "desc": "Look up user by email"},
        ],
        "json_flag": "--json",
        "example": "slack-cli --json message send #general 'Hello from Agent'",
    }
    click.echo(_json_str(info))


def _json_str(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    cli()
