# cli-anything-alphavantage

> Alpha Vantage Financial Data CLI — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI wrapper for Alpha Vantage API. Structured JSON output for AI agents.

## Install

```bash
pip install cli-anything-alphavantage
```

## Quick Start

```bash
export ALPHA_VANTAGE_API_KEY=your_key_here

cli-anything-alphavantage schema          # discover capabilities
cli-anything-alphavantage detect          # check connectivity
cli-anything-alphavantage --json quote --symbol AAPL
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
