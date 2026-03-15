"""
cli-anything-ollama 快速验证测试
不依赖 pytest — 直接运行: python test_ollama.py
需要 Ollama 已运行（ollama serve），且至少有一个已下载的模型。
"""
import json
import subprocess
import sys
import os

CLI = [sys.executable, os.path.join(os.path.dirname(__file__), "ollama_cli.py")]
PASS = 0
FAIL = 0


def run(args, check=True, timeout=120, use_json=False):
    """args: subcommand + its options/args. use_json puts --json at group level."""
    cmd = CLI[:]
    if use_json:
        cmd += ["--json"]
    cmd += args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
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
    """detect 命令：Ollama 需处于运行状态"""
    result = run(["detect"], check=False, use_json=True)
    if result.returncode != 0:
        fail("detect", f"Ollama 未运行或连接失败\n{result.stderr.strip()}")
        return False
    data = json.loads(result.stdout)
    assert data["status"] == "running", f"期望 running，得到: {data['status']}"
    ok("detect — Ollama running")
    return True


def test_version():
    """version 命令"""
    result = run(["version"], use_json=True)
    data = json.loads(result.stdout)
    assert "version" in data, f"缺少 version 字段: {data}"
    ok(f"version — {data['version']}")


def test_list():
    """list 命令，返回模型列表"""
    result = run(["list"], use_json=True)
    data = json.loads(result.stdout)
    assert "models" in data, f"缺少 models 字段: {data}"
    assert "count" in data, f"缺少 count 字段"
    ok(f"list — {data['count']} 个本地模型")
    return data["models"]


def test_show(model_name: str):
    """show 命令：获取模型详情"""
    result = run(["show", model_name], use_json=True)
    data = json.loads(result.stdout)
    assert "details" in data or "modelfile" in data, f"响应缺少必要字段: {list(data.keys())}"
    ok(f"show {model_name} — 详情正常")


def test_ps():
    """ps 命令：列出运行中模型"""
    result = run(["ps"], use_json=True)
    data = json.loads(result.stdout)
    assert "running" in data and "count" in data, f"缺少字段: {data}"
    ok(f"ps — 当前运行 {data['count']} 个模型")


def test_run(model_name: str):
    """run 命令：单次生成"""
    result = run(
        ["run", model_name, "Reply with exactly: PONG", "--max-tokens", "20"],
        use_json=True,
    )
    data = json.loads(result.stdout)
    assert "response" in data, f"缺少 response: {data}"
    assert len(data["response"]) > 0, "响应为空"
    ok(f"run {model_name} — 生成 {len(data['response'])} 字符")


def test_chat(model_name: str):
    """chat 命令：多轮对话"""
    result = run(
        ["chat", model_name, "--message", "user:Reply with exactly the word HELLO only.", "--max-tokens", "20"],
        use_json=True,
    )
    data = json.loads(result.stdout)
    assert "message" in data, f"缺少 message: {data}"
    content = data["message"].get("content", "")
    assert len(content) > 0, "对话回复为空"
    ok(f"chat {model_name} — 回复 {len(content)} 字符")


def test_embeddings(model_name: str):
    """embeddings 命令：生成向量"""
    result = run(["embeddings", model_name, "Hello world"], check=False, use_json=True)
    if result.returncode != 0:
        fail(f"embeddings {model_name}", "模型可能不支持嵌入向量")
        return
    data = json.loads(result.stdout)
    assert "embedding" in data, f"缺少 embedding: {data}"
    assert data["dimension"] > 0, "向量维度为 0"
    ok(f"embeddings {model_name} — 维度 {data['dimension']}")


def test_copy_delete(model_name: str):
    """copy + delete 命令"""
    alias = model_name.split(":")[0] + ":cli-test-copy"
    run(["copy", model_name, alias])
    # Verify alias exists
    result = run(["list"], use_json=True)
    models = json.loads(result.stdout)["models"]
    names = [m["name"] for m in models]
    assert alias in names, f"复制后未找到 {alias}，当前模型: {names}"
    # Delete alias
    run(["delete", alias, "--yes"])
    result2 = run(["list"], use_json=True)
    names2 = [m["name"] for m in json.loads(result2.stdout)["models"]]
    assert alias not in names2, f"删除后 {alias} 仍存在"
    ok(f"copy + delete — {model_name} → {alias} → 已清理")


def main():
    print("=" * 60)
    print("  cli-anything-ollama 测试套件")
    print("=" * 60)

    # Step 1: detect
    print("\n[1] 连接检测")
    alive = test_detect()
    if not alive:
        print("\n⚠  Ollama 未运行，后续测试跳过。请先执行: ollama serve")
        print(f"\n结果: {PASS} 通过, {FAIL} 失败")
        sys.exit(1 if FAIL else 0)

    # Step 2: version + list + ps
    print("\n[2] 服务器信息")
    test_version()
    test_ps()

    # Step 3: list and get a model to test against
    print("\n[3] 模型列表")
    models = test_list()
    if not models:
        print("\n⚠  没有已下载的模型，跳过生成/聊天/嵌入测试")
        print("    运行: ollama pull llama3.2  或  ollama pull qwen2.5:0.5b")
        print(f"\n结果: {PASS} 通过, {FAIL} 失败")
        sys.exit(0)

    model_name = models[0]["name"]
    print(f"    使用模型: {model_name}")

    # Step 4: show
    print("\n[4] 模型详情")
    test_show(model_name)

    # Step 5: run
    print("\n[5] 文本生成 (run)")
    test_run(model_name)

    # Step 6: chat
    print("\n[6] 多轮对话 (chat)")
    test_chat(model_name)

    # Step 7: embeddings (prefer a dedicated embed model if available)
    print("\n[7] 嵌入向量 (embeddings)")
    embed_candidates = [m["name"] for m in models if "embed" in m["name"].lower()]
    embed_model = embed_candidates[0] if embed_candidates else model_name
    test_embeddings(embed_model)

    # Step 8: copy + delete
    print("\n[8] 模型复制 & 删除")
    test_copy_delete(model_name)

    print("\n" + "=" * 60)
    print(f"  结果: {PASS} ✅ 通过   {FAIL} ❌ 失败")
    print("=" * 60)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
