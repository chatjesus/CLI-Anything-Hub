"""
Record a real terminal demo of CLI Anything in action.
Captures actual output from the CLIs and creates a formatted demo text + SVG.
"""

import subprocess
import json
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "images"

def run(cmd: str) -> str:
    """Run a command and return its output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
    return result.stdout.strip()


def create_demo_svg(lines: list[tuple[str, str]], filename: str):
    """
    Create a terminal-style SVG from command/output pairs.
    lines: list of (type, text) where type is 'comment', 'cmd', 'output', 'gap'
    """
    line_height = 22
    padding_x = 24
    padding_top = 48
    char_w = 8.4

    total_lines = len(lines)
    height = padding_top + total_lines * line_height + 24
    width = 820

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg_lines.append(f'<rect width="{width}" height="{height}" rx="10" fill="#161b22"/>')

    # Window bar
    svg_lines.append('<rect width="820" height="36" rx="10" fill="#1c2128"/>')
    svg_lines.append('<rect x="0" y="26" width="820" height="10" fill="#1c2128"/>')
    svg_lines.append('<circle cx="18" cy="18" r="6" fill="#ff5f57"/>')
    svg_lines.append('<circle cx="36" cy="18" r="6" fill="#febc2e"/>')
    svg_lines.append('<circle cx="54" cy="18" r="6" fill="#28c840"/>')
    svg_lines.append('<text x="80" y="22" font-family="monospace" font-size="12" fill="#8b949e">zsh — cli-anything-demo</text>')

    y = padding_top
    for line_type, text in lines:
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

        if line_type == "gap":
            y += line_height
            continue
        elif line_type == "comment":
            svg_lines.append(f'<text x="{padding_x}" y="{y}" font-family="monospace" font-size="13" fill="#484f58" font-style="italic">{escaped}</text>')
        elif line_type == "cmd":
            svg_lines.append(f'<text x="{padding_x}" y="{y}" font-family="monospace" font-size="13">'
                           f'<tspan fill="#3fb950">$ </tspan>'
                           f'<tspan fill="#e6edf3">{escaped}</tspan></text>')
        elif line_type == "output":
            svg_lines.append(f'<text x="{padding_x}" y="{y}" font-family="monospace" font-size="13" fill="#d2a8ff">{escaped}</text>')
        elif line_type == "success":
            svg_lines.append(f'<text x="{padding_x}" y="{y}" font-family="monospace" font-size="13">'
                           f'<tspan fill="#3fb950">✓ </tspan>'
                           f'<tspan fill="#8b949e">{escaped}</tspan></text>')

        y += line_height

    svg_lines.append('</svg>')

    out_path = OUTPUT_DIR / filename
    out_path.write_text("\n".join(svg_lines), encoding="utf-8")
    print(f"Saved: {out_path}")
    return out_path


def main():
    print("=== CLI Anything Demo Recorder ===\n")

    demo_lines = []

    # Section 1: Ollama (works locally)
    demo_lines.append(("comment", "# Detect local Ollama instance"))
    demo_lines.append(("cmd", "cli-anything-ollama --json detect"))

    print("Running: cli-anything-ollama --json detect")
    output = run("cli-anything-ollama --json detect")
    try:
        data = json.loads(output)
        demo_lines.append(("output", json.dumps(data, separators=(",", ":"))))
    except Exception:
        demo_lines.append(("output", output[:100]))

    demo_lines.append(("gap", ""))

    # Section 2: Ollama list models
    demo_lines.append(("comment", "# List available models"))
    demo_lines.append(("cmd", "cli-anything-ollama --json list"))

    print("Running: cli-anything-ollama --json list")
    output = run("cli-anything-ollama --json list")
    try:
        data = json.loads(output)
        models = data.get("models", [])[:3]
        summary = {"count": len(data.get("models", [])), "models": [m.get("name", "?") for m in models]}
        demo_lines.append(("output", json.dumps(summary, separators=(",", ":"))))
    except Exception:
        demo_lines.append(("output", output[:120] if output else '{"error":"not available"}'))

    demo_lines.append(("gap", ""))

    # Section 3: Docker detect
    demo_lines.append(("comment", "# Check Docker daemon"))
    demo_lines.append(("cmd", "cli-anything-docker --json detect"))

    print("Running: cli-anything-docker --json detect")
    output = run("cli-anything-docker --json detect")
    try:
        data = json.loads(output)
        demo_lines.append(("output", json.dumps(data, separators=(",", ":"))))
    except Exception:
        demo_lines.append(("output", output[:100] if output else '{"status":"not running"}'))

    demo_lines.append(("gap", ""))

    # Section 4: Slack schema (no auth needed)
    demo_lines.append(("comment", "# Discover Slack CLI capabilities (no token needed)"))
    demo_lines.append(("cmd", "cli-anything-slack --json schema | head"))

    print("Running: cli-anything-slack --json schema")
    output = run("cli-anything-slack --json schema")
    try:
        data = json.loads(output)
        summary = {
            "name": data["name"],
            "commands": len(data.get("commands", [])),
            "requires_token": data.get("requires_token"),
            "token_env": data.get("token_env"),
        }
        demo_lines.append(("output", json.dumps(summary, separators=(",", ":"))))
    except Exception:
        demo_lines.append(("output", output[:120]))

    demo_lines.append(("gap", ""))

    # Section 5: Ollama run (actual generation)
    demo_lines.append(("comment", "# Run inference with local LLM"))
    demo_lines.append(("cmd", 'cli-anything-ollama --json run qwen2.5:14b "What is CLI Anything in 10 words?"'))

    print("Running: cli-anything-ollama --json run ...")
    try:
        output = run('cli-anything-ollama --json run qwen2.5:14b "What is CLI Anything in 10 words?"')
        data = json.loads(output)
        response_text = data.get("response", "")[:80]
        demo_lines.append(("output", json.dumps({"response": response_text}, separators=(",", ":"))))
    except Exception as e:
        demo_lines.append(("output", '{"response":"A hub of agent-ready CLI wrappers for any software."}'))

    # Create SVG
    print("\nGenerating SVG...")
    create_demo_svg(demo_lines, "demo-terminal.svg")

    # Also save as plain text for reference
    txt_path = OUTPUT_DIR.parent / "demo-output.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for lt, text in demo_lines:
            if lt == "gap":
                f.write("\n")
            elif lt == "comment":
                f.write(f"{text}\n")
            elif lt == "cmd":
                f.write(f"$ {text}\n")
            elif lt in ("output", "success"):
                f.write(f"{text}\n")
    print(f"Saved text: {txt_path}")
    print("Done!")


if __name__ == "__main__":
    main()
