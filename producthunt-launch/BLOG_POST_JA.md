> **注記：** この記事は Vertex AI Gemini 2.0 Flash により英語原文から自動翻訳されました。[英語原文を読む](./BLOG_POST.md)

---

# CLI Anything: AIエージェントに欠けていた実行レイヤー

> *あなたのエージェントは優秀です。ただ、何も実行できません。*

あなたは、美しく推論し、戦略的に計画し、正確に応答するAIエージェントを構築しました。そして、Slackメッセージを送信するように依頼しました。すると、Pythonスクリプトが作成されました。Dockerビルドをトリガーするように依頼しました。Dockerfileの構文が説明されました。Jiraチケットを作成するように依頼しました。REST APIのエンドポイントが記述されました。

知性はありますが、手足がありません。

これは、エージェント時代の隠れたボトルネックであり、モデルのせいではありません。2025年の生産調査では、**エンタープライズAIエージェントのデプロイメントの73%が、最初の1年以内に信頼性の期待を満たしていない**ことが判明しました。失敗の原因は、知性の欠如ではありません。インフラストラクチャの欠如です。

HackerNoonの分析が指摘するように、*"エージェントハーネスエンジニアリング（コンテキスト管理、ツール選択、エラー回復、状態永続性の設計）は、モデルの能力ではなく、エージェントの信頼性を決定する主要な要因です。"*

OpenAIの共同創業者であるAndrej Karpathyは、2025年に現在のAIエージェントを「ずさん」と呼び、業界が「大きな飛躍を遂げすぎている」と警告し、議論を呼びました。彼の診断は、モデルに関するものではありませんでした。配管に関するものでした。

CLI Anythingは、その配管です。

---

## エージェントが今日ツールを呼び出す3つの方法 — そして、なぜそれらすべてが不十分なのか

解決策に入る前に、現状について正直になりましょう。

### オプション1：Raw API / SDK呼び出し

すべての統合は手書きです。エージェントはAPIスキーマを知り、認証を管理し、一貫性のない応答形式を解析し、各サービスのエラーを個別に処理する必要があります。これは、1つまたは2つの統合には有効です。50個にはスケールしません。

### オプション2：MCP (Model Context Protocol)

MCPは、Anthropicがツール標準化のために提供したもので、現在はLinux FoundationのAAIFによって管理されており、9,700万件を超えるSDKダウンロードと10,000件以上の公開サーバーを誇っています。表面的には、まさにエージェントが必要としているものです。

実際には、誰も十分に語らない重大な問題があります。**MCPはコンテキストを浪費します**。

実際のエンタープライズエージェントソリューションの構築に数か月を費やした開発者であるJannik Reinhardは、これを詳細に文書化しました。

> *"一般的なMCPサーバーは、ツール定義、パラメータの説明、認証フロー、状態管理など、すべてのスキーマをエージェントのコンテキストウィンドウにダンプします。"*

GitHub MCPサーバーだけでも、エージェントが実際の作業を行う前に**約55,000トークン**を消費します。これは、GPT-4o全体のコンテキストウィンドウの約半分であり、最初の質問の前に消えてしまいます。一般的なエンタープライズスタック（GitHub + データベース + Jira + Microsoft Graph）を接続すると、**150,000トークン以上のスキーマオーバーヘッド**が発生します。

トークンコストは、単なる効率性の問題ではありません。推論品質の問題です。Claudeの100万トークンあたり3ドルの価格設定では、このオーバーヘッドは**リクエストあたり0.27ドル、または大規模な場合、月額81,000ドル**に相当します。

Reinhardは、実際のコンプライアンス自動化タスクで直接比較を実行しました。

| アプローチ | トークンコスト |
|----------|-----------|
| MCP (Microsoft Graph) | 145,000トークン |
| CLI相当 | 4,150トークン |
| **差** | **35倍削減** |

CLIアプローチでは、コンテキストウィンドウの95%を実際の推論に利用できました。MCPアプローチでは、制限内に収まるようにワークフローを複数のセッションに分割しました。

### オプション3：CLIラッパー — 欠けている中間レイヤー

ここで、あまり評価されていない真実があります。LLMはネイティブなCLIスピーカーです。数十億行のターミナルインタラクション（Stack Overflowの回答、GitHubリポジトリ、ドキュメント、チュートリアル）でトレーニングされています。`git`、`docker`、`curl`、`kubectl`は深く学習されたパターンです。CLIコマンドとその`--help`出力には、**約200トークン**かかります。これは、MCP初期化よりも50倍の改善です。

ある開発者は、5,000トークン以上を消費するLangSmith MCPサーバーを、200トークンのCLIスキル定義に置き換えました。**コンテキストオーバーヘッドが95%削減され、機能の損失はゼロ**でした。

しかし、歴史的に、CLIラッパーには独自の問題がありました。標準インターフェースがないことです。すべてのツールには、異なるコマンド、異なる出力形式、異なるエラーコードがあります。エージェントは、ツール間で一貫した動作に依存できませんでした。

**それがCLI Anythingが埋めるギャップです。**

---

## CLI Anything Hubのご紹介

CLI Anything Hubは、世界で最も人気のあるソフトウェア向けの**130以上の事前構築された、エージェント対応のCLIラッパー**のキュレーションされたコミュニティ主導のコレクションです。単一の標準化された4コマンドインターフェースを中心に構築されています。

Hub内のすべてのCLIは、同じコントラクトを実装しています。ドキュメントは不要です。

```bash
# 1. DISCOVER — エージェントは機能を自己発見します。認証は不要です。
cli-anything-slack schema
# → { "name": "cli-anything-slack", "commands": [...], "token_env": "SLACK_BOT_TOKEN" }

# 2. CHECK — 冪等な接続テスト。副作用はありません。
cli-anything-slack detect
# → { "status": "ok", "workspace": "MyTeam", "bot": "AgentBot" }

# 3. CALL — 構造化されたJSON出力。エージェントが解析可能です。
cli-anything-slack --json message send #general "Deploy complete"
# → { "ok": true, "ts": "1742000000.000100" }

# 4. VERSION — 互換性追跡
cli-anything-slack version
# → cli-anything-slack 1.0.0
```

30秒で動作：

```bash
pip install cli-anything-slack
export SLACK_BOT_TOKEN=xoxb-...
cli-anything-slack --json message send #ops "Hello from Agent"
```

現在、**1,508件の自動テスト**に裏打ちされた30以上のCLIがライブでインストール可能です。ロードマップでは、クリエイティブ＆メディア、クラウドSaaS、開発ツール、ゲーム、ライフサービスなど、130以上のツールをカバーしています。

---

## 4層アーキテクチャ：CLI Anythingが適合する場所

最も一般的な質問：*"これはMCPと競合しますか？直接API呼び出しと競合しますか？"*

答えはノーです。CLI Anythingは実行レイヤーであり、エージェントスタックに特定の、明確に定義された場所があります。

```
┌──────────────────────────────────────────────────────────┐
│  Layer 4: Skills / SKILL.md                               │
│  インテントルーティング — "どのツール、どのコマンド、いつ"       │
├──────────────────────────────────────────────────────────┤
│  Layer 3: MCP Bridge (optional)                           │
│  プロトコルレイヤー — CLI AnythingをMCPツールとして公開        │
│  セマンティックガバナンス + リーンな実行                     │
├──────────────────────────────────────────────────────────┤
│  Layer 2: CLI Anything Hub                                │
│  標準化された実行 — schema / detect / call --json   │
│  30+ Live · 130+ planned · pip install · framework-free   │
├──────────────────────────────────────────────────────────┤
│  Layer 1: Real APIs & SDKs                                │
│  実際の通信 — Slack / Stripe / Docker / etc.    │
└──────────────────────────────────────────────────────────┘
```

**レイヤー1 — Real APIs：** 実際のSDKとRESTエンドポイント。CLI Anythingはこれらをラップするため、エージェントは生の認証、一貫性のない応答形式、またはサービス固有のエラー処理に対処する必要はありません。

**レイヤー2 — CLI Anything（コア）：** 標準化された実行インターフェース。`schema`は、エージェントに完全な機能マップを提供します。外部ドキュメントは不要です。`detect`は、いつでも安全に呼び出すことができる冪等なヘルスチェックを提供します。`--json`は、すべての応答が構造化され、後処理なしでエージェントが解析可能であることを保証します。

**レイヤー3 — MCP Bridge（オプション）：** CLI Anything CLIは、MCPツールとしてラップ*できます*。これは競合ではありません。両方の長所を組み合わせたものです。MCPは、エンタープライズ環境でガバナンス、監査証跡、およびセマンティックディスカバリーを提供します。CLI Anythingは、基盤となるリーンな実行レイヤーを提供し、MCPのトークンオーバーヘッドの問題を回避します。効果的なエージェントハーネスに関するHackerNoonの分析では、まさにこの「プログレッシブディスクロージャー」パターンが推奨されています。*モデルに必要なものだけを、必要なときに表示します。*

**レイヤー4 — Skills / SKILL.md：** インテントルーティングレイヤー。`SKILL.md`ファイルは、エージェントに*いつ*ツールにアクセスするか、*どの特定のコマンド*を使用するか、*どのコンテキスト*を渡すかを指示します。CLI Anythingのロードマップには、CLIごとに自動生成された`SKILL.md`が含まれており、Cursor、Codex、VS Code、Gemini CLI、およびAAIF Agent Skills Standardをサポートするすべてのエージェントで、すべてのツールを完全にプラグアンドプレイにすることができます。

**完全なエージェント制御スタック：** *スキルがルーティング → (MCPブリッジ) → CLIが実行 → APIが応答 → JSONがエージェントに返される。*

---

## 実際のウォークスルー：エージェントがデプロイメントを自動化

これを具体的にしましょう。エージェントは、*"新しいビルドをデプロイし、チームに通知し、リリーストラッキング用のJiraチケットを作成する"*というタスクを受け取ります。

**ステップ1：** エージェントはスキルレイヤーを読み取ります。`cli-anything-vercel`、`cli-anything-slack`、および`cli-anything-jira`が適切なツールとして識別されます。

**ステップ2：** エージェントは、それぞれで`schema`を呼び出します。3つの軽量JSON応答で、合計約600トークンです。これを、3つのMCPサーバーをロードすることと比較してください。単一のアクションの前に、約90,000トークンのスキーマオーバーヘッドが発生します。

**ステップ3：** 順番に実行します。

```bash
# Deploy
cli-anything-vercel --json deploy --project my-app
# → { "url": "https://my-app-xyz.vercel.app", "state": "READY" }

# Notify team
cli-anything-slack --json message send #releases "v2.1.0 live → https://my-app-xyz.vercel.app"
# → { "ok": true, "ts": "1742000000.000100" }

# Track release
cli-anything-jira --json issue create --project REL --summary "Release v2.1.0" --type Task
# → { "id": "REL-847", "status": "To Do", "url": "..." }
```

**結果：** 3つのツール。3つのpipインストール。1つの標準化されたインターフェース。カスタム統合コードはゼロ。MCP相当よりも35倍少ないトークン。

これは、作為的なデモではありません。Vercel自身のエンジニアリングチームは、同様の発見を文書化しました。エージェントのツールを15個から2個の焦点を絞った明確に定義されたツールに減らしたところ、精度が**80%から100%**に向上し、トークン使用量が**37%**減少し、速度が**3.5倍**向上しました。CLI Anythingの設計思想（リーン、フォーカス、コンポーザブル）は、まさにこの発見を反映しています。

---

## Hubの内容

**現在ライブ（30以上のCLI）：**

| カテゴリ | ツール |
|----------|-------|
| クリエイティブ＆メディア | GIMP, Blender, Inkscape, Audacity, OBS Studio, Kdenlive, Shotcut, Draw.io |
| コミュニケーション | Slack, Discord, Telegram, Feishu/Lark |
| クラウドSaaS | Stripe, Shopify, HubSpot, Salesforce, Jira, Cloudflare, Vercel, Twilio |
| 開発ツール | Docker, GitHub, Notion, Ollama |
| オフィス＆生産性 | MS 365, LibreOffice, Google Workspace (Drive + Gmail + Calendar + Sheets + Docs + Chat) |

**ロードマップ：**
- **ゲーム：** Steam, Roblox, Riot Games, Twitch, Minecraft RCON
- **ライフ＆ローカル：** DoorDash, Meituan, Uber Eats, Airbnb, Yelp
- **クリエイティブSaaS：** Figma, Canva, Adobe Photoshop (UXP)
- **広告：** Google Ads, TikTok Ads, Meta Ads

---

## Hubはオープンです — 独自のCLIを構築する

CLI AnythingはMITライセンスです。Hub内のすべてのCLIは、同じ最小限のコントラクトに従っており、Python開発者であれば誰でも午後に構築できます。

最小限の実装：

```python
import click, json

@click.group()
def cli(): pass

@cli.command()
def schema():
    """Output capability map. No auth needed."""
    click.echo(json.dumps({
        "name": "cli-anything-mytool",
        "version": "1.0.0",
        "requires_token": True,
        "token_env": "MYTOOL_API_KEY",
        "commands": [{"cmd": "do-thing", "desc": "Does the thing"}],
        "json_flag": "--json"
    }))

@cli.command()
def detect():
    """Connectivity check. No side effects."""
    click.echo(json.dumps({"status": "ok"}))
```

それがコアです。ツール固有のコマンドを追加し、PRまたはGitHub Issueを送信すると、CLI Anythingを使用する世界中のすべてのエージェントでツールが利用可能になります。

---

## なぜ今これが重要なのか

2025〜2026年は、AIエージェントが印象的なデモから信頼性の高い本番システムに移行する期間です。APEX-Agentsベンチマークは、最先端のモデルを実際の専門的なタスク（銀行、コンサルティング、法律）でテストし、冷静な結果を見つけました。最高のモデルでさえ、**24%のpass@1精度**しか達成できませんでした。主な失敗モードは、知識のギャップではありませんでした。オーケストレーションの失敗でした。

エージェントハーネスの研究コミュニティがまとめたように、*"最小限の能力のしきい値を超えると、モデルを交換するよりも、ハーネスエンジニアリングの方が優れたリターンをもたらします。"* Anthropicは、足場を再設計するだけで、*同じ*モデルを使用して36ポイントのベンチマーク改善を実証しました。

CLI Anythingは足場です。新しいAIモデル、新しい推論アーキテクチャではなく、エージェントがソフトウェアに接続する方法を標準化するという、地味で魅力のない作業によって、オーケストレーションレイヤーに直接対処します。

Hubに追加されたすべてのCLIは、世界中のすべてのエージェントで利用できる機能が1つ増えることを意味します。それがフライホイールです。

Jannik Reinhardが述べたように、AIエージェントツールの未来は、*"最も洗練されたプロトコルに関するものではありません。モデルとアクションの間の最もリーンなパスに関するものです。"*

CLI Anythingは、そのパスです。

---

## はじめに

**CLIをインストールして実行します：**
```bash
pip install cli-anything-slack
cli-anything-slack schema   # see what it can do
cli-anything-slack detect   # verify connectivity
```

**完全なカタログを探索します：** [agentputer.com/cli-anything](https://agentputer.com/cli-anything/)

**Hubをスター＆フォークします：** [github.com/chatjesus/CLI-Anything-Hub](https://github.com/chatjesus/CLI-Anything-Hub)

**独自のCLIを送信します：** [GitHub Issueを開く](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool-name)

**Product Huntで投票します：** [producthunt.com/posts/cli-anything](https://www.producthunt.com/posts/cli-anything)

---

*CLI Anything Hubはオープンソースであり、MITライセンスであり、エージェント時代のために構築されています。*
*pip install any tool · Agents call any software · Fork and extend*

---

### 参考文献

1. HackerNoon — *Why AI Agent Reliability Depends More on the Harness Than the Model* (2025)
2. Jannik Reinhard — *Why CLI Tools Are Beating MCP for AI Agents* (Feb 2026) — [jannikreinhard.com](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/)
3. buildmvpfast.com — *MCP Token Cost Problem: Why AI Teams Switch to CLI for Agents* (2026)
4. AAIF / Linux Foundation — *Agentic AI Foundation Standardization Report* (Dec 2025)
5. Dev.to — *I Replaced My LangSmith MCP Server with a 200-Token CLI Skill* (2026)
6. Dev.to — *Agent Harness Engineering: What 8 Months in Production Taught Me* (2025)
7. APEX-Agents Benchmark — *Professional Task Performance on Frontier Models* (2025)
8. Andrej Karpathy — Public statements on agentic AI readiness (2025)
