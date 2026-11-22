# Narrative architecture: Colah + annotated implementation

## The two complementary teaching moves

**Colah-style:** Start with a cognitive tension that the reader can feel, show a simple whole-network diagram, then unroll/focus/highlight a single reusable module in successive steps. Move from a concrete example to the architecture and only then formalize. Use color continuity and short figure captions. Avoid showing an entire graph with every arrow before the question exists.

**Annotated-Transformer-style:** Reorganize the paper into computational dependencies. Explain a code unit alongside the corresponding architecture component, then test on a tiny synthetic example, then explain real-world training/results. The implementation is evidence about shape/control flow; it is not proof of reported benchmarks.

## Required story beats

1. **Opening paradox**: one domain-specific question, no marketing claim.
2. **Baseline system**: current method and exactly where it fails; distinguish optimization, expressivity and generalization.
3. **Core conceptual shift**: one reusable idea in a single sentence + one top-level figure.
4. **Local unit**: show a minimal block/operation, then explain every connector and tensor.
5. **Stepwise walkthrough**: 2–5 diagram states, label what changes at each step.
6. **Equation with map**: each symbol points back to a named diagram part; add dimensions and normalization axis.
7. **Composition**: build the full architecture from that block; identify variants separately.
8. **Minimal experiment**: runnable, tested shapes/values, no false “production ready” claims.
9. **Paper evidence**: explicit dataset, split, metric, model, table/figure; report what comparisons actually show.
10. **Failure modes and boundaries**: edge cases, implementation pitfalls, what the study did not demonstrate.
11. **Synthesis**: compress to a few correct mental models and link primary references.

## Figure storyboard (example)

| Sequence | Question | Visual | Learner action |
|---|---|---|---|
| 1 | Why does the old path struggle? | baseline path vs new path | compare dependencies |
| 2 | What is the minimal unit? | single block | identify input and output |
| 3 | Where does information go? | highlighted flow | choose a source token / branch |
| 4 | How is it computed? | matrix/shape trace | select equation stage |
| 5 | How does it scale? | stacked architecture | inspect stage counts |
| 6 | Does evidence support it? | cited plot/table | inspect controls and limitations |

**Rule:** Write a caption and scientific assertion for every figure before drawing it. If a figure contributes no new explanatory content, remove it.
