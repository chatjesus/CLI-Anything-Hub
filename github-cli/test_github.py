"""
cli-anything-github 快速验证测试
不依赖 pytest — 直接运行: python test_github.py
需要 GITHUB_TOKEN 环境变量，或 --token 参数（会自动从环境读取）。
"""
import json
import subprocess
import sys
import os
import time

CLI = [sys.executable, os.path.join(os.path.dirname(__file__), "github_cli.py")]
PASS = 0
FAIL = 0
TEST_REPO_NAME = "cli-anything-test-repo"


def run(args, check=True, timeout=60, use_json=False):
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
        fail("detect", f"连接失败或 Token 无效\n{result.stderr.strip()[:200]}")
        return None
    data = json.loads(result.stdout)
    assert data["status"] == "ok", f"期望 ok: {data}"
    ok(f"detect — login={data['login']}")
    return data["login"]


def test_version():
    result = run(["version"], use_json=True)
    data = json.loads(result.stdout)
    assert "login" in data, f"缺少 login: {data}"
    ok(f"version — {data['login']} repos={data['public_repos']}")


def test_repo_list():
    result = run(["repo", "list", "--limit", "5"], use_json=True)
    data = json.loads(result.stdout)
    assert "repos" in data, f"缺少 repos: {data}"
    ok(f"repo list — {data['count']} 个仓库")
    return data["repos"]


def test_repo_create_delete(login: str):
    """创建测试仓库 → 验证 → 删除"""
    full_name = f"{login}/{TEST_REPO_NAME}"
    # Clean up from previous run
    run(["repo", "delete", full_name, "--yes"], check=False)
    time.sleep(1)
    # Create
    result = run(["repo", "create", TEST_REPO_NAME,
                  "--description", "cli-anything test repo",
                  "--auto-init"], use_json=True)
    data = json.loads(result.stdout)
    assert data["full_name"] == full_name, f"full_name 不匹配: {data}"
    ok(f"repo create — {full_name}")
    # Get
    result2 = run(["repo", "get", full_name], use_json=True)
    data2 = json.loads(result2.stdout)
    assert data2["full_name"] == full_name
    ok(f"repo get — {data2['stars']}★ {data2['language']}")
    return full_name


def test_issue_lifecycle(full_name: str):
    """创建 Issue → 评论 → 关闭"""
    # Create
    result = run(["issue", "create", full_name,
                  "--title", "CLI-Anything Test Issue",
                  "--body", "Automated test issue from cli-anything-github"], use_json=True)
    data = json.loads(result.stdout)
    assert "number" in data, f"缺少 number: {data}"
    num = data["number"]
    ok(f"issue create — #{num}")
    # Get
    result2 = run(["issue", "get", full_name, str(num)], use_json=True)
    data2 = json.loads(result2.stdout)
    assert data2["number"] == num
    ok(f"issue get — #{num}: {data2['title']}")
    # Comment
    result3 = run(["issue", "comment", full_name, str(num),
                   "--body", "Test comment from cli-anything"], use_json=True)
    data3 = json.loads(result3.stdout)
    assert "comment_id" in data3, f"缺少 comment_id: {data3}"
    ok(f"issue comment — id={data3['comment_id']}")
    # Close
    result4 = run(["issue", "close", full_name, str(num)], use_json=True)
    data4 = json.loads(result4.stdout)
    assert data4["state"] == "closed"
    ok(f"issue close — #{num} closed")
    # List
    result5 = run(["issue", "list", full_name, "--state", "closed"], use_json=True)
    data5 = json.loads(result5.stdout)
    nums = [i["number"] for i in data5["issues"]]
    assert num in nums, f"关闭后 #{num} 不在列表中"
    ok(f"issue list (closed) — {data5['count']} 个")


def test_release_lifecycle(full_name: str):
    """创建 Release → 列表"""
    result = run(["release", "create", full_name,
                  "--tag", "v0.0.1-test",
                  "--name", "Test Release",
                  "--body", "CLI-Anything automated test release",
                  "--prerelease"], use_json=True)
    data = json.loads(result.stdout)
    assert data.get("tag") == "v0.0.1-test", f"tag 不匹配: {data}"
    ok(f"release create — {data['tag']}")
    # List
    result2 = run(["release", "list", full_name], use_json=True)
    data2 = json.loads(result2.stdout)
    assert data2["count"] >= 1, "release list 为空"
    ok(f"release list — {data2['count']} 个 release")


def test_actions_list(full_name: str):
    """列出 Workflows（新仓库可能为空）"""
    result = run(["actions", "list-workflows", full_name], use_json=True)
    data = json.loads(result.stdout)
    assert "workflows" in data
    ok(f"actions list-workflows — {data['count']} 个工作流")


def test_gist():
    """创建 Gist"""
    result = run(["gist", "create",
                  "--file", "hello.txt:Hello from cli-anything-github!",
                  "--description", "CLI-Anything test gist"], use_json=True)
    data = json.loads(result.stdout)
    assert "id" in data and "url" in data, f"缺少 id/url: {data}"
    ok(f"gist create — {data['id'][:12]}...")


def cleanup(full_name: str):
    run(["repo", "delete", full_name, "--yes"], check=False)
    ok(f"cleanup — {full_name} deleted")


def main():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    print("=" * 60)
    print("  cli-anything-github 测试套件")
    print("=" * 60)
    if not token:
        print("\n⚠  未设置 GITHUB_TOKEN 环境变量，跳过所有测试。")
        print("    export GITHUB_TOKEN=ghp_xxxxxxxxxxxx")
        sys.exit(0)

    print("\n[1] 连接检测")
    login = test_detect()
    if login is None:
        print("\n⚠  GitHub API 不可用")
        sys.exit(1)

    print("\n[2] 版本信息")
    test_version()

    print("\n[3] 仓库列表")
    repos = test_repo_list()

    print("\n[4] 仓库创建 / 查询 / 删除")
    try:
        full_name = test_repo_create_delete(login)
    except Exception as e:
        fail("repo create/delete", str(e))
        print(f"\n结果: {PASS} 通过, {FAIL} 失败")
        sys.exit(1 if FAIL else 0)

    print("\n[5] Issue 完整流程")
    try:
        test_issue_lifecycle(full_name)
    except Exception as e:
        fail("issue lifecycle", str(e))

    print("\n[6] Release")
    try:
        test_release_lifecycle(full_name)
    except Exception as e:
        fail("release lifecycle", str(e))

    print("\n[7] Actions Workflows")
    try:
        test_actions_list(full_name)
    except Exception as e:
        fail("actions list", str(e))

    print("\n[8] Gist")
    try:
        test_gist()
    except Exception as e:
        fail("gist create", str(e))

    print("\n[9] 清理测试仓库")
    cleanup(full_name)

    print("\n" + "=" * 60)
    print(f"  结果: {PASS} ✅ 通过   {FAIL} ❌ 失败")
    print("=" * 60)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
