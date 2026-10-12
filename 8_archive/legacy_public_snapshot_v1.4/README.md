# Evidence alignment of transcriptomic treatment-biomarker claims in oncology

[![Validate public release](https://github.com/1209433622cz-maker/evidence-alignment-transcriptomic-biomarkers/actions/workflows/validate.yml/badge.svg)](https://github.com/1209433622cz-maker/evidence-alignment-transcriptomic-biomarkers/actions/workflows/validate.yml)

This repository is the public, aggregate-only research record for a finite retrospective methods study of whether published transcriptomic treatment-biomarker claims remain interpretable when five layers are aligned:

> original claim → evidence design → executable implementation → analysis population → statistical estimand.

The study does not train a new response classifier, optimize a cut-point after outcomes are known, or estimate a field-wide failure rate. Its 22 objects are a purposive, dependency-clustered set assembled through the recorded project history.

## Current status

The active plan is [`RPv4_Full_Research_Proposal_20261010.md`](protocol/RPv4_Full_Research_Proposal_20261010.md). The current release incorporates completed S0–S8B work, the 12 October S9 organization and a new **RebuildAudit** full physical-file audit. It retains baseline freeze, targeted AVAglio reanalysis, TRIO identifiability closure, evidence integration, four current main figures, manuscript candidate **v1.4**, supplementary CSVs and the dated preparation record. Earlier manuscripts remain historical versions, not competing current instructions.

This public repository was deleted and recreated under the same name with the user's explicit authorization on 12 October 2026. The old Git objects and dated platform metadata were backed up privately before deletion. The recreated repository starts a new Git history: retained historical research files are explicit artifacts, not inherited Git commits. Its first published payload passed 23/23 checks both locally and in a fresh remote clone; GitHub's hosted validation succeeded, four regenerated PNGs matched exactly, and three regenerated CSVs matched field-for-field. Publication does not disclose the full private workspace or imply that historical inferences were reinstated. See [the reconstruction record](docs/REBUILD_AUDIT_AND_REUSABLE_ASSETS_20261012.md).

Current public gate:

> `CURATED_PUBLIC_REBUILD_PAYLOAD_VALIDATED__SUBMISSION_CANDIDATE_ASSEMBLED__HOLD_11_REAL_AUTHOR_TRUTH_FIELDS__HOLD_JOURNAL_TRANSMISSION__HOLD_SUBMISSION`

GitHub publication is not journal submission. Eleven real author/accountability categories remain open: authors and order, affiliations, corresponding-author details, CRediT, funding, competing interests, ethics/consent, acknowledgements, repository/licence facts, AI/LLM disclosure facts and the institutional quartile rule. No synthetic or inherited values are used.

## Main scientific results

### Finite evidence set

| Item | Count or status |
|---|---:|
| Historical candidates | 28 |
| Current claim–estimand objects | 22 |
| Objects with historical local numerical results | 15 |
| Historical primary model rows | 27 |
| Absolute-effect sensitivity rows | 23 |
| Historical cross-trial units | 13 |
| Current verified strict cross-trial members | 0 |
| Current strict replication proportion | Not estimable |

Historical rows remain reproducible records. Their present inferential role is governed by the current source, implementation, population and estimand adjudication; reproducibility of a number does not by itself restore its earlier clinical interpretation.

### AVAglio model ladder

The AVAglio analysis separated the original 349 expression-evaluable set, the 339 IDH1-wild-type set and a fixed 333-participant, 260-event source-covariate-availability set. A2 applied the frozen unadjusted interaction formula on the 333-row set; A3 used the same rows with source-listed covariates.

| Deposited subtype label | A2 interaction HR (95% CI) | P value | Interpretation |
|---|---:|---:|---|
| Phillips proneural | 0.612 (0.355–1.056) | 0.0777 | Same-trial specification bridge; not independently significant |
| Verhaak proneural | 0.513 (0.296–0.891) | 0.0178 | Same-trial nominal interaction; not independent validation |

Both models passed the prespecified convergence and proportional-hazards checks and were independently reproduced in R. These results do not constitute two independent validations because they reuse the same trial, endpoint and participants.

### TRIO-US B07 identifiability boundary

The public source contains 110 unique rows in three treatment arms, but no authoritative participant-level assignment-phase field. Design documents identify arms 1 and 2 as randomized and establish that arm 3 mixes a lead-in with randomized participants, but they do not identify which arm-3 rows belong to which phase.

Accordingly, the ten TRIO-derived objects are not eligible for pure randomized treatment-effect-modification inference. The conditional aggregate arm-3 randomized count is 30–38 and its raw pCR proportion can range from 48.5% to 60.0%; this is an identification bound, not a confidence interval, and it does not identify a marker-by-treatment interaction. No pseudo-corrected model or participant-level guessing was performed.

### Historical absolute-effect layer

The 23 frozen absolute-effect sensitivities contain one nominal additive-scale result and no multiplicity-robust result. None changed a frozen primary label. They remain supporting analyses rather than a rescue path for a positive biomarker claim.

## Current manuscript and figures

The current Markdown manuscript is [`QiTeng_RPv4_BMC_MRM_submission_candidate_v1.4_20261011.md`](manuscript/QiTeng_RPv4_BMC_MRM_submission_candidate_v1.4_20261011.md). It uses the title:

> *From reproducible estimates to defensible inference: a provenance-aware audit and targeted reanalysis of oncology transcriptomic biomarkers*

The DOCX/PDF files remain in the private preparation package. The unchanged v1.4 documents passed 32/32 content/structure checks. Their recorded WPS-only visual coverage comprises a 16-page integrated reading manuscript, a 21-page submission-layout manuscript and a one-page draft letter (38 pages total). S9 verifies the exact hashes and the recorded page-image hashes; it does not claim a new render or independent human visual approval. LibreOffice was not used. The four current main figures have **11 actual panels (3 + 1 + 4 + 3)** and are available in SVG, PDF and 600-dpi PNG formats:

1. finite study boundary and correction pathways;
2. claim–evidence–estimand alignment matrix;
3. AVAglio population/model ladder;
4. historical replay versus current inferential eligibility.

Historical A1R2 figures and results remain versioned in place. They are not the current manuscript figure set.

The three [`supplementary_csv/`](supplementary_csv/) files contain 10 AVAglio ladder rows, 13 historical/current cross-trial rows and 23 absolute-effect rows. Their parsed fields equal the retained TSV tables; a nominal additive result is not upgraded to replication.

## Local audit and public boundary

The original, pre-organization audit covered **67,098 files / 4,265,073,613 logical bytes**, including archived dependencies. The later RebuildAudit snapshot contains **120,875 physical file paths**, representing **68,442 independent filesystem file identities**, **4,682,374,197 identity-level bytes**, and **43,187 distinct SHA-256 contents**. Path-level bytes are **8,580,171,904**; they must not be interpreted as independent disk usage, because **52,433 extra paths** share file identities through preserved compatibility hardlinks. The audit did not follow **992 reparse points**, and excluded its own newly generated outputs, new backup, fresh publication staging directory and new submission-copy directory to prevent self-inclusion.

Every file identity received a full-byte hash. Supported files also received complete text/structure reads, image decoding, PDF all-page text extraction or container/stream CRC checks. **No parser/CRC/read error was recorded.** An additional pass through 176 initially opaque non-runtime records fully parsed 59 JSON-lines files, read 45 additional text files and streamed all 16 file members in two TAR containers; 70 unsupported/binary records remain explicitly hash-only. Runtime and Git internals received hashes rather than semantic interpretation. There are **1,275 zero-byte file identities**; emptiness is recorded, not automatically called corruption. The audit indexed **2,198 visual file identities** and **32,676 ZIP-member records**, separately from the loose-file denominator. This is not a claim that every historical file, image or source paper received expert manual review. The original dated summary is retained in [`docs/V4_S9_WORKSPACE_AUDIT_AND_RELEASE_20261012.md`](docs/V4_S9_WORKSPACE_AUDIT_AND_RELEASE_20261012.md); current aggregate statistics and reuse guidance are in [the RebuildAudit record](docs/REBUILD_AUDIT_AND_REUSABLE_ASSETS_20261012.md). No scientific source was deleted or deduplicated.

The private workspace was organized into administration, data, code, results, figures, manuscripts, releases, reports, archive, references and versions. Old paths have compatibility entries. Main-number folders retain historical stage context: only Figures 1–4 belong to the current manuscript; Figure 5 is historical and Figures 6–8 are reserved. Rendered pages, source-paper images, contact sheets and software icons are not mislabelled as main figures.

**This repository is deliberately not a mirror of that workspace.** Participant-level inputs, individual influence records, private path maps, author facts, credentials, downloaded third-party papers, runtime trees and large delivery archives remain excluded. Aggregate reproduction does not imply that participant-level statistical refitting is possible from this repository alone.

## Repository map

| Directory | Contents |
|---|---|
| `protocol/` | RPv4, dated amendments and statistical addenda |
| `source_data/` | Aggregate claim, lineage and source-inventory tables |
| `results/` | Historical and current aggregate model, diagnostics and manuscript tables |
| `figures/` | Historical figures plus the current four-figure set |
| `manuscript/` | Historical manuscripts and current v1.4 Markdown candidate |
| `analysis_plan/` | Frozen absolute-effect sensitivity SOP |
| `scripts/` | Public validators, manifest builder, analysis and figure code |
| `audit/` | Machine validation, independent checks and stage status records |
| `docs/` | Roadmap, release history, data boundary and journal preflight |
| `templates/` | Claim-estimand and opportunity-ascertainment templates |
| `supplementary_csv/` | Lossless, standard-delimited derivatives of S1–S3 |
| `public_reproduction_v1_4/` | Self-contained frozen aggregate sources, tables and figure/CSV recipes |

See [`docs/REPOSITORY_CONTENT_MAP.md`](docs/REPOSITORY_CONTENT_MAP.md) for the release-specific index.

## Validation

The repository-wide validator uses only the Python standard library:

```bash
python scripts/validate_public_release.py
```

It checks the canonical SHA-256 manifest, aggregate-only boundary, absence of local paths and secrets, key S2/S3/S4/S5/S6H1 invariants, current v1.4 scientific bounds, supplement equivalence and required figure formats. It does not assert author approval, journal acceptance or portal upload.

To rebuild the **current v1.4** figures in a new generated workspace (historical recipes remain available):

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python public_reproduction_v1_4/scripts/build_v4_s8_figures.py
python public_reproduction_v1_4/scripts/prepare_supplementary_csv.py
```

The figure recipe verifies eleven frozen aggregate hashes before plotting. Generated output does not inherit the archived WPS visual PASS. See the reproduction-directory README for input/output scope. After intentionally promoting a new public result, rebuild the manifest and run the validator; do not edit a frozen estimate to make validation pass.

The figure builder uses only aggregate tables. Re-executing participant-level models requires lawful access to their original inputs and is outside the public repository.

## Data and redistribution boundary

This repository excludes raw expression matrices, participant-level clinical data, sample-linkage files, restricted influence-record listings, resampled participant indices, author/contact/accountability records, credentials, third-party PDFs, WPS QA page rasters and bulk delivery archives. See [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md).

## Next milestone

The next step is factual completion, not additional exploratory analysis. Real authors must close the eleven accountability categories, after which the manuscript, title page, cover letter and approved article-type enquiry can be finalized and rerendered in WPS for upload-level QA. External transmission and the final journal-submission click remain separate author-controlled actions.

## Reuse priorities and limits

| Priority | Resource | Reuse supported | Not supported |
|---|---|---|---|
| P0 | RPv4, current v1.4 manuscript, four figures and S1–S3 | Current argument, exact aggregate reporting and candidate preparation | Field-wide prevalence or an accepted journal submission |
| P0 | Eleven hash-locked aggregate inputs and figure recipes | Reconstructing figure/table geometry and values without participant data | Full Cox/logistic refitting from public inputs alone |
| P1 | AVAglio ladder and independent R/diagnostic summaries | Checking population-versus-model specification changes | Independent external validation or causal attribution of adjustment effects |
| P1 | TRIO design/identifiability record | Preserving an explicitly unresolved assignment-phase boundary | Guessing patient phase, constructing a pseudo-random subset or estimating an interaction bound |
| P1 | 23 absolute-effect sensitivity rows | Scale-aware uncertainty and primary-label preservation | Promoting a nominal additive-only result to replication |
| P2 | Historical manuscript, source-role and release records | Reconstructing chronology and preventing repeated retired work | Reactivating superseded protocols or inheriting old author sign-offs |
| P3 | Runtime/environment and private archive | Local recovery and implementation context | Automatically redistributing dependencies, papers, author facts or restricted data |

Four current figures have defined scientific roles; reserved Figures 6–8 are not missing analyses. Historical Figure 5, supplementary plots, document page renders and published source panels retain their own version/type. File organization is not new scientific evidence. Hardlinks and junctions are compatibility mechanisms, not independent backups.

## Submission candidate versus public release

The private candidate contains the integrated reading manuscript, submission-layout manuscript, draft cover letter, vector figures, editable table, three CSV supplements and the exact WPS visual-history binding. The planned portal attachment set contains nine files. The preparation ZIP itself, QA rasters and duplicate reading copies are not intended as portal attachments or public Git assets.

The RebuildAudit package does not modify DOCX/PDF content, statistics or primary labels. Its 38-page WPS record is revalidated by exact document/page hashes; no new WPS export or new all-page visual PASS is claimed. If real author data change a document, that changed document must be rebuilt and rendered again in **WPS only**. Eleven factual categories remain open; general approval cannot substitute for the actual author/ethics/funding/contact information. BMC Medical Research Methodology remains a conditional preparation route, not a guarantee of article acceptance or a verified institution-specific quartile.

## Recovery and version integrity

The old public `main` snapshot was `b483e9a88b93cd447b10442c6acb321479efbd7e`. Private backup records distinguish direct remote cloning from any API-verified local-object backup; they do not claim that a Git bundle restores GitHub repository IDs, stars, settings or all release metadata automatically. Do not merge the old full Git history into this curated release without a fresh privacy review.

Normal textual payload is manifest-checked after canonical LF normalization; eleven reproduction inputs additionally retain their exact raw-byte SHA-256 contract via `.gitattributes`. Do not weaken either contract to hide a line-ending change. A successful local check, remote push and hosted workflow are different events, and their results should be recorded separately.

## Licensing and disclaimer

Code is released under the MIT License. Original documentation and aggregate tables are released under CC BY 4.0; third-party materials retain their own terms. This is research software and an evolving evidence-audit record, not medical advice, a diagnostic device, a treatment recommendation or a peer-reviewed clinical validation.
