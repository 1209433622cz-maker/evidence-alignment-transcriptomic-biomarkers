# Evidence alignment of transcriptomic biomarker claims in oncology

[![Validate public release](https://github.com/1209433622cz-maker/evidence-alignment-transcriptomic-biomarkers/actions/workflows/validate.yml/badge.svg)](https://github.com/1209433622cz-maker/evidence-alignment-transcriptomic-biomarkers/actions/workflows/validate.yml)

**Current: RPv4 · manuscript v1.5 AUTHOR_REVIEW · four main figures + three supplementary figures · submission HOLD.**

本库按本地整理结果重构为编号目录，公开经过筛选的汇总证据、代码、稿件及工作记录；它不是整个私有工作区的镜像。最新v1.5作者审阅稿已插入对应图片与图注。旧v1.4及此前分析完整保留在版本归档中，不覆盖，也不恢复已被更正的临床解释。

## Scientific purpose

> A computationally reproducible estimate is not necessarily eligible for its original clinical interpretation.

This finite retrospective empirical methods study follows the links between published use, source evidence, implementation provenance, analysis population and target estimand. Its contribution is a source-aware correction workflow illustrated by two complementary cases:

- **AVAglio:** recoverable source rules permit a population/model-specification reconstruction.
- **TRIO-US B07:** unresolved participant-level allocation phase requires inferential qualification, not a guessed randomized subset.

The study does not train a new classifier, select biomarkers or cut-points by outcome, estimate a field-wide failure rate, or demonstrate the clinical utility of this workflow. The historical analyses were visible before the dated targeted-analysis addendum; the project is not retrospectively described as prospectively preregistered.

## Start here

1. [Current v1.5 manuscript with embedded figures](5_manuscript/current_v1.5/QiTeng_RPv4_author_review_candidate_v1.5_20261012.md).
2. [Full RPv4 research proposal](0_admin/protocol/RPv4_Full_Research_Proposal_20261010.md).
3. [Detailed supervisory review and action record](7.Report/474_本轮详细行动记录_导师级科学叙事与子图重构_20261012.md).
4. [Figure/subpanel selection and quality review](7.Report/475_结果与子图选择_Nature风格质量审查_20261012.md).
5. [Current result tables](3_results/current_v1.5/) and [public-release boundary](0_admin/DATA_AND_PUBLICATION_BOUNDARY.md).

## Repository structure

The first eight folders reproduce the requested organization; three additional folders preserve references and version history.

```text
0_admin/       protocol, analysis plans, templates, status and audit contracts
1_data/        frozen aggregate inputs only; no participant records
2_code/        validators, manifest builder and v1.5 figure reproduction
3_results/     current derived tables and CSV supplements
4_figures/     Fig1–Fig8 filing slots; active main and supplementary figures
5_manuscript/  current v1.5 author-review manuscript and legends
6_release/     public author-review preparation inventory and status
7.Report/      detailed action, narrative and panel-selection records
8_archive/    complete, unchanged legacy public v1.4 snapshot
8_reference/  reference identities, not downloaded publisher PDFs
9_version/    version timeline and publication-change record
```

Each category has its own README. The root retains licenses, security guidance, requirements, the manifest and GitHub Actions configuration. Historical files were moved into a coherent archived tree, rather than leaving broken root-level analysis paths. Its original validator remains runnable from that tree.

## Current scientific results and counting units

| Unit | Count/status | What it means |
| --- | ---: | --- |
| Historical candidates | 28 | Purposive lineage, not systematic-search records |
| Core claim–estimand objects | 22 | Fixed object set; not representative of all oncology biomarkers |
| Objects with local numerical records | 15 | Seven further objects are source-audit only |
| Historical primary model rows | 27 | Multiple rows share participants and resources |
| Binary absolute-effect rows | 23 | Scale sensitivities; do not promote primary labels |
| Historical cross-trial units | 13 | Three dependency clusters with 10, 2 and 1 units |
| Current eligible verified-strict set | Empty | **Replication proportion not estimable**, not 0% |

### Recoverable correction: AVAglio

The source-defined ladder distinguishes 349 expression-evaluable participants, 339 IDH1-wild-type participants and 333 fixed complete cases with 260 deaths. A2 and A3 use the same 333 participants, without and with source-listed clinical adjustment.

| Deposited label | A2 interaction HR (95% CI) | A3 interaction HR (95% CI) |
| --- | --- | --- |
| Phillips proneural | 0.612 (0.355–1.056) | 0.516 (0.292–0.912) |
| Verhaak proneural | 0.513 (0.296–0.891) | 0.460 (0.261–0.811) |

These HRs are ratios of treatment HRs between marker groups, not subgroup treatment effects. All ten A0–A4 rows remain visible. A4 changes population, missing-category handling and a fixed ridge penalty, so it is an alternative branch. Deposited labels were reused; the original centroid assay was not independently executed. Specification sensitivity and numerical R/Python agreement are not independent external validation, and observed adjustment-related movement is not a causal decomposition.

### Information-limited correction: TRIO-US B07

The public linkage has 110 participants across Arms 1/2/3: 31/29/50, with 15/7/25 pCRs. Arms 1 and 2 are randomized-phase arms by trial design; Arm 3 participant phase remains unresolved. Conditional on the public Arm 3 records being a subset of the reported combined arm with the same pCR definition, **24 feasible integer states** allow 30–38 randomized participants and raw pCR fractions of 48.5–60.0%.

Those values form an aggregate compatibility range: not a confidence interval, treatment-effect bound or marker-by-treatment interaction bound. No participant phase was inferred from identifiers/order, and no pseudo-corrected model was fitted. Ten historical TRIO estimates remain restricted computational history; CHER-LOB within-trial calculations retain their separate status.

### Full supporting layers

All 23 absolute-effect rows are retained: one nominal sign-tail result, no within-family BH-robust result, and one conditional bootstrap interval (CHER-LOB ESR1, 4,736/5,000 valid fits). The nominal Stromal_FARMER result belongs to assignment-unverified TRIO and has q≈0.416. All 27 historical primary values remain visible, separate from AVAglio A2/A3. No result or frozen label was altered to strengthen the story.

## Current figure architecture

| Filing folder | Manuscript figure | Scientific job |
| --- | --- | --- |
| [Fig1](4_figures/Fig1/current_v1.5/) | Main Fig. 1 | Finite counting units and complementary correction paths |
| [Fig2](4_figures/Fig2/current_v1.5/) | Main Fig. 2 | All 22 objects: evidence, provenance and current role kept separate |
| [Fig3](4_figures/Fig3/current_v1.5/) | Main Fig. 3 | Complete AVAglio ladder and the shared-population comparison |
| [Fig4](4_figures/Fig4/current_v1.5/) | Main Fig. 4 | TRIO arm identity, 24 aggregate states and the interaction boundary |
| [Fig5](4_figures/Fig5/current_v1.5/) | Supplementary Fig. S1 | All 13 cross-trial units and current eligibility |
| [Fig6](4_figures/Fig6/current_v1.5/) | Supplementary Fig. S2 | All 23 absolute-effect sensitivities and uncertainty |
| [Fig7](4_figures/Fig7/current_v1.5/) | Supplementary Fig. S3 | All 27 historical primary estimates and role qualifications |
| [Fig8](4_figures/Fig8/) | Reserved | No eighth empirical main figure is claimed |

Every active assembly has editable SVG, embedded-font PDF and 600-dpi PNG. The 183-mm author-review profile follows Nature-like scientific typography; this does not certify journal compliance. Seven single-page **figure PDFs** were rasterized and visually reviewed. That is not a new whole-manuscript WPS visual PASS. Nineteen existing assemblies were evaluated for reuse; unexecuted systematic-review placeholders and superseded randomized-replication headlines are archived rather than pasted into the current manuscript.

DOP is displayed as high-risk HER2-negative breast cancer, including hormone-receptor-positive and triple-negative disease; legacy `TNBC_03` remains a stable identifier, not a population definition. Historical F0/F1 labels do not certify independent assay execution. RCC_04 retains an explicit unresolved source-design/adjudication conflict.

## Validate the public release

Only the Python standard library is required for integrity, privacy and scientific-source validation:

```bash
python 2_code/validate_public_release.py
```

The checks cover the complete canonical manifest, exact raw-byte aggregate contracts, archived v1.4 integrity, source/table arithmetic, current figure formats/hashes, reference order, seven manuscript image targets and absence of local paths, secrets and participant-identifier columns. They do not establish independent clinical validation or author approval. GitHub Actions runs the same validator on Linux.

After an intentional public change:

```bash
python 2_code/build_manifest.py
python 2_code/validate_public_release.py
```

**Do not rebuild the manifest to conceal a changed frozen scientific input.** The independent raw-byte contract must still match; any scientific correction requires a new version and rationale.

## Reproduce the seven figures

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python 2_code/reproduce_v1_5.py --png-only
# Omit --png-only to generate editable PDF/SVG as well.
```

Outputs go to ignored `generated_v1_5/`, not the published figure folders. The recipe first verifies 16 exact aggregate-source hashes and uses the same v1.5 panel rules. Arial is used when installed, with Liberation Sans/DejaVu Sans fallbacks. Different fonts or Matplotlib versions may change pixel hashes; this is not a change in the statistical inputs. Exact byte reproduction was checked in the recorded local environment separately from remote integrity verification.

This reproduces **aggregate figure construction**, not the participant-level Cox/logistic fits or the 115,000 historical bootstrap runs. Their lawful source-data access is outside this repository. The original v1.4 recipe and complete public snapshot remain in [the archive](8_archive/legacy_public_snapshot_v1.4/).

## Data, privacy and licensing

Published: aggregate tables, object provenance, complete historical model summaries, authored diagrams, Markdown manuscript, code and curated action records.

Excluded: raw expression matrices; participant-level outcomes or sample linkage; individual influence listings or resampled indices; private path inventories; actual author/contact records; credentials; software environments; third-party PDFs; WPS document page rasters; the bulk private delivery ZIP; and the privately supplied QiTeng skill implementation.

Code remains under [MIT](LICENSE); original documentation/diagrams/aggregate tables use [CC BY 4.0](LICENSE-DATA.md), subject to stated third-party terms. A repository license does not grant rights to raw trial materials. This is a research record, not medical advice, a diagnostic device or a treatment recommendation.

## Version history and next step

This update preserves the existing Git history and repository identity. It does **not** delete/recreate the repository, force-push or transmit a journal submission. The previous public snapshot at `aaf1a956d143ae6a46ba21637c00ba86670a9889` is retained coherently under `8_archive/legacy_public_snapshot_v1.4/` and in Git history.

Next: author review of the v1.5 narrative/panel allocation, actual completion of eleven manuscript truth fields, and target-specific DOCX compilation followed by **WPS-only** PDF export and all-page review. The v1.4 WPS history is not inherited by the new manuscript. No new disease/signature/search program or speculative sensitivity layer is required. Submission remains **HOLD** until the factual and application-level requirements are satisfied.
