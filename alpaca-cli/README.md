# cli-anything-alpaca

> Alpaca Trading API CLI — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI wrapper for Alpaca Trading API. Structured JSON output for AI agents.

Supports Paper Trading (default) and Live Trading (`--live` flag).

## Install

```bash
pip install cli-anything-alpaca
```

## Quick Start

```bash
export ALPACA_API_KEY=your_key_here
export ALPACA_SECRET_KEY=your_secret_here
cli-anything-alpaca schema
cli-anything-alpaca detect
cli-anything-alpaca --json account
cli-anything-alpaca --json positions list
cli-anything-alpaca --json bars --symbol AAPL --timeframe 1Day --limit 10
cli-anything-alpaca --json order submit --symbol AAPL --qty 1 --side buy --type market
```

## License

MIT — [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)
