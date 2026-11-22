# Evidence and attribution standard

## Mandatory evidence ledger

One `evidence.json` per article; each factual or quantitative anchor has `id`, `claim`, `kind`, `source_url`, `locator`, `status`, `notes`. `status` is `verified`, `derived`, `illustrative`, or `unverified`. Never imply verification from a broken source. Cite primary papers for historical results, not unsourced blog recaps. Explicitly separate author claims, independent inference and toy examples.

## Metrics checklist

Every reported metric needs: model, dataset/benchmark, split, exact metric and direction, numeric value, source/table, and controlled comparison context. Avoid cherry-picked benchmark outcomes. Recompute derived percentage differences separately and label them derived.

## Code and diagram licenses

Illustrate ideas with your own SVG geometry and prose. Link Colah and The Annotated Transformer for attribution of **pedagogical approach**; do not import their image files, diagrams, logos, paragraphs, code blocks or stylesheet without license review and required notices. Published scientific equations and architecture concepts can be explained in independent language. For third-party visual assets, record author, license, URL, modification and required attribution in a manifest before use.

## Citation placement

- Cite nearest to the claim, including figure/table number where available.
- Link the official paper at first substantial mention and in closing references.
- For implementation-specific claims, cite the implementation and commit/version.
- Unsupported recent claims must be omitted or flagged with retrieval limits.
