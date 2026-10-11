# RebuildAudit release and reusable research assets

Date: 12 October 2026. Active research plan: RPv4. Manuscript: v1.4.

## What this release changes

It updates repository documentation, records a fresh whole-project physical-file audit, prepares a new independent submission-candidate copy and curates a fresh public Git history. It does not change model inputs, estimands, estimates, primary labels or the source/population adjudications. Local detailed file inventories and backup objects are not included in this public repository.

The approved local organization retains eleven top-level classes, with dated phase groups inside their existing subfolders. Original paths remain compatible. Main Figures 1–4 are current; Figure 5 is historical and Figures 6–8 are reserved. Source-paper panels, document renders, contact sheets, templates and software icons have distinct roles, not invented main-figure numbers.

## Exact audit denominator

| Measure | Value |
|---|---:|
| Physical file paths | 120,875 |
| Independent filesystem file identities | 68,442 |
| Extra paths sharing file identity | 52,433 |
| Path-level logical bytes | 8,580,171,904 |
| Identity-level bytes | 4,682,374,197 |
| Distinct SHA-256 contents | 43,187 |
| Distinct-content bytes | 3,714,464,737 |
| Zero-byte file identities | 1,275 |
| Reparse points recorded but not traversed | 992 |
| Visual file identities | 2,198 |
| ZIP-member index rows | 32,676 |
| File read/parse/CRC exceptions | 0 |

Snapshot excludes only this run's newly generated inventory, backup, public staging and candidate-copy directories. Hashing is exhaustive at file-identity level; metadata associates the result with all observed physical paths. Equal contents in different identities are not called hardlinks. These are not filesystem allocated-block or free-space measurements.

Inspection coverage: 5,997 complete text/structure reads; 216 container CRC/structure checks; 60 gzip stream checks; 429 PDF all-page text extractions; 1,195 raster decode checks; 60,360 runtime/Git byte-hash-only records; 176 other byte-hash-only records; 9 separately labelled zero-byte records. These categories describe machine inspection, not manual interpretation of every paper/image/dependency. No parser issue is not proof that every scientific result is correct.

The supplementary inspection of those 176 initially opaque records parsed 59 JSON-lines files, fully read 45 extra text records and streamed all 16 file members of two TAR archives. Seventy unsupported/binary records remain hash-only. This extension had no exceptions and did not overwrite the dated snapshot or execute/extract archived source code. A private reuse index covers 1,939 manuscript, reference, governance and work-record assets with size, hash, content-structure summary and reuse boundary; its automated priorities are triage, not new scientific verdicts.

## Valuable assets and their owner

The research contribution is the distinction between reproducing an estimate and defending the interpretation attached to it. The central chain is original claim, evidence design, implementation, population and estimand. Current source-role tables and manuscript support that chain; internal workflow complexity is not itself a result.

1. **Current plan and chronology:** RPv4 bounds the finite retrospective study. Historical R4/R5 review-first and human-gate designs are retained as history, not prerequisites for current completion.
2. **AVAglio targeted ladder:** ten aggregate rows, the fixed 333-participant/260-event bridge, diagnostics and independent R checking. The same-trial comparisons demonstrate specification sensitivity, not independent biomarker validation.
3. **TRIO identifiability closure:** public design evidence identifies a mixed arm without identifying each assignment phase. Aggregate conditional bounds cannot determine which patient to exclude or a marker-by-treatment effect.
4. **Historical model layers:** 27 primary and 23 absolute-effect rows remain distinct from current inference eligibility. One nominal additive-scale result does not overwrite a frozen primary label.
5. **Current manuscript interfaces:** Table 1 covers 22 objects; supplements contain 10, 13 and 23 rows. Four figures contain 11 panels. Aggregate figure reconstruction is supported publicly; participant-level refitting requires lawful original inputs.
6. **Work records and recovery:** dated reports, source decisions and exact hash manifests prevent chronology loss and repeated retired work. A conversation or machine report never substitutes for an original source, factual author confirmation or independent study data.

## Reproduction and privacy

Run `python scripts/validate_public_release.py` from the repository root. Reproduce plots and supplements in a disposable working copy using the commands in `public_reproduction_v1_4/README.md`. Keep the eleven raw input hashes unchanged. Generated figures are derivatives, not an automatic replacement of the promoted payload and not new WPS manuscript QA.

Private exclusions include participant/sample data, individual influence and resampling records, author truth/contact information, downloaded third-party PDFs, full local path maps, credential/config secrets, dependency trees and bulk delivery packages. The new Git history is constructed only from the already-curated aggregate public payload plus these non-sensitive descriptions.

## Honest completion boundary

The full local inventory, candidate assembly and publication preparation are distinct from deletion/recreation, push, fresh-remote readback and hosted CI. The external release receipt should document those events when they actually succeed. No new clinical claim, no new author fact and no journal submission is created by this release.

Actual first-publication verification: the recreated public repository has ID **1414689827**, replacing old ID **1412172637**. The first new-history commit is `19fd894297dae7a03ab8713042a4c0cb2214ab35`. Its clean remote clone passed **23/23** checks and a **177-row manifest**; all eleven raw aggregate inputs passed their hash contract, four regenerated PNGs had identical SHA-256 hashes, and three CSVs matched the promoted fields. [GitHub hosted validation](https://github.com/1209433622cz-maker/evidence-alignment-transcriptomic-biomarkers/actions/runs/38167299325) completed successfully for that commit. Subsequent documentation commits have their own manifest and workflow; this first-publication commit is not a self-referential promise of the final HEAD.

Next scientific milestone: complete the existing eleven real factual categories; rebuild only affected documents; run WPS-only full-page QA; then obtain the corresponding author's explicit portal-upload authorization. Do not reopen topic selection, grow the cohort set or run sensitivities without a concrete new input or defect.
