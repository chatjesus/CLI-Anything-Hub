# cli-anything-kalshi

> Kalshi Prediction Market CLI — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI wrapper for Kalshi Trading API. Structured JSON output for AI agents.

## Install

```bash
pip install cli-anything-kalshi
```

## Quick Start

```bash
export KALSHI_API_KEY=your_token_here

cli-anything-kalshi schema          # discover capabilities
cli-anything-kalshi detect          # check connectivity
cli-anything-kalshi --json market list --limit 5
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
