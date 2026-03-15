# Salesforce CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./salesforce-cli
```

## Setup

```bash
export SF_ACCESS_TOKEN=your-token
```

## Quick Start

```bash
# Check connectivity
cli-anything-salesforce detect

# Discover capabilities
cli-anything-salesforce schema

# Example
cli-anything-salesforce --json query "SELECT Id, Name FROM Account LIMIT 5"

# Example
cli-anything-salesforce --json describe Account

# Example
cli-anything-salesforce --json limits
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-salesforce --json query "SELECT Id, Name FROM Account LIMIT 5"
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
