# cli-anything-notion

**Notion REST API CLI** — part of the [CLI-Anything](https://www.agentputer.com/cli-anything) engine.

Manage Notion Pages, Blocks, Databases, and Users from the command line.

## Install

```bash
pip install cli-anything-notion
# or from source:
pip install -e .
```

Requires a Notion Integration Token. Create one at [notion.so/my-integrations](https://www.notion.so/my-integrations).

## Setup

```bash
export NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxx
# or pass per command:
notion-cli --token secret_xxx detect
```

## Command Groups

| Group | Commands |
|-------|----------|
| `search` | Full-text search across pages and databases |
| `page` | get, create, update-title, archive, append-text |
| `block` | children, get, delete |
| `database` | get, query, create-page |
| `users` | list, me |

## Usage

```bash
# Check connection
notion-cli detect
notion-cli detect --json

# Search
notion-cli search "Meeting Notes" --type page
notion-cli search "Project" --limit 20 --json

# Pages
notion-cli page get <page_id>
notion-cli page create --parent-page <page_id> --title "New Page" --content "Hello"
notion-cli page append-text <page_id> "## Section Header" --type heading_2
notion-cli page append-text <page_id> "- Item one" --type bulleted_list_item
notion-cli page archive <page_id>

# Blocks
notion-cli block children <page_id>
notion-cli block get <block_id>
notion-cli block delete <block_id>

# Databases
notion-cli database get <db_id>
notion-cli database query <db_id> --limit 50
notion-cli database query <db_id> --filter-prop Status --filter-value "In Progress"
notion-cli database create-page <db_id> --title "New Task" --prop "Status=Todo"

# Users
notion-cli users list
notion-cli users me
```

## JSON Output

```bash
$ notion-cli --json search "weekly report" --type page
{
  "results": [
    {"type": "page", "id": "xxx", "title": "Weekly Report 2026-W11", "url": "..."}
  ],
  "count": 1
}
```

## Run Tests

```bash
export NOTION_TOKEN=secret_xxxx
python test_notion.py <parent_page_id>
```

---

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies software availability before use
- Predictable exit codes: 0 (success), 1 (error), 2 (usage error)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## FAQ

### How do I install cli-anything-notion?

```bash
pip install cli-anything-notion
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/notion/).

### How do I check if the software is available?

```bash
cli-anything-notion detect --json
```

Returns a JSON object with installation status and version information.
