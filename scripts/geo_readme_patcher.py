#!/usr/bin/env python3
"""
geo_readme_patcher.py — Append "For AI Agents" + FAQ sections to all CLI README.md files.

Skips files that already contain these sections.

Usage: python scripts/geo_readme_patcher.py [--dry-run]
"""

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

SLUG_MAP = {
    "slack": "slack", "discord": "discord", "telegram": "telegram",
    "feishu": "feishu", "stripe": "stripe", "shopify": "shopify",
    "salesforce": "salesforce", "hubspot": "hubspot", "jira": "jira",
    "vercel": "vercel", "cloudflare": "cloudflare", "twilio": "twilio",
    "docker": "docker", "github": "github", "notion": "notion",
    "ollama": "ollama", "ms365": "ms365", "gworkspace": "gworkspace",
    "gimp": "gimp", "blender": "blender", "inkscape": "inkscape",
    "audacity": "audacity", "libreoffice": "libreoffice",
    "obs_studio": "obs-studio", "obs-studio": "obs-studio",
    "kdenlive": "kdenlive", "shotcut": "shotcut",
    "drawio": "drawio", "zoom": "zoom", "anygen": "anygen",
}


def detect_slug(filepath):
    """Detect the CLI slug from file path."""
    parts = str(filepath).replace("\\", "/").lower()
    for key, slug in SLUG_MAP.items():
        if f"/{key}/" in parts or f"/{key}-cli/" in parts:
            return slug
    # Fallback: extract from directory name
    for part in filepath.parts:
        clean = part.replace("-cli", "")
        if clean in SLUG_MAP:
            return SLUG_MAP[clean]
    return None


def build_agent_section(slug):
    pkg = f"cli-anything-{slug}"
    return f"""
---

## For AI Agents

This tool is designed for AI agents (Claude, ChatGPT, Copilot, Cursor, Codex).

- All commands support `--json` for structured machine-readable output
- `detect` command verifies software availability before use
- Predictable exit codes: 0 (success), 1 (error), 2 (usage error)
- Part of [CLI-Anything Hub](https://www.agentputer.com/cli-anything/) — 130+ agent-ready CLIs

## FAQ

### How do I install {pkg}?

```bash
pip install {pkg}
```

Requires Python 3.9+.

### Can AI agents use this tool?

Yes. All commands support the `--json` flag for structured output that LLMs can parse directly. This tool is listed on the [CLI-Anything Hub](https://www.agentputer.com/cli-anything/{slug}/).

### How do I check if the software is available?

```bash
{pkg} detect --json
```

Returns a JSON object with installation status and version information.
"""


def find_all_readmes():
    files = []
    # Hub CLIs
    for d in sorted(BASE.glob("*-cli")):
        readme = d / "README.md"
        if readme.exists():
            files.append(readme)
    # Agent-harness CLIs
    for d in sorted(BASE.iterdir()):
        ah = d / "agent-harness"
        if ah.is_dir():
            for readme in ah.rglob("README.md"):
                if ".pytest_cache" in str(readme) or "__pycache__" in str(readme):
                    continue
                files.append(readme)
    return files


def patch_readme(filepath, dry_run=False):
    content = filepath.read_text(encoding="utf-8")
    slug = detect_slug(filepath)

    if not slug:
        return False, "Could not detect slug"

    if "## For AI Agents" in content:
        return False, "Already has 'For AI Agents' section"

    section = build_agent_section(slug)
    new_content = content.rstrip() + "\n" + section

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")

    return True, f"Appended AI Agents section ({slug})"


def main():
    dry_run = "--dry-run" in sys.argv
    mode_label = "DRY RUN" if dry_run else "LIVE"
    print(f"=== GEO README Patcher ({mode_label}) ===\n")

    files = find_all_readmes()
    print(f"Found {len(files)} README.md files\n")

    patched = 0
    skipped = 0

    for f in files:
        success, msg = patch_readme(f, dry_run=dry_run)
        if success:
            patched += 1
            print(f"  [PATCH] {f.relative_to(BASE)} — {msg}")
        else:
            skipped += 1
            print(f"  [SKIP]  {f.relative_to(BASE)} — {msg}")

    print(f"\nDone: {patched} patched, {skipped} skipped")


if __name__ == "__main__":
    main()
