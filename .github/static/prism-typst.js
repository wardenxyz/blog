/**
 * Minimal Prism grammar for Typst markup and code.
 * Prism does not ship a Typst grammar, so this file provides one locally.
 * Load it after prism.min.js and before the autoloader.
 */
(function (Prism) {
  if (typeof Prism === 'undefined') {
    return;
  }

  var typst = {
    'comment': [
      {
        pattern: /\/\/[^\n\r]*/,
        greedy: true
      },
      {
        pattern: /\/\*[\s\S]*?\*\//,
        greedy: true
      }
    ],
    // Raw text: ```...``` and `...`
    'raw': [
      {
        pattern: /```[\s\S]*?```/,
        greedy: true,
        alias: 'string'
      },
      {
        pattern: /`[^`\n\r]*`/,
        greedy: true,
        alias: 'string'
      }
    ],
    'string': {
      pattern: /"(?:\\[\s\S]|[^"\\])*"/,
      greedy: true,
      inside: {
        'escape': /\\(?:u\{[0-9a-fA-F]+\}|.)/
      }
    },
    'heading': {
      pattern: /^=+[ \t].*$/m,
      greedy: true,
      alias: 'title'
    },
    // Markup label: <intro>  /  reference: @intro
    'label': {
      pattern: /<[\w.:-]+>/,
      alias: 'symbol'
    },
    'reference': {
      pattern: /@[\w.:-]+/,
      alias: 'symbol'
    },
    // Inline math: $ ... $
    'math': {
      pattern: /\$(?:\\[\s\S]|[^$\\])+\$/,
      greedy: true
    },
    // Hex colors such as #ff0000 / #ff000080
    'color': {
      pattern: /(^|[^\w#])#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?\b/,
      lookbehind: true
    },
    'keyword': /\b(?:as|auto|break|context|continue|else|for|if|import|include|in|let|none|return|set|show|while)\b/,
    'boolean': /\b(?:true|false)\b/,
    'number': /\b\d+(?:\.\d+)?(?:pt|mm|cm|in|em|fr|deg|rad|s|%)?/,
    // Function calls and built-in names: text(...), #set page(...)
    'function': /\b[a-zA-Z_][\w-]*(?=\s*\()/,
    'operator': /==|!=|<=|>=|=>|\.\.|\+=|-=|\*=|\/=|\+|-|\*|\/|=(?!=)|<(?!=)|>(?!=)|\band\b|\bor\b|\bnot\b/,
    'punctuation': /[{}[\];(),.:#]/
  };

  Prism.languages.typst = typst;
  Prism.languages.typ = typst;
})(Prism);
