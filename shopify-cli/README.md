# Shopify CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./shopify-cli
```

## Setup

```bash
export SHOPIFY_ACCESS_TOKEN=shpat_...
```

## Quick Start

```bash
# Check connectivity
cli-anything-shopify detect

# Discover capabilities
cli-anything-shopify schema

# Example
cli-anything-shopify --json products list

# Example
cli-anything-shopify --json orders list --limit 10

# Example
cli-anything-shopify --json inventory list
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-shopify --json products list
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
