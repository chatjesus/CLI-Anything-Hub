# Discord CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./discord-cli
```

## Setup

```bash
export DISCORD_BOT_TOKEN=your-bot-token
```

## Quick Start

```bash
# Check connectivity
cli-anything-discord detect

# Discover capabilities
cli-anything-discord schema

# Example
cli-anything-discord --json message send CHANNEL_ID "Hello"

# Example
cli-anything-discord --json guilds list

# Example
cli-anything-discord --json channels list GUILD_ID
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-discord --json message send CHANNEL_ID "Hello"
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
