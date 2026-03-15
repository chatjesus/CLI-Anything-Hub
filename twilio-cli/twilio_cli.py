"""cli-anything-twilio -- Twilio SMS/Voice/WhatsApp CLI"""
import json, os, sys, urllib.request, urllib.parse, urllib.error, base64
import click

def _err(msg):
    click.echo(json.dumps({"error": msg}), err=True)
    sys.exit(1)

def _req(ctx, method, path, form=None):
    sid = ctx.obj.get("sid") or _err("TWILIO_ACCOUNT_SID not set")
    token = ctx.obj.get("token") or _err("TWILIO_AUTH_TOKEN not set")
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}{path}"
    data = urllib.parse.urlencode(form).encode() if form else None
    req = urllib.request.Request(url, data=data, method=method)
    cred = base64.b64encode(f"{sid}:{token}".encode()).decode()
    req.add_header("Authorization", f"Basic {cred}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        _err(f"HTTP {e.code}: {e.read().decode()}")

def _out(ctx, data):
    if ctx.obj.get("json"):
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        if isinstance(data, dict) and "messages" in data:
            for m in data["messages"]:
                click.echo(f"  {m.get('sid')}  {m.get('status')}  to={m.get('to')}  from={m.get('from')}  body={str(m.get('body',''))[:40]}")
        elif isinstance(data, list):
            for item in data:
                click.echo(json.dumps(item, ensure_ascii=False))
        else:
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))

@click.group()
@click.option("--sid", envvar="TWILIO_ACCOUNT_SID", default=None)
@click.option("--token", envvar="TWILIO_AUTH_TOKEN", default=None)
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@click.pass_context
def cli(ctx, sid, token, as_json):
    """cli-anything-twilio -- SMS, Voice, WhatsApp via Twilio REST API"""
    ctx.ensure_object(dict)
    ctx.obj["sid"] = sid
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json

@cli.command()
@click.pass_context
def detect(ctx):
    """Check Twilio credentials."""
    r = _req(ctx, "GET", ".json")
    _out(ctx, {"status": "ok", "account": r.get("friendly_name"), "type": r.get("type"), "status": r.get("status")})

@cli.command()
@click.pass_context
def schema(ctx):
    """Output capability schema (no credentials needed)."""
    info = {
        "name": "cli-anything-twilio", "version": "1.0.0",
        "description": "Twilio REST API CLI - SMS, Voice calls, WhatsApp, phone numbers",
        "requires_token": True,
        "env_vars": {"TWILIO_ACCOUNT_SID": "AC...", "TWILIO_AUTH_TOKEN": "auth token from console.twilio.com"},
        "commands": [
            {"cmd": "detect", "desc": "Verify credentials"},
            {"cmd": "sms send", "args": ["--to STR", "--from STR", "--body STR"], "desc": "Send SMS"},
            {"cmd": "sms list", "args": ["--limit INT", "--to STR"], "desc": "List SMS messages"},
            {"cmd": "calls make", "args": ["--to STR", "--from STR", "--twiml URL"], "desc": "Make a voice call"},
            {"cmd": "calls list", "args": ["--limit INT"], "desc": "List calls"},
            {"cmd": "whatsapp send", "args": ["--to STR", "--from STR", "--body STR"], "desc": "Send WhatsApp message"},
            {"cmd": "numbers list", "args": [], "desc": "List owned phone numbers"},
        ],
        "json_flag": "--json",
        "example": "twilio-cli --json sms send --to +1234567890 --from +19876543210 --body 'Hello'",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))

@cli.group()
def sms():
    """Send and manage SMS messages."""

@sms.command("send")
@click.option("--to", required=True, help="Destination number +1234567890")
@click.option("--from", "from_", envvar="TWILIO_FROM_NUMBER", required=True, help="Your Twilio number")
@click.option("--body", required=True, help="Message body")
@click.pass_context
def sms_send(ctx, to, from_, body):
    """Send an SMS message."""
    r = _req(ctx, "POST", "/Messages.json", {"To": to, "From": from_, "Body": body})
    _out(ctx, {"status": "ok", "sid": r.get("sid"), "status": r.get("status"), "to": r.get("to")})

@sms.command("list")
@click.option("--limit", default=20)
@click.option("--to", "to_filter", default=None)
@click.pass_context
def sms_list(ctx, limit, to_filter):
    """List SMS messages."""
    qs = f"?PageSize={limit}" + (f"&To={urllib.parse.quote(to_filter)}" if to_filter else "")
    r = _req(ctx, "GET", f"/Messages.json{qs}")
    _out(ctx, r)

@cli.group()
def calls():
    """Make and list voice calls."""

@calls.command("make")
@click.option("--to", required=True)
@click.option("--from", "from_", envvar="TWILIO_FROM_NUMBER", required=True)
@click.option("--twiml", required=True, help="URL that returns TwiML, e.g. http://demo.twilio.com/docs/voice.xml")
@click.pass_context
def calls_make(ctx, to, from_, twiml):
    """Initiate a voice call."""
    r = _req(ctx, "POST", "/Calls.json", {"To": to, "From": from_, "Url": twiml})
    _out(ctx, {"status": "ok", "sid": r.get("sid"), "call_status": r.get("status")})

@calls.command("list")
@click.option("--limit", default=20)
@click.pass_context
def calls_list(ctx, limit):
    """List recent calls."""
    r = _req(ctx, "GET", f"/Calls.json?PageSize={limit}")
    _out(ctx, r)

@cli.group()
def whatsapp():
    """Send WhatsApp messages via Twilio."""

@whatsapp.command("send")
@click.option("--to", required=True, help="whatsapp:+1234567890")
@click.option("--from", "from_", envvar="TWILIO_WHATSAPP_NUMBER", required=True, help="whatsapp:+14155238886")
@click.option("--body", required=True)
@click.pass_context
def whatsapp_send(ctx, to, from_, body):
    """Send a WhatsApp message."""
    to_wa = to if to.startswith("whatsapp:") else f"whatsapp:{to}"
    from_wa = from_ if from_.startswith("whatsapp:") else f"whatsapp:{from_}"
    r = _req(ctx, "POST", "/Messages.json", {"To": to_wa, "From": from_wa, "Body": body})
    _out(ctx, {"status": "ok", "sid": r.get("sid"), "status": r.get("status")})

@cli.group()
def numbers():
    """Manage phone numbers."""

@numbers.command("list")
@click.pass_context
def numbers_list(ctx):
    """List owned phone numbers."""
    r = _req(ctx, "GET", "/IncomingPhoneNumbers.json")
    _out(ctx, r)

if __name__ == "__main__":
    cli()
