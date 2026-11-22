# HTML / CSS design contract (v1)

The article is a book chapter, **not** a software landing page. Prefer generous whitespace, narrow readable text, visible source links, a left table of contents on desktop, and diagrams occupying the main column. Readers must understand the content without animation.

## Semantic HTML

```html
<body>
  <a class="skip-link" href="#content">跳转至正文</a>
  <div class="layout">
    <nav class="toc" aria-label="文章目录">...</nav>
    <main id="content"><article>
      <header class="article-header"><h1>Understanding ...</h1><p class="dek">...</p></header>
      <section id="problem" aria-labelledby="problem-heading"><h2 id="problem-heading">...</h2>
        <p>...</p>
        <figure><svg role="img" aria-labelledby="fig-a-title fig-a-desc" viewBox="0 0 800 320">...</svg>
          <figcaption>...</figcaption></figure>
      </section>
      <section id="references" ...>...</section>
    </article></main>
  </div>
</body>
```

- One H1 per page; H2/H3 hierarchy reflects a learning sequence.
- Cite primary sources in article text; references have human-readable link text.
- Do not surface internal work notes, article format, vector claims, LLM tools, production credits, tests, or generator labels in hero/byline/footer.
- Figures have meaningful SVG `<title>`, `<desc>`, `role="img"`/labels, and figcaption.
- Interactive controls are native and keyboard operable, with focus-visible and live state changes.

## Mathematical typesetting

For any substantial formula, read [math-typesetting.md](math-typesetting.md). Prefer native MathML with real `mfrac`, `msub`, `munderover` and accessible labels, rather than Unicode-only faux equations. Wrap long display math in a named `tabindex="0"` region with `overflow-x:auto` and keep the equation visible under print emulation. MathML must stay outside SVG `<text>` to preserve the SVG namespace and standalone exports.

## Typography, spacing and width

| Token | Default | Reason |
|---|---|---|
| `--paper` | `#fffdf9` | Warm reading surface |
| `--ink` | `#203035` | Comfortable high-contrast body text |
| `--subtle` | `#53676d` | Annotations, not essential data |
| `--accent` | `#147f80` | Conceptual signal/path |
| `--transform` | `#d06d4d` | Learned transform / computation |
| `--structure` | `#7461ba` | Secondary route / memory |
| `--annotation` | `#916c22` | Auxiliary annotation |
| Body | 17px, line-height 1.85 | Long Chinese technical articles |
| Body column | max-width 820px | Figure/text readable |
| Figure width | 100% and viewBox | Responsive |
| Sidebar | 210px sticky | Locate sections |
| Major section margin | 4.25rem | Segmented progression |
| Focus outline | 3px solid `--accent` | Keyboard navigation |

## Responsive and print

- At <=900px: stack sidebar above article; TOC collapses to details or horizontal nav.
- At <=480px: page padding >=16px; heading with `clamp`, SVG viewBox preserved; horizontal scroll only **inside** explicit wide-code or math containers.
- At 360px and 390px viewport: `document.documentElement.scrollWidth <= innerWidth`; avoid tiny text in SVG; if graph is too dense, provide a simplified mobile figure or per-stage breakdown.
- `@media (prefers-reduced-motion: reduce)`: disable transitions and auto-scroll.
- `@media print`: remove interactive controls and sticky nav; ensure no clipped important figures, readable links and print-friendly contrast.

## CSS ownership and export

- Canonical style in `assets/css/article.css`, no externally hosted fonts or CSS required.
- Build may inline CSS for truly standalone offline HTML, but source remains readable and separate.
- SVG itself may carry its own fill/stroke/font attributes; extraction should embed **computed** styles when dependent on page CSS.
- `box-sizing:border-box`, accessible `:focus-visible`, `overflow-wrap:anywhere` for long URLs, avoid `overflow-x:hidden` as a substitute for fixing overflow.

## Banned process prose

**Never** add these or close paraphrases to article output: `原创图解 · 单文件离线 HTML`, `用直觉 → 图示 → 数学 → 工程实现，理解残差网络 · 参考 Colah 风格，非原文翻译`. These are format descriptors, not scientific explanation. An automated check enforces both exact stems.
