/* CLI Anything — Shared Components */

/* Resolve relative paths depending on page depth */
function basePath(){
  const p=window.location.pathname;
  if(p.includes('/cli/'))return '../';
  return '';
}

/* ── Nav ── */
function renderNav(active){
  const b=basePath();
  return `<nav class="nav">
  <div class="nav-inner">
    <a href="${b}index.html" class="nav-logo">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
      CLI Anything
    </a>
    <div class="nav-links">
      <a href="${b}cli/index.html"${active==='registry'?' style="color:var(--g900)"':''}>Registry</a>
      <a href="${b}docs.html"${active==='docs'?' style="color:var(--g900)"':''}>Docs</a>
      <a href="${b}about.html"${active==='about'?' style="color:var(--g900)"':''}>About</a>
      <a href="${b}index.html#integrations">Integrations</a>
      <a href="#" class="nav-cta" onclick="if(typeof openModal==='function')openModal();return false">Submit a CLI</a>
    </div>
  </div>
</nav>`;
}

/* ── Footer ── */
function renderFooter(){
  const b=basePath();
  return `<footer class="footer">
  <div class="footer-inner">
    <span class="footer-copy">clianything.ai &middot; Making software agent-native</span>
    <div class="footer-links">
      <a href="${b}cli/index.html">Registry</a>
      <a href="${b}docs.html">Docs</a>
      <a href="${b}about.html">About</a>
      <a href="#">GitHub</a>
    </div>
  </div>
</footer>`;
}

/* ── Card renderer ── */
function renderCard(c, opts){
  const name='cli-anything-'+c.n;
  const install='pip install '+name;
  const ic=getIconClass(c.c);
  const b=basePath();
  const linkable=opts&&opts.linkable;
  const tag=linkable?'a':'div';
  const href=linkable?' href="'+b+'cli/'+c.n+'.html"':'';
  return `<${tag} class="card"${href} data-c="${c.c}">
    <div class="card-top">
      <div class="card-icon${c.logo?'':' '+ic}">${c.logo?'<img src="'+c.logo+'" alt="'+c.n+'" onerror="this.parentNode.classList.add(\''+ic+'\');this.replaceWith(document.createTextNode(\''+c.n.slice(0,2).toUpperCase()+'\'))">':c.n.slice(0,2).toUpperCase()}</div>
      <div><div class="card-name">${name}</div><div class="card-ver">v${c.v}</div></div>
    </div>
    <div class="card-desc">${c.d}</div>
    <div class="card-tags">${(c.t||[]).map(t=>'<span class="card-tag">'+t+'</span>').join('')}</div>
    <div class="card-foot">
      <div class="card-stats"><span>${c.dl} installs</span><span>${c.ts} tests</span></div>
      <span class="card-install" onclick="event.preventDefault();event.stopPropagation();cpInstall(event,'${install}')">${install}</span>
    </div>
  </${tag}>`;
}

function renderCards(items, containerId, opts){
  document.getElementById(containerId).innerHTML=items.map(c=>renderCard(c,opts)).join('');
}

/* ── Copy install command ── */
function cpInstall(e,cmd){
  e.stopPropagation();
  if(e.preventDefault)e.preventDefault();
  navigator.clipboard.writeText(cmd);
  const el=e.target;const o=el.textContent;
  el.textContent='copied';el.style.color='var(--green-muted)';
  setTimeout(()=>{el.textContent=o;el.style.color=''},1200);
}

/* ── Head tags for SEO ── */
function seoHead(title,desc,canonical){
  document.title=title;
  let m=document.querySelector('meta[name="description"]');
  if(!m){m=document.createElement('meta');m.name='description';document.head.appendChild(m)}
  m.content=desc;
  if(canonical){
    let l=document.querySelector('link[rel="canonical"]');
    if(!l){l=document.createElement('link');l.rel='canonical';document.head.appendChild(l)}
    l.href=canonical;
  }
}

/* ── Detail page renderer ── */
function renderDetailPage(slug){
  const pkg=getPkg(slug);
  if(!pkg){document.body.innerHTML='<p style="padding:40px;text-align:center">Package not found.</p>';return}

  const name='cli-anything-'+pkg.n;
  const install='pip install '+name;
  const ic=getIconClass(pkg.c);
  const catLabel=getCatLabel(pkg.c);
  const catColor=getCatColor(pkg.c);
  const b=basePath();

  // SEO
  const title=name+' — CLI Anything | '+pkg.d.split('.')[0];
  const desc='Install '+name+': '+pkg.d+' CLI wrapper for AI agents. '+pkg.ts+' tests passing, '+pkg.dl+' installs.';
  seoHead(title,desc);

  // JSON-LD
  const ld=document.createElement('script');
  ld.type='application/ld+json';
  ld.textContent=JSON.stringify({
    "@context":"https://schema.org",
    "@type":"SoftwareApplication",
    "name":name,
    "applicationCategory":"DeveloperApplication",
    "operatingSystem":(pkg.plat||[]).join(', '),
    "description":pkg.ld||pkg.d,
    "softwareVersion":pkg.v,
    "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}
  });
  document.head.appendChild(ld);

  // Related packages (same category, excluding self)
  const related=getPkgsByCategory(pkg.c).filter(p=>p.n!==pkg.n).slice(0,4);

  const content=`
  ${renderNav('registry')}
  <div class="breadcrumb">
    <a href="${b}index.html">Home</a><span>/</span>
    <a href="${b}cli/index.html">Registry</a><span>/</span>
    <a href="${b}cli/index.html#${pkg.c}">${catLabel}</a><span>/</span>
    ${name}
  </div>
  <div class="detail-hero">
    <div class="detail-hero-inner">
      <div class="detail-icon${pkg.logo?'':' '+ic}" style="${pkg.logo?'':'background:'+catColor}">
        ${pkg.logo?'<img src="'+pkg.logo+'" alt="'+pkg.n+'" onerror="this.replaceWith(document.createTextNode(\''+pkg.n.slice(0,2).toUpperCase()+'\'))">':pkg.n.slice(0,2).toUpperCase()}
      </div>
      <div class="detail-meta">
        <h1>${name}</h1>
        <div class="detail-ver">v${pkg.v} &middot; ${catLabel}</div>
        <div class="detail-desc">${pkg.ld||pkg.d}</div>
        <div class="detail-actions">
          <div class="detail-install-box" onclick="cpInstall(event,'${install}')">${install}</div>
          <div class="card-tags" style="margin:0">${(pkg.t||[]).map(t=>'<span class="card-tag">'+t+'</span>').join('')}</div>
        </div>
      </div>
    </div>
  </div>

  <div class="detail-body">
    <div class="detail-main">
      <div class="detail-section">
        <h2>Capabilities</h2>
        <div class="cap-grid">
          ${(pkg.caps||[]).map(c=>'<div class="cap-item">'+c+'</div>').join('')}
        </div>
      </div>

      <div class="detail-section">
        <h2>Example commands</h2>
        <div class="cmd-list">
          ${(pkg.cmds||[]).map(c=>'<div class="cmd-item"><span class="cmd-prompt">$</span>'+c.replace(/</g,'&lt;')+'</div>').join('')}
        </div>
      </div>

      <div class="detail-section">
        <h2>Manifest</h2>
        <div class="code-card">
          <div class="code-bar"><span>manifest.json</span><small>JSON</small></div>
          <pre class="code-pre">${generateManifestJSON(pkg)}</pre>
        </div>
      </div>

      ${related.length?`<div class="detail-section">
        <h2>Related packages</h2>
        <div class="related-grid">
          ${related.map(r=>`<a class="related-card" href="${b}cli/${r.n}.html">
            <div class="related-name">cli-anything-${r.n}</div>
            <div class="related-desc">${r.d.split('.')[0]}</div>
          </a>`).join('')}
        </div>
      </div>`:''}
    </div>

    <div class="detail-sidebar">
      <div class="sidebar-card">
        <h3>Package info</h3>
        <div class="sidebar-row"><span class="sidebar-label">Version</span><span class="sidebar-value">${pkg.v}</span></div>
        <div class="sidebar-row"><span class="sidebar-label">Downloads</span><span class="sidebar-value">${pkg.dl}</span></div>
        <div class="sidebar-row"><span class="sidebar-label">Tests passing</span><span class="sidebar-value">${pkg.ts}</span></div>
        <div class="sidebar-row"><span class="sidebar-label">Quality</span><span class="sidebar-value">${pkg.q?Math.round(pkg.q*100)+'%':'N/A'}</span></div>
        <div class="sidebar-row"><span class="sidebar-label">Output</span><span class="sidebar-value">JSON</span></div>
      </div>

      <div class="sidebar-card">
        <h3>Platforms</h3>
        <div class="sidebar-tags">
          ${(pkg.plat||[]).map(p=>'<span class="platform-badge">'+p+'</span>').join('')}
        </div>
      </div>

      <div class="sidebar-card">
        <h3>Requirements</h3>
        ${(pkg.req||[]).map(r=>'<div class="req-item">'+r+'</div>').join('')||'<div class="req-item" style="color:var(--g500)">None specified</div>'}
      </div>

      <div class="sidebar-card">
        <h3>Formats</h3>
        <div class="sidebar-row"><span class="sidebar-label">Input</span><span class="sidebar-value" style="font-family:var(--mono);font-size:12px">${(pkg.inf||[]).join(', ')||'N/A'}</span></div>
        <div class="sidebar-row"><span class="sidebar-label">Output</span><span class="sidebar-value" style="font-family:var(--mono);font-size:12px">${(pkg.outf||[]).join(', ')||'N/A'}</span></div>
      </div>
    </div>
  </div>
  ${renderFooter()}`;

  document.body.innerHTML=content;
}

function generateManifestJSON(pkg){
  const name='cli-anything-'+pkg.n;
  const obj={
    name:name,
    version:pkg.v,
    description:pkg.d.split('.')[0],
    capabilities:pkg.caps||[],
    input_formats:pkg.inf||[],
    output:'json',
    platform:pkg.plat||[],
    install:'pip install '+name,
    requires:pkg.req||[],
    tests_passed:pkg.ts,
    quality_score:pkg.q||0
  };
  // Manually format for syntax highlighting
  const json=JSON.stringify(obj,null,2);
  return json
    .replace(/"([^"]+)":/g,'<span class="k">"$1"</span>:')
    .replace(/: "([^"]+)"/g,': <span class="v">"$1"</span>')
    .replace(/: (\d+\.?\d*)/g,': <span class="n">$1</span>')
    .replace(/"([^"]+)"(?=,|\n|\])/g,'<span class="v">"$1"</span>');
}
