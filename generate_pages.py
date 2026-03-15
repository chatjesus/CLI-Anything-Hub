#!/usr/bin/env python3
"""
generate_pages.py
Generates SEO-optimized sub-pages for every cli-anything tool.
Output: AgentPuter/landing/public/cli-anything/{slug}/index.html
Run:  python generate_pages.py
"""
import os
import json

OUTPUT_BASE = r"c:\Users\PRO\Desktop\CUDA\AgentPuter\landing\public\cli-anything"

# ─────────────────────────────────────────────────────────────────────────────
# CLI DATA
# ─────────────────────────────────────────────────────────────────────────────
TOOLS = [
    {
        "slug": "gimp",
        "name": "GIMP",
        "package": "cli-anything-gimp",
        "cmd": "gimp-cli",
        "category": "Image & Design",
        "icon": "https://cdn.simpleicons.org/gimp",
        "badge": "107 tests passed",
        "tagline": "Batch image processing, filters, watermarks & format conversion",
        "description": "Full programmatic control over GIMP via Python-Fu and Pillow. Batch crop, resize, apply filters, add watermarks, convert between formats — all from the command line with structured JSON output for AI agents.",
        "install": "pip install cli-anything-gimp",
        "requires": "GIMP (optional, falls back to Pillow)",
        "tags": ["Image Processing", "Batch Operations", "Pillow", "GEGL"],
        "commands": [
            ("detect", [], "Check GIMP / Pillow availability"),
            ("version", [], "Show backend versions"),
            ("info", ["IMAGE"], "Get image metadata (size, mode, EXIF)"),
            ("resize", ["IMAGE", "--width W", "--height H", "--output OUT"], "Resize image"),
            ("crop", ["IMAGE", "--x X", "--y Y", "--w W", "--h H", "--output OUT"], "Crop image"),
            ("convert", ["IMAGE", "--format png|jpg|webp|...", "--output OUT"], "Convert format"),
            ("watermark", ["IMAGE", "--text TEXT", "--output OUT"], "Add text watermark"),
            ("filter", ["IMAGE", "--type blur|sharpen|grayscale|...", "--output OUT"], "Apply filter"),
            ("batch", ["DIR", "--op resize|convert|...", "--output-dir OUT"], "Batch process folder"),
        ],
        "json_example": '{"width":1920,"height":1080,"mode":"RGB","format":"JPEG","size_bytes":245760}',
        "seo_keywords": "GIMP CLI, batch image processing command line, GIMP Python automation, image resize CLI",
    },
    {
        "slug": "blender",
        "name": "Blender",
        "package": "cli-anything-blender",
        "cmd": "blender-cli",
        "category": "Image & Design",
        "icon": "https://cdn.simpleicons.org/blender",
        "badge": "208 tests passed",
        "tagline": "3D scene management, rendering and object creation via bpy",
        "description": "Control Blender headlessly via Python bpy API. Create scenes, add objects, apply materials, configure lighting and render with CYCLES or EEVEE. Perfect for automated 3D pipeline integration.",
        "install": "pip install cli-anything-blender",
        "requires": "Blender with Python (bpy)",
        "tags": ["3D Rendering", "Scene Management", "bpy", "CYCLES"],
        "commands": [
            ("detect", [], "Verify Blender/bpy installation"),
            ("version", [], "Show Blender version"),
            ("render", ["SCENE_FILE", "--output OUT", "--engine cycles|eevee", "--samples N"], "Render scene to image"),
            ("info", ["SCENE_FILE"], "List objects, materials, cameras in scene"),
            ("add-object", ["SCENE_FILE", "--type mesh|light|camera", "--name NAME"], "Add object to scene"),
            ("export", ["SCENE_FILE", "--format obj|fbx|glb|stl", "--output OUT"], "Export 3D model"),
        ],
        "json_example": '{"objects":["Cube","Light","Camera"],"materials":["Material.001"],"render_engine":"CYCLES"}',
        "seo_keywords": "Blender CLI, blender headless rendering, bpy command line, 3D render automation",
    },
    {
        "slug": "inkscape",
        "name": "Inkscape",
        "package": "cli-anything-inkscape",
        "cmd": "inkscape-cli",
        "category": "Image & Design",
        "icon": "https://cdn.simpleicons.org/inkscape",
        "badge": "202 tests passed",
        "tagline": "SVG creation, vector editing and multi-format export",
        "description": "Create and manipulate SVG files programmatically. Add shapes, text, gradients and transforms. Export to PNG, PDF or other formats. Automate vector artwork pipelines without a GUI.",
        "install": "pip install cli-anything-inkscape",
        "requires": "Inkscape (optional, falls back to svgwrite)",
        "tags": ["SVG Design", "Vector Art", "PDF Export"],
        "commands": [
            ("detect", [], "Check Inkscape / svgwrite availability"),
            ("create", ["--output OUT", "--width W", "--height H"], "Create new SVG canvas"),
            ("export", ["SVG_FILE", "--format png|pdf|eps", "--output OUT"], "Export SVG to other format"),
            ("add-text", ["SVG_FILE", "--text TEXT", "--x X", "--y Y", "--size S"], "Add text element"),
            ("add-rect", ["SVG_FILE", "--x X", "--y Y", "--w W", "--h H", "--fill COLOR"], "Add rectangle"),
            ("info", ["SVG_FILE"], "Get SVG metadata and element count"),
        ],
        "json_example": '{"width":"800","height":"600","elements":12,"viewBox":"0 0 800 600"}',
        "seo_keywords": "Inkscape CLI, SVG automation command line, vector graphics Python, inkscape headless export",
    },
    {
        "slug": "obs-studio",
        "name": "OBS Studio",
        "package": "cli-anything-obs-studio",
        "cmd": "obs-cli",
        "category": "Video & Audio",
        "icon": "https://cdn.simpleicons.org/obsstudio/ffffff",
        "badge": "153 tests passed",
        "tagline": "Live streaming and screen recording control via obs-websocket",
        "description": "Control OBS Studio programmatically via JSON scene files and obs-websocket protocol. Manage scenes, sources, recording state, stream configuration and transitions from the command line.",
        "install": "pip install cli-anything-obs-studio",
        "requires": "OBS Studio with obs-websocket plugin",
        "tags": ["Live Streaming", "Screen Recording", "WebSocket"],
        "commands": [
            ("detect", [], "Check OBS WebSocket connection"),
            ("version", [], "Show OBS and websocket version"),
            ("scene list", [], "List all scenes"),
            ("scene switch", ["SCENE_NAME"], "Switch to scene"),
            ("record start", [], "Start recording"),
            ("record stop", [], "Stop recording"),
            ("stream start", [], "Start streaming"),
            ("stream stop", [], "Stop streaming"),
            ("source list", ["--scene SCENE"], "List sources in scene"),
        ],
        "json_example": '{"recording":true,"streaming":false,"current_scene":"Game Capture","fps":60}',
        "seo_keywords": "OBS CLI, OBS Studio command line, obs-websocket Python, streaming automation",
    },
    {
        "slug": "audacity",
        "name": "Audacity",
        "package": "cli-anything-audacity",
        "cmd": "audacity-cli",
        "category": "Video & Audio",
        "icon": "https://cdn.simpleicons.org/audacity",
        "badge": "161 tests passed",
        "tagline": "Audio editing, noise reduction and format conversion",
        "description": "Process audio files: cut, mix, denoise, equalize, normalize and convert formats (MP3, WAV, FLAC, OGG). Uses Python wave and sox for processing without a GUI.",
        "install": "pip install cli-anything-audacity",
        "requires": "sox (recommended), Python wave",
        "tags": ["Audio Editing", "Format Conversion", "sox"],
        "commands": [
            ("detect", [], "Check audio processing backend"),
            ("info", ["AUDIO_FILE"], "Get audio metadata"),
            ("convert", ["INPUT", "--format mp3|wav|flac|ogg", "--output OUT"], "Convert audio format"),
            ("trim", ["INPUT", "--start S", "--end E", "--output OUT"], "Trim audio clip"),
            ("normalize", ["INPUT", "--output OUT"], "Normalize audio levels"),
            ("merge", ["FILE1", "FILE2", "--output OUT"], "Merge audio files"),
            ("denoise", ["INPUT", "--output OUT"], "Apply noise reduction"),
        ],
        "json_example": '{"duration":120.5,"channels":2,"sample_rate":44100,"format":"mp3","bitrate":"320k"}',
        "seo_keywords": "Audacity CLI, audio processing command line, sox Python, audio format conversion",
    },
    {
        "slug": "libreoffice",
        "name": "LibreOffice",
        "package": "cli-anything-libreoffice",
        "cmd": "libreoffice-cli",
        "category": "Office & Productivity",
        "icon": "https://cdn.simpleicons.org/libreoffice",
        "badge": "158 tests passed",
        "tagline": "Writer, Calc, Impress headless — real PDF export",
        "description": "Generate and convert Office documents headlessly. Create Writer documents, Calc spreadsheets and Impress presentations programmatically. Export real PDFs with full formatting preservation.",
        "install": "pip install cli-anything-libreoffice",
        "requires": "LibreOffice",
        "tags": ["Document Generation", "PDF Export", "Headless"],
        "commands": [
            ("detect", [], "Check LibreOffice installation"),
            ("version", [], "Show LibreOffice version"),
            ("convert", ["INPUT", "--format pdf|docx|odt|xlsx|pptx", "--output OUT"], "Convert document format"),
            ("create-doc", ["--content TEXT", "--output OUT"], "Create Writer document"),
            ("create-sheet", ["--csv DATA", "--output OUT"], "Create Calc spreadsheet from CSV"),
            ("info", ["FILE"], "Get document metadata"),
            ("batch-convert", ["DIR", "--from-format odt", "--to-format pdf"], "Batch convert directory"),
        ],
        "json_example": '{"pages":5,"words":1250,"author":"AgentPuter","created":"2026-03-15","format":"pdf"}',
        "seo_keywords": "LibreOffice CLI, LibreOffice headless convert, PDF generation command line, soffice Python",
    },
    {
        "slug": "ms365",
        "name": "Microsoft 365",
        "package": "cli-anything-ms365",
        "cmd": "ms365-cli",
        "category": "Office & Productivity",
        "icon": "https://cdn.simpleicons.org/microsoftoffice",
        "badge": "Live",
        "tagline": "Word, Excel, PowerPoint, Outlook — full COM automation",
        "description": "Control Microsoft 365 applications via Windows COM automation. Create Word documents, manipulate Excel spreadsheets, build PowerPoint presentations and send Outlook emails — fully programmatic.",
        "install": "pip install cli-anything-ms365",
        "requires": "Windows + Microsoft Office installed",
        "tags": ["COM Automation", "Word", "Excel", "PowerPoint", "Outlook"],
        "commands": [
            ("detect", [], "Check Office COM availability"),
            ("word create", ["--content TEXT", "--output OUT.docx"], "Create Word document"),
            ("word convert", ["INPUT.docx", "--format pdf", "--output OUT"], "Convert to PDF"),
            ("excel create", ["--data JSON", "--output OUT.xlsx"], "Create Excel file"),
            ("excel read", ["INPUT.xlsx", "--sheet SHEET"], "Read spreadsheet data"),
            ("ppt create", ["--title TITLE", "--slides JSON", "--output OUT.pptx"], "Create presentation"),
            ("outlook send", ["--to EMAIL", "--subject SUBJ", "--body BODY"], "Send email via Outlook"),
        ],
        "json_example": '{"application":"Word","version":"16.0","path":"C:\\\\doc.docx","pages":3}',
        "seo_keywords": "Microsoft 365 CLI, Word automation Python, Excel command line, COM automation Python",
    },
    {
        "slug": "notion",
        "name": "Notion",
        "package": "cli-anything-notion",
        "cmd": "notion-cli",
        "category": "Office & Productivity",
        "icon": "https://cdn.simpleicons.org/notion/ffffff",
        "badge": "13 tests passed",
        "tagline": "Pages, databases and blocks via Notion REST API",
        "description": "Full programmatic control over Notion workspaces. Create and update pages, append blocks, query databases with filters, search across workspace — all via official Notion REST API v1.",
        "install": "pip install cli-anything-notion",
        "requires": "NOTION_TOKEN (Integration token)",
        "tags": ["Knowledge Base", "Database Query", "REST API"],
        "commands": [
            ("detect", [], "Verify Notion integration token"),
            ("version", [], "Show API version and user info"),
            ("search", ["QUERY", "--limit N"], "Search pages and databases"),
            ("page get", ["PAGE_ID"], "Get page content"),
            ("page create", ["--parent-id ID", "--title TITLE"], "Create page"),
            ("page append-text", ["PAGE_ID", "TEXT"], "Append text block to page"),
            ("page archive", ["PAGE_ID"], "Archive page"),
            ("database query", ["DB_ID", "--filter JSON", "--limit N"], "Query database"),
            ("users list", [], "List workspace members"),
        ],
        "json_example": '{"id":"abc-123","title":"My Page","created":"2026-03-15","blocks":8}',
        "seo_keywords": "Notion CLI, Notion API command line, Notion automation Python, Notion database query CLI",
    },
    {
        "slug": "zoom",
        "name": "Zoom",
        "package": "cli-anything-zoom",
        "cmd": "zoom-cli",
        "category": "Communication",
        "icon": "https://cdn.simpleicons.org/zoom",
        "badge": "22 tests passed",
        "tagline": "Meeting management via Zoom REST API (OAuth2)",
        "description": "Create, list and delete Zoom meetings. Manage participants, retrieve recordings and configure meeting settings via the official Zoom REST API with OAuth2 authentication.",
        "install": "pip install cli-anything-zoom",
        "requires": "ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, ZOOM_ACCOUNT_ID",
        "tags": ["REST API", "Meeting Automation", "OAuth2"],
        "commands": [
            ("detect", [], "Check Zoom API credentials"),
            ("version", [], "Show API version"),
            ("meeting list", ["--limit N"], "List meetings"),
            ("meeting create", ["--topic TOPIC", "--start DATETIME", "--duration MIN"], "Create meeting"),
            ("meeting get", ["MEETING_ID"], "Get meeting details"),
            ("meeting delete", ["MEETING_ID"], "Delete meeting"),
            ("recording list", ["--user USER_ID"], "List cloud recordings"),
        ],
        "json_example": '{"id":12345,"topic":"AI Demo","join_url":"https://zoom.us/j/...","start_time":"2026-03-15T10:00:00Z"}',
        "seo_keywords": "Zoom CLI, Zoom REST API Python, meeting automation command line, Zoom OAuth2",
    },
    {
        "slug": "slack",
        "name": "Slack",
        "package": "cli-anything-slack",
        "cmd": "slack-cli",
        "category": "Communication",
        "icon": "https://cdn.simpleicons.org/slack",
        "badge": "18 tests passed",
        "tagline": "Messages, channels, files and users via Slack Web API",
        "description": "Post messages, upload files, list channels, manage reactions and search messages across your Slack workspace. Uses the official Slack SDK for Python with full Bot token support.",
        "install": "pip install cli-anything-slack",
        "requires": "SLACK_BOT_TOKEN (xoxb-...)",
        "tags": ["Team Messaging", "Workflow Bots", "slack-sdk"],
        "commands": [
            ("detect", [], "Verify Slack Bot token"),
            ("schema", [], "Output full capability schema (no token needed)"),
            ("channel list", ["--limit N"], "List all channels"),
            ("channel create", ["NAME", "--private"], "Create channel"),
            ("message send", ["CHANNEL", "TEXT", "--thread-ts TS"], "Send message"),
            ("message history", ["CHANNEL", "--limit N"], "Get message history"),
            ("message search", ["QUERY", "--count N"], "Search messages globally"),
            ("message react", ["CHANNEL", "TS", "EMOJI"], "React to message"),
            ("file upload", ["FILEPATH", "--channel C", "--title T"], "Upload file"),
            ("user list", ["--limit N"], "List workspace members"),
            ("user lookup", ["EMAIL"], "Find user by email"),
        ],
        "json_example": '{"ts":"1710000000.000001","channel":"C0ABC123","status":"sent"}',
        "seo_keywords": "Slack CLI, Slack Bot API Python, slack-sdk command line, Slack message automation",
    },
    {
        "slug": "discord",
        "name": "Discord",
        "package": "cli-anything-discord",
        "cmd": "discord-cli",
        "category": "Communication",
        "icon": "https://cdn.simpleicons.org/discord",
        "badge": "21 tests passed",
        "tagline": "Guilds, channels, members, webhooks via Discord REST API v10",
        "description": "Send messages, manage Discord servers (guilds), channels, roles and members. Create and use webhooks for notifications. Pure REST implementation — no heavy discord.py dependency required.",
        "install": "pip install cli-anything-discord",
        "requires": "DISCORD_BOT_TOKEN",
        "tags": ["Community Bots", "Webhook Automation", "REST API v10"],
        "commands": [
            ("detect", [], "Verify Discord Bot token"),
            ("schema", [], "Output full capability schema (no token needed)"),
            ("guild list", [], "List all guilds Bot joined"),
            ("guild channels", ["GUILD_ID"], "List guild channels"),
            ("guild members", ["GUILD_ID", "--limit N"], "List guild members"),
            ("guild roles", ["GUILD_ID"], "List guild roles"),
            ("message send", ["CHANNEL_ID", "CONTENT"], "Send message"),
            ("message history", ["CHANNEL_ID", "--limit N"], "Get message history"),
            ("message react", ["CHANNEL_ID", "MESSAGE_ID", "EMOJI"], "Add reaction"),
            ("webhook send", ["WEBHOOK_URL", "CONTENT"], "Send via webhook (no token needed)"),
            ("webhook create", ["CHANNEL_ID", "NAME"], "Create webhook"),
        ],
        "json_example": '{"id":"1234567890","channel_id":"987654321","content":"Hello","status":"sent"}',
        "seo_keywords": "Discord CLI, Discord Bot API Python, Discord webhook command line, discord server automation",
    },
    {
        "slug": "telegram",
        "name": "Telegram",
        "package": "cli-anything-telegram",
        "cmd": "telegram-cli",
        "category": "Communication",
        "icon": "https://cdn.simpleicons.org/telegram",
        "badge": "24 tests passed",
        "tagline": "Bot messages, groups, polls and notifications — pure REST",
        "description": "Full Telegram Bot API access with zero extra dependencies beyond click. Send text, photos, documents, polls and location. Manage groups, pin messages, kick members and set Bot commands.",
        "install": "pip install cli-anything-telegram",
        "requires": "TELEGRAM_BOT_TOKEN (from @BotFather)",
        "tags": ["Bot API", "Notifications", "Zero Dependencies"],
        "commands": [
            ("detect", [], "Verify Bot token and get Bot info"),
            ("schema", [], "Output full capability schema (no token needed)"),
            ("send text", ["CHAT_ID", "TEXT", "--parse-mode HTML|Markdown"], "Send text message"),
            ("send photo", ["CHAT_ID", "PHOTO_URL", "--caption TEXT"], "Send photo"),
            ("send document", ["CHAT_ID", "DOC_URL", "--caption TEXT"], "Send document"),
            ("send poll", ["CHAT_ID", "QUESTION", "--option A --option B"], "Create poll"),
            ("send location", ["CHAT_ID", "LAT", "LON"], "Send location"),
            ("chat info", ["CHAT_ID"], "Get chat/group details"),
            ("chat pin", ["CHAT_ID", "MESSAGE_ID"], "Pin message"),
            ("chat kick", ["CHAT_ID", "USER_ID"], "Kick member"),
            ("updates get", ["--limit N"], "Get latest updates"),
            ("bot set-commands", ["--cmd cmd:desc ..."], "Set Bot command menu"),
        ],
        "json_example": '{"message_id":42,"chat_id":"@mychannel","date":1710000000,"status":"sent"}',
        "seo_keywords": "Telegram Bot CLI, Telegram API Python command line, telegram bot send message, telegram notification CLI",
    },
    {
        "slug": "docker",
        "name": "Docker",
        "package": "cli-anything-docker",
        "cmd": "docker-cli",
        "category": "Development",
        "icon": "https://cdn.simpleicons.org/docker",
        "badge": "12 tests passed",
        "tagline": "Container lifecycle, images, volumes and networks via Docker SDK",
        "description": "Manage Docker containers, images, volumes and networks programmatically using the Docker Python SDK. Run containers, stream logs, exec commands and monitor stats with structured JSON output.",
        "install": "pip install cli-anything-docker",
        "requires": "Docker daemon running, docker SDK",
        "tags": ["Containers", "Docker SDK", "DevOps"],
        "commands": [
            ("detect", [], "Check Docker daemon connection"),
            ("version", [], "Show Docker version info"),
            ("container list", ["--all"], "List containers"),
            ("container run", ["IMAGE", "--name N", "--env K=V", "--port H:C"], "Run container"),
            ("container stop", ["CONTAINER"], "Stop container"),
            ("container logs", ["CONTAINER", "--tail N"], "Stream container logs"),
            ("container exec", ["CONTAINER", "COMMAND"], "Execute command in container"),
            ("image list", [], "List images"),
            ("image pull", ["IMAGE:TAG"], "Pull image from registry"),
            ("volume list", [], "List volumes"),
            ("network list", [], "List networks"),
            ("system df", [], "Show disk usage"),
        ],
        "json_example": '{"id":"abc123","name":"my-app","status":"running","image":"nginx:latest","ports":{"80/tcp":"8080"}}',
        "seo_keywords": "Docker CLI Python, docker SDK command line, container management Python, docker automation agent",
    },
    {
        "slug": "github",
        "name": "GitHub",
        "package": "cli-anything-github",
        "cmd": "github-cli",
        "category": "Development",
        "icon": "https://cdn.simpleicons.org/github/ffffff",
        "badge": "14 tests passed",
        "tagline": "Issues, PRs, Actions, releases and gists via GitHub REST API",
        "description": "Full GitHub automation via PyGithub. Create issues and pull requests, trigger GitHub Actions workflows, manage releases, gists and repository metadata — all with JSON output for AI agent pipelines.",
        "install": "pip install cli-anything-github",
        "requires": "GITHUB_TOKEN (Personal Access Token)",
        "tags": ["CI/CD", "Code Management", "PyGithub"],
        "commands": [
            ("detect", [], "Verify GitHub token"),
            ("repo list", ["--org ORG", "--limit N"], "List repositories"),
            ("repo create", ["--name NAME", "--private", "--desc DESC"], "Create repository"),
            ("issue list", ["OWNER/REPO", "--state open|closed"], "List issues"),
            ("issue create", ["OWNER/REPO", "--title T", "--body B", "--label L"], "Create issue"),
            ("pr list", ["OWNER/REPO", "--state open|closed"], "List pull requests"),
            ("pr create", ["OWNER/REPO", "--title T", "--head BRANCH", "--base main"], "Create PR"),
            ("release list", ["OWNER/REPO"], "List releases"),
            ("release create", ["OWNER/REPO", "--tag v1.0", "--title T", "--notes N"], "Create release"),
            ("actions list-workflows", ["OWNER/REPO"], "List GitHub Actions workflows"),
            ("actions trigger", ["OWNER/REPO", "WORKFLOW_ID", "--ref main"], "Trigger workflow"),
            ("gist create", ["FILE", "--desc DESC", "--public"], "Create gist"),
        ],
        "json_example": '{"number":42,"title":"Fix login bug","state":"open","url":"https://github.com/..."}',
        "seo_keywords": "GitHub CLI Python, PyGithub command line, GitHub Actions automation, GitHub API Python agent",
    },
    {
        "slug": "ollama",
        "name": "Ollama",
        "package": "cli-anything-ollama",
        "cmd": "ollama-cli",
        "category": "AI & Automation",
        "icon": "https://cdn.simpleicons.org/ollama/ffffff",
        "badge": "9 tests passed",
        "tagline": "Local LLM management, chat and embeddings via Ollama REST API",
        "description": "Manage your local Ollama LLM server from the command line. Pull and delete models, run single prompts or multi-turn conversations, generate embeddings — all with streaming support and JSON output.",
        "install": "pip install cli-anything-ollama",
        "requires": "Ollama server running (localhost:11434)",
        "tags": ["Local LLMs", "Model Management", "Embeddings"],
        "commands": [
            ("detect", [], "Check Ollama server connection"),
            ("version", [], "Show Ollama server version"),
            ("list", [], "List downloaded models"),
            ("ps", [], "Show running models"),
            ("pull", ["MODEL"], "Pull model from Ollama Hub"),
            ("show", ["MODEL"], "Show model details"),
            ("run", ["MODEL", "PROMPT", "--system SYS", "--temperature T"], "Single text generation"),
            ("chat", ["MODEL", "--system SYS"], "Interactive multi-turn chat"),
            ("embeddings", ["MODEL", "TEXT"], "Generate text embeddings"),
            ("delete", ["MODEL"], "Delete model"),
        ],
        "json_example": '{"model":"llama3.2","response":"Hello! How can I help?","total_duration_ms":1250}',
        "seo_keywords": "Ollama CLI, Ollama REST API Python, local LLM command line, llama command line tool",
    },
    {
        "slug": "drawio",
        "name": "Draw.io",
        "package": "cli-anything-drawio",
        "cmd": "drawio-cli",
        "category": "Cloud & Utilities",
        "icon": "https://cdn.simpleicons.org/diagramsdotnet",
        "badge": "138 tests passed",
        "tagline": "Flowcharts and architecture diagrams via mxGraph XML",
        "description": "Create and manipulate Draw.io (diagrams.net) files programmatically. Generate flowcharts, architecture diagrams and ER diagrams using mxGraph XML. Export to PNG, SVG or PDF via the draw.io CLI.",
        "install": "pip install cli-anything-drawio",
        "requires": "draw.io desktop (for export)",
        "tags": ["Flowcharts", "Architecture Diagrams", "mxGraph"],
        "commands": [
            ("detect", [], "Check draw.io installation"),
            ("create", ["--output FILE.drawio", "--template flowchart|erd|network"], "Create diagram from template"),
            ("export", ["FILE.drawio", "--format png|svg|pdf", "--output OUT"], "Export to image/PDF"),
            ("add-shape", ["FILE.drawio", "--label LABEL", "--style STYLE", "--x X", "--y Y"], "Add shape"),
            ("add-edge", ["FILE.drawio", "--from SRC", "--to DST", "--label L"], "Add connection"),
            ("info", ["FILE.drawio"], "Get diagram metadata"),
        ],
        "json_example": '{"shapes":12,"edges":8,"pages":2,"format":"drawio","export":"diagram.png"}',
        "seo_keywords": "Draw.io CLI, diagrams.net command line, flowchart automation Python, mxGraph Python",
    },
    {
        "slug": "stripe",
        "name": "Stripe",
        "package": "cli-anything-stripe",
        "cmd": "stripe-cli",
        "category": "SaaS & Business APIs",
        "icon": "https://cdn.simpleicons.org/stripe",
        "badge": "19 tests passed",
        "tagline": "Payments, subscriptions, refunds and products via Stripe SDK",
        "description": "Full Stripe payment automation via the official Python SDK. Manage customers, create PaymentIntents, handle subscriptions and process refunds. Supports both test and live modes with structured JSON output.",
        "install": "pip install cli-anything-stripe",
        "requires": "STRIPE_SECRET_KEY (sk_test_... or sk_live_...)",
        "tags": ["Payments", "Stripe SDK", "E-Commerce"],
        "commands": [
            ("detect", [], "Verify API key and show account"),
            ("schema", [], "Output full capability schema (no key needed)"),
            ("customer list", ["--limit N", "--email E"], "List customers"),
            ("customer create", ["--email E", "--name N", "--phone P"], "Create customer"),
            ("customer get", ["CUSTOMER_ID"], "Get customer details"),
            ("payment list", ["--limit N", "--customer C"], "List PaymentIntents"),
            ("payment create", ["--amount N", "--currency usd", "--customer C"], "Create PaymentIntent"),
            ("subscription list", ["--customer C", "--status active"], "List subscriptions"),
            ("subscription cancel", ["SUB_ID", "--at-period-end"], "Cancel subscription"),
            ("refund create", ["PAYMENT_INTENT_ID", "--amount N"], "Create refund"),
            ("product list", ["--limit N"], "List products"),
            ("product create", ["--name N", "--price P", "--currency usd"], "Create product with price"),
        ],
        "json_example": '{"id":"cus_abc123","email":"user@example.com","name":"Alice","subscriptions":1}',
        "seo_keywords": "Stripe CLI Python, Stripe payment automation, Stripe API command line, payment processing CLI agent",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# HTML TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────
def render_commands(commands):
    rows = ""
    for cmd in commands:
        args_html = " ".join(f'<code class="arg">{a}</code>' for a in cmd[1])
        rows += f"""
        <tr>
          <td><code class="cmd-name">{cmd[0]}</code></td>
          <td>{args_html}</td>
          <td>{cmd[2]}</td>
        </tr>"""
    return rows

def render_page(tool):
    slug = tool["slug"]
    name = tool["name"]
    package = tool["package"]
    cmd = tool["cmd"]
    icon = tool["icon"]
    badge = tool["badge"]
    tagline = tool["tagline"]
    description = tool["description"]
    install = tool["install"]
    requires = tool["requires"]
    tags = tool["tags"]
    commands = tool["commands"]
    json_example = tool["json_example"]
    category = tool["category"]
    seo_keywords = tool["seo_keywords"]

    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    cmd_rows = render_commands(commands)
    icon_html = f'<img src="{icon}" alt="{name}" width="48" height="48" onerror="this.style.display=\'none\'">'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{name} CLI Tool | {package} | AgentPuter CLI-Anything</title>
  <meta name="description" content="{tagline}. {description[:120]}. Install: pip install {package}">
  <meta name="keywords" content="{seo_keywords}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://www.agentputer.com/cli-anything/{slug}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{name} CLI | {package}">
  <meta property="og:description" content="{tagline}. Agent-ready. pip install {package}">
  <meta property="og:url" content="https://www.agentputer.com/cli-anything/{slug}/">
  <meta property="og:image" content="https://www.agentputer.com/cli-anything/og-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{name} CLI | AgentPuter">
  <meta name="twitter:description" content="{tagline}">
  <script type="application/ld+json">{{
    "@context":"https://schema.org",
    "@type":"SoftwareApplication",
    "name":"{package}",
    "applicationCategory":"DeveloperApplication",
    "operatingSystem":"Windows, macOS, Linux",
    "description":"{description[:200]}",
    "url":"https://www.agentputer.com/cli-anything/{slug}/",
    "author":{{"@type":"Organization","name":"AgentPuter"}},
    "offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}},
    "downloadUrl":"https://pypi.org/project/{package}/"
  }}</script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    :root{{--g:#00ff41;--b:#000;--s:#0a0a0a;--t:#e0e0e0;--dim:#888;--bdr:rgba(0,255,65,.15);--gd:rgba(0,255,65,.04)}}
    body{{background:var(--b);color:var(--t);font-family:'Courier New',monospace;min-height:100vh;line-height:1.6}}
    a{{color:var(--g);text-decoration:none}}a:hover{{text-decoration:underline}}
    .nav{{display:flex;align-items:center;justify-content:space-between;padding:16px 32px;border-bottom:1px solid var(--bdr);background:rgba(0,0,0,.8);position:sticky;top:0;z-index:100;backdrop-filter:blur(8px)}}
    .nav-logo{{font-size:13px;font-weight:700;color:var(--g);letter-spacing:1px}}.nav-logo span{{color:var(--t)}}
    .nav-links{{display:flex;gap:24px;font-size:12px;color:var(--dim)}}
    .hero{{max-width:900px;margin:60px auto 40px;padding:0 24px;text-align:center}}
    .hero-cat{{font-size:11px;letter-spacing:2px;color:var(--dim);text-transform:uppercase;margin-bottom:16px}}
    .hero-icon{{margin-bottom:20px;display:flex;align-items:center;justify-content:center;gap:16px}}
    .hero-icon img{{filter:brightness(0) invert(1)}}
    .hero-name{{font-size:clamp(36px,6vw,64px);font-weight:900;color:#fff;letter-spacing:-1px;line-height:1}}
    .hero-name span{{color:var(--g)}}
    .hero-tagline{{font-size:16px;color:var(--dim);margin:16px 0 24px;max-width:600px;margin-left:auto;margin-right:auto}}
    .badge{{display:inline-flex;align-items:center;gap:8px;background:var(--gd);border:1px solid var(--bdr);border-radius:4px;padding:6px 16px;font-size:13px;color:var(--g)}}
    .install-block{{max-width:900px;margin:0 auto 40px;padding:0 24px}}
    .install-title{{font-size:12px;letter-spacing:2px;color:var(--dim);text-transform:uppercase;margin-bottom:12px}}
    .install-cmd{{background:#0a0a0a;border:1px solid var(--bdr);border-radius:6px;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px}}
    .install-cmd code{{font-size:15px;color:var(--g);font-family:'Courier New',monospace}}
    .copy-btn{{background:transparent;border:1px solid var(--bdr);color:var(--dim);font-size:11px;padding:4px 12px;border-radius:3px;cursor:pointer;font-family:inherit;transition:.2s}}
    .copy-btn:hover{{border-color:var(--g);color:var(--g)}}
    .section{{max-width:900px;margin:0 auto 48px;padding:0 24px}}
    .section-title{{font-size:12px;letter-spacing:2px;color:var(--g);text-transform:uppercase;margin-bottom:20px;padding-bottom:8px;border-bottom:1px solid var(--bdr)}}
    .desc-text{{color:var(--dim);font-size:14px;line-height:1.8;font-family:system-ui,-apple-system,sans-serif}}
    .tags{{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}}
    .tag{{font-size:11px;padding:3px 10px;border:1px solid var(--bdr);border-radius:3px;color:var(--dim)}}
    .cmd-table{{width:100%;border-collapse:collapse;font-size:13px}}
    .cmd-table th{{text-align:left;padding:8px 12px;color:var(--g);font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid var(--bdr)}}
    .cmd-table td{{padding:10px 12px;border-bottom:1px solid rgba(0,255,65,.06);vertical-align:top;color:var(--dim)}}
    .cmd-table tr:hover td{{background:var(--gd)}}
    code.cmd-name{{color:var(--g);font-weight:700}}
    code.arg{{color:#7ec8e3;font-size:11px;background:rgba(126,200,227,.08);padding:1px 6px;border-radius:2px;margin:0 2px}}
    .json-block{{background:#0a0a0a;border:1px solid var(--bdr);border-radius:6px;padding:20px;overflow-x:auto}}
    .json-block pre{{color:#7ec8e3;font-size:13px;font-family:'Courier New',monospace;white-space:pre-wrap}}
    .requires-block{{background:var(--gd);border:1px solid var(--bdr);border-radius:6px;padding:16px 20px;font-size:13px}}
    .requires-label{{color:var(--g);font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px}}
    .requires-value{{color:var(--dim)}}
    .footer{{border-top:1px solid var(--bdr);padding:32px;text-align:center;color:var(--dim);font-size:12px;margin-top:80px}}
    .footer a{{color:var(--g)}}
    @media(max-width:600px){{.nav-links{{display:none}}.install-cmd{{flex-direction:column;align-items:flex-start}}}}
  </style>
</head>
<body>
<nav class="nav">
  <div class="nav-logo">&gt;_ <span>Agent</span>Puter</div>
  <div class="nav-links">
    <a href="/cli-anything/">← All Tools</a>
    <a href="https://pypi.org/project/{package}/" target="_blank">PyPI</a>
    <a href="https://github.com/agentputer/cli-anything" target="_blank">GitHub</a>
    <a href="https://www.agentputer.com/" target="_blank">AgentPuter Home</a>
  </div>
</nav>

<main>
  <div class="hero">
    <div class="hero-cat">{category}</div>
    <div class="hero-icon">
      {icon_html}
    </div>
    <h1 class="hero-name"><span>{name}</span> CLI</h1>
    <p class="hero-tagline">{tagline}</p>
    <div class="badge">✓ {badge}</div>
  </div>

  <div class="install-block">
    <div class="install-title">Install</div>
    <div class="install-cmd">
      <code>$ {install}</code>
      <button class="copy-btn" onclick="navigator.clipboard.writeText('{install}');this.textContent='✓ Copied';setTimeout(()=>this.textContent='Copy',2000)">Copy</button>
    </div>
  </div>

  <div class="section">
    <div class="section-title">About</div>
    <p class="desc-text">{description}</p>
    <div class="tags">{tags_html}</div>
  </div>

  <div class="section">
    <div class="requires-block">
      <div class="requires-label">Requirements</div>
      <div class="requires-value">{requires}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Command Reference</div>
    <table class="cmd-table">
      <thead>
        <tr>
          <th>Command</th>
          <th>Arguments</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>{cmd_rows}
      </tbody>
    </table>
  </div>

  <div class="section">
    <div class="section-title">Usage Examples</div>
    <div class="json-block">
      <pre><code class="language-bash"># Install
$ pip install {package}

# Health check
$ {cmd} detect

# Get capabilities schema (Agent-ready, no token needed)
$ {cmd} schema

# Run with JSON output (for AI Agent integration)
$ {cmd} --json detect

# Example JSON response:
{json_example}</code></pre>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Agent Integration</div>
    <div class="json-block">
      <pre><code class="language-python"># Python — call from AI Agent
import subprocess, json

result = subprocess.run(
    ["{cmd}", "--json", "detect"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
print(data)

# Discover all commands without credentials:
schema = subprocess.run(
    ["{cmd}", "schema"],
    capture_output=True, text=True
)
capabilities = json.loads(schema.stdout)</code></pre>
    </div>
  </div>
</main>

<footer class="footer">
  <p>
    <a href="/cli-anything/">&lt; Back to CLI-Anything Hub</a>
    &nbsp;·&nbsp;
    <a href="https://pypi.org/project/{package}/" target="_blank">PyPI: {package}</a>
    &nbsp;·&nbsp;
    <a href="https://www.agentputer.com/" target="_blank">AgentPuter.com</a>
  </p>
  <p style="margin-top:8px">Part of <strong>CLI-Anything</strong> — one command turns any software into an AI Agent tool.</p>
</footer>
</body>
</html>"""


def main():
    generated = 0
    for tool in TOOLS:
        slug = tool["slug"]
        out_dir = os.path.join(OUTPUT_BASE, slug)
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "index.html")
        html = render_page(tool)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Generated: cli-anything/{slug}/index.html")
        generated += 1

    # Generate sitemap fragment
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap_lines.append('  <url><loc>https://www.agentputer.com/cli-anything/</loc><priority>1.0</priority></url>')
    for tool in TOOLS:
        sitemap_lines.append(f'  <url><loc>https://www.agentputer.com/cli-anything/{tool["slug"]}/</loc><priority>0.8</priority><changefreq>monthly</changefreq></url>')
    sitemap_lines.append('</urlset>')
    sitemap_path = os.path.join(OUTPUT_BASE, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_lines))
    print(f"✅ Generated: sitemap.xml ({generated} tools)")

    print(f"\n🎉 Done — {generated} sub-pages generated in: {OUTPUT_BASE}")


if __name__ == "__main__":
    main()
