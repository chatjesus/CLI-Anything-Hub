> **Nota:** Este artigo foi traduzido automaticamente do inglês pelo Vertex AI Gemini 2.0 Flash. [Ler original em inglês](./BLOG_POST.md)

---

# CLI Anything: A Camada de Execução Que Faltava no Seu Agente de IA

> *Seu agente é brilhante. Só não consegue fazer nada.*

Você construiu um agente de IA que raciocina maravilhosamente, planeja estrategicamente e responde com precisão. Então você pediu para ele enviar uma mensagem no Slack. Ele escreveu um script Python para você. Você pediu para ele disparar um build do Docker. Ele explicou a sintaxe do Dockerfile. Você pediu para ele criar um ticket no Jira. Ele descreveu os endpoints da REST API.

A inteligência está lá. As mãos, não.

Este é o gargalo oculto da era agentic — e não é culpa do modelo. Uma pesquisa de produção de 2025 descobriu que **73% das implementações de agentes de IA corporativos não atendem às expectativas de confiabilidade no primeiro ano**. As falhas não são por falta de inteligência. São por falta de infraestrutura.

Como a análise do HackerNoon colocou: *"A engenharia de harness de agentes — o design do gerenciamento de contexto, seleção de ferramentas, recuperação de erros e persistência de estado — é o principal determinante da confiabilidade do agente, não a capacidade do modelo."*

Andrej Karpathy, cofundador da OpenAI, provocou um debate em 2025 quando chamou os agentes de IA atuais de "porcaria", alertando que a indústria está "dando um salto muito grande". Seu diagnóstico não era sobre os modelos. Era sobre o encanamento.

CLI Anything é o encanamento.

---

## As Três Formas Que os Agentes Chamam Ferramentas Hoje — E Por Que Todas Elas Falham

Antes de chegarmos à solução, vamos ser honestos sobre o cenário.

### Opção 1: Chamadas Diretas de API / SDK

Cada integração é escrita à mão. O agente deve conhecer o schema da API, gerenciar a autenticação, analisar formatos de resposta inconsistentes e lidar com erros de forma diferente para cada serviço. Isso funciona para uma ou duas integrações. Não escala para cinquenta.

### Opção 2: MCP (Model Context Protocol)

MCP é a resposta da Anthropic à padronização de ferramentas, agora governada pela AAIF da Linux Foundation com impressionantes 97 milhões de downloads de SDK e mais de 10.000 servidores publicados. No papel, é exatamente o que os agentes precisam.

Na prática, há um problema crítico que ninguém comenta o suficiente: **MCP é um devorador de contexto**.

Jannik Reinhard, um desenvolvedor que passou meses construindo soluções de agentes corporativos reais, documentou isso em detalhes:

> *"Um servidor MCP típico despeja todo o seu schema na janela de contexto do agente — definições de ferramentas, descrições de parâmetros, fluxos de autenticação, gerenciamento de estado, todo o pacote."*

O servidor GitHub MCP sozinho consome **~55.000 tokens** antes que o agente faça qualquer trabalho real. Isso é aproximadamente metade de toda a janela de contexto do GPT-4o — gasta antes da primeira pergunta. Conecte uma stack corporativa típica (GitHub + banco de dados + Jira + Microsoft Graph) e você estará olhando para **mais de 150.000 tokens de overhead de schema sozinho**.

O custo do token não é apenas uma preocupação de eficiência. É um problema de qualidade de raciocínio. No preço do Claude de US$ 3 por milhão de tokens, esse overhead se traduz em **US$ 0,27 por solicitação, ou US$ 81.000 por mês em escala**.

Reinhard executou uma comparação direta em uma tarefa real de automação de conformidade:

| Abordagem | Custo de Token |
|----------|-----------|
| MCP (Microsoft Graph) | 145.000 tokens |
| Equivalente em CLI | 4.150 tokens |
| **Diferença** | **Redução de 35×** |

A abordagem CLI deixou 95% da janela de contexto disponível para raciocínio real. A abordagem MCP dividiu o fluxo de trabalho em várias sessões apenas para ficar dentro dos limites.

### Opção 3: Wrappers de CLI — A Camada Intermediária Que Falta

Aqui está a verdade subestimada: LLMs são falantes nativos de CLI. Eles foram treinados em bilhões de linhas de interações de terminal — respostas do Stack Overflow, repositórios do GitHub, documentação, tutoriais. `git`, `docker`, `curl`, `kubectl` são padrões profundamente aprendidos. Um comando CLI mais sua saída `--help` custa aproximadamente **200 tokens** — uma melhoria de 50× em relação à inicialização do MCP.

Um desenvolvedor substituiu um servidor LangSmith MCP consumindo mais de 5.000 tokens por uma definição de skill CLI de 200 tokens: **redução de 95% no overhead de contexto, zero perda de recursos**.

Mas, historicamente, os wrappers de CLI têm seu próprio problema: nenhuma interface padrão. Cada ferramenta tem comandos diferentes, formatos de saída diferentes, códigos de erro diferentes. Os agentes não podiam confiar em um comportamento consistente entre as ferramentas.

**Essa é a lacuna que o CLI Anything preenche.**

---

## Apresentando o CLI Anything Hub

CLI Anything Hub é uma coleção com curadoria e orientada pela comunidade de **mais de 130 wrappers de CLI pré-construídos e prontos para agentes** para o software mais popular do mundo — construídos em torno de uma única interface padronizada de 4 comandos.

Cada CLI no Hub implementa o mesmo contrato. Nenhuma documentação necessária:

```bash
# 1. DISCOVER — agente auto-descobre capacidades, sem necessidade de autenticação
cli-anything-slack schema
# → { "name": "cli-anything-slack", "commands": [...], "token_env": "SLACK_BOT_TOKEN" }

# 2. CHECK — teste de conectividade idempotente, zero efeitos colaterais
cli-anything-slack detect
# → { "status": "ok", "workspace": "MyTeam", "bot": "AgentBot" }

# 3. CALL — saída JSON estruturada, analisável pelo agente
cli-anything-slack --json message send #general "Deploy complete"
# → { "ok": true, "ts": "1742000000.000100" }

# 4. VERSION — rastreamento de compatibilidade
cli-anything-slack version
# → cli-anything-slack 1.0.0
```

De zero a funcionando em 30 segundos:

```bash
pip install cli-anything-slack
export SLACK_BOT_TOKEN=xoxb-...
cli-anything-slack --json message send #ops "Hello from Agent"
```

Atualmente, mais de 30 CLIs estão ativos e instaláveis, apoiados por **1.508 testes automatizados**. O roadmap cobre mais de 130 ferramentas em Creative & Media, Cloud SaaS, Dev Tools, Gaming, Life Services e muito mais.

---

## A Arquitetura de Quatro Camadas: Onde o CLI Anything Se Encaixa

A pergunta mais comum: *"Isso está competindo com o MCP? Com chamadas diretas de API?"*

A resposta é não. CLI Anything é uma camada de execução — e tem um lugar específico e bem definido na stack do agente:

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

**Camada 1 — APIs Reais:** Os SDKs e endpoints REST reais. CLI Anything envolve estes para que os agentes nunca lidem com autenticação bruta, formatos de resposta inconsistentes ou tratamento de erros específicos do serviço.

**Camada 2 — CLI Anything (o núcleo):** A interface de execução padronizada. `schema` dá aos agentes um mapa de capacidade completo — eles precisam de zero documentação externa. `detect` fornece uma verificação de saúde idempotente segura para chamar a qualquer momento. `--json` garante que cada resposta seja estruturada e analisável pelo agente sem pós-processamento.

**Camada 3 — MCP Bridge (opcional):** CLIs do CLI Anything *podem* ser envolvidos como ferramentas MCP. Isso não é um conflito — é o melhor dos dois mundos. MCP fornece governança, trilhas de auditoria e descoberta semântica em ambientes corporativos. CLI Anything fornece a camada de execução enxuta por baixo, evitando o problema de overhead de token do MCP. A análise do HackerNoon sobre harnesses de agentes eficazes recomenda exatamente este padrão de "divulgação progressiva": *mostre aos modelos apenas o que eles precisam, quando precisam.*

**Camada 4 — Skills / SKILL.md:** A camada de roteamento de intenção. Arquivos `SKILL.md` dizem aos agentes *quando* alcançar uma ferramenta, *qual comando específico* usar e *qual contexto* passar. O roadmap do CLI Anything inclui `SKILL.md` gerado automaticamente por CLI — tornando cada ferramenta totalmente plug-and-play em Cursor, Codex, VS Code, Gemini CLI e qualquer agente que suporte o AAIF Agent Skills Standard.

**A stack de controle de agente completa:** *Skills roteiam → (MCP bridges) → CLI executa → API responde → JSON retorna ao agente.*

---

## Um Passo a Passo Real: Agente Automatiza um Deployment

Vamos tornar isso concreto. Seu agente recebe uma tarefa: *"Implante a nova build, notifique a equipe e crie um ticket no Jira para rastreamento de lançamento."*

**Passo 1:** Agente lê a camada Skills. Ele identifica `cli-anything-vercel`, `cli-anything-slack` e `cli-anything-jira` como as ferramentas certas.

**Passo 2:** Agente chama `schema` em cada um — 3 respostas JSON leves, aproximadamente 600 tokens no total. Compare isso com o carregamento de três servidores MCP: ~90.000 tokens de overhead de schema antes de uma única ação.

**Passo 3:** Execute em sequência:

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

**Resultado:** Três ferramentas. Três instalações pip. Uma interface padronizada. Zero código de integração personalizado. 35× menos tokens do que o equivalente em MCP.

Esta não é uma demonstração forçada. A própria equipe de engenharia da Vercel documentou uma descoberta semelhante: quando eles reduziram as ferramentas de seu agente de 15 para 2 ferramentas focadas e bem definidas, a precisão saltou de **80% para 100%**, o uso de tokens caiu **37%** e a velocidade melhorou **3,5×**. A filosofia de design do CLI Anything — enxuto, focado, composable — espelha exatamente esta descoberta.

---

## O Que Tem no Hub

**Atualmente Ativo (Mais de 30 CLIs):**

| Categoria | Ferramentas |
|----------|-------|
| Creative & Media | GIMP, Blender, Inkscape, Audacity, OBS Studio, Kdenlive, Shotcut, Draw.io |
| Comunicação | Slack, Discord, Telegram, Feishu/Lark |
| Cloud SaaS | Stripe, Shopify, HubSpot, Salesforce, Jira, Cloudflare, Vercel, Twilio |
| Dev Tools | Docker, GitHub, Notion, Ollama |
| Escritório & Produtividade | MS 365, LibreOffice, Google Workspace (Drive + Gmail + Calendar + Sheets + Docs + Chat) |

**No Roadmap:**
- **Gaming:** Steam, Roblox, Riot Games, Twitch, Minecraft RCON
- **Life & Local:** DoorDash, Meituan, Uber Eats, Airbnb, Yelp
- **Creative SaaS:** Figma, Canva, Adobe Photoshop (UXP)
- **Advertising:** Google Ads, TikTok Ads, Meta Ads

---

## O Hub Está Aberto — Construa Seu Próprio CLI

CLI Anything é licenciado sob MIT. Cada CLI no Hub segue o mesmo contrato mínimo, e qualquer desenvolvedor Python pode construir um em uma tarde.

A implementação mínima viável:

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

Esse é o núcleo. Adicione seus comandos específicos da ferramenta, envie um PR ou GitHub Issue, e sua ferramenta se torna disponível para todos os agentes no mundo que usam CLI Anything.

---

## Por Que Isso Importa Agora

2025–2026 é a janela onde os agentes de IA passam de demonstrações impressionantes para sistemas de produção confiáveis. O benchmark APEX-Agents testou modelos de fronteira em tarefas profissionais reais — bancárias, consultoria, direito — e encontrou um resultado preocupante: mesmo os melhores modelos alcançaram apenas **24% de precisão pass@1**. O principal modo de falha não eram lacunas de conhecimento. Eram falhas de orquestração.

Como a comunidade de pesquisa de harness de agentes convergiu: *"Passado um limite mínimo de capacidade, a engenharia de harness oferece melhores retornos do que trocar modelos."* A Anthropic demonstrou uma melhoria de benchmark de 36 pontos usando o *mesmo* modelo apenas redesenhando o scaffolding.

CLI Anything é scaffolding. Ele aborda diretamente a camada de orquestração — não com um novo modelo de IA, não com uma nova arquitetura de raciocínio, mas com o trabalho não sexy e não glamoroso de padronizar como os agentes se conectam ao software.

Cada CLI adicionado ao Hub é mais uma capacidade disponível para todos os agentes no mundo. Essa é a flywheel.

O futuro das ferramentas de agentes de IA, como Jannik Reinhard colocou, *"não é sobre o protocolo mais sofisticado. É sobre o caminho mais enxuto entre o modelo e a ação."*

CLI Anything é esse caminho.

---

## Comece Agora

**Instale qualquer CLI e execute-o:**
```bash
pip install cli-anything-slack
cli-anything-slack schema   # veja o que ele pode fazer
cli-anything-slack detect   # verifique a conectividade
```

**Explore o catálogo completo:** [agentputer.com/cli-anything](https://agentputer.com/cli-anything/)

**Dê uma estrela e faça um fork do Hub:** [github.com/chatjesus/CLI-Anything-Hub](https://github.com/chatjesus/CLI-Anything-Hub)

**Envie seu próprio CLI:** [Abra um GitHub Issue](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool-name)

**Vote no Product Hunt:** [producthunt.com/posts/cli-anything](https://www.producthunt.com/posts/cli-anything)

---

*CLI Anything Hub é open source, licenciado sob MIT e construído para a era agentic.*
*pip install qualquer ferramenta · Agentes chamam qualquer software · Faça um fork e estenda*

---

### Referências

1. HackerNoon — *Why AI Agent Reliability Depends More on the Harness Than the Model* (2025)
2. Jannik Reinhard — *Why CLI Tools Are Beating MCP for AI Agents* (Feb 2026) — [jannikreinhard.com](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/)
3. buildmvpfast.com — *MCP Token Cost Problem: Why AI Teams Switch to CLI for Agents* (2026)
4. AAIF / Linux Foundation — *Agentic AI Foundation Standardization Report* (Dec 2025)
5. Dev.to — *I Replaced My LangSmith MCP Server with a 200-Token CLI Skill* (2026)
6. Dev.to — *Agent Harness Engineering: What 8 Months in Production Taught Me* (2025)
7. APEX-Agents Benchmark — *Professional Task Performance on Frontier Models* (2025)
8. Andrej Karpathy — Public statements on agentic AI readiness (2025)
