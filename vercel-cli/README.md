# Vercel CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./vercel-cli
```

## Setup

```bash
export VERCEL_TOKEN=your-vercel-token
```

## Quick Start

```bash
# Check connectivity
cli-anything-vercel detect

# Discover capabilities
cli-anything-vercel schema

# Example
cli-anything-vercel --json projects list

# Example
cli-anything-vercel --json deployments list --limit 5

# Example
cli-anything-vercel --json domains list
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-vercel --json projects list
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
