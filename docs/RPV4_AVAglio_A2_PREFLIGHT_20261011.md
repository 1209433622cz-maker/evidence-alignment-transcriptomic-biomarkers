# RPV4 AVAglio A2 execution preflight

## Outcome

**READY_FOR_V4_S2_EXECUTION**

- Input SHA-256: `7d561840758f9a7ea2e897c05789f0414255f008698fc538add1219d9083d707`
- Lineage: 349 expression-evaluable → 339 IDH1-WT → 333 frozen A2 rows.
- A2 events: 260.
- Excluded unique rows: 6; literal-NA counts by covariate: `{'age': 0, 'corticosteroids': 1, 'surgical_status': 2, 'sex': 0, 'kps': 0, 'mgmt_status': 0, 'mmse': 3, 'rpa_class': 2, 'who': 2}`.
- MGMT `Missing` category retained: 68 rows.
- Model fitted in this stage: **NO**.
- Effect estimates generated in this stage: **NO**.

## Important definition correction

The 333-row set is defined by a version-specific literal-`NA` source-covariate availability rule. It is not described as a universal conventional complete-case set because the deposited MGMT `Missing` category remains an explicit level. This wording prevents an overclaim without changing the previously selected 333 rows.

## Execution lock

A2 must use the A0 unadjusted formula on the frozen 333 rows for both classifiers. A2 must not acquire source covariates, ridge penalty, a different missing-data rule or a result-dependent participant deletion. All effect estimates and diagnostics must be written only to a new V4-S2 directory.

## Checklist

| check_id | criterion | pass | evidence |
| --- | --- | --- | --- |
| P01 | Raw input is frozen | PASS | Expected Q2-R3 SHA-256 |
| P02 | Expression-evaluable row count | PASS | observed=349 |
| P03 | IDH1-WT row count | PASS | observed=339 |
| P04 | Fixed literal-NA exclusion count | PASS | observed=6 |
| P05 | A2 row count | PASS | observed=333 |
| P06 | A2 event count | PASS | observed=260 |
| P07 | Both treatment arms retained | PASS | {'Placebo': 171, 'Bevacizumab': 162} |
| P08 | Both Phillips classes retained | PASS | binary marker derivable |
| P09 | Both Verhaak classes retained | PASS | binary marker derivable |
| P10 | OS duration and event complete | PASS | time in months; event 1, censor 0 |
| P11 | A2 model fixed to A0 formula | PASS | duration + event + marker + treatment + marker×treatment; no covariates |
| P12 | A2 output cells remain empty | PASS | enforced in model registry and QA |
| P13 | Diagnostics frozen before execution | PASS | convergence; finite estimates; Schoenfeld PH; interaction DFBETA \|x\|>2/sqrt(n) plus top five |
| P14 | No outcome-driven extension | PASS | all results reported; no sample/covariate substitution after viewing result |
