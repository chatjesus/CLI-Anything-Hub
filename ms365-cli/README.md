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
