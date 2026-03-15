<div align="center">

```
  ██████╗██╗     ██╗      █████╗ ███╗   ██╗██╗   ██╗████████╗██╗  ██╗██╗███╗   ██╗ ██████╗
 ██╔════╝██║     ██║     ██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║  ██║██║████╗  ██║██╔════╝
 ██║     ██║     ██║     ███████║██╔██╗ ██║ ╚████╔╝    ██║   ███████║██║██╔██╗ ██║██║  ███╗
 ██║     ██║     ██║     ██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██╔══██║██║██║╚██╗██║██║   ██║
 ╚██████╗███████╗██║     ██║  ██║██║ ╚████║   ██║      ██║   ██║  ██║██║██║ ╚████║╚██████╔╝
  ╚═════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝
                                          H  U  B
```

**The Open Hub for 100+ Agent-Ready CLIs**

*pip install any tool. Agents call any software. Zero friction.*

[![Hub CLIs](https://img.shields.io/badge/Hub_CLIs-30%2B_Ready-00ff41?style=for-the-badge&logo=python&logoColor=white)](https://github.com/chatjesus/CLI-Anything-Hub)
[![pip install](https://img.shields.io/badge/pip_install-cli--anything--*-blue?style=for-the-badge&logo=pypi&logoColor=white)](https://github.com/chatjesus/CLI-Anything-Hub)
[![Tests](https://img.shields.io/badge/Tests-1%2C508_Passing-brightgreen?style=for-the-badge)](https://github.com/chatjesus/CLI-Anything-Hub)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Fork](https://img.shields.io/badge/Fork_%26_Extend-Welcome-orange?style=for-the-badge&logo=github)](https://github.com/chatjesus/CLI-Anything-Hub/fork)

</div>

---

## What is CLI-Anything Hub?

> **CLI-Anything Hub** is a curated, community-driven collection of **pre-built, agent-ready CLI wrappers** for the world's most popular software — covering desktop apps, cloud APIs, SaaS platforms, and more.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLI-Anything Hub Architecture                     │
│                                                                      │
│   Your AI Agent (Claude / Cursor / Codex / OpenCode)                │
│          │                                                           │
│          ▼                                                           │
│   ┌─────────────────────────────────────────────────────────┐       │
│   │              CLI-Anything Hub                           │       │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │       │
│   │  │  Slack   │ │  Stripe  │ │  Docker  │ │  GIMP    │  │       │
│   │  │   CLI    │ │   CLI    │ │   CLI    │ │   CLI    │  │       │
│   │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │       │
│   │       │            │            │            │         │       │
│   │  ┌────▼─────┐ ┌────▼─────┐ ┌────▼─────┐ ┌────▼─────┐  │       │
│   │  │  Slack   │ │  Stripe  │ │  Docker  │ │  GIMP    │  │       │
│   │  │   API    │ │   SDK    │ │ Python   │ │Script-Fu │  │       │
│   │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │       │
│   └─────────────────────────────────────────────────────────┘       │
│                                                                      │
│   One interface. 30+ tools. All agent-native. All JSON output.      │
└─────────────────────────────────────────────────────────────────────┘
```

**Two ways to use the Hub:**

| Mode | What it does | When to use |
|------|-------------|-------------|
| 📦 **Install Pre-built** | `pip install` any of the 30+ ready CLIs | Slack, Stripe, Docker, GIMP, etc. |
| 🔨 **Generate New** | Use `/cli-anything` plugin to build a CLI for any codebase | Your own software, niche tools |

---

## ⚡ 30-Second Quick Start

```bash
# 1. Pick any tool from the Hub catalog
pip install -e ./slack-cli        # or stripe, docker, notion, etc.

# 2. Set credentials
export SLACK_BOT_TOKEN=xoxb-...

# 3. Agent calls it directly
cli-anything-slack --json message send \#general "Hello from Agent"

# 4. Discover all capabilities (no auth needed)
cli-anything-slack schema
```

---

## 📦 Hub Catalog — 30+ Pre-built CLIs

> All CLIs follow the same interface: `--json` flag, `schema` command, `detect` command.

### 🎨 Creative & Media

```bash
pip install -e ./gimp          # cli-anything-gimp        · Image editing (107 tests)
pip install -e ./blender       # cli-anything-blender     · 3D rendering  (208 tests)
pip install -e ./inkscape      # cli-anything-inkscape    · Vector SVG    (202 tests)
pip install -e ./audacity      # cli-anything-audacity    · Audio editing (161 tests)
pip install -e ./kdenlive      # cli-anything-kdenlive    · Video editing (155 tests)
pip install -e ./shotcut       # cli-anything-shotcut     · Video editing (154 tests)
pip install -e ./obs-studio    # cli-anything-obs-studio  · Streaming     (153 tests)
pip install -e ./drawio        # cli-anything-drawio      · Diagrams      (138 tests)
```

### 💬 Communication & Messaging

```bash
pip install -e ./slack-cli     # cli-anything-slack       · Channels, DMs, files
pip install -e ./discord-cli   # cli-anything-discord     · Bot messaging, guilds
pip install -e ./telegram-cli  # cli-anything-telegram    · Bot API, groups, channels
pip install -e ./feishu-cli    # cli-anything-feishu      · Feishu/Lark open platform
```

### ☁️ Cloud & SaaS APIs

```bash
pip install -e ./stripe-cli      # cli-anything-stripe    · Payments, subscriptions
pip install -e ./shopify-cli     # cli-anything-shopify   · Products, orders, inventory
pip install -e ./hubspot-cli     # cli-anything-hubspot   · CRM, contacts, deals
pip install -e ./salesforce-cli  # cli-anything-salesforce· SOQL, leads, opportunities
pip install -e ./jira-cli        # cli-anything-jira      · Issues, sprints, JQL
pip install -e ./vercel-cli      # cli-anything-vercel    · Deploy, domains, env vars
pip install -e ./cloudflare-cli  # cli-anything-cloudflare· DNS, Workers, R2
pip install -e ./twilio-cli      # cli-anything-twilio    · SMS, voice, WhatsApp
```

### 🛠️ Dev Tools & Automation

```bash
pip install -e ./docker-cli    # cli-anything-docker      · Containers, images, compose
pip install -e ./github-cli    # cli-anything-github      · Issues, PRs, Actions, releases
pip install -e ./notion-cli    # cli-anything-notion      · Pages, databases, blocks
pip install -e ./ollama-cli    # cli-anything-ollama      · Local LLM, models, chat
```

### 📊 Office & Productivity

```bash
pip install -e ./ms365-cli     # cli-anything-ms365       · Word, Excel, Outlook via COM
pip install -e ./wps-cli       # cli-anything-wps         · WPS Office automation
pip install -e ./libreoffice   # cli-anything-libreoffice · Writer, Calc, Impress (158 tests)
pip install -e ./zoom          # cli-anything-zoom        · Meetings, recordings (22 tests)
```

### 🔑 Google Workspace (Suite)

```bash
pip install -e ./gworkspace-cli  # One package — 6 services:
                                 #   cli-anything-gworkspace drive   · Drive API v3
                                 #   cli-anything-gworkspace gmail   · Gmail API v1
                                 #   cli-anything-gworkspace calendar· Calendar API v3
                                 #   cli-anything-gworkspace sheets  · Sheets API v4
                                 #   cli-anything-gworkspace docs    · Docs API v1
                                 #   cli-anything-gworkspace chat    · Chat API v1
```

### ✨ AI Content Generation

```bash
pip install -e ./anygen        # cli-anything-anygen      · AI slides, docs, diagrams (50 tests)
```

---

## 🤖 Agent-Native Design — The Hub Standard

Every CLI in this Hub implements the **same 4-command interface** so agents can use any tool without reading docs:

```bash
# 1. DISCOVER capabilities (no token/auth needed)
cli-anything-slack schema
# → JSON: all commands, args, required env vars, examples

# 2. CHECK connectivity
cli-anything-slack detect
# → JSON: {"status": "ok", "workspace": "MyTeam", "bot": "AgentBot"}

# 3. CALL with structured output
cli-anything-slack --json message send \#ops "Deploy started"
# → JSON: {"ok": true, "ts": "1742000000.000100", "channel": "C123"}

# 4. DISCOVER installed tools (agent self-discovery)
which cli-anything-slack   # standard PATH lookup
```

### Schema Command — Agent Self-Discovery

```json
$ cli-anything-stripe schema
{
  "name": "cli-anything-stripe",
  "version": "1.0.0",
  "requires_token": true,
  "token_env": "STRIPE_SECRET_KEY",
  "token_hint": "sk-... from https://dashboard.stripe.com/apikeys",
  "commands": [
    {"cmd": "customers list",   "args": ["--limit INT"],       "desc": "List customers"},
    {"cmd": "payment create",   "args": ["--amount", "--currency", "--customer"], "desc": "Create payment"},
    {"cmd": "subscriptions cancel", "args": ["SUB_ID"],        "desc": "Cancel subscription"}
  ],
  "json_flag": "--json",
  "example": "cli-anything-stripe --json customers list --limit 5"
}
```

---

## 📁 Repository Structure

```
CLI-Anything-Hub/
│
├── 📋 BATCH_PLAN.md              ← Roadmap: 100+ CLIs planned
├── 📋 LOCAL_CLI_CANDIDATES.md    ← Local/offline service CLIs queue
│
├── ─── Pre-built Hub CLIs ───────────────────────────────────────────
│
├── 💬  slack-cli/                ← cli-anything-slack
├── 💬  discord-cli/              ← cli-anything-discord
├── 💬  telegram-cli/             ← cli-anything-telegram
├── 💬  feishu-cli/               ← cli-anything-feishu
│
├── 💳  stripe-cli/               ← cli-anything-stripe
├── 🛒  shopify-cli/              ← cli-anything-shopify
├── 🏢  salesforce-cli/           ← cli-anything-salesforce
├── 📞  twilio-cli/               ← cli-anything-twilio
├── 📊  hubspot-cli/              ← cli-anything-hubspot
├── 🎯  jira-cli/                 ← cli-anything-jira
├── 🚀  vercel-cli/               ← cli-anything-vercel
├── 🌐  cloudflare-cli/           ← cli-anything-cloudflare
│
├── 🐳  docker-cli/               ← cli-anything-docker
├── 🐙  github-cli/               ← cli-anything-github
├── 📝  notion-cli/               ← cli-anything-notion
├── 🦙  ollama-cli/               ← cli-anything-ollama
├── 🏢  ms365-cli/                ← cli-anything-ms365
├── 📄  wps-cli/                  ← cli-anything-wps
│
├── 🌐  gworkspace-cli/           ← cli-anything-gworkspace (Drive+Gmail+Cal+Sheets+Docs+Chat)
│
├── ─── Original Agent-Harness CLIs (from upstream, 1,508 tests) ────
│
├── 🎨  gimp/agent-harness/       ← cli-anything-gimp      (107 tests)
├── 🧊  blender/agent-harness/    ← cli-anything-blender   (208 tests)
├── ✏️   inkscape/agent-harness/   ← cli-anything-inkscape  (202 tests)
├── 🎵  audacity/agent-harness/   ← cli-anything-audacity  (161 tests)
├── 📄  libreoffice/agent-harness/← cli-anything-libreoffice(158 tests)
├── 📹  obs-studio/agent-harness/ ← cli-anything-obs-studio(153 tests)
├── 🎞️   kdenlive/agent-harness/   ← cli-anything-kdenlive  (155 tests)
├── 🎬  shotcut/agent-harness/    ← cli-anything-shotcut   (154 tests)
├── 📞  zoom/agent-harness/       ← cli-anything-zoom      (22 tests)
├── 📐  drawio/agent-harness/     ← cli-anything-drawio    (138 tests)
└── ✨  anygen/agent-harness/     ← cli-anything-anygen    (50 tests)
```

---

## 🔨 Build Your Own CLI (Generate Mode)

Don't see your tool in the Hub? Use the **CLI-Anything plugin** to generate a new harness in one command:

### With Claude Code

```bash
# Step 1: Add the Hub as plugin marketplace
/plugin marketplace add chatjesus/CLI-Anything-Hub

# Step 2: Install the plugin
/plugin install cli-anything

# Step 3: Generate a CLI for any software
/cli-anything:cli-anything ./my-software
/cli-anything:cli-anything https://github.com/user/repo
```

The generator runs a 7-phase pipeline:

```
1. Analyze    → Scan source code, map APIs and capabilities
2. Design     → Architect command groups + state model
3. Implement  → Build Click CLI with REPL + JSON output
4. Plan Tests → Create TEST.md with unit + E2E plans
5. Write Tests→ Implement comprehensive test suite
6. Document   → Update TEST.md with results
7. Publish    → Create setup.py, install to PATH
```

### With OpenCode / Codex

```bash
# OpenCode
cp CLI-Anything-Hub/opencode-commands/*.md ~/.config/opencode/commands/
/cli-anything ./my-software

# Codex
bash CLI-Anything-Hub/codex-skill/scripts/install.sh
# then: "Use CLI-Anything to build a harness for ./my-software"
```

---

## 🚀 Fork the Hub — Contribute Your CLI

```
                ┌─────────────────────────────┐
                │  chatjesus/CLI-Anything-Hub  │
                │                             │
                │  30+ CLIs  ·  MIT License   │
                │                             │
                └──────────┬──────────────────┘
                           │  Fork
                    ┌──────▼──────────┐
                    │  your-username/ │
                    │  CLI-Anything-Hub│
                    └──────┬──────────┘
                           │  Add your CLI
                    ┌──────▼──────────┐
                    │  my-tool-cli/   │
                    │  my_tool_cli.py │ ← click + --json + schema
                    │  setup.py       │ ← pip installable
                    │  README.md      │ ← quick start
                    └──────┬──────────┘
                           │  Pull Request
                    ┌──────▼──────────┐
                    │   Hub grows!    │
                    └─────────────────┘
```

### CLI Standard — What Every Hub CLI Must Have

```python
# Every Hub CLI implements these 4 commands:

@cli.command()
def detect():
    """Check connectivity without side effects."""
    # Returns: {"status": "ok", "version": "...", ...}

@cli.command()
def schema():
    """Output full capability schema (no auth needed)."""
    # Returns: {name, commands[], token_env, examples}

@cli.command()
def version():
    """Print version info."""

# All commands support --json flag for structured output
```

### Submit a PR

```bash
# 1. Fork this repo
# 2. Add your CLI under my-tool-cli/
# 3. Implement: detect, schema, version + core commands
# 4. Add --json flag support
# 5. Add setup.py with entry_point = "cli-anything-mytool"
# 6. Open a Pull Request
```

---

## 📊 Hub Stats

| Category | CLIs Ready | CLIs Planned |
|----------|-----------|-------------|
| Creative & Media | 8 | + DaVinci, Premiere, Photoshop, FFmpeg |
| Communication | 4 | + Teams, WhatsApp |
| Cloud SaaS | 8 | + PayPal, Square, Google Ads, LinkedIn |
| Dev Tools | 4 | + GitLab, VS Code, Chrome CDP |
| Office | 4 | + Google Docs, Slides |
| Google Workspace | 6 (1 pkg) | — |
| Gaming & Entertainment | 0 | 13 planned (Steam, Riot, Roblox...) |
| Life & Local Services | 0 | 9 planned (DoorDash, Meituan, Uber...) |
| **Total** | **30+** | **100+ target** |

---

## 🗺️ Roadmap

- [x] Core Hub CLIs: Slack, Discord, Telegram, Stripe, Shopify, HubSpot, Jira, Vercel, Cloudflare, Salesforce, Docker, GitHub, Notion, Ollama, MS365, Feishu, WPS, Google Workspace
- [x] Agent-native standard: `schema` + `detect` + `--json` on every CLI
- [ ] **Gaming CLIs**: Steam, Epic, Roblox, Riot Games, Battle.net, Minecraft RCON, Twitch
- [ ] **Life & Local Services**: DoorDash, Meituan, Uber Eats, Grab, Airbnb, Yelp
- [ ] **Advertising APIs**: Google Ads, TikTok Ads, Meta Ads
- [ ] **Creative SaaS**: Figma, Canva, Adobe (UXP)
- [ ] PyPI releases for all Hub CLIs (`pip install cli-anything-slack`)
- [ ] Auto-generated `SKILL.md` per CLI for agent skill discovery
- [ ] CLI-Anything Hub website: [agentputer.com/cli-anything](https://www.agentputer.com/cli-anything)

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [`BATCH_PLAN.md`](BATCH_PLAN.md) | Full roadmap — all 100+ planned CLIs with API details |
| [`LOCAL_CLI_CANDIDATES.md`](LOCAL_CLI_CANDIDATES.md) | Local/offline service CLI candidates |
| [`cli-anything-plugin/HARNESS.md`](cli-anything-plugin/HARNESS.md) | Methodology SOP for generating new CLIs |
| [`cli-anything-plugin/PUBLISHING.md`](cli-anything-plugin/PUBLISHING.md) | PyPI distribution guide |

---

## 📄 License

MIT License — free to use, modify, and distribute.

This repository is a community fork and extension of [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything), with significant additions and a Hub-first approach.

---

<div align="center">

**CLI-Anything Hub** — *The open hub for 100+ agent-ready CLIs.*

`pip install` any tool · Agents call any software · Fork and extend

[![Star this repo](https://img.shields.io/github/stars/chatjesus/CLI-Anything-Hub?style=social)](https://github.com/chatjesus/CLI-Anything-Hub)
&nbsp;&nbsp;
[![Fork the Hub](https://img.shields.io/github/forks/chatjesus/CLI-Anything-Hub?style=social)](https://github.com/chatjesus/CLI-Anything-Hub/fork)

[agentputer.com/cli-anything](https://www.agentputer.com/cli-anything) · MIT License · Built with SelfEvolveAI

</div>
