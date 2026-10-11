# R5B-A1R scientific hierarchy freeze v1.0

**Freeze date:** 13 September 2026  
**Applies to:** R5B systematic/scoping outer frame and the nested frozen R5A randomized-trial benchmark  
**Machine status:** `A1R2_MACHINE_REFRAME_AND_EFFECT_SCALE_PASS__READY_FOR_FRESH_A1H_SIGNOFF__NO_GO_FINAL_SEARCH__HOLD_SUBMISSION`

## Frozen thesis

Published transcriptomic claims intended to inform oncology treatment selection must be evaluated as a linked evidence chain: claim wording, original evidence design, formula executability and implementation fidelity, randomized treatment-comparison opportunity, estimand compatibility, lawful data access, independent evaluation and interval-supported treatment-effect modification. Biological relevance, treated-arm response association, prognostic association and directional concordance cannot substitute for this chain.

## Frozen working title

**Evidence alignment and randomized reproducibility of transcriptomic treatment-selection biomarkers in oncology**

The former title, *Randomized trial reproducibility of published transcriptomic treatment biomarkers across cancers*, is retired as the top-level title because it makes a purposive, clustered nested benchmark appear field-wide.

## Scientific hierarchy

### Outer-primary study

A protocol-governed systematic scoping review and evidence/estimand audit will estimate and display the structure of eligible treatment-selection claims across three domains:

1. **Claim/evidence alignment** — claim wording, original evidence class and whether a formal comparative treatment-by-biomarker interaction was reported.
2. **Executability/evaluability** — formula and feature recoverability, implementation fidelity, randomized opportunity, estimand compatibility and lawful data path.
3. **Validation maturity** — independent evaluation and interval-supported evidence.

The unit of analysis is `claim_estimand_id`. Reports, datasets, implementations and claim-estimands remain separate entities joined by explicit identifiers. No composite readiness score will be calculated.

### Nested-secondary study

R5A is retained intact as a frozen empirical benchmark among the subset of claims for which a lawful and sufficiently compatible randomized or controlled evaluation could be executed. Its 27 primary marker-by-treatment models, 15 local claims, treatment contrasts, outcomes, marker definitions, analysis rows, multiplicity families, strict denominator and adjudication labels remain immutable.

The nested benchmark answers what happens after a claim crosses enough of the evidence chain to permit controlled re-execution. It does not estimate a field-wide replication proportion.

## Metric hierarchy

The binding registry is `primary_metric_registry_v0.6.tsv`.

- PM01–PM02 are outer-primary Domain A metrics.
- PM03–PM06 are outer-primary Domain B metrics.
- PM07 is the outer-primary Domain C metric.
- PM08 is supporting reporting-quality context, not a co-primary endpoint.
- PM09 is the bridge into the nested R5A benchmark, not a prevalence endpoint.

All proportions use the denominator written in the metric registry. Missingness is displayed explicitly; it is not silently removed to improve apparent readiness.

## Implementation-fidelity axis

Implementation fidelity is frozen as an independent axis under `implementation_fidelity_taxonomy_v0.1`:

- F0: exact original executable implementation;
- F1: platform-bridged implementation preserving the published mathematical function;
- F2: source-compatible approximation with declared deviations;
- F3: partial implementation or material missing component;
- F4: non-executable from available information.

Fidelity is not ordered into an outcome-derived score and cannot be inferred from a positive association.

## Effect-scale hierarchy

The 23 binary logistic marker-by-treatment interactions remain the frozen primary binary estimands. The additive-risk analysis is a prespecified sensitivity under `binary_effect_scale_sensitivity_SOP_v1.0`:

`ΔRD = [P(Y=1|T=1,Q75) - P(Y=1|T=0,Q75)] - [P(Y=1|T=1,Q25) - P(Y=1|T=0,Q25)]`.

Q25 and Q75 are frozen once on each original analytic sample. Randomized-arm-stratified bootstrap resampling does not re-estimate quantiles or re-standardize markers. An additive-only result is `scale-dependent uncertainty`; it cannot relabel a frozen primary result as replicated.

## Prospective redesign boundary

This hierarchy was frozen before A1G01 scientific sign-off, OSF registration and formal multi-database search. It is therefore a prospective redesign of the planned outer study, not an outcome-driven amendment to an active registered review.

The redesign did **not** change:

- R5A eligibility or search history;
- any biomarker formula, orientation or cutpoint;
- any treatment contrast or endpoint;
- any participant row or exclusion;
- any primary model or coefficient;
- any multiplicity family;
- the historical strict denominator or its dependency clusters;
- any frozen label.

The observed R5A results did motivate a more accurate hierarchy and an additive-scale sensitivity. They did not determine which claims or results were retained.

## Interpretation locks

Permitted:

- “No multiplicity-robust evidence was observed in the frozen nested benchmark.”
- “Clinically relevant treatment-effect heterogeneity remained unresolved in imprecise subsets.”
- “One additive-scale nominal result was observed but did not survive its frozen family correction.”
- “The 13 historical label replays comprised three dependency clusters; 12 of 13 units arose from two clusters.”

Prohibited:

- “The biomarkers failed.”
- “Transcriptomic biomarkers do not predict treatment benefit.”
- treating 0/13 as 13 statistically independent replications;
- calling an additive-only nominal result replication;
- filling outer-primary counts before registered A2 screening;
- ranking biomarkers with an arbitrary readiness composite.

## Governance and release

This machine freeze does not authorize formal search or submission. The next authorized phase is fresh human-governed sign-off on this exact hierarchy, protocol v0.7, metric registry v0.6, fidelity taxonomy v0.1, templates v0.8, absolute-effect SOP v1.0 and their hashes. A2 may begin only after all human and machine gates produce the exact semantic release state `READY_FOR_A2_RELEASE`.
