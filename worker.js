/**
 * CLI Anything — Cloudflare Worker
 *
 * Proxies requests from the frontend to:
 *   1. GitHub API (fetch repo info)
 *   2. Anthropic Claude API (generate CLI code)
 *
 * Environment variable required:
 *   ANTHROPIC_API_KEY — set in Cloudflare Dashboard → Worker → Settings → Variables
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);

    try {
      if (url.pathname === '/github/repo-info') {
        return await handleGitHubInfo(request);
      }

      if (url.pathname === '/generate') {
        return await handleGenerate(request, env);
      }

      return json({ error: 'Not found' }, 404);
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  }
};

// ─── GitHub: fetch repo README + file tree ───
async function handleGitHubInfo(request) {
  const { repo_url } = await request.json();

  const match = repo_url.match(/github\.com\/([^/]+)\/([^/]+)/);
  if (!match) return json({ error: 'Invalid GitHub URL' }, 400);
  const [, owner, repo] = match;

  const headers = { 'User-Agent': 'CLI-Anything-Hub', 'Accept': 'application/vnd.github.v3+json' };

  const [repoRes, readmeRes, treeRes] = await Promise.all([
    fetch(`https://api.github.com/repos/${owner}/${repo}`, { headers }),
    fetch(`https://api.github.com/repos/${owner}/${repo}/readme`, { headers }),
    fetch(`https://api.github.com/repos/${owner}/${repo}/git/trees/HEAD?recursive=1`, { headers }),
  ]);

  const repoData = await repoRes.json();
  if (repoData.message === 'Not Found') {
    return json({ error: 'Repository not found' }, 404);
  }

  let readme = '';
  if (readmeRes.ok) {
    const readmeData = await readmeRes.json();
    readme = atob(readmeData.content);
    if (readme.length > 8000) readme = readme.slice(0, 8000) + '\n\n[truncated]';
  }

  let files = [];
  if (treeRes.ok) {
    const treeData = await treeRes.json();
    files = (treeData.tree || [])
      .filter(f => f.type === 'blob')
      .map(f => f.path)
      .slice(0, 200);
  }

  return json({
    name: repoData.name,
    description: repoData.description,
    language: repoData.language,
    stars: repoData.stargazers_count,
    topics: repoData.topics || [],
    readme,
    files,
  });
}

// ─── Generate: call Claude API using our own key ───
async function handleGenerate(request, env) {
  const apiKey = env.ANTHROPIC_API_KEY;
  if (!apiKey) return json({ error: 'Server misconfigured: missing API key' }, 500);

  const { repo_info, software_name, category } = await request.json();

  const prompt = buildPrompt(repo_info, software_name, category);

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 8000,
      stream: true,
      messages: [{ role: 'user', content: prompt }],
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    return json({ error: `Claude API error: ${response.status} — ${err}` }, response.status);
  }

  // Stream SSE through to browser
  const { readable, writable } = new TransformStream();
  const writer = writable.getWriter();
  const reader = response.body.getReader();

  (async () => {
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        await writer.write(value);
      }
    } finally {
      await writer.close();
    }
  })();

  return new Response(readable, {
    headers: {
      ...CORS_HEADERS,
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
    },
  });
}

function buildPrompt(repo, name, category) {
  return `You are a CLI generator for the CLI Anything project. Your job is to analyze a software repository and generate a complete, production-ready Python CLI wrapper using Click.

## Software: ${name}
## Category: ${category}
## Repository: ${repo.name}
## Description: ${repo.description || 'N/A'}
## Language: ${repo.language || 'N/A'}
## Stars: ${repo.stars || 0}

## README (excerpt):
${repo.readme || 'No README available.'}

## File structure (top files):
${(repo.files || []).slice(0, 80).join('\n')}

---

Based on the above, generate a complete CLI package. Output the following files in order, each wrapped in a code block with the filename as a comment on the first line:

### 1. manifest.json
The CLI Anything manifest with:
- name: "cli-anything-${name.toLowerCase().replace(/\s+/g, '-')}"
- version: "1.0.0"
- description
- capabilities array (e.g., ["image.resize", "image.filter"])
- input_formats, output: "json"
- platform: ["linux", "macos", "windows"]
- install command
- requires array
- tags array

### 2. cli.py
A complete Click-based CLI with:
- Proper click.group() and subcommands
- JSON output mode (--output json)
- Error handling
- Help text for every command and option
- Real subprocess calls to the actual software binary
- At minimum 5-10 useful subcommands based on the software's capabilities

### 3. setup.py
Standard Python package setup.

### 4. test_cli.py
Pytest tests covering the main commands.

Make the CLI practical and production-ready. Call the real software binary — do NOT mock or simulate. Use subprocess.run() to invoke the actual tool.`;
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
  });
}
