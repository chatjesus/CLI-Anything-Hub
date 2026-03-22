# cli-anything-dune

> Dune Analytics CLI — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI wrapper for Dune Analytics. Structured JSON output for AI agents.

## Install
```bash
pip install cli-anything-dune
```

## Quick Start
```bash
export DUNE_API_KEY=your_key
cli-anything-dune schema
cli-anything-dune detect
cli-anything-dune --json query execute --query-id 1234
cli-anything-dune --json query results --execution-id abc123
cli-anything-dune --json dataset search --keyword "uniswap" --chain ethereum
```

## License
MIT
