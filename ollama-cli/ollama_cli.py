"""
cli-anything-ollama — Ollama local LLM server CLI
Wraps Ollama REST API (localhost:11434) for AI Agent use.
"""
import json
import sys
import time
import urllib.request
import urllib.error
from typing import Optional

import click

DEFAULT_HOST = "http://localhost:11434"


# ─── helpers ─────────────────────────────────────────────────────────────────

def _url(host: str, path: str) -> str:
    return host.rstrip("/") + path


def _get(host: str, path: str) -> dict:
    req = urllib.request.Request(_url(host, path), headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise click.ClickException(f"无法连接 Ollama ({host}): {e.reason}")


def _post(host: str, path: str, body: dict, timeout: int = 120) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        _url(host, path),
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            # Ollama streaming: multiple JSON lines → take last non-empty
            lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
            if not lines:
                return {}
            # Merge streaming chunks: concat response text
            chunks = [json.loads(l) for l in lines]
            if len(chunks) == 1:
                return chunks[0]
            # For generate/chat: stitch together
            merged = chunks[-1].copy()
            if "response" in chunks[0]:
                merged["response"] = "".join(c.get("response", "") for c in chunks)
            elif "message" in chunks[0]:
                merged["message"] = {
                    "role": "assistant",
                    "content": "".join(c.get("message", {}).get("content", "") for c in chunks),
                }
            return merged
    except urllib.error.URLError as e:
        raise click.ClickException(f"请求失败 ({host}{path}): {e.reason}")


def _delete(host: str, path: str, body: dict) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        _url(host, path),
        data=data,
        headers={"Content-Type": "application/json"},
        method="DELETE",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else {"status": "deleted"}
    except urllib.error.URLError as e:
        raise click.ClickException(f"删除失败: {e.reason}")


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        if isinstance(data, str):
            click.echo(data)
        elif isinstance(data, list):
            for item in data:
                click.echo(item)
        else:
            click.echo(str(data))


# ─── root ─────────────────────────────────────────────────────────────────────

@click.group()
@click.option("--host", default=DEFAULT_HOST, envvar="OLLAMA_HOST",
              show_default=True, help="Ollama 服务地址")
@click.option("--json", "as_json", is_flag=True, help="以 JSON 格式输出（Agent 友好）")
@click.pass_context
def cli(ctx, host, as_json):
    """cli-anything-ollama — Ollama 本地 LLM 服务器 CLI\n
    控制 Ollama 模型：拉取/删除/运行/聊天/嵌入向量/服务器管理。
    默认连接 http://localhost:11434，可通过 --host 或 OLLAMA_HOST 修改。
    """
    ctx.ensure_object(dict)
    ctx.obj["host"] = host
    ctx.obj["json"] = as_json


# ─── detect ───────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def detect(ctx):
    """检测 Ollama 是否运行并返回版本信息。"""
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    try:
        data = _get(host, "/api/version")
        result = {"status": "running", "host": host, "version": data.get("version", "unknown")}
        _out(result, as_json) if as_json else click.echo(
            f"✅ Ollama running @ {host}  version={result['version']}"
        )
    except click.ClickException:
        result = {"status": "not_running", "host": host}
        if as_json:
            _out(result, True)
        else:
            click.echo(f"❌ Ollama not running @ {host}")
        sys.exit(1)


# ─── version ──────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def version(ctx):
    """显示 Ollama 服务器版本。"""
    data = _get(ctx.obj["host"], "/api/version")
    _out(data, ctx.obj["json"]) if ctx.obj["json"] else click.echo(data.get("version", "unknown"))


# ─── list ─────────────────────────────────────────────────────────────────────

@cli.command(name="list")
@click.pass_context
def list_models(ctx):
    """列出本地已下载的所有模型。"""
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    data = _get(host, "/api/tags")
    models = data.get("models", [])
    if as_json:
        _out({"models": models, "count": len(models)}, True)
    else:
        if not models:
            click.echo("（没有已下载的模型）")
            return
        click.echo(f"{'NAME':<35} {'SIZE':>10}  {'MODIFIED'}")
        click.echo("─" * 70)
        for m in models:
            size_gb = m.get("size", 0) / 1024**3
            modified = m.get("modified_at", "")[:10]
            click.echo(f"{m['name']:<35} {size_gb:>9.2f}G  {modified}")


# ─── ps ───────────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def ps(ctx):
    """列出当前正在运行（已加载到内存）的模型。"""
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    data = _get(host, "/api/ps")
    models = data.get("models", [])
    if as_json:
        _out({"running": models, "count": len(models)}, True)
    else:
        if not models:
            click.echo("（没有模型正在运行）")
            return
        click.echo(f"{'NAME':<35} {'SIZE':>10}  EXPIRES_AT")
        click.echo("─" * 70)
        for m in models:
            size_gb = m.get("size", 0) / 1024**3
            expires = m.get("expires_at", "")[:19]
            click.echo(f"{m['name']:<35} {size_gb:>9.2f}G  {expires}")


# ─── show ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("model")
@click.pass_context
def show(ctx, model):
    """显示模型详细信息（架构、参数量、量化方式、Modelfile 等）。"""
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    data = _post(host, "/api/show", {"name": model}, timeout=30)
    if as_json:
        _out(data, True)
    else:
        details = data.get("details", {})
        info = [
            ("Model", model),
            ("Family", details.get("family", "—")),
            ("Parameter size", details.get("parameter_size", "—")),
            ("Quantization", details.get("quantization_level", "—")),
            ("Format", details.get("format", "—")),
        ]
        for k, v in info:
            click.echo(f"  {k:<20} {v}")
        if "modelfile" in data:
            click.echo("\n── Modelfile ──")
            click.echo(data["modelfile"])


# ─── pull ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("model")
@click.option("--insecure", is_flag=True, help="允许使用不安全的注册表（测试用）")
@click.pass_context
def pull(ctx, model, insecure):
    """从 Ollama Hub 拉取模型（支持流式进度显示）。"""
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    body = {"name": model, "insecure": insecure, "stream": True}
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        _url(host, "/api/pull"),
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    if as_json:
        click.echo(json.dumps({"action": "pull", "model": model, "status": "started"}))
    else:
        click.echo(f"⬇  Pulling {model} ...")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            last_status = ""
            while True:
                line = resp.readline()
                if not line:
                    break
                try:
                    event = json.loads(line.decode())
                except json.JSONDecodeError:
                    continue
                status = event.get("status", "")
                if as_json:
                    click.echo(json.dumps(event, ensure_ascii=False))
                else:
                    if status != last_status:
                        click.echo(f"  {status}")
                        last_status = status
        if not as_json:
            click.echo(f"✅ Pull complete: {model}")
    except urllib.error.URLError as e:
        raise click.ClickException(f"Pull 失败: {e.reason}")


# ─── delete ───────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("model")
@click.option("--yes", is_flag=True, help="跳过确认提示")
@click.pass_context
def delete(ctx, model, yes):
    """删除本地模型。"""
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    if not yes:
        click.confirm(f"确认删除模型 {model!r}？", abort=True)
    result = _delete(host, "/api/delete", {"name": model})
    result["model"] = model
    if as_json:
        _out(result, True)
    else:
        click.echo(f"🗑  已删除: {model}")


# ─── copy ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("source")
@click.argument("destination")
@click.pass_context
def copy(ctx, source, destination):
    """复制模型（相当于创建别名，不占用额外磁盘空间）。"""
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    _post(host, "/api/copy", {"source": source, "destination": destination}, timeout=30)
    result = {"status": "copied", "source": source, "destination": destination}
    if as_json:
        _out(result, True)
    else:
        click.echo(f"✅ {source} → {destination}")


# ─── run ──────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("model")
@click.argument("prompt")
@click.option("--system", default=None, help="系统提示词（system prompt）")
@click.option("--temperature", "-t", default=0.7, show_default=True, type=float)
@click.option("--max-tokens", default=2048, show_default=True, type=int)
@click.option("--raw", is_flag=True, help="不使用模板，直接发送 raw prompt")
@click.pass_context
def run(ctx, model, prompt, system, temperature, max_tokens, raw):
    """单次文本生成（非对话模式）。\n
    示例: ollama-cli run llama3.2 "用一句话解释量子计算"
    """
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "raw": raw,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    if system:
        body["system"] = system
    data = _post(host, "/api/generate", body, timeout=300)
    response_text = data.get("response", "")
    if as_json:
        _out({
            "model": model,
            "response": response_text,
            "eval_count": data.get("eval_count"),
            "eval_duration_ms": round(data.get("eval_duration", 0) / 1e6),
            "total_duration_ms": round(data.get("total_duration", 0) / 1e6),
        }, True)
    else:
        click.echo(response_text)


# ─── chat ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("model")
@click.option("--message", "-m", "messages", multiple=True,
              help="消息（格式 role:content，可重复）。例: -m user:你好 -m assistant:你好！ -m user:讲个笑话")
@click.option("--system", default=None, help="系统提示词")
@click.option("--temperature", "-t", default=0.7, show_default=True, type=float)
@click.option("--max-tokens", default=2048, show_default=True, type=int)
@click.pass_context
def chat(ctx, model, messages, system, temperature, max_tokens):
    """多轮对话模式（ChatML 格式）。\n
    示例: ollama-cli chat llama3.2 -m user:"What is 2+2?"
    """
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    msg_list = []
    if system:
        msg_list.append({"role": "system", "content": system})
    for m in messages:
        if ":" in m:
            role, content = m.split(":", 1)
            msg_list.append({"role": role.strip(), "content": content.strip()})
        else:
            msg_list.append({"role": "user", "content": m})
    if not msg_list:
        raise click.UsageError("至少提供一条消息：--message user:你好")
    body = {
        "model": model,
        "messages": msg_list,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    data = _post(host, "/api/chat", body, timeout=300)
    reply = data.get("message", {}).get("content", "")
    if as_json:
        _out({
            "model": model,
            "message": {"role": "assistant", "content": reply},
            "eval_count": data.get("eval_count"),
            "total_duration_ms": round(data.get("total_duration", 0) / 1e6),
        }, True)
    else:
        click.echo(reply)


# ─── embeddings ───────────────────────────────────────────────────────────────

@cli.command()
@click.argument("model")
@click.argument("text")
@click.option("--truncate/--no-truncate", default=True, show_default=True,
              help="超长输入是否截断")
@click.pass_context
def embeddings(ctx, model, text, truncate):
    """生成文本嵌入向量（Embedding）。\n
    示例: ollama-cli embeddings nomic-embed-text "Hello world"
    """
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    body = {"model": model, "input": text, "truncate": truncate}
    data = _post(host, "/api/embed", body, timeout=60)
    vectors = data.get("embeddings", [data.get("embedding", [])])
    vec = vectors[0] if vectors else []
    if as_json:
        _out({
            "model": model,
            "dimension": len(vec),
            "embedding": vec,
        }, True)
    else:
        click.echo(f"模型: {model}  维度: {len(vec)}")
        click.echo(f"前 8 维: {vec[:8]}")


# ─── serve ────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--wait", default=10, show_default=True, type=int,
              help="等待服务就绪的最长秒数")
@click.pass_context
def serve(ctx, wait):
    """启动 Ollama 服务（若未运行）并等待就绪。\n
    依赖系统 PATH 中存在 `ollama` 可执行文件。
    """
    import subprocess
    host = ctx.obj["host"]
    as_json = ctx.obj["json"]
    # Check if already running
    try:
        _get(host, "/api/version")
        result = {"status": "already_running", "host": host}
        if as_json:
            _out(result, True)
        else:
            click.echo("Ollama 已在运行")
        return
    except click.ClickException:
        pass
    # Start ollama serve in background
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
    except FileNotFoundError:
        raise click.ClickException("未找到 ollama 可执行文件，请先安装 Ollama")
    # Wait for ready
    deadline = time.time() + wait
    while time.time() < deadline:
        try:
            _get(host, "/api/version")
            result = {"status": "started", "host": host}
            if as_json:
                _out(result, True)
            else:
                click.echo(f"✅ Ollama 已启动 ({host})")
            return
        except click.ClickException:
            time.sleep(0.5)
    raise click.ClickException(f"Ollama 启动超时（{wait}s），请手动运行 `ollama serve`")


if __name__ == "__main__":
    cli()
