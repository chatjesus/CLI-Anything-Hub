"""
cli-anything-docker — Docker engine CLI
Wraps Docker Python SDK (docker) and docker-compose for AI Agent use.
"""
import json
import sys
import os
from typing import Optional

import click

try:
    import docker as docker_sdk
    from docker.errors import DockerException, NotFound, APIError, ImageNotFound
    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False


# ─── helpers ─────────────────────────────────────────────────────────────────

def _client():
    if not _SDK_AVAILABLE:
        raise click.ClickException(
            "docker SDK 未安装，请运行: pip install docker"
        )
    try:
        c = docker_sdk.from_env()
        c.ping()
        return c
    except Exception as e:
        raise click.ClickException(
            f"无法连接 Docker daemon: {e}\n"
            "请确认 Docker Desktop / dockerd 正在运行。"
        )


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        if isinstance(data, str):
            click.echo(data)
        elif isinstance(data, list):
            for item in data:
                click.echo(item if isinstance(item, str) else json.dumps(item, ensure_ascii=False))
        else:
            click.echo(str(data))


def _size_str(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


# ─── root ─────────────────────────────────────────────────────────────────────

@click.group()
@click.option("--json", "as_json", is_flag=True, help="以 JSON 格式输出（Agent 友好）")
@click.pass_context
def cli(ctx, as_json):
    """cli-anything-docker — Docker 引擎 CLI\n
    管理容器、镜像、网络、卷，并支持 docker compose。
    """
    ctx.ensure_object(dict)
    ctx.obj["json"] = as_json


# ─── detect ───────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def detect(ctx):
    """检测 Docker daemon 是否可用并返回版本信息。"""
    as_json = ctx.obj["json"]
    if not _SDK_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install docker"}
        _out(result, as_json) if as_json else click.echo("❌ docker SDK 未安装：pip install docker")
        sys.exit(1)
    try:
        c = _client()
        info = c.version()
        result = {
            "status": "running",
            "version": info.get("Version", "unknown"),
            "api_version": info.get("ApiVersion", "unknown"),
            "os": info.get("Os", "unknown"),
            "arch": info.get("Arch", "unknown"),
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ Docker running  version={result['version']}  api={result['api_version']}  {result['os']}/{result['arch']}")
    except click.ClickException as e:
        result = {"status": "not_running", "error": str(e)}
        _out(result, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


# ─── version ──────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def version(ctx):
    """显示 Docker 版本信息。"""
    c = _client()
    info = c.version()
    as_json = ctx.obj["json"]
    if as_json:
        _out(info, True)
    else:
        click.echo(f"Docker:    {info.get('Version', '?')}")
        click.echo(f"API:       {info.get('ApiVersion', '?')}")
        click.echo(f"Go:        {info.get('GoVersion', '?')}")
        click.echo(f"Platform:  {info.get('Os', '?')}/{info.get('Arch', '?')}")


# ══════════════════════════════════════════════════════════════════════════════
# CONTAINERS
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def container():
    """容器管理（list / run / start / stop / remove / logs / exec / inspect）。"""


@container.command(name="list")
@click.option("--all", "-a", "show_all", is_flag=True, help="包含已停止的容器")
@click.pass_context
def container_list(ctx, show_all):
    """列出容器。"""
    c = _client()
    as_json = ctx.obj["json"]
    containers = c.containers.list(all=show_all)
    data = [
        {
            "id": ct.short_id,
            "name": ct.name,
            "image": ct.image.tags[0] if ct.image.tags else ct.image.short_id,
            "status": ct.status,
            "ports": ct.ports,
        }
        for ct in containers
    ]
    if as_json:
        _out({"containers": data, "count": len(data)}, True)
    else:
        if not data:
            click.echo("（无容器）")
            return
        click.echo(f"{'ID':<14} {'NAME':<28} {'IMAGE':<35} STATUS")
        click.echo("─" * 90)
        for d in data:
            click.echo(f"{d['id']:<14} {d['name']:<28} {d['image']:<35} {d['status']}")


@container.command(name="run")
@click.argument("image")
@click.option("--name", default=None, help="容器名称")
@click.option("--cmd", "-c", default=None, help="覆盖默认 CMD")
@click.option("--env", "-e", multiple=True, help="环境变量（KEY=VALUE）")
@click.option("--port", "-p", multiple=True, help="端口映射（host:container）")
@click.option("--volume", "-v", multiple=True, help="卷挂载（host_path:container_path）")
@click.option("--detach/--foreground", default=True, show_default=True, help="后台运行")
@click.option("--remove", is_flag=True, help="容器退出后自动删除")
@click.option("--network", default=None, help="指定网络")
@click.pass_context
def container_run(ctx, image, name, cmd, env, port, volume, detach, remove, network):
    """运行容器。\n
    示例: docker-cli container run nginx --port 8080:80 --detach
    """
    c = _client()
    as_json = ctx.obj["json"]
    ports = {}
    for p in port:
        host_p, container_p = p.split(":", 1)
        ports[container_p] = int(host_p)
    vols = {}
    for vol in volume:
        parts = vol.split(":", 1)
        vols[parts[0]] = {"bind": parts[1], "mode": "rw"} if len(parts) > 1 else {"bind": parts[0], "mode": "rw"}
    env_dict = {}
    for e in env:
        k, v = e.split("=", 1)
        env_dict[k] = v
    kwargs = dict(
        image=image,
        name=name,
        command=cmd,
        environment=env_dict or None,
        ports=ports or None,
        volumes=vols or None,
        detach=detach,
        remove=remove,
        network=network,
    )
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    ct = c.containers.run(**kwargs)
    if detach:
        result = {"id": ct.short_id, "name": ct.name, "status": ct.status, "image": image}
        if as_json:
            _out(result, True)
        else:
            click.echo(f"🚀 {ct.name} ({ct.short_id}) started")
    else:
        output = ct.decode() if isinstance(ct, bytes) else str(ct)
        if as_json:
            _out({"output": output}, True)
        else:
            click.echo(output)


@container.command(name="start")
@click.argument("container_id")
@click.pass_context
def container_start(ctx, container_id):
    """启动已停止的容器。"""
    c = _client()
    as_json = ctx.obj["json"]
    ct = c.containers.get(container_id)
    ct.start()
    result = {"id": ct.short_id, "name": ct.name, "status": "started"}
    _out(result, as_json) if as_json else click.echo(f"▶  {ct.name} started")


@container.command(name="stop")
@click.argument("container_id")
@click.option("--timeout", default=10, show_default=True, type=int, help="等待秒数")
@click.pass_context
def container_stop(ctx, container_id, timeout):
    """停止容器。"""
    c = _client()
    as_json = ctx.obj["json"]
    ct = c.containers.get(container_id)
    ct.stop(timeout=timeout)
    result = {"id": ct.short_id, "name": ct.name, "status": "stopped"}
    _out(result, as_json) if as_json else click.echo(f"⏹  {ct.name} stopped")


@container.command(name="restart")
@click.argument("container_id")
@click.pass_context
def container_restart(ctx, container_id):
    """重启容器。"""
    c = _client()
    as_json = ctx.obj["json"]
    ct = c.containers.get(container_id)
    ct.restart()
    result = {"id": ct.short_id, "name": ct.name, "status": "restarted"}
    _out(result, as_json) if as_json else click.echo(f"🔄 {ct.name} restarted")


@container.command(name="remove")
@click.argument("container_id")
@click.option("--force", "-f", is_flag=True, help="强制删除运行中容器")
@click.pass_context
def container_remove(ctx, container_id, force):
    """删除容器。"""
    c = _client()
    as_json = ctx.obj["json"]
    ct = c.containers.get(container_id)
    name = ct.name
    short_id = ct.short_id
    ct.remove(force=force)
    result = {"id": short_id, "name": name, "status": "removed"}
    _out(result, as_json) if as_json else click.echo(f"🗑  {name} removed")


@container.command(name="logs")
@click.argument("container_id")
@click.option("--tail", default=100, show_default=True, type=int, help="最后 N 行")
@click.option("--timestamps", is_flag=True, help="显示时间戳")
@click.pass_context
def container_logs(ctx, container_id, tail, timestamps):
    """获取容器日志。"""
    c = _client()
    as_json = ctx.obj["json"]
    ct = c.containers.get(container_id)
    log_bytes = ct.logs(tail=tail, timestamps=timestamps)
    log_text = log_bytes.decode("utf-8", errors="replace")
    if as_json:
        _out({"container": ct.name, "logs": log_text}, True)
    else:
        click.echo(log_text)


@container.command(name="exec")
@click.argument("container_id")
@click.argument("command", nargs=-1, required=True)
@click.pass_context
def container_exec(ctx, container_id, command):
    """在运行中的容器内执行命令。\n
    示例: docker-cli container exec mycontainer ls /app
    """
    c = _client()
    as_json = ctx.obj["json"]
    ct = c.containers.get(container_id)
    exit_code, output = ct.exec_run(list(command))
    out_text = output.decode("utf-8", errors="replace") if output else ""
    if as_json:
        _out({"exit_code": exit_code, "output": out_text}, True)
    else:
        click.echo(out_text)
        if exit_code != 0:
            sys.exit(exit_code)


@container.command(name="inspect")
@click.argument("container_id")
@click.pass_context
def container_inspect(ctx, container_id):
    """获取容器详细信息（JSON）。"""
    c = _client()
    ct = c.containers.get(container_id)
    attrs = ct.attrs
    as_json = ctx.obj["json"]
    if as_json:
        _out(attrs, True)
    else:
        keys = ["Id", "Name", "State", "Config", "NetworkSettings", "Mounts"]
        for k in keys:
            if k in attrs:
                click.echo(f"── {k} ──")
                click.echo(json.dumps(attrs[k], indent=2, ensure_ascii=False))


@container.command(name="stats")
@click.argument("container_id")
@click.pass_context
def container_stats(ctx, container_id):
    """获取容器实时资源使用情况（单次快照）。"""
    c = _client()
    as_json = ctx.obj["json"]
    ct = c.containers.get(container_id)
    st = ct.stats(stream=False)
    # Compute CPU %
    cpu_delta = st["cpu_stats"]["cpu_usage"]["total_usage"] - st["precpu_stats"]["cpu_usage"]["total_usage"]
    sys_delta = st["cpu_stats"].get("system_cpu_usage", 0) - st["precpu_stats"].get("system_cpu_usage", 0)
    num_cpus = st["cpu_stats"].get("online_cpus") or len(st["cpu_stats"]["cpu_usage"].get("percpu_usage", [1]))
    cpu_pct = (cpu_delta / sys_delta * num_cpus * 100.0) if sys_delta > 0 else 0.0
    mem_usage = st["memory_stats"].get("usage", 0)
    mem_limit = st["memory_stats"].get("limit", 1)
    mem_pct = mem_usage / mem_limit * 100
    result = {
        "container": ct.name,
        "cpu_percent": round(cpu_pct, 2),
        "memory_usage": _size_str(mem_usage),
        "memory_limit": _size_str(mem_limit),
        "memory_percent": round(mem_pct, 2),
    }
    if as_json:
        _out(result, True)
    else:
        click.echo(f"CPU:    {result['cpu_percent']:.2f}%")
        click.echo(f"Memory: {result['memory_usage']} / {result['memory_limit']} ({result['memory_percent']:.2f}%)")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGES
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def image():
    """镜像管理（list / pull / push / build / remove / inspect / tag）。"""


@image.command(name="list")
@click.pass_context
def image_list(ctx):
    """列出本地镜像。"""
    c = _client()
    as_json = ctx.obj["json"]
    images = c.images.list()
    data = [
        {
            "id": img.short_id.replace("sha256:", ""),
            "tags": img.tags,
            "size": _size_str(img.attrs.get("Size", 0)),
            "created": img.attrs.get("Created", "")[:10],
        }
        for img in images
    ]
    if as_json:
        _out({"images": data, "count": len(data)}, True)
    else:
        if not data:
            click.echo("（无本地镜像）")
            return
        click.echo(f"{'TAG':<45} {'SIZE':>10}  CREATED")
        click.echo("─" * 70)
        for d in data:
            tags = d["tags"] or ["<none>"]
            for tag in tags:
                click.echo(f"{tag:<45} {d['size']:>10}  {d['created']}")


@image.command(name="pull")
@click.argument("image_name")
@click.pass_context
def image_pull(ctx, image_name):
    """拉取镜像（支持流式进度）。"""
    c = _client()
    as_json = ctx.obj["json"]
    if not as_json:
        click.echo(f"⬇  Pulling {image_name} ...")
    layers = {}
    for event in c.api.pull(image_name, stream=True, decode=True):
        if as_json:
            click.echo(json.dumps(event, ensure_ascii=False))
        else:
            status = event.get("status", "")
            layer = event.get("id", "")
            progress = event.get("progressDetail", {})
            if progress.get("total"):
                pct = int(progress["current"] / progress["total"] * 100) if progress.get("current") else 0
                if layer not in layers or layers[layer] != pct:
                    layers[layer] = pct
    if not as_json:
        click.echo(f"✅ Pulled: {image_name}")


@image.command(name="build")
@click.argument("path", default=".")
@click.option("--tag", "-t", default=None, help="镜像标签（name:tag）")
@click.option("--file", "-f", "dockerfile", default=None, help="Dockerfile 路径")
@click.option("--no-cache", is_flag=True, help="禁用缓存")
@click.pass_context
def image_build(ctx, path, tag, dockerfile, no_cache):
    """从 Dockerfile 构建镜像。"""
    c = _client()
    as_json = ctx.obj["json"]
    if not as_json:
        click.echo(f"🔨 Building {tag or 'image'} from {path} ...")
    kwargs = {"path": path, "nocache": no_cache, "rm": True}
    if tag:
        kwargs["tag"] = tag
    if dockerfile:
        kwargs["dockerfile"] = dockerfile
    image_obj, logs = c.images.build(**kwargs)
    for log in logs:
        line = log.get("stream", "").rstrip()
        if line:
            if as_json:
                click.echo(json.dumps(log, ensure_ascii=False))
            else:
                click.echo(f"  {line}")
    result = {"id": image_obj.short_id, "tags": image_obj.tags}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"✅ Built: {image_obj.short_id}  tags={image_obj.tags}")


@image.command(name="remove")
@click.argument("image_name")
@click.option("--force", "-f", is_flag=True)
@click.pass_context
def image_remove(ctx, image_name, force):
    """删除本地镜像。"""
    c = _client()
    as_json = ctx.obj["json"]
    c.images.remove(image_name, force=force)
    result = {"removed": image_name}
    _out(result, as_json) if as_json else click.echo(f"🗑  Removed: {image_name}")


@image.command(name="tag")
@click.argument("source")
@click.argument("target")
@click.pass_context
def image_tag(ctx, source, target):
    """为镜像打标签。"""
    c = _client()
    as_json = ctx.obj["json"]
    img = c.images.get(source)
    repo, tag = target.rsplit(":", 1) if ":" in target else (target, "latest")
    img.tag(repo, tag=tag)
    result = {"source": source, "target": target}
    _out(result, as_json) if as_json else click.echo(f"🏷  Tagged: {source} → {target}")


@image.command(name="inspect")
@click.argument("image_name")
@click.pass_context
def image_inspect(ctx, image_name):
    """获取镜像详细信息。"""
    c = _client()
    as_json = ctx.obj["json"]
    img = c.images.get(image_name)
    if as_json:
        _out(img.attrs, True)
    else:
        a = img.attrs
        click.echo(f"ID:          {img.short_id}")
        click.echo(f"Tags:        {img.tags}")
        click.echo(f"Created:     {a.get('Created', '')[:19]}")
        click.echo(f"Size:        {_size_str(a.get('Size', 0))}")
        click.echo(f"OS/Arch:     {a.get('Os', '?')}/{a.get('Architecture', '?')}")
        click.echo(f"Entrypoint:  {a.get('Config', {}).get('Entrypoint')}")
        click.echo(f"Cmd:         {a.get('Config', {}).get('Cmd')}")


# ══════════════════════════════════════════════════════════════════════════════
# VOLUMES
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def volume():
    """卷管理（list / create / remove / inspect）。"""


@volume.command(name="list")
@click.pass_context
def volume_list(ctx):
    """列出所有卷。"""
    c = _client()
    as_json = ctx.obj["json"]
    vols = c.volumes.list()
    data = [{"name": v.name, "driver": v.attrs.get("Driver", "local"), "mountpoint": v.attrs.get("Mountpoint", "")} for v in vols]
    if as_json:
        _out({"volumes": data, "count": len(data)}, True)
    else:
        if not data:
            click.echo("（无卷）")
            return
        click.echo(f"{'NAME':<45} {'DRIVER':<12} MOUNTPOINT")
        click.echo("─" * 100)
        for d in data:
            click.echo(f"{d['name']:<45} {d['driver']:<12} {d['mountpoint']}")


@volume.command(name="create")
@click.argument("name", required=False, default=None)
@click.option("--driver", default="local")
@click.pass_context
def volume_create(ctx, name, driver):
    """创建卷。"""
    c = _client()
    as_json = ctx.obj["json"]
    v = c.volumes.create(name=name, driver=driver)
    result = {"name": v.name, "driver": v.attrs.get("Driver")}
    _out(result, as_json) if as_json else click.echo(f"✅ Volume created: {v.name}")


@volume.command(name="remove")
@click.argument("name")
@click.option("--force", "-f", is_flag=True)
@click.pass_context
def volume_remove(ctx, name, force):
    """删除卷。"""
    c = _client()
    as_json = ctx.obj["json"]
    v = c.volumes.get(name)
    v.remove(force=force)
    result = {"name": name, "status": "removed"}
    _out(result, as_json) if as_json else click.echo(f"🗑  Volume removed: {name}")


# ══════════════════════════════════════════════════════════════════════════════
# NETWORKS
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def network():
    """网络管理（list / create / remove / inspect / connect / disconnect）。"""


@network.command(name="list")
@click.pass_context
def network_list(ctx):
    """列出所有网络。"""
    c = _client()
    as_json = ctx.obj["json"]
    nets = c.networks.list()
    data = [{"id": n.short_id, "name": n.name, "driver": n.attrs.get("Driver", ""), "scope": n.attrs.get("Scope", "")} for n in nets]
    if as_json:
        _out({"networks": data, "count": len(data)}, True)
    else:
        click.echo(f"{'NAME':<30} {'DRIVER':<12} SCOPE")
        click.echo("─" * 60)
        for d in data:
            click.echo(f"{d['name']:<30} {d['driver']:<12} {d['scope']}")


@network.command(name="create")
@click.argument("name")
@click.option("--driver", default="bridge", show_default=True)
@click.pass_context
def network_create(ctx, name, driver):
    """创建网络。"""
    c = _client()
    as_json = ctx.obj["json"]
    n = c.networks.create(name, driver=driver)
    result = {"id": n.short_id, "name": n.name, "driver": driver}
    _out(result, as_json) if as_json else click.echo(f"✅ Network created: {n.name} ({n.short_id})")


@network.command(name="remove")
@click.argument("name")
@click.pass_context
def network_remove(ctx, name):
    """删除网络。"""
    c = _client()
    as_json = ctx.obj["json"]
    n = c.networks.get(name)
    n.remove()
    result = {"name": name, "status": "removed"}
    _out(result, as_json) if as_json else click.echo(f"🗑  Network removed: {name}")


@network.command(name="connect")
@click.argument("network_name")
@click.argument("container_id")
@click.pass_context
def network_connect(ctx, network_name, container_id):
    """将容器加入网络。"""
    c = _client()
    as_json = ctx.obj["json"]
    n = c.networks.get(network_name)
    n.connect(container_id)
    result = {"network": network_name, "container": container_id, "action": "connected"}
    _out(result, as_json) if as_json else click.echo(f"🔗 {container_id} → {network_name}")


@network.command(name="disconnect")
@click.argument("network_name")
@click.argument("container_id")
@click.pass_context
def network_disconnect(ctx, network_name, container_id):
    """将容器从网络移除。"""
    c = _client()
    as_json = ctx.obj["json"]
    n = c.networks.get(network_name)
    n.disconnect(container_id)
    result = {"network": network_name, "container": container_id, "action": "disconnected"}
    _out(result, as_json) if as_json else click.echo(f"🔌 {container_id} ⇥ {network_name}")


# ══════════════════════════════════════════════════════════════════════════════
# SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def system():
    """系统管理（info / prune / df）。"""


@system.command(name="info")
@click.pass_context
def system_info(ctx):
    """显示 Docker 系统信息。"""
    c = _client()
    as_json = ctx.obj["json"]
    info = c.info()
    if as_json:
        _out(info, True)
    else:
        fields = [
            ("Containers", info.get("Containers")),
            ("Running", info.get("ContainersRunning")),
            ("Images", info.get("Images")),
            ("Storage Driver", info.get("Driver")),
            ("Memory", _size_str(info.get("MemTotal", 0))),
            ("CPUs", info.get("NCPU")),
            ("OS", info.get("OperatingSystem")),
            ("Kernel", info.get("KernelVersion")),
        ]
        for k, v in fields:
            click.echo(f"  {k:<20} {v}")


@system.command(name="prune")
@click.option("--volumes", is_flag=True, help="同时清理未使用的卷")
@click.option("--yes", is_flag=True, help="跳过确认")
@click.pass_context
def system_prune(ctx, volumes, yes):
    """清理未使用的容器、镜像、网络（可选卷）。"""
    c = _client()
    as_json = ctx.obj["json"]
    if not yes:
        click.confirm("确认清理所有未使用的资源？", abort=True)
    result = {}
    result["containers"] = c.containers.prune()
    result["images"] = c.images.prune()
    result["networks"] = c.networks.prune()
    if volumes:
        result["volumes"] = c.volumes.prune()
    if as_json:
        _out(result, True)
    else:
        for resource, info in result.items():
            deleted = info.get("VolumesDeleted") or info.get("ImagesDeleted") or info.get("ContainersDeleted") or info.get("NetworksDeleted") or []
            click.echo(f"  {resource}: {len(deleted or [])} deleted, {_size_str(info.get('SpaceReclaimed', 0))} reclaimed")


@system.command(name="df")
@click.pass_context
def system_df(ctx):
    """显示 Docker 磁盘使用情况。"""
    c = _client()
    as_json = ctx.obj["json"]
    df = c.df()
    if as_json:
        _out(df, True)
    else:
        images = df.get("Images", [])
        containers = df.get("Containers", [])
        volumes = df.get("Volumes", [])
        click.echo(f"Images:     {len(images)} total, {_size_str(sum(i.get('Size',0) for i in images))}")
        click.echo(f"Containers: {len(containers)} total")
        click.echo(f"Volumes:    {len(volumes)} total")


if __name__ == "__main__":
    cli()
