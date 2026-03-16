# cli-anything-zoom

CLI harness for **Zoom** — manage meetings, participants, and recordings from the command line via the Zoom REST API.

## Installation

```bash
pip install cli-anything-zoom
# or from source:
cd zoom/agent-harness && pip install -e .
```

## Prerequisites

1. A Zoom account (free or paid)
2. A Zoom OAuth App — create one at https://marketplace.zoom.us/develop/create
   - App type: **General App** (OAuth)
   - Redirect URL: `http://localhost:4199/callback`
   - Required scopes: `user:read:admin`, `meeting:read:admin`, `meeting:write:admin`, `recording:read:admin`

## Quick Start

```bash
# 1. Configure OAuth credentials
cli-anything-zoom auth setup --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET

# 2. Login (opens browser)
cli-anything-zoom auth login

# 3. Create a meeting
cli-anything-zoom meeting create --topic "Team Standup" --duration 30

# 4. List meetings
cli-anything-zoom meeting list

# 5. Interactive mode
cli-anything-zoom repl
```

## Commands

| Group | Commands |
|---|---|
| `auth` | `setup`, `login`, `status`, `logout` |
| `meeting` | `create`, `list`, `info`, `update`, `delete`, `join`, `start` |
| `participant` | `add`, `add-batch`, `list`, `remove`, `attended` |
| `recording` | `list`, `files`, `download`, `delete` |

## Agent Usage (JSON mode)

All commands support `--json` for machine-readable output:

```bash
cli-anything-zoom --json meeting list
cli-anything-zoom --json meeting create --topic "Sync" --duration 60 --auto-recording cloud
```

---

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies software availability before use
- Predictable exit codes: 0 (success), 1 (error), 2 (usage error)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## FAQ

### How do I install cli-anything-zoom?

```bash
pip install cli-anything-zoom
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/zoom/).

### How do I check if the software is available?

```bash
cli-anything-zoom detect --json
```

Returns a JSON object with installation status and version information.
