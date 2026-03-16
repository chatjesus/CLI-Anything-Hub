# Google Workspace CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./gworkspace-cli
```

## Setup

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
```

## Quick Start

```bash
# Check connectivity
cli-anything-gworkspace detect

# Discover capabilities
cli-anything-gworkspace schema

# Example
cli-anything-gworkspace --json drive list

# Example
cli-anything-gworkspace --json gmail send --to user@co.com -s Subject -b Body

# Example
cli-anything-gworkspace --json calendar events --days 7
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-gworkspace --json drive list
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

### How do I install cli-anything-gworkspace?

```bash
pip install cli-anything-gworkspace
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/gworkspace/).

### How do I check if the software is available?

```bash
cli-anything-gworkspace detect --json
```

Returns a JSON object with installation status and version information.
