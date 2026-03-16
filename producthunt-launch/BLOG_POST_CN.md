> **注意：** 本文由 Vertex AI Gemini 2.0 Flash 从英文原文自动翻译。[查看英文原文](./BLOG_POST.md)

---

# CLI Anything：你的 AI 智能体一直缺失的执行层

> *你的智能体很聪明，但就是什么都做不了。*

你构建了一个 AI 智能体，它推理能力出色，策略规划周密，响应精准。然后你让它发送一条 Slack 消息。它给你写了一个 Python 脚本。你让它触发一个 Docker 构建。它解释了 Dockerfile 的语法。你让它创建一个 Jira 工单。它描述了 REST API 端点。

智能是有的，但执行力不足。

这是智能体时代的隐藏瓶颈 —— 而且这并非模型的问题。2025 年的一项生产调查发现，**73% 的企业 AI 智能体部署在第一年内未能达到可靠性预期**。失败的原因不是缺乏智能，而是缺乏基础设施。

正如 HackerNoon 的分析所说：“*智能体工作框架（Agent Harness）工程 —— 上下文管理、工具选择、错误恢复和状态持久化的设计 —— 是智能体可靠性的主要决定因素，而不是模型能力。*”

OpenAI 联合创始人 Andrej Karpathy 在 2025 年引发了一场辩论，他称当前的 AI 智能体为“垃圾”，并警告业界“步子迈得太大了”。他的诊断不是关于模型，而是关于底层管道。

CLI Anything 就是这个管道。

---

## 智能体调用工具的三种方式 —— 以及它们为何都存在不足

在讨论解决方案之前，让我们先诚实地审视一下现状。

### 选项 1：原始 API / SDK 调用

每个集成都是手工编写的。智能体必须了解 API 模式，管理身份验证，解析不一致的响应格式，并为每个服务处理不同的错误。这对于一两个集成来说还可以，但无法扩展到五十个。

### 选项 2：MCP (Model Context Protocol，模型上下文协议)

MCP 是 Anthropic 对工具标准化给出的答案，现在由 Linux 基金会的 AAIF 管理，拥有令人印象深刻的 9700 万 SDK 下载量和 10,000 多个已发布的服务器。从理论上讲，它正是智能体所需要的。

但在实践中，存在一个没有人充分讨论的关键问题：**MCP 是一个上下文消耗大户**。

Jannik Reinhard 是一位花费数月时间构建真正企业智能体解决方案的开发者，他详细记录了这一点：

> *“一个典型的 MCP 服务器将其整个模式转储到智能体的上下文窗口中 —— 工具定义、参数描述、身份验证流程、状态管理，整个包。”*

仅 GitHub MCP 服务器就消耗了 **~55,000 个 tokens**，而智能体还没有做任何实际工作。这大约是 GPT-4o 整个上下文窗口的一半 —— 在第一个问题之前就消耗掉了。连接一个典型的企业堆栈（GitHub + 数据库 + Jira + Microsoft Graph），你将看到 **150,000+ 个 tokens 的模式开销**。

token 成本不仅仅是一个效率问题，它还是一个推理质量问题。按照 Claude 每百万 tokens 3 美元的价格计算，这种开销转化为**每次请求 0.27 美元，或者大规模部署时每月 81,000 美元**。

Reinhard 在一个真实的合规性自动化任务上进行了直接比较：

| 方法 | Token 成本 |
|----------|-----------|
| MCP (Microsoft Graph) | 145,000 tokens |
| CLI 等效方法 | 4,150 tokens |
| **差异** | **减少 35 倍** |

CLI 方法留下了 95% 的上下文窗口用于实际推理。MCP 方法将工作流程分成多个会话，只是为了保持在限制范围内。

### 选项 3：CLI 包装器 —— 缺失的中间层

这里有一个被低估的事实：LLM 是天生的 CLI 语言使用者。它们接受了数十亿行终端交互的训练 —— Stack Overflow 答案、GitHub 仓库、文档、教程。`git`、`docker`、`curl`、`kubectl` 都是深度学习的模式。一个 CLI 命令加上它的 `--help` 输出大约花费 **200 个 tokens** —— 比 MCP 初始化提高了 50 倍。

一位开发者用一个 200-token 的 CLI 技能定义替换了一个消耗 5,000 多个 tokens 的 LangSmith MCP 服务器：**上下文开销减少 95%，功能零损失**。

但从历史上看，CLI 包装器有其自身的问题：没有标准接口。每个工具都有不同的命令、不同的输出格式、不同的错误代码。智能体无法依赖跨工具的一致行为。

**这正是 CLI Anything 填补的空白。**

---

## 介绍 CLI Anything Hub

CLI Anything Hub 是一个精选的、社区驱动的集合，包含 **130 多个预构建的、智能体就绪的 CLI 包装器**，用于世界上最流行的软件 —— 围绕一个标准化的 4 命令接口构建。

Hub 中的每个 CLI 都实现了相同的约定。无需文档：

```bash
# 1. DISCOVER — 智能体自我发现能力，无需身份验证
cli-anything-slack schema
# → { "name": "cli-anything-slack", "commands": [...], "token_env": "SLACK_BOT_TOKEN" }

# 2. CHECK — 幂等连接性测试，零副作用
cli-anything-slack detect
# → { "status": "ok", "workspace": "MyTeam", "bot": "AgentBot" }

# 3. CALL — 结构化 JSON 输出，智能体可解析
cli-anything-slack --json message send #general "Deploy complete"
# → { "ok": true, "ts": "1742000000.000100" }

# 4. VERSION — 兼容性跟踪
cli-anything-slack version
# → cli-anything-slack 1.0.0
```

从零到工作只需 30 秒：

```bash
pip install cli-anything-slack
export SLACK_BOT_TOKEN=xoxb-...
cli-anything-slack --json message send #ops "Hello from Agent"
```

目前，有 30 多个 CLI 处于活动状态并可安装，并由 **1,508 个自动化测试**支持。路线图涵盖了创意与媒体、云 SaaS、开发者工具、游戏、生活服务等领域的 130 多个工具。

---

## 四层架构：CLI Anything 的位置

最常见的问题是：“*这是否与 MCP 竞争？与直接 API 调用竞争？*”

答案是否定的。CLI Anything 是一个执行层 —— 它在智能体堆栈中有一个特定的、明确定义的位置：

```
┌──────────────────────────────────────────────────────────┐
│  Layer 4: Skills / SKILL.md                               │
│  Intent routing — "which tool, which command, when"       │
│  意图路由 —— “哪个工具，哪个命令，何时”                                   │
├──────────────────────────────────────────────────────────┤
│  Layer 3: MCP Bridge (optional)                           │
│  Protocol layer — expose CLI Anything as MCP tools        │
│  协议层 —— 将 CLI Anything 作为 MCP 工具公开                               │
│  Semantic governance + lean execution                     │
│  语义治理 + 精益执行                                         │
├──────────────────────────────────────────────────────────┤
│  Layer 2: CLI Anything Hub                                │
│  Standardized execution — schema / detect / call --json   │
│  标准化执行 —— schema / detect / call --json                               │
│  30+ Live · 130+ planned · pip install · framework-free   │
│  30+ 活跃 · 130+ 计划 · pip install · 无框架                               │
├──────────────────────────────────────────────────────────┤
│  Layer 1: Real APIs & SDKs                                │
│  Actual communication — Slack / Stripe / Docker / etc.    │
│  实际通信 —— Slack / Stripe / Docker / 等                                 │
└──────────────────────────────────────────────────────────┘
```

**Layer 1 — 真实 API：** 实际的 SDK 和 REST 端点。CLI Anything 包装了这些，因此智能体永远不必处理原始身份验证、不一致的响应格式或特定于服务的错误处理。

**Layer 2 — CLI Anything（核心）：** 标准化的执行接口。`schema` 为智能体提供了一个完整的功能图 —— 它们不需要任何外部文档。`detect` 提供了一个幂等的健康检查，可以随时安全地调用。`--json` 确保每个响应都是结构化的，并且智能体可以解析，无需后处理。

**Layer 3 — MCP Bridge（可选）：** CLI Anything CLI *可以* 被包装为 MCP 工具。这并不是冲突 —— 而是两全其美。MCP 在企业环境中提供治理、审计跟踪和语义发现。CLI Anything 在底层提供精益执行层，避免了 MCP 的 token 开销问题。HackerNoon 对有效智能体工作框架的分析建议采用这种“渐进式披露”模式：*只在需要时向模型展示它们需要的东西。*

**Layer 4 — Skills / SKILL.md：** 意图路由层。`SKILL.md` 文件告诉智能体 *何时* 使用工具，*使用哪个特定命令*，以及 *传递什么上下文*。CLI Anything 路线图包括每个 CLI 自动生成的 `SKILL.md` —— 使每个工具都可以在 Cursor、Codex、VS Code、Gemini CLI 以及任何支持 AAIF Agent Skills Standard 的智能体中完全即插即用。

**完整的智能体控制堆栈：** *技能路由 → (MCP 桥接) → CLI 执行 → API 响应 → JSON 返回给智能体。*

---

## 真实演练：智能体自动化部署

让我们具体说明一下。你的智能体收到一个任务：“*部署新版本，通知团队，并创建一个 Jira 工单用于发布跟踪。*”

**步骤 1：** 智能体读取 Skills 层。它将 `cli-anything-vercel`、`cli-anything-slack` 和 `cli-anything-jira` 识别为正确的工具。

**步骤 2：** 智能体对每个工具调用 `schema` —— 3 个轻量级 JSON 响应，总共大约 600 个 tokens。将其与加载三个 MCP 服务器进行比较：在执行任何操作之前，大约需要 90,000 个 tokens 的模式开销。

**步骤 3：** 按顺序执行：

```bash
# Deploy
cli-anything-vercel --json deploy --project my-app
# → { "url": "https://my-app-xyz.vercel.app", "state": "READY" }

# Notify team
cli-anything-slack --json message send #releases "v2.1.0 live → https://my-app-xyz.vercel.app"
# → { "ok": true, "ts": "1742000000.000100" }

# Track release
cli-anything-jira --json issue create --project REL --summary "Release v2.1.0" --type Task
# → { "id": "REL-847", "status": "To Do", "url": "..." }
```

**结果：** 三个工具。三个 pip 安装。一个标准化的接口。零自定义集成代码。比 MCP 等效方法少 35 倍的 tokens。

这并不是一个虚构的演示。Vercel 自己的工程团队记录了一个类似的发现：当他们将智能体的工具从 15 个减少到 2 个专注的、定义明确的工具时，准确率从 **80% 跃升到 100%**，token 使用量下降 **37%**，速度提高了 **3.5 倍**。CLI Anything 的设计理念 —— 精益、专注、可组合 —— 正好反映了这一发现。

---

## Hub 中有什么

**当前活跃（30 多个 CLI）：**

| 类别 | 工具 |
|----------|-------|
| 创意与媒体 | GIMP, Blender, Inkscape, Audacity, OBS Studio, Kdenlive, Shotcut, Draw.io |
| 通信 | Slack, Discord, Telegram, Feishu/Lark（飞书/Lark） |
| 云 SaaS | Stripe, Shopify, HubSpot, Salesforce, Jira, Cloudflare, Vercel, Twilio |
| 开发者工具 | Docker, GitHub, Notion, Ollama |
| 办公与效率 | MS 365, LibreOffice, Google Workspace (Drive + Gmail + Calendar + Sheets + Docs + Chat) |

**路线图：**
- **游戏：** Steam, Roblox, Riot Games, Twitch, Minecraft RCON
- **生活与本地：** DoorDash, Meituan（美团）, Uber Eats, Airbnb, Yelp
- **创意 SaaS：** Figma, Canva, Adobe Photoshop (UXP)
- **广告：** Google Ads, TikTok Ads, Meta Ads

---

## Hub 是开放的 —— 构建你自己的 CLI

CLI Anything 采用 MIT 许可。Hub 中的每个 CLI 都遵循相同的最小约定，任何 Python 开发者都可以在一个下午构建一个。

最小可行实现：

```python
import click, json

@click.group()
def cli(): pass

@cli.command()
def schema():
    """Output capability map. No auth needed."""
    click.echo(json.dumps({
        "name": "cli-anything-mytool",
        "version": "1.0.0",
        "requires_token": True,
        "token_env": "MYTOOL_API_KEY",
        "commands": [{"cmd": "do-thing", "desc": "Does the thing"}],
        "json_flag": "--json"
    }))

@cli.command()
def detect():
    """Connectivity check. No side effects."""
    click.echo(json.dumps({"status": "ok"}))
```

这就是核心。添加你的工具特定命令，提交一个 PR 或 GitHub Issue，你的工具就可以供世界上每个使用 CLI Anything 的智能体使用。

---

## 为何现在很重要

2025-2026 年是 AI 智能体从令人印象深刻的演示转向可靠的生产系统的窗口。APEX-Agents 基准测试在真实的专业任务（银行、咨询、法律）上测试了前沿模型，并发现了一个令人清醒的结果：即使是最好的模型也只达到了 **24% 的 pass@1 准确率**。主要的失败模式不是知识差距，而是编排失败。

正如智能体工作框架研究社区所达成共识的：“*超过最小能力阈值后，工作框架工程比更换模型带来更好的回报。*” Anthropic 通过重新设计脚手架，使用 *相同* 的模型实现了 36 点的基准改进。

CLI Anything 就是脚手架。它直接解决了编排层 —— 不是通过新的 AI 模型，不是通过新的推理架构，而是通过标准化智能体连接到软件的这种不性感、不光鲜的工作。

添加到 Hub 的每个 CLI 都是世界上每个智能体都可以使用的更多功能。这就是飞轮效应。

正如 Jannik Reinhard 所说，AI 智能体工具的未来，“*不是关于最复杂的协议，而是关于模型和行动之间最精益的路径。*”

CLI Anything 就是这条路径。

---

## 开始使用

**安装任何 CLI 并运行它：**
```bash
pip install cli-anything-slack
cli-anything-slack schema   # see what it can do
cli-anything-slack detect   # verify connectivity
```

**浏览完整目录：** [agentputer.com/cli-anything](https://agentputer.com/cli-anything/)

**Star & fork Hub：** [github.com/chatjesus/CLI-Anything-Hub](https://github.com/chatjesus/CLI-Anything-Hub)

**提交你自己的 CLI：** [Open a GitHub Issue](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool-name)

**在 Product Hunt 上投票：** [producthunt.com/posts/cli-anything](https://www.producthunt.com/posts/cli-anything)

---

*CLI Anything Hub 是开源的，采用 MIT 许可，专为智能体时代而构建。*
*pip install 任何工具 · 智能体调用任何软件 · Fork 并扩展*

---

### 参考

1. HackerNoon — *Why AI Agent Reliability Depends More on the Harness Than the Model* (2025)
2. Jannik Reinhard — *Why CLI Tools Are Beating MCP for AI Agents* (Feb 2026) — [jannikreinhard.com](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/)
3. buildmvpfast.com — *MCP Token Cost Problem: Why AI Teams Switch to CLI for Agents* (2026)
4. AAIF / Linux Foundation — *Agentic AI Foundation Standardization Report* (Dec 2025)
5. Dev.to — *I Replaced My LangSmith MCP Server with a 200-Token CLI Skill* (2026)
6. Dev.to — *Agent Harness Engineering: What 8 Months in Production Taught Me* (2025)
7. APEX-Agents Benchmark — *Professional Task Performance on Frontier Models* (2025)
8. Andrej Karpathy — Public statements on agentic AI readiness (2025)
