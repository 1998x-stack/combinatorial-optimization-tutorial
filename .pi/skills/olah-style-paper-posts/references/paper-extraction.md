# Decompose a paper without losing its experimental meaning

1. **Provenance:** title, authors, release date, paper version/DOI/arXiv and official code (if any). Distinguish updated arXiv versions from original publication.
2. **Problem:** What behavior was inadequate? State the exact objective and whether evidence is empirical/theoretical/qualitative.
3. **Model graph:** input, output, repeated units, branch joins, normalization, skip paths, positional information, tensor dimensions, train/inference graph.
4. **Algorithm:** equations in causal order, variable glossary, axes, numerical assumptions, masks, initialization and losses.
5. **Comparators:** baselines, controlled variables, dataset splits, training compute and differing configurations.
6. **Tables:** for every number retain table label and column name; never compare Top-1 to Top-5, error to accuracy, or validation to test.
7. **Ablations:** identify which change was isolated and which variables confound the conclusion.
8. **Limitations:** model size, quadratic costs, data regime, evaluation bias, omitted details, historical vs modern practice.
9. **Modern extensions:** separate section with citations and explicit dates rather than silently “updating” the historical model.

## Mechanism record template

```yaml
name: causal self-attention
source: "Vaswani et al. 2017, Section 3.2"
input: "Q: [B,H,Tq,Dk]; K: [B,H,Tk,Dk]; V: [B,H,Tk,Dv]"
output: "[B,H,Tq,Dv]"
equation: "softmax((Q K^T / sqrt(Dk)) + mask) V"
axis: "softmax over Tk"
assumption: "masked positions have -infinity score; each query has at least one valid key"
not_in_paper: "KV-cache details are later engineering practice"
verification: "shape test + future-token masking test"
```
