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

---

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies software availability before use
- Predictable exit codes: 0 (success), 1 (error), 2 (usage error)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## FAQ

### How do I install cli-anything-stripe?

```bash
pip install cli-anything-stripe
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/stripe/).

### How do I check if the software is available?

```bash
cli-anything-stripe detect --json
```

Returns a JSON object with installation status and version information.
