"""
Screenshot HTML gallery pages to PNG images at exact 1270x760 resolution.
Uses html2image (Chrome headless).
"""

from html2image import Html2Image
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "images"
HTML_DIR = Path(__file__).parent

hti = Html2Image(
    output_path=str(OUTPUT_DIR),
    size=(1270, 760),
)

pages = [
    ("gallery-hero.html", "gallery-1-hero.png"),
    ("gallery-terminal.html", "gallery-2-terminal.png"),
    ("gallery-icons.html", "gallery-3-icons.png"),
    ("gallery-arch.html", "gallery-4-arch.png"),
    ("gallery-code.html", "gallery-5-code.png"),
]

for html_file, output_name in pages:
    html_path = HTML_DIR / html_file
    html_content = html_path.read_text(encoding="utf-8")
    print(f"Rendering {html_file} -> {output_name} ...")
    hti.screenshot(
        html_str=html_content,
        save_as=output_name,
    )
    out = OUTPUT_DIR / output_name
    if out.exists():
        print(f"  OK: {out} ({out.stat().st_size / 1024:.0f} KB)")
    else:
        print(f"  FAILED: {out} not found")

print("\nDone!")
