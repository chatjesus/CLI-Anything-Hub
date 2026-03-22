# cli-anything-wooo

> All-in-One Crypto CLI — Part of [CLI-Anything Hub](https://github.com/chatjesus/CLI-Anything-Hub)

Agent-native CLI aggregating CEX (OKX/Binance/Bybit) + DEX (Uniswap/Curve/Jupiter) + DeFi (Aave/Lido/Compound) + Hyperliquid. Structured JSON output for AI agents.

## Install
```bash
pip install cli-anything-wooo
```

## Quick Start
```bash
# Set exchange keys
export OKX_API_KEY=your_key
export BINANCE_API_KEY=your_key
export BYBIT_API_KEY=your_key

# Or use config file
mkdir -p ~/.wooo && cat > ~/.wooo/config.json << 'EOF'
{
  "exchanges": {
    "okx": { "api_key": "xxx", "api_secret": "xxx", "passphrase": "xxx" },
    "binance": { "api_key": "xxx", "api_secret": "xxx" },
    "bybit": { "api_key": "xxx", "api_secret": "xxx" }
  },
  "hyperliquid": { "wallet": "0x..." }
}
EOF

cli-anything-wooo schema
cli-anything-wooo detect
cli-anything-wooo --json cex balance --exchange okx
cli-anything-wooo --json dex quote --dex uniswap --from ETH --to USDC --amount 1.0
cli-anything-wooo --json defi positions --protocol aave
cli-anything-wooo --json hyperliquid positions
```

## License
MIT
