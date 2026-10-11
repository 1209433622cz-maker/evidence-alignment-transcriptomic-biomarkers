# From reproducible estimates to defensible inference: a provenance-aware audit and targeted reanalysis of oncology transcriptomic biomarkers

**Authors:** `[[AUTHORS_PENDING]]`  
**Affiliations:** `[[AFFILIATIONS_PENDING]]`  
**Corresponding author:** `[[CORRESPONDING_AUTHOR_PENDING]]`  
**Target journal route:** BMC Medical Research Methodology  
**Article type:** Research Article; author-approved conditional route pending editorial scope confirmation

## Abstract

### Background

Transcriptomic biomarkers may be biologically relevant, associated with response under treatment, or informative about differential treatment benefit. These are not equivalent claims. Reproducible computation cannot resolve discrepancies in source wording, assay implementation, analysis population or target estimand.

### Methods

We performed a finite retrospective empirical methods study of 22 claim–estimand objects selected from 28 historical candidates. Original use, source evidence, implementation fidelity, population identity, estimand compatibility and current inferential role were recorded separately. Twenty-seven historical marker-by-treatment rows and 23 binary absolute-effect sensitivities were preserved. New numerical work was restricted to a source-defined AVAglio model ladder; TRIO-US B07 analysis stopped when randomized-phase identity could not be recovered from public participant records.

### Results

The 22 objects comprised 15 with local numerical records and seven source-audit objects. In TRIO-US B07, trial design identified Arms 1 and 2 as randomized, but 50 public Arm 3 records could include direct-assignment and randomized participants. No authoritative participant-level phase mapping was available. Under report-compatible aggregate constraints, the randomized subset of public Arm 3 could contain 30–38 participants, with a raw pathologic-complete-response proportion of 48.5–60.0%; this range did not identify a marker-by-treatment interaction. The ten historical TRIO models were retained as computational history, not verified randomized evidence. In AVAglio, 349 expression-evaluable, 339 IDH1-wild-type and 333 fixed complete-case participants separated population restriction from model adjustment. On the shared 333-participant set, unadjusted interaction hazard ratios were 0.612 (95% CI 0.355–1.056; P=0.0777) for Phillips proneural and 0.513 (0.296–0.891; P=0.0178) for Verhaak proneural; source-covariate adjustment yielded 0.516 (0.292–0.912; P=0.0229) and 0.460 (0.261–0.811; P=0.00728), respectively. Historical cross-trial replay retained 13 units in three dependency clusters, but no unit met the current verified-strict denominator. Among 23 absolute-effect sensitivities, one was nominal and none was multiplicity robust.

### Conclusions

Computational reproducibility and defensible clinical inference require separate, versioned records. In this selected set, source provenance, implementation, population identity and estimand alignment changed what historical results could support without deleting unfavourable results or creating a post hoc denominator. The output is an auditable evidence-alignment framework and two correction pathways, not a field-wide biomarker failure rate.

## Keywords

Transcriptomic biomarkers; treatment-effect modification; claim-estimand alignment; provenance; randomized trials; reproducibility

## Background

Transcriptomic signatures can describe tumour lineage, proliferation, immune activity, stromal composition and DNA-repair biology. Their clinical interpretation depends on the question being asked. Association with outcome among recipients of one therapy is not the same estimand as differential benefit between therapies, and neither is equivalent to the utility of a biomarker-guided treatment strategy.[1,2]

That distinction can be lost at several points. A candidate may be called predictive although only a treated-cohort association was estimated. A molecular analysis embedded in a randomized trial may include participants from different allocation phases. A score may be approximated while retaining the original assay name. A numerical estimate may therefore be reproducible while answering a different clinical question from the published claim. Prior oncology-wide work assessed treatment-by-biomarker interaction evidence for approved biomarkers,[17] but did not combine transcriptomic claim provenance, implementation fidelity, population recoverability, target estimand and frozen re-execution within the same selected resource set.

RPv4 defined a bounded empirical question: among a fixed set of oncology transcriptomic biomarker objects, how do published claims, source evidence, implementation, population identity and validation estimands align, and what happens when a discrepancy permits numerical reconstruction versus only inferential qualification? The study does not develop a response classifier, optimize a cut point, search for favourable biomarkers or estimate field-wide prevalence. Historical values remain visible even when their current interpretation changes.

## Methods

### Study design and chronological transparency

This was a finite retrospective empirical methods study with provenance auditing and targeted secondary reanalysis. The historical analyses preceded RPv4 and were not relabelled as prospectively registered. RPv4 froze the revised hierarchy, the A0–A4 AVAglio ladder, the TRIO stopping rule and the manuscript/figure architecture before their corresponding V4 executions. Existing Q2-R5 files remained read-only writing and numerical history.

### Object hierarchy and selection

Five identifiers were maintained separately: report, `claim_estimand_id`, implementation, trial/population and statistical model. The 28 historical candidates formed a purposive lineage. The 22 core objects were frozen before V4-S2 and retained without outcome-driven reselection; 15 had local numerical records. Candidate counts, objects and model rows were never combined into a screening denominator.

### Source-claim and implementation adjudication

Primary reports, available supplementary material, publisher corrections and repository records were reviewed for original use, evidence design, result wording, treatment comparison, endpoint, implementation and formal interaction evidence. Treatment-conditioned association (U1), differential treatment benefit (U2) and biomarker-guided strategy utility were kept separate. A tested candidate was not coded as a positive claim unless the source made a positive conclusion. Machine assistance supported file comparison, code checks and prose organization; final scientific adjudication remains the authors' responsibility.

### TRIO population and identifiability audit

Public participant records were checked for unique linkage, treatment arm and outcome. Randomized-phase identity required an explicit source field or authoritative mapping. Trial design was used to identify Arms 1 and 2 as randomized-phase arms, but participant identifiers and row order were prohibited as evidence for splitting Arm 3. Aggregate constraints enumerated report-compatible integer combinations only. Because those combinations did not identify marker values, treatment contrasts or marker-by-treatment coefficients, no corrected randomized interaction or simulation was performed.

### AVAglio A0–A4 model ladder

For both source-deposited proneural labels, A0 was an unadjusted Cox marker, treatment and marker-by-treatment model in all 349 expression-evaluable participants. A1 applied the same model in 339 IDH1-wild-type participants. A2 applied the same unadjusted model after the frozen six-row literal-NA exclusion, yielding 333 participants. A3 used the identical 333 rows and adjusted for the source-listed clinical covariates: age, corticosteroid use, surgical status, sex, Karnofsky performance status, MGMT status, Mini-Mental State Examination, RPA class and WHO performance status. Age was continuous and categorical covariates were indicator encoded. A4 retained all 339 IDH1-wild-type rows using explicit missing levels and a fixed `lifelines` Cox ridge penalty of 0.01. No hyperparameter tuning or outcome-guided model selection was performed. Interaction hazard ratios are exponentiated marker-by-treatment coefficients with Wald intervals.

### Historical model and absolute-effect records

The 27 historical primary interaction rows and 23 binary absolute-effect rows were imported without overwriting historical coefficients, intervals, P values, q values, multiplicity families or primary labels. For the historical binary sensitivity, delta risk difference was `RD(Q75) − RD(Q25)`, where `RD(m)=P(Y=1|T=1,m)−P(Y=1|T=0,m)`. Marker quartiles were fixed from the pooled analytic sample. Five thousand nonparametric replicates resampled within each frozen recorded treatment arm. Percentile intervals used valid replicates, and Benjamini–Hochberg correction was applied within five frozen trial–contrast families. Additive-scale results could not promote a primary label.

### Cross-trial eligibility

All 13 historical units and three dependency-cluster identifiers were retained. Current verified-strict membership required a phase-verified target population, sufficient estimand compatibility, an independent evaluation and a recoverable source-defined positive decision path. Eligibility did not depend on whether the local P value was significant. Units failing any prerequisite remained visible with a reason; no smaller post hoc denominator was created.

### Figure construction and validation

Figures 1–4 were regenerated from the V4-S4 source contract without statistical refitting. Each panel had a frozen source table, filter, required label and forbidden inference. Figures used a white background, colour-blind-safe palette, redundant text/position encoding, vector PDF/SVG output and 600-dpi PNG output. A semantic validator checked source hashes, row counts, stable identifiers, manuscript numerics, forbidden phrases, figure inventory and historical-label immutability.

### AI-assisted research and manuscript support

AI-assisted tools supported file comparison, code checking, document organization and language refinement under human review. Before submission, the authors must confirm the exact tool name, model or version, creator, access dates, specific research and writing uses, and the accountable human verification pathway: `[[AI_DISCLOSURE_PENDING]]`. No AI system qualifies as an author or replaces scientific accountability.

## Results

### A finite purposive study boundary

The historical lineage contains 28 purposively assembled candidates. Twenty-two form the core claim–estimand audit set, 15 have local numerical records, and those records contain 27 historical marker-by-treatment model rows. These are different counting units rather than a sequential screening flow (Fig. 1a; Table 1). Six partially recoverable candidates remained in lineage but were not promoted to the 22-object set. The sampling process was informed by known literature and data availability and cannot support a prevalence estimate for transcriptomic biomarkers as a field.

Each object retains a stable `claim_estimand_id`. Original use, claim polarity, source design, implementation, population, estimand compatibility and current role are separate fields (Fig. 1b and Fig. 2). No composite readiness score was calculated. Across the 22 objects, current roles were 10 population-unverified, seven role-reframed, two targeted-reanalysis, two not-currently-evaluable and one implementation-limited.

### Published response association, formal interaction and external validation were non-equivalent evidence layers

Fourteen objects originated as treatment-conditioned response or outcome associations (U1), whereas eight concerned differential treatment benefit (U2). The sources contained positive, negative, exploratory and mixed conclusions. A positive U1 result did not become U2 evidence merely because a later common interaction model was applied; similarly, a non-significant interaction did not prove biological irrelevance or equivalence. Figure 2 preserves use, claim polarity, fidelity, population and estimand as distinct dimensions.

The ten TRIO signatures illustrate this distinction. ESR1_DESMEDT supported a positive treatment-conditioned response association rather than an exact treatment-selection interaction. Five signatures had published negative response-association interpretations, and four were exploratory or lacked a signature-specific positive conclusion.[3] The historical application of a common interaction model therefore did not constitute ten attempts to replicate ten equivalent positive predictive claims.

Other source audits produced object-specific boundaries. CIN70 had a negative prespecified dichotomous evaluation for specific veliparib–carboplatin response while a continuous response association was described separately.[8] RevisedPARPi7 used an author-released score in a 105-participant expression/score subset, with five unknown outcomes leaving 100 model-complete rows.[9] The IMmotion150 publisher correction changed the Figure 2n top Myeloid comparison to combination therapy versus atezolizumab monotherapy; it did not rewrite Angio or Teff results.[10,11] JAVELIN and related renal-cell-carcinoma signatures remained aggregate/source-audit objects in this project.[12,13] GARD provided endpoint-specific pooled interaction evidence across heterogeneous cohorts rather than a single randomized trial,[14] and BCI had positive randomized-source interaction evidence although the simplified local ratio was not an executable reconstruction of the calibrated assay.[15,16]

### TRIO showed design-level partial identifiability without a corrected randomized interaction

The public TRIO linkage contained 110 unique rows: 31 in Arm 1, 29 in Arm 2 and 50 in Arm 3, with 15, seven and 25 pathologic complete responses, respectively. No raw randomized-phase field was present. Trial design identified Arms 1 and 2 as randomized-phase arms, whereas Arm 3 could include both direct-assignment and randomized participants. Thus, absence of a raw field did not make all 110 participants equally uncertain: Arms 1 and 2 were identifiable at the design level, but Arm 3 remained unresolved at the participant level.

The historical target comparison used Arm 1 (n=31) and all public Arm 3 records (n=50), with 40 responses. The report states that the first 20 participants were assigned directly to combined therapy and that 38 participants remained in the corresponding combined-treatment group after those participants were excluded.[3] Participant number and row order were not treated as phase labels. Under conditional integer constraints compatible with the public and reported aggregate counts, the randomized component of public Arm 3 could contain 30–38 participants and have a raw response proportion of 48.5–60.0% (Fig. 4c). This is a compatibility range, not a confidence interval, corrected treatment effect or marker-by-treatment interaction bound.

No pseudo-corrected TRIO model was fitted. The ten historical estimates remain available as computational history and scale sensitivity, but not as verified randomized treatment-effect-modification estimates. CHER-LOB remains a separate randomized-context analysis; loss of a verified TRIO anchor does not invalidate CHER-LOB within-trial calculations.[4]

### AVAglio separated population restriction from model adjustment

The AVAglio source and repository records supported a five-specification ladder for both Phillips and Verhaak proneural labels (Fig. 3). A0 used all 349 expression-evaluable participants; A1 excluded 10 IDH1-mutant tumours, leaving 339; A2 excluded a fixed six rows with a literal unavailable value in a required clinical covariate, leaving 333, but remained unadjusted; A3 applied the source-listed clinical adjustment on the same 333 rows; A4 used all 339 IDH1-wild-type rows with explicit missing levels and a fixed ridge penalty. The later erratum supplied an omitted repository link but did not alter the reported population or interaction result.[5,18]

On the shared 333-row set, the A2 unadjusted Phillips interaction was HR 0.612 (95% CI 0.355–1.056; P=0.0777), and the Verhaak interaction was HR 0.513 (0.296–0.891; P=0.0178) (Fig. 3b,c). The A3 adjusted estimates were HR 0.516 (0.292–0.912; P=0.0229) and HR 0.460 (0.261–0.811; P=0.00728), respectively. From A1 to A2, HR ratios were 0.980 and 0.990; from A2 to A3 on the same rows they were 0.843 and 0.896. In this dataset, the fixed six-row exclusion caused little movement, whereas clinical adjustment produced a larger numerical shift. These differences are descriptive specification sensitivity, not additive causal contributions, and crossing P=0.05 does not imply that two specifications differ significantly.

The A4 estimates were similar—HR 0.540 (0.311–0.940; P=0.0292) for Phillips and HR 0.480 (0.276–0.834; P=0.00926) for Verhaak—but A4 differs from A3 in population, missing-category handling and penalization. It is therefore displayed as an alternative branch rather than a fourth single-factor step (Fig. 3d). Source-deposited subtype labels were reused; the original NanoString centroid pipelines were not independently re-executed.[5] All AVAglio estimates are same-trial specification analyses, not independent validations.

### Historical cross-trial labels were separated from current verified eligibility

The historical replay retained all 13 units and their three dependency clusters: ten HER2 units sharing the TRIO–CHER-LOB pair, two glioblastoma units sharing AVAglio–GLARIUS, and one IGG14–BrighTNess unit (Fig. 4a). These units are not 13 independent replications. Historical membership and current verified-strict membership are now separate fields.

All ten HER2 units are descriptive because the TRIO anchor population is unresolved. The two glioblastoma units compare a reconstructed AVAglio anchor with a medium-transportability GLARIUS analysis rather than an exact replication.[6] The IGG14 analysis is dependent on a report already containing the BrighTNess resource.[7] No unit currently satisfies all prerequisites for a verified-strict denominator. The current strict proportion is therefore not estimable; neither `0/13`, `0/3` nor `0/0` is an authorized current replication rate (Fig. 4b).

### Absolute-effect sensitivities did not promote a primary label

All 23 historical binary absolute-effect rows were retained. Ten TRIO rows are population-unverified scale sensitivities; ten CHER-LOB rows remain standalone trial-specific sensitivities, with ESR1_DESMEDT retaining its historical technical warning because 4,736 of 5,000 bootstrap replicates were valid. The remaining three rows retain trial-specific source and implementation boundaries.

Stromal_FARMER was the sole nominal additive result: delta risk difference −0.360, 95% bootstrap interval −0.748 to −0.013, sign-tail P=0.0416 and within-family q=0.416. None of the 23 results was multiplicity robust. This nominal result arose from the assignment-unverified TRIO population and did not promote a frozen primary label (Fig. 4c; Supplementary Table S3).

## Discussion

This study separates two histories that biomarker reanalysis often collapses: what was computed and what the computation is allowed to mean. The distinction is empirical rather than semantic. TRIO yielded reproducible historical calculations, but its public Arm 3 records could not be partitioned into randomized and direct-assignment phases. AVAglio, by contrast, provided enough source information to reconstruct analysis populations and compare model specifications. One correction pathway changed inferential eligibility without changing historical numbers; the other changed numerical estimates under versioned, source-defined models (Fig. 1c).

The AVAglio ladder adds an important qualification to the earlier manuscript. The 333-row unadjusted A2 models isolate the effect of fixing the complete-case population from subsequent clinical adjustment. The small A1-to-A2 movement and larger A2-to-A3 movement show why population restriction and covariate adjustment should not be described as a single “corrected model” contrast. At the same time, nominal P values from five related specifications are not five independent confirmations and do not create external validation.

The same discipline applies to negative or uncertain results. A response association is not automatically a treatment-selection interaction; a non-significant interaction is not proof of no heterogeneity; an implementation-limited object is not a biomarker failure; and the absence of an eligible denominator is not a zero replication rate. The 23 absolute-effect sensitivities illustrate scale dependence, but their interpretation remains conditional on population and estimand validity.

This work has limitations. The object set is purposive and cannot estimate field prevalence. Historical results were visible before RPv4, so RPv4 is a versioned redesign and targeted-analysis addendum, not a retroactive preregistration. TRIO participant-level phase remains unrecoverable in public data. AVAglio reused deposited subtype labels rather than recreating the original centroid classifiers. A4 differs from A3 along more than one dimension. GLARIUS is not an exact transportability match. RCC_04 and RCC_05 remain not currently evaluable because provenance is open. Several clinical assays, including BCI, cannot be reconstructed from simplified public formulas. Author accountability, institutional ethics determination, repository release and journal-specific declarations remain unresolved.

The strength of the study is a versioned evidence chain in which source claim, implementation, population, estimand and current role remain separate. Historical rows are not deleted, results are not selected for significance, dependency clusters remain explicit, and every main figure is generated from frozen tables. The selected examples show why reproducible estimates are necessary but insufficient for defensible clinical inference.

## Conclusions

Computational reproducibility and defensible clinical inference require separate, versioned records. In this selected object set, source provenance, implementation, population identity and estimand alignment changed what historical results could support without deleting unfavourable results or creating a post hoc denominator. The practical output is an auditable evidence-alignment framework and two complementary correction pathways, not a field-wide biomarker failure rate.

## List of abbreviations

BH, Benjamini-Hochberg; CI, confidence interval; HR, hazard ratio; IDH1, isocitrate dehydrogenase 1; MGMT, O6-methylguanine-DNA methyltransferase; MMSE, Mini-Mental State Examination; pCR, pathologic complete response; RPA, recursive partitioning analysis; WHO, World Health Organization.

## Declarations

### Ethics approval and consent to participate

This retrospective secondary study used published evidence and public de-identified resources. The original studies reported their ethics and consent procedures. The institution-specific determination for the present secondary analysis must be supplied by the responsible author: `[[ETHICS_DETERMINATION_PENDING]]`.

### Consent for publication

`[[CONSENT_FOR_PUBLICATION_PENDING]]`

### Availability of data and materials

The disclosure-safe derived tables, provenance records, code and manifests are prepared for release; restricted participant-level inputs are not redistributed. The authors must approve the public repository, archived DOI, licence and any access restrictions: `[[DATA_CODE_REPOSITORY_PENDING]]`.

### Competing interests

`[[COMPETING_INTERESTS_PENDING]]`

### Funding

`[[FUNDING_PENDING]]`

### Authors contributions

`[[CREDIT_PENDING]]`

### Acknowledgements

`[[ACKNOWLEDGEMENTS_PENDING]]`

## References

1. Mandrekar, S. J. & Sargent, D. J. Clinical trial designs for predictive biomarker validation: one size does not fit all. *J. Biopharm. Stat.* **19**, 530–542 (2009). https://doi.org/10.1080/10543400902802458
2. Renfro, L. A. et al. Clinical trial designs incorporating predictive biomarkers. *Cancer Treat. Rev.* **43**, 74–82 (2016). https://doi.org/10.1016/j.ctrv.2015.12.008
3. Hurvitz, S. A. et al. Pathologic and molecular responses to neoadjuvant trastuzumab and/or lapatinib from a phase II randomized trial in HER2-positive breast cancer (TRIO-US B07). *Nat. Commun.* **11**, 5824 (2020). https://doi.org/10.1038/s41467-020-19494-2
4. Guarneri, V. et al. Prospective biomarker analysis of the randomized CHER-LOB study evaluating dual anti-HER2 treatment with trastuzumab and lapatinib plus chemotherapy as neoadjuvant therapy for HER2-positive breast cancer. *Oncologist* **20**, 1001–1010 (2015). https://doi.org/10.1634/theoncologist.2015-0138
5. Sandmann, T. et al. Patients with proneural glioblastoma may derive overall survival benefit from the addition of bevacizumab to first-line radiotherapy and temozolomide: retrospective analysis of the AVAglio trial. *J. Clin. Oncol.* **33**, 2735–2744 (2015). https://doi.org/10.1200/JCO.2015.61.5005
6. Weller, J. et al. The proneural subtype is not associated with survival benefit from bevacizumab in newly diagnosed glioblastoma: a secondary analysis of the GLARIUS trial. *J. Neurooncol.* **164**, 749–755 (2023). https://doi.org/10.1007/s11060-023-04470-9
7. Conte, B. et al. A 14-gene B-cell immune signature in early-stage triple-negative breast cancer: a pooled analysis of seven studies. *EBioMedicine* **102**, 105043 (2024). https://doi.org/10.1016/j.ebiom.2024.105043
8. Wolf, D. M. et al. DNA repair deficiency biomarkers and the 70-gene ultra-high-risk signature as predictors of veliparib/carboplatin response in the I-SPY 2 breast cancer trial. *npj Breast Cancer* **3**, 31 (2017). https://doi.org/10.1038/s41523-017-0025-7
9. Pusztai, L. et al. Durvalumab with olaparib and paclitaxel for high-risk HER2-negative stage II/III breast cancer: results from the adaptively randomized I-SPY2 trial. *Cancer Cell* **39**, 989–998.e5 (2021). https://doi.org/10.1016/j.ccell.2021.05.009
10. McDermott, D. F. et al. Clinical activity and molecular correlates of response to atezolizumab alone or in combination with bevacizumab versus sunitinib in renal cell carcinoma. *Nat. Med.* **24**, 749–757 (2018). https://doi.org/10.1038/s41591-018-0053-3
11. McDermott, D. F. et al. Publisher Correction: Clinical activity and molecular correlates of response to atezolizumab alone or in combination with bevacizumab versus sunitinib in renal cell carcinoma. *Nat. Med.* **24**, 1941 (2018). https://doi.org/10.1038/s41591-018-0235-z
12. Motzer, R. J. et al. Avelumab plus axitinib versus sunitinib in advanced renal cell carcinoma: biomarker analysis of the phase 3 JAVELIN Renal 101 trial. *Nat. Med.* **26**, 1733–1741 (2020). https://doi.org/10.1038/s41591-020-1044-8
13. Braun, D. A. et al. Interplay of somatic alterations and immune infiltration modulates response to PD-1 blockade in advanced clear cell renal cell carcinoma. *Nat. Med.* **26**, 909–918 (2020). https://doi.org/10.1038/s41591-020-0839-y
14. Scott, J. G. et al. Pan-cancer prediction of radiotherapy benefit using genomic-adjusted radiation dose (GARD): a cohort-based pooled analysis. *Lancet Oncol.* **22**, 1221–1229 (2021). https://doi.org/10.1016/S1470-2045(21)00347-8
15. Sgroi, D. C. et al. Prediction of late disease recurrence and extended adjuvant letrozole benefit by the HOXB13/IL17BR biomarker. *J. Natl Cancer Inst.* **105**, 1036–1042 (2013). https://doi.org/10.1093/jnci/djt146
16. Bartlett, J. M. S. et al. Breast Cancer Index and prediction of benefit from extended endocrine therapy in breast cancer patients treated in the Adjuvant Tamoxifen—To Offer More? trial. *Ann. Oncol.* **30**, 1776–1783 (2019). https://doi.org/10.1093/annonc/mdz289
17. Vivot, A. et al. Evidence for treatment-by-biomarker interaction for FDA-approved oncology drugs with required pharmacogenomic biomarker testing. *Sci. Rep.* **7**, 6882 (2017). https://doi.org/10.1038/s41598-017-07358-7
18. Sandmann, T. et al. Erratum: Patients with proneural glioblastoma may derive overall survival benefit from the addition of bevacizumab to first-line radiotherapy and temozolomide: retrospective analysis of the AVAglio trial. *J. Clin. Oncol.* **34**, 3113 (2016). https://doi.org/10.1200/JCO.2016.69.6674

## Figure legends

**Figure 1 | Finite study boundary and two correction pathways.** **a,** The 28 historical candidates, 22 claim–estimand objects, 15 local-numeric objects and 27 historical model rows are different units; the arrangement is not a PRISMA flow. **b,** Published claim, source evidence, implementation, population, estimand and current role remain separate. **c,** TRIO and AVAglio represent inferential qualification and numerical reconstruction, respectively.

**Figure 2 | Claim–estimand alignment across 22 frozen objects.** Rows show original use, claim polarity, implementation fidelity, population evidence, estimand compatibility and current role. Colours and abbreviations represent categories, not a composite score. Historical formula status does not imply current randomized eligibility.

**Figure 3 | AVAglio population and model-specification ladder.** **a,** Source-defined analysis populations and events. **b,c,** Phillips and Verhaak A0–A3 interaction hazard ratios with 95% confidence intervals; A2 is unadjusted on the fixed 333 rows and A3 is adjusted on the same rows. **d,** A4 is an alternative 339-row ridge specification with explicit missing levels and is not a single-factor continuation after A3. All panels reuse source-deposited subtype labels and do not constitute independent validation.

**Figure 4 | Historical replay and current evidentiary eligibility.** **a,** Thirteen historical units are grouped into three dependency clusters. **b,** Historical denominator membership is retained while current verified-strict membership is zero; the current strict proportion is not estimable. **c,** Twenty-three absolute-effect sensitivities produced one nominal and no multiplicity-robust result; the separate TRIO range is an aggregate compatibility constraint, not a confidence interval or interaction bound.

## Table and additional file legends

**Table 1 | Claim–estimand summary for 22 frozen objects.** Original use, claim polarity, implementation fidelity, population status, estimand compatibility and current role. The set is purposive and not a prevalence denominator.

**Supplementary Table S1 | AVAglio A0–A4 model ladder.** Snapshot and current fields remain versioned; A2 and A3 use the same fixed 333 rows but different adjustment.

**Supplementary Table S2 | Historical and current cross-trial eligibility for 13 units.** Historical labels, dependency clusters and current verified-strict status are displayed together without constructing a new denominator.

**Supplementary Table S3 | Binary absolute-effect sensitivities for 23 model rows.** Historical estimates and diagnostics are retained with a V4-S5 current role; no primary label is changed.
