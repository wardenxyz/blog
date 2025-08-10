(function(){
  // Dynamic header height -> CSS variable --header-h
  function setHeaderHeight(){
    const header = document.querySelector('.site-header');
    if(!header) return;
    const h = header.getBoundingClientRect().height;
    document.documentElement.style.setProperty('--header-h', h + 'px');
  }

  // Maintain --toc-h for mobile to reserve space when TOC is fixed
  function setTocHeightVar(){
    try{
      const toc = document.getElementById('toc');
      const isMobile = window.matchMedia('(max-width: 959px)').matches;
      if(!toc || !isMobile){
        document.documentElement.style.setProperty('--toc-h', '0px');
        return;
      }
  // Measure the actual TOC bar height (including paddings/border)
  const rect = toc.getBoundingClientRect();
  const h = rect.height || 0;
      document.documentElement.style.setProperty('--toc-h', Math.ceil(h) + 'px');
    }catch(_e){
      document.documentElement.style.setProperty('--toc-h', '0px');
    }
  }

  // Compute scroll offset so the heading is fully visible below sticky bars
  function computeScrollOffset(){
    try{
      const header = document.querySelector('.site-header');
      const cssVar = getComputedStyle(document.documentElement).getPropertyValue('--header-h').trim();
      const headerH = cssVar ? parseFloat(cssVar) : (header ? header.getBoundingClientRect().height : 72);
    let extra = 0;
      const isMobile = window.matchMedia('(max-width: 959px)').matches;
      if(isMobile){
        const tocEl = document.getElementById('toc');
        if(tocEl){
      const h = tocEl.getBoundingClientRect().height || 0;
      extra += h;
        }
      }
      const baseBuffer = isMobile ? 16 : 12; // slightly larger buffer so heading is fully visible
      return headerH + extra + baseBuffer;
    }catch(_e){
      return 84;
    }
  }

  // Set once early to avoid jump
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setHeaderHeight);
  } else {
    setHeaderHeight();
  }

  window.addEventListener('resize', ()=>{
  setHeaderHeight();
  setTocHeightVar();
  });

  const btn = document.getElementById('backToTop');
  const onScroll = () => {
    if(window.scrollY > 300){
      btn.style.display = 'flex';
      btn.style.opacity = '1';
    }else{
      btn.style.opacity = '0';
      btn.style.display = 'none';
    }
  };
  window.addEventListener('scroll', onScroll, {passive:true});
  btn.addEventListener('click', () => window.scrollTo({top:0, behavior:'smooth'}));

  const toc = document.getElementById('toc');
  if(toc){
    toc.addEventListener('click', (e)=>{
      const a = e.target.closest('a');
      if(!a) return;
      const id = decodeURIComponent((a.getAttribute('href')||'').slice(1));
      const target = id && document.getElementById(id);
      if(target){
        e.preventDefault();
        const isMobile = window.matchMedia('(max-width: 959px)').matches;
        // Collapse first on mobile so we can compute correct offset without TOC bar
        if(isMobile){
          toc.classList.add('collapsed');
          const titleEl = toc.querySelector('.toc-title');
          if(titleEl){ titleEl.setAttribute('aria-expanded','false'); }
          setTocHeightVar();
        }
        // Scroll with header offset and update hash without jump
    const doScroll = () => {
          try{
      const offset = computeScrollOffset();
            const rect = target.getBoundingClientRect();
            const top = rect.top + window.scrollY - offset;
            window.scrollTo({ top, behavior: 'smooth' });
            if(id){
              try{ history.pushState(null, '', '#' + encodeURIComponent(id)); }catch(_e){ /* noop */ }
            }
          }catch(_e){
            target.scrollIntoView({behavior:'smooth', block:'start'});
          }
        };
        // Wait a frame to let layout update after collapsing
  requestAnimationFrame(() => setTimeout(doScroll, 0));
      }
    });
  }

  // Code copy functionality
  function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('.content pre');
    codeBlocks.forEach(pre => {
      // Skip if already wrapped
      if (pre.parentElement.classList.contains('code-container')) return;
      
      // Wrap pre element
      const container = document.createElement('div');
      container.className = 'code-container';
      pre.parentNode.insertBefore(container, pre);
      container.appendChild(pre);
      
      // Create copy button
      const copyBtn = document.createElement('button');
      copyBtn.className = 'copy-btn';
      copyBtn.textContent = '复制';
      copyBtn.setAttribute('aria-label', '复制代码');
      
      // Add click handler
      copyBtn.addEventListener('click', async () => {
        const code = pre.querySelector('code');
        const text = code ? code.textContent : pre.textContent;
        
        try {
          await navigator.clipboard.writeText(text);
          copyBtn.textContent = '已复制';
          copyBtn.classList.add('copied');
          setTimeout(() => {
            copyBtn.textContent = '复制';
            copyBtn.classList.remove('copied');
          }, 2000);
        } catch (err) {
          // Fallback for older browsers
          const textArea = document.createElement('textarea');
          textArea.value = text;
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand('copy');
          document.body.removeChild(textArea);
          
          copyBtn.textContent = '已复制';
          copyBtn.classList.add('copied');
          setTimeout(() => {
            copyBtn.textContent = '复制';
            copyBtn.classList.remove('copied');
          }, 2000);
        }
      });
      
      container.appendChild(copyBtn);
    });
  }

  // Initialize copy buttons when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addCopyButtons);
  } else {
    addCopyButtons();
  }

  // Mobile nav toggle
  function initMenuToggle(){
    const toggle = document.getElementById('menuToggle');
    const nav = document.getElementById('primaryNav');
    if(!toggle || !nav) return;
    const mq = window.matchMedia('(max-width: 800px)');

    function closeMenu(){
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded','false');
    }
    function openMenu(){
      nav.classList.add('open');
      toggle.setAttribute('aria-expanded','true');
    }
    toggle.addEventListener('click', ()=>{
      if(nav.classList.contains('open')) closeMenu(); else openMenu();
      // header height may change when nav opens/closes on mobile
      requestAnimationFrame(setHeaderHeight);
    });
    // Close on resize to desktop
    mq.addEventListener('change', e=>{ if(!e.matches) { closeMenu(); requestAnimationFrame(setHeaderHeight);} });
    // Close when clicking a link (for single page feel)
    nav.addEventListener('click', e=>{ if(e.target.closest('a')) { closeMenu(); requestAnimationFrame(setHeaderHeight);} });
  }

  // Collapsible TOC on mobile
  function initCollapsibleToc(){
    const toc = document.getElementById('toc');
    if(!toc) return;
    const title = toc.querySelector('.toc-title');
    if(!title) return;
    const mq = window.matchMedia('(max-width: 959px)');
    // Default to collapsed on mobile; expanded on larger screens
    function syncForViewport(){
      if(mq.matches){ toc.classList.add('collapsed'); }
      else{ toc.classList.remove('collapsed'); }
      title.setAttribute('role','button');
      title.setAttribute('tabindex','0');
      title.setAttribute('aria-expanded', String(!toc.classList.contains('collapsed')));
      setTocHeightVar();
    }
    syncForViewport();
    mq.addEventListener('change', syncForViewport);
    title.addEventListener('click', ()=>{
      if(!mq.matches) return;
      toc.classList.toggle('collapsed');
      title.setAttribute('aria-expanded', String(!toc.classList.contains('collapsed')));
      setTocHeightVar();
    });
    title.addEventListener('keydown', (e)=>{
      if(!mq.matches) return;
      if(e.key === 'Enter' || e.key === ' '){
        e.preventDefault();
        toc.classList.toggle('collapsed');
        title.setAttribute('aria-expanded', String(!toc.classList.contains('collapsed')));
        setTocHeightVar();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ()=>{
      initMenuToggle();
      initCollapsibleToc();
      initSearch();
      initContentHighlight();
  initThemeToggle();
      setHeaderHeight();
  setTocHeightVar();
      // Offset scroll for initial hash navigation (skip if highlight param is present)
      try{
        const params = new URLSearchParams(window.location.search);
        if(!params.get('highlight') && window.location.hash){
          const id = decodeURIComponent(window.location.hash.slice(1));
          const target = id && document.getElementById(id);
          if(target){
            const doScroll=()=>{
              const offset = computeScrollOffset();
              const rect = target.getBoundingClientRect();
              const top = rect.top + window.scrollY - offset;
              window.scrollTo({top, behavior:'auto'});
            };
            requestAnimationFrame(()=> setTimeout(doScroll, 0));
          }
        }
      }catch(_e){/* noop */}
    });
  } else {
    initMenuToggle();
    initCollapsibleToc();
    initSearch();
    initContentHighlight();
  initThemeToggle();
    setHeaderHeight();
  setTocHeightVar();
    // Same for immediate load state
    try{
      const params = new URLSearchParams(window.location.search);
      if(!params.get('highlight') && window.location.hash){
        const id = decodeURIComponent(window.location.hash.slice(1));
        const target = id && document.getElementById(id);
        if(target){
          const offset = computeScrollOffset();
          const rect = target.getBoundingClientRect();
          const top = rect.top + window.scrollY - offset;
          window.scrollTo({top, behavior:'auto'});
        }
      }
    }catch(_e){/* noop */}
  }
})();

// --- Search ---
function initSearch(){
  const input = document.getElementById('searchInput');
  const results = document.getElementById('searchResults');
  const base = (document.body.getAttribute('data-base')||'');
  if(!input || !results) return;

  let index = [];
  let active = -1;

  async function ensureIndex(){
    if(index.length) return index;
    try{
      const res = await fetch(base + 'search.json', {cache:'no-store'});
      index = await res.json();
    }catch(e){
      index = [];
    }
    return index;
  }

  function render(items, words){
    results.innerHTML = '';
    if(!items.length){ results.classList.remove('open'); return; }
    for(const it of items.slice(0, 50)){
      const a = document.createElement('a');
      a.className = 'search-item';
      a.setAttribute('role','option');
      const qParam = words && words.length ? ('?highlight=' + encodeURIComponent(words.join(' '))) : '';
      a.href = base + it.path + qParam;
      const titleHTML = highlightHtml(it.title, words);
      const pathHTML = highlightHtml(it.path, words);
      const snippetText = makeSnippet(it.content||'', words, 40, 140);
      const snippetHTML = snippetText ? `<div class=\"search-item-snippet\">${highlightHtml(snippetText, words)}</div>` : '';
      a.innerHTML = `<div class=\"search-item-title\">${titleHTML}</div><div class=\"search-item-path\">${pathHTML}</div>${snippetHTML}`;
      results.appendChild(a);
    }
    results.classList.add('open');
    active = -1;
  }

  function escapeHtml(s){
    return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  function matchItems(q){
    const qs = q.trim().toLowerCase();
    if(!qs) return [];
    const words = Array.from(new Set(qs.split(/\s+/).filter(Boolean))).slice(0, 8);
    return index.filter(it =>{
      const hay = (it.title + ' ' + (it.content||'') + ' ' + (it.tags||'').toString()).toLowerCase();
      return words.every(w => hay.includes(w));
    }).map(it => ({title: it.title, path: it.path, content: it.content||''}));
  }

  let t;
  input.addEventListener('input', async () =>{
    clearTimeout(t);
    const q = input.value;
    if(!q.trim()){ results.classList.remove('open'); results.innerHTML=''; return; }
    t = setTimeout(async ()=>{
      await ensureIndex();
      const items = matchItems(q);
      const words = Array.from(new Set(q.trim().toLowerCase().split(/\s+/).filter(Boolean))).slice(0, 8);
      render(items, words);
    }, 120);
  });

  input.addEventListener('keydown', (e)=>{
    if(!results.classList.contains('open')) return;
    const items = Array.from(results.querySelectorAll('.search-item'));
    if(!items.length) return;
    if(e.key === 'ArrowDown'){
      e.preventDefault(); active = (active + 1) % items.length; setActive(items);
    }else if(e.key === 'ArrowUp'){
      e.preventDefault(); active = (active - 1 + items.length) % items.length; setActive(items);
    }else if(e.key === 'Enter'){
      if(active>=0){ e.preventDefault(); items[active].click(); }
    }else if(e.key === 'Escape'){
      // keep results, but refocus the input and select text
      e.preventDefault();
      input.focus();
      input.select();
    }
  });

  // Global ESC: if focus moved elsewhere, ESC returns focus to search input
  document.addEventListener('keydown', (e)=>{
    if(e.key === 'Escape'){
      if(document.activeElement !== input){
        input.focus();
        input.select();
      }
    }
  });

  document.addEventListener('click', (e)=>{
    if(e.target === input || results.contains(e.target)) return;
    results.classList.remove('open');
  });

  function setActive(items){
    items.forEach((el,i)=>{
      if(i===active){ el.classList.add('active'); el.setAttribute('aria-selected','true'); el.scrollIntoView({block:'nearest'}); }
      else{ el.classList.remove('active'); el.removeAttribute('aria-selected'); }
    });
  }

  function highlightHtml(text, words){
    if(!words || !words.length) return escapeHtml(text);
    let pattern = words.map(escapeRegExp).join('|');
    if(!pattern) return escapeHtml(text);
    const re = new RegExp(`(${pattern})`, 'ig');
    const parts = text.split(re);
    return parts.map((p, i) => i % 2 === 1 ? `<mark>${escapeHtml(p)}</mark>` : escapeHtml(p)).join('');
  }

  function makeSnippet(text, words, ctxBefore=30, ctxLen=120){
    if(!text) return '';
    const lc = text.toLowerCase();
    const ws = (words||[]).filter(Boolean);
    let pos = -1;
    for(const w of ws){
      const i = lc.indexOf(w);
      if(i !== -1){ pos = i; break; }
    }
    if(pos === -1){ pos = 0; }
    const start = Math.max(0, pos - ctxBefore);
    let snippet = text.slice(start, start + ctxLen);
    if(start > 0) snippet = '…' + snippet;
    if(start + ctxLen < text.length) snippet = snippet + '…';
    return snippet;
  }

  function escapeRegExp(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
}

// --- Theme toggle ---
function initThemeToggle(){
  const btn = document.getElementById('themeToggle');
  if(!btn) return;
  const docEl = document.documentElement;

  function applyIcon(theme){
    // Use simple icons: sun for light, moon for dark, monitor for auto
    if(theme === 'light') btn.textContent = '☀️';
    else if(theme === 'dark') btn.textContent = '🌙';
    else btn.textContent = '🖥️';
  }

  function getSystemDark(){
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function currentTheme(){
    try{ const t = localStorage.getItem('theme'); if(t==='light'||t==='dark') return t; }catch(_e){}
    return getSystemDark() ? 'dark' : 'light';
  }

  function setTheme(t){
    if(t === 'light' || t === 'dark'){
      try{ localStorage.setItem('theme', t); }catch(_e){}
      docEl.setAttribute('data-theme', t);
    }else{
      try{ localStorage.removeItem('theme'); }catch(_e){}
      docEl.removeAttribute('data-theme');
    }
    applyIcon(t);
    // Update Mermaid diagrams theme if available
    try{
      if(window.mermaid && mermaid.initialize){
        const theme = (t==='dark') ? 'dark' : (t==='light' ? 'default' : (getSystemDark() ? 'dark' : 'default'));
        mermaid.initialize({ startOnLoad: false, theme });
        if(mermaid.run){ mermaid.run({ querySelector: '.mermaid' }); }
      }
    }catch(_e){}
  }

  // Initialize
  setTheme(currentTheme());

  // Cycle: light -> dark -> auto -> light
  btn.addEventListener('click', ()=>{
    let t;
    try{ t = localStorage.getItem('theme'); }catch(_e){ t = null; }
    if(t === 'light') setTheme('dark');
    else if(t === 'dark') setTheme(null);
    else setTheme('light');
  });

  // React to system scheme changes when in auto mode
  const mql = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
  if(mql && mql.addEventListener){
    mql.addEventListener('change', ()=>{
      try{ if(!localStorage.getItem('theme')) setTheme(null); }catch(_e){ setTheme(null); }
    });
  }
}

// Highlight terms on destination page based on ?highlight= query and scroll to first
function initContentHighlight(){
  try{
    const params = new URLSearchParams(window.location.search);
    const q = params.get('highlight');
    if(!q) return;
    const words = Array.from(new Set(q.trim().toLowerCase().split(/\s+/).filter(Boolean)));
    if(!words.length) return;
    const content = document.getElementById('content');
    if(!content) return;
    const first = highlightInElement(content, words);
    if(first){
  const offset = (typeof computeScrollOffset === 'function') ? computeScrollOffset() : (function(){
    const header = document.querySelector('.site-header');
    const cssVar = getComputedStyle(document.documentElement).getPropertyValue('--header-h').trim();
    const headerH = cssVar ? parseFloat(cssVar) : (header ? header.getBoundingClientRect().height : 72);
    return headerH + 8;
  })();
      const go = ()=>{
        const rect = first.getBoundingClientRect();
        const top = rect.top + window.scrollY - offset;
        window.scrollTo({top, behavior:'smooth'});
      };
      // try now and after layout settles
      go();
      requestAnimationFrame(()=> setTimeout(go, 50));
    }
  }catch(e){ /* noop */ }
}

function highlightInElement(root, words){
  if(!root || !words || !words.length) return null;
  const pattern = words.map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
  if(!pattern) return null;
  const re = new RegExp(`(${pattern})`, 'gi');
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node){
      if(!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      const pe = node.parentElement;
      if(pe && (pe.closest('.MathJax') || pe.closest('mjx-container'))) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  let firstMark = null;
  const nodes = [];
  let n;
  while((n = walker.nextNode())) nodes.push(n);
  for(const textNode of nodes){
    const text = textNode.nodeValue;
    if(!re.test(text)) { re.lastIndex = 0; continue; }
    re.lastIndex = 0;
    const frag = document.createDocumentFragment();
    let lastIndex = 0;
    text.replace(re, (m, _g1, offset)=>{
      if(offset > lastIndex) frag.appendChild(document.createTextNode(text.slice(lastIndex, offset)));
      const mark = document.createElement('mark');
      mark.className = 'hl';
      mark.textContent = m;
      if(!firstMark) firstMark = mark;
      frag.appendChild(mark);
      lastIndex = offset + m.length;
      return m;
    });
    if(lastIndex < text.length) frag.appendChild(document.createTextNode(text.slice(lastIndex)));
    textNode.parentNode.replaceChild(frag, textNode);
  }
  return firstMark;
}
