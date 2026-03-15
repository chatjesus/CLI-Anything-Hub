"""
cli-anything-gworkspace -- Google Workspace CLI
Drive / Gmail / Calendar / Sheets / Docs / Chat
Inspired by https://github.com/googleworkspace/cli (20.5k stars)

Auth priority:
  1. --token  /  GOOGLE_WORKSPACE_TOKEN   (pre-obtained access token)
  2. --creds  /  GOOGLE_APPLICATION_CREDENTIALS  (service account JSON)
  3. GWS_OAUTH_FILE  (OAuth2 user credentials JSON)
"""
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
import base64
import email as email_lib
from typing import Optional

import click

SCOPES = {
    "drive":    "https://www.googleapis.com/auth/drive",
    "gmail":    "https://mail.google.com/",
    "calendar": "https://www.googleapis.com/auth/calendar",
    "sheets":   "https://www.googleapis.com/auth/spreadsheets",
    "docs":     "https://www.googleapis.com/auth/documents",
    "chat":     "https://www.googleapis.com/auth/chat.messages",
}

# ─────────────────────────────────────────────────────────────────────────────
# Auth helpers
# ─────────────────────────────────────────────────────────────────────────────

def _get_token(ctx) -> str:
    """Return a valid OAuth2 / service-account access token."""
    # 1. Pre-obtained access token
    token = ctx.obj.get("token") or os.environ.get("GOOGLE_WORKSPACE_TOKEN")
    if token:
        return token

    # 2. Service account via google-auth
    creds_file = ctx.obj.get("creds") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_file and os.path.isfile(creds_file):
        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests
            sa = service_account.Credentials.from_service_account_file(
                creds_file,
                scopes=list(SCOPES.values()),
            )
            req = google.auth.transport.requests.Request()
            sa.refresh(req)
            return sa.token
        except ImportError:
            raise click.ClickException("google-auth 未安装: pip install google-auth google-auth-oauthlib")

    # 3. OAuth2 user flow
    oauth_file = os.environ.get("GWS_OAUTH_FILE")
    if oauth_file and os.path.isfile(oauth_file):
        try:
            from google.oauth2.credentials import Credentials
            import google.auth.transport.requests
            creds = Credentials.from_authorized_user_file(oauth_file, scopes=list(SCOPES.values()))
            if creds.expired and creds.refresh_token:
                creds.refresh(google.auth.transport.requests.Request())
            return creds.token
        except ImportError:
            raise click.ClickException("google-auth-oauthlib 未安装: pip install google-auth-oauthlib")

    raise click.ClickException(
        "未找到 Google 凭证。请设置以下之一:\n"
        "  1. export GOOGLE_WORKSPACE_TOKEN=<access_token>  (最简单)\n"
        "  2. export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json\n"
        "  3. export GWS_OAUTH_FILE=/path/to/oauth-credentials.json\n"
        "获取方式: https://console.cloud.google.com/apis/credentials\n"
        "参考: https://github.com/googleworkspace/cli"
    )


def _api(token: str, method: str, url: str, body: Optional[dict] = None,
         params: Optional[dict] = None, timeout: int = 30) -> dict:
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            msg = err.get("error", {})
            raise click.ClickException(
                f"Google API {e.code}: {msg.get('message', body_text[:300])}"
            )
        except (json.JSONDecodeError, AttributeError):
            raise click.ClickException(f"Google API {e.code}: {body_text[:300]}")
    except urllib.error.URLError as e:
        raise click.ClickException(f"网络错误: {e.reason}")


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if isinstance(data, (dict, list)):
            click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        else:
            click.echo(str(data))


# ─────────────────────────────────────────────────────────────────────────────
# Root group
# ─────────────────────────────────────────────────────────────────────────────

@click.group()
@click.option("--token", envvar="GOOGLE_WORKSPACE_TOKEN", default=None,
              help="Google OAuth2 access token (highest priority)")
@click.option("--creds", envvar="GOOGLE_APPLICATION_CREDENTIALS", default=None,
              help="Path to service account JSON file")
@click.option("--json", "as_json", is_flag=True, help="JSON output (Agent-friendly)")
@click.pass_context
def cli(ctx, token, creds, as_json):
    """cli-anything-gworkspace -- Google Workspace CLI\n
    Drive / Gmail / Calendar / Sheets / Docs / Chat\n
    Inspired by https://github.com/googleworkspace/cli (20.5k stars, Apache-2.0)
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["creds"] = creds
    ctx.obj["json"] = as_json


@cli.command()
@click.pass_context
def detect(ctx):
    """Verify Google credentials and list accessible services."""
    as_json = ctx.obj["json"]
    try:
        token = _get_token(ctx)
        data = _api(token, "GET", "https://www.googleapis.com/oauth2/v3/userinfo")
        result = {
            "status": "ok",
            "email": data.get("email"),
            "name": data.get("name"),
            "services": ["drive", "gmail", "calendar", "sheets", "docs", "chat"],
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"OK  {result['email']}  ({result['name']})")
    except click.ClickException as e:
        _out({"status": "error", "error": e.format_message()}, as_json) if as_json else click.echo(f"ERR {e.format_message()}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """Show CLI version and auth method."""
    as_json = ctx.obj["json"]
    info = {"version": "1.0.0", "name": "cli-anything-gworkspace", "services": 6}
    _out(info, as_json) if as_json else click.echo(f"cli-anything-gworkspace v1.0.0 -- 6 services")


@cli.command()
@click.pass_context
def schema(ctx):
    """Output full capability schema (no credentials needed, Agent-discovery)."""
    info = {
        "name": "cli-anything-gworkspace",
        "version": "1.0.0",
        "description": "Google Workspace CLI: Drive, Gmail, Calendar, Sheets, Docs, Chat",
        "reference": "https://github.com/googleworkspace/cli",
        "auth": {
            "methods": ["access_token", "service_account", "oauth2_user"],
            "env_vars": ["GOOGLE_WORKSPACE_TOKEN", "GOOGLE_APPLICATION_CREDENTIALS", "GWS_OAUTH_FILE"],
        },
        "services": {
            "drive": ["list", "upload", "download", "share", "delete", "mkdir", "info"],
            "gmail": ["send", "list", "get", "search", "trash", "reply", "labels"],
            "calendar": ["events", "create", "get", "delete", "calendars"],
            "sheets": ["read", "write", "append", "create", "info"],
            "docs": ["create", "get", "append", "info"],
            "chat": ["spaces", "messages", "send"],
        },
        "json_flag": "--json",
        "example": "gworkspace-cli --json drive list --limit 10",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


# ─────────────────────────────────────────────────────────────────────────────
# DRIVE
# ─────────────────────────────────────────────────────────────────────────────

DRIVE_API = "https://www.googleapis.com/drive/v3"
DRIVE_UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"


@cli.group()
def drive():
    """Google Drive: list / upload / download / share / delete / mkdir."""


@drive.command(name="list")
@click.option("--limit", default=20, show_default=True, type=int)
@click.option("--query", "-q", default=None, help="Drive search query (e.g. \"name contains 'report'\")")
@click.option("--folder", default=None, help="Parent folder ID to list")
@click.option("--trashed/--no-trashed", default=False)
@click.pass_context
def drive_list(ctx, limit, query, folder, trashed):
    """List files in Google Drive."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    q_parts = [] if trashed else ["trashed=false"]
    if query:
        q_parts.append(query)
    if folder:
        q_parts.append(f"'{folder}' in parents")
    params = {
        "pageSize": min(limit, 1000),
        "fields": "files(id,name,mimeType,size,modifiedTime,parents)",
        "orderBy": "modifiedTime desc",
    }
    if q_parts:
        params["q"] = " and ".join(q_parts)
    data = _api(token, "GET", f"{DRIVE_API}/files", params=params)
    files = data.get("files", [])
    if as_json:
        _out({"files": files, "count": len(files)}, True)
    else:
        click.echo(f"{'ID':<36} {'SIZE':>10}  {'MODIFIED':<22} NAME")
        click.echo("-" * 100)
        for f in files:
            size = f.get("size", "folder")
            if isinstance(size, str) and size.isdigit():
                size_str = f"{int(size)//1024}K"
            else:
                size_str = str(size)
            click.echo(f"{f['id']:<36} {size_str:>10}  {f.get('modifiedTime','')[:19]:<22} {f['name']}")


@drive.command(name="info")
@click.argument("file_id")
@click.pass_context
def drive_info(ctx, file_id):
    """Get file metadata."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{DRIVE_API}/files/{file_id}",
                params={"fields": "id,name,mimeType,size,modifiedTime,webViewLink,parents,owners"})
    _out(data, as_json) if as_json else click.echo("\n".join(f"  {k:<20} {v}" for k, v in data.items()))


@drive.command(name="upload")
@click.argument("filepath")
@click.option("--name", default=None, help="Override filename in Drive")
@click.option("--folder", default=None, help="Parent folder ID")
@click.option("--mime", default=None, help="Override MIME type")
@click.pass_context
def drive_upload(ctx, filepath, name, folder, mime):
    """Upload a file to Google Drive (multipart upload)."""
    import mimetypes
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    if not os.path.isfile(filepath):
        raise click.ClickException(f"文件不存在: {filepath}")
    file_name = name or os.path.basename(filepath)
    content_type = mime or mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    metadata: dict = {"name": file_name}
    if folder:
        metadata["parents"] = [folder]
    # Simple multipart upload
    boundary = "gws_boundary_cli_anything"
    meta_bytes = json.dumps(metadata).encode()
    with open(filepath, "rb") as f:
        file_bytes = f.read()
    body = (
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode()
        + meta_bytes + f"\r\n--{boundary}\r\nContent-Type: {content_type}\r\n\r\n".encode()
        + file_bytes + f"\r\n--{boundary}--".encode()
    )
    url = f"{DRIVE_UPLOAD}?uploadType=multipart"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/related; boundary={boundary}",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise click.ClickException(f"Upload error {e.code}: {e.read().decode()[:200]}")
    _out(result, as_json) if as_json else click.echo(f"Uploaded: {result.get('name')}  id={result.get('id')}")


@drive.command(name="download")
@click.argument("file_id")
@click.option("--output", "-o", default=None, help="Output path (default: file name from Drive)")
@click.pass_context
def drive_download(ctx, file_id, output):
    """Download a file from Google Drive."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    meta = _api(token, "GET", f"{DRIVE_API}/files/{file_id}",
                params={"fields": "id,name,mimeType"})
    file_name = output or meta.get("name", file_id)
    url = f"{DRIVE_API}/files/{file_id}?alt=media"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(file_name, "wb") as f:
                f.write(resp.read())
    except urllib.error.HTTPError as e:
        raise click.ClickException(f"Download error {e.code}: {e.read().decode()[:200]}")
    result = {"id": file_id, "saved_as": file_name, "status": "ok"}
    _out(result, as_json) if as_json else click.echo(f"Downloaded: {file_name}")


@drive.command(name="share")
@click.argument("file_id")
@click.option("--email", "-e", default=None, help="Share with email (omit for public link)")
@click.option("--role", default="reader", type=click.Choice(["reader", "commenter", "writer", "owner"]))
@click.pass_context
def drive_share(ctx, file_id, email, role):
    """Share a file or make it public."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    if email:
        body = {"type": "user", "role": role, "emailAddress": email}
    else:
        body = {"type": "anyone", "role": "reader"}
    data = _api(token, "POST", f"{DRIVE_API}/files/{file_id}/permissions", body=body)
    _out(data, as_json) if as_json else click.echo(f"Shared: {file_id}  role={role}  to={email or 'anyone'}")


@drive.command(name="delete")
@click.argument("file_id")
@click.option("--yes", is_flag=True)
@click.pass_context
def drive_delete(ctx, file_id, yes):
    """Delete (trash) a file."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    if not yes:
        click.confirm(f"Move {file_id} to trash?", abort=True)
    _api(token, "DELETE", f"{DRIVE_API}/files/{file_id}")
    result = {"id": file_id, "status": "deleted"}
    _out(result, as_json) if as_json else click.echo(f"Deleted: {file_id}")


@drive.command(name="mkdir")
@click.argument("name")
@click.option("--parent", default=None, help="Parent folder ID")
@click.pass_context
def drive_mkdir(ctx, name, parent):
    """Create a folder in Google Drive."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent:
        body["parents"] = [parent]
    data = _api(token, "POST", f"{DRIVE_API}/files", body=body)
    _out(data, as_json) if as_json else click.echo(f"Created folder: {name}  id={data.get('id')}")


# ─────────────────────────────────────────────────────────────────────────────
# GMAIL
# ─────────────────────────────────────────────────────────────────────────────

GMAIL_API = "https://gmail.googleapis.com/gmail/v1/users/me"


def _encode_email(to: str, subject: str, body: str, from_addr: str = "",
                  reply_to_id: str = "") -> str:
    from email.mime.text import MIMEText
    msg = MIMEText(body, "html" if body.strip().startswith("<") else "plain")
    msg["to"] = to
    msg["subject"] = subject
    if from_addr:
        msg["from"] = from_addr
    if reply_to_id:
        msg["In-Reply-To"] = reply_to_id
        msg["References"] = reply_to_id
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()


@cli.group()
def gmail():
    """Gmail: send / list / get / search / reply / trash / labels."""


@gmail.command(name="send")
@click.option("--to", required=True)
@click.option("--subject", "-s", required=True)
@click.option("--body", "-b", required=True)
@click.option("--thread-id", default=None, help="Reply to thread")
@click.pass_context
def gmail_send(ctx, to, subject, body, thread_id):
    """Send an email via Gmail."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    raw = _encode_email(to, subject, body)
    payload: dict = {"raw": raw}
    if thread_id:
        payload["threadId"] = thread_id
    data = _api(token, "POST", f"{GMAIL_API}/messages/send", body=payload)
    result = {"id": data.get("id"), "threadId": data.get("threadId"), "to": to, "subject": subject}
    _out(result, as_json) if as_json else click.echo(f"Sent: id={data.get('id')}  to={to}")


@gmail.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.option("--label", default="INBOX", help="Label to filter")
@click.option("--query", "-q", default=None, help="Gmail search query")
@click.pass_context
def gmail_list(ctx, limit, label, query):
    """List emails."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    params: dict = {"maxResults": min(limit, 500), "labelIds": label}
    if query:
        params["q"] = query
    data = _api(token, "GET", f"{GMAIL_API}/messages", params=params)
    messages = data.get("messages", [])
    results = []
    for m in messages[:min(limit, 20)]:
        msg = _api(token, "GET", f"{GMAIL_API}/messages/{m['id']}",
                   params={"format": "metadata", "metadataHeaders": "From,Subject,Date"})
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        results.append({
            "id": m["id"], "threadId": m.get("threadId"),
            "from": headers.get("From", ""), "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
        })
    if as_json:
        _out({"messages": results, "count": len(results)}, True)
    else:
        click.echo(f"{'ID':<18} {'FROM':<35} SUBJECT")
        click.echo("-" * 90)
        for r in results:
            click.echo(f"{r['id']:<18} {r['from'][:33]:<35} {r['subject'][:40]}")


@gmail.command(name="get")
@click.argument("message_id")
@click.option("--format", "fmt", default="full", type=click.Choice(["full", "metadata", "minimal"]))
@click.pass_context
def gmail_get(ctx, message_id, fmt):
    """Get email by ID."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{GMAIL_API}/messages/{message_id}", params={"format": fmt})
    if as_json:
        _out(data, True)
    else:
        headers = {h["name"]: h["value"] for h in data.get("payload", {}).get("headers", [])}
        for k in ["From", "To", "Subject", "Date"]:
            if k in headers:
                click.echo(f"  {k:<10} {headers[k]}")
        click.echo(f"  snippet   {data.get('snippet', '')[:120]}")


@gmail.command(name="search")
@click.argument("query")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
def gmail_search(ctx, query, limit):
    """Search emails (Gmail query syntax: from:, subject:, has:attachment, etc.)."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{GMAIL_API}/messages", params={"q": query, "maxResults": min(limit, 100)})
    messages = data.get("messages", [])
    results = []
    for m in messages[:min(limit, 20)]:
        msg = _api(token, "GET", f"{GMAIL_API}/messages/{m['id']}",
                   params={"format": "metadata", "metadataHeaders": "From,Subject,Date"})
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        results.append({"id": m["id"], "from": headers.get("From", ""),
                        "subject": headers.get("Subject", ""), "date": headers.get("Date", "")})
    if as_json:
        _out({"query": query, "results": results, "count": len(results)}, True)
    else:
        for r in results:
            click.echo(f"[{r['id']}] {r['from'][:30]}: {r['subject'][:50]}")


@gmail.command(name="trash")
@click.argument("message_id")
@click.pass_context
def gmail_trash(ctx, message_id):
    """Move email to trash."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    _api(token, "POST", f"{GMAIL_API}/messages/{message_id}/trash")
    result = {"id": message_id, "status": "trashed"}
    _out(result, as_json) if as_json else click.echo(f"Trashed: {message_id}")


@gmail.command(name="labels")
@click.pass_context
def gmail_labels(ctx):
    """List Gmail labels."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{GMAIL_API}/labels")
    labels = [{"id": l["id"], "name": l["name"], "type": l.get("type", "")} for l in data.get("labels", [])]
    if as_json:
        _out({"labels": labels}, True)
    else:
        for l in labels:
            click.echo(f"{l['id']:<30} {l['name']}")


@gmail.command(name="reply")
@click.argument("message_id")
@click.option("--body", "-b", required=True)
@click.pass_context
def gmail_reply(ctx, message_id, body):
    """Reply to an email."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    orig = _api(token, "GET", f"{GMAIL_API}/messages/{message_id}",
                params={"format": "metadata", "metadataHeaders": "From,Subject,Message-ID,References"})
    headers = {h["name"]: h["value"] for h in orig.get("payload", {}).get("headers", [])}
    to = headers.get("From", "")
    subject = "Re: " + headers.get("Subject", "")
    msg_id = headers.get("Message-ID", "")
    thread_id = orig.get("threadId")
    raw = _encode_email(to, subject, body, reply_to_id=msg_id)
    data = _api(token, "POST", f"{GMAIL_API}/messages/send",
                body={"raw": raw, "threadId": thread_id})
    result = {"id": data.get("id"), "threadId": thread_id, "to": to}
    _out(result, as_json) if as_json else click.echo(f"Reply sent: {data.get('id')}  to={to}")


# ─────────────────────────────────────────────────────────────────────────────
# CALENDAR
# ─────────────────────────────────────────────────────────────────────────────

CAL_API = "https://www.googleapis.com/calendar/v3"


@cli.group()
def calendar():
    """Google Calendar: events / create / get / delete / calendars."""


@calendar.command(name="calendars")
@click.pass_context
def cal_calendars(ctx):
    """List all calendars."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{CAL_API}/users/me/calendarList")
    cals = [{"id": c["id"], "summary": c.get("summary", ""), "primary": c.get("primary", False), "timeZone": c.get("timeZone", "")} for c in data.get("items", [])]
    if as_json:
        _out({"calendars": cals}, True)
    else:
        for c in cals:
            primary = " [PRIMARY]" if c["primary"] else ""
            click.echo(f"{c['id']:<50} {c['summary']}{primary}")


@calendar.command(name="events")
@click.option("--calendar-id", default="primary", show_default=True)
@click.option("--days", default=7, show_default=True, type=int, help="Upcoming days")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def cal_events(ctx, calendar_id, days, limit):
    """List upcoming calendar events."""
    import datetime
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    now = datetime.datetime.utcnow().isoformat() + "Z"
    end = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + "Z"
    data = _api(token, "GET", f"{CAL_API}/calendars/{urllib.parse.quote(calendar_id)}/events",
                params={"timeMin": now, "timeMax": end, "maxResults": min(limit, 2500),
                        "singleEvents": "true", "orderBy": "startTime"})
    items = data.get("items", [])
    events = []
    for e in items:
        start = e.get("start", {})
        events.append({
            "id": e["id"],
            "summary": e.get("summary", "(no title)"),
            "start": start.get("dateTime") or start.get("date", ""),
            "location": e.get("location", ""),
            "attendees": len(e.get("attendees", [])),
        })
    if as_json:
        _out({"events": events, "count": len(events)}, True)
    else:
        for e in events:
            click.echo(f"{e['start'][:19]:<22} {e['summary'][:50]}")


@calendar.command(name="create")
@click.option("--calendar-id", default="primary")
@click.option("--title", "-t", required=True)
@click.option("--start", required=True, help="ISO datetime (e.g. 2026-03-20T10:00:00)")
@click.option("--end", required=True, help="ISO datetime")
@click.option("--timezone", default="UTC", show_default=True)
@click.option("--description", "-d", default=None)
@click.option("--location", default=None)
@click.option("--attendees", default=None, help="Comma-separated email list")
@click.pass_context
def cal_create(ctx, calendar_id, title, start, end, timezone, description, location, attendees):
    """Create a calendar event."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    body: dict = {
        "summary": title,
        "start": {"dateTime": start, "timeZone": timezone},
        "end": {"dateTime": end, "timeZone": timezone},
    }
    if description:
        body["description"] = description
    if location:
        body["location"] = location
    if attendees:
        body["attendees"] = [{"email": e.strip()} for e in attendees.split(",")]
    data = _api(token, "POST",
                f"{CAL_API}/calendars/{urllib.parse.quote(calendar_id)}/events", body=body)
    result = {"id": data.get("id"), "summary": title, "start": start, "htmlLink": data.get("htmlLink")}
    _out(result, as_json) if as_json else click.echo(f"Event created: {title}  id={data.get('id')}")


@calendar.command(name="get")
@click.argument("event_id")
@click.option("--calendar-id", default="primary")
@click.pass_context
def cal_get(ctx, event_id, calendar_id):
    """Get event details."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET",
                f"{CAL_API}/calendars/{urllib.parse.quote(calendar_id)}/events/{event_id}")
    _out(data, as_json) if as_json else click.echo(json.dumps(data, indent=2, default=str))


@calendar.command(name="delete")
@click.argument("event_id")
@click.option("--calendar-id", default="primary")
@click.option("--yes", is_flag=True)
@click.pass_context
def cal_delete(ctx, event_id, calendar_id, yes):
    """Delete a calendar event."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    if not yes:
        click.confirm(f"Delete event {event_id}?", abort=True)
    _api(token, "DELETE",
         f"{CAL_API}/calendars/{urllib.parse.quote(calendar_id)}/events/{event_id}")
    result = {"id": event_id, "status": "deleted"}
    _out(result, as_json) if as_json else click.echo(f"Deleted: {event_id}")


# ─────────────────────────────────────────────────────────────────────────────
# SHEETS
# ─────────────────────────────────────────────────────────────────────────────

SHEETS_API = "https://sheets.googleapis.com/v4/spreadsheets"


@cli.group()
def sheets():
    """Google Sheets: read / write / append / create / info."""


@sheets.command(name="info")
@click.argument("spreadsheet_id")
@click.pass_context
def sheets_info(ctx, spreadsheet_id):
    """Get spreadsheet metadata."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{SHEETS_API}/{spreadsheet_id}",
                params={"fields": "spreadsheetId,properties,sheets"})
    result = {
        "id": data.get("spreadsheetId"),
        "title": data.get("properties", {}).get("title"),
        "sheets": [s["properties"]["title"] for s in data.get("sheets", [])],
    }
    _out(result, as_json) if as_json else click.echo(json.dumps(result, indent=2))


@sheets.command(name="read")
@click.argument("spreadsheet_id")
@click.argument("range_name", metavar="RANGE")
@click.pass_context
def sheets_read(ctx, spreadsheet_id, range_name):
    """Read values from a range (e.g. Sheet1!A1:C10)."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET",
                f"{SHEETS_API}/{spreadsheet_id}/values/{urllib.parse.quote(range_name)}")
    values = data.get("values", [])
    if as_json:
        _out({"range": data.get("range"), "values": values, "rows": len(values)}, True)
    else:
        for row in values:
            click.echo("\t".join(str(c) for c in row))


@sheets.command(name="write")
@click.argument("spreadsheet_id")
@click.argument("range_name", metavar="RANGE")
@click.option("--values", "-v", required=True, help='JSON 2D array: [["a","b"],["c","d"]]')
@click.option("--input-option", default="USER_ENTERED")
@click.pass_context
def sheets_write(ctx, spreadsheet_id, range_name, values, input_option):
    """Write values to a range (overwrites)."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(
        token, "PUT",
        f"{SHEETS_API}/{spreadsheet_id}/values/{urllib.parse.quote(range_name)}",
        body={"range": range_name, "majorDimension": "ROWS", "values": json.loads(values)},
        params={"valueInputOption": input_option},
    )
    _out(data, as_json) if as_json else click.echo(f"Updated {data.get('updatedCells')} cells")


@sheets.command(name="append")
@click.argument("spreadsheet_id")
@click.argument("range_name", metavar="RANGE")
@click.option("--values", "-v", required=True, help='JSON row: ["val1","val2"] or 2D array')
@click.option("--input-option", default="USER_ENTERED")
@click.pass_context
def sheets_append(ctx, spreadsheet_id, range_name, values, input_option):
    """Append rows to a spreadsheet (after last non-empty row)."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    raw = json.loads(values)
    rows = raw if isinstance(raw[0], list) else [raw]
    data = _api(
        token, "POST",
        f"{SHEETS_API}/{spreadsheet_id}/values/{urllib.parse.quote(range_name)}:append",
        body={"majorDimension": "ROWS", "values": rows},
        params={"valueInputOption": input_option, "insertDataOption": "INSERT_ROWS"},
    )
    _out(data, as_json) if as_json else click.echo(f"Appended {len(rows)} row(s)")


@sheets.command(name="create")
@click.option("--title", "-t", required=True)
@click.option("--sheets", "sheet_titles", default="Sheet1", help="Comma-separated sheet names")
@click.pass_context
def sheets_create(ctx, title, sheet_titles):
    """Create a new spreadsheet."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    sheets_list = [{"properties": {"title": s.strip()}} for s in sheet_titles.split(",")]
    body = {"properties": {"title": title}, "sheets": sheets_list}
    data = _api(token, "POST", SHEETS_API, body=body)
    result = {"id": data.get("spreadsheetId"), "title": title,
              "url": data.get("spreadsheetUrl")}
    _out(result, as_json) if as_json else click.echo(f"Created: {title}  id={result['id']}")


# ─────────────────────────────────────────────────────────────────────────────
# DOCS
# ─────────────────────────────────────────────────────────────────────────────

DOCS_API = "https://docs.googleapis.com/v1/documents"


@cli.group()
def docs():
    """Google Docs: create / get / append / info."""


@docs.command(name="create")
@click.option("--title", "-t", required=True)
@click.option("--content", "-c", default=None, help="Initial paragraph text")
@click.pass_context
def docs_create(ctx, title, content):
    """Create a new Google Doc."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "POST", DOCS_API, body={"title": title})
    doc_id = data.get("documentId")
    if content:
        _api(token, "POST", f"{DOCS_API}/{doc_id}:batchUpdate",
             body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]})
    result = {"id": doc_id, "title": title, "url": f"https://docs.google.com/document/d/{doc_id}/edit"}
    _out(result, as_json) if as_json else click.echo(f"Created: {title}  id={doc_id}")


@docs.command(name="get")
@click.argument("document_id")
@click.option("--text-only", is_flag=True, help="Extract plain text only")
@click.pass_context
def docs_get(ctx, document_id, text_only):
    """Get a Google Doc's content."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{DOCS_API}/{document_id}")
    if text_only:
        text_parts = []
        for elem in data.get("body", {}).get("content", []):
            for para in elem.get("paragraph", {}).get("elements", []):
                text_parts.append(para.get("textRun", {}).get("content", ""))
        result = {"id": document_id, "title": data.get("title"), "text": "".join(text_parts)}
        _out(result, as_json) if as_json else click.echo(result["text"])
    else:
        _out({"id": document_id, "title": data.get("title"), "revisionId": data.get("revisionId")}, as_json) if as_json else click.echo(json.dumps({"id": document_id, "title": data.get("title")}, indent=2))


@docs.command(name="info")
@click.argument("document_id")
@click.pass_context
def docs_info(ctx, document_id):
    """Get document metadata."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{DOCS_API}/{document_id}",
                params={"fields": "documentId,title,revisionId,documentStyle"})
    _out(data, as_json) if as_json else click.echo(json.dumps(data, indent=2, default=str))


@docs.command(name="append")
@click.argument("document_id")
@click.argument("text")
@click.option("--newline/--no-newline", default=True)
@click.pass_context
def docs_append(ctx, document_id, text, newline):
    """Append text to a Google Doc (at end)."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    doc = _api(token, "GET", f"{DOCS_API}/{document_id}",
               params={"fields": "body.content"})
    # Get end index
    last_idx = max((e.get("endIndex", 1) for c in doc.get("body", {}).get("content", [])
                    for e in [c] if "endIndex" in c), default=1)
    insert_text = ("\n" if newline else "") + text
    _api(token, "POST", f"{DOCS_API}/{document_id}:batchUpdate",
         body={"requests": [{"insertText": {"location": {"index": last_idx - 1}, "text": insert_text}}]})
    result = {"id": document_id, "appended": len(insert_text), "status": "ok"}
    _out(result, as_json) if as_json else click.echo(f"Appended {len(insert_text)} chars to {document_id}")


# ─────────────────────────────────────────────────────────────────────────────
# CHAT
# ─────────────────────────────────────────────────────────────────────────────

CHAT_API = "https://chat.googleapis.com/v1"


@cli.group()
def chat():
    """Google Chat: spaces / messages / send."""


@chat.command(name="spaces")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def chat_spaces(ctx, limit):
    """List Google Chat spaces."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{CHAT_API}/spaces", params={"pageSize": min(limit, 1000)})
    spaces = [{"name": s["name"], "displayName": s.get("displayName", ""), "type": s.get("type", "")}
              for s in data.get("spaces", [])]
    if as_json:
        _out({"spaces": spaces, "count": len(spaces)}, True)
    else:
        for s in spaces:
            click.echo(f"{s['name']:<35} {s['displayName']}")


@chat.command(name="send")
@click.argument("space_name")
@click.argument("text")
@click.pass_context
def chat_send(ctx, space_name, text):
    """Send a message to a Google Chat space."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "POST", f"{CHAT_API}/{space_name}/messages", body={"text": text})
    result = {"name": data.get("name"), "space": space_name, "text": text[:50]}
    _out(result, as_json) if as_json else click.echo(f"Sent to {space_name}: {text[:60]}")


@chat.command(name="messages")
@click.argument("space_name")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def chat_messages(ctx, space_name, limit):
    """List messages in a Chat space."""
    token = _get_token(ctx)
    as_json = ctx.obj["json"]
    data = _api(token, "GET", f"{CHAT_API}/{space_name}/messages",
                params={"pageSize": min(limit, 1000)})
    msgs = [{"name": m["name"], "sender": m.get("sender", {}).get("displayName", ""),
             "text": m.get("text", "")[:80], "createTime": m.get("createTime", "")}
            for m in data.get("messages", [])]
    if as_json:
        _out({"messages": msgs, "count": len(msgs)}, True)
    else:
        for m in msgs:
            click.echo(f"{m['createTime'][:19]:<22} @{m['sender'][:20]}: {m['text'][:60]}")


if __name__ == "__main__":
    cli()
