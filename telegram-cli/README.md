# Telegram CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./telegram-cli
```

## Setup

```bash
export TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
```

## Quick Start

```bash
# Check connectivity
cli-anything-telegram detect

# Discover capabilities
cli-anything-telegram schema

# Example
cli-anything-telegram --json message send CHAT_ID "Hello"

# Example
cli-anything-telegram --json me

# Example
cli-anything-telegram --json updates
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-telegram --json message send CHAT_ID "Hello"
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
