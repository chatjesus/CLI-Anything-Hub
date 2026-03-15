#!/usr/bin/env python3
"""MS365 CLI 快速验证测试（不依赖 pytest，直接运行）"""

import subprocess
import sys
import os
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
CLI = [sys.executable, str(HERE / "ms365_cli.py")]


def run(args, check=True):
    result = subprocess.run(
        CLI + args, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=120
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"命令失败: {args}\nstderr: {result.stderr}")
    return result


def test_detect():
    print("▶ test_detect ... ", end="", flush=True)
    r = run(["--json", "detect"])
    data = json.loads(r.stdout)
    assert "com_word" in data, "缺少 com_word 字段"
    print("✓")
    return data


def test_version():
    print("▶ test_version ... ", end="", flush=True)
    r = run(["--json", "version"])
    data = json.loads(r.stdout)
    assert "version" in data
    print(f"✓  ({data.get('product')})")


def test_word_new_and_pdf():
    print("▶ test_word_new_and_pdf ... ", end="", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        docx = os.path.join(tmp, "test.docx")
        pdf  = os.path.join(tmp, "test.pdf")
        run(["--json", "word", "new", "-o", docx, "-t", "MS365 CLI Test",
             "--body", "This document was created by ms365_cli.py."])
        assert os.path.exists(docx), "docx 未生成"
        run(["word", "to-pdf", docx, "-o", pdf])
        assert os.path.exists(pdf), "PDF 未生成"
        with open(pdf, "rb") as f:
            assert f.read(4) == b"%PDF", "PDF 魔术字节错误"
        print(f"✓  ({os.path.getsize(pdf):,} bytes)")


def test_word_find_replace():
    print("▶ test_word_find_replace ... ", end="", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        docx = os.path.join(tmp, "fr.docx")
        run(["word", "new", "-o", docx, "-t", "Hello World",
             "--body", "Hello World is a common phrase."])
        run(["word", "find-replace", docx,
             "--find", "Hello World", "--replace", "MS365 CLI"])
        r = run(["--json", "word", "read", docx])
        data = json.loads(r.stdout)
        assert "MS365 CLI" in data.get("text_preview", ""), "替换未生效"
        print("✓")


def test_excel_new_write_read():
    print("▶ test_excel_new_write_read ... ", end="", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        xlsx = os.path.join(tmp, "test.xlsx")
        run(["excel", "new", "-o", xlsx, "--sheet", "数据"])
        run(["excel", "write-cell", xlsx, "--cell", "A1", "--value", "产品"])
        run(["excel", "write-cell", xlsx, "--cell", "B1", "--value", "100"])
        run(["excel", "write-cell", xlsx, "--cell", "A2", "--value", "MS365 CLI"])
        run(["excel", "write-cell", xlsx, "--cell", "B2", "--value", "42"])
        r = run(["--json", "excel", "read-range", xlsx,
                 "--range", "A1:B2", "--sheet", "数据"])
        data = json.loads(r.stdout)
        assert data["rows"] == 2, f"期望 2 行，实际 {data['rows']}"
        print("✓")


def test_excel_to_pdf():
    print("▶ test_excel_to_pdf ... ", end="", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        xlsx = os.path.join(tmp, "data.xlsx")
        pdf  = os.path.join(tmp, "data.pdf")
        run(["excel", "new", "-o", xlsx])
        run(["excel", "write-cell", xlsx, "--cell", "A1", "--value", "Test"])
        run(["excel", "to-pdf", xlsx, "-o", pdf])
        assert os.path.exists(pdf)
        with open(pdf, "rb") as f:
            assert f.read(4) == b"%PDF"
        print(f"✓  ({os.path.getsize(pdf):,} bytes)")


def test_powerpoint_new_and_pdf():
    print("▶ test_powerpoint_new_and_pdf ... ", end="", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        pptx = os.path.join(tmp, "test.pptx")
        pdf  = os.path.join(tmp, "test.pdf")
        run(["powerpoint", "new", "-o", pptx,
             "--title", "MS365 CLI Demo",
             "--subtitle", "PowerPoint COM Automation"])
        run(["powerpoint", "add-slide", pptx,
             "-t", "Slide 2", "--body", "Created via ms365_cli.py"])
        run(["powerpoint", "to-pdf", pptx, "-o", pdf])
        assert os.path.exists(pdf)
        with open(pdf, "rb") as f:
            assert f.read(4) == b"%PDF"
        print(f"✓  ({os.path.getsize(pdf):,} bytes)")


def test_convert():
    print("▶ test_convert (docx→pdf) ... ", end="", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        docx = os.path.join(tmp, "x.docx")
        pdf  = os.path.join(tmp, "x.pdf")
        run(["word", "new", "-o", docx, "-t", "Convert Test"])
        run(["convert", docx, pdf])
        assert os.path.exists(pdf)
        print("✓")


if __name__ == "__main__":
    print("=" * 55)
    print("MS365 CLI 测试套件")
    print("=" * 55)

    detect_data = test_detect()
    com_word = detect_data.get("com_word", "")
    if "✗" in com_word:
        print(f"\n⚠  Word COM 不可用: {com_word}")
        print("   跳过文档测试，仅运行 detect 和 version\n")
        test_version()
    else:
        test_version()
        test_word_new_and_pdf()
        test_word_find_replace()
        test_excel_new_write_read()
        test_excel_to_pdf()
        test_powerpoint_new_and_pdf()
        test_convert()

    print("\n✅ 所有测试通过！")
