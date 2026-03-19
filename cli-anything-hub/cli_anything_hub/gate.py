"""
Pro feature gating for CLI-Anything Hub.

Usage in any CLI:

    from cli_anything_hub import require_pro

    @cli.command()
    @require_pro
    @click.pass_context
    def expensive_command(ctx):
        # Only runs if user has Pro subscription
        ...

Or for a whole command group:

    @cli.group()
    @require_pro
    def advanced():
        '''Advanced features (Pro only).'''
"""
import functools
import webbrowser

import click

from .auth import is_pro, is_logged_in, get_plan_display, get_email
from .subscription import PLANS

UPGRADE_URL = "https://agentputer.com/cli-anything/pricing"


def require_pro(fn):
    """Decorator that gates a click command behind Pro subscription."""
    @functools.wraps(fn)
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        if is_pro():
            return ctx.invoke(fn, *args, **kwargs)

        click.echo("")
        click.echo("⚡ This is a Pro feature.")
        click.echo("")

        if not is_logged_in():
            click.echo("   You're not logged in yet.")
            click.echo("   Run: cli-anything login --email you@example.com")
            click.echo("")
        else:
            click.echo(f"   Logged in as: {get_email()}")
            click.echo(f"   Current plan: {get_plan_display()}")
            click.echo("")

        click.echo("   📋 Available plans:")
        for p in PLANS:
            click.echo(f"      • {p['name']:<10} {p['price']:<16} — {p['description']}")
        click.echo("")
        click.echo("   Subscribe:  cli-anything subscribe create --plan monthly --email you@co.com")
        click.echo(f"   Or visit:   {UPGRADE_URL}")
        click.echo("")

        if click.confirm("   Open pricing page in browser?", default=False):
            webbrowser.open(UPGRADE_URL)

    return wrapper


def pro_command(group, name=None, **kwargs):
    """
    Convenience: register a Pro-gated command on a click group.

        @pro_command(cli, name="export")
        @click.option("--format", ...)
        @click.pass_context
        def export_data(ctx, format):
            ...
    """
    def decorator(fn):
        fn = require_pro(fn)
        return group.command(name=name, **kwargs)(fn)
    return decorator
