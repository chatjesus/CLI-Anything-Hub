> **Note :** Cet article a été traduit automatiquement de l'anglais par Vertex AI Gemini 2.0 Flash. [Lire l'original en anglais](./BLOG_POST.md)

---

# CLI Anything : La couche d'exécution qui manquait à votre agent IA

> *Votre agent est brillant. Il ne peut juste rien faire.*

Vous avez développé un agent IA qui raisonne magnifiquement, planifie stratégiquement et répond avec précision. Puis vous lui avez demandé d'envoyer un message Slack. Il vous a écrit un script Python. Vous lui avez demandé de déclencher un build Docker. Il vous a expliqué la syntaxe du Dockerfile. Vous lui avez demandé de créer un ticket Jira. Il a décrit les endpoints de l'API REST.

L'intelligence est là. Les mains ne le sont pas.

C'est le goulot d'étranglement caché de l'ère agentique — et ce n'est pas la faute du modèle. Une enquête de production de 2025 a révélé que **73 % des déploiements d'agents IA en entreprise ne répondent pas aux attentes de fiabilité au cours de leur première année**. Les échecs ne sont pas dus à un manque d'intelligence. Ils sont dus à un manque d'infrastructure.

Comme l'a dit l'analyse de HackerNoon : *"L'ingénierie du harnais d'agent — la conception de la gestion du contexte, de la sélection des outils, de la récupération des erreurs et de la persistance de l'état — est le principal déterminant de la fiabilité de l'agent, et non la capacité du modèle."*

Andrej Karpathy, co-fondateur d'OpenAI, a déclenché un débat en 2025 lorsqu'il a qualifié les agents IA actuels de "gadoue", avertissant que l'industrie "fait un trop grand saut". Son diagnostic ne portait pas sur les modèles. Il portait sur la plomberie.

CLI Anything est la plomberie.

---

## Les trois façons dont les agents appellent les outils aujourd'hui — et pourquoi elles sont toutes insuffisantes

Avant d'aborder la solution, soyons honnêtes sur le paysage.

### Option 1 : Appels API / SDK bruts

Chaque intégration est écrite à la main. L'agent doit connaître le schéma de l'API, gérer l'authentification, analyser les formats de réponse incohérents et gérer les erreurs différemment pour chaque service. Cela fonctionne pour une ou deux intégrations. Cela ne s'étend pas à cinquante.

### Option 2 : MCP (Model Context Protocol)

MCP est la réponse d'Anthropic à la standardisation des outils, maintenant gouvernée par l'AAIF de la Linux Foundation avec un nombre impressionnant de 97 millions de téléchargements de SDK et plus de 10 000 serveurs publiés. Sur le papier, c'est exactement ce dont les agents ont besoin.

En pratique, il y a un problème critique dont personne ne parle assez : **MCP est un gouffre à contexte**.

Jannik Reinhard, un développeur qui a passé des mois à construire de véritables solutions d'agents d'entreprise, l'a documenté en détail :

> *"Un serveur MCP typique déverse l'ensemble de son schéma dans la fenêtre de contexte de l'agent — définitions d'outils, descriptions de paramètres, flux d'authentification, gestion de l'état, l'ensemble du package."*

Le serveur GitHub MCP consomme à lui seul **~55 000 tokens** avant que l'agent ne fasse un travail réel. C'est à peu près la moitié de la fenêtre de contexte entière de GPT-4o — disparue avant la première question. Connectez une stack d'entreprise typique (GitHub + base de données + Jira + Microsoft Graph) et vous vous retrouvez avec **plus de 150 000 tokens de surcharge de schéma uniquement**.

Le coût en tokens n'est pas seulement un problème d'efficacité. C'est un problème de qualité de raisonnement. Au prix de Claude de 3 $ par million de tokens, cette surcharge se traduit par **0,27 $ par requête, soit 81 000 $ par mois à l'échelle**.

Reinhard a effectué une comparaison directe sur une tâche réelle d'automatisation de la conformité :

| Approche | Coût en tokens |
|----------|-----------|
| MCP (Microsoft Graph) | 145 000 tokens |
| Équivalent CLI | 4 150 tokens |
| **Différence** | **Réduction de 35×** |

L'approche CLI a laissé 95 % de la fenêtre de contexte disponible pour le raisonnement réel. L'approche MCP a divisé le workflow en plusieurs sessions juste pour rester dans les limites.

### Option 3 : Wrappers CLI — La couche intermédiaire manquante

Voici la vérité sous-estimée : les LLM sont des locuteurs CLI natifs. Ils ont été entraînés sur des milliards de lignes d'interactions de terminal — réponses de Stack Overflow, dépôts GitHub, documentation, tutoriels. `git`, `docker`, `curl`, `kubectl` sont des modèles profondément appris. Une commande CLI plus sa sortie `--help` coûte environ **200 tokens** — une amélioration de 50× par rapport à l'initialisation MCP.

Un développeur a remplacé un serveur LangSmith MCP consommant plus de 5 000 tokens par une définition de compétence CLI de 200 tokens : **réduction de 95 % de la surcharge de contexte, aucune perte de fonctionnalité**.

Mais historiquement, les wrappers CLI ont eu leur propre problème : aucune interface standard. Chaque outil a des commandes différentes, des formats de sortie différents, des codes d'erreur différents. Les agents ne pouvaient pas compter sur un comportement cohérent entre les outils.

**C'est le fossé que CLI Anything comble.**

---

## Présentation de CLI Anything Hub

CLI Anything Hub est une collection organisée et communautaire de **plus de 130 wrappers CLI pré-construits et prêts pour les agents** pour les logiciels les plus populaires au monde — construits autour d'une seule interface standardisée à 4 commandes.

Chaque CLI dans le Hub implémente le même contrat. Aucune documentation requise :

```bash
# 1. DISCOVER — l'agent auto-découvre les capacités, aucune authentification nécessaire
cli-anything-slack schema
# → { "name": "cli-anything-slack", "commands": [...], "token_env": "SLACK_BOT_TOKEN" }

# 2. CHECK — test de connectivité idempotent, aucun effet secondaire
cli-anything-slack detect
# → { "status": "ok", "workspace": "MyTeam", "bot": "AgentBot" }

# 3. CALL — sortie JSON structurée, analysable par l'agent
cli-anything-slack --json message send #general "Deploy complete"
# → { "ok": true, "ts": "1742000000.000100" }

# 4. VERSION — suivi de la compatibilité
cli-anything-slack version
# → cli-anything-slack 1.0.0
```

De zéro à fonctionnel en 30 secondes :

```bash
pip install cli-anything-slack
export SLACK_BOT_TOKEN=xoxb-...
cli-anything-slack --json message send #ops "Hello from Agent"
```

Actuellement, plus de 30 CLIs sont en ligne et installables, soutenues par **1 508 tests automatisés**. La roadmap couvre plus de 130 outils dans les domaines de la création et des médias, du SaaS cloud, des outils de développement, des jeux, des services de la vie et plus encore.

---

## L'architecture à quatre couches : où CLI Anything s'intègre

La question la plus fréquente : *"Est-ce que cela est en concurrence avec MCP ? Avec les appels API directs ?"*

La réponse est non. CLI Anything est une couche d'exécution — et elle a une place spécifique et bien définie dans la stack d'agent :

```
┌──────────────────────────────────────────────────────────┐
│  Layer 4: Skills / SKILL.md                               │
│  Routage d'intention — "quel outil, quelle commande, quand"       │
├──────────────────────────────────────────────────────────┤
│  Layer 3: MCP Bridge (optional)                           │
│  Couche de protocole — exposer CLI Anything comme outils MCP        │
│  Gouvernance sémantique + exécution allégée                     │
├──────────────────────────────────────────────────────────┤
│  Layer 2: CLI Anything Hub                                │
│  Exécution standardisée — schema / detect / call --json   │
│  30+ en ligne · 130+ prévus · pip install · sans framework   │
├──────────────────────────────────────────────────────────┤
│  Layer 1: Real APIs & SDKs                                │
│  Communication réelle — Slack / Stripe / Docker / etc.    │
└──────────────────────────────────────────────────────────┘
```

**Couche 1 — APIs réelles :** Les SDKs et endpoints REST réels. CLI Anything les enveloppe afin que les agents n'aient jamais à gérer l'authentification brute, les formats de réponse incohérents ou la gestion des erreurs spécifiques au service.

**Couche 2 — CLI Anything (le cœur) :** L'interface d'exécution standardisée. `schema` donne aux agents une carte complète des capacités — ils n'ont besoin d'aucune documentation externe. `detect` fournit un contrôle de santé idempotent sûr à appeler à tout moment. `--json` garantit que chaque réponse est structurée et analysable par l'agent sans post-traitement.

**Couche 3 — MCP Bridge (optionnel) :** Les CLIs CLI Anything *peuvent* être enveloppées en tant qu'outils MCP. Ce n'est pas un conflit — c'est le meilleur des deux mondes. MCP fournit la gouvernance, les pistes d'audit et la découverte sémantique dans les environnements d'entreprise. CLI Anything fournit la couche d'exécution allégée en dessous, évitant le problème de surcharge de tokens de MCP. L'analyse de HackerNoon sur les harnais d'agents efficaces recommande exactement ce modèle de "divulgation progressive" : *ne montrez aux modèles que ce dont ils ont besoin, quand ils en ont besoin.*

**Couche 4 — Skills / SKILL.md :** La couche de routage d'intention. Les fichiers `SKILL.md` indiquent aux agents *quand* utiliser un outil, *quelle commande spécifique* utiliser et *quel contexte* transmettre. La roadmap de CLI Anything comprend la génération automatique de `SKILL.md` par CLI — rendant chaque outil entièrement plug-and-play dans Cursor, Codex, VS Code, Gemini CLI et tout agent prenant en charge la norme AAIF Agent Skills Standard.

**La stack complète de contrôle d'agent :** *Les compétences routent → (ponts MCP) → CLI exécute → API répond → JSON retourne à l'agent.*

---

## Une vraie démonstration : l'agent automatise un déploiement

Concrétisons cela. Votre agent reçoit une tâche : *"Déployer la nouvelle build, notifier l'équipe et créer un ticket Jira pour le suivi de la release."*

**Étape 1 :** L'agent lit la couche Skills. Il identifie `cli-anything-vercel`, `cli-anything-slack` et `cli-anything-jira` comme les bons outils.

**Étape 2 :** L'agent appelle `schema` sur chacun — 3 réponses JSON légères, environ 600 tokens au total. Comparez cela au chargement de trois serveurs MCP : ~90 000 tokens de surcharge de schéma avant une seule action.

**Étape 3 :** Exécuter en séquence :

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

**Résultat :** Trois outils. Trois pip installs. Une interface standardisée. Zéro code d'intégration personnalisé. 35× moins de tokens que l'équivalent MCP.

Ce n'est pas une démo artificielle. L'équipe d'ingénierie de Vercel a elle-même documenté une découverte similaire : lorsqu'elle a réduit les outils de son agent de 15 à 2 outils ciblés et bien définis, la précision a bondi de **80 % à 100 %**, l'utilisation de tokens a chuté de **37 %** et la vitesse s'est améliorée de **3,5×**. La philosophie de conception de CLI Anything — allégée, ciblée, composable — reflète exactement cette découverte.

---

## Ce qu'il y a dans le Hub

**Actuellement en ligne (plus de 30 CLIs) :**

| Catégorie | Outils |
|----------|-------|
| Création et médias | GIMP, Blender, Inkscape, Audacity, OBS Studio, Kdenlive, Shotcut, Draw.io |
| Communication | Slack, Discord, Telegram, Feishu/Lark |
| SaaS cloud | Stripe, Shopify, HubSpot, Salesforce, Jira, Cloudflare, Vercel, Twilio |
| Outils de développement | Docker, GitHub, Notion, Ollama |
| Bureau et productivité | MS 365, LibreOffice, Google Workspace (Drive + Gmail + Calendar + Sheets + Docs + Chat) |

**Sur la roadmap :**
- **Gaming :** Steam, Roblox, Riot Games, Twitch, Minecraft RCON
- **Vie et local :** DoorDash, Meituan, Uber Eats, Airbnb, Yelp
- **SaaS créatif :** Figma, Canva, Adobe Photoshop (UXP)
- **Publicité :** Google Ads, TikTok Ads, Meta Ads

---

## Le Hub est ouvert — Construisez votre propre CLI

CLI Anything est sous licence MIT. Chaque CLI dans le Hub suit le même contrat minimal, et tout développeur Python peut en construire un en un après-midi.

L'implémentation minimale viable :

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

C'est le cœur. Ajoutez vos commandes spécifiques à l'outil, soumettez une PR ou un GitHub Issue, et votre outil devient disponible pour tous les agents du monde qui utilisent CLI Anything.

---

## Pourquoi c'est important en ce moment

2025–2026 est la fenêtre où les agents IA passent de démos impressionnantes à des systèmes de production fiables. Le benchmark APEX-Agents a testé des modèles de pointe sur des tâches professionnelles réelles — banque, conseil, droit — et a abouti à un résultat qui donne à réfléchir : même les meilleurs modèles n'ont atteint qu'une précision de **24 % pass@1**. Le principal mode de défaillance n'était pas le manque de connaissances. C'était les échecs d'orchestration.

Comme la communauté de recherche sur les harnais d'agents l'a confirmé : *"Au-delà d'un seuil de capacité minimum, l'ingénierie du harnais offre de meilleurs rendements que le remplacement des modèles."* Anthropic a démontré une amélioration de 36 points du benchmark en utilisant le *même* modèle simplement en redessinant l'échafaudage.

CLI Anything est un échafaudage. Il s'attaque directement à la couche d'orchestration — pas avec un nouveau modèle d'IA, pas avec une nouvelle architecture de raisonnement, mais avec le travail peu sexy et peu glamour de la standardisation de la façon dont les agents se connectent aux logiciels.

Chaque CLI ajouté au Hub est une capacité de plus disponible pour tous les agents du monde. C'est la dynamique.

L'avenir des outils d'agents IA, comme l'a dit Jannik Reinhard, *"ne concerne pas le protocole le plus sophistiqué. Il s'agit du chemin le plus court entre le modèle et l'action."*

CLI Anything est ce chemin.

---

## Démarrez

**Installez n'importe quelle CLI et exécutez-la :**
```bash
pip install cli-anything-slack
cli-anything-slack schema   # see what it can do
cli-anything-slack detect   # verify connectivity
```

**Explorez le catalogue complet :** [agentputer.com/cli-anything](https://agentputer.com/cli-anything/)

**Star & fork le Hub :** [github.com/chatjesus/CLI-Anything-Hub](https://github.com/chatjesus/CLI-Anything-Hub)

**Soumettez votre propre CLI :** [Ouvrez un GitHub Issue](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool-name)

**Votez sur Product Hunt :** [producthunt.com/posts/cli-anything](https://www.producthunt.com/posts/cli-anything)

---

*CLI Anything Hub est open source, sous licence MIT et conçu pour l'ère agentique.*
*pip install n'importe quel outil · Les agents appellent n'importe quel logiciel · Fork et étendez*

---

### Références

1. HackerNoon — *Why AI Agent Reliability Depends More on the Harness Than the Model* (2025)
2. Jannik Reinhard — *Why CLI Tools Are Beating MCP for AI Agents* (Feb 2026) — [jannikreinhard.com](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/)
3. buildmvpfast.com — *MCP Token Cost Problem: Why AI Teams Switch to CLI for Agents* (2026)
4. AAIF / Linux Foundation — *Agentic AI Foundation Standardization Report* (Dec 2025)
5. Dev.to — *I Replaced My LangSmith MCP Server with a 200-Token CLI Skill* (2026)
6. Dev.to — *Agent Harness Engineering: What 8 Months in Production Taught Me* (2025)
7. APEX-Agents Benchmark — *Professional Task Performance on Frontier Models* (2025)
8. Andrej Karpathy — Public statements on agentic AI readiness (2025)
