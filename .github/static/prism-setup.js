/**
 * Prism configuration for the blog.
 *
 * - Normalizes fenced-code language names to Prism language IDs before the
 *   autoloader starts (pymdownx emits `<code class="language-xxx">`).
 * - Registers placeholder grammars for languages that Prism does not ship,
 *   so the autoloader does not request missing components.
 * - Renders the language label shown in the top-left corner of code blocks.
 *
 * Load this file after prism.min.js (and prism-typst.js) but before
 * prism-autoloader.min.js.
 */
(function () {
  if (typeof Prism === 'undefined' || typeof document === 'undefined') {
    return;
  }

  // Languages without a Prism grammar: keep the code readable, just unhighlighted.
  Prism.languages.plaintext = Prism.languages.plaintext || {};
  Prism.languages.txt = Prism.languages.plaintext;
  Prism.languages.text = Prism.languages.plaintext;

  var LANGUAGE_ALIASES = {
    ps1: 'powershell',
    ps: 'powershell',
    pwsh: 'powershell',
    typ: 'typst',
    txt: 'plaintext',
    text: 'plaintext',
    plain: 'plaintext',
    iframe: 'markup',
    modelfile: 'dockerfile'
  };

  var LANGUAGE_LABELS = {
    typst: 'Typst',
    typ: 'Typst',
    powershell: 'PowerShell',
    ps1: 'PowerShell',
    ps: 'PowerShell',
    pwsh: 'PowerShell',
    python: 'Python',
    markup: 'HTML',
    iframe: 'HTML',
    modelfile: 'Modelfile',
    plaintext: 'Text',
    plain: 'Text',
    javascript: 'JavaScript',
    js: 'JavaScript',
    typescript: 'TypeScript',
    ts: 'TypeScript',
    markdown: 'Markdown',
    md: 'Markdown',
    bash: 'Bash',
    sh: 'Shell',
    shell: 'Shell',
    zsh: 'Zsh',
    fish: 'Fish',
    json: 'JSON',
    yaml: 'YAML',
    yml: 'YAML',
    toml: 'TOML',
    ini: 'INI',
    vim: 'Vim',
    git: 'Git',
    dockerfile: 'Dockerfile',
    docker: 'Docker',
    html: 'HTML',
    xml: 'XML',
    css: 'CSS',
    scss: 'SCSS',
    sass: 'Sass',
    sql: 'SQL',
    graphql: 'GraphQL',
    rust: 'Rust',
    rs: 'Rust',
    go: 'Go',
    c: 'C',
    cpp: 'C++',
    csharp: 'C#',
    cs: 'C#',
    java: 'Java',
    kotlin: 'Kotlin',
    swift: 'Swift',
    lua: 'Lua',
    php: 'PHP',
    ruby: 'Ruby',
    rb: 'Ruby',
    r: 'R',
    latex: 'LaTeX',
    tex: 'TeX',
    nginx: 'Nginx',
    plaintext: 'Text',
    text: 'Text'
  };

  var LANGUAGE_CLASS_RE = /\blang(?:uage)?-([\w-]+)\b/;

  function languageOf(element) {
    var match = LANGUAGE_CLASS_RE.exec(element.className || '');
    return match ? match[1].toLowerCase() : null;
  }

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function renameLanguage(element, from, to) {
    var pattern = new RegExp('\\b(lang(?:uage)?-)' + escapeRegExp(from) + '\\b', 'gi');
    element.className = element.className.replace(pattern, '$1' + to);
  }

  function normalize(element) {
    var language = languageOf(element);
    if (!language) {
      return null;
    }
    var mapped = LANGUAGE_ALIASES[language] || language;
    if (mapped !== language) {
      renameLanguage(element, language, mapped);
    }
    return mapped;
  }

  function addLabel(pre) {
    var code = pre.querySelector('code');
    var host = (code && languageOf(code)) ? code : (languageOf(pre) ? pre : null);
    if (!host) {
      return;
    }
    var original = languageOf(host);
    var language = normalize(host);
    pre.setAttribute(
      'data-language',
      LANGUAGE_LABELS[original] || LANGUAGE_LABELS[language] || language.toUpperCase()
    );
  }

  function prepareCodeBlocks() {
    var blocks = document.querySelectorAll('pre');
    Array.prototype.forEach.call(blocks, addLabel);
  }

  // Deferred scripts run after the document has been parsed, so the DOM is ready.
  // Normalizing here guarantees the autoloader sees canonical language names.
  prepareCodeBlocks();

  // Also handle content inserted after load (e.g. future dynamic rendering).
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', prepareCodeBlocks);
  }
})();
