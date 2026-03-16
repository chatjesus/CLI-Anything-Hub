> **Nota:** Este artículo fue traducido automáticamente del inglés por Vertex AI Gemini 2.0 Flash. [Leer original en inglés](./BLOG_POST.md)

---

# CLI Anything: La Capa de Ejecución que le Faltaba a tu Agente de IA

> *Tu agente es brillante. Simplemente no puede hacer nada.*

Has construido un agente de IA que razona maravillosamente, planifica estratégicamente y responde con precisión. Luego le pediste que enviara un mensaje de Slack. Te escribió un script de Python. Le pediste que activara una compilación de Docker. Te explicó la sintaxis del Dockerfile. Le pediste que creara un ticket de Jira. Describió los endpoints de la API REST.

La inteligencia está ahí. Las manos no.

Este es el cuello de botella oculto de la era agentic — y no es culpa del modelo. Una encuesta de producción de 2025 encontró que **el 73% de las implementaciones de agentes de IA empresariales no cumplen con las expectativas de confiabilidad dentro de su primer año**. Los fallos no se deben a la falta de inteligencia. Se deben a la falta de infraestructura.

Como lo expresó el análisis de HackerNoon: *"La ingeniería del arnés del agente — el diseño de la gestión del contexto, la selección de herramientas, la recuperación de errores y la persistencia del estado — es el principal determinante de la confiabilidad del agente, no la capacidad del modelo."*

Andrej Karpathy, cofundador de OpenAI, provocó un debate en 2025 cuando calificó a los agentes de IA actuales como "chapuceros", advirtiendo que la industria está "dando un salto demasiado grande". Su diagnóstico no se trataba de los modelos. Se trataba de la fontanería.

CLI Anything es la fontanería.

---

## Las Tres Formas en que los Agentes Llaman a las Herramientas Hoy — Y Por Qué Todas Se Quedan Cortas

Antes de llegar a la solución, seamos honestos sobre el panorama.

### Opción 1: Llamadas Directas a la API / SDK

Cada integración está escrita a mano. El agente debe conocer el esquema de la API, gestionar la autenticación, analizar formatos de respuesta inconsistentes y manejar los errores de manera diferente para cada servicio. Esto funciona para una o dos integraciones. No escala a cincuenta.

### Opción 2: MCP (Model Context Protocol)

MCP es la respuesta de Anthropic a la estandarización de herramientas, ahora gobernada por la AAIF de la Linux Foundation con unas impresionantes 97 millones de descargas de SDK y más de 10,000 servidores publicados. En teoría, es exactamente lo que los agentes necesitan.

En la práctica, hay un problema crítico del que nadie habla lo suficiente: **MCP es un acaparador de contexto**.

Jannik Reinhard, un desarrollador que pasó meses construyendo soluciones de agentes empresariales reales, documentó esto en detalle:

> *"Un servidor MCP típico vuelca todo su esquema en la ventana de contexto del agente — definiciones de herramientas, descripciones de parámetros, flujos de autenticación, gestión del estado, todo el paquete."*

El servidor GitHub MCP por sí solo consume **~55,000 tokens** antes de que el agente haga algún trabajo real. Eso es aproximadamente la mitad de la ventana de contexto completa de GPT-4o — desaparecida antes de la primera pregunta. Conecta una pila empresarial típica (GitHub + base de datos + Jira + Microsoft Graph) y estás viendo **más de 150,000 tokens solo de sobrecarga de esquema**.

El costo de los tokens no es solo una preocupación de eficiencia. Es un problema de calidad de razonamiento. Al precio de Claude de $3 por millón de tokens, esta sobrecarga se traduce en **$0.27 por solicitud, o $81,000 por mes a escala**.

Reinhard realizó una comparación directa en una tarea real de automatización del cumplimiento:

| Enfoque | Costo de Tokens |
|----------|-----------|
| MCP (Microsoft Graph) | 145,000 tokens |
| Equivalente en CLI | 4,150 tokens |
| **Diferencia** | **Reducción de 35×** |

El enfoque de CLI dejó el 95% de la ventana de contexto disponible para el razonamiento real. El enfoque MCP dividió el flujo de trabajo en múltiples sesiones solo para mantenerse dentro de los límites.

### Opción 3: Wrappers de CLI — La Capa Intermedia Faltante

Aquí está la verdad subestimada: los LLM son hablantes nativos de CLI. Fueron entrenados con miles de millones de líneas de interacciones de terminal — respuestas de Stack Overflow, repositorios de GitHub, documentación, tutoriales. `git`, `docker`, `curl`, `kubectl` son patrones profundamente aprendidos. Un comando CLI más su salida `--help` cuesta aproximadamente **200 tokens** — una mejora de 50× sobre la inicialización de MCP.

Un desarrollador reemplazó un servidor LangSmith MCP que consumía más de 5,000 tokens con una definición de habilidad de CLI de 200 tokens: **95% de reducción en la sobrecarga de contexto, cero pérdida de características**.

Pero históricamente, los wrappers de CLI han tenido su propio problema: ninguna interfaz estándar. Cada herramienta tiene diferentes comandos, diferentes formatos de salida, diferentes códigos de error. Los agentes no podían confiar en un comportamiento consistente entre las herramientas.

**Ese es el vacío que CLI Anything llena.**

---

## Presentamos CLI Anything Hub

CLI Anything Hub es una colección curada e impulsada por la comunidad de **más de 130 wrappers de CLI preconstruidos y listos para agentes** para el software más popular del mundo — construidos alrededor de una única interfaz estandarizada de 4 comandos.

Cada CLI en el Hub implementa el mismo contrato. No se requiere documentación:

```bash
# 1. DISCOVER — el agente autodescubre las capacidades, no se necesita autenticación
cli-anything-slack schema
# → { "name": "cli-anything-slack", "commands": [...], "token_env": "SLACK_BOT_TOKEN" }

# 2. CHECK — prueba de conectividad idempotente, cero efectos secundarios
cli-anything-slack detect
# → { "status": "ok", "workspace": "MyTeam", "bot": "AgentBot" }

# 3. CALL — salida JSON estructurada, analizable por el agente
cli-anything-slack --json message send #general "Deploy complete"
# → { "ok": true, "ts": "1742000000.000100" }

# 4. VERSION — seguimiento de la compatibilidad
cli-anything-slack version
# → cli-anything-slack 1.0.0
```

De cero a funcionando en 30 segundos:

```bash
pip install cli-anything-slack
export SLACK_BOT_TOKEN=xoxb-...
cli-anything-slack --json message send #ops "Hello from Agent"
```

Actualmente, más de 30 CLIs están activas e instalables, respaldadas por **1,508 pruebas automatizadas**. La hoja de ruta cubre más de 130 herramientas en Creative & Media, Cloud SaaS, Dev Tools, Gaming, Life Services y más.

---

## La Arquitectura de Cuatro Capas: Dónde Encaja CLI Anything

La pregunta más común: *"¿Esto compite con MCP? ¿Con las llamadas directas a la API?"*

La respuesta es no. CLI Anything es una capa de ejecución — y tiene un lugar específico y bien definido en la pila del agente:

```
┌──────────────────────────────────────────────────────────┐
│  Layer 4: Skills / SKILL.md                               │
│  Enrutamiento de intención — "qué herramienta, qué comando, cuándo"       │
├──────────────────────────────────────────────────────────┤
│  Layer 3: MCP Bridge (opcional)                           │
│  Capa de protocolo — expone CLI Anything como herramientas MCP        │
│  Gobernanza semántica + ejecución eficiente                     │
├──────────────────────────────────────────────────────────┤
│  Layer 2: CLI Anything Hub                                │
│  Ejecución estandarizada — schema / detect / call --json   │
│  30+ Activas · 130+ planificadas · pip install · sin framework   │
├──────────────────────────────────────────────────────────┤
│  Layer 1: APIs y SDKs Reales                                │
│  Comunicación real — Slack / Stripe / Docker / etc.    │
└──────────────────────────────────────────────────────────┘
```

**Capa 1 — APIs Reales:** Los SDKs y endpoints REST reales. CLI Anything envuelve estos para que los agentes nunca tengan que lidiar con la autenticación sin procesar, los formatos de respuesta inconsistentes o el manejo de errores específicos del servicio.

**Capa 2 — CLI Anything (el núcleo):** La interfaz de ejecución estandarizada. `schema` le da a los agentes un mapa de capacidades completo — no necesitan documentación externa. `detect` proporciona una verificación de estado idempotente que es segura de llamar en cualquier momento. `--json` asegura que cada respuesta esté estructurada y sea analizable por el agente sin post-procesamiento.

**Capa 3 — MCP Bridge (opcional):** Las CLIs de CLI Anything *pueden* ser envueltas como herramientas MCP. Esto no es un conflicto — es lo mejor de ambos mundos. MCP proporciona gobernanza, pistas de auditoría y descubrimiento semántico en entornos empresariales. CLI Anything proporciona la capa de ejecución eficiente subyacente, evitando el problema de sobrecarga de tokens de MCP. El análisis de HackerNoon sobre arneses de agentes efectivos recomienda exactamente este patrón de "divulgación progresiva": *mostrar a los modelos solo lo que necesitan, cuando lo necesitan.*

**Capa 4 — Skills / SKILL.md:** La capa de enrutamiento de intención. Los archivos `SKILL.md` les dicen a los agentes *cuándo* buscar una herramienta, *qué comando específico* usar y *qué contexto* pasar. La hoja de ruta de CLI Anything incluye `SKILL.md` autogenerados por CLI — haciendo que cada herramienta sea completamente plug-and-play en Cursor, Codex, VS Code, Gemini CLI y cualquier agente que admita el estándar AAIF Agent Skills.

**La pila completa de control del agente:** *Skills route → (MCP bridges) → CLI executes → API responds → JSON returns to agent.*

---

## Un Recorrido Real: El Agente Automatiza una Implementación

Hagamos esto concreto. Tu agente recibe una tarea: *"Implementar la nueva compilación, notificar al equipo y crear un ticket de Jira para el seguimiento de la versión."*

**Paso 1:** El agente lee la capa Skills. Identifica `cli-anything-vercel`, `cli-anything-slack` y `cli-anything-jira` como las herramientas correctas.

**Paso 2:** El agente llama a `schema` en cada uno — 3 respuestas JSON ligeras, aproximadamente 600 tokens en total. Compara esto con la carga de tres servidores MCP: ~90,000 tokens de sobrecarga de esquema antes de una sola acción.

**Paso 3:** Ejecutar en secuencia:

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

**Resultado:** Tres herramientas. Tres instalaciones de pip. Una interfaz estandarizada. Cero código de integración personalizado. 35× menos tokens que el equivalente de MCP.

Esta no es una demostración artificiosa. El propio equipo de ingeniería de Vercel documentó un descubrimiento similar: cuando redujeron las herramientas de su agente de 15 a 2 herramientas enfocadas y bien definidas, la precisión saltó de **80% a 100%**, el uso de tokens se redujo **37%** y la velocidad mejoró **3.5×**. La filosofía de diseño de CLI Anything — eficiente, enfocada, componible — refleja exactamente este hallazgo.

---

## Qué Hay en el Hub

**Actualmente Activas (Más de 30 CLIs):**

| Categoría | Herramientas |
|----------|-------|
| Creative & Media | GIMP, Blender, Inkscape, Audacity, OBS Studio, Kdenlive, Shotcut, Draw.io |
| Comunicación | Slack, Discord, Telegram, Feishu/Lark |
| Cloud SaaS | Stripe, Shopify, HubSpot, Salesforce, Jira, Cloudflare, Vercel, Twilio |
| Dev Tools | Docker, GitHub, Notion, Ollama |
| Office & Productivity | MS 365, LibreOffice, Google Workspace (Drive + Gmail + Calendar + Sheets + Docs + Chat) |

**En la Hoja de Ruta:**
- **Gaming:** Steam, Roblox, Riot Games, Twitch, Minecraft RCON
- **Life & Local:** DoorDash, Meituan, Uber Eats, Airbnb, Yelp
- **Creative SaaS:** Figma, Canva, Adobe Photoshop (UXP)
- **Advertising:** Google Ads, TikTok Ads, Meta Ads

---

## El Hub Está Abierto — Construye Tu Propia CLI

CLI Anything tiene licencia MIT. Cada CLI en el Hub sigue el mismo contrato mínimo, y cualquier desarrollador de Python puede construir uno en una tarde.

La implementación mínima viable:

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

Ese es el núcleo. Agrega tus comandos específicos de la herramienta, envía un PR o GitHub Issue, y tu herramienta estará disponible para todos los agentes en el mundo que usen CLI Anything.

---

## Por Qué Esto Importa Ahora Mismo

2025–2026 es la ventana donde los agentes de IA pasan de demostraciones impresionantes a sistemas de producción confiables. El benchmark APEX-Agents probó modelos de frontera en tareas profesionales reales — banca, consultoría, derecho — y encontró un resultado aleccionador: incluso los mejores modelos lograron solo **24% de precisión pass@1**. El principal modo de falla no fueron las lagunas de conocimiento. Fueron las fallas de orquestación.

Como la comunidad de investigación del arnés de agentes ha convergido en: *"Más allá de un umbral de capacidad mínimo, la ingeniería del arnés ofrece mejores retornos que el intercambio de modelos."* Anthropic demostró una mejora de 36 puntos en el benchmark usando el *mismo* modelo solo rediseñando el andamiaje.

CLI Anything es andamiaje. Aborda directamente la capa de orquestación — no con un nuevo modelo de IA, no con una nueva arquitectura de razonamiento, sino con el trabajo poco atractivo y poco glamoroso de estandarizar cómo los agentes se conectan al software.

Cada CLI agregada al Hub es una capacidad más disponible para todos los agentes en el mundo. Ese es el volante de inercia.

El futuro de las herramientas de agentes de IA, como lo expresó Jannik Reinhard, *"no se trata del protocolo más sofisticado. Se trata del camino más eficiente entre el modelo y la acción."*

CLI Anything es ese camino.

---

## Comienza

**Instala cualquier CLI y ejecútala:**
```bash
pip install cli-anything-slack
cli-anything-slack schema   # see what it can do
cli-anything-slack detect   # verify connectivity
```

**Explora el catálogo completo:** [agentputer.com/cli-anything](https://agentputer.com/cli-anything/)

**Marca con una estrella y haz un fork del Hub:** [github.com/chatjesus/CLI-Anything-Hub](https://github.com/chatjesus/CLI-Anything-Hub)

**Envía tu propia CLI:** [Open a GitHub Issue](https://github.com/chatjesus/CLI-Anything-Hub/issues/new?labels=cli-submission&title=[CLI+Submission]+your-tool-name)

**Vota en Product Hunt:** [producthunt.com/posts/cli-anything](https://www.producthunt.com/posts/cli-anything)

---

*CLI Anything Hub es de código abierto, con licencia MIT y está construido para la era agentic.*
*pip install any tool · Agents call any software · Fork and extend*

---

### Referencias

1. HackerNoon — *Why AI Agent Reliability Depends More on the Harness Than the Model* (2025)
2. Jannik Reinhard — *Why CLI Tools Are Beating MCP for AI Agents* (Feb 2026) — [jannikreinhard.com](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/)
3. buildmvpfast.com — *MCP Token Cost Problem: Why AI Teams Switch to CLI for Agents* (2026)
4. AAIF / Linux Foundation — *Agentic AI Foundation Standardization Report* (Dec 2025)
5. Dev.to — *I Replaced My LangSmith MCP Server with a 200-Token CLI Skill* (2026)
6. Dev.to — *Agent Harness Engineering: What 8 Months in Production Taught Me* (2025)
7. APEX-Agents Benchmark — *Professional Task Performance on Frontier Models* (2025)
8. Andrej Karpathy — Public statements on agentic AI readiness (2025)
