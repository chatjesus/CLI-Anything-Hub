# cli-anything-ollama

**Ollama local LLM server CLI** — part of the [CLI-Anything](https://www.agentputer.com/cli-anything) engine.

Control Ollama from the command line or AI Agent with JSON-first output.

## Install

```bash
pip install cli-anything-ollama
# or from source:
pip install -e .
```

Requires [Ollama](https://ollama.com) to be installed and running (`ollama serve`).

## Commands

| Command | Description |
|---------|-------------|
| `detect` | Check if Ollama is running |
| `version` | Show Ollama server version |
| `list` | List downloaded models |
| `ps` | List currently loaded models |
| `show <model>` | Show model details (architecture, params, quantization) |
| `pull <model>` | Pull a model from Ollama Hub |
| `delete <model>` | Delete a local model |
| `copy <src> <dst>` | Copy/alias a model |
| `run <model> <prompt>` | Single-turn text generation |
| `chat <model>` | Multi-turn chat (ChatML) |
| `embeddings <model> <text>` | Generate embedding vector |
| `serve` | Start Ollama if not running |

## Usage

```bash
# Check status
ollama-cli detect
ollama-cli detect --json

# List local models
ollama-cli list
ollama-cli list --json

# Pull a model
ollama-cli pull llama3.2
ollama-cli pull qwen2.5:0.5b

# Single generation
ollama-cli run llama3.2 "Explain quantum computing in one sentence"

# Multi-turn chat
ollama-cli chat llama3.2 \
  --message "system:You are a concise assistant" \
  --message "user:What is 2+2?" \
  --json

# Embeddings
ollama-cli embeddings nomic-embed-text "Hello world" --json

# Custom host
ollama-cli --host http://192.168.1.100:11434 list
# or
OLLAMA_HOST=http://192.168.1.100:11434 ollama-cli list
```

## JSON Output (Agent-Friendly)

All commands support `--json` for machine-readable output:

```bash
$ ollama-cli detect --json
{
  "status": "running",
  "host": "http://localhost:11434",
  "version": "0.6.2"
}

$ ollama-cli run llama3.2 "2+2=?" --json
{
  "model": "llama3.2",
  "response": "4",
  "eval_count": 3,
  "eval_duration_ms": 142,
  "total_duration_ms": 891
}
```

## Run Tests

```bash
# Requires Ollama running with at least one model downloaded
python test_ollama.py
```

---

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies software availability before use
- Predictable exit codes: 0 (success), 1 (error), 2 (usage error)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## FAQ

### How do I install cli-anything-ollama?

```bash
pip install cli-anything-ollama
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/ollama/).

### How do I check if the software is available?

```bash
cli-anything-ollama detect --json
```

Returns a JSON object with installation status and version information.
