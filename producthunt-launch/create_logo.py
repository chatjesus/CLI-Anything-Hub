"""
CLI Anything Hub — Logo Generator
Programmatic logo creation using Pillow for pixel-perfect results.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)


def create_logo_v1(size=960):
    """
    Main logo: '>_' terminal prompt in a rounded square.
    Dark background + green terminal text.
    Designed to look clean at 240px and recognizable at 16px.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bg_color = (13, 17, 23)        # GitHub dark: #0d1117
    green = (0, 255, 65)           # Terminal green: #00ff41
    margin = int(size * 0.06)
    radius = int(size * 0.18)

    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=bg_color,
    )

    # '>_' drawn as geometric shapes for crispness
    cx, cy = size // 2, size // 2
    stroke_w = int(size * 0.065)

    # '>' chevron — two lines forming a right-pointing arrow
    chevron_left = int(size * 0.22)
    chevron_right = int(size * 0.48)
    chevron_top = int(size * 0.28)
    chevron_mid = int(size * 0.48)
    chevron_bot = int(size * 0.68)

    # Top line of >
    draw.line(
        [(chevron_left, chevron_top), (chevron_right, chevron_mid)],
        fill=green, width=stroke_w,
    )
    # Bottom line of >
    draw.line(
        [(chevron_left, chevron_bot), (chevron_right, chevron_mid)],
        fill=green, width=stroke_w,
    )

    # Round the joints
    joint_r = stroke_w // 2
    draw.ellipse(
        [chevron_left - joint_r, chevron_top - joint_r,
         chevron_left + joint_r, chevron_top + joint_r],
        fill=green,
    )
    draw.ellipse(
        [chevron_right - joint_r, chevron_mid - joint_r,
         chevron_right + joint_r, chevron_mid + joint_r],
        fill=green,
    )
    draw.ellipse(
        [chevron_left - joint_r, chevron_bot - joint_r,
         chevron_left + joint_r, chevron_bot + joint_r],
        fill=green,
    )

    # '_' underscore — horizontal line
    underscore_left = int(size * 0.54)
    underscore_right = int(size * 0.78)
    underscore_y = int(size * 0.68)

    draw.line(
        [(underscore_left, underscore_y), (underscore_right, underscore_y)],
        fill=green, width=stroke_w,
    )
    draw.ellipse(
        [underscore_left - joint_r, underscore_y - joint_r,
         underscore_left + joint_r, underscore_y + joint_r],
        fill=green,
    )
    draw.ellipse(
        [underscore_right - joint_r, underscore_y - joint_r,
         underscore_right + joint_r, underscore_y + joint_r],
        fill=green,
    )

    return img


def create_logo_v2(size=960):
    """
    Variant 2: '>_' with a subtle border ring instead of filled bg.
    More open, modern feel.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bg_color = (13, 17, 23)
    green = (0, 255, 65)
    border_color = (48, 54, 61)     # Subtle gray border: #30363d
    margin = int(size * 0.06)
    radius = int(size * 0.18)
    border_w = int(size * 0.025)

    # Filled dark background
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=bg_color,
    )

    # Border stroke
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        outline=border_color,
        width=border_w,
    )

    stroke_w = int(size * 0.058)

    # '>' — slightly larger, more centered
    cl = int(size * 0.20)
    cr = int(size * 0.46)
    ct = int(size * 0.30)
    cm = int(size * 0.50)
    cb = int(size * 0.70)

    draw.line([(cl, ct), (cr, cm)], fill=green, width=stroke_w)
    draw.line([(cl, cb), (cr, cm)], fill=green, width=stroke_w)

    jr = stroke_w // 2
    for x, y in [(cl, ct), (cr, cm), (cl, cb)]:
        draw.ellipse([x-jr, y-jr, x+jr, y+jr], fill=green)

    # '_'
    ul = int(size * 0.52)
    ur = int(size * 0.78)
    uy = int(size * 0.70)

    draw.line([(ul, uy), (ur, uy)], fill=green, width=stroke_w)
    for x in [ul, ur]:
        draw.ellipse([x-jr, uy-jr, x+jr, uy+jr], fill=green)

    return img


def create_logo_v3(size=960):
    """
    Variant 3: Hexagonal container with '>_'.
    More distinctive, npm-like geometric feel.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bg_color = (13, 17, 23)
    green = (0, 255, 65)
    cx, cy = size // 2, size // 2
    hex_r = int(size * 0.44)

    # Draw hexagon
    hex_points = []
    for i in range(6):
        angle = math.radians(60 * i - 90)
        hx = cx + hex_r * math.cos(angle)
        hy = cy + hex_r * math.sin(angle)
        hex_points.append((hx, hy))

    draw.polygon(hex_points, fill=bg_color)

    stroke_w = int(size * 0.055)
    jr = stroke_w // 2

    # '>' offset left
    cl = int(size * 0.24)
    cr = int(size * 0.47)
    ct = int(size * 0.32)
    cm = int(size * 0.50)
    cb = int(size * 0.68)

    draw.line([(cl, ct), (cr, cm)], fill=green, width=stroke_w)
    draw.line([(cl, cb), (cr, cm)], fill=green, width=stroke_w)
    for x, y in [(cl, ct), (cr, cm), (cl, cb)]:
        draw.ellipse([x-jr, y-jr, x+jr, y+jr], fill=green)

    # '_'
    ul = int(size * 0.53)
    ur = int(size * 0.76)
    uy = int(size * 0.68)

    draw.line([(ul, uy), (ur, uy)], fill=green, width=stroke_w)
    for x in [ul, ur]:
        draw.ellipse([x-jr, uy-jr, x+jr, uy+jr], fill=green)

    return img


def save_all_sizes(img: Image.Image, base_name: str):
    """Save at multiple sizes for different use cases."""
    sizes = {
        "240x240": (240, 240),
        "480x480": (480, 480),
        "128x128": (128, 128),
        "64x64": (64, 64),
        "32x32": (32, 32),
    }

    for suffix, (w, h) in sizes.items():
        resized = img.resize((w, h), Image.LANCZOS)
        out = OUTPUT_DIR / f"{base_name}-{suffix}.png"
        resized.save(out, "PNG")
        print(f"  {out.name}")


def main():
    print("=== CLI Anything Hub — Logo Generator ===\n")

    print("Logo V1 (rounded square):")
    v1 = create_logo_v1()
    v1.save(OUTPUT_DIR / "logo-v1-full.png", "PNG")
    save_all_sizes(v1, "logo-v1")

    print("\nLogo V2 (rounded square + border):")
    v2 = create_logo_v2()
    v2.save(OUTPUT_DIR / "logo-v2-full.png", "PNG")
    save_all_sizes(v2, "logo-v2")

    print("\nLogo V3 (hexagon):")
    v3 = create_logo_v3()
    v3.save(OUTPUT_DIR / "logo-v3-full.png", "PNG")
    save_all_sizes(v3, "logo-v3")

    # Default: V1 as the primary logo
    v1_240 = v1.resize((240, 240), Image.LANCZOS)
    v1_240.save(OUTPUT_DIR / "logo-240x240.png", "PNG")
    print(f"\nPrimary logo saved: logo-240x240.png")
    print("Done! Review all variants in images/ folder.")


if __name__ == "__main__":
    main()
