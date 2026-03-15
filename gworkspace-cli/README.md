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
