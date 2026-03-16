# cli-anything-docker

**Docker engine CLI** — part of the [CLI-Anything](https://www.agentputer.com/cli-anything) engine.

Full container lifecycle management via Docker Python SDK with JSON-first output.

## Install

```bash
pip install cli-anything-docker
# or from source:
pip install -e .
```

Requires Docker Desktop or Docker Engine running.

## Command Groups

| Group | Commands |
|-------|----------|
| `container` | list, run, start, stop, restart, remove, logs, exec, inspect, stats |
| `image` | list, pull, build, remove, tag, inspect |
| `volume` | list, create, remove |
| `network` | list, create, remove, connect, disconnect |
| `system` | info, prune, df |

## Usage

```bash
# Check Docker status
docker-cli detect --json

# Containers
docker-cli container list --all
docker-cli container run nginx --name my-nginx --port 8080:80 --detach
docker-cli container logs my-nginx --tail 50
docker-cli container exec my-nginx ls /usr/share/nginx/html
docker-cli container stop my-nginx
docker-cli container remove my-nginx --force

# Images
docker-cli image list
docker-cli image pull python:3.12-slim
docker-cli image build . --tag myapp:latest
docker-cli image tag myapp:latest registry.io/myapp:v1.0

# Volumes
docker-cli volume list
docker-cli volume create my-data
docker-cli volume remove my-data

# Networks
docker-cli network list
docker-cli network create my-net --driver bridge
docker-cli network connect my-net my-container

# System
docker-cli system info
docker-cli system df
docker-cli system prune --yes
```

## JSON Output

```bash
$ docker-cli --json container list
{
  "containers": [
    {"id": "a1b2c3d4", "name": "my-nginx", "image": "nginx:latest", "status": "running", "ports": {...}}
  ],
  "count": 1
}
```

## Run Tests

```bash
python test_docker.py
```

---

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies software availability before use
- Predictable exit codes: 0 (success), 1 (error), 2 (usage error)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## FAQ

### How do I install cli-anything-docker?

```bash
pip install cli-anything-docker
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/docker/).

### How do I check if the software is available?

```bash
cli-anything-docker detect --json
```

Returns a JSON object with installation status and version information.
