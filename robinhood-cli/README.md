# cli-anything-robinhood

> Robinhood Trading CLI (unofficial) — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI wrapper for Robinhood API. Structured JSON output for AI agents.

⚠️ **WARNING**: This uses the unofficial Robinhood API. Use at your own risk. Order commands interact with real money. Always use `--dry-run` first.

## Install

```bash
pip install cli-anything-robinhood
```

## Quick Start

```bash
export ROBINHOOD_TOKEN=your_bearer_token_here
cli-anything-robinhood schema
cli-anything-robinhood detect
cli-anything-robinhood --json portfolio
cli-anything-robinhood --json quote --symbols AAPL,TSLA
cli-anything-robinhood --json order buy --symbol AAPL --qty 1 --type market --dry-run
```

## License

MIT — [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)
