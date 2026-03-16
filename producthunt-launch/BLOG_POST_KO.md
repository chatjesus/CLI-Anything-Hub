> **참고:** 이 글은 Vertex AI Gemini 2.0 Flash를 사용하여 영어 원문에서 자동 번역되었습니다.[영어 원문 읽기](./BLOG_POST.md)

---

# CLI Anything: AI 에이전트에게 부족했던 실행 레이어

> *당신의 에이전트는 훌륭합니다. 단지 아무것도 할 수 없을 뿐입니다.*

당신은 아름답게 추론하고, 전략적으로 계획하며, 정확하게 응답하는 AI 에이전트를 구축했습니다. 그런 다음 Slack 메시지를 보내도록 요청했습니다. 에이전트는 Python 스크립트를 작성했습니다. Docker 빌드를 트리거하도록 요청했습니다. 에이전트는 Dockerfile 구문을 설명했습니다. Jira 티켓을 생성하도록 요청했습니다. 에이전트는 REST API 엔드포인트를 설명했습니다.

지능은 있지만, 손이 없습니다.

이것이 에이전트 시대의 숨겨진 병목 현상이며, 모델의 잘못이 아닙니다. 2025년 생산 설문 조사에 따르면 **엔터프라이즈 AI 에이전트 배포의 73%가 첫 해에 안정성 기대치를 충족하지 못하는 것**으로 나타났습니다. 실패는 지능 부족에서 비롯된 것이 아닙니다. 인프라 부족에서 비롯된 것입니다.

HackerNoon 분석에서 다음과 같이 밝혔습니다. *"에이전트 하네스 엔지니어링(컨텍스트 관리, 도구 선택, 오류 복구 및 상태 지속성 설계)은 모델 기능이 아닌 에이전트 안정성의 주요 결정 요인입니다."*

OpenAI의 공동 창립자인 Andrej Karpathy는 2025년에 현재 AI 에이전트를 "엉성하다"고 부르며 업계가 "너무 큰 도약을 하고 있다"고 경고하면서 논쟁을 촉발했습니다. 그의 진단은 모델에 대한 것이 아니었습니다. 배관에 대한 것이었습니다.

CLI Anything은 바로 그 배관입니다.

---

## 에이전트가 오늘날 도구를 호출하는 세 가지 방법 — 그리고 그 방법들이 모두 부족한 이유

해결책을 살펴보기 전에 먼저 상황을 솔직하게 이야기해 봅시다.

### 옵션 1: Raw API / SDK 호출

모든 통합은 손으로 작성됩니다. 에이전트는 API 스키마를 알고, 인증을 관리하고, 일관성 없는 응답 형식을 파싱하고, 각 서비스에 대해 서로 다른 방식으로 오류를 처리해야 합니다. 이는 한두 개의 통합에는 효과적이지만, 50개로 확장되지는 않습니다.

### 옵션 2: MCP (Model Context Protocol)

MCP는 도구 표준화에 대한 Anthropic의 답변이며, 현재 Linux Foundation의 AAIF에서 관리하며 9,700만 건 이상의 SDK 다운로드와 10,000개 이상의 게시된 서버를 보유하고 있습니다. 이론적으로는 에이전트에게 필요한 바로 그것입니다.

실제로 아무도 충분히 이야기하지 않는 중요한 문제가 있습니다. **MCP는 컨텍스트를 너무 많이 차지합니다**.

실제 엔터프라이즈 에이전트 솔루션을 구축하는 데 몇 달을 보낸 개발자인 Jannik Reinhard는 이를 자세히 문서화했습니다.

> *"일반적인 MCP 서버는 전체 스키마(도구 정의, 매개변수 설명, 인증 흐름, 상태 관리, 전체 패키지)를 에이전트의 컨텍스트 창에 덤프합니다."*

GitHub MCP 서버만으로도 에이전트가 실제 작업을 수행하기 전에 **약 55,000개의 토큰**을 소비합니다. 이는 GPT-4o 전체 컨텍스트 창의 거의 절반에 해당하며, 첫 번째 질문 전에 사라집니다. 일반적인 엔터프라이즈 스택(GitHub + 데이터베이스 + Jira + Microsoft Graph)을 연결하면 **스키마 오버헤드만 150,000개 이상의 토큰**이 필요합니다.

토큰 비용은 효율성 문제일 뿐만 아니라 추론 품질 문제입니다. Claude의 백만 토큰당 3달러 가격으로 이 오버헤드는 **요청당 0.27달러 또는 규모에 따라 월 81,000달러**로 환산됩니다.

Reinhard는 실제 규정 준수 자동화 작업에 대한 직접 비교를 실행했습니다.

| 접근 방식 | 토큰 비용 |
|----------|-----------|
| MCP (Microsoft Graph) | 145,000 tokens |
| CLI equivalent | 4,150 tokens |
| **차이** | **35배 감소** |

CLI 접근 방식은 컨텍스트 창의 95%를 실제 추론에 사용할 수 있도록 했습니다. MCP 접근 방식은 제한 내에 머무르기 위해 워크플로를 여러 세션으로 분할했습니다.

### 옵션 3: CLI 래퍼 — 누락된 중간 레이어

여기 과소 평가된 진실이 있습니다. LLM은 기본적으로 CLI를 사용합니다. LLM은 수십억 줄의 터미널 상호 작용(Stack Overflow 답변, GitHub 리포지토리, 문서, 튜토리얼)을 통해 훈련되었습니다. `git`, `docker`, `curl`, `kubectl`은 깊이 학습된 패턴입니다. CLI 명령과 해당 `--help` 출력은 대략 **200개의 토큰**이 필요하며, 이는 MCP 초기화보다 50배 향상된 것입니다.

한 개발자는 5,000개 이상의 토큰을 소비하는 LangSmith MCP 서버를 200개의 토큰 CLI 스킬 정의로 대체했습니다. **컨텍스트 오버헤드가 95% 감소하고 기능 손실은 없습니다**.

그러나 역사적으로 CLI 래퍼에는 자체적인 문제가 있었습니다. 표준 인터페이스가 없었습니다. 모든 도구에는 다른 명령, 다른 출력 형식, 다른 오류 코드가 있습니다. 에이전트는 도구 간에 일관된 동작을 기대할 수 없었습니다.

**CLI Anything이 채우는 간격이 바로 그것입니다.**

---

## CLI Anything Hub 소개

CLI Anything Hub는 단일 표준화된 4개 명령 인터페이스를 중심으로 구축된 세계에서 가장 인기 있는 소프트웨어에 대한 **130개 이상의 사전 구축된 에이전트 지원 CLI 래퍼**의 선별된 커뮤니티 기반 컬렉션입니다.

Hub의 모든 CLI는 동일한 계약을 구현합니다. 문서가 필요하지 않습니다.

```bash
# 1. DISCOVER — 에이전트가 자체적으로 기능을 검색하며 인증이 필요하지 않습니다.
cli-anything-slack schema
# → { "name": "cli-anything-slack", "commands": [...], "token_env": "SLACK_BOT_TOKEN" }

# 2. CHECK — 멱등성 연결 테스트, 부작용 없음
cli-anything-slack detect
# → { "status": "ok", "workspace": "MyTeam", "bot": "AgentBot" }

# 3. CALL — 구조화된 JSON 출력, 에이전트 파싱 가능
cli-anything-slack --json message send #general "Deploy complete"
# → { "ok": true, "ts": "1742000000.000100" }

# 4. VERSION — 호환성 추적
cli-anything-slack version
# → cli-anything-slack 1.0.0
```

30초 만에 작동:

```bash
pip install cli-anything-slack
export SLACK_BOT_TOKEN=xoxb-...
cli-anything-slack --json message send #ops "Hello from Agent"
```

현재 **1,508개의 자동화된 테스트**로 지원되는 30개 이상의 CLI가 라이브로 설치 가능합니다. 로드맵은 Creative & Media, Cloud SaaS, Dev Tools, Gaming, Life Services 등에서 130개 이상의 도구를 다룹니다.

---

## 4계층 아키텍처: CLI Anything이 적합한 위치

가장 일반적인 질문: *"이것이 MCP와 경쟁하는 것입니까? 직접 API 호출과 경쟁하는 것입니까?"*

대답은 아니오입니다. CLI Anything은 실행 레이어이며 에이전트 스택에서 특정하고 잘 정의된 위치를 가지고 있습니다.

```
┌──────────────────────────────────────────────────────────┐
│  Layer 4: Skills / SKILL.md                               │
│  Intent routing — "which tool, which command, when"       │
├──────────────────────────────────────────────────────────┤
│  Layer 3: MCP Bridge (optional)                           │
│  Protocol layer — expose CLI Anything as MCP tools        │
│  Semantic governance + lean execution                     │
├──────────────────────────────────────────────────────────┤
│  Layer 2: CLI Anything Hub                                │
│  Standardized execution — schema / detect / call --json   │
│  30+ Live · 130+ planned · pip install · framework-free   │
├──────────────────────────────────────────────────────────┤
│  Layer 1: Real APIs & SDKs                                │
│  Actual communication — Slack / Stripe / Docker / etc.    │
└──────────────────────────────────────────────────────────┘
```

**레이어 1 — Real APIs:** 실제 SDK 및 REST 엔드포인트. CLI Anything은 에이전트가 원시 인증, 일관성 없는 응답 형식 또는 서비스별 오류 처리를 처리하지 않도록 래핑합니다.

**레이어 2 — CLI Anything (코어):** 표준화된 실행 인터페이스. `schema`는 에이전트에게 완전한 기능 맵을 제공합니다. 외부 문서가 필요하지 않습니다. `detect`는 언제든지 호출하기에 안전한 멱등성 상태 검사를 제공합니다. `--json`은 모든 응답이 후처리 없이 구조화되고 에이전트가 파싱할 수 있도록 보장합니다.

**레이어 3 — MCP Bridge (선택 사항):** CLI Anything CLI는 MCP 도구로 래핑될 *수 있습니다*. 이는 충돌이 아니라 최고의 장점을 결합한 것입니다. MCP는 엔터프라이즈 환경에서 거버넌스, 감사 추적 및 의미 체계 검색을 제공합니다. CLI Anything은 MCP의 토큰 오버헤드 문제를 피하면서 기본적으로 린 실행 레이어를 제공합니다. 효과적인 에이전트 하네스에 대한 HackerNoon 분석은 정확히 이 "점진적 공개" 패턴을 권장합니다. *모델에 필요한 것만, 필요할 때 보여주십시오.*

**레이어 4 — Skills / SKILL.md:** 의도 라우팅 레이어. `SKILL.md` 파일은 에이전트에게 도구를 *언제* 사용해야 하는지, *어떤 특정 명령*을 사용해야 하는지, *어떤 컨텍스트*를 전달해야 하는지 알려줍니다. CLI Anything 로드맵에는 CLI당 자동 생성된 `SKILL.md`가 포함되어 있어 Cursor, Codex, VS Code, Gemini CLI 및 AAIF Agent Skills Standard를 지원하는 모든 에이전트에서 모든 도구를 완전히 플러그 앤 플레이할 수 있습니다.

**완전한 에이전트 제어 스택:** *스킬 라우팅 → (MCP 브리지) → CLI 실행 → API 응답 → JSON이 에이전트로 반환됩니다.*

---

## 실제 연습: 에이전트가 배포를 자동화합니다.

이를 구체적으로 만들어 보겠습니다. 에이전트는 *"새 빌드를 배포하고, 팀에 알리고, 릴리스 추적을 위한 Jira 티켓을 생성하십시오."*라는 작업을 받습니다.

**1단계:** 에이전트는 스킬 레이어를 읽습니다. `cli-anything-vercel`, `cli-anything-slack` 및 `cli-anything-jira`를 올바른 도구로 식별합니다.

**2단계:** 에이전트는 각 도구에서 `schema`를 호출합니다. 3개의 경량 JSON 응답으로 총 약 600개의 토큰이 필요합니다. 이를 3개의 MCP 서버 로드와 비교하십시오. 단일 작업을 수행하기 전에 스키마 오버헤드가 약 90,000개의 토큰이 필요합니다.

**3단계:** 순서대로 실행합니다.

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

**결과:** 세 개의 도구. 세 개의 pip 설치. 하나의 표준화된 인터페이스. 사용자 지정 통합 코드가 없습니다. MCP에 비해 35배 적은 토큰이 필요합니다.

이것은 꾸며낸 데모가 아닙니다. Vercel의 엔지니어링 팀은 유사한 발견을 문서화했습니다. 에이전트의 도구를 15개에서 2개의 집중적이고 잘 정의된 도구로 줄였을 때 정확도가 **80%에서 100%**로 급증하고, 토큰 사용량이 **37%** 감소하고, 속도가 **3.5배** 향상되었습니다. 린, 집중적, 구성 가능한 CLI Anything의 설계 철학은 정확히 이 발견을 반영합니다.

---

## Hub에 있는 내용

**현재 라이브 (30개 이상의 CLI):**

| 카테고리 | 도구 |
|----------|-------|
| Creative & Media | GIMP, Blender, Inkscape, Audacity, OBS Studio, Kdenlive, Shotcut, Draw.io |
| Communication | Slack, Discord, Telegram, Feishu/Lark |
| Cloud SaaS | Stripe, Shopify, HubSpot, Salesforce, Jira, Cloudflare, Vercel, Twilio |
| Dev Tools | Docker, GitHub, Notion, Ollama |
| Office & Productivity | MS 365, LibreOffice, Google Workspace (Drive + Gmail + Calendar + Sheets + Docs + Chat) |

**로드맵:**
- **Gaming:** Steam, Roblox, Riot Games, Twitch, Minecraft RCON
- **Life & Local:** DoorDash, Meituan, Uber Eats, Airbnb, Yelp
- **Creative SaaS:** Figma, Canva, Adobe Photoshop (UXP)
- **Advertising:** Google Ads, TikTok Ads, Meta Ads

---

## Hub는 열려 있습니다 — 자신만의 CLI를 구축하십시오.

CLI Anything은 MIT 라이선스를 받았습니다. Hub의 모든 CLI는 동일한 최소 계약을 따르며 모든 Python 개발자는 오후에 하나를 구축할 수 있습니다.

최소 실행 가능 구현:

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

이것이 핵심입니다. 도구별 명령을 추가하고 PR 또는 GitHub Issue를 제출하면 도구를 CLI Anything을 사용하는 전 세계 모든 에이전트에서 사용할 수 있습니다.

---

## 지금 이것이 중요한 이유

2025–2026년은 AI 에이전트가 인상적인 데모에서 안정적인 프로덕션 시스템으로 이동하는 시기입니다. APEX-Agents 벤치마크는 실제 전문 작업(은행, 컨설팅, 법률)에서 프런티어 모델을 테스트했으며, 최고의 모델조차도 **24%의 pass@1 정확도**만 달성했다는 냉정한 결과를 발견했습니다. 주요 실패 모드는 지식 격차가 아니었습니다. 오케스트레이션 실패였습니다.

에이전트 하네스 연구 커뮤니티가 수렴한 바와 같이: *"최소 기능 임계값을 넘어서면 하네스 엔지니어링이 모델 교체보다 더 나은 수익을 제공합니다."* Anthropic은 스캐폴딩을 재설계하는 것만으로도 *동일한* 모델을 사용하여 36포인트 벤치마크 개선을 입증했습니다.

CLI Anything은 스캐폴딩입니다. 새로운 AI 모델, 새로운 추론 아키텍처가 아닌 에이전트가 소프트웨어에 연결되는 방식을 표준화하는 매력적이지 않고 화려하지 않은 작업을 통해 오케스트레이션 레이어를 직접적으로 해결합니다.

Hub에 추가된 모든 CLI는 전 세계 모든 에이전트에서 사용할 수 있는 또 다른 기능입니다. 이것이 플라이휠입니다.

Jannik Reinhard가 말했듯이 AI 에이전트 도구의 미래는 *"가장 정교한 프로토콜에 대한 것이 아닙니다. 모델과 작업 간의 가장 린한 경로에 대한 것입니다."*

CLI Anything이 바로 그 경로입니다.

---

## 시작하기

**CLI를 설치하고 실행하십시오.**
```bash
pip install cli-anything-slack
cli-anything-slack schema   # see what it can do
cli-anything-slack detect   # verify connectivity
```

**전체 카탈로그를 탐색하십시오.** [agentputer.com/cli-anything](https://agentputer.com/cli-anything/)

**Hub를 Star & fork하십시오.** [github.com/chatjesus/CLI-Anything-Hub](https://github.com/chatjesus/CLI-Anything-Hub)

**자신만의 CLI를 제출하십시오.** [GitHub Issue 열기](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool-name)

**Product Hunt에서 투표하십시오.** [producthunt.com/posts/cli-anything](https://www.producthunt.com/posts/cli-anything)

---

*CLI Anything Hub는 오픈 소스, MIT 라이선스이며 에이전트 시대를 위해 구축되었습니다.*
*pip install any tool · Agents call any software · Fork and extend*

---

### 참고 자료

1. HackerNoon — *Why AI Agent Reliability Depends More on the Harness Than the Model* (2025)
2. Jannik Reinhard — *Why CLI Tools Are Beating MCP for AI Agents* (Feb 2026) — [jannikreinhard.com](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/)
3. buildmvpfast.com — *MCP Token Cost Problem: Why AI Teams Switch to CLI for Agents* (2026)
4. AAIF / Linux Foundation — *Agentic AI Foundation Standardization Report* (Dec 2025)
5. Dev.to — *I Replaced My LangSmith MCP Server with a 200-Token CLI Skill* (2026)
6. Dev.to — *Agent Harness Engineering: What 8 Months in Production Taught Me* (2025)
7. APEX-Agents Benchmark — *Professional Task Performance on Frontier Models* (2025)
8. Andrej Karpathy — Public statements on agentic AI readiness (2025)
