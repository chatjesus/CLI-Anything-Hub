# Microsoft 365 CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./ms365-cli
```

## Setup

No API key needed. Uses local COM automation (Windows only).

## Quick Start

```bash
# Check connectivity
cli-anything-ms365 detect

# Discover capabilities
cli-anything-ms365 schema

# Example
cli-anything-ms365 --json word create output.docx --text Hello

# Example
cli-anything-ms365 --json excel create data.xlsx

# Example
cli-anything-ms365 --json outlook send --to user@co.com
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-ms365 --json word create output.docx --text Hello
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

### How do I install cli-anything-ms365?

```bash
pip install cli-anything-ms365
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/ms365/).

### How do I check if the software is available?

```bash
cli-anything-ms365 detect --json
```

Returns a JSON object with installation status and version information.
