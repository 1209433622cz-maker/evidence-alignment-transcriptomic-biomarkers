# R5B-A1R systematic-scoping outer-frame protocol and execution SOP candidate v0.7

**Project designation:** Systematic scoping review with a nested computational reproducibility benchmark  
**Version/date:** candidate v0.7, 13 September 2026  
**Status:** `A1R2_MACHINE_SCIENTIFIC_REFRAME_COMPLETE__FRESH_HUMAN_SIGNOFF_REQUIRED__FINAL_SEARCH_FORBIDDEN`  
**Prospective boundary:** this protocol governs only the R5B outer-frame search, screening, charting and bridge analysis. The R5A 22-claim benchmark, its 27 frozen primary models and all observed R5A results pre-date this protocol and must be disclosed as existing work.

This file is the sole authoritative A1R candidate. The A0 v0.3 protocol, v0.4 addendum, v0.5 machine-SOP candidate and A1 v0.6 candidate are retained as provenance only. If they conflict with this document, v0.7 controls. It does not become a registered protocol until the named scientific lead, information specialist and reviewers sign fresh human gates against the v0.7 hashes and the accepted OSF registration is archived.

## Scientific hierarchy and prospective reframe

The paper is prospectively organized as a **systematic evidence/estimand audit with a nested frozen randomized-trial reproducibility benchmark**.

- **Outer primary question:** among eligible published treatment-selection claim-estimands, how well do claim wording, original evidence design, executable biomarker definition, implementation fidelity, randomized or controlled opportunity, estimand compatibility, lawful data access and independent external evaluation align?
- **Nested secondary question:** among the purposively assembled claim-estimands already frozen before R5B, what occurs when executable biomarkers are re-evaluated in randomized or explicitly compatible controlled data without retraining, cutpoint search or outcome-driven selection?

This hierarchy was adopted before A1G01 sign-off, before OSF registration, before any `FORMAL_FINAL` search and before creation of the systematic outer denominator. It does not change R5A eligibility, its 22-claim registry, 15 locally evaluated claims, 27 primary models, treatment or endpoint coding, multiplicity families, 13 historical strict units or their labels. The 23-model absolute-risk analysis specified in `analysis_plan/binary_effect_scale_sensitivity_SOP_v1.0.md` is a nested robustness sensitivity only.

## 1. Review question and rationale

Among human cancers, how have pretreatment transcriptome-derived biomarkers been claimed to select therapy or predict differential treatment benefit, what evidence class and treatment-effect estimand support each claim, and how often are the marker definition, relevant randomized opportunity and analysis data sufficiently recoverable for estimand-aligned evaluation?

The outer frame is needed because the frozen R5A registry was purposive, date-limited and enriched for executable formulas and controlled data. R5A can test a nested reproducibility workflow but cannot estimate field-wide frequencies. R5B will create an auditable literature universe and a transparent bridge from that universe to the unchanged R5A core.

## 2. Standards and registration

- Conduct will follow the JBI Manual for Evidence Synthesis chapter on scoping reviews.
- Reporting will use PRISMA-ScR and the applicable PRISMA 2020 flow elements.
- Search methods will be archived against PRISMA-S.
- The primary MEDLINE strategy will undergo independent PRESS 2015 review before translation and final execution.
- The finalized protocol, search files, seed registry and SHA-256 manifest will be submitted through the OSF Generalized Systematic Review workflow before the first formal final search or screening of newly retrieved records. A valid freeze requires the registration GUID/URL, template name/version, public-versus-embargo choice, accepted/approved status, timestamp with timezone, downloadable snapshot, attachment list and snapshot/manifest hashes. A DOI is recorded only when issued.
- PROSPERO will not be used because its current guidance does not accept scoping reviews.
- Registration language must state that R5A and its findings already existed. It must not claim retrospective preregistration of the full project.

## 3. PCC eligibility framework

### Population

Human participants with any malignant neoplasm, at any disease stage or treatment line. Mixed cohorts are eligible only when cancer-patient results can be isolated.

### Concept

A pretreatment RNA/transcriptome-derived marker that is presented as selecting between therapeutic options, predicting differential treatment benefit, or identifying treatment-sensitive/resistant patients. The main scope includes:

- multigene expression scores or signatures;
- transcriptome-defined subtypes or classifiers;
- locked expression-derived models combining RNA features with clinical covariates, provided the RNA component and treatment-selection claim are separable.

Single-gene expression claims, protein-only assays, germline variants, DNA-only signatures, circulating-cell counts and post-treatment response markers are excluded from the primary universe. Potential single-gene expression records will be retained in a boundary ledger for a prespecified scope-sensitivity count; they will not be silently mixed into the main denominator.

Importantly, weak statistical design is not an exclusion criterion. Reports using treatment-selection or predictive language may be included even when the underlying evidence is only a treated-arm association. Evidence adequacy is charted after inclusion.

### Context

Anticancer therapeutic interventions evaluated in clinical patient data, including systemic therapy, radiotherapy and treatment strategies. Preclinical-only studies, cell lines, organoids, animal models, purely prognostic cohorts without a treatment-selection claim and diagnostic/screening applications are excluded.

## 4. Eligible report types and version rules

Peer-reviewed full reports, conference abstracts with sufficient claim information, trial biomarker reports and eligible preprints are included. Reviews, editorials and methods-only papers are used for citation discovery but are not claim reports unless they present a new eligible clinical claim.

Multiple records describing one study or claim are linked rather than double counted. Version priority is:

1. final peer-reviewed full report;
2. peer-reviewed companion biomarker report;
3. accepted manuscript;
4. preprint;
5. conference abstract.

Earlier versions remain in the record ledger and can establish claim chronology. Retractions and expressions of concern are retained in a status ledger, flagged prominently and excluded from evidentiary-positive counts unless the protocol is amended before results are viewed.

No language filter will be used in database searches. Non-English full texts will be translated with documented software or human assistance; claim wording and critical eligibility fields require bilingual or second-reviewer verification. The final search will cover database inception through its actual execution date, which must be written into the registered protocol and every exported search log.

## 5. Units and relational data model

Counts must never silently switch units. The database will maintain:

- `record_id`: one database or website retrieval;
- `report_id`: one publication, abstract, preprint or versioned report;
- `study_or_trial_id`: one underlying clinical study or trial;
- `trial_dataset_id`: one clinical/molecular data realization or repository deposit;
- `biomarker_definition_id`: one executable or described marker version;
- `claim_estimand_id`: biomarker version × population/setting × treatment contrast/backbone × endpoint/horizon × intended use;
- `claim_family_id`: optional linkage cluster only, never the default denominator.

One report may contain several claim-estimands; one claim may be supported by several reports; one trial may contribute several datasets. Many-to-many linkage tables are required. Correlated claims sharing trials, signatures or reports will be summarized with cluster-aware denominators and never called statistically independent.

The primary outer-frame analysis unit is the unique eligible `claim_estimand_id`. Every domain-primary percentage uses all eligible unique claim-estimands unless a metric in `protocol/primary_metric_registry_v0.6.tsv` explicitly declares a logically required conditional denominator. Report-, trial-, biomarker-definition- and dependency-cluster counts are mandatory companion counts and may not replace the primary denominator after results are known. `claim_family_id` is linkage/clustering only.

Split/merge decisions follow `protocol/claim_estimand_split_merge_manual_v0.5.md` and its signed fixtures. In brief, a substantive change in executable biomarker definition, population/setting, treatment contrast/backbone, endpoint family or claim-specific horizon, or intended use creates a separate claim-estimand. Multiple reports or versions of the same scientific claim are linked, not counted as new claim-estimands. A significant subgroup plus a nonsignificant subgroup does not create a formal interaction claim.

The frozen inventory column `published_language` is a legacy misnomer containing claim wording. R5B will map it to `published_claim_wording_legacy` and create a separate `publication_language` field without altering the frozen R5A table.

## 6. Evidence and estimand taxonomy

Each included claim-estimand will be classified independently on these axes:

1. **Claim language:** differential-benefit/treatment-selection; treatment-sensitive/resistant; response association; prognostic only; ambiguous.
2. **Evidence design:** randomized interaction tested; randomized subgroup without formal interaction; comparative non-randomized; treated single arm; mixed/unclear.
3. **Estimand recoverability:** exact; explicitly compatible; near-estimand; incompatible; indeterminate.
4. **Formula status:** executable exact; executable with prespecified compatibility adaptation; partial; unavailable; proprietary/controlled.
5. **Implementation fidelity:** F0 exact executable original; F1 prespecified platform-bridged exact function; F2 source-compatible approximation; F3 partial or missing component; F4 non-executable, as defined in `protocol/implementation_fidelity_taxonomy_v0.1.md`.
6. **Clinical/expression data access:** public immediate; controlled application; sponsor/author request; aggregate only; unavailable/unknown.
7. **Trial opportunity:** relevant randomized trial exists; controlled non-randomized opportunity; no identified opportunity; indeterminate.
8. **External-evaluation maturity:** no external evaluation; overlapping/internal evaluation; nonoverlapping near-estimand evaluation; nonoverlapping estimand-compatible evaluation; indeterminate.
9. **Interaction interval reporting:** reported; recoverable from sufficient statistics; absent; indeterminate.

Trial existence, formula executability, implementation fidelity, data access, estimand compatibility, external evaluation and interval reporting are separate axes. They are not assumed to form a nested one-way funnel and must not be converted into an unweighted or post hoc composite score.

## 7. Search architecture

Two complementary tracks will be searched and linked.

### Track A — claim literature

The primary search targets human cancer transcriptomic signatures/classifiers combined with treatment prediction, treatment selection, response/resistance or treatment-effect heterogeneity. The strategy will use both controlled vocabulary and text words and will not require a formal interaction term, because doing so would preferentially exclude mislabelled predictive claims.

Minimum bibliographic coverage, whose exact platform and institutional access must be selected without unresolved “and/or” entries before registration:

- PubMed, explicitly treated as the PubMed record universe rather than the MEDLINE subset alone;
- either Embase.com (Elsevier) or Embase via Ovid, named exactly;
- Web of Science Core Collection and/or Scopus only after the team explicitly freezes whether one or both will be used;
- CENTRAL via the Cochrane Library, with access route and export behavior recorded.

Grey/supplemental coverage:

- ASCO, AACR and ESMO conference sources;
- medRxiv and bioRxiv/Europe PMC preprints as applicable;
- backward and forward citation chaining of every included report and every frozen known item;
- related-article and author/signature-name searches specified in advance.

### Track B — trial and data opportunity

This track is not used to inflate the claim-literature denominator. It identifies randomized/controlled trials, companion biomarker reports and data deposits relevant to included claims through:

- ClinicalTrials.gov;
- WHO ICTRP;
- CENTRAL trial records;
- GEO, ArrayExpress/BioStudies, dbGaP, EGA and trial-specific repositories;
- cited data-availability statements, supplements and sponsor portals.

For every opportunity search, record repository/registry, query, date, accession, access tier, licence, expected files, stopping rule and reviewer. The stopping rule is completion of all predeclared sources plus backward/forward chaining with no new eligible report or dataset in two successive citation rounds.

## 8. Search development, known-item validation and PRESS

Search development may inspect hit counts, syntax errors and retrieval of frozen known items, but newly found scientific records must not be screened into the final denominator before registration. Every candidate iteration is logged with query, date, hit count, known-item recall and reason for change.

The seed registry is report-level, not claim-row-level. It must include anchor, validation/replication and boundary-sentinel reports and must be hash locked before final search testing. The current candidate contains 27 unique reports; two are not PubMed-indexed and therefore test grey-literature routes rather than PubMed recall.

Mandatory boundary sentinels are:

- the randomized STAMPEDE transcriptomic treatment-interaction report (Cell, 2025);
- the PASS-01 randomized biomarker preprint (medRxiv, 2026).

Failure of the complete predeclared search package to retrieve either sentinel is a search-calibration failure. A PubMed strategy is not expected to retrieve the non-indexed PASS-01 preprint.

Before registration, an independent information specialist must PRESS-review the versioned PubMed/MEDLINE candidate across question translation, Boolean/proximity logic, subject headings, text words, syntax/spelling and limits/filters. The review, response and any amendments are archived before translation to other platforms. A substantive change to a concept block, subject heading, text-word family, field, proximity expression or filter returns to the information specialist for scoped re-PRESS.

Pre-registration development may expose only explicitly isolated calibration or workload-pilot records. These records are not enumerated as the final eligible universe, are not scientifically extracted, do not enter final counts, and must be re-encountered and re-screened in A2 if retrieved by the registered final search. Every development execution is labelled `DEVELOPMENT_VALIDATION_ONLY`; only a post-registration execution may be labelled `FORMAL_FINAL`.

## 9. Selection process

- Two named human reviewers independently screen titles/abstracts and full texts; their raw decisions are append-only and never overwritten by consensus or adjudication.
- Before the 200-record workload pilot or formal screening, both reviewers independently classify the same 25 heterogeneous calibration records under the frozen manual. Calibration passes only at at least 75% raw agreement and after all conceptual disagreements are documented and resolved; Cohen's kappa is descriptive, not the sole gate. A failed calibration triggers a manual amendment and a new non-overlapping calibration set.
- Conflicts are resolved by consensus, then by a third clinical/statistical adjudicator.
- Automation or AI may assist deduplication and prioritization but cannot be the sole screener or adjudicator.
- Full-text exclusions use a single prespecified primary reason, while secondary reasons remain available in an audit field.
- Unavailable full texts enter a dedicated contact/access ledger with dates and outcomes.

## 10. Data charting and verification

Critical fields—report/study linkage, biomarker definition, published claim wording, treatment contrast, endpoint/horizon, intended use, evidence class, interaction test, formula status, trial opportunity, access tier and mapping to the frozen core—will be independently double extracted or extracted by one reviewer and verified field by field by another. Disagreement requires documented resolution.

The extraction form will distinguish reported subgroup effects from a formal marker-by-treatment interaction and its confidence interval. Significance in one marker subgroup and non-significance in another is insufficient to establish treatment-effect modification.

## 11. Analysis plan

Outer-primary outputs are descriptive counts and proportions governed by `protocol/primary_metric_registry_v0.6.tsv`. The default denominator is all eligible unique `claim_estimand_id`s. Every metric predeclares its numerator, denominator, missing/indeterminate handling, report-version precedence and permitted companion counts. Alternative report-, study/trial-, biomarker-definition- and dependency-cluster summaries are labelled sensitivities and cannot replace the primary metric after results are known.

The nine registered metrics are not nine co-equal headlines. They are organized prospectively into three evidentiary domains:

- **Domain A — claim/evidence alignment:** PM01 and PM02;
- **Domain B — executability/evaluability:** PM03 through PM06;
- **Domain C — validation maturity:** PM07.

PM08 is a supporting reporting-quality metric conditional on formal interaction evidence. PM09 is a bridge/coverage metric linking the systematic outer universe to the frozen R5A benchmark. Neither is a field-quality headline endpoint. No composite score will be calculated.

No oncology-wide pooled interaction effect will be calculated across heterogeneous cancers, therapies, marker scales and endpoints. Meta-analysis is allowed only in a prospectively defined stratum with sufficiently aligned biomarker version, population/setting, treatment contrast, endpoint/horizon and interaction estimand. Otherwise, effect estimates are displayed without pooling.

Planned maps include:

- claim wording versus actual evidence class;
- exact/compatible/near/unavailable estimand opportunity;
- formula status, data access and trial existence as separate axes;
- randomized interaction testing and confidence-interval reporting;
- mapping from the outer universe into the frozen R5A 22-claim benchmark.

The R5A bridge is purely classificatory. R5B must not redefine the frozen 22 claims, 27 primary models, 13 historical strict-denominator claim units or their results. New eligible reports enter the outer universe. Any future computational expansion requires a separately versioned protocol amendment and analysis stage.

For the 23 frozen binary pCR models, the key effect-scale sensitivity follows the pre-run frozen SOP v1.0. The same analytic rows and four-parameter logistic model are used to calculate treatment risk differences at fixed pooled-sample Q25 and Q75 marker values and `ΔRD = RD(Q75) - RD(Q25)`. Participants are resampled within randomized arm for 5,000 replicates. Percentile intervals, explicit failed-fit accounting, deterministic replay and within-trial/contrast Benjamini–Hochberg values are reported. Additive-only signals are labelled `scale-dependent uncertainty` and cannot alter a frozen replication label.

## 12. Bias, certainty and sensitivity analyses

This scoping review will not assign a single evidence-certainty score across all designs. Instead it will chart design features relevant to predictive inference: randomized allocation, prespecified marker and cutpoint, formal interaction, treatment contrast, endpoint alignment, missingness, multiplicity, independent evaluation and data/formula availability. Applicable randomized evidence will be checked against CONSORT 2025 principles; biomarker reporting will be checked against REMARK where relevant.

Prespecified sensitivities:

- peer-reviewed full reports only;
- exclusion of conference abstracts/preprints;
- one claim per report and one claim per trial cluster;
- main multigene/transcriptome classifier scope versus the single-gene boundary ledger;
- exact estimands only versus exact plus explicitly compatible estimands;
- public-IPD-available versus all access tiers.

## 13. Reproducibility and public package

Raw database exports will be stored read-only and hashed before deduplication. The package will include database/platform, complete query, date, hit count, export format, deduplication rules/software, citation-chaining log, screening ledgers, extraction dictionary, amendment log and PRISMA-S checklist.

The nested computational benchmark also requires a `source_acquisition_manifest.tsv` with accession/URL, access date, licence, expected hash and local filename; configurable `--data-root`; `verify-inputs` and, where lawful, rehydration modes; and a clean-directory reproducibility test. Public packaging must not redistribute controlled or licence-restricted data.

## 14. AI and human-accountability boundary

AI may support code drafting, query formatting, deduplication suggestions, candidate prioritization, translation assistance and prose organization. Humans remain responsible for eligibility, claim/estimand classification, statistical interpretation, source verification and final text. Tool identity, version, creator/provider, access date and exact uses will be disclosed truthfully under the target journal's policy. Sensitive or controlled data will not be placed in unapproved external systems.

## 15. A1 no-cycle execution order and release gates

Formal final searches and formal screening are prohibited until all machine and human gates below are closed in this order:

1. freeze this sole authoritative v0.7 protocol candidate, PCC, scientific hierarchy, report hierarchy, single-gene boundary and amendment policy;
2. freeze the `claim_estimand_id` key, controlled vocabularies, split/merge manual, primary metric registry and synthetic fixtures, then obtain scientific-lead semantic sign-off;
3. complete full-text RCC_04/RCC_05 provenance adjudication and update only the R5B relational registry;
4. freeze exact database/platform/access, grey/preprint/trial-data routes, screening software and export capabilities;
5. name two screeners, one clinical/statistical adjudicator, one search executor/data manager and one independent PRESS information specialist; record training and conflicts; the five governance roles must be explicitly rostered and the PRESS reviewer must not be the search executor or either screener;
6. freeze title/abstract and full-text manuals; complete and resolve the 25-record calibration;
7. complete independent PRESS review and response on the versioned PubMed/MEDLINE candidate;
8. fill and sign the team-capacity thresholds, lock the PubMed sampling frame/query hash/RNG plan, then materialize a 200-record non-overlapping title/abstract yield and workload sample;
9. calibrated reviewers independently classify all 200 records and record time; freeze and hash both raw submissions before any adjudication; then run the deterministic pilot analyzer to calculate apparent likely-eligible yield, conservative forward fraction (`likely eligible + uncertain`), uncertain fraction, disagreement, Wilson 95% intervals and workload range;
10. apply the predeclared `FEASIBLE`, `REVISE` or `HOLD` rule from machine-recomputed metrics and the pre-signed capacity thresholds. A human decision may be more conservative than the machine recommendation but may not upgrade `REVISE`/`HOLD` to `FEASIBLE` without a new prespecified cycle. Any substantive search change creates a new hash, reruns sentinel recall and triggers scoped re-PRESS plus a new non-overlapping pilot. At most two substantive revision cycles are allowed;
11. translate the closed strategy to each frozen database and complete information-specialist semantic review plus development-only sentinel validation;
12. validate raw export, deterministic deduplication, version linking, dual-decision preservation, extraction round-trip and source lineage on isolated fixtures;
13. assemble the registration bundle, PRISMA-S prospective crosswalk, hashes and human/machine gate table;
14. submit and confirm an accepted/approved OSF Generalized Systematic Review registration with preserved snapshot evidence;
15. only after the effective OSF timestamp and PI/methods-lead release signature may the first `FORMAL_FINAL` run begin.

The report-status hierarchy is frozen as: final peer-reviewed full report; peer-reviewed companion biomarker report; accepted manuscript; preprint without a peer-reviewed successor at cutoff; conference abstract without a fuller successor and with every key claim-estimand component recoverable. Earlier versions remain chronology records. Main-scope analyses include multigene RNA signatures/transcriptome classifiers; single-gene expression remains a separately enumerated boundary ledger and sensitivity only.

Amendments made before any development labels are viewed are documented and versioned. After calibration or pilot labels are viewed, amendments may address only demonstrated eligibility-language ambiguity, retrieval error, platform syntax or workload feasibility; they may not use replication direction, effect size, significance or desired manuscript result. Any change to eligibility, primary metrics, denominator, or scientific scope after registration requires an OSF-visible amendment before implementation and cannot retroactively redefine prior decisions.

### Machine semantic closure rule

A1 gate closure is not established by file existence, a SHA-256 value or a signature alone. Before fresh human execution, `scripts/validate_r5b_a1r_scientific_reframe.py` must verify the v0.7 hierarchy, metric roles, absolute-effect outputs, frozen R5A identities, prohibited language and figure lineage. Before A2 release, the versioned A1H semantic validator must then parse the evidence content for every gate and verify role identity, status values, cross-file consistency, chronology and gate-specific invariants. In particular, blank but signed templates, a `REVISE`/`HOLD` workload decision, unresolved core database access, unmatched calibration raw decisions, or an OSF snapshot/hash mismatch are fail-closed. The workbook is a dashboard only and can never authorize A2.

The governance roster must contain five distinct named roles: `RG01` independent PRESS information specialist, `RG02` reviewer A, `RG03` reviewer B, `RG04` clinical/statistical adjudicator and `RG05` search executor/data manager. Calibration reviewer IDs must be exactly `RG02`/`RG03`, adjudication must bind to `RG04`, and the PRESS record must bind to `RG01`.

The 200-record pilot is completed in two machine stages: materialization (before labels) and deterministic analysis (after two frozen reviewer submissions plus adjudication). The machine analyzer writes `audit/pubmed_workload_pilot_metrics_v0.6.json`; the signed human decision in `templates/pubmed_workload_pilot_final_decision_v0.6.json` must bind to that file and cannot contradict a non-FEASIBLE machine result.

Current gate:

> `A1R2_MACHINE_REFRAME_AND_EFFECT_SCALE_PASS__READY_FOR_FRESH_A1H_SIGNOFF__NO_GO_FINAL_SEARCH__HOLD_SUBMISSION`

## 16. Current unresolved decisions before registration

- Fresh scientific-lead sign-off on this v0.7 protocol, the v0.6 metric registry, the frozen absolute-effect SOP and the unchanged split/merge semantics.
- Human RCC adjudication. Machine evidence supports a role split for RCC_04, but its formal interaction status is not located; RCC_05 mixes a weighted T-cell-inflamed GEP with formula-inexact RNA-seq implementations and remains unresolved.
- Institutional access and exact platform choices for Embase, Web of Science/Scopus and CENTRAL.
- PRESS reviewer, two screeners, adjudicator and searcher identities, training and conflicts.
- Screening software, blinding/export workflow, team capacity and final search execution/cutoff date.
- Completion of 25-record calibration, independent PRESS, the subsequent 200-record workload pilot, strategy translations and sentinel checks.
- OSF public/embargo decision, accepted registration GUID/URL/status/timestamp, downloadable snapshot and hashes.

## 17. Core methodological sources

1. PRISMA-ScR: https://www.prisma-statement.org/scoping
2. PRISMA 2020: https://www.bmj.com/content/372/bmj.n71
3. JBI Manual for Evidence Synthesis 2024: https://jbi-global-wiki.refined.site/download/attachments/355599504/JBI%20Manual%20for%20Evidence%20Synthesis%202024.pdf
4. PRISMA-S: https://doi.org/10.1186/s13643-020-01542-z
5. PRESS 2015: https://pubmed.ncbi.nlm.nih.gov/27005575/
6. OSF registrations: https://help.osf.io/article/330-welcome-to-registrations
7. PROSPERO registration guidance: https://www.crd.york.ac.uk/prospero/documents/Registering%20a%20review%20on%20PROSPERO.pdf
8. CONSORT 2025: https://www.bmj.com/content/389/bmj-2024-081123
