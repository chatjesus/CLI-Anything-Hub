"""
cli-anything-notion 快速验证测试
用法: python test_notion.py [PARENT_PAGE_ID]
需要 NOTION_TOKEN 环境变量。PARENT_PAGE_ID 用于创建测试页面（需已分享给集成）。
"""
import json
import subprocess
import sys
import os

CLI = [sys.executable, os.path.join(os.path.dirname(__file__), "notion_cli.py")]
PASS = 0
FAIL = 0


def run(args, check=True, timeout=30, use_json=False):
    cmd = CLI[:]
    if use_json:
        cmd += ["--json"]
    cmd += args
    result = subprocess.run(
        cmd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"命令失败: {cmd}\nstdout: {result.stdout}\nstderr: {result.stderr}")
    return result


def ok(name):
    global PASS
    PASS += 1
    print(f"  ✅ {name}")


def fail(name, reason):
    global FAIL
    FAIL += 1
    print(f"  ❌ {name}: {reason}")


def test_detect():
    result = run(["detect"], check=False, use_json=True)
    if result.returncode != 0:
        fail("detect", result.stderr.strip()[:200])
        return False
    data = json.loads(result.stdout)
    assert data["status"] == "ok", f"期望 ok: {data}"
    ok(f"detect — bot={data['bot_name']} workspace={data['workspace_name']}")
    return True


def test_version():
    result = run(["version"], use_json=True)
    data = json.loads(result.stdout)
    assert "api_version" in data, f"缺少 api_version: {data}"
    ok(f"version — {data['api_version']}")


def test_users_me():
    result = run(["users", "me"], use_json=True)
    data = json.loads(result.stdout)
    assert "id" in data, f"缺少 id: {data}"
    ok(f"users me — {data.get('name', '?')}")


def test_users_list():
    result = run(["users", "list"], use_json=True)
    data = json.loads(result.stdout)
    assert "users" in data, f"缺少 users: {data}"
    ok(f"users list — {data['count']} 个成员")


def test_search():
    result = run(["search", "a", "--limit", "5"], use_json=True)
    data = json.loads(result.stdout)
    assert "results" in data, f"缺少 results: {data}"
    ok(f"search — {data['count']} 个结果")


def test_page_lifecycle(parent_page_id: str):
    """完整 page 流程"""
    # Create
    result = run([
        "page", "create",
        "--parent-page", parent_page_id,
        "--title", "CLI-Anything Test Page",
        "--content", "This is an automated test page.",
    ], use_json=True)
    data = json.loads(result.stdout)
    assert "id" in data, f"缺少 id: {data}"
    page_id = data["id"]
    ok(f"page create — {page_id[:8]}...")

    # Get
    result2 = run(["page", "get", page_id], use_json=True)
    data2 = json.loads(result2.stdout)
    assert data2["id"] == page_id
    ok(f"page get — title confirmed")

    # Append text
    result3 = run(["page", "append-text", page_id, "## Test Heading",
                   "--type", "heading_2"], use_json=True)
    data3 = json.loads(result3.stdout)
    assert data3["added_blocks"] >= 1
    ok(f"page append-text heading_2")

    result4 = run(["page", "append-text", page_id, "A bullet point",
                   "--type", "bulleted_list_item"], use_json=True)
    ok(f"page append-text bulleted_list_item")

    # Block children
    result5 = run(["block", "children", page_id], use_json=True)
    data5 = json.loads(result5.stdout)
    assert data5["count"] >= 1, f"子 block 为空"
    ok(f"block children — {data5['count']} 个 block")

    # Update title
    result6 = run(["page", "update-title", page_id, "CLI-Anything Test (Updated)"], use_json=True)
    ok(f"page update-title")

    # Archive
    result7 = run(["page", "archive", page_id], use_json=True)
    data7 = json.loads(result7.stdout)
    assert data7["archived"] == True
    ok(f"page archive — archived=True")

    return page_id


def main():
    parent_page_id = sys.argv[1] if len(sys.argv) > 1 else None
    token = os.environ.get("NOTION_TOKEN") or os.environ.get("NOTION_API_KEY")

    print("=" * 60)
    print("  cli-anything-notion 测试套件")
    print("=" * 60)

    if not token:
        print("\n⚠  未设置 NOTION_TOKEN，跳过所有测试。")
        print("    export NOTION_TOKEN=secret_xxx")
        sys.exit(0)

    print("\n[1] 连接检测")
    alive = test_detect()
    if not alive:
        sys.exit(1)

    print("\n[2] 版本信息")
    test_version()

    print("\n[3] 用户信息")
    test_users_me()
    test_users_list()

    print("\n[4] 搜索")
    test_search()

    if parent_page_id:
        print(f"\n[5] Page 完整流程（parent={parent_page_id[:8]}...）")
        try:
            test_page_lifecycle(parent_page_id)
        except Exception as e:
            fail("page lifecycle", str(e))
    else:
        print("\n[5] Page 流程（跳过，未提供 PARENT_PAGE_ID）")
        print("    用法: python test_notion.py <parent_page_id>")

    print("\n" + "=" * 60)
    print(f"  结果: {PASS} ✅ 通过   {FAIL} ❌ 失败")
    print("=" * 60)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
