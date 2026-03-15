# 飞书 CLI 快速上手

## 第一步：创建飞书自建应用（2 分钟）

1. 打开 https://open.feishu.cn/app
2. 点击 **"创建企业自建应用"**
3. 填写应用名称（如 `my-cli-bot`）
4. 进入 **凭证与基础信息** → 复制 `App ID` 和 `App Secret`
5. 进入 **权限管理** → 开通以下权限：

| 权限名称 | 用途 |
|---------|------|
| `im:message` | 发送/读取消息 |
| `im:message:send_as_bot` | 以机器人身份发送 |
| `im:chat` | 查询群组信息 |
| `docs:doc` | 文档读写 |
| `drive:drive` | 云空间文件列表 |
| `calendar:calendar` | 日历读写 |
| `contact:user.base:readonly` | 查询用户信息 |

6. 进入 **版本管理与发布** → 发布应用（或申请发布）
7. 将机器人 **加入目标群组**（「飞书」→ 群设置 → 机器人 → 添加）

---

## 第二步：配置凭证

```bash
python feishu_cli.py config setup
# 按提示输入 App ID 和 App Secret
```

凭证存储在 `~/.feishu_cli.json`（本地加密），后续自动复用。

---

## 常用命令示例

### 发消息

```bash
# 发文本消息（需先获取 chat_id，用 chat list 命令）
python feishu_cli.py msg send --to oc_xxxxxxxx --text "Hello from CLI"

# 发格式化卡片
python feishu_cli.py msg send-card \
  --to oc_xxxxxxxx \
  --title "部署成功" \
  --body "**prod** 环境已更新到 v2.3.1\n- 构建时间: 3m 20s\n- 测试通过率: 100%" \
  --color green \
  --btn-text "查看详情" \
  --btn-url "https://github.com/xxx/releases"

# 一键发通知（最常用）
python feishu_cli.py notify \
  --to oc_xxxxxxxx \
  --title "告警：CPU 使用率过高" \
  --content "服务器 prod-01 CPU 使用率达到 **95%**\n请及时处理！" \
  --level error
```

### 列出群组 & 消息历史

```bash
python feishu_cli.py chat list
python feishu_cli.py chat members oc_xxxxxxxx
python feishu_cli.py msg list --chat-id oc_xxxxxxxx --limit 10
```

### 文档操作

```bash
python feishu_cli.py doc list
python feishu_cli.py doc create --title "周报 2026-03" --content "## 本周工作\n- 完成需求 A"
python feishu_cli.py doc get <document_id>
```

### 日历操作

```bash
# 列出本周日程
python feishu_cli.py cal list

# 创建日程
python feishu_cli.py cal add \
  --title "项目评审会" \
  --start "2026-03-18 14:00" \
  --end   "2026-03-18 15:30" \
  --location "会议室 A-302"

# 删除日程
python feishu_cli.py cal delete <event_id>
```

### JSON 输出（供 AI Agent 消费）

```bash
python feishu_cli.py --json chat list
python feishu_cli.py --json msg list --chat-id oc_xxx --limit 5
```

---

## 如何获取 chat_id

```bash
# 1. 列出机器人所在群
python feishu_cli.py chat list

# 2. 也可以在飞书 Web 版群聊 URL 中找到：
# https://applink.feishu.cn/client/chat/open?openChatId=oc_xxxxxxxx
#                                                              ^^^^^^^^ 这就是 chat_id
```
