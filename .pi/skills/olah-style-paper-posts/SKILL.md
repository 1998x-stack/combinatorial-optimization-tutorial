---
name: olah-style-paper-posts
description: Turn a scientific/ML paper into an evidence-grounded, illustrated, responsive, interactive long-form HTML explanation, pairing Colah-style progressive disclosure with Annotated-Transformer-style runnable code. Use for paper explainers, model architecture deep-dives, and reproducible technical teaching posts.
---

# Olah-style Paper Posts

Create **a correct explanation first**, then a visually elegant post. The goal is an independently useful article, not a slide deck, template showcase, or sales landing page. This skill takes inspiration from Christopher Olah's *Understanding LSTM Networks* and the Harvard NLP *Annotated Transformer*; do not copy their diagrams, prose, branding, or code wholesale.

## When to use

- User gives a paper, arXiv ID, model, or several papers to explain with narrative, SVG, equations and reproducible code.
- User asks to refresh an existing technical HTML article without losing pedagogical correctness.
- Do **not** use just to redesign a generic corporate site.

## Inputs and outputs

**Inputs:** paper title/URL/PDF, topic, audience, language, depth, optional reference article, desired runtime (e.g. PyTorch), output path, optional publication destination. Missing preferences default to Chinese, deep technical audience, offline-first HTML, no third-party JS.

**Outputs:** `index.html`, `assets/*.svg`, `evidence.json` (claims mapped to sources), executable example and tests when appropriate, browser screenshots/check report, a short factual completion summary. Deliver files or repository paths and disclose any missing tests. Keep explanatory prose in article; put production notes in README and reports **not** in article header/footer.

## Workflow (mandatory, ordered gates)

### Gate 0 — Inspect sources, examples, assets
1. Read primary paper thoroughly including appendix, figure captions, method and ablation tables; identify versions.
2. Read a high-quality implementation or official code if needed, but distinguish it from the original paper.
3. Review `references/source-notes.md` and `examples/resnet/` + `examples/transformer/` for form and depth, **not wording to replicate**.
4. Assemble a claims/evidence ledger before writing. Unverified metrics remain omitted or explicitly uncertain.

### Gate 1 — Plan the causal learning path
Produce a private article map: `reader misconception → concrete problem → minimum diagram → mechanism → equation with shape → runnable experiment → evidence → limitations`. Read [narrative-architecture.md](references/narrative-architecture.md) and [paper-extraction.md](references/paper-extraction.md).

Write a diagram storyboard with one question per figure, 2–5 progressive states for complex mechanisms, consistent color meaning and explicit tensor shapes. Readers must be able to understand the figure caption without hovering.

### Gate 2 — Draft technical truth before illustrations
For each mechanism, record: inputs and shapes, transformation, outputs, precise equation, masking/normalization conventions, train-vs-infer differences and version scope. Keep a traceable LaTeX/MathML expression, confirm indices, operator limits and assumptions against the paper; a formula that looks attractive but differs algebraically is a failure. In text, separate **paper claim**, **intuition**, **toy demo**, **modern variant**, **engineering choice**, **open issue**. Cross-check all reported results against the source (table/section/figure and version), see [evidence-and-citation.md](references/evidence-and-citation.md).

### Gate 3 — Implement semantic HTML + CSS
Start with `assets/templates/article.html` and `assets/css/article.css`. For math-heavy posts, first follow [math-typesetting.md](references/math-typesetting.md): native offline MathML Core, real fractions/scripts/limits, numbered display equations, accessible inline math, internal keyboard-scrollable formula areas and no MathML inside SVG. Follow [html-design-system.md](references/html-design-system.md): semantic `<main><article>`, navigable `nav`, one H1, ordered H2, native buttons/controls, visible focus, mobile/print/reduced-motion CSS. Inline external assets in a release export only when needed. Do not auto-inject build-system notes or conspicuous format claims into the article.

### Gate 4 — Draw SVG, extract, render and compare
Use standalone SVG with `viewBox`, `<title>`, accessible description and unique IDs. Follow [svg-production.md](references/svg-production.md). Preserve semantic color identities; use font-safe Chinese/English labels, avoid illegible nodes. The diagram's topology must match model computation, not merely look plausible.

If SVGs are embedded inline, run `python skills/olah-style-paper-posts/scripts/extract_svg.py path/to/index.html --out path/to/assets/` to extract browser-computed, standalone figures. Re-open each SVG independently, render it, and compare with inline appearance. Keep naming stable.

### Gate 5 — Make claims executable
Include small deterministic code, shape/mask tests and the exact dependencies; do not label a minimal cell as a complete model. Interactive figures must have meaningful default states, accessible controls and deterministic assertions. See [implementation-and-interactivity.md](references/implementation-and-interactivity.md).

### Gate 6 — Validate and inspect the browser
Run:

```bash
python skills/olah-style-paper-posts/scripts/validate.py examples/resnet/index.html
python skills/olah-style-paper-posts/scripts/browser_check.py examples/resnet/index.html --output reports/resnet
python skills/olah-style-paper-posts/scripts/browser_check.py examples/transformer/index.html --output reports/transformer
python -m pytest -q
```

Install tooling first (`pip install -r requirements-dev.txt && python -m playwright install chromium`). Browser QA must inspect 1440px desktop, 390px/360px mobile, screenshot, scroll overflow, JavaScript errors, broken images/links, SVG render, keyboard focus and at least one live interaction per article. Report skips as **not verified**, never as passing. For articles containing MathML, also inspect namespace, nonzero geometry, stacked fractions, no SVG-nested math and mobile formula scrolling as documented in [math-typesetting.md](references/math-typesetting.md). See [browser-qa.md](references/browser-qa.md) and [scorecard.md](references/scorecard.md).

### Gate 7 — Package, publish, verify
Remove creation-process metadata, preserve source citations, and record the final HTML/SVG/code filenames. When publishing, use a branch/PR or approved target branch, run CI, inspect diff, then verify remote files/merge status. Do not claim a GitHub Pages site is live before checking it. See [publishing.md](references/publishing.md).

## Hard constraints

- Never fabricate results, metrics, reference links, training behavior, paper figures, tensor shapes or browser test status.
- Never copy Colah's diagram assets or text; use independently drafted illustrations; attribute stylistic inspiration in project docs.
- Never confuse the original architecture with later variants (e.g. Transformer post-LN vs pre-LN; ResNet v1 vs v2).
- Keep all diagrams interpretable without JavaScript. Interactivity is progressive enhancement.
- Never fake complex mathematical typesetting with Unicode-only strings or rely on CDN math scripts; treat mathematical semantics, offline rendering, accessible labels and mobile overflow as quality gates.
- In final article, do not render these production notes (nor close paraphrases):
  - `原创图解 · 单文件离线 HTML · SVG 矢量图 · 页面适配手机阅读与浏览器打印。文章中的教学简化已单独注明，历史实验指标均标注来源。`
  - `用直觉 → 图示 → 数学 → 工程实现，理解残差网络 · 参考 Colah 风格，非原文翻译`
- In general never add footnotes about file format, toolchain, being AI-generated, CSS/SVG, or “reference style” to the finished article. Technical caveats and actual citations **are** article content.

## Reference routing (read only what you need)

| Need | File |
|---|---|
| Storytelling and figure sequence | `references/narrative-architecture.md` |
| Paper decomposition | `references/paper-extraction.md` |
| Claims, experiments and license | `references/evidence-and-citation.md` |
| Semantic HTML / exact CSS tokens | `references/html-design-system.md` |
| Mathematical formula markup, offline rendering and QA | `references/math-typesetting.md` |
| SVG design, extraction and render checks | `references/svg-production.md` |
| Executable code and widgets | `references/implementation-and-interactivity.md` |
| Playwright browser protocol | `references/browser-qa.md` |
| Scoring and release gate | `references/scorecard.md` |
| Inspiration sources and comparison | `references/source-notes.md` |
| Release/PR/Pages | `references/publishing.md` |

## Working example invocation

```text
Use olah-style-paper-posts on Attention Is All You Need. Explain why recurrence was replaced, animate Q/K/V and masking, walk through the 2017 encoder-decoder model, reproduce a minimal attention function with PyTorch tests, keep all illustrations as original SVG, and hand back HTML + standalone SVG + evidence ledger + browser QA report.
```
