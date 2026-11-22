# Publishing and release checklist

1. Start from repository default branch; preserve existing content and branch protection.
2. Create a topic branch with files organized under `skills/`, `examples/`, `tests/`, and `.github/`.
3. Commit only source HTML, SVG, Python and docs; omit screenshots or caches unless deliberately documented.
4. Run static test + Playwright, inspect 1440/390/360 px, print mode and interactive controls; create `reports/` only as CI artifact if useful.
5. Open PR, check changed paths, status and mergeability; merge only after checks pass or with an honest manual acceptance when checks are not configured. Then fetch the default-branch `SKILL.md` and README to verify the release.
6. GitHub Pages is a separate deployment feature; a workflow file alone does not establish a live website. If deployment isn't configured, state 'Pages ready' instead of 'Pages live'.
7. ZIP includes the exact source tree and reproducible usage, excluding `.git/`, `__pycache__/`, virtualenvs and temporary browser screenshots.
