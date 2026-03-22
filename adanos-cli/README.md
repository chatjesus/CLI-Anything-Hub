# Adanos CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

Adanos 多源情绪分析平台 CLI，聚合 News + Polymarket + X/Twitter + Reddit 情绪数据。

## Install

```bash
pip install -e ./adanos-cli
```

## Setup

```bash
export ADANOS_API_KEY=your_key
```

## Quick Start

```bash
# 检测连接
cli-anything-adanos detect

# 查看能力
cli-anything-adanos schema

# 情绪分析
cli-anything-adanos --json sentiment --query AAPL --sources news,x,reddit

# 每日简报
cli-anything-adanos --json briefing daily

# 每周摘要
cli-anything-adanos --json briefing weekly

# 监控列表
cli-anything-adanos --json watchlist list
cli-anything-adanos watchlist add --name "Tech" --ticker AAPL

# 告警
cli-anything-adanos --json alerts list
cli-anything-adanos alerts create --ticker AAPL --threshold 0.8 --direction above

# 预测市场关联
cli-anything-adanos --json predict --ticker AAPL --market polymarket
```

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies API connectivity before use
- `schema` command returns full command schema (no auth needed)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## License

MIT
