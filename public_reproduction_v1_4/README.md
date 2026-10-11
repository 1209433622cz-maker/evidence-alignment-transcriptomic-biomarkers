# v1.4 aggregate figure and supplementary-table reproduction

This directory is self-contained for **aggregate figure/table reconstruction**, not participant-level Cox/logistic refitting or Word rendering. Its eleven inputs retain the exact frozen hashes checked by the plotting recipe. Original scientific labels and unknown population identities are not edited by the recipes.

From the repository root, after installing `requirements.txt` in a working environment:

```bash
python public_reproduction_v1_4/scripts/build_v4_s8_figures.py
python public_reproduction_v1_4/scripts/prepare_supplementary_csv.py
```

The first command writes four SVG/PDF/PNG figures, derived tables and a build audit to `public_reproduction_v1_4/figure_regeneration_workspace/`. The second writes three CSVs to `public_reproduction_v1_4/supplementary_csv/` and checks parsed-field equivalence to `tables/`. Use a disposable clone/working copy: these are regenerated artifacts, not an automatic replacement of the public frozen payload. Current promoted figures remain in the repository-level `figures/` and current CSVs in `supplementary_csv/`.

The four current figures have 3, 1, 4 and 3 panels. Reproduction neither fills reserved Figures 6–8 nor restores randomized inference for TRIO Arm 3. A successful build is not full-page WPS QA, an author declaration or submission permission.

`.gitattributes` pins normal text to LF and marks the eleven frozen input files byte-preserved (`-text -eol`), because their historical raw-byte contract includes mixed line endings. A fresh clone is recommended after updating from a pre-attribute checkout; do not weaken the plotting hash guard or hand-edit data to bypass it. The standard-library validator checks these eleven raw hashes without importing plotting libraries.
