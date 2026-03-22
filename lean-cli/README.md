# Lean CLI

> Part of [CLI Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub) — the open hub for 100+ agent-ready CLIs.

QuantConnect / Lean 量化平台 CLI，管理项目、回测、实盘交易和数据。

## Install

```bash
pip install -e ./lean-cli
```

## Setup

```bash
export QUANTCONNECT_USER_ID=your_user_id
export QUANTCONNECT_API_KEY=your_api_key
```

获取凭证: https://www.quantconnect.com/account

## Quick Start

```bash
# 检测凭证
cli-anything-lean detect

# 查看能力
cli-anything-lean schema

# 项目管理
cli-anything-lean --json project list
cli-anything-lean project create --name "MyAlgo" --language python
cli-anything-lean --json project get --project-id 12345

# 回测
cli-anything-lean backtest run --project-id 12345
cli-anything-lean --json backtest list --project-id 12345
cli-anything-lean --json backtest results --project-id 12345 --backtest-id abc123

# 实盘
cli-anything-lean --json live list
cli-anything-lean live start --project-id 12345 --brokerage alpaca
cli-anything-lean live stop --project-id 12345

# 数据
cli-anything-lean --json data list
```

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies API credentials before use
- `schema` command returns full command schema (no auth needed)
- Basic Auth with User ID + API Key
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## License

MIT
