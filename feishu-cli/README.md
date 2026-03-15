# Feishu CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./feishu-cli
```

## Setup

```bash
export FEISHU_APP_ID=your-app-id
```

## Quick Start

```bash
# Check connectivity
cli-anything-feishu detect

# Discover capabilities
cli-anything-feishu schema

# Example
cli-anything-feishu --json message send CHAT_ID "Hello"

# Example
cli-anything-feishu --json contacts list

# Example
cli-anything-feishu --json calendar events
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-feishu --json message send CHAT_ID "Hello"
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
