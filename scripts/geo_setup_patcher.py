#!/usr/bin/env python3
"""
geo_setup_patcher.py — Batch-patch all CLI-Anything setup.py files for GEO optimization.

Adds/updates: keywords, project_urls, AI classifiers, enhanced descriptions.
Generates a diff report for human review.

Usage: python scripts/geo_setup_patcher.py [--dry-run]
"""

import os
import re
import sys
import difflib
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

TOOL_META = {
    "slack": {"category": "communication", "topic": "Team Messaging"},
    "discord": {"category": "communication", "topic": "Community Bots"},
    "telegram": {"category": "communication", "topic": "Bot Messaging"},
    "feishu": {"category": "communication", "topic": "Enterprise Messaging"},
    "stripe": {"category": "fintech", "topic": "Payment Processing"},
    "shopify": {"category": "ecommerce", "topic": "E-Commerce Management"},
    "salesforce": {"category": "crm", "topic": "CRM Automation"},
    "hubspot": {"category": "crm", "topic": "CRM and Marketing"},
    "jira": {"category": "project-management", "topic": "Issue Tracking"},
    "vercel": {"category": "cloud", "topic": "Cloud Deployment"},
    "cloudflare": {"category": "cloud", "topic": "DNS and Edge Computing"},
    "twilio": {"category": "communication", "topic": "SMS and Voice"},
    "docker": {"category": "devops", "topic": "Container Management"},
    "github": {"category": "development", "topic": "Code Management"},
    "notion": {"category": "productivity", "topic": "Knowledge Management"},
    "ollama": {"category": "ai", "topic": "Local LLM Management"},
    "ms365": {"category": "office", "topic": "Office Automation"},
    "gworkspace": {"category": "office", "topic": "Google Workspace"},
    "gimp": {"category": "image", "topic": "Image Editing"},
    "blender": {"category": "3d", "topic": "3D Rendering"},
    "inkscape": {"category": "image", "topic": "Vector Graphics"},
    "audacity": {"category": "audio", "topic": "Audio Editing"},
    "libreoffice": {"category": "office", "topic": "Document Conversion"},
    "obs-studio": {"category": "video", "topic": "Live Streaming"},
    "kdenlive": {"category": "video", "topic": "Video Editing"},
    "shotcut": {"category": "video", "topic": "Video Editing"},
    "drawio": {"category": "diagrams", "topic": "Diagram Creation"},
    "zoom": {"category": "communication", "topic": "Meeting Management"},
    "anygen": {"category": "ai", "topic": "Content Generation"},
}

HUB_URL = "https://www.agentputer.com/cli-anything"
GITHUB_URL = "https://github.com/chatjesus/CLI-Anything-Hub"

AI_CLASSIFIER = "Topic :: Scientific/Engineering :: Artificial Intelligence"


def extract_pkg_name(content):
    m = re.search(r'name\s*=\s*["\']cli-anything-([^"\']+)["\']', content)
    return m.group(1) if m else None


def build_keywords(slug):
    base = ["cli", slug, "automation", "ai-agent", "agent-native",
            "cli-anything", "json-output", "llm-tools", "command-line"]
    meta = TOOL_META.get(slug, {})
    cat = meta.get("category", "")
    if cat:
        base.append(cat)
    return base


def format_keywords_block(keywords):
    items = ",\n        ".join(f'"{k}"' for k in keywords)
    return f"    keywords=[\n        {items},\n    ],"


def format_project_urls_block(slug, indent=4):
    sp = " " * indent
    sp2 = " " * (indent + 4)
    return (
        f'project_urls={{\n'
        f'{sp2}"Documentation": "{HUB_URL}/{slug}/",\n'
        f'{sp2}"GitHub": "{GITHUB_URL}",\n'
        f'{sp2}"Hub": "{HUB_URL}",\n'
        f'{sp2}"Agent Guide": "{HUB_URL}/docs.html",\n'
        f'{sp}}},'
    )


def patch_setup_py(filepath, dry_run=False):
    content = filepath.read_text(encoding="utf-8")
    original = content
    slug = extract_pkg_name(content)
    if not slug:
        return None, "Could not extract package name"

    slug_key = slug  # e.g. "obs-studio", "gimp"

    # 0. Enhance description FIRST (before adding keywords that contain "ai-agent")
    desc_match = re.search(r'(?<!\w)description\s*=\s*["\']([^"\']*?)["\']', content)
    if desc_match:
        desc_val = desc_match.group(1)
        if "ai agent" not in desc_val.lower() and "ai-agent" not in desc_val.lower():
            new_desc = desc_val.rstrip(". ") + ". AI-agent-friendly, JSON output, works with Claude/ChatGPT/Copilot"
            content = content.replace(desc_match.group(0),
                                       desc_match.group(0).replace(desc_val, new_desc), 1)

    # 1. Add keywords if missing
    if "keywords" not in content or (re.search(r'keywords\s*=\s*\[\s*\]', content)):
        kw_block = format_keywords_block(build_keywords(slug_key))
        # Insert before classifiers
        if "classifiers" in content:
            content = re.sub(
                r'(\n\s*classifiers\s*=)',
                f'\n{kw_block}\n\\1',
                content,
                count=1,
            )
    else:
        # Enhance existing keywords — add missing GEO keywords
        geo_kws = ["ai-agent", "agent-native", "cli-anything", "json-output", "llm-tools"]
        for kw in geo_kws:
            if f'"{kw}"' not in content and f"'{kw}'" not in content:
                content = re.sub(
                    r'(keywords\s*=\s*\[(?:[^\]]*?))([\s,]*\])',
                    lambda m: m.group(1) + f',\n        "{kw}"' + m.group(2),
                    content,
                    count=1,
                )

    # 2. Add AI classifier if missing
    if AI_CLASSIFIER not in content:
        content = re.sub(
            r'(classifiers\s*=\s*\[(?:[^\]]*?))([\s,]*\])',
            lambda m: m.group(1) + f',\n        "{AI_CLASSIFIER}"' + m.group(2),
            content,
            count=1,
        )

    # 3. Add/update project_urls
    new_urls = format_project_urls_block(slug_key)
    if "project_urls" in content:
        content = re.sub(
            r'project_urls\s*=\s*\{[^}]*\},?',
            new_urls,
            content,
            count=1,
        )
    else:
        anchors = (["py_modules", "packages", "install_requires"]
                   if "agent-harness" not in str(filepath)
                   else ["license", "packages", "install_requires"])
        for anchor in anchors:
            if anchor in content:
                content = re.sub(
                    rf'(\n(\s*){anchor}\s*=)',
                    f'\n    {new_urls}\n\\1',
                    content,
                    count=1,
                )
                break

    # 4. (description enhancement moved to step 0)

    if content == original:
        return None, "No changes needed"

    diff = list(difflib.unified_diff(
        original.splitlines(keepends=True),
        content.splitlines(keepends=True),
        fromfile=str(filepath),
        tofile=str(filepath) + " (patched)",
    ))

    if not dry_run:
        filepath.write_text(content, encoding="utf-8")

    return diff, f"Patched {slug}"


def find_all_setup_files():
    files = []
    # Hub CLIs
    for d in sorted(BASE.glob("*-cli")):
        sp = d / "setup.py"
        if sp.exists():
            files.append(sp)
    # Agent-harness CLIs
    for d in sorted(BASE.iterdir()):
        sp = d / "agent-harness" / "setup.py"
        if sp.exists():
            files.append(sp)
    return files


def main():
    dry_run = "--dry-run" in sys.argv
    mode_label = "DRY RUN" if dry_run else "LIVE"
    print(f"=== GEO Setup Patcher ({mode_label}) ===\n")

    files = find_all_setup_files()
    print(f"Found {len(files)} setup.py files\n")

    patched = 0
    skipped = 0
    all_diffs = []

    for f in files:
        diff, msg = patch_setup_py(f, dry_run=dry_run)
        if diff:
            patched += 1
            print(f"  [PATCH] {f.relative_to(BASE)} — {msg}")
            all_diffs.extend(diff)
        else:
            skipped += 1
            print(f"  [SKIP]  {f.relative_to(BASE)} — {msg}")

    print(f"\nDone: {patched} patched, {skipped} skipped")

    # Write diff report
    report_path = BASE / "scripts" / "geo_setup_patch_report.diff"
    report_path.write_text("".join(all_diffs), encoding="utf-8")
    print(f"Diff report: {report_path}")


if __name__ == "__main__":
    main()
