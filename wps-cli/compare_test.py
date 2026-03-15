#!/usr/bin/env python3
"""
对比测试：WPS CLI  vs  LibreOffice CLI
完成相同的 3 个任务，对比速度、文件大小、PDF 质量
"""
import sys, os, time, subprocess, json
sys.path.insert(0, os.path.dirname(__file__))

OUT = r"C:\Users\PRO\Desktop\CUDA\CLI-Anything\compare_output"
os.makedirs(OUT, exist_ok=True)

WPS_CLI  = [sys.executable, r"C:\Users\PRO\Desktop\CUDA\CLI-Anything\wps-cli\wps_cli.py"]
LO_CLI   = ["cli-anything-libreoffice"]

results = []

def run(label, cmd, check_output=None):
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    elapsed = round((time.time() - t0) * 1000)
    ok = r.returncode == 0
    size = os.path.getsize(check_output) if check_output and os.path.exists(check_output) else 0
    # 验证PDF魔术字节
    valid_pdf = False
    if check_output and check_output.endswith(".pdf") and os.path.exists(check_output):
        with open(check_output, "rb") as f:
            valid_pdf = f.read(4) == b"%PDF"
    entry = {
        "label": label, "ok": ok, "ms": elapsed,
        "size_bytes": size, "valid_pdf": valid_pdf,
        "stdout": r.stdout.strip()[:200],
        "stderr": r.stderr.strip()[:100] if r.stderr else ""
    }
    results.append(entry)
    status = "✓" if ok else "✗"
    print(f"  {status} {label:35s} {elapsed:5d}ms  {size//1024:4d}KB  {'PDF✓' if valid_pdf else '    '}")
    return ok

print("=" * 70)
print("对比测试：WPS CLI  vs  LibreOffice CLI")
print("=" * 70)

# ── 任务 1：新建 Writer/Writer 文档 ─────────────────────────────
print("\n【任务 1】新建文字文档")
wps_doc  = os.path.join(OUT, "wps_doc.docx")
lo_doc   = os.path.join(OUT, "lo_doc.json")

run("WPS  writer new",
    WPS_CLI + ["writer", "new", "-o", wps_doc, "-t", "WPS CLI 测试文档"],
    wps_doc)

run("LO   document new",
    LO_CLI + ["document", "new", "--type", "writer", "-o", lo_doc],
    lo_doc)

# ── 任务 2：导出 PDF ─────────────────────────────────────────────
print("\n【任务 2】导出为 PDF（真实渲染）")
wps_pdf = os.path.join(OUT, "wps_output.pdf")
lo_pdf  = os.path.join(OUT, "lo_output.pdf")

run("WPS  writer to-pdf",
    WPS_CLI + ["writer", "to-pdf", wps_doc, "-o", wps_pdf],
    wps_pdf)

run("LO   export render pdf",
    LO_CLI + ["--project", lo_doc, "export", "render", lo_pdf, "-p", "pdf", "--overwrite"],
    lo_pdf)

# ── 任务 3：新建表格 ─────────────────────────────────────────────
print("\n【任务 3】新建表格文件")
wps_xls = os.path.join(OUT, "wps_table.xlsx")
lo_xls  = os.path.join(OUT, "lo_table.json")

run("WPS  calc new",
    WPS_CLI + ["calc", "new", "-o", wps_xls, "--sheet", "销售数据"],
    wps_xls)

run("LO   document new calc",
    LO_CLI + ["document", "new", "--type", "calc", "-o", lo_xls],
    lo_xls)

# ── 汇总 ────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("汇总结果")
print("=" * 70)
wps_r = [r for r in results if r["label"].startswith("WPS")]
lo_r  = [r for r in results if r["label"].startswith("LO")]

wps_ok    = sum(1 for r in wps_r if r["ok"])
lo_ok     = sum(1 for r in lo_r  if r["ok"])
wps_total = sum(r["ms"] for r in wps_r)
lo_total  = sum(r["ms"] for r in lo_r)

print(f"\n  WPS CLI    : {wps_ok}/{len(wps_r)} 成功  总耗时 {wps_total}ms")
print(f"  LibreOffice: {lo_ok}/{len(lo_r)} 成功  总耗时 {lo_total}ms")

print("\n  输出文件列表:")
for f in os.listdir(OUT):
    fp = os.path.join(OUT, f)
    sz = os.path.getsize(fp)
    print(f"    {f:35s} {sz:8,} bytes")

# 保存 JSON 报告
with open(os.path.join(OUT, "compare_report.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\n  详细报告: {OUT}\\compare_report.json")
print("=" * 70)
