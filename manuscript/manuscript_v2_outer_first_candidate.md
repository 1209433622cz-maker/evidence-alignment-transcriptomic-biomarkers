# Evidence alignment and randomized reproducibility of transcriptomic treatment-selection biomarkers in oncology

**Scientific master:** A1R2 outer-first candidate, 13 September 2026  
**Status:** scientific hierarchy and nested results are machine-frozen; systematic-search counts marked `PENDING_A2_OUTER_RESULT` are intentionally unresolved. Human protocol sign-off, formal registration/search, authorship/accountability fields and submission approval are outstanding.  
**Candidate journal family:** npj Precision Oncology first-line; British Journal of Cancer backup; Clinical Cancer Research stretch target after the systematic outer frame is complete.

## Abstract

Transcriptomic biomarkers are often described as selecting therapy although their claims may originate from treated-arm response associations, incompletely executable assays or comparisons that do not estimate differential treatment benefit. We designed a protocol-governed systematic evidence and estimand audit with a nested, frozen randomized-trial re-execution benchmark. The outer study links each claim-estimand to its wording, original evidence design, formula executability, implementation fidelity, randomized comparison opportunity, estimand compatibility, lawful data path, independent evaluation and interval reporting. Its registered multi-database search and dual screening have not yet begun; field-level counts therefore remain `[[PENDING_A2_OUTER_RESULT:ABSTRACT]]`. The nested benchmark comprised 15 locally executable claims and 27 frozen marker-by-treatment models across breast cancer and glioblastoma. One model was nominally significant and none survived within-context multiplicity correction. Ten of 27 ratio-scale confidence intervals spanned more than tenfold. Across 13 historical label replays in three dependency clusters, no positive label was reproduced; 12 of 13 units arose from two clusters. A prespecified additive-risk sensitivity completed all 23 binary models: 22 passed the bootstrap validity gate, one was conditional-warning and none was non-estimable. One additive-scale interval excluded zero nominally, but its within-family q value was 0.416; no result was multiplicity robust. These findings do not establish a universal absence of treatment-effect heterogeneity. They show why claim language, assay executability, randomized estimand alignment, effect scale, uncertainty and independent evaluation must remain separate evidentiary layers before a biomarker is described as treatment selecting.

## Introduction

Transcriptomic signatures can capture proliferation, immune activity, stromal composition, DNA repair and tumour lineage. Their clinical promise in precision oncology is not merely to classify tumours or predict outcome, but to help choose between plausible treatments. That use requires evidence that the treatment effect differs with the biomarker. A response association among recipients of one therapy can be biologically meaningful and prognostic without establishing a comparative treatment-benefit estimand.[1,2]

The path from a published claim to treatment selection contains several non-interchangeable steps. The biomarker must have an identifiable formula and orientation; the implementation must preserve the published mathematical function or transparently declare deviations; an eligible randomized comparison must exist; the endpoint, treatment contrast and analysis population must align with the original claim; the data must be lawfully accessible; and the evaluation must report uncertainty. Directional concordance, a significant within-subgroup treatment comparison, or significance in one arm but not another cannot replace a formal interaction analysis.[1,6]

Positive randomized transcriptomic interactions are possible. A large STAMPEDE ancillary analysis reported heterogeneity in docetaxel effects for selected expression classifiers.[3] Conversely, the prospectively specified PASS-01 biomarker challenge found prognostic information without a biomarker meeting its differential-treatment-benefit endpoint.[4] Computational benchmarks can compare discovery algorithms,[5] but they do not necessarily trace the chain from predictive wording through executable formula and randomized estimand to external re-execution. Earlier reviews of oncology biomarkers have assessed interaction evidence broadly,[20]; a defensible new contribution therefore requires the narrower combination of transcriptomic treatment-selection claims, claim identity and provenance, implementation fidelity, randomized estimand alignment, data recoverability and frozen re-execution.

We designed a systematic evidence/estimand audit with a nested randomized-trial benchmark. The outer-primary study will estimate how often eligible oncology transcriptomic treatment-selection claims traverse each evidence layer. The nested-secondary study asks what happens among claims that can already be frozen and mapped to randomized or explicitly compatible controlled-trial data without retraining, outcome-driven cutpoints or favourable-result selection. The hierarchy was fixed before human protocol sign-off, registration and formal searching.

## Results

### The systematic claim universe is the outer-primary analysis

The registered multi-database search, deduplication, dual screening and report-to-claim mapping remain pending. Figure 1a will show records, reports and unique `claim_estimand_id` units after A2; no count from the earlier purposive 22-claim registry will be presented as field prevalence.

`[[PENDING_A2_OUTER_RESULT:PRISMA_RECORDS_REPORTS_CLAIMS]]`

Figure 1b treats formula executability, randomized opportunity, estimand compatibility and lawful data access as intersecting axes rather than sequential filters. Figure 1c preserves separate identifiers for reports, biomarkers, claim-estimands, implementations and trials/datasets. The prior R5A benchmark is linked as a nested empirical subset (Fig. 1d), not as the systematic universe.

### Claim wording will be cross-classified with original evidence design

The outer audit will cross-classify differential-benefit, treatment-selection, sensitive/resistant, response-association and ambiguous wording against randomized-interaction, randomized-subgroup-only, comparative non-randomized, treated-single-arm and mixed/unclear evidence (Fig. 2). Whether the source reported a formal treatment-by-biomarker interaction is an independent field.

`[[PENDING_A2_OUTER_RESULT:PM01_PM02_CLAIM_EVIDENCE_ALIGNMENT]]`

No claim will be upgraded because predictive language appears in a title, abstract or discussion. Disagreements between two reviewers will remain visible until adjudication.

### Executability and implementation fidelity are distinct from biological plausibility

Formula recoverability, feature availability, weights, normalization, orientation and platform dependence will be extracted separately. Implementations will be classified as exact original executable (F0), platform-bridged exact-function (F1), source-compatible approximation (F2), partial/materially incomplete (F3), or non-executable (F4). No fidelity level will be inferred from an observed outcome association.

`[[PENDING_A2_OUTER_RESULT:PM03_FORMULA_EXECUTABILITY_AND_FIDELITY]]`

Figure 3 will display fidelity alongside randomized opportunity, estimand compatibility, lawful data path, independent evaluation and interval support. These dimensions will not be collapsed into a weighted readiness score.

### Randomized opportunity, estimand alignment and lawful data paths will be jointly mapped

The outer review will distinguish the existence of a controlled comparison from its clinical and statistical compatibility with the claim. Treatment regimen and comparator, disease state, line of therapy, endpoint, timing, analysis population and biomarker scale will be adjudicated explicitly. Public availability and lawful analytic access will be recorded separately from the existence of a trial.

`[[PENDING_A2_OUTER_RESULT:PM04_PM06_OPPORTUNITY_ESTIMAND_DATA_PATH]]`

This structure prevents unavailable data from being described as biological failure and prevents a merely accessible dataset from being called a valid replication opportunity.

### Independent evaluation and interval reporting define validation maturity

The outer study will report independent evaluation at the claim-estimand level and will retain whether effect estimates were accompanied by uncertainty intervals. PM07 is the primary validation-maturity metric; interval reporting is supporting reporting-quality context.

`[[PENDING_A2_OUTER_RESULT:PM07_PM08_VALIDATION_MATURITY]]`

PM09 will identify the bridge into the frozen R5A benchmark but will not be interpreted as a field-wide replication denominator.

### The nested frozen benchmark comprised 15 claims and 27 primary interaction models

The pre-existing local benchmark generated 27 frozen primary marker-by-treatment models from 15 claims across HER2 dual blockade, glioblastoma bevacizumab, triple-negative breast cancer platinum, PARP/platinum and PARP/immunotherapy contexts (Fig. 4 and Supplementary Table 1). Twenty-three models used logistic regression for pathologic complete response and four used Cox regression for overall survival. All were reproduced from participant-level or hash-frozen score inputs within an absolute numerical difference below 1 × 10−6.

One model was nominally significant: the AVAglio Verhaak-proneural overall-survival interaction (interaction HR 0.586, 95% CI 0.346–0.992; P=0.0468). It did not pass its frozen within-context Benjamini–Hochberg correction (q=0.1871). No primary model had q<0.10. Complete intervals, rather than significance-filtered estimates, are displayed; odds-ratio and hazard-ratio contexts are not pooled.

### Precision and effect scale constrained interpretation of non-significant interactions

Sample sizes ranged from 57 to 360 (median 81) and event counts from 19 to 270 (median 40). Ten of 27 ratio-scale confidence intervals spanned more than tenfold, all in CHER-LOB, which contained 57 participants and 19 pCR events. Each primary interval retained an interaction ratio of 1.5 in at least one direction. These results support “no multiplicity-robust evidence observed,” not equivalence or biomarker failure.

The formal additive-risk sensitivity completed all 23 binary models with frozen analytic rows and Q25/Q75 marker values (Fig. 5c and Fig. S5). Twenty-two models had at least 4,750 valid arm-stratified bootstrap replicates and passed; CHER-LOB ESR1_DESMEDT had 4,736/5,000 valid replicates and was retained with a conditional-percentile warning. No model was non-estimable. The signs of ΔRD and the frozen logistic interaction coefficient agreed in all 23 models.

TRIO-US B07 Stromal_FARMER was the sole additive-scale nominal result: ΔRD=−0.360, bootstrap 95% CI −0.748 to −0.013, sign-tail P=0.0416. It did not survive the ten-marker HER2 family correction (q=0.416) and is classified as scale-dependent nominal uncertainty, not replication. The earlier exploratory CHER-LOB GEPARSIXTO_IMMUNE linear-probability diagnostic did not reproduce as nominal under the frozen logistic g-computation estimand (ΔRD=−0.364, 95% CI −0.880 to 0.036; P=0.0824; q=0.300). No additive result was multiplicity robust, and the additive sensitivity changed no frozen primary label.

Firth/Jeffreys refitting of the same 23 binary designs retained all coefficient signs and produced no nominal interaction; correlation-aware maxT analyses of the two ten-marker HER2 families produced no familywise-significant result. These sensitivity layers characterize small-sample and dependence uncertainty without replacing the primary analyses.

### Cross-trial effect migration remained uncertain

Twelve claims had quantitative estimates in paired trials (Fig. 5a,b). Nine of ten HER2 signatures retained their interaction-coefficient sign from TRIO-US B07 to CHER-LOB, as did both glioblastoma signatures from AVAglio to GLARIUS. None met the frozen strict positive rule. Trial-stratified bootstrap intervals for the change in absolute interaction magnitude crossed zero for all 12 pairs.

For Verhaak-proneural glioblastoma, the nominal AVAglio coefficient moved from −0.534 to −0.086 in GLARIUS. The change in absolute magnitude was −0.448 (95% bootstrap interval −0.869 to 0.618), compatible with attenuation but not demonstrating it. Absolute-scale survival analyses at 12, 15 and 18 months also retained intervals crossing zero. The 18-month GLARIUS proneural-control cells had only two participants at risk, so later horizons are displayed transparently rather than used to redefine the primary Cox estimand.

### Historical label replay was descriptive and dependency-aware

The frozen historical strict denominator contained 13 claim units across three dependency clusters. Ten were HER2 units, two were glioblastoma units and one was TNBC IGG14. Twelve of 13 units (92.3%) arose from the two HER2 and glioblastoma clusters; they are not 13 independent replications.

No historical label was positive on replay. Twelve units had complete executable positive-path rules and none met them. For IGG14, published CALGB 40603 P=0.800 made a necessary condition fail, while the unavailable signed anchor coefficient prevented reconstruction of the full positive path. The valid description is therefore 0/13 historical label replays positive across three dependency clusters, with 12 of 13 units arising from two clusters and 0/12 complete positive paths; it is not a field-wide replication rate.

## Discussion

The outer-primary study is designed around a simple but often obscured distinction: predictive wording does not itself establish randomized evidence of differential treatment benefit. A treatment-selection claim must remain connected to its evidence design, executable assay, controlled comparison, estimand, lawful data path, independent evaluation and uncertainty. The formal prevalence of gaps along that chain cannot be stated until the registered A2 review is complete.

The nested randomized benchmark demonstrates why this hierarchy matters. None of 27 frozen primary interactions was multiplicity robust, but precision was limited and several estimates remained compatible with clinically relevant effects. The new additive-risk analysis found one nominal scale-specific result that did not survive family correction and could not relabel the primary model. This pattern separates absence of robust evidence from evidence of absence.

Effect modification is scale dependent. A logistic interaction addresses departure from multiplicative odds, whereas clinical decision making often concerns absolute benefit. Freezing both the primary scale and the sensitivity interpretation prevents the analysis from selecting whichever scale looks most favourable. The shift from an exploratory linear-probability diagnostic to formal logistic g-computation changed which row appeared nominal; this is evidence for disciplined prespecification, not an invitation to promote either result.

The project also separates replication from direction. Eleven of 12 paired claims retained coefficient direction, yet every interval for cross-trial change in absolute magnitude crossed zero and no strict positive rule was met. Directional concordance can coexist with weak information, attenuated magnitude or incompatible estimands. It should be displayed with intervals and dependency structure, not converted into a validation label.

These findings should not be generalized to all transcriptomic biomarkers. Large randomized resources can detect genuine treatment heterogeneity,[3] and prospective challenges can distinguish prognostic performance from differential benefit.[4] The nested benchmark is purposive, concentrated in a small number of treatment contexts and dominated by shared trial pairs. Its contribution is methodological and empirical: it shows the consequences of requiring claim identity, executable formulas, compatible randomized estimands and frozen re-execution.

The completed outer review will add the field-level evidence map that the nested study lacks. It will quantify claim/evidence alignment, executability/evaluability and validation maturity using `claim_estimand_id`, while preventing reports, claims and datasets from being counted as interchangeable units. It will also show which barriers are scientific, computational, access-related or reporting-related. The independent-axis design is important because a biomarker may be executable but lack an eligible trial, or have a trial but no lawful participant-level data path.

Limitations of the nested benchmark include small biomarker subsets, correlated signatures, heterogeneous platforms and treatment backbones, aggregate-only claims, and public-data availability bias. The additive bootstrap produced one conditional-warning row owing to separation/non-convergence; its interval is explicitly conditional on 4,736 valid resamples. The outer protocol is not yet registered or executed, so the manuscript deliberately contains unresolved tokens rather than reconstructed counts. Human authors must approve the hierarchy and complete governance before formal search.

Strengths include a frozen primary layer, stable claim identifiers, explicit dependency clusters, complete confidence intervals, implementation-fidelity taxonomy, independent numerical reconciliation, deterministic 5,000-replicate replay, a prespecified additive-risk estimand and source-driven vector figures. Together these safeguards make both the evidence chain and its remaining uncertainty auditable.

Transcriptomic treatment-selection biomarkers should be advanced through aligned evidence rather than predictive language alone. Formula recoverability, randomized estimand compatibility, absolute and relative effect scales, independent evaluation and adequate interaction precision are distinct requirements. The completed systematic outer frame will establish how often the literature meets them; the nested benchmark shows what disciplined re-execution reveals when evaluation is possible.

## Methods

### Study design and chronology

This project combines an outer systematic scoping review/evidence audit with a nested retrospective secondary analysis of public de-identified trial data and published aggregate evidence. The hierarchy in `R5B_A1R_scientific_hierarchy_freeze_v1.0` was set before A1G01 human sign-off, registration and formal multi-database searching. R5A treatment contrasts, endpoints, analytic rows, biomarker definitions, multiplicity families, primary coefficients and labels were not changed.

### Outer systematic review

The binding protocol is `R5B_A1R_systematic_scoping_protocol_candidate_v0.7.md`. Searches will be peer reviewed under PRESS before registration. After deduplication, two reviewers will independently screen records and extract eligible reports. The primary unit is `claim_estimand_id`; report, biomarker, trial/dataset and implementation identifiers are retained separately. Disagreements require adjudication with a recorded reason.

The primary metric registry groups PM01–PM02 as claim/evidence alignment, PM03–PM06 as executability/evaluability and PM07 as validation maturity. PM08 is supporting interval-reporting context and PM09 bridges to the nested benchmark. Denominators and missingness rules are frozen per metric. No composite readiness score is permitted.

### Claim and evidence classification

Claim wording is classified from explicit source text and mapped to original evidence design. A formal interaction requires an explicit comparative treatment-by-biomarker test or equivalent contrast; differences in subgroup-specific significance do not qualify. Randomized opportunity is separate from estimand compatibility. Compatibility adjudication considers disease setting, treatment regimen and comparator, line of therapy, endpoint, timing, population, marker form and analysis scale.

### Executability and implementation fidelity

Formula recovery captures features, aliases, weights, intercepts, transformations, normalization, orientation, platform and cutpoint. Implementations are classified F0–F4 under the frozen taxonomy. F1 must preserve the published mathematical function despite a declared platform bridge; F2 denotes a source-compatible approximation with material deviations declared. Outcome performance cannot determine fidelity.

### Nested trial data and signature reconstruction

The nested benchmark used public data associated with TRIO-US B07 and CHER-LOB for HER2-positive breast cancer,[7,8] AVAglio and GLARIUS for glioblastoma,[9,10] BrighTNess and CALGB 40603 evidence for IGG14,[11] BrighTNess and I-SPY2 resources for CIN70,[12] and the DOP arm of I-SPY2 for revisedPARPi7.[13] Biomarkers were reconstructed from published genes and weights where available. No signature was retrained, reweighted or selected using the current outcomes; no outcome-driven cutpoint or cohort search was performed.

### Frozen primary estimands

For pathologic complete response, logistic regression included marker, randomized treatment and marker×treatment. For overall survival, Cox regression used the analogous terms. Treatment and marker coding were preserved by context, so ratios above or below one do not have a universal favourable direction. P values were adjusted within the frozen context or family using Benjamini–Hochberg. The primary interaction scale and labels remain immutable.

### Binary absolute-effect sensitivity

For each of 23 binary designs, Q25 and Q75 of the standardized marker were computed once on the frozen analytic rows using the linear quantile definition. From the fitted logistic model, treatment-specific risks were predicted at each marker value. `RD(m)=P(Y=1|T=1,m)−P(Y=1|T=0,m)` and `ΔRD=RD(Q75)−RD(Q25)`.

Uncertainty used 5,000 nonparametric resamples within randomized arms with fixed Q25/Q75 values and no re-standardization. Percentile intervals and a two-sided sign-tail P value with a plus-one correction were calculated among valid resamples. At least 4,750 valid resamples constituted PASS; 4,500–4,749 produced a conditional-percentile warning; fewer than 4,500 were non-estimable. Benjamini–Hochberg correction used five frozen families: ten TRIO-US B07 HER2 markers, ten CHER-LOB HER2 markers and three prespecified singleton TNBC contrasts. The analysis was repeated deterministically with identical seeds and arrays; all 23 digests matched.

An additive-only nominal or adjusted result could not promote a frozen primary label. A linear-probability model with HC3 covariance was retained as a diagnostic and not treated as the g-computation estimand.

### Precision, bias-reduction, dependence and migration

Interaction information was characterized with complete confidence intervals, interval fold widths and model-specific detectable magnitudes. Firth/Jeffreys logistic regression used the same 23 designs. Within each HER2 trial, common-outcome parametric bootstrap retained treatment allocation and joint marker dependence for maxT adjustment. Cross-trial migration resampled participants within treatment arms for HER2 and within treatment-by-marker cells for glioblastoma; intervals were reported for signed coefficient change and change in absolute magnitude.

### Historical strict denominator

Strict membership required an executable marker and an exact or prospectively declared compatible external randomized/controlled opportunity. External participants were independent of source-claim cohorts, but claim units sharing trial pairs were not statistically independent. Results are reported as descriptive label replays and complete-rule paths with cluster counts.

### Software and reproducibility

Analyses used Python 3.12.14, NumPy 2.5.2, pandas 2.3.3, SciPy 1.18.0, statsmodels 0.14.6 and lifelines 0.30.3. Inputs and outputs carry SHA-256 hashes. An independent validator reconstructed the 23 designs, refit point models with a separate SciPy optimizer, recalculated bootstrap intervals and sign-tail P values from 115,000 persisted replicates, reimplemented BH adjustment and checked every input hash. All 23 model rows and 23 multiplicity rows passed.

### Ethics, accountability and availability

Only public de-identified data and published aggregate results were used; original studies reported ethics and consent. Before submission, human authors must verify trial registration identifiers, authorship and CRediT roles, funding, competing interests, acknowledgements, repository DOI/licence and the exact AI-assisted research/writing disclosure. The future public package will redistribute disclosure-safe derived tables, code, protocol and manifests, not restricted participant-level inputs.

## References

1. Mandrekar, S. J. & Sargent, D. J. Clinical trial designs for predictive biomarker validation: one size does not fit all. *J. Biopharm. Stat.* **19**, 530–542 (2009). https://doi.org/10.1080/10543400902802458
2. Renfro, L. A. et al. Clinical trial designs incorporating predictive biomarkers. *Cancer Treat. Rev.* **43**, 74–82 (2016). https://doi.org/10.1016/j.ctrv.2015.12.008
3. Grist, E. et al. Tumor transcriptome-wide expression classifiers predict treatment sensitivity in advanced prostate cancers. *Cell* **188**, 5717–5734.e10 (2025). https://doi.org/10.1016/j.cell.2025.07.042
4. Quan, W. et al. Multimodal machine learning for predicting outcomes in the PASS-01 trial. *medRxiv* (2026). https://doi.org/10.64898/2026.08.24.26360900
5. Li, A. Z. et al. Benchmarking computational methods for multi-omics biomarker discovery in cancer. *Brief. Bioinform.* **27**, bbag200 (2026). https://doi.org/10.1093/bib/bbag200
6. Hopewell, S. et al. CONSORT 2025 statement. *BMJ* **389**, e081123 (2025). https://doi.org/10.1136/bmj-2024-081123
7. Hurvitz, S. A. et al. Pathologic and molecular responses in TRIO-US B07. *Nat. Commun.* **11**, 5824 (2020). https://doi.org/10.1038/s41467-020-19494-2
8. Guarneri, V. et al. Prospective biomarker analysis of CHER-LOB. *Oncologist* **20**, 1001–1010 (2015). https://doi.org/10.1634/theoncologist.2015-0138
9. Sandmann, T. et al. Proneural glioblastoma and bevacizumab in AVAglio. *J. Clin. Oncol.* **33**, 2735–2744 (2015). https://doi.org/10.1200/JCO.2015.61.5005
10. Weller, J. et al. Proneural subtype in GLARIUS. *J. Neurooncol.* **165**, 337–347 (2023). https://doi.org/10.1007/s11060-023-04470-9
11. Conte, B. et al. A 14-gene B-cell immune signature and platinum response. *EBioMedicine* **101**, 105043 (2024). https://doi.org/10.1016/j.ebiom.2024.105043
12. Wolf, D. M. et al. DNA repair biomarkers and CIN70 in I-SPY2. *npj Breast Cancer* **3**, 31 (2017). https://doi.org/10.1038/s41523-017-0025-7
13. Pusztai, L. et al. Durvalumab with olaparib and paclitaxel in I-SPY2. *Cancer Cell* **39**, 989–998.e5 (2021). https://doi.org/10.1016/j.ccell.2021.05.009
14. McDermott, D. F. et al. Molecular correlates of atezolizumab with or without bevacizumab. *Nat. Med.* **24**, 749–757 (2018). https://doi.org/10.1038/s41591-018-0053-3
15. Motzer, R. J. et al. Biomarker analysis of JAVELIN Renal 101. *Nat. Med.* **26**, 1733–1741 (2020). https://doi.org/10.1038/s41591-020-1044-8
16. Braun, D. A. et al. Somatic alterations and immune infiltration under PD-1 blockade. *Nat. Med.* **26**, 909–918 (2020). https://doi.org/10.1038/s41591-020-0839-y
17. Scott, J. G. et al. Pan-cancer prediction of radiotherapy benefit. *Lancet Oncol.* **22**, 1221–1229 (2021). https://doi.org/10.1016/S1470-2045(21)00347-8
18. Sgroi, D. C. et al. HOXB13/IL17BR and extended letrozole benefit. *J. Natl Cancer Inst.* **105**, 1036–1042 (2013). https://doi.org/10.1093/jnci/djt146
19. Bartlett, J. M. S. et al. Breast Cancer Index and extended endocrine therapy. *Ann. Oncol.* **30**, 1776–1783 (2019). https://doi.org/10.1093/annonc/mdz289
20. Simon, R. M. et al. Evaluation of treatment-by-biomarker interaction evidence for oncology biomarkers. *Sci. Rep.* **7** (2017). https://doi.org/10.1038/s41598-017-07358-7

## Figure legends

**Fig. 1 | Systematic claim universe, independent evidence axes and bridge to the nested benchmark.** Panels a–c are architecture only until registered A2 screening. Panel d distinguishes the outer eligible universe from the pre-existing purposive 15-claim/27-model R5A subset. Formula, randomized opportunity, estimand alignment and lawful data path are independent axes, not a sequential funnel.

**Fig. 2 | Claim language and original supporting evidence.** Claim-language classes are cross-tabulated against original evidence designs, with formal-interaction reporting shown separately. Counts remain pending dual A2 extraction and adjudication.

**Fig. 3 | Multi-axis treatment-selection readiness.** Claim-estimands are displayed across formula, implementation fidelity, randomized opportunity, estimand compatibility, lawful data path, independent evaluation and interval support. No composite score or rank is calculated. Rows remain pending A2.

**Fig. 4 | Claim-centred nested randomized-trial benchmark.** Fifteen locally executable claims are primary visual units; 27 trial-level OR or HR interaction estimates and full 95% confidence intervals are nested beneath them. Endpoint scales are separated. Nominal significance does not denote multiplicity-robust replication.

**Fig. 5 | Cross-trial migration and effect-scale sensitivity.** **a,** Anchor and external-trial interaction coefficients for 12 paired claims. **b,** Bootstrap change in absolute coefficient magnitude. **c,** ΔRD(Q75−Q25) for all 23 binary models; the nominal TRIO-US B07 Stromal_FARMER result did not survive family correction. **d,** GBM absolute-survival analogues. Relative, additive-binary and time-to-event scales are not pooled.

**Fig. S5 | Complete binary additive-effect forest.** ΔRD estimates and arm-stratified bootstrap percentile intervals for 23 models. The CHER-LOB ESR1_DESMEDT interval is conditional on 4,736/5,000 valid resamples and carries a warning. Additive-only evidence cannot alter a frozen primary label.
