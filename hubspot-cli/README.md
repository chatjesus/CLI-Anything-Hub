# HubSpot CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./hubspot-cli
```

## Setup

```bash
export HUBSPOT_ACCESS_TOKEN=pat-...
```

## Quick Start

```bash
# Check connectivity
cli-anything-hubspot detect

# Discover capabilities
cli-anything-hubspot schema

# Example
cli-anything-hubspot --json contacts list

# Example
cli-anything-hubspot --json deals list

# Example
cli-anything-hubspot --json companies list
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-hubspot --json contacts list
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
