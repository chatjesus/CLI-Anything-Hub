# cli-anything-nansen

> Nansen Analytics CLI — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI wrapper for Nansen on-chain analytics. Structured JSON output for AI agents.

## Install
```bash
pip install cli-anything-nansen
```

## Quick Start
```bash
export NANSEN_API_KEY=your_key
cli-anything-nansen schema
cli-anything-nansen detect
cli-anything-nansen --json smart-money --chain ethereum --timeframe 24h
cli-anything-nansen --json token analysis --address 0x... --chain ethereum
cli-anything-nansen --json wallet profile --address 0x...
```

## License
MIT
