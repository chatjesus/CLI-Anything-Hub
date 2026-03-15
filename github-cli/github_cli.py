"""
cli-anything-github — GitHub REST API CLI
Wraps GitHub REST API v3 via PyGithub for AI Agent use.
"""
import json
import sys
import os
from typing import Optional

import click

try:
    from github import Github, Auth, GithubException
    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False


# ─── helpers ─────────────────────────────────────────────────────────────────

def _gh(token: Optional[str]):
    if not _SDK_AVAILABLE:
        raise click.ClickException("PyGithub 未安装，请运行: pip install PyGithub")
    t = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not t:
        raise click.ClickException(
            "未提供 GitHub token。\n"
            "方式1: --token <PAT>\n"
            "方式2: export GITHUB_TOKEN=<PAT>\n"
            "获取 token: https://github.com/settings/tokens"
        )
    try:
        g = Github(auth=Auth.Token(t))
        g.get_user().login  # validate
        return g
    except GithubException as e:
        raise click.ClickException(f"GitHub 认证失败: {e.data.get('message', str(e))}")


def _out(data, as_json: bool):
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        if isinstance(data, str):
            click.echo(data)
        elif isinstance(data, list):
            for item in data:
                click.echo(item if isinstance(item, str) else json.dumps(item, ensure_ascii=False, default=str))
        else:
            click.echo(str(data))


def _repo_dict(repo) -> dict:
    return {
        "full_name": repo.full_name,
        "description": repo.description,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "language": repo.language,
        "private": repo.private,
        "url": repo.html_url,
        "default_branch": repo.default_branch,
        "updated_at": str(repo.updated_at),
    }


def _issue_dict(issue) -> dict:
    return {
        "number": issue.number,
        "title": issue.title,
        "state": issue.state,
        "author": issue.user.login,
        "labels": [l.name for l in issue.labels],
        "url": issue.html_url,
        "created_at": str(issue.created_at),
        "body_preview": (issue.body or "")[:200],
    }


def _pr_dict(pr) -> dict:
    return {
        "number": pr.number,
        "title": pr.title,
        "state": pr.state,
        "author": pr.user.login,
        "base": pr.base.ref,
        "head": pr.head.ref,
        "url": pr.html_url,
        "mergeable": pr.mergeable,
        "created_at": str(pr.created_at),
    }


# ─── root ─────────────────────────────────────────────────────────────────────

@click.group()
@click.option("--token", envvar="GITHUB_TOKEN", default=None, help="GitHub PAT（或设置 GITHUB_TOKEN 环境变量）")
@click.option("--json", "as_json", is_flag=True, help="以 JSON 格式输出（Agent 友好）")
@click.pass_context
def cli(ctx, token, as_json):
    """cli-anything-github — GitHub REST API CLI\n
    管理仓库、Issues、Pull Requests、Releases、Actions、Gists 等。
    需要 GitHub Personal Access Token（--token 或 GITHUB_TOKEN 环境变量）。
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["json"] = as_json


# ─── detect ───────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def detect(ctx):
    """检测 GitHub API 可用性并验证 token。"""
    as_json = ctx.obj["json"]
    if not _SDK_AVAILABLE:
        result = {"status": "sdk_missing", "fix": "pip install PyGithub"}
        _out(result, as_json) if as_json else click.echo("❌ PyGithub 未安装")
        sys.exit(1)
    try:
        g = _gh(ctx.obj["token"])
        user = g.get_user()
        rate = g.get_rate_limit().core
        result = {
            "status": "ok",
            "login": user.login,
            "name": user.name,
            "rate_limit_remaining": rate.remaining,
            "rate_limit_reset": str(rate.reset),
        }
        if as_json:
            _out(result, True)
        else:
            click.echo(f"✅ GitHub API OK  login={result['login']}  rate={rate.remaining}/{rate.limit}")
    except click.ClickException as e:
        result = {"status": "error", "error": e.format_message()}
        _out(result, as_json) if as_json else click.echo(f"❌ {e.format_message()}")
        sys.exit(1)


# ─── version ──────────────────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def version(ctx):
    """显示 GitHub API 版本及用户信息。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    user = g.get_user()
    rate = g.get_rate_limit()
    result = {
        "api_version": "v3",
        "login": user.login,
        "public_repos": user.public_repos,
        "followers": user.followers,
        "rate_limit_core_remaining": rate.core.remaining,
    }
    _out(result, as_json) if as_json else click.echo(
        f"GitHub API v3  user={result['login']}  repos={result['public_repos']}  rate={result['rate_limit_core_remaining']}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# REPO
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def repo():
    """仓库管理（list / get / create / delete / clone-url / topics）。"""


@repo.command(name="list")
@click.option("--user", default=None, help="指定用户名（默认为认证用户）")
@click.option("--limit", default=30, show_default=True, type=int)
@click.option("--sort", default="updated", type=click.Choice(["updated", "created", "pushed", "full_name"]))
@click.pass_context
def repo_list(ctx, user, limit, sort):
    """列出仓库。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    owner = g.get_user(user) if user else g.get_user()
    repos = list(owner.get_repos(sort=sort, direction="desc"))[:limit]
    data = [_repo_dict(r) for r in repos]
    if as_json:
        _out({"repos": data, "count": len(data)}, True)
    else:
        click.echo(f"{'REPO':<45} {'★':>6}  {'LANG':<15} UPDATED")
        click.echo("─" * 90)
        for d in data:
            click.echo(f"{d['full_name']:<45} {d['stars']:>6}  {(d['language'] or '—'):<15} {d['updated_at'][:10]}")


@repo.command(name="get")
@click.argument("repo_name")
@click.pass_context
def repo_get(ctx, repo_name):
    """获取仓库详细信息。\n REPO_NAME 格式: owner/repo"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    data = _repo_dict(r)
    data.update({
        "open_issues": r.open_issues_count,
        "topics": r.topics,
        "license": r.license.name if r.license else None,
        "clone_url": r.clone_url,
        "ssh_url": r.ssh_url,
    })
    _out(data, as_json) if as_json else click.echo(
        "\n".join(f"  {k:<20} {v}" for k, v in data.items() if v is not None)
    )


@repo.command(name="create")
@click.argument("name")
@click.option("--description", "-d", default="", help="仓库描述")
@click.option("--private", is_flag=True, help="私有仓库")
@click.option("--auto-init", is_flag=True, help="自动初始化（创建 README）")
@click.pass_context
def repo_create(ctx, name, description, private, auto_init):
    """创建新仓库。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    user = g.get_user()
    r = user.create_repo(name, description=description, private=private, auto_init=auto_init)
    result = _repo_dict(r)
    _out(result, as_json) if as_json else click.echo(f"✅ Created: {r.html_url}")


@repo.command(name="delete")
@click.argument("repo_name")
@click.option("--yes", is_flag=True)
@click.pass_context
def repo_delete(ctx, repo_name, yes):
    """删除仓库（不可恢复！）。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    if not yes:
        click.confirm(f"确认删除仓库 {repo_name!r}？此操作不可恢复！", abort=True)
    r = g.get_repo(repo_name)
    r.delete()
    result = {"deleted": repo_name}
    _out(result, as_json) if as_json else click.echo(f"🗑  Deleted: {repo_name}")


@repo.command(name="topics")
@click.argument("repo_name")
@click.option("--set", "set_topics", multiple=True, help="替换 topics（可重复）")
@click.pass_context
def repo_topics(ctx, repo_name, set_topics):
    """查看或替换仓库 topics。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    if set_topics:
        r.replace_topics(list(set_topics))
    topics = r.topics
    result = {"repo": repo_name, "topics": topics}
    _out(result, as_json) if as_json else click.echo(", ".join(topics) or "（无 topics）")


# ══════════════════════════════════════════════════════════════════════════════
# ISSUE
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def issue():
    """Issue 管理（list / get / create / close / comment）。"""


@issue.command(name="list")
@click.argument("repo_name")
@click.option("--state", default="open", type=click.Choice(["open", "closed", "all"]))
@click.option("--label", default=None, help="按标签筛选")
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def issue_list(ctx, repo_name, state, label, limit):
    """列出 Issues。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    kwargs = {"state": state}
    if label:
        kwargs["labels"] = [r.get_label(label)]
    issues = list(r.get_issues(**kwargs))
    # Filter out PRs (GitHub API returns PRs in get_issues)
    issues = [i for i in issues if not i.pull_request][:limit]
    data = [_issue_dict(i) for i in issues]
    if as_json:
        _out({"issues": data, "count": len(data)}, True)
    else:
        click.echo(f"{'#':>6}  {'STATE':<8} {'TITLE':<55} AUTHOR")
        click.echo("─" * 90)
        for d in data:
            click.echo(f"#{d['number']:>5}  {d['state']:<8} {d['title'][:54]:<55} {d['author']}")


@issue.command(name="get")
@click.argument("repo_name")
@click.argument("number", type=int)
@click.pass_context
def issue_get(ctx, repo_name, number):
    """获取 Issue 详情。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    i = r.get_issue(number)
    data = _issue_dict(i)
    data["body"] = i.body or ""
    data["comments"] = i.comments
    _out(data, as_json) if as_json else (
        click.echo(f"#{i.number} [{i.state}] {i.title}"),
        click.echo(f"Author: {i.user.login}  Labels: {[l.name for l in i.labels]}"),
        click.echo(f"\n{i.body or '（无正文）'}")
    )


@issue.command(name="create")
@click.argument("repo_name")
@click.option("--title", "-t", required=True, help="Issue 标题")
@click.option("--body", "-b", default="", help="Issue 正文（支持 Markdown）")
@click.option("--label", multiple=True, help="标签（可重复）")
@click.option("--assignee", multiple=True, help="指派给（用户名，可重复）")
@click.pass_context
def issue_create(ctx, repo_name, title, body, label, assignee):
    """创建新 Issue。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    kwargs = {"title": title, "body": body}
    if label:
        kwargs["labels"] = list(label)
    if assignee:
        kwargs["assignees"] = list(assignee)
    i = r.create_issue(**kwargs)
    result = _issue_dict(i)
    _out(result, as_json) if as_json else click.echo(f"✅ Issue #{i.number}: {i.html_url}")


@issue.command(name="close")
@click.argument("repo_name")
@click.argument("number", type=int)
@click.pass_context
def issue_close(ctx, repo_name, number):
    """关闭 Issue。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    i = r.get_issue(number)
    i.edit(state="closed")
    result = {"number": number, "state": "closed"}
    _out(result, as_json) if as_json else click.echo(f"✅ Issue #{number} closed")


@issue.command(name="comment")
@click.argument("repo_name")
@click.argument("number", type=int)
@click.option("--body", "-b", required=True, help="评论内容")
@click.pass_context
def issue_comment(ctx, repo_name, number, body):
    """在 Issue 上添加评论。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    i = r.get_issue(number)
    c = i.create_comment(body)
    result = {"issue": number, "comment_id": c.id, "url": c.html_url}
    _out(result, as_json) if as_json else click.echo(f"✅ Comment added: {c.html_url}")


# ══════════════════════════════════════════════════════════════════════════════
# PR
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def pr():
    """Pull Request 管理（list / get / create / merge / close / review）。"""


@pr.command(name="list")
@click.argument("repo_name")
@click.option("--state", default="open", type=click.Choice(["open", "closed", "all"]))
@click.option("--limit", default=20, show_default=True, type=int)
@click.pass_context
def pr_list(ctx, repo_name, state, limit):
    """列出 Pull Requests。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    prs = list(r.get_pulls(state=state, sort="updated", direction="desc"))[:limit]
    data = [_pr_dict(p) for p in prs]
    if as_json:
        _out({"prs": data, "count": len(data)}, True)
    else:
        click.echo(f"{'#':>6}  {'STATE':<8} {'BASE←HEAD':<30} TITLE")
        click.echo("─" * 90)
        for d in data:
            branch_info = f"{d['base']}←{d['head']}"
            click.echo(f"#{d['number']:>5}  {d['state']:<8} {branch_info:<30} {d['title'][:40]}")


@pr.command(name="get")
@click.argument("repo_name")
@click.argument("number", type=int)
@click.pass_context
def pr_get(ctx, repo_name, number):
    """获取 PR 详情。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    p = r.get_pull(number)
    data = _pr_dict(p)
    data.update({
        "body": p.body or "",
        "commits": p.commits,
        "additions": p.additions,
        "deletions": p.deletions,
        "changed_files": p.changed_files,
        "review_comments": p.review_comments,
    })
    _out(data, as_json) if as_json else (
        click.echo(f"#{p.number} [{p.state}] {p.title}"),
        click.echo(f"  {p.head.ref} → {p.base.ref}  +{p.additions}/-{p.deletions}  {p.changed_files} files"),
        click.echo(f"\n{p.body or '（无描述）'}")
    )


@pr.command(name="create")
@click.argument("repo_name")
@click.option("--title", "-t", required=True)
@click.option("--body", "-b", default="")
@click.option("--head", required=True, help="源分支（feature/xxx）")
@click.option("--base", default="main", show_default=True, help="目标分支")
@click.option("--draft", is_flag=True, help="创建为草稿 PR")
@click.pass_context
def pr_create(ctx, repo_name, title, body, head, base, draft):
    """创建 Pull Request。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    p = r.create_pull(title=title, body=body, head=head, base=base, draft=draft)
    result = _pr_dict(p)
    _out(result, as_json) if as_json else click.echo(f"✅ PR #{p.number}: {p.html_url}")


@pr.command(name="merge")
@click.argument("repo_name")
@click.argument("number", type=int)
@click.option("--method", default="merge", type=click.Choice(["merge", "squash", "rebase"]))
@click.option("--message", default=None, help="合并提交信息")
@click.pass_context
def pr_merge(ctx, repo_name, number, method, message):
    """合并 Pull Request。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    p = r.get_pull(number)
    merged = p.merge(merge_method=method, commit_message=message)
    result = {"number": number, "merged": merged.merged, "sha": merged.sha}
    _out(result, as_json) if as_json else click.echo(f"✅ PR #{number} merged ({method})")


# ══════════════════════════════════════════════════════════════════════════════
# RELEASE
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def release():
    """Release 管理（list / get / create / delete）。"""


@release.command(name="list")
@click.argument("repo_name")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
def release_list(ctx, repo_name, limit):
    """列出 Releases。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    releases = list(r.get_releases())[:limit]
    data = [{
        "tag": rel.tag_name,
        "name": rel.title,
        "draft": rel.draft,
        "prerelease": rel.prerelease,
        "published_at": str(rel.published_at),
        "url": rel.html_url,
    } for rel in releases]
    if as_json:
        _out({"releases": data, "count": len(data)}, True)
    else:
        click.echo(f"{'TAG':<25} {'NAME':<35} PUBLISHED")
        click.echo("─" * 80)
        for d in data:
            flags = " [DRAFT]" if d["draft"] else (" [PRE]" if d["prerelease"] else "")
            click.echo(f"{d['tag']:<25} {(d['name'] or '')[:34]:<35} {str(d['published_at'])[:10]}{flags}")


@release.command(name="create")
@click.argument("repo_name")
@click.option("--tag", "-t", required=True, help="Tag 名称（如 v1.0.0）")
@click.option("--name", "-n", default=None, help="Release 名称")
@click.option("--body", "-b", default="", help="Release 说明")
@click.option("--draft", is_flag=True)
@click.option("--prerelease", is_flag=True)
@click.option("--target", default=None, help="目标 commit/branch（默认 default_branch）")
@click.pass_context
def release_create(ctx, repo_name, tag, name, body, draft, prerelease, target):
    """创建 Release。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    kwargs = {
        "tag": tag,
        "name": name or tag,
        "message": body,
        "draft": draft,
        "prerelease": prerelease,
    }
    if target:
        kwargs["target_commitish"] = target
    rel = r.create_git_release(**kwargs)
    result = {"tag": rel.tag_name, "url": rel.html_url, "id": rel.id}
    _out(result, as_json) if as_json else click.echo(f"✅ Release {rel.tag_name}: {rel.html_url}")


# ══════════════════════════════════════════════════════════════════════════════
# ACTIONS (Workflows)
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def actions():
    """GitHub Actions 管理（list-workflows / list-runs / trigger / get-run）。"""


@actions.command(name="list-workflows")
@click.argument("repo_name")
@click.pass_context
def actions_list_workflows(ctx, repo_name):
    """列出仓库中的所有 Workflows。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    workflows = list(r.get_workflows())
    data = [{"id": w.id, "name": w.name, "state": w.state, "path": w.path} for w in workflows]
    if as_json:
        _out({"workflows": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':>10}  {'NAME':<40} {'STATE':<12} PATH")
        click.echo("─" * 90)
        for d in data:
            click.echo(f"{d['id']:>10}  {d['name']:<40} {d['state']:<12} {d['path']}")


@actions.command(name="list-runs")
@click.argument("repo_name")
@click.option("--workflow", "-w", default=None, help="Workflow 文件名（如 ci.yml）")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
def actions_list_runs(ctx, repo_name, workflow, limit):
    """列出 Workflow 运行记录。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    if workflow:
        wf = r.get_workflow(workflow)
        runs = list(wf.get_runs())[:limit]
    else:
        runs = list(r.get_workflow_runs())[:limit]
    data = [{
        "id": run.id,
        "name": run.name,
        "status": run.status,
        "conclusion": run.conclusion,
        "branch": run.head_branch,
        "created_at": str(run.created_at),
        "url": run.html_url,
    } for run in runs]
    if as_json:
        _out({"runs": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':>12}  {'STATUS':<12} {'CONCLUSION':<12} {'BRANCH':<20} NAME")
        click.echo("─" * 90)
        for d in data:
            click.echo(f"{d['id']:>12}  {(d['status'] or ''):<12} {(d['conclusion'] or ''):<12} {(d['branch'] or ''):<20} {d['name']}")


@actions.command(name="trigger")
@click.argument("repo_name")
@click.argument("workflow_id")
@click.option("--ref", default="main", show_default=True, help="分支/tag/commit")
@click.option("--input", "-i", "inputs", multiple=True, help="workflow_dispatch 输入（KEY=VALUE）")
@click.pass_context
def actions_trigger(ctx, repo_name, workflow_id, ref, inputs):
    """手动触发 workflow_dispatch 事件。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    r = g.get_repo(repo_name)
    wf = r.get_workflow(workflow_id)
    input_dict = {}
    for inp in inputs:
        k, v = inp.split("=", 1)
        input_dict[k] = v
    result_bool = wf.create_dispatch(ref, input_dict)
    result = {"triggered": result_bool, "workflow": workflow_id, "ref": ref}
    _out(result, as_json) if as_json else click.echo(
        f"{'✅' if result_bool else '❌'} Triggered {workflow_id} on {ref}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# GIST
# ══════════════════════════════════════════════════════════════════════════════

@cli.group()
def gist():
    """Gist 管理（list / create / get）。"""


@gist.command(name="list")
@click.option("--limit", default=10, show_default=True, type=int)
@click.pass_context
def gist_list(ctx, limit):
    """列出自己的 Gists。"""
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    gists = list(g.get_user().get_gists())[:limit]
    data = [{
        "id": gs.id,
        "description": gs.description,
        "public": gs.public,
        "files": list(gs.files.keys()),
        "url": gs.html_url,
        "updated_at": str(gs.updated_at),
    } for gs in gists]
    if as_json:
        _out({"gists": data, "count": len(data)}, True)
    else:
        click.echo(f"{'ID':<25} {'PUBLIC':<8} {'FILES':<30} DESCRIPTION")
        click.echo("─" * 90)
        for d in data:
            click.echo(f"{d['id']:<25} {str(d['public']):<8} {','.join(d['files'])[:28]:<30} {(d['description'] or '')[:30]}")


@gist.command(name="create")
@click.option("--file", "-f", "files", multiple=True, required=True,
              help="文件（格式: filename:content 或 filename:@filepath）")
@click.option("--description", "-d", default="", help="Gist 描述")
@click.option("--public", is_flag=True, help="公开 Gist（默认私有）")
@click.pass_context
def gist_create(ctx, files, description, public):
    """创建 Gist。"""
    from github import InputFileContent
    g = _gh(ctx.obj["token"])
    as_json = ctx.obj["json"]
    file_dict = {}
    for f in files:
        if ":" in f:
            name, content = f.split(":", 1)
            if content.startswith("@"):
                with open(content[1:], encoding="utf-8") as fh:
                    content = fh.read()
        else:
            name, content = f, ""
        file_dict[name] = InputFileContent(content)
    gs = g.get_user().create_gist(public=public, files=file_dict, description=description)
    result = {"id": gs.id, "url": gs.html_url, "public": gs.public}
    _out(result, as_json) if as_json else click.echo(f"✅ Gist: {gs.html_url}")


if __name__ == "__main__":
    cli()
