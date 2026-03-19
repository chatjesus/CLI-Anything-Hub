# cli-anything-hub

Shared authentication, subscription, and Pro feature gating for all **CLI-Anything** tools.

One login → all 160+ CLIs unlocked.

## Install

```bash
pip install -e ./cli-anything-hub
```

## Commands

```bash
# Show available plans
cli-anything subscribe list

# Start a subscription (opens Stripe Checkout)
cli-anything subscribe create --plan monthly --email you@co.com

# Login with email verification
cli-anything login --email you@co.com --send-code
cli-anything login --email you@co.com --code 123456

# Or activate a license key
cli-anything activate YOUR_LICENSE_KEY

# Check current status
cli-anything status

# Run diagnostics
cli-anything doctor

# Log out
cli-anything logout
```

## For CLI Authors — Gating Pro Features

```python
from cli_anything_hub import require_pro

@cli.command()
@require_pro
@click.pass_context
def expensive_export(ctx):
    """This command requires a Pro subscription."""
    # Your code here — only runs for Pro users
```

## Architecture

```
~/.cli-anything/
  └── credentials.json    # Shared by all CLIs (chmod 600)

CLI-Anything Hub API (api.agentputer.com)
  ├── POST /subscribe/create     → Stripe Checkout Session
  ├── GET  /subscribe/status     → Subscription verification
  ├── POST /auth/send-code       → Email verification
  ├── POST /auth/verify-code     → Login + token
  └── POST /auth/activate        → License key activation
```
