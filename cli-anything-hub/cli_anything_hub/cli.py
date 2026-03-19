"""
cli-anything — Main entry point for CLI-Anything Hub.

Commands:
  subscribe list                     Show available plans
  subscribe create --plan --email    Start Stripe Checkout
  login --email --send-code          Send verification code
  login --email --code <code>        Verify and log in
  activate <LICENSE_KEY>             Activate license key
  status                             Show current auth state
  doctor                             Full diagnostic check
  logout                             Clear local credentials
"""
import json
import sys
import platform
import shutil

import click

from . import __version__
from .auth import (
    get_credentials,
    save_credentials,
    clear_credentials,
    is_logged_in,
    is_pro,
    get_email,
    get_plan,
    get_plan_display,
    get_subscription_status,
    get_config_dir,
)
from .subscription import (
    list_plans,
    create_checkout_session,
    verify_subscription,
    send_login_code,
    verify_login_code,
    activate_license_key,
)


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if isinstance(data, dict):
            for k, v in data.items():
                if v is not None:
                    click.echo(f"  {k:<24} {v}")
        else:
            click.echo(str(data))


# ── ROOT ─────────────────────────────────────────────────────────────────────

@click.group()
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@click.pass_context
def cli(ctx, as_json):
    """cli-anything — Hub manager for 160+ agent-ready CLIs.

    Subscribe, authenticate, and manage your CLI-Anything Pro account.
    """
    ctx.ensure_object(dict)
    ctx.obj["json"] = as_json


# ── SUBSCRIBE ────────────────────────────────────────────────────────────────

@cli.group()
def subscribe():
    """Subscription management (list plans / create checkout)."""


@subscribe.command(name="list")
@click.pass_context
def subscribe_list(ctx):
    """Show available subscription plans."""
    as_json = ctx.obj["json"]
    plans = list_plans()
    if as_json:
        _out({"plans": plans}, True)
    else:
        click.echo("")
        click.echo("  📋 CLI-Anything Pro Plans")
        click.echo("  ─────────────────────────────────────────────────")
        for p in plans:
            click.echo(f"  • {p['name']:<10} {p['price']:<16} {p['description']}")
        click.echo("")
        click.echo("  Subscribe: cli-anything subscribe create --plan monthly --email you@co.com")
        click.echo("")


@subscribe.command(name="create")
@click.option("--plan", required=True, type=click.Choice(["weekly", "monthly", "yearly"]), help="Plan ID")
@click.option("--email", required=True, help="Your email address")
@click.pass_context
def subscribe_create(ctx, plan, email):
    """Create a Stripe Checkout session and open payment page."""
    as_json = ctx.obj["json"]
    click.echo(f"  Creating checkout for {plan} plan...") if not as_json else None
    result = create_checkout_session(plan, email)

    if result.get("error"):
        if as_json:
            _out(result, True)
        else:
            click.echo(f"  ❌ {result.get('message', 'Unknown error')}")
        sys.exit(1)

    if as_json:
        _out(result, True)
    else:
        click.echo("")
        click.echo("  ✅ Payment page opened in your browser!")
        click.echo("")
        click.echo("  After completing payment:")
        click.echo(f"    1. Run: cli-anything login --email {email} --send-code")
        click.echo(f"    2. Check your email for the 6-digit code")
        click.echo(f"    3. Run: cli-anything login --email {email} --code <CODE>")
        click.echo("")
        click.echo("  Or if you received a license key:")
        click.echo("    cli-anything activate <YOUR_LICENSE_KEY>")
        click.echo("")


@subscribe.command(name="status")
@click.pass_context
def subscribe_status(ctx):
    """Check subscription status from server (syncs local state)."""
    as_json = ctx.obj["json"]
    email = get_email()
    if not email:
        msg = "Not logged in. Run: cli-anything login --email you@co.com --send-code"
        if as_json:
            _out({"error": True, "message": msg}, True)
        else:
            click.echo(f"  ❌ {msg}")
        sys.exit(1)

    token = get_credentials().get("access_token")
    result = verify_subscription(email, token)
    if result.get("error"):
        if as_json:
            _out(result, True)
        else:
            click.echo(f"  ❌ {result.get('message', 'Could not verify')}")
        sys.exit(1)

    if result.get("plan"):
        save_credentials(
            plan=result["plan"],
            subscription_id=result.get("subscription_id"),
            subscription_expires_at=result.get("expires_at"),
            customer_id=result.get("customer_id"),
        )

    if as_json:
        _out(result, True)
    else:
        click.echo("")
        click.echo(f"  Email:        {result.get('email', email)}")
        click.echo(f"  Plan:         {result.get('plan', 'free')}")
        click.echo(f"  Status:       {result.get('status', 'unknown')}")
        if result.get("expires_at"):
            import datetime
            exp = datetime.datetime.fromtimestamp(result["expires_at"]).strftime("%Y-%m-%d")
            click.echo(f"  Expires:      {exp}")
        click.echo("")


# ── LOGIN ────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--email", required=True, help="Your email address")
@click.option("--send-code", "do_send", is_flag=True, help="Send a verification code to email")
@click.option("--code", default=None, help="6-digit verification code")
@click.pass_context
def login(ctx, email, do_send, code):
    """Log in with email verification code."""
    as_json = ctx.obj["json"]

    if do_send and not code:
        result = send_login_code(email)
        if result.get("error"):
            if as_json:
                _out(result, True)
            else:
                click.echo(f"  ❌ {result.get('message', 'Failed to send code')}")
            sys.exit(1)

        if as_json:
            _out({"status": "code_sent", "email": email}, True)
        else:
            click.echo("")
            click.echo(f"  ✅ Verification code sent to {email}")
            click.echo("  Check your inbox (and spam folder).")
            click.echo("")
            click.echo(f"  Next: cli-anything login --email {email} --code <6-DIGIT-CODE>")
            click.echo("")
        return

    if code:
        result = verify_login_code(email, code)
        if result.get("error"):
            if as_json:
                _out(result, True)
            else:
                click.echo(f"  ❌ {result.get('message', 'Invalid code')}")
                click.echo(f"  Try again: cli-anything login --email {email} --send-code")
            sys.exit(1)

        save_credentials(
            email=email,
            access_token=result.get("access_token"),
            plan=result.get("plan", "free"),
            customer_id=result.get("customer_id"),
            subscription_id=result.get("subscription_id"),
            subscription_expires_at=result.get("expires_at"),
        )

        if as_json:
            _out({
                "status": "logged_in",
                "email": email,
                "plan": result.get("plan", "free"),
                "is_pro": result.get("plan", "free") != "free",
            }, True)
        else:
            plan = result.get("plan", "free")
            click.echo("")
            click.echo(f"  ✅ Logged in as {email}")
            click.echo(f"  Plan: {plan}")
            if plan != "free":
                click.echo("  All Pro features are now unlocked across every CLI!")
            else:
                click.echo("  Upgrade: cli-anything subscribe list")
            click.echo("")
        return

    click.echo("  Provide --send-code to get a code, or --code <CODE> to verify.")
    click.echo(f"  Example: cli-anything login --email {email} --send-code")


# ── ACTIVATE ─────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("license_key")
@click.pass_context
def activate(ctx, license_key):
    """Activate a license key (received after purchase)."""
    as_json = ctx.obj["json"]
    result = activate_license_key(license_key)

    if result.get("error"):
        if as_json:
            _out(result, True)
        else:
            click.echo(f"  ❌ {result.get('message', 'Invalid license key')}")
        sys.exit(1)

    save_credentials(
        email=result.get("email"),
        access_token=result.get("access_token"),
        plan=result.get("plan", "free"),
        customer_id=result.get("customer_id"),
        subscription_id=result.get("subscription_id"),
        subscription_expires_at=result.get("expires_at"),
        license_key=license_key,
    )

    if as_json:
        _out({
            "status": "activated",
            "email": result.get("email"),
            "plan": result.get("plan"),
        }, True)
    else:
        click.echo("")
        click.echo(f"  ✅ License activated!")
        click.echo(f"  Email: {result.get('email')}")
        click.echo(f"  Plan:  {result.get('plan')}")
        click.echo("  All Pro features are now unlocked across every CLI!")
        click.echo("")


# ── STATUS ───────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def status(ctx):
    """Show current authentication and subscription status."""
    as_json = ctx.obj["json"]
    info = get_subscription_status()

    if as_json:
        _out(info, True)
    else:
        click.echo("")
        click.echo("  CLI-Anything Hub Status")
        click.echo("  ───────────────────────────────")
        if info["logged_in"]:
            click.echo(f"  Email:   {info['email']}")
            click.echo(f"  Plan:    {info['plan_display']}")
            click.echo(f"  Pro:     {'✅ Yes' if info['is_pro'] else '❌ No'}")
            if info.get("expires_at"):
                import datetime
                exp = datetime.datetime.fromtimestamp(info["expires_at"]).strftime("%Y-%m-%d")
                click.echo(f"  Expires: {exp}")
        else:
            click.echo("  Status:  Not logged in")
            click.echo("")
            click.echo("  Get started:")
            click.echo("    cli-anything subscribe list")
            click.echo("    cli-anything login --email you@co.com --send-code")
        click.echo("")


# ── DOCTOR ───────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def doctor(ctx):
    """Run diagnostics — check environment, auth, subscription, and network."""
    as_json = ctx.obj["json"]
    checks = {}

    checks["cli_version"] = __version__
    checks["python"] = platform.python_version()
    checks["os"] = f"{platform.system()} {platform.release()}"
    checks["config_dir"] = str(get_config_dir())
    checks["logged_in"] = is_logged_in()
    checks["email"] = get_email()
    checks["plan"] = get_plan()
    checks["is_pro"] = is_pro()

    try:
        from urllib.request import urlopen
        resp = urlopen("https://api.agentputer.com/health", timeout=5)
        checks["api_reachable"] = resp.status == 200
    except Exception:
        checks["api_reachable"] = False

    installed_clis = []
    for cli_name in [
        "cli-anything-slack", "cli-anything-stripe", "cli-anything-docker",
        "cli-anything-github", "cli-anything-notion", "cli-anything-discord",
        "cli-anything-telegram", "cli-anything-shopify", "cli-anything-ollama",
    ]:
        if shutil.which(cli_name):
            installed_clis.append(cli_name)
    checks["installed_clis"] = installed_clis
    checks["installed_count"] = len(installed_clis)

    if as_json:
        _out(checks, True)
    else:
        click.echo("")
        click.echo("  🩺 CLI-Anything Doctor")
        click.echo("  ───────────────────────────────────────")
        click.echo(f"  Version:       {checks['cli_version']}")
        click.echo(f"  Python:        {checks['python']}")
        click.echo(f"  OS:            {checks['os']}")
        click.echo(f"  Config:        {checks['config_dir']}")
        click.echo(f"  API:           {'✅ Reachable' if checks['api_reachable'] else '❌ Unreachable'}")
        click.echo(f"  Logged in:     {'✅ ' + (checks['email'] or '') if checks['logged_in'] else '❌ No'}")
        click.echo(f"  Plan:          {checks['plan']}")
        click.echo(f"  Pro:           {'✅ Yes' if checks['is_pro'] else '❌ No'}")
        click.echo(f"  Installed CLIs: {checks['installed_count']}")
        if installed_clis:
            for c in installed_clis:
                click.echo(f"    • {c}")
        click.echo("")
        if not checks["logged_in"]:
            click.echo("  💡 Next: cli-anything login --email you@co.com --send-code")
        elif not checks["is_pro"]:
            click.echo("  💡 Next: cli-anything subscribe list")
        else:
            click.echo("  ✅ Everything looks good!")
        click.echo("")


# ── LOGOUT ───────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def logout(ctx):
    """Clear all local credentials and log out."""
    as_json = ctx.obj["json"]
    email = get_email()
    clear_credentials()

    if as_json:
        _out({"status": "logged_out", "email": email}, True)
    else:
        click.echo(f"  ✅ Logged out{' (' + email + ')' if email else ''}")
        click.echo("  Local credentials cleared.")


# ── SCHEMA ───────────────────────────────────────────────────────────────────

@cli.command()
def schema():
    """Output full capability JSON (for agent discovery, no auth needed)."""
    info = {
        "name": "cli-anything",
        "version": __version__,
        "description": "Hub manager for 160+ agent-ready CLIs — subscribe, login, diagnose",
        "requires_token": False,
        "commands": [
            {"cmd": "subscribe list", "args": [], "desc": "Show available subscription plans"},
            {"cmd": "subscribe create", "args": [
                {"name": "--plan", "type": "choice", "choices": ["weekly", "monthly", "yearly"], "required": True},
                {"name": "--email", "type": "str", "required": True},
            ], "desc": "Create Stripe Checkout session"},
            {"cmd": "subscribe status", "args": [], "desc": "Check subscription status from server"},
            {"cmd": "login", "args": [
                {"name": "--email", "type": "str", "required": True},
                {"name": "--send-code", "type": "flag"},
                {"name": "--code", "type": "str"},
            ], "desc": "Log in with email verification"},
            {"cmd": "activate", "args": [{"name": "LICENSE_KEY", "type": "str"}], "desc": "Activate license key"},
            {"cmd": "status", "args": [], "desc": "Show current auth state"},
            {"cmd": "doctor", "args": [], "desc": "Run full diagnostics"},
            {"cmd": "logout", "args": [], "desc": "Clear credentials"},
        ],
        "json_flag": "--json",
        "example": "cli-anything subscribe list",
    }
    click.echo(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
