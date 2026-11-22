# Math typesetting and verification standard

A mathematical expression is a computational claim, not visual decoration. Write **mathematical truth** first, then represent it with accessible, portable mathematical markup. This applies to SVM, attention, normalization, optimizers, GPU cost models and every future paper explainer.

## Rendering decision

1. **Default: native MathML Core** in HTML, fully offline with zero CDN, remote font or JavaScript dependencies. Use semantic math elements and the browser's native math layout for roots, fractions, operators, limits, matrices and scripts. In modern evergreen Chromium, Safari and Firefox, inspect the *actual output*. Do not assume support from an HTML parser alone.
2. **Fallback only for a demonstrated compatibility gap:** bundle a pinned licensed build of KaTeX or an equivalent renderer and its fonts locally (never fetch from a CDN). Commit license notices, an offline/network-blocked smoke test, and a static or prerendered fallback usable without JavaScript. The fallback must not duplicate, conceal or reorder the underlying mathematical claim.
3. Do **not** emulate a long equation with a styled Unicode string: `Σᵢ`, `||w||²`, `½` and `→` do not provide stacked fractions, operators with limits, robust wrapping or mathematical semantics. Short conventional symbols in ordinary prose are fine; substantive equations require actual markup.
4. Keep canonical source equations in a human-auditable form (LaTeX notation in research notes or MathML in authored HTML), with paper locators and a brief explanation of every symbol. Avoid blind regular-expression replacements across an HTML document, especially across inline `<svg><text>` labels or code blocks.

## MathML Core markup contract

- Inline equations: `<math class="math-inline" aria-label="...">...</math>`.
- Display equations: `<math display="block" aria-label="...">...</math>` within a named, keyboard-focusable scrolling region. The region must be `tabindex="0"`, have an accessible name, and have `overflow-x:auto`; the **page itself** must not overflow.
- Use `<mi>` for identifiers, `<mn>` for numbers, `<mo>` for operators, `<mtext>` for text, `<mrow>` for groups, `<mfrac>` for fractions, `<msub>`/`<msup>`/`<msubsup>` for scripts, and `<munder>`/`<munderover>` for limits. Matrix rows use `<mtable><mtr><mtd>...</mtd></mtr></mtable>`.
- A fraction must have **exactly two** element children; `munder` exactly two, `munderover` exactly three. Do not replace a meaningful operator limit with Unicode subscript.
- Use `xmlns="http://www.w3.org/1998/Math/MathML"` when serializing standalone XML/XHTML; HTML5 math elements inserted by the HTML parser are automatically placed in the MathML namespace **unless nested inside SVG**.
- All math should have a human-readable accessible description using `aria-label` or `aria-labelledby` (prefer an accurate statement over a raw symbol-by-symbol list). Number significant display equations and separate constraints from the objective, without splitting their mathematical dependence.
- Do not mix `<math>` into `<svg><text>`. SVG text is an SVG context; MathML markup inserted there can have the wrong namespace and cause missing graphics. If a diagram needs a mathematical label, use compact plain SVG text or separately positioned HTML MathML; validate SVG text and standalone exports.
- Keep equations outside `<pre><code>` and escaped examples. Do not duplicate live MathML in hidden fallback content without explicit accessibility control.

## Minimal correct example

```html
<p>预测得分是 <math class="math-inline" aria-label="w 转置乘 x 加 b">
  <mrow><msup><mi>w</mi><mo>⊤</mo></msup><mi>x</mi><mo>+</mo><mi>b</mi></mrow>
</math>。</p>
<div class="math-equation" role="group" aria-label="点到决策边界的距离">
  <div class="math-scroll" data-math-scroll tabindex="0" role="region" aria-label="距离公式，可横向滚动">
    <math display="block" aria-label="绝对值 w 转置乘 x 加 b 除以 w 的二范数">
      <mfrac>
        <mrow><mo>|</mo><msup><mi>w</mi><mo>⊤</mo></msup><mi>x</mi><mo>+</mo><mi>b</mi><mo>|</mo></mrow>
        <msub><mrow><mo>‖</mo><mi>w</mi><mo>‖</mo></mrow><mn>2</mn></msub>
      </mfrac>
    </math>
  </div>
</div>
```

```css
.math-inline{font-family:"Cambria Math","STIX Two Math","Latin Modern Math",serif}
.math-equation{max-width:100%;min-width:0}
.math-scroll{max-width:100%;min-width:0;overflow-x:auto;overflow-y:hidden}
.math-scroll:focus-visible{outline:3px solid #147f80;outline-offset:2px}
.math-scroll math[display="block"]{width:max-content;min-width:100%;font-size:1.2rem}
@media print{.math-scroll{overflow:visible}.math-scroll math[display="block"]{font-size:1rem}}
```

An HTML5 parser should create MathML-namespace elements. On mobile widths, the scrolling region has no missing terms and horizontal scrolling is usable by touch **and keyboard**. Avoid `overflow-x:hidden` on the entire document, which conceals bugs.

## QA evidence

1. **Static**: no MathML nested inside SVG; all math has accessible text; `mfrac` arity is two; no malformed empty equation; clear number/constraint structure.
2. **Browser at 1440, 768, 390, 360 px**: check `namespaceURI === "http://www.w3.org/1998/Math/MathML"`, visible nonzero geometry, numerator positioned above denominator, correct operator script placement, no document horizontal overflow, and internal scrolling where needed.
3. **Interaction**: focus the wide formula region, press ArrowRight, assert `scrollLeft` changes (only if content actually overflows). Check that no MathML enters SVG text and standalone SVG export remains readable.
4. **Print / offline**: capture print emulation, disable network requests, and make sure the formula remains readable without JavaScript.
5. **Evidence**: compare the rendered equation and algebra to the primary source: signs, indices, axes, reduction operation, normalization, assumptions, optimizer constraints and variant scope. A visually correct formula can still be mathematically wrong.

Record checks as `passed`, `failed` or `not verified`. Do not claim cross-browser compatibility unless those browsers were actually tested. Existing legacy posts need not be rewritten in unrelated PRs; new math-heavy posts must comply.
