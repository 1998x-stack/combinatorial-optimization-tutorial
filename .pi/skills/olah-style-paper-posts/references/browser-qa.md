# Browser QA protocol

Use actual Chromium/Playwright; HTML parsing alone is insufficient. Save a machine-readable report and captures.

## Smoke checklist

| View | Check |
|---|---|
| Desktop 1440×900 | No unexpected horizontal overflow; heading, figure and sidebar readable |
| Tablet 768×1024 | TOC/body not overlapping |
| Mobile 390×844 | No horizontal document overflow; text size and controls legible |
| Narrow mobile 360×800 | Same plus no clipped diagram labels |
| Print emulation | No blank critical figures; sensible page breaks |
| Network disabled | Local article content renders; no remote CSS/JS/font dependency |

## Technical checks

- Collect `pageerror`, console errors and request failures; distinguish expected offline aborts from a truly passing result.
- Each `<figure>` contains SVG/image plus nonempty figcaption; inline SVG has meaningful title/role/label.
- Check anchor targets, image loads and SVGs with nonzero dimensions.
- For MathML posts, verify valid MathML namespace, no math nested within SVG, nonzero formula dimensions, numerator above denominator for fractions, accessible math descriptions and responsive equation-region scrolling (including keyboard). See [math-typesetting.md](math-typesetting.md). Do not call DOM presence alone a rendering check.
- Tab through controls; verify visible focus and accessible names.
- Click each article's declared demo selector (if present) and assert a meaningful DOM/text change; inspect JS exception log.
- Take screenshot on each viewport and at least one representative dense figure. Report skip if any test could not execute.

Command:

```bash
python skills/olah-style-paper-posts/scripts/browser_check.py examples/transformer/index.html --output reports/transformer
```

A failing automated check must be repaired **or transparently flagged**, not bypassed by making the rule weaker. The final completion message should say which browser sizes and interactions were verified.
