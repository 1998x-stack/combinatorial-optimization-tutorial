# SVG pipeline: storyboard → design → extract → render → verify

## Construct

1. Make a state/edge list (e.g. input → projection Q/K/V → score → softmax → values) **before** drawing.
2. Draw shapes in model execution order; separate arrows for data flow from labels for tensors. Use `stroke-dasharray` only for an explicitly described secondary/gradient path.
3. For stacked architecture, distinguish repeated blocks and stage count; for masked attention show which entries are blocked, not just a colored matrix.
4. Each SVG must have `xmlns`, `viewBox`, `<title>`, `<desc>` and unique IDs; use `role="img" aria-labelledby` when inline.
5. Minimum label ~13px at nominal width; use native sans fonts with Chinese fallbacks. Treat color as redundant with labels/dashes.
6. Use color semantics consistently **within** a paper; do not claim identical colors across very different scientific domains.
7. Captions should describe a verifiable statement about the path, not simply 'architecture overview'.

## Extraction

Run `extract_svg.py` against **rendered HTML** with Playwright. It clones each SVG, snapshots visible CSS computed style fields (fill, stroke, font, opacity, etc.) onto the SVG elements, ensures `xmlns/viewBox`, cleans unsafe script/event attributes, and writes independent XML files. This retains labels that were previously styled only via article CSS. It does not download external assets; CSS background images and remote font dependencies must be eliminated upstream. Names prefer `<svg data-export="filename">`, otherwise stable section/figure ID.

```bash
python skills/olah-style-paper-posts/scripts/extract_svg.py examples/resnet/index.html --out /tmp/resnet-svg
```

## Verify

- Parse as XML, confirm width/height from viewBox, no missing assets, and unique IDs.
- Open standalone SVG in a browser and capture screenshot; compare to the inline figure (cropping might differ because CSS dimensions differ).
- Inspect all lines and arrows visually: joins, topology, direction, equation symbols and labels; no visible overprint/clipping.
- Maintain a manifest mapping filename → figure number → concept → source verification.
- Do not blindly scrape or publish third-party paper SVGs: check license and permission first.

## Two anti-patterns

- Arrows that merely decorate a box: no scientific connection to described operation.
- “Perfect-looking” shapes with wrong semantics (e.g. residual skip starting after the transform, or cross-attention K/V originating in Decoder).
