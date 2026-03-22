# Bloomberg CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

Bloomberg 金融数据 CLI，支持 BLPAPI（本地 Terminal）和 HTTP MCP 双模式。

## Install

```bash
pip install -e ./bloomberg-cli
```

## Setup

**模式 1: Bloomberg Terminal (BLPAPI)**

```bash
pip install blpapi
# 需要本地运行 Bloomberg Terminal
```

**模式 2: HTTP MCP**

```bash
export BLOOMBERG_API_KEY=your_key
export BLOOMBERG_MCP_URL=https://your-mcp-endpoint.com/api/v1  # 可选
```

## Quick Start

```bash
# 检测连接
cli-anything-bloomberg detect

# 查看能力
cli-anything-bloomberg schema

# 参考数据
cli-anything-bloomberg --json reference --securities "AAPL US Equity" --fields PX_LAST,PE_RATIO

# 历史数据
cli-anything-bloomberg --json historical --security "AAPL US Equity" --fields PX_LAST --start 2024-01-01

# 实时行情
cli-anything-bloomberg --json market-data --securities "AAPL US Equity" --securities "MSFT US Equity"

# 证券搜索
cli-anything-bloomberg --json search --query "Apple"

# 字段搜索
cli-anything-bloomberg --json field-search --query "price"
```

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies connectivity before use
- `schema` command returns full command schema (no auth needed)
- Dual mode: BLPAPI (local Terminal) or HTTP MCP (remote)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## License

MIT
