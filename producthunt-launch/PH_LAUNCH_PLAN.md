# CLI Anything Hub — Product Hunt 发布计划

> 创建时间：2026-03-16  
> 目标：Product Hunt 首页 Top 5，开发者社区传播  
> 产品主页：https://www.agentputer.com/cli-anything/  
> GitHub：https://github.com/chatjesus/CLI-Anything-Hub

---

## 一、发布信息（PH 表单）

### 1.1 Name

```
CLI Anything
```

### 1.2 Tagline（60 字符以内）

```
100+ pre-built CLIs so AI agents can control any software
```

### 1.3 Description（500 字符以内）

```
pip install cli-anything-slack
Now your AI agent can send Slack messages.

That's the idea. We wrapped 30+ popular tools — Stripe, Docker, GIMP, Blender, Notion, GitHub — into agent-ready CLIs with a unified interface: detect, schema, call, JSON. 100+ more on the roadmap. MIT licensed.
```

> 285 字符，简洁有力，代码开头抓眼球。

### 1.4 Links

| 类型 | URL |
|------|-----|
| 主链接 | https://www.agentputer.com/cli-anything/ |
| GitHub | https://github.com/chatjesus/CLI-Anything-Hub |
| ☑ Open Source | 勾选 |

### 1.5 Launch Tags（选 3 个）

1. `Developer Tools`
2. `Artificial Intelligence`
3. `Open Source`

### 1.6 Product Status

选择 **Beta** — 降低预期，激发好奇。

---

## 二、视觉物料清单

```
producthunt-launch/
├── PH_LAUNCH_PLAN.md          ← 本文件
├── FIRST_COMMENT.md           ← 发布首评内容
├── images/
│   ├── logo-240x240.png       ← PH Thumbnail / Logo
│   ├── gallery-1-hero.png     ← 1270×760 主视觉
│   ├── gallery-2-terminal.png ← 1270×760 终端演示
│   ├── gallery-3-icons.png    ← 1270×760 工具矩阵
│   ├── gallery-4-arch.png     ← 1270×760 架构图
│   └── gallery-5-code.png     ← 1270×760 代码示例
└── generate_images.py         ← Vertex AI 图片生成脚本
```

### 2.1 Logo（240×240）

**设计方向：**
- 黑色/深灰背景 + 绿色终端光标风格
- 核心图形：`>_` 终端光标 + 开放圆环（代表 Hub / Anything）
- 极简几何，不要渐变光效、不要 3D 感、不要抽象 blob
- 参考风格：Docker logo 的简洁度 + npm logo 的几何感
- 可辨识尺寸：16px favicon 也能看清

**文件：** `images/logo-240x240.png`

### 2.2 Gallery Image 1 — Hero（1270×760）

**内容：**
- 大标题："The Software Registry Built for AI Agents"
- 副标题："pip install any tool. Agents call any software."
- 背景：深色终端风，带微妙的网格纹理
- 底部：软件 logo 图标带（Slack/Stripe/Docker/GIMP/Blender/Notion/GitHub）

**文件：** `images/gallery-1-hero.png`

### 2.3 Gallery Image 2 — Terminal Demo（1270×760）

**内容：**
- 模拟终端窗口，展示 3 步流程：
  ```
  $ pip install cli-anything-slack
  ✓ Installed cli-anything-slack 1.0.0

  $ cli-anything-slack detect
  {"status": "ok", "workspace": "MyTeam"}

  $ cli-anything-slack --json message send #general "Hello from Agent"
  {"ok": true, "ts": "1742000000.000100"}
  ```
- 干净的终端 UI，带窗口三色按钮

**文件：** `images/gallery-2-terminal.png`

### 2.4 Gallery Image 3 — Tool Matrix（1270×760）

**内容：**
- 5×6 或 6×5 网格，每格一个软件 icon + 名字
- 已就绪的用绿色勾 ✓，即将推出的用灰色
- 分类色带：Creative（紫）/ Communication（蓝）/ SaaS（橙）/ Dev（绿）

**文件：** `images/gallery-3-icons.png`

### 2.5 Gallery Image 4 — Architecture（1270×760）

**内容：**
- 流程图：AI Agent → CLI Anything Hub → [各软件]
- 强调统一接口：`detect → schema → call → JSON`
- 极简线条风格，非 3D 非拟物

**文件：** `images/gallery-4-arch.png`

### 2.6 Gallery Image 5 — Code Example（1270×760）

**内容：**
- 左侧：3 个不同 CLI 的代码片段（Slack / Stripe / Docker）
- 右侧：对应的 JSON 输出
- 突出"一个标准接口控制一切"

**文件：** `images/gallery-5-code.png`

---

## 三、First Comment（发布首评）

见 `FIRST_COMMENT.md` 文件。

---

## 四、发布时间策略

| 要素 | 建议 |
|------|------|
| **日期** | 周二 ~ 周四（避免周一/周五） |
| **时间** | 太平洋时间 00:01（北京时间 15:01） |
| **避开** | 查看 producthunt.com/upcoming 避免和大产品撞车 |

### 推荐发布日：2026 年 3 月 17 日（周二）或 3 月 18 日（周三）

---

## 五、发布前 Checklist

### T-7（发布前一周）

- [ ] PH Upcoming 页面上线，收集 "Notify me"
- [ ] 所有 Gallery 图片完成
- [ ] Logo 定稿
- [ ] GitHub Repo public，README 完善
- [ ] 在 X/Twitter 发 3 条预告推文

### T-3（发布前三天）

- [ ] agentputer.com/cli-anything 网站检查
- [ ] 核心 CLI 发布到 PyPI（至少 slack / stripe / docker）
- [ ] 邀请 10+ 开发者朋友准备 upvote + 真实评论
- [ ] First Comment 终稿审核
- [ ] 准备 Reddit / HN / Discord 同步帖

### T-0（发布当天）

- [ ] PST 00:01 准时发布
- [ ] 立即在 X/Twitter 发帖 + pin
- [ ] Reddit: r/programming, r/artificial, r/commandline
- [ ] Hacker News: Show HN 帖
- [ ] Discord: AI 相关社区
- [ ] 前 4 小时：每条 PH 评论都回复

### T+1（发布后一天）

- [ ] 持续回复所有评论
- [ ] 如进 Top 5，发感谢推文 + 二次传播
- [ ] 收集反馈，更新 roadmap
- [ ] 在 README 添加 PH badge

---

## 六、社交媒体同步推广

### X / Twitter 发布帖模板

```
🚀 CLI Anything is live on Product Hunt!

Your AI agent can now pip install 30+ tools and directly control 
Slack, Stripe, Docker, GIMP, Blender, and more.

One interface. Structured JSON. Zero friction.

▸ Product Hunt: [link]
▸ GitHub: github.com/chatjesus/CLI-Anything-Hub
▸ MIT open source

#AIAgents #DevTools #OpenSource #CLI
```

### Reddit 帖子模板

**标题：** `Show r/programming: CLI Anything — 30+ pip-installable CLIs that let AI agents control any software`

**正文：** 保持技术性，展示 3 行代码示例，说明为什么 CLI 是 agent 的最佳接口。

### Hacker News

**标题：** `Show HN: CLI Anything Hub – 30+ agent-ready CLI wrappers for popular software`

---

## 七、成功指标

| 指标 | 目标 |
|------|------|
| PH 排名 | Top 5 |
| PH Upvotes | 300+ |
| GitHub Stars（当天） | +200 |
| pip install（当周） | +500 |
| 评论数 | 30+ 有价值评论 |

---

*文件位置：`CLI-Anything/producthunt-launch/PH_LAUNCH_PLAN.md`*
