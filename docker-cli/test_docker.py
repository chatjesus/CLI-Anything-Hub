"""
cli-anything-docker 快速验证测试
不依赖 pytest — 直接运行: python test_docker.py
需要 Docker Desktop / dockerd 正在运行。
"""
import json
import subprocess
import sys
import os
import time

CLI = [sys.executable, os.path.join(os.path.dirname(__file__), "docker_cli.py")]
PASS = 0
FAIL = 0
TEST_IMAGE = "hello-world"
TEST_CONTAINER = "clitest-hello"
TEST_NETWORK = "clitest-net"
TEST_VOLUME = "clitest-vol"


def run(args, check=True, timeout=120, use_json=False):
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
        fail("detect", f"Docker 未运行\n{result.stderr.strip()}")
        return False
    data = json.loads(result.stdout)
    assert data["status"] == "running", f"期望 running, 得到: {data}"
    ok(f"detect — Docker {data['version']}")
    return True


def test_version():
    result = run(["version"], use_json=True)
    data = json.loads(result.stdout)
    assert "Version" in data or "version" in data, f"缺少版本字段: {data}"
    ok("version — OK")


def test_system_info():
    result = run(["system", "info"], use_json=True)
    data = json.loads(result.stdout)
    assert "Containers" in data or "containers" in data.get("ContainersRunning", {}).__class__.__name__, \
        f"缺少容器信息: {list(data.keys())[:5]}"
    ok("system info — OK")


def test_system_df():
    result = run(["system", "df"], use_json=True)
    data = json.loads(result.stdout)
    assert "Images" in data or "Layers" in data, f"缺少磁盘信息: {list(data.keys())[:5]}"
    ok("system df — OK")


def test_image_pull():
    result = run(["image", "pull", TEST_IMAGE], use_json=False, timeout=120)
    ok(f"image pull {TEST_IMAGE}")


def test_image_list():
    result = run(["image", "list"], use_json=True)
    data = json.loads(result.stdout)
    assert "images" in data, f"缺少 images: {data}"
    ok(f"image list — {data['count']} 个镜像")
    return data["images"]


def test_image_inspect():
    result = run(["image", "inspect", TEST_IMAGE], use_json=True)
    data = json.loads(result.stdout)
    assert "Id" in data or "id" in data, f"缺少 Id: {list(data.keys())[:5]}"
    ok(f"image inspect {TEST_IMAGE}")


def test_image_tag():
    result = run(["image", "tag", TEST_IMAGE, f"{TEST_IMAGE}:cli-test"], use_json=True)
    data = json.loads(result.stdout)
    assert data.get("target") == f"{TEST_IMAGE}:cli-test", f"tag 结果异常: {data}"
    # cleanup tag
    run(["image", "remove", f"{TEST_IMAGE}:cli-test", "--force"])
    ok(f"image tag + cleanup")


def test_container_run():
    # Remove if exists from previous run
    run(["container", "remove", TEST_CONTAINER, "--force"], check=False)
    result = run(["container", "run", TEST_IMAGE, "--name", TEST_CONTAINER, "--remove"], use_json=True, timeout=60)
    data = json.loads(result.stdout)
    ok(f"container run {TEST_IMAGE} — {data.get('name', '?')}")


def test_container_list():
    result = run(["container", "list", "--all"], use_json=True)
    data = json.loads(result.stdout)
    assert "containers" in data, f"缺少 containers: {data}"
    ok(f"container list --all — {data['count']} 个容器")


def test_network_lifecycle():
    # Remove if exists
    run(["network", "remove", TEST_NETWORK], check=False)
    # Create
    result = run(["network", "create", TEST_NETWORK], use_json=True)
    data = json.loads(result.stdout)
    assert data["name"] == TEST_NETWORK, f"创建后名称不匹配: {data}"
    # List
    result2 = run(["network", "list"], use_json=True)
    nets = [n["name"] for n in json.loads(result2.stdout)["networks"]]
    assert TEST_NETWORK in nets, f"{TEST_NETWORK} 不在网络列表中"
    # Remove
    run(["network", "remove", TEST_NETWORK])
    ok(f"network create / list / remove")


def test_volume_lifecycle():
    # Remove if exists
    run(["volume", "remove", TEST_VOLUME], check=False)
    # Create
    result = run(["volume", "create", TEST_VOLUME], use_json=True)
    data = json.loads(result.stdout)
    assert data["name"] == TEST_VOLUME, f"创建后名称不匹配: {data}"
    # List
    result2 = run(["volume", "list"], use_json=True)
    vols = [v["name"] for v in json.loads(result2.stdout)["volumes"]]
    assert TEST_VOLUME in vols, f"{TEST_VOLUME} 不在卷列表中"
    # Remove
    run(["volume", "remove", TEST_VOLUME])
    ok(f"volume create / list / remove")


def main():
    print("=" * 60)
    print("  cli-anything-docker 测试套件")
    print("=" * 60)

    print("\n[1] 连接检测")
    alive = test_detect()
    if not alive:
        print("\n⚠  Docker 未运行，跳过后续测试。请启动 Docker Desktop。")
        sys.exit(1)

    print("\n[2] 系统信息")
    test_version()
    test_system_info()
    test_system_df()

    print("\n[3] 镜像操作")
    test_image_pull()
    test_image_list()
    test_image_inspect()
    test_image_tag()

    print("\n[4] 容器操作")
    test_container_run()
    test_container_list()

    print("\n[5] 网络操作")
    test_network_lifecycle()

    print("\n[6] 卷操作")
    test_volume_lifecycle()

    print("\n" + "=" * 60)
    print(f"  结果: {PASS} ✅ 通过   {FAIL} ❌ 失败")
    print("=" * 60)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
