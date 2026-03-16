"""
CLI Anything Hub — Blog Multilingual Generator
Uses Vertex AI Gemini 2.0 Flash to translate BLOG_POST.md into:
  - Simplified Chinese (zh-CN)  -> BLOG_POST_CN.md
  - Japanese (ja)               -> BLOG_POST_JA.md
  - Korean (ko)                 -> BLOG_POST_KO.md

Usage:
    python generate_blog_translations.py
    python generate_blog_translations.py --lang zh ja   # specific languages only
    python generate_blog_translations.py --dry-run      # validate setup, no API calls
"""

import argparse
import io
import os
import sys
import time
from pathlib import Path

# Force UTF-8 output on Windows consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from google import genai
from google.genai.types import GenerateContentConfig

# ── Credentials ───────────────────────────────────────────────────────────────
CREDENTIALS_PATH = r"C:\Users\PRO\Desktop\CUDA\credentials\pdfconverter-415414-d9dbb1a4eec6.json"
PROJECT_ID = "pdfconverter-415414"
MODEL = "gemini-2.0-flash-001"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# ── Paths ─────────────────────────────────────────────────────────────────────
HERE = Path(__file__).parent
SOURCE_FILE = HERE / "BLOG_POST.md"

def _base_prompt(language: str, extra: str = "") -> str:
    return (
        f"You are a professional technical translator specializing in AI, developer tools, "
        f"and software engineering content. Translate the following English blog post into {language}. "
        f"\n\nTranslation requirements:"
        f"\n- Preserve ALL markdown formatting exactly (headers, code blocks, tables, bold, italic, links)"
        f"\n- Keep ALL code blocks, CLI commands, JSON examples, and bash snippets in English — do NOT translate code"
        f"\n- Keep product names in English: CLI Anything, MCP, Slack, Stripe, Docker, GIMP, Blender, GitHub, etc."
        f"\n- Use natural, fluent {language} that reads like original developer-focused content, not a translation"
        f"\n- Tone: technical and precise, suitable for software engineers"
        f"\n- Preserve all URLs, links, and reference citations exactly"
        f"\n- Translate the blog post title and all section headers"
        f"\n- Numbers, statistics, and data points must be preserved exactly"
        + (f"\n{extra}" if extra else "")
    )


LANGUAGE_CONFIG = {
    "zh": {
        "name": "Simplified Chinese",
        "native_name": "简体中文",
        "output_file": HERE / "BLOG_POST_CN.md",
        "notice": "> **注意：** 本文由 Vertex AI Gemini 2.0 Flash 从英文原文自动翻译。[查看英文原文](./BLOG_POST.md)\n\n---\n\n",
        "system_prompt": _base_prompt(
            "Simplified Chinese (简体中文)",
            "- Use simplified Chinese characters (简体), not traditional\n"
            "- Keep technical terms in English with Chinese on first use where helpful: e.g. 'Agent Harness（智能体工作框架）'",
        ),
    },
    "ja": {
        "name": "Japanese",
        "native_name": "日本語",
        "output_file": HERE / "BLOG_POST_JA.md",
        "notice": "> **注記：** この記事は Vertex AI Gemini 2.0 Flash により英語原文から自動翻訳されました。[英語原文を読む](./BLOG_POST.md)\n\n---\n\n",
        "system_prompt": _base_prompt(
            "Japanese (日本語)",
            "- Use appropriate technical Japanese: エージェント (agent), トークン (token), etc.",
        ),
    },
    "ko": {
        "name": "Korean",
        "native_name": "한국어",
        "output_file": HERE / "BLOG_POST_KO.md",
        "notice": "> **참고:** 이 글은 Vertex AI Gemini 2.0 Flash를 사용하여 영어 원문에서 자동 번역되었습니다.[영어 원문 읽기](./BLOG_POST.md)\n\n---\n\n",
        "system_prompt": _base_prompt("Korean (한국어)"),
    },
    "es": {
        "name": "Spanish",
        "native_name": "Español",
        "output_file": HERE / "BLOG_POST_ES.md",
        "notice": "> **Nota:** Este artículo fue traducido automáticamente del inglés por Vertex AI Gemini 2.0 Flash. [Leer original en inglés](./BLOG_POST.md)\n\n---\n\n",
        "system_prompt": _base_prompt(
            "Spanish (Español)",
            "- Use Latin American Spanish conventions (more widely understood globally)\n"
            "- Avoid overly formal register; use natural developer-community tone",
        ),
    },
    "pt": {
        "name": "Portuguese",
        "native_name": "Português",
        "output_file": HERE / "BLOG_POST_PT.md",
        "notice": "> **Nota:** Este artigo foi traduzido automaticamente do inglês pelo Vertex AI Gemini 2.0 Flash. [Ler original em inglês](./BLOG_POST.md)\n\n---\n\n",
        "system_prompt": _base_prompt(
            "Brazilian Portuguese (Português do Brasil)",
            "- Use Brazilian Portuguese (pt-BR) conventions\n"
            "- Natural, developer-friendly tone suitable for the Brazilian tech community",
        ),
    },
    "de": {
        "name": "German",
        "native_name": "Deutsch",
        "output_file": HERE / "BLOG_POST_DE.md",
        "notice": "> **Hinweis:** Dieser Artikel wurde automatisch aus dem Englischen von Vertex AI Gemini 2.0 Flash übersetzt. [Englisches Original lesen](./BLOG_POST.md)\n\n---\n\n",
        "system_prompt": _base_prompt(
            "German (Deutsch)",
            "- Use modern technical German; avoid overly bureaucratic phrasing\n"
            "- Keep English loanwords common in tech (Agent, Token, Stack, Deploy, etc.) in English",
        ),
    },
    "fr": {
        "name": "French",
        "native_name": "Français",
        "output_file": HERE / "BLOG_POST_FR.md",
        "notice": "> **Note :** Cet article a été traduit automatiquement de l'anglais par Vertex AI Gemini 2.0 Flash. [Lire l'original en anglais](./BLOG_POST.md)\n\n---\n\n",
        "system_prompt": _base_prompt(
            "French (Français)",
            "- Use modern, developer-friendly French; avoid overly formal register\n"
            "- Keep English tech terms common in the French developer community (agent, token, stack, deploy, etc.)",
        ),
    },
}


FALLBACK_MODELS = [
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite-001",
    "gemini-2.0-flash-001",   # retry same model on transient disconnect
]


def translate(client: genai.Client, lang_key: str, source_text: str, retries: int = 3) -> str | None:
    """Translate source_text into the target language using Gemini Flash. Retries on failure."""
    config = LANGUAGE_CONFIG[lang_key]
    print(f"\n{'='*60}")
    print(f"Translating -> {config['name']} ({config['native_name']})")
    print(f"{'='*60}")

    prompt = (
        f"{config['system_prompt']}"
        f"\n\n---\n\nSOURCE TEXT TO TRANSLATE:\n\n{source_text}"
    )

    for attempt in range(1, retries + 1):
        model = FALLBACK_MODELS[min(attempt - 1, len(FALLBACK_MODELS) - 1)]
        print(f"  Attempt {attempt}/{retries} | Model: {model}")
        try:
            t0 = time.time()
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=8192,
                ),
            )
            elapsed = time.time() - t0
            translated = response.text
            word_count = len(translated.split())
            print(f"  Done in {elapsed:.1f}s | ~{word_count} words output.")
            return translated

        except Exception as e:
            wait = 5 * attempt
            print(f"  ERROR: {e}")
            if attempt < retries:
                print(f"  Retrying in {wait}s...")
                time.sleep(wait)

    print(f"  All {retries} attempts failed.")
    return None


def add_translation_header(text: str, lang_key: str, source_file: str = "./BLOG_POST.md") -> str:
    """Prepend a localised machine-translation notice."""
    notice = LANGUAGE_CONFIG[lang_key].get("notice", "")
    return notice + text


def main():
    parser = argparse.ArgumentParser(
        description="Generate multilingual blog posts using Vertex AI Gemini Flash"
    )
    parser.add_argument(
        "--lang",
        nargs="+",
        choices=list(LANGUAGE_CONFIG.keys()),
        default=list(LANGUAGE_CONFIG.keys()),
        help="Languages to generate (default: all). Choices: zh ja ko",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate setup without making API calls",
    )
    args = parser.parse_args()

    # Validate source file
    if not SOURCE_FILE.exists():
        print(f"ERROR: Source file not found: {SOURCE_FILE}")
        sys.exit(1)

    source_text = SOURCE_FILE.read_text(encoding="utf-8")
    print(f"Source: {SOURCE_FILE} ({len(source_text.split())} words approx.)")
    print(f"Target languages: {', '.join(args.lang)}")

    if args.dry_run:
        print("\nDRY RUN — setup looks good. No API calls made.")
        for lang in args.lang:
            cfg = LANGUAGE_CONFIG[lang]
            print(f"  Would generate: {cfg['output_file']}")
        sys.exit(0)

    # Initialize Vertex AI client
    print(f"\nInitializing Vertex AI client (project: {PROJECT_ID})...")
    try:
        client = genai.Client()
        print("  Client initialized.")
    except Exception as e:
        print(f"ERROR initializing client: {e}")
        sys.exit(1)

    # Translate each language
    results = {}
    for lang_key in args.lang:
        cfg = LANGUAGE_CONFIG[lang_key]

        translated = translate(client, lang_key, source_text)

        if translated:
            final_text = add_translation_header(
                translated,
                lang_key,
                source_file="./BLOG_POST.md",
            )
            cfg["output_file"].write_text(final_text, encoding="utf-8")
            print(f"  Saved → {cfg['output_file']}")
            results[lang_key] = "OK"
        else:
            results[lang_key] = "FAILED"

        # Respectful delay between API calls
        if lang_key != args.lang[-1]:
            print("  Waiting 3s before next translation...")
            time.sleep(3)

    # Summary
    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"{'='*60}")
    for lang_key, status in results.items():
        cfg = LANGUAGE_CONFIG[lang_key]
        icon = "✓" if status == "OK" else "✗"
        print(f"  {icon} {cfg['name']:20s} → {cfg['output_file'].name}  [{status}]")

    failed = [k for k, v in results.items() if v == "FAILED"]
    if failed:
        print(f"\nFailed languages: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\nAll translations completed successfully.")


if __name__ == "__main__":
    main()
