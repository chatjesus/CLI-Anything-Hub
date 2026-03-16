# CLI Anything — Project Context

## What is this?
CLI Anything (clianything.ai) is a website that CLI-ifies all world's software and makes them available for AI agents — essentially a "CLI App Store for Agents".

## Brand & Domain
- Name: **CLI Anything**
- Domain: **clianything.ai** (purchased on Cloudflare)
- GitHub: https://github.com/chatjesus/CLI-Anything-Hub

## Architecture

### Frontend (Static HTML — works on file:// protocol, no server needed)
- `index.html` — Main landing page (hero, terminal demo, metrics, registry preview, manifest spec, integrations, submit modal)
- `style.css` — All styles (extracted from inline, supports all pages)
- `packages.js` — Central data store with 55+ CLI packages across 10 categories
- `shared.js` — Reusable components (nav, footer, card renderer, detail page renderer, SEO helpers)
- `cli/index.html` — Full registry browse page with search + category filters
- `cli/*.html` — 59 individual package detail pages (SEO-optimized, JSON-LD structured data)
- `docs.html` — Documentation (install, manifest spec, capabilities, agent integration, MCP bridge)
- `about.html` — Mission, problem/solution, open source

### Backend
- `worker.js` — Cloudflare Worker API proxy
  - `/github/repo-info` — Fetches repo README + file tree from GitHub API
  - `/generate` — Calls Claude API (streaming SSE) to generate CLI code
  - Deployed at: `https://clianything.contract-tools.workers.dev/`
  - Requires `ANTHROPIC_API_KEY` env variable in Cloudflare Dashboard

## Tech Stack
- Pure HTML/CSS/JS (no frameworks, no build step)
- IBM Plex Sans/Mono fonts
- Light professional theme (inspired by Linear/Stripe, NOT dark AI theme)
- Simple Icons CDN for app logos (`https://cdn.simpleicons.org/{name}/{color}`)
- Fallback to letter abbreviation when icon unavailable (Microsoft, Adobe, VS Code icons removed from Simple Icons)
- Cloudflare Worker for API proxy (CORS + secure API key)

## 10 Categories
image (Image/Design), video (Video/Audio), 3d (3D/Gaming), office (Office/Docs), dev (Developer Tools), ai (AI/ML), comm (Communication), database (Database), cloud (Cloud/Infra), browser (Browser)

## CRITICAL Design Rules (DO NOT CHANGE)
- **LIGHT THEME ONLY** — White background (#fff), dark text (#212529). NO dark theme, NO dark backgrounds, NO neon colors, NO green-on-black terminal aesthetics. The user explicitly rejected dark/geeky AI themes ("减少AI感"). Design inspired by **Linear and Stripe** — clean, professional, minimal.
- **No API key in frontend** — User said "填写key这个动作不安全". API key stored as Cloudflare Worker secret.
- **IBM Plex Sans/Mono fonts** — Professional look. No monospace-heavy layouts.
- **No gradients, no glows, no emoji** — Clean borders, subtle shadows only.
- **SEO-first** — Each software gets its own detail page for search indexing with JSON-LD.
- **file:// compatible** — All pages work when opened locally without a server.
- **Real app icons** — User wants real software icons, not generic ones. Use Simple Icons CDN.
- **Color palette**: --white:#fff, --g50:#f8f9fa through --g900:#212529, --blue:#2563eb (accent). See style.css :root for full palette.

## Key Files to Know
- `packages.js` — Edit this to add/remove/modify CLI packages. Each package has: n(name), v(version), d(description), ld(long description), c(category), t(tags), dl(downloads), ts(tests), logo, q(quality score), caps(capabilities), cmds(example commands), plat(platforms), req(requirements), inf(input formats), outf(output formats)
- `shared.js` — renderNav(), renderFooter(), renderCard(), renderDetailPage(), cpInstall(), generateManifestJSON()
- `style.css` — All CSS including responsive breakpoints at 900px and 640px

## Pending Work
- Deploy latest worker.js to Cloudflare and set ANTHROPIC_API_KEY env variable
- Connect domain clianything.ai to the static site (Cloudflare Pages or similar)
- Some icons still use letter fallback — could find alternative icon sources for Microsoft/Adobe
