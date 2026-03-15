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
