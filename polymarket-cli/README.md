# cli-anything-polymarket

> Polymarket Prediction Market CLI — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI wrapper for Polymarket CLOB API. Structured JSON output for AI agents.

## Install

```bash
pip install cli-anything-polymarket
```

## Quick Start

```bash
export POLYMARKET_API_KEY=your_key_here

cli-anything-polymarket schema          # discover capabilities
cli-anything-polymarket detect          # check connectivity
cli-anything-polymarket --json market list --limit 5
```

## Agent-Native Standard

| Command | Description |
|---------|-------------|
| `schema` | JSON capability map (no auth needed) |
| `detect` | Connectivity check |
| `version` | Version info |
| `--json` | Structured JSON output on all commands |

## License

MIT — [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)
