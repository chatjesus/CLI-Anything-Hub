# cli-anything-github

**GitHub REST API CLI** — part of the [CLI-Anything](https://www.agentputer.com/cli-anything) engine.

Manage repos, issues, PRs, releases, Actions, and Gists via GitHub REST API v3.

## Install

```bash
pip install cli-anything-github
# or from source:
pip install -e .
```

Requires a GitHub Personal Access Token with appropriate scopes.

## Setup

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
# or pass per command:
github-cli --token ghp_xxx detect
```

## Command Groups

| Group | Commands |
|-------|----------|
| `repo` | list, get, create, delete, topics |
| `issue` | list, get, create, close, comment |
| `pr` | list, get, create, merge |
| `release` | list, create |
| `actions` | list-workflows, list-runs, trigger |
| `gist` | list, create |

## Usage

```bash
# Check connection
github-cli detect --json

# Repos
github-cli repo list --limit 10
github-cli repo get octocat/Hello-World --json
github-cli repo create my-new-repo --private --auto-init

# Issues
github-cli issue list owner/repo --state open --limit 20
github-cli issue create owner/repo --title "Bug: X" --body "Steps..."
github-cli issue close owner/repo 42

# PRs
github-cli pr list owner/repo
github-cli pr create owner/repo --title "feat: add feature" --head feature/x --base main

# Releases
github-cli release list owner/repo
github-cli release create owner/repo --tag v1.0.0 --name "v1.0.0"

# Actions
github-cli actions list-workflows owner/repo
github-cli actions trigger owner/repo ci.yml --ref main

# Gist
github-cli gist list
github-cli gist create --file "hello.py:print('hello')" --description "Test"
```

## JSON Output

```bash
$ github-cli --json repo list --limit 2
{
  "repos": [
    {"full_name": "user/repo", "stars": 42, "language": "Python", ...}
  ],
  "count": 2
}
```

## Run Tests

```bash
export GITHUB_TOKEN=ghp_xxxx
python test_github.py
```

---

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies software availability before use
- Predictable exit codes: 0 (success), 1 (error), 2 (usage error)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## FAQ

### How do I install cli-anything-github?

```bash
pip install cli-anything-github
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/github/).

### How do I check if the software is available?

```bash
cli-anything-github detect --json
```

Returns a JSON object with installation status and version information.
