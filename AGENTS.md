# AGENTS.md — CLI-Anything Hub

## What Is CLI-Anything?

A collection of 29+ production-ready CLI wrappers for popular desktop apps, cloud APIs, and SaaS platforms. Every tool follows the same interface: `pip install cli-anything-{name}`, supports `--json` output, and includes a `detect` command. Built specifically for AI agent consumption.

## When to Use

- User asks to automate a desktop application (GIMP, Blender, OBS, LibreOffice, MS Office)
- User needs batch file processing (images, documents, audio, video)
- User wants to send messages or manage channels (Slack, Discord, Telegram, Feishu)
- User needs to interact with a SaaS API (Stripe, Shopify, Notion, Jira, GitHub)
- User wants to manage containers or deployments (Docker, Vercel, Cloudflare)
- User wants to run a local LLM inference (Ollama)
- User needs programmatic control of software without GUI interaction

## Installation

```bash
pip install cli-anything-{software}
```

All packages are on PyPI. Python 3.9+ required.

## Quick Examples

```bash
# Image processing
cli-anything-gimp convert input.png --resize 800x600 --format webp --json

# 3D rendering
cli-anything-blender render scene.blend --output frame.png --engine CYCLES --json

# Office documents
cli-anything-ms365 word export report.docx --format pdf --json
cli-anything-libreoffice convert report.odt --format pdf --json

# Communication
cli-anything-slack message send C0ABC123 "Deploy complete" --json
cli-anything-telegram send text 123456 "Server restarted" --json
cli-anything-discord message send 987654321 "Build passed" --json

# Development
cli-anything-docker container list --all --json
cli-anything-github issue create owner/repo --title "Bug fix" --json

# SaaS
cli-anything-stripe customer list --limit 10 --json
cli-anything-notion search "meeting notes" --limit 5 --json

# AI
cli-anything-ollama run llama3.2 "Summarize this text" --json

# Streaming
cli-anything-obs-studio scene switch "Gaming Scene" --json

# Check if software is available before use
cli-anything-gimp detect --json
# Returns: {"installed": true, "version": "2.10.38"}
```

## Available Tools (29 packages)

**Image & Design:** gimp, blender, inkscape
**Video & Audio:** obs-studio, audacity, shotcut, kdenlive
**Office:** ms365, libreoffice, notion, gworkspace, feishu
**Communication:** slack, discord, telegram, zoom
**Development:** docker, github
**AI:** ollama
**SaaS:** stripe, shopify, salesforce, hubspot, jira
**Cloud:** vercel, cloudflare, twilio
**Utilities:** drawio, anygen

## Standard Commands (every CLI implements these)

| Command | Purpose |
|---------|---------|
| `detect` | Check if the software/service is available and reachable |
| `version` | Show version information |
| `schema` | Output full capability schema as JSON (some CLIs) |
| `--json` | Flag to get structured JSON output from any command |

## Output Format

All tools support `--json` for machine-readable structured output:
```json
{"status": "success", "data": {...}}
```

Exit codes follow Unix conventions:
- `0` — success
- `1` — runtime error
- `2` — usage error (bad arguments)

## Project Structure

```
CLI-Anything/
├── {name}-cli/              # Hub CLIs (18 packages)
│   ├── {name}_cli.py        # Main CLI (click framework)
│   ├── setup.py             # PyPI packaging
│   ├── README.md            # Documentation
│   └── test_{name}.py       # Tests
├── {name}/agent-harness/    # Agent-harness CLIs (11 packages)
│   ├── cli_anything/{name}/ # CLI module
│   ├── setup.py             # PyPI packaging
│   └── README.md            # Documentation
├── index.html               # Landing page
├── cli/                     # 60+ tool detail pages
├── sitemap.xml              # Search engine sitemap
├── llms.txt                 # AI engine discovery file
└── robots.txt               # Crawler directives
```

## Build & Test

```bash
# Install a specific CLI for development
cd slack-cli && pip install -e .

# Run tests
python test_slack.py

# All CLIs use click framework — run --help for full docs
cli-anything-slack --help
```

## Links

- Website: https://agentputer.com/cli-anything/
- GitHub: https://github.com/chatjesus/CLI-Anything-Hub
- PyPI: https://pypi.org/search/?q=cli-anything
