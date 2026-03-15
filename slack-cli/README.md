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
