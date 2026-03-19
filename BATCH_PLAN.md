# CLI-Anything 全球软件 CLI 化计划

> 更新时间：2026-03-15  
> 目标：将世界上所有主流知名软件系统地 CLI 化，统一打包发布到 GitHub + PyPI

---

## 一、已完成清单（13 个）

| # | 软件 | 目录 | 接口方式 | 状态 |
|---|------|------|----------|------|
| 1 | Microsoft 365 (Word/Excel/PPT/Outlook) | `ms365-cli/` | COM 自动化 | ✅ |
| 2 | Inkscape | `inkscape/agent-harness/` | 内置 CLI | ✅ |
| 3 | LibreOffice | `libreoffice/agent-harness/` | `--headless` CLI | ✅ |
| 4 | OBS Studio | `obs-studio/agent-harness/` | WebSocket API | ✅ |
| 5 | Shotcut | `shotcut/agent-harness/` | MLT XML + `melt` | ✅ |
| 6 | Kdenlive | `kdenlive/agent-harness/` | MLT XML + `melt` | ✅ |
| 7 | GIMP | `gimp/agent-harness/` | Script-Fu / Python-Fu | ✅ |
| 8 | Blender | `blender/agent-harness/` | `bpy` Python scripting | ✅ |
| 9 | Audacity | `audacity/agent-harness/` | Mod-Script-Pipe | ✅ |
| 10 | Draw.io | `drawio/agent-harness/` | `@diagrams.net/cli` | ✅ |
| 11 | Zoom | `zoom/agent-harness/` | Zoom REST API | ✅ |
| 12 | AnyGen | `anygen/agent-harness/` | AnyGen REST API | ✅ |
| 13 | 飞书 (Feishu) | `feishu-cli/` | 飞书开放平台 API | ✅ |

---

## 二、IMAGE & DESIGN（图像与设计）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 |
|---|------|------------------|----------|--------|
| 14 | **Krita** | `krita` | Python scripting API | 🔥 高 |
| 15 | **Adobe Photoshop** | `adobephotoshop` | @adobe/aio-lib-photoshop-api (官方) — 批量处理/抠图/图层自动化 | 🔥 高 |
| 16 | **Adobe Illustrator** | `adobeillustrator` | UXP JavaScript API | 🔥 高 |
| 17 | **Figma** | `figma` | figma-ds-cli — 无需 API Key 直接控制 Figma Desktop，读写组件/变量/Token | 🔥 高 |
| 18 | **Canva** | `canva` | Canva Connect API | 🟡 中 |
| 19 | **Sketch** | `sketch` | REST API (macOS) | 🟡 中 |
| 20 | **Affinity Designer** | `affinity` | 有限脚本接口 | 🟡 中 |

---

## 三、VIDEO & AUDIO（视频与音频）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 |
|---|------|------------------|----------|--------|
| 21 | **FFmpeg / CutAgent** | `ffmpeg` | CutAgent (PyPI) — agent-first 视频编辑，EDL JSON 格式，场景/静音检测 | 🔥 高 |
| 22 | **VLC** | `vlcmediaplayer` | HTTP 接口 + RC mode | 🔥 高 |
| 23 | **DaVinci Resolve** | `davinciresolve` | davinci-cli (PyPI) + resolve-mcp (295+ tools)，MCP Server，Agent 可用 | 🔥 高 |
| 24 | **Adobe Premiere Pro** | `adobepremierepro` | UXP ExtendScript | 🟡 中 |
| 25 | **Adobe After Effects** | `adobeaftereffects` | UXP ExtendScript | 🟡 中 |
| 26 | **HandBrake** | `handbrake` | HandBrakeCLI.exe 封装 | 🔥 高 |
| 27 | **FL Studio** | — | Python scripting API | 🟡 中 |
| 28 | **Ableton Live** | — | Max for Live API | 🟡 中 |

---

## 四、OFFICE & PRODUCTIVITY（办公与生产力）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 |
|---|------|------------------|----------|--------|
| 29 | **Google Docs** | `googledocs` | Google Docs API v1 | 🔥 高 |
| 30 | **Google Sheets** | `googlesheets` | Sheets API v4 | 🔥 高 |
| 31 | **Google Slides** | `googleslides` | Slides API | 🟡 中 |
| 32 | **Google Drive** | `googledrive` | Drive API v3 | 🔥 高 |
| 33 | **Notion** | `notion` | Notion REST API | 🔥 高 |
| 34 | **Obsidian** | `obsidian` | obsidian-cli-rest + MCP Server — vault 搜索/笔记/标签/任务/模板/每日笔记 | 🔥 高 |
| 35 | **Evernote** | `evernote` | Evernote API | 🟡 中 |
| 36 | **Anki** | `anki` | AnkiConnect REST API | 🟡 中 |

---

## 五、COMMUNICATION（沟通协作）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 |
|---|------|------------------|----------|--------|
| 37 | **Slack** | `slack` | Slack Web API | 🔥 高 |
| 38 | **Discord** | `discord` | Discord Bot API | 🔥 高 |
| 39 | **Telegram** | `telegram` | Telegram Bot API | 🔥 高 |
| 40 | **Microsoft Teams** | `microsoftteams` | Microsoft Graph API | 🔥 高 |
| 41 | **WhatsApp** | `whatsapp` | wacli (个人, 22K+ 下载) + WhatsApp Cloud API (商业) — 消息/文件/群组 | 🔥 高 |

---

## 六、DEVELOPMENT（开发工具）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 |
|---|------|------------------|----------|--------|
| 42 | **Docker** | `docker` | Docker Python SDK | 🔥 高 |
| 43 | **GitHub** | `github` | GitHub REST + GraphQL | 🔥 高 |
| 44 | **GitLab** | `gitlab` | GitLab REST API | 🔥 高 |
| 45 | **VS Code** | `visualstudiocode` | `code` CLI + Extension API | 🔥 高 |
| 46 | **Chrome / Edge** | `googlechrome` | Chrome DevTools Protocol | 🔥 高 |
| 47 | **Firefox** | `firefoxbrowser` | Remote Debugging Protocol | 🟡 中 |
| 48 | **JetBrains IDEs** | `jetbrains` | Toolbox + IDE REST API | 🟡 中 |
| 49 | **Postman** | `postman` | Postman API | 🟡 中 |

---

## 七、AI & AUTOMATION（AI 与自动化）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 |
|---|------|------------------|----------|--------|
| 50 | **Ollama** | `ollama` | REST API `localhost:11434` | 🔥 高 |
| 51 | **OpenAI / ChatGPT** | `openai` | OpenAI Python SDK | 🔥 高 |
| 52 | **ComfyUI** | — | REST API `localhost:8188` | 🔥 高 |
| 53 | **Stable Diffusion (A1111)** | — | REST API | 🟡 中 |
| 54 | **Anthropic / Claude** | `anthropic` | Anthropic Python SDK | 🔥 高 |
| 55 | **Midjourney** | — | Discord Bot API 间接调用 | 🔴 低 |

---

## 八、CLOUD & UTILITIES（云存储与工具）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 |
|---|------|------------------|----------|--------|
| 56 | **Google Drive** | `googledrive` | Drive API v3 | 🔥 高 |
| 57 | **OneDrive** | `microsoftonedrive` | Microsoft Graph API | 🔥 高 |
| 58 | **Dropbox** | `dropbox` | Dropbox Python SDK | 🔥 高 |
| 59 | **AWS S3** | `amazonaws` | boto3 | 🔥 高 |
| 60 | **7-Zip** | `7zip` | subprocess 封装 | 🔥 高 |
| 61 | **yt-dlp** | — | Python API | 🔥 高 |
| 62 | **ImageMagick** | `imagemagick` | `magick` subprocess | 🟡 中 |
| 63 | **HandBrake** | `handbrake` | `HandBrakeCLI` 封装 | 🟡 中 |

---

## 九、GAMING & ENTERTAINMENT（游戏娱乐）

> **研究来源（2026-03-15 联网调研）：**  
> Steam Charts 实时同时在线、Riot Developer Portal 官方文档、Roblox Open Cloud API 官方规范、  
> SteamCMD REST API、Chess.com Published-Data API、Lichess 开放 REST API、Speedrun.com REST API、  
> Twitch Helix API、HoYoverse hoyoverse-api、fortnitepy 文档、RCON-CLI 仓库  
> 新增 **20 个 CLI**，总目标扩展至 **83 个**

### 9.1 游戏平台 & 商店（Game Launchers & Stores）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 64 | **Steam** | `steam` | Steam Web API v2 + steamctl Python 库 | 🔥 高 | 获取游戏库/成就/在线好友/游戏统计；`steamctl` PyPI 已有封装 |
| 65 | **Epic Games Store** | `epicgames` | EGS OAuth2 REST API + legendary CLI | 🔥 高 | 获取账号游戏库、免费领取资格查询、安装/更新游戏 |
| 66 | **GOG Galaxy** | `gog` | gogdl CLI + GOG Games DB API | 🟡 中 | 游戏库列表、安装包下载、版本比较 |
| 67 | **Battle.net (Blizzard)** | `battlenet` | Blizzard OAuth2 REST API (官方) | 🔥 高 | WoW 角色数据、Overwatch 战绩、Diablo/SC2 成就 |
| 68 | **Xbox / Game Pass** | `xbox` | Xbox Live API + Microsoft Graph | 🟡 中 | 游戏库、成就、Game Pass 目录、云游戏状态 |
| 69 | **SteamCMD** | `steam` | SteamCMD subprocess + `api.steamcmd.net` | 🔥 高 | 专用服务端：部署/更新 Steam 专用服务器、查询 App 元数据 |

### 9.2 多人游戏服务器管理（RCON & Server APIs）

> RCON（Remote CONsole）是 Valve 开放的通用游戏服务器协议，适用于 CS2、Minecraft、Factorio、Rust 等

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 70 | **Minecraft** | `minecraft` | RCON TCP + MSCS Shell API | 🔥 高 | 启停世界、白名单/OP、命令执行、备份；覆盖 Java & Bedrock |
| 71 | **Counter-Strike 2** | — | RCON TCP + CS2 Server Manager REST | 🔥 高 | 服务器控制、换图、踢人、Bot管理；2025年最高同时在线 882K |
| 72 | **Factorio** | — | factorioctl REST (localhost) + RCON | 🟡 中 | 无头服务器控制、存档管理、模组安装 |
| 73 | **Rust (game)** | — | RCON TCP（Oxide/uMod 支持） | 🟡 中 | 玩家管理、物资发放、地图刷新 |
| 74 | **Valheim** | — | RCON TCP | 🟡 中 | 世界管理、玩家命令、服务器状态 |
| 75 | **ARK: Survival Evolved / Ascended** | — | RCON TCP + REST API | 🟡 中 | 驯服/传送/物品管理、定时备份 |

### 9.3 官方游戏 REST API（Official Game APIs）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 76 | **Roblox** | `roblox` | Roblox Open Cloud API（**官方**，rbxcloud） | 🔥 高 | 资产上传、DataStore 操作、Place 发布、用户通知；官方 CLI 已有 Rust SDK |
| 77 | **Riot Games（LoL / Valorant / TFT）** | `riotgames` | Riot REST API（**官方**） | 🔥 高 | 对局历史、段位查询、召唤师信息；LoL/Valorant/TFT 三合一 |
| 78 | **HoYoverse（原神 / 星穹 / ZZZ）** | — | HoYoAPI cookie-based（hoyoverse-api Rust） | 🟡 中 | 每日签到、兑换码批量使用、角色详情、活动日历；非官方但广泛使用 |
| 79 | **Fortnite** | `epicgames` | fortnitepy Python 库 + Epic 内部 API | 🟡 中 | 玩家战绩查询、好友列表、商店物品检查 |

### 9.4 竞技 & 休闲平台（Competitive & Casual）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 80 | **Chess.com** | — | Published-Data API（**无需 Key**，只读 REST） | 🔥 高 | 玩家战绩/等级/近期对局/谜题；全球最大在线象棋平台 |
| 81 | **Lichess** | `lichess` | Open REST API（Bearer token，完全免费开源） | 🔥 高 | 对局导出、锦标赛查询、开局数据库、广播事件 |
| 82 | **Speedrun.com** | — | REST API（无需 Auth 可读公开数据） | 🟡 中 | 游戏排行榜、WR 查询、跑者档案、分类数据 |

### 9.5 流媒体 & 电竞内容（Streaming & Esports Content）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 83 | **Twitch** | `twitch` | Twitch Helix API（OAuth2，官方） | 🔥 高 | 直播管理、Clip 创建/导出、订阅查询、频道积分奖励；与 OBS 联动 |

### 9.6 CLI 功能设计参考

```
# Steam CLI 示例
cli-anything-steam library list               # 列出游戏库（JSON）
cli-anything-steam achievements --game 730    # CS2成就进度
cli-anything-steam friends online             # 在线好友列表
cli-anything-steam stats --user STEAM_ID --game 570  # Dota2 统计

# Minecraft Server CLI 示例
cli-anything-minecraft detect                 # 检测 RCON 可达性
cli-anything-minecraft rcon "whitelist add PlayerName"  # 执行RCON命令
cli-anything-minecraft backup --world world   # 打包存档
cli-anything-minecraft players list           # 在线玩家

# Riot Games CLI 示例（League of Legends）
cli-anything-riot lol summoner --name "Faker" --region kr   # 召唤师查询
cli-anything-riot lol matches --puuid XXX --count 10        # 近期对局
cli-anything-riot valorant ranked --name "TenZ#NA1"         # Valorant段位

# Chess.com CLI 示例（无需API Key）
cli-anything-chess stats --user hikaru       # 统计数据
cli-anything-chess games --user magnuscarlsen --type rapid --limit 20  # 对局列表
cli-anything-chess puzzle daily              # 今日谜题
```

---

## 九（新）、GOOGLE WORKSPACE（谷歌全家桶）

> **参考：** [googleworkspace/cli ★20.5k](https://github.com/googleworkspace/cli)（Apache-2.0）  
> 动态构建自 Google Discovery Service，含 40+ Agent Skills。我们用 Python click 封装相同 API。

| # | 服务 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 77 | **Google Drive** | `googledrive` | Drive API v3 | 🔥 高 | list/upload/download/share/mkdir — 多路上传 |
| 78 | **Gmail** | `gmail` | Gmail API v1 | 🔥 高 | send/list/get/search/reply/trash/labels |
| 79 | **Google Calendar** | `googlecalendar` | Calendar API v3 | 🔥 高 | events/create/delete/calendars，支持多日历 |
| 80 | **Google Sheets** | `googlesheets` | Sheets API v4 | 🔥 高 | read/write/append/create — 数据管道 |
| 81 | **Google Docs** | `googledocs` | Docs API v1 | 🟡 中 | create/get/append/info — 报告自动化 |
| 82 | **Google Chat** | `googlechat` | Chat API v1 | 🟡 中 | spaces/send/messages — 内部通知 Bot |

### 9.1 auth 体系（参考 gws）

```bash
# 优先级 1: 预获取 access token
export GOOGLE_WORKSPACE_TOKEN=$(gcloud auth print-access-token)

# 优先级 2: 服务账号 JSON
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json

# 优先级 3: OAuth2 用户凭证
export GWS_OAUTH_FILE=~/.config/gws/credentials.json
```

### 9.2 CLI 示例（对标 gws helper commands）

```bash
# +agenda 等价
gworkspace-cli --json calendar events --days 7

# +send 等价
gworkspace-cli --json gmail send --to team@co.com -s "Deploy done" -b "v2 is live"

# +upload 等价
gworkspace-cli --json drive upload ./report.pdf --folder FOLDER_ID

# Sheets data pipeline
gworkspace-cli --json sheets append SHEET_ID "A1" -v '["2026-03-15","42ms","pass"]'
```

---

## 十（新）、SAAS & BUSINESS APIs（SaaS 商业平台）

> **联网调研（2026-03-15）：** Google Ads Python SDK v29、TikTok Business API SDK v1.0.1、  
> Stripe Python SDK、Shopify Admin API、Salesforce REST API、HubSpot CRM API、  
> Twilio、SendGrid、Mailchimp、Vercel API、Google Play Developer API、Zendesk API  
> 新增 **20 个 CLI**，总目标扩展至 **103 个**

### 10.1 支付 & 电商（Payments & E-Commerce）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 84 | **Stripe** | `stripe` | Stripe Python SDK（官方） | 🔥 高 | 支付/订阅/退款/发票/Webhook；Agent 控制收款全流程 |
| 85 | **Shopify** | `shopify` | Shopify Admin REST + GraphQL | 🔥 高 | 商品/订单/库存/折扣/物流 |
| 86 | **PayPal** | `paypal` | PayPal REST API | 🟡 中 | 支付/退款/发票/订阅 |
| 87 | **Square** | `square` | Square Python SDK | 🟡 中 | POS/在线支付/库存/礼品卡 |

### 10.2 广告平台（Advertising APIs）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 88 | **Google Ads** | `googleads` | google-ads Python SDK v29（官方） | 🔥 高 | 广告系列/关键词/出价/报告；支持 MCC 多账户 |
| 89 | **TikTok Ads** | `tiktok` | TikTok Business API SDK v1.0.1（官方） | 🔥 高 | 广告/受众/素材/预算/数据分析 |
| 90 | **Meta Ads** | `meta` | Meta Marketing API v21 | 🔥 高 | Facebook + Instagram 广告全链路 |
| 91 | **LinkedIn Ads** | `linkedin` | LinkedIn Marketing API | 🟡 中 | 赞助内容/受众/转化追踪 |

### 10.3 社交媒体（Social Media APIs）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 92 | **X / Twitter** | `x` | X API v2（OAuth2） | 🔥 高 | 发推/搜索/DM/分析/定时发布 |
| 93 | **YouTube** | `youtube` | YouTube Data API v3 | 🔥 高 | 视频上传/元数据/字幕/评论/分析 |
| 94 | **Instagram** | `instagram` | Instagram Graph API（Meta） | 🔥 高 | 发布媒体/评论/消息/洞察数据 |
| 95 | **LinkedIn** | `linkedin` | LinkedIn REST API | 🟡 中 | 发帖/个人资料/连接/消息 |
| 96 | **Pinterest** | `pinterest` | Pinterest API v5 | 🟡 中 | Pin/Board管理/广告/分析 |

### 10.4 CRM & 项目管理（CRM & Project Mgmt）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 97 | **Salesforce** | `salesforce` | Salesforce REST + Bulk API | 🔥 高 | SOQL查询/潜客/商机/报告/Apex |
| 98 | **HubSpot** | `hubspot` | HubSpot CRM REST API | 🔥 高 | 联系人/交易/工作流/邮件序列 |
| 99 | **Jira** | `jira` | Atlassian REST API | 🔥 高 | Issue/Sprint/JQL/看板/工作流 |
| 100 | **Zendesk** | `zendesk` | Zendesk REST API | 🟡 中 | 工单/用户/宏/视图/满意度报告 |

### 10.5 通讯 & 邮件（Messaging & Email）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 101 | **Twilio** | `twilio` | Twilio Python SDK（官方） | 🔥 高 | SMS/MMS/语音通话/WhatsApp/录音 |
| 102 | **SendGrid** | `sendgrid` | SendGrid Python SDK（官方） | 🔥 高 | 事务性邮件/模板/退订/统计 |
| 103 | **Mailchimp** | `mailchimp` | Mailchimp Marketing API | 🔥 高 | 订阅者/营销活动/自动化/报告 |

### 10.6 云平台 & 部署（Cloud & Deploy）

| # | 软件 | Simple Icons slug | 接口方式 | 优先级 | 说明 |
|---|------|------------------|----------|--------|------|
| 104 | **Vercel** | `vercel` | Vercel REST API | 🔥 高 | 部署/域名/环境变量/Edge函数/分析 |
| 105 | **Google Play** | `googleplay` | Google Play Developer API | 🟡 中 | App元数据/评论回复/发布管理 |
| 106 | **Cloudflare** | `cloudflare` | Cloudflare REST API | 🔥 高 | DNS/防火墙/Workers/R2/D1 |

### 10.7 CLI 示例参考

```bash
# Stripe CLI 示例
cli-anything-stripe customers list --limit 10
cli-anything-stripe payment create --amount 1999 --currency usd --customer cus_xxx
cli-anything-stripe subscriptions cancel sub_xxx

# TikTok Ads CLI 示例  
cli-anything-tiktok campaigns list --advertiser-id 123
cli-anything-tiktok report --campaign-id 456 --start 2026-03-01 --end 2026-03-15

# Twilio CLI 示例
cli-anything-twilio sms send --to +1234567890 --body "Hello from Agent"
cli-anything-twilio calls list --limit 20

# Google Ads CLI 示例
cli-anything-gads campaigns list --customer-id 1234567890
cli-anything-gads keywords add --campaign ad_group_id --keyword "AI tools"
```

---

## 十一、发布到 Hub 的策略

### 9.1 GitHub（monorepo）

```
github.com/chatjesus/cli-anything     ← 目标仓库（新建或推送到 AgentPuter 子目录）

目录结构：
cli-anything/
├── README.md                          # 全局说明 + 链接到各工具
├── packages/
│   ├── gimp/                          # cli-anything-gimp
│   ├── blender/                       # cli-anything-blender
│   ├── ms365/                         # cli-anything-ms365
│   ├── docker/                        # cli-anything-docker
│   └── ...（每个软件一个 package）
└── scripts/
    ├── build-all.sh
    └── publish-pypi.sh
```

### 9.2 PyPI（独立包）

统一命名规范：`cli-anything-{software}`

```bash
pip install cli-anything-gimp          # 图像编辑
pip install cli-anything-blender       # 3D 渲染
pip install cli-anything-ms365         # Office 365
pip install cli-anything-docker        # 容器管理
pip install cli-anything-github        # 代码管理
```

### 9.3 agentputer.com/cli-anything

- 页面已展示 50+ 工具（13 live + 37 coming）
- 每个新 CLI 完成后：更新页面 badge `SOON → ✓` + 运行翻译脚本
- 图标已使用 Simple Icons CDN，产品 logo 与真实品牌一致

---

## 十二、构建优先顺序

```
Week 1（本地服务类）
  Ollama → ComfyUI → Docker → Chrome CDP → VS Code

Week 2（REST API 类）
  Notion → Google Docs/Sheets → Slack → Discord → Telegram

Week 3（Adobe / 创意类）
  Photoshop UXP → Illustrator UXP → Premiere Pro

Week 4（云存储 + 工具）
  Google Drive → OneDrive → Dropbox → AWS S3 → 7-Zip → yt-dlp

Week 5（发布）
  整理 monorepo → 完善 README → 批量发布 PyPI → 推送 GitHub
```

---

## 十三、每个 CLI 交付物标准

```
{software}-cli/
├── {software}_cli.py     # 主 CLI（click 框架，--json 输出）
├── setup.py              # PyPI 打包，入口 {software}-cli
├── test_{software}.py    # 无依赖快速验证测试
└── README.md             # 安装 + 命令速查表
```

**必须实现的标准命令：**
- `detect` — 检测安装状态 / 服务可达
- `version` — 版本信息
- `--json` — 机器可读输出（Agent 友好）
- 核心功能命令组（3–8 个子命令）

---

---

## 十四（新）、DATABASE & INFRASTRUCTURE（数据库与基础设施）

> **联网调研（2026-03-19）：**  
> Supabase CLI v2.81.2、Neon CLI（npm/brew）、PlanetScale CLI v0.276.0、  
> Turso CLI v1.0.17、Upstash CLI（npm）、Weaviate CLI v3.3.0、Qdrant CLI（Go）  
> 新增 **8 个 CLI**

| # | 软件 | 接口方式 | 优先级 | 说明 |
|---|------|----------|--------|------|
| 107 | **Supabase** | Supabase CLI (Go, 1,635 stars) | 🔥 高 | PostgreSQL + Auth + Edge Functions + 实时数据库 + 迁移 |
| 108 | **Neon** | Neon CLI (npm/brew) | 🔥 高 | Serverless Postgres — 分支管理、角色、连接字符串，JSON/YAML 输出 |
| 109 | **PlanetScale** | PlanetScale CLI (Go, 647 stars) | 🔥 高 | MySQL 分支、Deploy Requests、Schema 管理 |
| 110 | **Turso** | Turso CLI (Go, 289 stars) | 🟡 中 | 边缘 SQLite (libSQL)，全球复制，Groups |
| 111 | **Upstash** | Upstash CLI (npm) | 🟡 中 | Serverless Redis + Kafka，创建/管理/CRUD |
| 112 | **Weaviate** | Weaviate CLI (Python, v3.3.0) | 🟡 中 | 向量数据库，集合管理，多租户，备份/恢复 |
| 113 | **Qdrant** | Qdrant CLI (Go, 单二进制) | 🟡 中 | 向量数据库，集合/点/快照/集群，JSON/YAML/Table 输出 |
| 114 | **Redis** | Redis CLI 封装 | 🟡 中 | 内存数据存储，Keys/Streams/Pub-Sub |

### CLI 示例

```bash
# Supabase CLI
cli-anything-supabase projects list
cli-anything-supabase db push --project-ref xxx
cli-anything-supabase functions deploy my-function

# Neon CLI
cli-anything-neon projects list --output json
cli-anything-neon branches create --project-id xxx --name feature-branch
cli-anything-neon connection-string --project-id xxx

# PlanetScale CLI
cli-anything-planetscale database list
cli-anything-planetscale branch create main-db add-users-table
cli-anything-planetscale deploy-request create main-db add-users-table
```

---

## 十五（新）、MONITORING & OBSERVABILITY（监控与可观测性）

> **联网调研（2026-03-19）：**  
> Sentry CLI (AI-native)、Datadog Pup (200+ commands)、Grafana Assistant CLI、PostHog Wizard  
> 新增 **4 个 CLI**

| # | 软件 | 接口方式 | 优先级 | 说明 |
|---|------|----------|--------|------|
| 115 | **Sentry** | Sentry CLI (AI-native, cli.sentry.dev) | 🔥 高 | AI 驱动错误分析 "Seer"，自然语言命令，JSON 输出，Agent 友好 |
| 116 | **Datadog** | Datadog Pup CLI (200+ commands) | 🔥 高 | 33 个产品覆盖，OAuth2+PKCE，监控/日志/指标/安全 |
| 117 | **Grafana** | Grafana Assistant CLI (A2A API) | 🟡 中 | Agent-to-Agent API 交互，实时流式聊天，仪表板/告警 |
| 118 | **PostHog** | PostHog Wizard CLI | 🟡 中 | 自动代码插桩，支持 15+ 框架（Next.js/React/Django/Rails） |

### CLI 示例

```bash
# Sentry CLI
cli-anything-sentry issues list --project my-app --json
cli-anything-sentry explain "TypeError: Cannot read property 'map' of undefined"
cli-anything-sentry releases new v2.1.0

# Datadog CLI
cli-anything-datadog monitors list --json
cli-anything-datadog logs search "error" --from 1h --limit 50
cli-anything-datadog metrics query "avg:system.cpu.user{*}" --from 24h
```

---

## 十六（新）、PROJECT MANAGEMENT（项目管理）

> **联网调研（2026-03-19）：**  
> Linear CLI (TypeScript)、ClickUp CLI (99.3% API, 134/135 endpoints)、  
> Asana MCP (Rust)、Airtable CLI v0.1.0 (PyPI)  
> 新增 **5 个 CLI**

| # | 软件 | 接口方式 | 优先级 | 说明 |
|---|------|----------|--------|------|
| 119 | **Linear** | Linear CLI (TypeScript, JSON 输出) | 🔥 高 | Issues/Projects/Cycles/Teams，Shell Completion |
| 120 | **ClickUp** | ClickUp CLI (99.3% API 覆盖) | 🔥 高 | 134/135 端点，JSON-first，Docs API，Agent 优先设计 |
| 121 | **Asana** | Asana MCP (Rust) | 🟡 中 | 任务/项目/工作区，关系管理 |
| 122 | **Airtable** | Airtable CLI (Python, PyPI v0.1.0) | 🟡 中 | Bases/Tables/Records/Comments/Webhooks，交互式模糊搜索 |
| 123 | **Monday.com** | Monday.com GraphQL API | 🟡 中 | Boards/Items/Updates/Automations |

### CLI 示例

```bash
# Linear CLI
cli-anything-linear issues list --team ENG --state "In Progress" --json
cli-anything-linear issues create --title "Fix auth bug" --team ENG --priority urgent
cli-anything-linear cycles current --team ENG

# ClickUp CLI
cli-anything-clickup tasks list --list-id xxx --json
cli-anything-clickup tasks create --name "Deploy v2" --assignee user@co.com
cli-anything-clickup docs create --space-id xxx --name "API Reference"
```

---

## 十七（新）、DEPLOYMENT & HOSTING（部署与托管）

> **联网调研（2026-03-19）：**  
> Netlify MCP Server、Render CLI (Agent Skill)、Fly.io flyctl、Railway CLI  
> 新增 **6 个 CLI**

| # | 软件 | 接口方式 | 优先级 | 说明 |
|---|------|----------|--------|------|
| 124 | **Netlify** | Netlify MCP + CLI | 🔥 高 | Agent 直接部署到生产环境，项目/env/域名管理 |
| 125 | **Render** | Render CLI (Agent Skill 内置) | 🔥 高 | 服务/数据库管理，日志，CI/CD，Agent Skill 支持 |
| 126 | **Fly.io** | flyctl CLI (Go) | 🔥 高 | 全球边缘部署，Machines API，Volumes，Secrets |
| 127 | **Railway** | Railway CLI | 🟡 中 | 一键部署，环境管理，变量，数据库 |
| 128 | **Heroku** | Heroku CLI | 🟡 中 | Apps/Dynos/Add-ons/Config Vars/Logs |
| 129 | **DigitalOcean** | doctl CLI (Go) | 🟡 中 | Droplets/App Platform/数据库/K8s |

### CLI 示例

```bash
# Netlify CLI
cli-anything-netlify deploy --dir ./dist --prod
cli-anything-netlify sites list --json
cli-anything-netlify env set API_KEY "xxx" --context production

# Fly.io CLI
cli-anything-flyio apps list --json
cli-anything-flyio deploy --app my-app --image my-image:latest
cli-anything-flyio secrets set DATABASE_URL="postgres://..."
```

---

## 十八（新）、AI & LLM PLATFORMS（AI 与 LLM 平台）

> **联网调研（2026-03-19）：**  
> Hugging Face MCP、Replicate CLI、Groq API、Together AI、Anthropic SDK  
> 新增 **6 个 CLI**（与第七章部分重叠，此处为扩展版）

| # | 软件 | 接口方式 | 优先级 | 说明 |
|---|------|----------|--------|------|
| 130 | **OpenAI** | OpenAI Python SDK | 🔥 高 | Chat/Embeddings/Image Gen/Fine-tuning/Assistants |
| 131 | **Hugging Face** | HF MCP Server + huggingface-cli | 🔥 高 | 模型/数据集/Spaces/推理端点 |
| 132 | **Replicate** | Replicate CLI + Python SDK | 🟡 中 | 模型推理/训练/部署/Collections |
| 133 | **Groq** | Groq API | 🟡 中 | 超快推理，LLM Chat，音频转写 |
| 134 | **Together AI** | Together Python SDK | 🟡 中 | 开源模型推理/Fine-tuning/Embeddings |
| 135 | **Anthropic** | Anthropic Python SDK | 🔥 高 | Claude API — Messages/Tool Use/Batch Processing |

---

## 十九（新）、SOCIAL MEDIA & EMAIL（社交媒体与邮件）

> **联网调研（2026-03-19）：**  
> Postiz Agent (30+ platforms)、Post Bridge (9 platforms)、Resend CLI (53 commands)  
> 新增 **3 个 CLI**

| # | 软件 | 接口方式 | 优先级 | 说明 |
|---|------|----------|--------|------|
| 136 | **Postiz** | Postiz Agent CLI (npm, 30+ 平台) | 🔥 高 | TikTok/IG/YouTube/Twitch/Spotify 等一键发布，定时发布，富媒体 |
| 137 | **Post Bridge** | Post Bridge Agent Mode (9 平台) | 🟡 中 | IG/TikTok/YouTube/X/LinkedIn/Facebook/Pinterest/Threads/Bluesky |
| 138 | **Resend** | Resend CLI (TypeScript, 53 commands) | 🔥 高 | 13 个资源，域名/模板/广播/联系人管理，2026-03 新发布 |

### CLI 示例

```bash
# Postiz CLI
cli-anything-postiz post --platform tiktok,instagram --text "New release!" --media ./video.mp4
cli-anything-postiz schedule --platform twitter --text "Launch day" --at "2026-03-20T10:00Z"

# Resend CLI
cli-anything-resend emails send --from hi@co.com --to user@co.com --subject "Welcome" --html "<h1>Hi</h1>"
cli-anything-resend domains list --json
cli-anything-resend contacts list --audience-id xxx
```

---

## 二十（新）、AUTOMATION & SCHEDULING（自动化与日程）

> **联网调研（2026-03-19）：**  
> Cal.com CLI + MCP、n8n CLI (PR #26943)  
> 新增 **2 个 CLI**

| # | 软件 | 接口方式 | 优先级 | 说明 |
|---|------|----------|--------|------|
| 139 | **Cal.com** | @calcom/cli + MCP Server | 🔥 高 | 日程安排/可用性检查/预约管理，Agent 友好 |
| 140 | **n8n** | @n8n/cli (轻量客户端) | 🔥 高 | 工作流/执行/凭证/项目/标签/变量/数据表，Agent Skill 定义 |

### CLI 示例

```bash
# Cal.com CLI
cli-anything-calcom availability check --date 2026-03-20
cli-anything-calcom bookings list --status upcoming --json
cli-anything-calcom event-types list

# n8n CLI
cli-anything-n8n workflows list --active --json
cli-anything-n8n workflows execute --id 123
cli-anything-n8n credentials list --type postgres
```

---

## 更新后统计

```
已完成（Live）：         35+ CLIs
新增规划（2026-03-19）：  34 CLIs（#107–#140）
原有规划：               71 CLIs（#37–#106）
总计规划：               140 CLIs → 目标 160+（含未编号项）
```

---

*当前进度：35/140 完成 (25%)*  
*文档位置：`CLI-Anything/BATCH_PLAN.md`*  
*最近更新：2026-03-19 新增 Database/Monitoring/ProjectMgmt/Deployment/AI/Social/Automation 七大板块（34个软件，#107–#140）*  
*(全网调研数据源：GitHub trending, PyPI, npm, Sentry, Datadog, Netlify, Supabase, Neon, PlanetScale 官方文档)*
