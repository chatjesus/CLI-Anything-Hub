<div align="center">

```
  ██████╗██╗     ██╗      █████╗ ███╗   ██╗██╗   ██╗████████╗██╗  ██╗██╗███╗   ██╗  ██████╗
 ██╔════╝██║     ██║     ██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║  ██║██║████╗  ██║ ██╔════╝
 ██║     ██║     ██║     ███████║██╔██╗ ██║ ╚████╔╝    ██║   ███████║██║██╔██╗ ██║ ██║  ███╗
 ██║     ██║     ██║     ██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██╔══██║██║██║╚██╗██║ ██║   ██║
 ╚██████╗███████╗███████╗██║  ██║██║ ╚████║   ██║      ██║   ██║  ██║██║██║ ╚████║ ╚██████╔╝
  ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝
                                         H  U  B
```

**The Open Hub for 160+ Agent-Ready CLIs**

*pip install any tool · Agents call any software · Zero friction*

[![Product Hunt](https://img.shields.io/badge/Product%20Hunt-Launch-DA552F?style=for-the-badge&logo=producthunt&logoColor=white)](https://www.producthunt.com/posts/cli-anything)
[![Hub CLIs](https://img.shields.io/badge/Hub_CLIs-160%2B_Planned-00ff41?style=for-the-badge&logo=python&logoColor=white)](https://github.com/chatjesus/CLI-Anything-Hub)
[![Live CLIs](https://img.shields.io/badge/Live_CLIs-35%2B_Ready-brightgreen?style=for-the-badge&logo=python)](https://github.com/chatjesus/CLI-Anything-Hub)
[![PyPI](https://img.shields.io/badge/PyPI-cli--anything--*-blue?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/search/?q=cli-anything)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Fork](https://img.shields.io/badge/Fork_%26_Extend-Welcome-orange?style=for-the-badge&logo=github)](https://github.com/chatjesus/CLI-Anything-Hub/fork)

**[Website](https://agentputer.com/cli-anything/)** · **[Product Hunt](https://www.producthunt.com/posts/cli-anything)** · **[Submit Your CLI](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool)** · **[Fork the Hub](https://github.com/chatjesus/CLI-Anything-Hub/fork)**

</div>

---

## What is CLI-Anything Hub?

> **CLI-Anything Hub** is a curated, community-driven collection of **pre-built, agent-ready CLI wrappers** for the world's most popular software — covering desktop apps, cloud APIs, SaaS platforms, gaming, local services, and more.

Every CLI in this Hub implements the same 4-command interface so **AI agents (Claude, Cursor, Codex, OpenCode) can call any software without reading docs**.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     CLI-Anything Hub Architecture                        │
│                                                                          │
│   Your AI Agent (Claude / Cursor / Codex / OpenCode / any LLM)          │
│          │                                                               │
│          ▼   cli-anything-slack schema  →  JSON capability map          │
│   ┌──────────────────────────────────────────────────────────────┐       │
│   │                    CLI-Anything Hub                          │       │
│   │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │       │
│   │  │ Slack  │ │ Stripe │ │ Docker │ │  GIMP  │ │ Steam  │    │       │
│   │  │  CLI   │ │  CLI   │ │  CLI   │ │  CLI   │ │  CLI   │    │       │
│   │  └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘    │       │
│   │      │          │          │          │          │          │       │
│   │   Slack API  Stripe SDK  Docker SDK  Script-Fu  Steam API   │       │
│   └──────────────────────────────────────────────────────────────┘       │
│                                                                          │
│   One interface. 160+ tools. All agent-native. All JSON output.         │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ 30-Second Quick Start

```bash
# 1. Pick any live CLI from the catalog below
pip install -e ./slack-cli       # Communication
pip install -e ./stripe-cli      # Payments
pip install -e ./docker-cli      # Dev Tools
pip install -e ./gworkspace-cli  # Google Workspace

# 2. Set credentials
export SLACK_BOT_TOKEN=xoxb-...

# 3. Agent calls it — JSON output, zero friction
cli-anything-slack --json message send \#general "Hello from Agent"

# 4. Agent self-discovers capabilities (no auth needed)
cli-anything-slack schema
```

---

## 📦 Complete CLI Catalog

> ✅ = Live & installable · 🔜 = Coming soon (submit a PR to accelerate!)

### 🎨 Creative & Media

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| GIMP | `cli-anything-gimp` | ✅ Live | Image editing, filters, batch processing (107 tests) |
| Blender | `cli-anything-blender` | ✅ Live | 3D rendering, scene management, Python scripting (208 tests) |
| Inkscape | `cli-anything-inkscape` | ✅ Live | Vector SVG editing, export, element manipulation (202 tests) |
| Audacity | `cli-anything-audacity` | ✅ Live | Audio editing, effects, format conversion (161 tests) |
| Kdenlive | `cli-anything-kdenlive` | ✅ Live | Video editing, timeline, MLT framework (155 tests) |
| Shotcut | `cli-anything-shotcut` | ✅ Live | Video editing, export, filters (154 tests) |
| OBS Studio | `cli-anything-obs-studio` | ✅ Live | Streaming, recording, scene switching (153 tests) |
| Draw.io | `cli-anything-drawio` | ✅ Live | Diagrams, flowcharts, export (138 tests) |
| AnyGen | `cli-anything-anygen` | ✅ Live | AI slides, docs, diagrams generation (50 tests) |
| DaVinci Resolve | `cli-anything-davinci` | 🔜 Soon | MCP server (295+ tools), Python scripting, color grading, rendering |
| Premiere Pro | `cli-anything-premiere` | 🔜 Soon | Adobe UXP sequence automation |
| FFmpeg / CutAgent | `cli-anything-ffmpeg` | 🔜 Soon | Agent-first video editing, EDL JSON format, scene/silence detection |
| VLC | `cli-anything-vlc` | 🔜 Soon | HTTP REST API — playback, playlist, volume, fullscreen control |
| ComfyUI | `cli-anything-comfyui` | 🔜 Soon | AI workflow agent (Claude Vision), 31K+ node search, natural language |
| 7-Zip | `cli-anything-7zip` | 🔜 Soon | 30+ archive formats, cross-platform, SFX self-extracting |

### 🎨 Design & Creativity

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Figma | `cli-anything-figma` | 🔜 Soon | Full read/write Figma Desktop control, shadcn/ui generation, design tokens |
| Canva | `cli-anything-canva` | 🔜 Soon | Connect API — populate templates, brand kits |
| Photoshop | `cli-anything-photoshop` | 🔜 Soon | Adobe API — batch image processing, background removal, layer automation |
| Illustrator | `cli-anything-illustrator` | 🔜 Soon | UXP — vector automation, artboard export |
| Krita | `cli-anything-krita` | 🔜 Soon | Scripting API — batch paint, digital art export |

### 💬 Communication & Messaging

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Slack | `cli-anything-slack` | ✅ Live | Channels, DMs, files, webhooks |
| Discord | `cli-anything-discord` | ✅ Live | Bot messaging, guilds, threads |
| Telegram | `cli-anything-telegram` | ✅ Live | Bot API, groups, channels, media |
| Feishu / Lark | `cli-anything-feishu` | ✅ Live | Feishu/Lark open platform — messages, docs |
| Resend | `cli-anything-resend` | 🔜 Soon | Email API — 53 commands, domains, templates, broadcasts |
| WhatsApp | `cli-anything-whatsapp` | 🔜 Soon | wacli (personal) + Cloud API (business) — messages, files, groups |
| Microsoft Teams | `cli-anything-teams` | 🔜 Soon | Graph API — channels, meetings, notifications |
| X / Twitter | `cli-anything-x` | 🔜 Soon | API v2 — tweets, timeline, DMs, analytics |
| Postiz (Multi-Platform) | `cli-anything-postiz` | 🔜 Soon | 30+ social platforms — TikTok, IG, YouTube, Twitch, Spotify |
| Post Bridge | `cli-anything-postbridge` | 🔜 Soon | 9 platforms — IG, TikTok, YouTube, X, LinkedIn, Facebook |

### ☁️ Cloud SaaS & APIs

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Stripe | `cli-anything-stripe` | ✅ Live | Payments, subscriptions, customers, webhooks |
| Shopify | `cli-anything-shopify` | ✅ Live | Products, orders, inventory, customers |
| HubSpot | `cli-anything-hubspot` | ✅ Live | CRM, contacts, deals, pipelines |
| Salesforce | `cli-anything-salesforce` | ✅ Live | SOQL, leads, opportunities, cases |
| Jira | `cli-anything-jira` | ✅ Live | Issues, sprints, JQL queries, projects |
| Vercel | `cli-anything-vercel` | ✅ Live | Deploy, domains, env vars, deployments |
| Cloudflare | `cli-anything-cloudflare` | ✅ Live | DNS, Workers, R2, KV, Pages |
| Twilio | `cli-anything-twilio` | ✅ Live | SMS, voice calls, WhatsApp messaging |
| SendGrid | `cli-anything-sendgrid` | 🔜 Soon | Transactional email, templates, contacts |
| Mailchimp | `cli-anything-mailchimp` | 🔜 Soon | Email campaigns, audiences, automation |
| Zendesk | `cli-anything-zendesk` | 🔜 Soon | Support tickets, users, macros |
| Dropbox | `cli-anything-dropbox` | 🔜 Soon | File storage, sharing, sync |
| Cal.com | `cli-anything-calcom` | 🔜 Soon | Scheduling, availability, bookings, MCP server |
| n8n | `cli-anything-n8n` | 🔜 Soon | Workflow automation — workflows, executions, credentials |

### 🛠️ Dev Tools & Automation

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Docker | `cli-anything-docker` | ✅ Live | Containers, images, compose, networks |
| GitHub | `cli-anything-github` | ✅ Live | Issues, PRs, Actions, releases, repos |
| Notion | `cli-anything-notion` | ✅ Live | Pages, databases, blocks, comments |
| Ollama | `cli-anything-ollama` | ✅ Live | Local LLM, models, chat, embeddings |
| Sentry | `cli-anything-sentry` | 🔜 Soon | AI error analysis "Seer", natural language commands, JSON output |
| Datadog | `cli-anything-datadog` | 🔜 Soon | 200+ commands, 33 products — monitors, logs, metrics, security |
| Grafana | `cli-anything-grafana` | 🔜 Soon | A2A API, dashboards, alerts, assistant CLI |
| PostHog | `cli-anything-posthog` | 🔜 Soon | Auto-instrumentation, analytics, 15+ framework support |
| AWS | `cli-anything-aws` | 🔜 Soon | S3, Lambda, EC2, DynamoDB, CloudFormation |
| GitLab | `cli-anything-gitlab` | 🔜 Soon | Repos, MRs, pipelines, CI/CD |
| VS Code | `cli-anything-vscode` | 🔜 Soon | Extensions, workspace, tasks, debugging |
| JetBrains | `cli-anything-jetbrains` | 🔜 Soon | IDE inspections, refactoring, builds |
| Browser / Playwright | `cli-anything-browser` | 🔜 Soon | Web automation, screenshot, form fill |
| Obsidian | `cli-anything-obsidian` | 🔜 Soon | CLI REST + MCP server — vault search, notes, tags, tasks, templates, daily notes |

### 📊 Office & Productivity

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| MS 365 | `cli-anything-ms365` | ✅ Live | Word, Excel, Outlook automation via COM |
| WPS Office | `cli-anything-wps` | ✅ Live | WPS Writer, Spreadsheet, Presentation |
| LibreOffice | `cli-anything-libreoffice` | ✅ Live | Writer, Calc, Impress (158 tests) |
| Zoom | `cli-anything-zoom` | ✅ Live | Meetings, recordings, participants (22 tests) |
| OneDrive | `cli-anything-onedrive` | 🔜 Soon | File upload, download, share via Graph |
| Todoist | `cli-anything-todoist` | 🔜 Soon | Tasks, projects, labels, comments, sync API |
| Raindrop.io | `cli-anything-raindrop` | 🔜 Soon | Bookmarks, collections, tags, highlights |

### 🔑 Google Workspace (Suite)

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Google Drive | `cli-anything-gworkspace drive` | ✅ Live | Drive API v3 — upload, share, search |
| Gmail | `cli-anything-gworkspace gmail` | ✅ Live | Gmail API v1 — send, search, labels |
| Calendar | `cli-anything-gworkspace calendar` | ✅ Live | Calendar API v3 — events, attendees |
| Sheets | `cli-anything-gworkspace sheets` | ✅ Live | Sheets API v4 — read, write, format |
| Docs | `cli-anything-gworkspace docs` | ✅ Live | Docs API v1 — create, edit, export |
| Chat | `cli-anything-gworkspace chat` | ✅ Live | Chat API v1 — spaces, messages |
| Google Drive (standalone) | `cli-anything-gdrive` | 🔜 Soon | Standalone Drive wrapper |

```bash
# All 6 Google Workspace services in one package
pip install -e ./gworkspace-cli
cli-anything-gworkspace drive list-files
cli-anything-gworkspace gmail send --to user@example.com --subject "Hello" --body "From agent"
cli-anything-gworkspace calendar list-events --max-results 10
```

### 📣 Advertising & Marketing APIs

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Google Ads | `cli-anything-gads` | 🔜 Soon | Campaign management, bidding, reporting |
| Google Play | `cli-anything-gplay` | 🔜 Soon | App management, reviews, sales data |
| TikTok Ads | `cli-anything-tiktok` | 🔜 Soon | Campaigns, creatives, audiences, analytics |
| Meta Ads | `cli-anything-meta-ads` | 🔜 Soon | Facebook/Instagram ads — campaigns, audiences, insights |
| Apple Search Ads | `cli-anything-apple-ads` | 🔜 Soon | App Store campaigns, keywords, reporting |
| SensorTower | `cli-anything-sensortower` | 🔜 Soon | App intelligence, rankings, downloads, revenue estimates |

### 📋 Project Management

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Linear | `cli-anything-linear` | 🔜 Soon | Issues, projects, cycles, teams — JSON output, shell completion |
| ClickUp | `cli-anything-clickup` | 🔜 Soon | 99.3% API coverage (134/135 endpoints), JSON-first, Docs API |
| Asana | `cli-anything-asana` | 🔜 Soon | Tasks, projects, workspaces, relationship management |
| Airtable | `cli-anything-airtable` | 🔜 Soon | Bases, tables, records, comments, webhooks — fuzzy search |
| Monday.com | `cli-anything-monday` | 🔜 Soon | Boards, items, updates, automations via GraphQL |

### 🗄️ Database & Infrastructure

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Supabase | `cli-anything-supabase` | 🔜 Soon | PostgreSQL, Auth, Edge Functions, real-time, migrations |
| Neon | `cli-anything-neon` | 🔜 Soon | Serverless Postgres — branches, roles, connection strings |
| PlanetScale | `cli-anything-planetscale` | 🔜 Soon | MySQL branching, deploy requests, schema management |
| Turso | `cli-anything-turso` | 🔜 Soon | Edge SQLite (libSQL), global replication, groups |
| Upstash | `cli-anything-upstash` | 🔜 Soon | Serverless Redis + Kafka — create, manage, CRUD |
| Weaviate | `cli-anything-weaviate` | 🔜 Soon | Vector DB — collections, multi-tenancy, backup/restore |
| Qdrant | `cli-anything-qdrant` | 🔜 Soon | Vector DB — collections, points, snapshots, clusters |
| Redis | `cli-anything-redis` | 🔜 Soon | In-memory data store — keys, streams, pub/sub |

### 🚀 Deployment & Hosting

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Netlify | `cli-anything-netlify` | 🔜 Soon | Deploy from agents, projects, env vars, MCP server |
| Render | `cli-anything-render` | 🔜 Soon | Services, datastores, deploys, logs, agent skill support |
| Fly.io | `cli-anything-flyio` | 🔜 Soon | Global edge deploy, Machines API, volumes, secrets |
| Railway | `cli-anything-railway` | 🔜 Soon | One-click deploy, environments, variables, databases |
| Heroku | `cli-anything-heroku` | 🔜 Soon | Apps, dynos, add-ons, config vars, logs |
| DigitalOcean | `cli-anything-digitalocean` | 🔜 Soon | Droplets, App Platform, databases, Kubernetes |

### 🤖 AI & LLM Platforms

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| OpenAI | `cli-anything-openai` | 🔜 Soon | Chat, embeddings, image gen, fine-tuning, assistants |
| Hugging Face | `cli-anything-huggingface` | 🔜 Soon | Models, datasets, Spaces, inference endpoints |
| Replicate | `cli-anything-replicate` | 🔜 Soon | Model inference, training, deployments, collections |
| Groq | `cli-anything-groq` | 🔜 Soon | Ultra-fast inference, LLM chat, audio transcription |
| Together AI | `cli-anything-together` | 🔜 Soon | Open-source model inference, fine-tuning, embeddings |
| Anthropic | `cli-anything-anthropic` | 🔜 Soon | Claude API — messages, tool use, batch processing |

### 🎮 Gaming & Entertainment

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| Steam | `cli-anything-steam` | 🔜 Soon | Web API v2 — library, achievements, friends, game stats, steamctl |
| Epic Games | `cli-anything-epic` | 🔜 Soon | Store, free games, library, launcher |
| GOG Galaxy | `cli-anything-gog` | 🔜 Soon | DRM-free library, achievements, sync |
| Battle.net | `cli-anything-battlenet` | 🔜 Soon | WoW, D4, OW2 — character profiles, OAuth |
| Roblox | `cli-anything-roblox` | 🔜 Soon | Open Cloud API — game data, virtual economy |
| Riot Games | `cli-anything-riot` | 🔜 Soon | League, Valorant, TFT player stats |
| Minecraft RCON | `cli-anything-minecraft` | 🔜 Soon | Server RCON — commands, players, worlds |
| Fortnite | `cli-anything-fortnite` | 🔜 Soon | Player stats, shop, season data |
| HoYoverse | `cli-anything-hoyoverse` | 🔜 Soon | Genshin/HSR/ZZZ daily check-in, character data |
| CS2 / CSGO | `cli-anything-cs2` | 🔜 Soon | Player stats, match history, inventory |
| Xbox / Game Pass | `cli-anything-xbox` | 🔜 Soon | Xbox Live API — library, achievements, Game Pass |
| Speedrun.com | `cli-anything-speedrun` | 🔜 Soon | Leaderboards, world records, categories |
| Lichess | `cli-anything-lichess` | 🔜 Soon | Play, analyze, tournaments, user stats |
| Chess.com | `cli-anything-chess` | 🔜 Soon | Player stats, game history, puzzles |
| Twitch | `cli-anything-twitch` | 🔜 Soon | Official CLI + Helix API — streams, clips, subscriptions, webhooks |
| Spotify | `cli-anything-spotify` | 🔜 Soon | Rust/Go CLI — playback, playlists, search, queue, JSON output |
| YouTube | `cli-anything-youtube` | 🔜 Soon | Data API v3 CLI — upload, search, playlists, analytics, JSON/YAML/CSV |
| Valheim | `cli-anything-valheim` | 🔜 Soon | Server control, players, world saves |

### 🍔 Life & Local Services

| CLI | Package | Status | Description |
|-----|---------|--------|-------------|
| McDonald's | `cli-anything-mcdonalds` | 🔜 Soon | Store locator, menu lookup, nutritional data |
| KFC | `cli-anything-kfc` | 🔜 Soon | Nearest locations, menu, delivery availability |
| Meituan | `cli-anything-meituan` | 🔜 Soon | Food delivery, hotel, entertainment (China) |
| Ele.me | `cli-anything-eleme` | 🔜 Soon | Order tracking, restaurant search (Alibaba) |
| DoorDash | `cli-anything-doordash` | 🔜 Soon | Drive API — delivery quotes, order tracking |
| Uber Eats | `cli-anything-ubereats` | 🔜 Soon | Restaurant catalog, delivery estimates |
| Grab | `cli-anything-grab` | 🔜 Soon | GrabFood, GrabCar, GrabPay (SEA) |
| DiDi | `cli-anything-didi` | 🔜 Soon | Ride estimates, booking, tracking (China/LATAM) |
| Airbnb | `cli-anything-airbnb` | 🔜 Soon | Listing search, availability, pricing |
| Booking.com | `cli-anything-booking` | 🔜 Soon | Hotel search, availability, reservations |
| Yelp | `cli-anything-yelp` | 🔜 Soon | Fusion API — business search, reviews |

---

## 🤖 Agent-Native Standard

Every CLI in this Hub implements the **same 4-command interface**:

```bash
# 1. DISCOVER — No auth needed. Agent calls this first.
cli-anything-slack schema
# → {"name":"cli-anything-slack","commands":[...],"token_env":"SLACK_BOT_TOKEN",...}

# 2. CHECK — Connectivity test, no side effects
cli-anything-slack detect
# → {"status":"ok","workspace":"MyTeam","bot":"AgentBot"}

# 3. CALL — Structured JSON output
cli-anything-slack --json message send \#ops "Deploy started"
# → {"ok":true,"ts":"1742000000.000100","channel":"C123"}

# 4. VERSION — Compatibility tracking
cli-anything-slack version
# → cli-anything-slack 1.0.0
```

### Schema Example

```json
{
  "name": "cli-anything-stripe",
  "version": "1.0.0",
  "requires_token": true,
  "token_env": "STRIPE_SECRET_KEY",
  "token_hint": "sk-... from https://dashboard.stripe.com/apikeys",
  "commands": [
    {"cmd": "customers list",    "args": ["--limit INT"],                          "desc": "List customers"},
    {"cmd": "payment create",    "args": ["--amount", "--currency", "--customer"], "desc": "Create payment"},
    {"cmd": "subscriptions list","args": ["--customer"],                           "desc": "List subscriptions"}
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
├── 📋 README.md                   ← This file
├── 📋 BATCH_PLAN.md               ← Full 130+ CLI roadmap with API details
├── 📋 LOCAL_CLI_CANDIDATES.md     ← Local/offline service CLI candidates
│
├── ─── ✅ Live Hub CLIs ──────────────────────────────────────────────────
│
├── 💬  slack-cli/                 ← cli-anything-slack
├── 💬  discord-cli/               ← cli-anything-discord
├── 💬  telegram-cli/              ← cli-anything-telegram
├── 💬  feishu-cli/                ← cli-anything-feishu
│
├── 💳  stripe-cli/                ← cli-anything-stripe
├── 🛒  shopify-cli/               ← cli-anything-shopify
├── 🏢  salesforce-cli/            ← cli-anything-salesforce
├── 📞  twilio-cli/                ← cli-anything-twilio
├── 📊  hubspot-cli/               ← cli-anything-hubspot
├── 🎯  jira-cli/                  ← cli-anything-jira
├── 🚀  vercel-cli/                ← cli-anything-vercel
├── 🌐  cloudflare-cli/            ← cli-anything-cloudflare
│
├── 🐳  docker-cli/                ← cli-anything-docker
├── 🐙  github-cli/                ← cli-anything-github
├── 📝  notion-cli/                ← cli-anything-notion
├── 🦙  ollama-cli/                ← cli-anything-ollama
├── 🏢  ms365-cli/                 ← cli-anything-ms365
├── 📄  wps-cli/                   ← cli-anything-wps
│
├── 🌐  gworkspace-cli/            ← cli-anything-gworkspace (Drive+Gmail+Cal+Sheets+Docs+Chat)
│
├── ─── ✅ Original Agent-Harness CLIs (1,508 tests) ──────────────────────
│
├── 🎨  gimp/agent-harness/        ← cli-anything-gimp       (107 tests)
├── 🧊  blender/agent-harness/     ← cli-anything-blender    (208 tests)
├── ✏️   inkscape/agent-harness/    ← cli-anything-inkscape   (202 tests)
├── 🎵  audacity/agent-harness/    ← cli-anything-audacity   (161 tests)
├── 📄  libreoffice/agent-harness/ ← cli-anything-libreoffice(158 tests)
├── 📹  obs-studio/agent-harness/  ← cli-anything-obs-studio (153 tests)
├── 🎞️   kdenlive/agent-harness/    ← cli-anything-kdenlive   (155 tests)
├── 🎬  shotcut/agent-harness/     ← cli-anything-shotcut    (154 tests)
├── 📞  zoom/agent-harness/        ← cli-anything-zoom       (22 tests)
├── 📐  drawio/agent-harness/      ← cli-anything-drawio     (138 tests)
└── ✨  anygen/agent-harness/      ← cli-anything-anygen     (50 tests)
```

---

## 🚀 Fork the Hub — Submit Your CLI

```
         ┌──────────────────────────────┐
         │  chatjesus/CLI-Anything-Hub  │
         │  160+ CLIs · MIT License     │
         └──────────────┬───────────────┘
                        │  Fork
               ┌────────▼─────────┐
               │  your-username/  │
               │  CLI-Anything-Hub│
               └────────┬─────────┘
                        │  Add: my-tool-cli/
               ┌────────▼─────────┐
               │  my_tool_cli.py  │  ← click + --json + schema
               │  setup.py        │  ← pip entry_point
               │  README.md       │  ← quick start docs
               └────────┬─────────┘
                        │  Pull Request
               ┌────────▼─────────┐
               │   Hub grows!     │
               └──────────────────┘
```

### Every Hub CLI must implement

```python
@cli.command()
def schema():
    """Output full capability JSON. No auth needed."""
    click.echo(json.dumps({
        "name": "cli-anything-mytool",
        "version": "1.0.0",
        "requires_token": True,
        "token_env": "MYTOOL_API_KEY",
        "commands": [...],
        "json_flag": "--json"
    }))

@cli.command()
def detect():
    """Check connectivity. No side effects."""
    # Returns: {"status": "ok", ...}

# All commands accept --json flag for structured output
```

**[Open a submission issue →](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool-name)**

---

## 📊 Hub Stats

| Category | Live | Planned | Total |
|----------|------|---------|-------|
| Creative & Media | 9 | 6 | 15 |
| Design & Creativity | 0 | 5 | 5 |
| Communication & Social | 4 | 8 | 12 |
| Cloud SaaS & APIs | 8 | 8 | 16 |
| Dev Tools & Monitoring | 4 | 10 | 14 |
| Office & Productivity | 4 | 3 | 7 |
| Google Workspace | 6 (1 pkg) | 1 | 7 |
| Project Management | 0 | 5 | 5 |
| Database & Infrastructure | 0 | 8 | 8 |
| Deployment & Hosting | 0 | 6 | 6 |
| AI & LLM Platforms | 0 | 6 | 6 |
| Advertising & Marketing | 0 | 6 | 6 |
| Gaming & Entertainment | 0 | 18 | 18 |
| Life & Local Services | 0 | 11 | 11 |
| **Total** | **35+** | **100+** | **135+** |

---

## 🗺️ Roadmap

- [x] Core Hub CLIs: Slack, Discord, Telegram, Stripe, Shopify, HubSpot, Jira, Vercel, Cloudflare, Salesforce, Docker, GitHub, Notion, Ollama, MS365, Feishu, WPS, Google Workspace
- [x] Agent-native standard: `schema` + `detect` + `--json` on every CLI
- [x] Landing page: agentputer.com/cli-anything — 160+ tools
- [x] SEO sub-pages for all CLIs
- [ ] **Database & Infra CLIs**: Supabase, Neon, PlanetScale, Turso, Upstash, Weaviate, Qdrant
- [ ] **Monitoring & Observability**: Sentry, Datadog, Grafana, PostHog
- [ ] **Project Management**: Linear, ClickUp, Asana, Airtable, Monday.com
- [ ] **Deployment & Hosting**: Netlify, Render, Fly.io, Railway, Heroku, DigitalOcean
- [ ] **AI & LLM Platforms**: OpenAI, Hugging Face, Replicate, Groq, Together AI, Anthropic
- [ ] **Social Media**: Postiz (30+ platforms), Post Bridge (9 platforms), Resend
- [ ] **Gaming CLIs**: Steam, Epic, Roblox, Riot, Battle.net, Minecraft RCON, Twitch
- [ ] **Life & Local**: DoorDash, Meituan, Uber Eats, Grab, Airbnb, Yelp
- [ ] **Advertising & Marketing**: Google Ads, TikTok Ads, Meta Ads, Apple Search Ads, SensorTower
- [ ] **Creative SaaS**: Figma, Canva, Adobe Photoshop/Illustrator
- [ ] PyPI releases for all Hub CLIs (`pip install cli-anything-slack`)
- [ ] Auto-generated `SKILL.md` per CLI for agent skill discovery
- [ ] Community CLI submissions via GitHub Issues

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [BATCH_PLAN.md](BATCH_PLAN.md) | Full roadmap — all 130+ planned CLIs with API details |
| [LOCAL_CLI_CANDIDATES.md](LOCAL_CLI_CANDIDATES.md) | Local/offline service CLI candidates |
| [cli-anything-plugin/HARNESS.md](cli-anything-plugin/HARNESS.md) | Methodology SOP for generating new CLIs |
| [cli-anything-plugin/PUBLISHING.md](cli-anything-plugin/PUBLISHING.md) | PyPI distribution guide |
| [agentputer.com/cli-anything](https://agentputer.com/cli-anything/) | Live website with all CLI docs |

---

## 📄 License

MIT License — free to use, modify, and distribute.

This repository is a community fork and extension of [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything), with significant additions and a Hub-first approach.

---

<div align="center">

**CLI-Anything Hub** — *The open hub for 160+ agent-ready CLIs.*

`pip install` any tool · Agents call any software · Fork and extend

[⭐ Star this repo](https://github.com/chatjesus/CLI-Anything-Hub) · [🍴 Fork the Hub](https://github.com/chatjesus/CLI-Anything-Hub/fork) · [📝 Submit Your CLI](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool)

agentputer.com/cli-anything · MIT License · Built with SelfEvolveAI

</div>
