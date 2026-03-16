"""用 CLI-Anything Inkscape API 直接生成科技风海报"""
import sys
sys.path.insert(0, r"C:\Users\PRO\Desktop\CUDA\CLI-Anything\inkscape\agent-harness")

from cli_anything.inkscape.core import document as doc_mod
from cli_anything.inkscape.core import shapes as shape_mod
from cli_anything.inkscape.core import text as text_mod
from cli_anything.inkscape.core import export as export_mod

OUT_JSON = r"C:\Users\PRO\Desktop\CUDA\CLI-Anything\poster_final.json"
OUT_SVG  = r"C:\Users\PRO\Desktop\CUDA\CLI-Anything\poster_final.svg"
OUT_PNG  = r"C:\Users\PRO\Desktop\CUDA\CLI-Anything\poster_final.png"

# ── 新建文档 ────────────────────────────────────────────────────
proj = doc_mod.create_document(name="CLI-Anything Poster", width=1200, height=675)
print("✓ 新建文档 1200x675")

# ── 背景 ────────────────────────────────────────────────────────
shape_mod.add_rect(proj, x=0, y=0, width=1200, height=675, name="bg",        style="fill:#0d0d1a")
shape_mod.add_rect(proj, x=0, y=0, width=1200, height=5,   name="top-bar",   style="fill:#00d4ff")
shape_mod.add_rect(proj, x=0, y=670, width=1200, height=5, name="bot-bar",   style="fill:#00d4ff")
print("✓ 背景绘制完成")

# ── 右侧同心圆装饰 ───────────────────────────────────────────────
shape_mod.add_circle(proj, cx=950, cy=337, r=290, name="ring3", style="fill:none;stroke:#00d4ff;stroke-width:1.5;opacity:0.25")
shape_mod.add_circle(proj, cx=950, cy=337, r=210, name="ring2", style="fill:none;stroke:#00d4ff;stroke-width:1;opacity:0.18")
shape_mod.add_circle(proj, cx=950, cy=337, r=140, name="ring1", style="fill:#00d4ff;opacity:0.07")
shape_mod.add_circle(proj, cx=950, cy=337, r=80,  name="ring0", style="fill:#00d4ff;opacity:0.06")
shape_mod.add_circle(proj, cx=950, cy=337, r=48,  name="core",  style="fill:#00d4ff;opacity:0.92")
print("✓ 同心圆装饰完成")

# ── 角落方框装饰 ─────────────────────────────────────────────────
for nx, ny in [(55,50),(1125,50),(55,605),(1125,605)]:
    shape_mod.add_rect(proj, x=nx, y=ny, width=20, height=20, rx=3,
                       style="fill:none;stroke:#00d4ff;stroke-width:1.5")

# 左侧竖线
shape_mod.add_rect(proj, x=60, y=80,  width=4, height=110, style="fill:#00d4ff;opacity:0.75")
shape_mod.add_rect(proj, x=72, y=100, width=2, height=75,  style="fill:#00d4ff;opacity:0.38")

# 分隔线
shape_mod.add_rect(proj, x=95, y=298, width=530, height=1, style="fill:#00d4ff;opacity:0.35")
print("✓ 几何装饰完成")

# ── 文字内容 ─────────────────────────────────────────────────────
text_mod.add_text(proj, text="CLI-Anything",
                  x=100, y=240, font_size=96, font_weight="bold",
                  fill="#ffffff", font_family="Arial")

text_mod.add_text(proj, text="Making ALL Software Agent-Native",
                  x=100, y=285, font_size=28,
                  fill="#00d4ff", font_family="Arial")

text_mod.add_text(proj, text="One command. Any software. Full agent control.",
                  x=100, y=355, font_size=22,
                  fill="#8888aa", font_family="Arial")
print("✓ 标题文字完成")

# ── 标签胶囊 ─────────────────────────────────────────────────────
tags = [
    (95,  408, 148, "#00d4ff", "MIT License"),
    (258, 408, 138, "#00d4ff", "14k+ Stars"),
    (410, 408, 155, "#e94560", "1508 Tests"),
    (580, 408, 138, "#a78bfa", "Python CLI"),
]
for tx, ty, tw, color, label in tags:
    shape_mod.add_rect(proj, x=tx, y=ty, width=tw, height=40, rx=20,
                       style=f"fill:{color};opacity:0.18;stroke:{color};stroke-width:1.5")
    text_mod.add_text(proj, text=label,
                      x=tx + tw//2, y=ty + 26, font_size=16,
                      fill=color, font_weight="bold", font_family="Arial", text_anchor="middle")
print("✓ 标签完成")

# 底部链接
text_mod.add_text(proj, text="github.com/HKUDS/CLI-Anything",
                  x=100, y=560, font_size=17, fill="#556677", font_family="Arial")
text_mod.add_text(proj, text="HKUDS Lab  ·  2026  ·  MIT License",
                  x=100, y=585, font_size=15, fill="#445566", font_family="Arial")

# 圆心 AI 字样
text_mod.add_text(proj, text="AI", x=950, y=355,
                  font_size=42, font_weight="bold",
                  fill="#0a0a18", font_family="Arial", text_anchor="middle")
print("✓ 全部元素添加完成")

# ── 保存项目 & 导出 ───────────────────────────────────────────────
doc_mod.save_document(proj, OUT_JSON)
print(f"✓ 项目已保存: {OUT_JSON}")

result_svg = export_mod.export_svg(proj, OUT_SVG, overwrite=True)
print(f"✓ SVG 导出: {OUT_SVG}  ({result_svg['size_bytes']} bytes)")

try:
    result_png = export_mod.render_to_png(proj, OUT_PNG, overwrite=True)
    print(f"✓ PNG 渲染: {OUT_PNG}  ({result_png['size_bytes']:,} bytes  {result_png['width']}x{result_png['height']})")
except Exception as e:
    # 尝试直接用 Inkscape 命令渲染 SVG
    import subprocess, os
    try:
        inkscape = r"C:\Program Files\Inkscape\bin\inkscape.exe"
        subprocess.run([inkscape, OUT_SVG, "--export-filename", OUT_PNG,
                        "--export-width", "1200", "--export-height", "675"], check=True)
        size = os.path.getsize(OUT_PNG)
        print(f"✓ PNG 渲染（Inkscape CLI）: {OUT_PNG}  ({size:,} bytes)")
    except Exception as e2:
        print(f"⚠ PNG 渲染失败: {e2}")

print("\n🎉 海报生成完毕！")
