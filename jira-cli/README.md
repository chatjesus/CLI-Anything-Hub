# Jira CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

## Install

```bash
pip install -e ./jira-cli
```

## Setup

```bash
export JIRA_API_TOKEN=your-api-token
```

## Quick Start

```bash
# Check connectivity
cli-anything-jira detect

# Discover capabilities
cli-anything-jira schema

# Example
cli-anything-jira --json issues search "project=PROJ" --limit 10

# Example
cli-anything-jira --json issue get PROJ-123

# Example
cli-anything-jira --json projects list
```

## Agent Usage

```bash
# All commands support --json for structured output
cli-anything-jira --json issues search "project=PROJ" --limit 10
```

## Links

- [CLI Anything Hub](https://www.agentputer.com/cli-anything)
- [GitHub](https://github.com/chatjesus/CLI-Anything-Hub)
- [MIT License](https://github.com/chatjesus/CLI-Anything-Hub/blob/main/LICENSE)
