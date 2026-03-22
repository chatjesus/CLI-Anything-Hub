# cli-anything-fred

> FRED (Federal Reserve Economic Data) CLI — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI wrapper for FRED API. Structured JSON output for AI agents.

## Install

```bash
pip install cli-anything-fred
```

## Quick Start

```bash
export FRED_API_KEY=your_key_here
cli-anything-fred schema
cli-anything-fred detect
cli-anything-fred --json series get --series-id GDP
cli-anything-fred --json series observations --series-id UNRATE --start 2020-01-01
cli-anything-fred --json series search --text "unemployment rate"
cli-anything-fred --json category list
cli-anything-fred --json releases list
```

## License

MIT — [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)
