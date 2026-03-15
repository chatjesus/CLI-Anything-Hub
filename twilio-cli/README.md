# Twilio CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./twilio-cli
```

## Setup

```bash
export TWILIO_AUTH_TOKEN=your-auth-token
```

## Quick Start

```bash
# Check connectivity
cli-anything-twilio detect

# Discover capabilities
cli-anything-twilio schema

# Example
cli-anything-twilio --json sms send --to +1234567890 --body "Hello"

# Example
cli-anything-twilio --json calls list --limit 10

# Example
cli-anything-twilio --json account info
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-twilio --json sms send --to +1234567890 --body "Hello"
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
