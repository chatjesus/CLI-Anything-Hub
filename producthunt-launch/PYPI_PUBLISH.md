# PyPI 发布指南 — 一键上传 18 个 CLI 包

> 所有包已构建完毕，位于 `producthunt-launch/dist/`

---

## 准备工作（一次性）

### 1. 注册 PyPI 账号

前往 https://pypi.org/account/register/ 注册

### 2. 创建 API Token

前往 https://pypi.org/manage/account/token/ → 创建一个全局 scope 的 token

### 3. 配置 .pypirc

```bash
# 在用户目录创建 .pypirc
# Windows: C:\Users\PRO\.pypirc
# macOS/Linux: ~/.pypirc
```

文件内容:

```ini
[pypi]
username = __token__
password = pypi-AgXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

> 把 `pypi-AgXXXX...` 替换为你的真实 token

---

## 上传

### 方式一：一键上传全部 18 个包

```bash
cd c:\Users\PRO\Desktop\CUDA\CLI-Anything\producthunt-launch
twine upload dist/*
```

### 方式二：先用 TestPyPI 测试

```bash
# 1. 注册 test.pypi.org 账号 + token
# 2. 上传到测试仓库
twine upload --repository testpypi dist/*

# 3. 测试安装
pip install --index-url https://test.pypi.org/simple/ cli-anything-slack

# 4. 确认没问题后，上传到正式仓库
twine upload dist/*
```

### 方式三：只上传核心 5 个（推荐先发这些）

```bash
twine upload dist/cli_anything_slack* dist/cli_anything_stripe* dist/cli_anything_docker* dist/cli_anything_ollama* dist/cli_anything_notion*
```

---

## 上传后验证

```bash
# 等 1-2 分钟后
pip install cli-anything-slack
cli-anything-slack schema

pip install cli-anything-docker  
cli-anything-docker detect

pip install cli-anything-ollama
cli-anything-ollama detect
```

---

## 已构建的包清单

| 包名 | 文件 |
|------|------|
| cli-anything-slack | cli_anything_slack-1.0.0-py3-none-any.whl |
| cli-anything-stripe | cli_anything_stripe-1.0.0-py3-none-any.whl |
| cli-anything-docker | cli_anything_docker-1.0.0-py3-none-any.whl |
| cli-anything-ollama | cli_anything_ollama-1.0.0-py3-none-any.whl |
| cli-anything-notion | cli_anything_notion-1.0.0-py3-none-any.whl |
| cli-anything-discord | cli_anything_discord-1.0.0-py3-none-any.whl |
| cli-anything-telegram | cli_anything_telegram-1.0.0-py3-none-any.whl |
| cli-anything-github | cli_anything_github-1.0.0-py3-none-any.whl |
| cli-anything-shopify | cli_anything_shopify-1.0.0-py3-none-any.whl |
| cli-anything-hubspot | cli_anything_hubspot-1.0.0-py3-none-any.whl |
| cli-anything-salesforce | cli_anything_salesforce-1.0.0-py3-none-any.whl |
| cli-anything-jira | cli_anything_jira-1.0.0-py3-none-any.whl |
| cli-anything-vercel | cli_anything_vercel-1.0.0-py3-none-any.whl |
| cli-anything-cloudflare | cli_anything_cloudflare-1.0.0-py3-none-any.whl |
| cli-anything-twilio | cli_anything_twilio-1.0.0-py3-none-any.whl |
| cli-anything-gworkspace | cli_anything_gworkspace-1.0.0-py3-none-any.whl |
| cli-anything-feishu | cli_anything_feishu-1.0.0-py3-none-any.whl |
| cli-anything-ms365 | cli_anything_ms365-1.0.0-py3-none-any.whl |
