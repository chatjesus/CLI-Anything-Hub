# Slack CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./slack-cli
```

## Setup

```bash
export SLACK_BOT_TOKEN=xoxb-...
```

## Quick Start

```bash
# Check connectivity
cli-anything-slack detect

# Discover capabilities
cli-anything-slack schema

# Example
cli-anything-slack --json message send #general "Hello"

# Example
cli-anything-slack --json channels list

# Example
cli-anything-slack --json users list
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-slack --json message send #general "Hello"
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

### How do I install cli-anything-slack?

```bash
pip install cli-anything-slack
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/slack/).

### How do I check if the software is available?

```bash
cli-anything-slack detect --json
```

Returns a JSON object with installation status and version information.
