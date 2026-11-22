# Executable teaching and interactive controls

## Code

- Smallest executable unit first (e.g. residual block or masked attention); validate dimensions and numerical invariants.
- Pin required dependencies, versions, device assumptions and random seed. Keep runtime local-friendly.
- Distinguish a **toy example**, a **paper-faithful block** and a **reproduction of a benchmark**. Only the latter requires training config, dataset, seeds and repeated runs.
- For attention: correct Q/K/V projection origin, mask semantics (`True=allowed` or `True=blocked`, never ambiguous), softmax along keys, shape of multi-head output, all-masked-row treatment.
- For residual blocks: distinguish pre-/post-activation, downsampling/projected shortcut, channel matching and activation locations.

## Interactivity

- Controls have `<button type="button">` or properly associated `<label>`; pressed/selected states update `aria-pressed` or equivalent.
- Provide default static SVG explaining the concept before JS runs; widget must not be the only way to understand the paper.
- Each interaction answers one named question (e.g. 'Which earlier tokens can this token see?').
- No autoplay, flashing, unexplained canvas black boxes, analytics or network dependency.
- Assert that changing control changes a non-decorative output and does not break screen-reader status (`aria-live="polite"`).
