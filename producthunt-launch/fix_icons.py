"""
Fix broken icons by replacing CDN URLs with inline base64 data URIs.
Uses devicon CDN where available, hand-crafted SVGs for the rest.
"""

import re
import base64
import requests
from pathlib import Path

HTML_DIR = Path(__file__).parent
CACHE = {}


HANDCRAFTED_SVGS = {
    "https://cdn.simpleicons.org/microsoftteams/6264A7": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#6264A7"><path d="M20.7 4.1c1.1 0 2 .9 2 2v4.7c0 1.1-.9 2-2 2h-.1c.1-.3.1-.6.1-.9V7.3c0-.7-.2-1.3-.5-1.8.4-.8 1.3-1.4 2.3-1.4h-1.8zM16.2 2.7a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm3.1 4.6v4.6c0 2.2-1.8 4-4 4h-.3c.3-.6.5-1.3.5-2V8.3c0-.7-.2-1.4-.6-2 .6-.6 1.4-1 2.4-1 1.1 0 2 .9 2 2zM12 1a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm4.3 6.3v6.6c0 2.8-2.2 5-5 5h-2.6c-2.8 0-5-2.2-5-5V7.3c0-.7.6-1.3 1.3-1.3h10c.7 0 1.3.6 1.3 1.3zM1.3 9H5v5.9c0 1.3.4 2.5 1 3.5-.4.1-.8.1-1.3.1C2.1 18.5 0 16.4 0 13.8V10.3c0-.7.6-1.3 1.3-1.3z"/></svg>''',
    "https://cdn.simpleicons.org/microsoftoutlook/0078D4": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0078D4"><path d="M24 7.8v8.4c0 .8-.7 1.5-1.5 1.5H15v-12h7.5c.8 0 1.5.7 1.5 1.5v.6zm-10.5 9.9V5.7l-1.2-.6V18.3l1.2-.6zm-3-12L0 9v10.5l10.5-3.7V5.7zM5.3 15.4c-1.7 0-3-1.6-3-3.5s1.3-3.5 3-3.5 3 1.6 3 3.5-1.3 3.5-3 3.5zm0-5.7c-.9 0-1.6.9-1.6 2.1s.7 2.1 1.6 2.1 1.6-.9 1.6-2.1-.7-2.1-1.6-2.1z"/></svg>''',
    "https://cdn.simpleicons.org/microsoftword/2B579A": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#2B579A"><rect x="0" y="3" width="24" height="18" rx="2" fill="#2B579A"/><text x="12" y="16" font-family="Arial,sans-serif" font-weight="bold" font-size="12" fill="white" text-anchor="middle">W</text></svg>''',
    "https://cdn.simpleicons.org/microsoftexcel/217346": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#217346"><rect x="0" y="3" width="24" height="18" rx="2" fill="#217346"/><text x="12" y="16" font-family="Arial,sans-serif" font-weight="bold" font-size="12" fill="white" text-anchor="middle">X</text></svg>''',
    "https://cdn.simpleicons.org/microsoftpowerpoint/B7472A": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#B7472A"><rect x="0" y="3" width="24" height="18" rx="2" fill="#B7472A"/><text x="12" y="16" font-family="Arial,sans-serif" font-weight="bold" font-size="12" fill="white" text-anchor="middle">P</text></svg>''',
    "https://cdn.simpleicons.org/minecraft/62B47A": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#62B47A"><rect width="24" height="24" rx="2" fill="#62B47A"/><rect x="4" y="4" width="5" height="5" fill="#3B7A2B"/><rect x="15" y="4" width="5" height="5" fill="#3B7A2B"/><rect x="8" y="10" width="8" height="4" fill="#3B7A2B"/><rect x="6" y="15" width="4" height="4" fill="#3B7A2B"/><rect x="14" y="15" width="4" height="4" fill="#3B7A2B"/></svg>''',
    "https://cdn.simpleicons.org/lark/3370FF": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#3370FF"><path d="M5.6 21.3c-.4-.5-.3-1.1.1-1.5l8-6.3c.4-.3 1-.3 1.4 0l3.3 2.5c.5.4.6 1 .1 1.5L12.7 23c-.5.5-1.2.5-1.7 0L5.6 21.3z"/><path d="M2.2 11.4c-.5-.4-.5-1.1-.1-1.5L10.5 1c.5-.5 1.2-.5 1.7 0l5.3 5.3c.4.5.4 1.1-.1 1.5l-8.2 6.4c-.4.3-1 .3-1.4 0L2.2 11.4z" opacity=".6"/></svg>''',
}

DEVICON_MAP = {
    "https://cdn.simpleicons.org/slack/E01E5A": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/slack/slack-original.svg",
    "https://cdn.simpleicons.org/adobephotoshop/31A8FF": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/photoshop/photoshop-original.svg",
    "https://cdn.simpleicons.org/visualstudiocode/007ACC": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg",
    "https://cdn.simpleicons.org/twilio/F22F46": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/twilio/twilio-original.svg",
}


def svg_to_data_uri(svg_text: str) -> str:
    b64 = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def fetch_and_encode(url: str) -> str:
    if url in CACHE:
        return CACHE[url]
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        b64 = base64.b64encode(r.content).decode("ascii")
        data_uri = f"data:image/svg+xml;base64,{b64}"
        CACHE[url] = data_uri
        return data_uri
    except Exception as e:
        print(f"  FETCH FAIL: {url} -> {e}")
        return None


def get_replacement(original_url: str) -> str | None:
    if original_url in HANDCRAFTED_SVGS:
        return svg_to_data_uri(HANDCRAFTED_SVGS[original_url])

    if original_url in DEVICON_MAP:
        return fetch_and_encode(DEVICON_MAP[original_url])

    return fetch_and_encode(original_url)


def fix_file(filepath: Path):
    content = filepath.read_text(encoding="utf-8")

    urls = set(re.findall(r'https://cdn\.simpleicons\.org/[^"\'>\s]+', content))
    devicon_urls = set(re.findall(r'https://cdn\.jsdelivr\.net/gh/devicons/[^"\'>\s]+', content))
    all_urls = urls | devicon_urls

    if not all_urls:
        print(f"  No icon URLs in {filepath.name}")
        return

    already_inlined = content.count("data:image/svg+xml;base64,")
    print(f"  {filepath.name}: {len(all_urls)} URLs ({already_inlined} already inlined)")

    success = 0
    fail = 0
    for url in sorted(all_urls):
        if url.startswith("data:"):
            continue
        data_uri = get_replacement(url)
        if data_uri:
            content = content.replace(url, data_uri)
            slug = url.split("/")[-1] if "/" in url else url
            source = "handcrafted" if url in HANDCRAFTED_SVGS else ("devicon" if url in DEVICON_MAP else "simpleicons")
            print(f"    OK [{source}]: .../{'/'.join(url.split('/')[-2:])}")
            success += 1
        else:
            print(f"    FAIL: {url}")
            fail += 1

    filepath.write_text(content, encoding="utf-8")
    print(f"  Saved: {filepath.name} ({success} ok, {fail} fail)")


def main():
    print("=== Fix Icons v2: Inline all icons as base64 ===\n")

    for name in ["gallery-hero.html", "gallery-icons.html"]:
        path = HTML_DIR / name
        if path.exists():
            fix_file(path)
            print()

    print("Done! Now re-run screenshot_gallery.py.")


if __name__ == "__main__":
    main()
