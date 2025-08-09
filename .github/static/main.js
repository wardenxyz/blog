(function(){
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
        target.scrollIntoView({behavior:'smooth', block:'start'});
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
    });
    // Close on resize to desktop
    mq.addEventListener('change', e=>{ if(!e.matches) closeMenu(); });
    // Close when clicking a link (for single page feel)
    nav.addEventListener('click', e=>{ if(e.target.closest('a')) closeMenu(); });
  }

  // Collapsible TOC on mobile
  function initCollapsibleToc(){
    const toc = document.getElementById('toc');
    if(!toc) return;
    const title = toc.querySelector('.toc-title');
    if(!title) return;
  const mq = window.matchMedia('(max-width: 959px)');
    function ensureCollapsed(){ if(mq.matches) toc.classList.add('collapsed'); else toc.classList.remove('collapsed'); }
    ensureCollapsed();
    mq.addEventListener('change', ensureCollapsed);
    title.addEventListener('click', ()=>{
      if(!mq.matches) return;
      toc.classList.toggle('collapsed');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ()=>{
      initMenuToggle();
      initCollapsibleToc();
    });
  } else {
    initMenuToggle();
    initCollapsibleToc();
  }
})();
