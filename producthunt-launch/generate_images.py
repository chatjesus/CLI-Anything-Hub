"""
CLI Anything Hub — Product Hunt Launch Image Generator
Uses Vertex AI Gemini 3 Pro Image to generate all launch visuals.
"""

import os
import sys
import time
from io import BytesIO
from pathlib import Path

from google import genai
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image

CREDENTIALS_PATH = r"C:\Users\PRO\Desktop\CUDA\credentials\pdfconverter-415414-d9dbb1a4eec6.json"
PROJECT_ID = "pdfconverter-415414"
OUTPUT_DIR = Path(__file__).parent / "images"
MODEL = "gemini-2.5-flash-image"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

OUTPUT_DIR.mkdir(exist_ok=True)

client = genai.Client()

PROMPTS = {

    # ── Logo 240×240 ──────────────────────────────────────────────
    "logo-240x240": {
        "prompt": (
            "Design a minimal, professional logo icon for a developer tool called 'CLI Anything'. "
            "The logo is a stylized terminal prompt cursor '>_' placed inside a clean rounded square shape. "
            "Use ONLY two colors: charcoal black (#1a1a2e) background and bright terminal green (#00ff41) for the '>_' symbol. "
            "The design must be perfectly flat — no gradients, no shadows, no 3D effects, no gloss, no reflections. "
            "Think of the simplicity of the Docker whale logo or the npm red square. "
            "The icon should be recognizable at 16px. "
            "Pure geometric shapes, pixel-perfect edges, vector-quality rendering. "
            "Square canvas, centered composition. White/transparent margin around the shape."
        ),
        "size": (240, 240),
    },

    "logo-alt": {
        "prompt": (
            "Design a minimalist logo mark for a software product called 'CLI Anything Hub'. "
            "Concept: a single right-angle bracket '>' character in bold monospace font, "
            "with a blinking cursor line next to it, all enclosed in a hexagonal border. "
            "Color palette: deep navy (#0d1117) background, electric green (#39d353) for the bracket and cursor. "
            "Style: completely flat design, no bevels, no lighting effects, geometric precision. "
            "Similar aesthetic to GitHub's octocat simplicity or Vercel's triangle logo. "
            "Square canvas. Clean edges. The hexagon border has 2px stroke weight."
        ),
        "size": (240, 240),
    },

    # ── Gallery 1: Hero ───────────────────────────────────────────
    "gallery-1-hero": {
        "prompt": (
            "Create a wide banner image for a developer product launch. "
            "Dark background (#0d1117) with a subtle dot grid pattern. "
            "Center text in bold white sans-serif font: 'CLI Anything' on line 1 (large), "
            "'The Software Registry Built for AI Agents' on line 2 (medium, light gray). "
            "Below the text, a row of 7 small software icons in a horizontal line: "
            "a chat bubble (Slack), a lightning bolt (Stripe), a whale shape (Docker), "
            "a paintbrush (GIMP), a 3D cube (Blender), a document (Notion), a git branch (GitHub). "
            "Each icon is a simple monochrome outline in different muted colors. "
            "Clean, editorial design. Generous whitespace. No clutter. "
            "Aspect ratio 16:9 landscape."
        ),
        "size": (1270, 760),
    },

    # ── Gallery 2: Terminal Demo ──────────────────────────────────
    "gallery-2-terminal": {
        "prompt": (
            "Create a product screenshot showing a macOS-style terminal window on a dark background. "
            "The terminal has three colored dots (red/yellow/green) at top left and title 'zsh'. "
            "Terminal background is #1a1a2e. The terminal shows this exact sequence:\n"
            "Line 1: green '$ ' then white 'pip install cli-anything-slack'\n"
            "Line 2: green checkmark then gray 'Installed cli-anything-slack 1.0.0'\n"
            "Line 3: empty\n"
            "Line 4: green '$ ' then white 'cli-anything-slack detect'\n"
            "Line 5: yellow JSON: {\"status\": \"ok\", \"workspace\": \"MyTeam\"}\n"
            "Line 6: empty\n"
            "Line 7: green '$ ' then white 'cli-anything-slack --json message send #general \"Hello\"'\n"
            "Line 8: yellow JSON: {\"ok\": true, \"channel\": \"C123\"}\n"
            "Font: monospace. Clean rendering. The terminal floats with a subtle shadow on a #0d1117 bg. "
            "Aspect ratio 16:9 landscape."
        ),
        "size": (1270, 760),
    },

    # ── Gallery 3: Tool Matrix ────────────────────────────────────
    "gallery-3-icons": {
        "prompt": (
            "Create an infographic showing a grid of 30 software tool icons on a dark background (#0d1117). "
            "Arrange icons in a 6×5 grid. Each cell has: a simple flat icon + tool name below in small text. "
            "Tools include: Slack, Stripe, Docker, GIMP, Blender, Notion, GitHub, Inkscape, "
            "OBS Studio, Audacity, Discord, Telegram, Shopify, Jira, Vercel, Cloudflare, "
            "Twilio, HubSpot, Salesforce, Ollama, LibreOffice, Gmail, Google Drive, Google Sheets, "
            "MS Word, MS Excel, MS PowerPoint, FFmpeg, Chrome, VS Code. "
            "Icons that are 'ready' have a small green checkmark badge. "
            "Title at top: '30+ Agent-Ready CLIs' in white bold text. "
            "Clean grid layout, consistent spacing, flat colored icons. "
            "Aspect ratio 16:9 landscape."
        ),
        "size": (1270, 760),
    },

    # ── Gallery 4: Architecture ───────────────────────────────────
    "gallery-4-arch": {
        "prompt": (
            "Create a technical architecture diagram on dark background (#0d1117). "
            "Flow diagram showing: "
            "TOP: A box labeled 'AI Agent' with icons for Claude, Cursor, GPT, Codex. "
            "MIDDLE: A large rounded rectangle labeled 'CLI Anything Hub' containing "
            "the text 'detect → schema → call → JSON' as a horizontal flow. "
            "BOTTOM: Six boxes in a row representing different software: "
            "'Slack API', 'Stripe SDK', 'Docker Engine', 'GIMP Script-Fu', 'Blender bpy', 'GitHub REST'. "
            "Arrows connect top to middle to bottom. "
            "Use thin white lines for arrows, muted colored fills for boxes. "
            "Clean, minimal diagram style — NOT a 3D illustration. "
            "Think of technical documentation diagrams. "
            "Aspect ratio 16:9 landscape."
        ),
        "size": (1270, 760),
    },

    # ── Gallery 5: Code Example ───────────────────────────────────
    "gallery-5-code": {
        "prompt": (
            "Create a developer-focused product image showing three code snippets side by side. "
            "Dark background (#0d1117). Three terminal/code panels arranged horizontally:\n"
            "Panel 1 (blue header 'Slack'): shows 'cli-anything-slack --json message send #ops \"Deploy done\"' "
            "with JSON response below.\n"
            "Panel 2 (purple header 'Stripe'): shows 'cli-anything-stripe --json customers list --limit 5' "
            "with JSON response below.\n"
            "Panel 3 (green header 'Docker'): shows 'cli-anything-docker --json containers list' "
            "with JSON response below.\n"
            "Below all three panels, centered text: 'One interface. Any software. Structured output.' "
            "Monospace font for code, clean sans-serif for labels. "
            "Aspect ratio 16:9 landscape."
        ),
        "size": (1270, 760),
    },
}


def generate_image(name: str, spec: dict) -> Path:
    """Generate a single image and save it."""
    print(f"\n{'='*60}")
    print(f"Generating: {name}")
    print(f"{'='*60}")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=spec["prompt"],
            config=GenerateContentConfig(
                response_modalities=[Modality.TEXT, Modality.IMAGE],
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                target_w, target_h = spec["size"]
                if image.size != (target_w, target_h):
                    image = image.resize((target_w, target_h), Image.LANCZOS)
                out_path = OUTPUT_DIR / f"{name}.png"
                image.save(out_path, "PNG")
                print(f"  Saved: {out_path} ({image.size[0]}x{image.size[1]})")
                return out_path
            elif part.text:
                print(f"  Model text: {part.text[:200]}")

        print(f"  WARNING: No image returned for {name}")
        return None

    except Exception as e:
        print(f"  ERROR generating {name}: {e}")
        return None


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(PROMPTS.keys())
    print(f"CLI Anything Hub — PH Launch Image Generator")
    print(f"Model: {MODEL}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Targets: {', '.join(targets)}")

    results = {}
    for name in targets:
        if name not in PROMPTS:
            print(f"Unknown target: {name}, skipping")
            continue
        result = generate_image(name, PROMPTS[name])
        results[name] = result
        time.sleep(2)

    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"{'='*60}")
    for name, path in results.items():
        status = f"OK → {path}" if path else "FAILED"
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
