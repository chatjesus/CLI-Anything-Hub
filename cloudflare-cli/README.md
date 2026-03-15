# Cloudflare CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./cloudflare-cli
```

## Setup

```bash
export CF_API_TOKEN=your-cf-token
```

## Quick Start

```bash
# Check connectivity
cli-anything-cloudflare detect

# Discover capabilities
cli-anything-cloudflare schema

# Example
cli-anything-cloudflare --json zones list

# Example
cli-anything-cloudflare --json dns list ZONE_ID

# Example
cli-anything-cloudflare --json workers list
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-cloudflare --json zones list
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
