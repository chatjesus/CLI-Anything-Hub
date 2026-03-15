# Stripe CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./stripe-cli
```

## Setup

```bash
export STRIPE_SECRET_KEY=sk_test_...
```

## Quick Start

```bash
# Check connectivity
cli-anything-stripe detect

# Discover capabilities
cli-anything-stripe schema

# Example
cli-anything-stripe --json customers list --limit 5

# Example
cli-anything-stripe --json payment create --amount 1999

# Example
cli-anything-stripe --json subscriptions list
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-stripe --json customers list --limit 5
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
