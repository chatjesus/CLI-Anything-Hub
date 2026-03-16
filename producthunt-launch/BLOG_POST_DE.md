> **Hinweis:** Dieser Artikel wurde automatisch aus dem Englischen von Vertex AI Gemini 2.0 Flash übersetzt. [Englisches Original lesen](./BLOG_POST.md)

---

# CLI Anything: Die Ausführungsschicht, die Ihrem KI-Agenten gefehlt hat

> *Ihr Agent ist brillant. Er kann nur nichts tun.*

Sie haben einen KI-Agenten entwickelt, der hervorragend argumentiert, strategisch plant und präzise antwortet. Dann haben Sie ihn gebeten, eine Slack-Nachricht zu senden. Er hat Ihnen ein Python-Skript geschrieben. Sie haben ihn gebeten, einen Docker-Build auszulösen. Er hat die Dockerfile-Syntax erklärt. Sie haben ihn gebeten, ein Jira-Ticket zu erstellen. Er hat die REST-API-Endpunkte beschrieben.

Die Intelligenz ist da. Die Hände fehlen.

Dies ist der versteckte Engpass der Agenten-Ära – und es ist nicht die Schuld des Modells. Eine Produktionsumfrage aus dem Jahr 2025 ergab, dass **73 % der Enterprise-KI-Agenten-Deployments innerhalb ihres ersten Jahres die Zuverlässigkeitserwartungen nicht erfüllen**. Die Fehler resultieren nicht aus mangelnder Intelligenz. Sie resultieren aus mangelnder Infrastruktur.

Wie die HackerNoon-Analyse es formulierte: *"Agent Harness Engineering – die Gestaltung von Kontextmanagement, Tool-Auswahl, Fehlerbehebung und Statuspersistenz – ist der Hauptfaktor für die Zuverlässigkeit von Agenten, nicht die Modellfähigkeit."*

Andrej Karpathy, Mitbegründer von OpenAI, löste 2025 eine Debatte aus, als er aktuelle KI-Agenten als "Schlamperei" bezeichnete und die Industrie davor warnte, "einen zu großen Sprung zu machen". Seine Diagnose betraf nicht die Modelle. Es ging um die Infrastruktur.

CLI Anything ist die Infrastruktur.

---

## Die drei Arten, wie Agenten heute Tools aufrufen – und warum sie alle scheitern

Bevor wir zur Lösung kommen, wollen wir ehrlich über die Landschaft sprechen.

### Option 1: Rohe API / SDK-Aufrufe

Jede Integration ist handgeschrieben. Der Agent muss das API-Schema kennen, die Authentifizierung verwalten, inkonsistente Antwortformate parsen und Fehler für jeden Dienst unterschiedlich behandeln. Dies funktioniert für ein oder zwei Integrationen. Es skaliert nicht auf fünfzig.

### Option 2: MCP (Model Context Protocol)

MCP ist die Antwort von Anthropic auf die Tool-Standardisierung, die jetzt von der AAIF der Linux Foundation mit beeindruckenden 97 Millionen SDK-Downloads und über 10.000 veröffentlichten Servern verwaltet wird. Auf dem Papier ist es genau das, was Agenten brauchen.

In der Praxis gibt es ein kritisches Problem, über das niemand genug spricht: **MCP ist ein Kontext-Fresser**.

Jannik Reinhard, ein Entwickler, der Monate damit verbracht hat, echte Enterprise-Agenten-Lösungen zu entwickeln, dokumentierte dies ausführlich:

> *"Ein typischer MCP-Server speichert sein gesamtes Schema im Kontextfenster des Agenten – Tool-Definitionen, Parameterbeschreibungen, Authentifizierungsabläufe, Statusverwaltung, das ganze Paket."*

Allein der GitHub MCP-Server verbraucht **~55.000 Tokens**, bevor der Agent tatsächlich etwas tut. Das ist ungefähr die Hälfte des gesamten Kontextfensters von GPT-4o – weg vor der ersten Frage. Verbinden Sie einen typischen Enterprise-Stack (GitHub + Datenbank + Jira + Microsoft Graph) und Sie erhalten **150.000+ Tokens allein für Schema-Overhead**.

Die Token-Kosten sind nicht nur ein Effizienzproblem. Es ist ein Problem der Argumentationsqualität. Bei Claudes Preis von 3 US-Dollar pro Million Tokens entspricht dieser Overhead **0,27 US-Dollar pro Anfrage oder 81.000 US-Dollar pro Monat in der Größenordnung**.

Reinhard führte einen direkten Vergleich bei einer realen Compliance-Automatisierungsaufgabe durch:

| Ansatz | Token-Kosten |
|----------|-----------|
| MCP (Microsoft Graph) | 145.000 Tokens |
| CLI-Äquivalent | 4.150 Tokens |
| **Differenz** | **35× Reduktion** |

Der CLI-Ansatz ließ 95 % des Kontextfensters für die eigentliche Argumentation frei. Der MCP-Ansatz teilte den Workflow in mehrere Sitzungen auf, nur um innerhalb der Grenzen zu bleiben.

### Option 3: CLI-Wrapper – Die fehlende mittlere Schicht

Hier ist die unterschätzte Wahrheit: LLMs sind native CLI-Sprecher. Sie wurden mit Milliarden von Zeilen Terminal-Interaktionen trainiert – Stack Overflow-Antworten, GitHub-Repositories, Dokumentation, Tutorials. `git`, `docker`, `curl`, `kubectl` sind tief erlernte Muster. Ein CLI-Befehl plus seine `--help`-Ausgabe kostet ungefähr **200 Tokens** – eine 50-fache Verbesserung gegenüber der MCP-Initialisierung.

Ein Entwickler ersetzte einen LangSmith MCP-Server, der über 5.000 Tokens verbrauchte, durch eine 200-Token-CLI-Skill-Definition: **95 % Reduktion des Kontext-Overheads, kein Feature-Verlust**.

Aber historisch gesehen hatten CLI-Wrapper ihr eigenes Problem: keine Standardschnittstelle. Jedes Tool hat unterschiedliche Befehle, unterschiedliche Ausgabeformate, unterschiedliche Fehlercodes. Agenten konnten sich nicht auf ein konsistentes Verhalten über alle Tools hinweg verlassen.

**Das ist die Lücke, die CLI Anything füllt.**

---

## Einführung von CLI Anything Hub

CLI Anything Hub ist eine kuratierte, Community-gesteuerte Sammlung von **über 130 vorgefertigten, Agenten-bereiten CLI-Wrappern** für die weltweit beliebteste Software – aufgebaut um eine einzige standardisierte 4-Befehl-Schnittstelle.

Jede CLI im Hub implementiert denselben Vertrag. Keine Dokumentation erforderlich:

```bash
# 1. DISCOVER — Agent entdeckt selbstständig Fähigkeiten, keine Authentifizierung erforderlich
cli-anything-slack schema
# → { "name": "cli-anything-slack", "commands": [...], "token_env": "SLACK_BOT_TOKEN" }

# 2. CHECK — idempotenter Konnektivitätstest, keine Nebenwirkungen
cli-anything-slack detect
# → { "status": "ok", "workspace": "MyTeam", "bot": "AgentBot" }

# 3. CALL — strukturierte JSON-Ausgabe, vom Agenten parsbar
cli-anything-slack --json message send #general "Deploy complete"
# → { "ok": true, "ts": "1742000000.000100" }

# 4. VERSION — Kompatibilitätsverfolgung
cli-anything-slack version
# → cli-anything-slack 1.0.0
```

Von Null auf Funktionieren in 30 Sekunden:

```bash
pip install cli-anything-slack
export SLACK_BOT_TOKEN=xoxb-...
cli-anything-slack --json message send #ops "Hello from Agent"
```

Derzeit sind über 30 CLIs live und installierbar, unterstützt von **1.508 automatisierten Tests**. Die Roadmap umfasst über 130 Tools aus den Bereichen Creative & Media, Cloud SaaS, Dev Tools, Gaming, Life Services und mehr.

---

## Die Vier-Schichten-Architektur: Wo CLI Anything passt

Die häufigste Frage: *"Konkurriert dies mit MCP? Mit direkten API-Aufrufen?"*

Die Antwort ist nein. CLI Anything ist eine Ausführungsschicht – und sie hat einen spezifischen, klar definierten Platz im Agenten-Stack:

```
┌──────────────────────────────────────────────────────────┐
│  Layer 4: Skills / SKILL.md                               │
│  Intent-Routing — "welches Tool, welcher Befehl, wann"       │
├──────────────────────────────────────────────────────────┤
│  Layer 3: MCP Bridge (optional)                           │
│  Protokollschicht — CLI Anything als MCP-Tools bereitstellen        │
│  Semantische Governance + schlanke Ausführung                     │
├──────────────────────────────────────────────────────────┤
│  Layer 2: CLI Anything Hub                                │
│  Standardisierte Ausführung — schema / detect / call --json   │
│  30+ Live · 130+ geplant · pip install · Framework-frei   │
├──────────────────────────────────────────────────────────┤
│  Layer 1: Reale APIs & SDKs                                │
│  Tatsächliche Kommunikation — Slack / Stripe / Docker / etc.    │
└──────────────────────────────────────────────────────────┘
```

**Layer 1 – Reale APIs:** Die tatsächlichen SDKs und REST-Endpunkte. CLI Anything umschließt diese, sodass Agenten sich nie mit roher Authentifizierung, inkonsistenten Antwortformaten oder dienstspezifischer Fehlerbehandlung befassen müssen.

**Layer 2 – CLI Anything (der Kern):** Die standardisierte Ausführungsschnittstelle. `schema` gibt Agenten eine vollständige Fähigkeitskarte – sie benötigen keine externe Dokumentation. `detect` bietet eine idempotente Gesundheitsprüfung, die jederzeit sicher aufgerufen werden kann. `--json` stellt sicher, dass jede Antwort strukturiert und vom Agenten parsbar ist, ohne Nachbearbeitung.

**Layer 3 – MCP Bridge (optional):** CLI Anything CLIs *können* als MCP-Tools umschlossen werden. Dies ist kein Konflikt – es ist das Beste aus beiden Welten. MCP bietet Governance, Audit-Trails und semantische Erkennung in Enterprise-Umgebungen. CLI Anything bietet die schlanke Ausführungsschicht darunter und vermeidet das Token-Overhead-Problem von MCP. Die HackerNoon-Analyse zu effektiven Agenten-Harnesses empfiehlt genau dieses "Progressive Disclosure"-Muster: *Zeigen Sie Modellen nur das, was sie brauchen, wann sie es brauchen.*

**Layer 4 – Skills / SKILL.md:** Die Intent-Routing-Schicht. `SKILL.md`-Dateien sagen Agenten, *wann* sie nach einem Tool greifen sollen, *welchen spezifischen Befehl* sie verwenden sollen und *welchen Kontext* sie übergeben sollen. Die CLI Anything-Roadmap umfasst automatisch generierte `SKILL.md` pro CLI – wodurch jedes Tool vollständig Plug-and-Play über Cursor, Codex, VS Code, Gemini CLI und jeden Agenten wird, der den AAIF Agent Skills Standard unterstützt.

**Der komplette Agenten-Kontroll-Stack:** *Skills routen → (MCP Bridges) → CLI führt aus → API antwortet → JSON kehrt zum Agenten zurück.*

---

## Eine echte exemplarische Vorgehensweise: Agent automatisiert ein Deployment

Machen wir das konkret. Ihr Agent erhält eine Aufgabe: *"Stellen Sie den neuen Build bereit, benachrichtigen Sie das Team und erstellen Sie ein Jira-Ticket für die Release-Verfolgung."*

**Schritt 1:** Der Agent liest die Skills-Schicht. Er identifiziert `cli-anything-vercel`, `cli-anything-slack` und `cli-anything-jira` als die richtigen Tools.

**Schritt 2:** Der Agent ruft `schema` für jedes Tool auf – 3 Lightweight-JSON-Antworten, insgesamt ungefähr 600 Tokens. Vergleichen Sie dies mit dem Laden von drei MCP-Servern: ~90.000 Tokens Schema-Overhead vor einer einzigen Aktion.

**Schritt 3:** Ausführung in Sequenz:

```bash
# Deploy
cli-anything-vercel --json deploy --project my-app
# → { "url": "https://my-app-xyz.vercel.app", "state": "READY" }

# Team benachrichtigen
cli-anything-slack --json message send #releases "v2.1.0 live → https://my-app-xyz.vercel.app"
# → { "ok": true, "ts": "1742000000.000100" }

# Release verfolgen
cli-anything-jira --json issue create --project REL --summary "Release v2.1.0" --type Task
# → { "id": "REL-847", "status": "To Do", "url": "..." }
```

**Ergebnis:** Drei Tools. Drei pip-Installationen. Eine standardisierte Schnittstelle. Null benutzerdefinierter Integrationscode. 35× weniger Tokens als das MCP-Äquivalent.

Dies ist keine konstruierte Demo. Das eigene Engineering-Team von Vercel dokumentierte eine ähnliche Entdeckung: Als sie die Tools ihres Agenten von 15 auf 2 fokussierte, klar definierte Tools reduzierten, stieg die Genauigkeit von **80 % auf 100 %**, der Token-Verbrauch sank um **37 %** und die Geschwindigkeit verbesserte sich um **3,5×**. Die Designphilosophie von CLI Anything – schlank, fokussiert, zusammensetzbar – spiegelt genau diese Erkenntnis wider.

---

## Was im Hub enthalten ist

**Derzeit Live (30+ CLIs):**

| Kategorie | Tools |
|----------|-------|
| Creative & Media | GIMP, Blender, Inkscape, Audacity, OBS Studio, Kdenlive, Shotcut, Draw.io |
| Kommunikation | Slack, Discord, Telegram, Feishu/Lark |
| Cloud SaaS | Stripe, Shopify, HubSpot, Salesforce, Jira, Cloudflare, Vercel, Twilio |
| Dev Tools | Docker, GitHub, Notion, Ollama |
| Office & Productivity | MS 365, LibreOffice, Google Workspace (Drive + Gmail + Calendar + Sheets + Docs + Chat) |

**Auf der Roadmap:**
- **Gaming:** Steam, Roblox, Riot Games, Twitch, Minecraft RCON
- **Life & Local:** DoorDash, Meituan, Uber Eats, Airbnb, Yelp
- **Creative SaaS:** Figma, Canva, Adobe Photoshop (UXP)
- **Advertising:** Google Ads, TikTok Ads, Meta Ads

---

## Der Hub ist offen – Erstellen Sie Ihre eigene CLI

CLI Anything ist MIT-lizenziert. Jede CLI im Hub folgt demselben minimalen Vertrag, und jeder Python-Entwickler kann eine an einem Nachmittag erstellen.

Die minimal lebensfähige Implementierung:

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

Das ist der Kern. Fügen Sie Ihre toolspezifischen Befehle hinzu, senden Sie einen PR oder ein GitHub Issue, und Ihr Tool wird für jeden Agenten auf der Welt verfügbar, der CLI Anything verwendet.

---

## Warum das gerade jetzt wichtig ist

2025–2026 ist das Fenster, in dem KI-Agenten von beeindruckenden Demos zu zuverlässigen Produktionssystemen übergehen. Der APEX-Agents-Benchmark testete Frontier-Modelle auf reale professionelle Aufgaben – Bankwesen, Beratung, Recht – und fand ein ernüchterndes Ergebnis: Selbst die besten Modelle erreichten nur **24 % pass@1 Genauigkeit**. Der Hauptfehler war nicht Wissenslücken. Es waren Orchestrierungsfehler.

Wie sich die Agent Harness Research Community geeinigt hat: *"Ab einer minimalen Fähigkeitsschwelle liefert Harness Engineering bessere Ergebnisse als das Austauschen von Modellen."* Anthropic demonstrierte eine Benchmark-Verbesserung um 36 Punkte mit dem *gleichen* Modell, nur durch die Neugestaltung des Scaffolding.

CLI Anything ist Scaffolding. Es adressiert direkt die Orchestrierungsschicht – nicht mit einem neuen KI-Modell, nicht mit einer neuen Argumentationsarchitektur, sondern mit der unsexy, unglamourösen Arbeit der Standardisierung, wie Agenten sich mit Software verbinden.

Jede CLI, die dem Hub hinzugefügt wird, ist eine weitere Fähigkeit, die jedem Agenten auf der Welt zur Verfügung steht. Das ist das Schwungrad.

Die Zukunft der KI-Agenten-Tooling, wie Jannik Reinhard es formulierte, *"dreht sich nicht um das ausgefeilteste Protokoll. Es geht um den schlanksten Pfad zwischen dem Modell und der Aktion."*

CLI Anything ist dieser Pfad.

---

## Loslegen

**Installieren Sie eine beliebige CLI und führen Sie sie aus:**
```bash
pip install cli-anything-slack
cli-anything-slack schema   # sehen Sie, was es kann
cli-anything-slack detect   # Konnektivität überprüfen
```

**Entdecken Sie den vollständigen Katalog:** [agentputer.com/cli-anything](https://agentputer.com/cli-anything/)

**Star & Fork des Hub:** [github.com/chatjesus/CLI-Anything-Hub](https://github.com/chatjesus/CLI-Anything-Hub)

**Senden Sie Ihre eigene CLI:** [Open a GitHub Issue](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool-name)

**Vote on Product Hunt:** [producthunt.com/posts/cli-anything](https://www.producthunt.com/posts/cli-anything)

---

*CLI Anything Hub ist Open Source, MIT-lizenziert und für die Agenten-Ära entwickelt.*
*pip install any tool · Agents call any software · Fork and extend*

---

### Referenzen

1. HackerNoon — *Why AI Agent Reliability Depends More on the Harness Than the Model* (2025)
2. Jannik Reinhard — *Why CLI Tools Are Beating MCP for AI Agents* (Feb 2026) — [jannikreinhard.com](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/)
3. buildmvpfast.com — *MCP Token Cost Problem: Why AI Teams Switch to CLI for Agents* (2026)
4. AAIF / Linux Foundation — *Agentic AI Foundation Standardization Report* (Dec 2025)
5. Dev.to — *I Replaced My LangSmith MCP Server with a 200-Token CLI Skill* (2026)
6. Dev.to — *Agent Harness Engineering: What 8 Months in Production Taught Me* (2025)
7. APEX-Agents Benchmark — *Professional Task Performance on Frontier Models* (2025)
8. Andrej Karpathy — Public statements on agentic AI readiness (2025)
