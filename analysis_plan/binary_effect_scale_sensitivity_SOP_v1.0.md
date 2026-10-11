# Binary-outcome absolute-effect sensitivity SOP v1.0

**Phase:** R5B-A1R2 formal scientific reframe  
**Freeze date:** 13 September 2026 (Asia/Hong_Kong)  
**Status:** `FROZEN_BEFORE_FULL_23_MODEL_RUN`  
**Role:** key robustness sensitivity nested beneath the immutable 23 frozen logistic primary models

## 1. Scientific purpose and hierarchy

The frozen binary primary analyses test marker-by-treatment interaction on the log-odds scale. Because effect modification is scale dependent, those models do not by themselves determine whether absolute treatment benefit varies across marker values. This sensitivity adds an absolute-risk estimand without replacing, relabelling or selecting among the frozen primary results.

The hierarchy is fixed as:

1. **Nested benchmark primary:** the existing logistic marker + treatment + marker×treatment model, treatment contrast, analytic rows, marker orientation, endpoint, multiplicity family and frozen label.
2. **Key robustness sensitivity:** logistic-model g-computation of absolute-risk treatment-benefit heterogeneity.
3. **Diagnostic only:** an HC3 linear-probability interaction expressed across the same Q25–Q75 marker contrast.

No additive-scale result can promote a claim to replicated or alter outer-review eligibility, denominator membership, evidence class or implementation-fidelity class.

## 2. Included models and outcome orientation

All 23 frozen binary pCR models are included:

- TRIO-US B07: 10 frozen HER2 signatures;
- CHER-LOB: the same 10 frozen HER2 signatures;
- BrighTNess B versus C: IGG14;
- BrighTNess A versus C: CIN70;
- I-SPY2 DOP/GSE173839: revisedPARPi7_FFPE.

For every model, `Y=1` denotes pCR and is favourable. `T=1` is the experimental treatment exactly as frozen. Therefore, a positive risk difference denotes higher predicted pCR under the experimental treatment, and a positive ΔRD denotes a larger absolute experimental-treatment benefit at the higher marker value.

## 3. Frozen analytic inputs

For each trial×claim model:

- reconstruct exactly the frozen complete-case rows from the hash-verified source files;
- retain the frozen treatment coding, endpoint coding, marker formula, marker orientation and standardization convention;
- refit the same unadjusted logistic model `Y ~ 1 + T + M + T×M` only to verify the frozen point estimate;
- require model count, sample size, event count, interaction coefficient and interaction P value to reconcile to the frozen source table within `1e-8` absolute tolerance;
- do not use outcome-driven exclusions, cutpoints, sign flips, endpoint substitutions, covariate selection or model selection.

All input paths, byte counts and SHA-256 hashes are recorded before computation. Participant-level inputs are read in place and are not redistributed in the release package.

## 4. Marker contrast

All 23 included markers are continuous. Let `M` be the already frozen standardized marker.

- Calculate pooled-analytic-sample Q25 and Q75 once from the original frozen rows using the linear interpolation definition used by NumPy `quantile(method="linear")`, equivalent to R quantile type 7.
- Freeze those two numerical values before resampling.
- Do not restandardize the marker and do not recompute either quantile inside a bootstrap replicate.

If a future model uses an intrinsically categorical marker, it requires a prospective amendment specifying the category contrast; sample-derived quantiles must not be invented for it.

## 5. Absolute-risk estimand

Fit the frozen logistic model and obtain its coefficient vector. At marker value `m`, calculate:

`risk(t,m) = expit(β0 + βT t + βM m + βTM t m)`

`RD(m) = risk(1,m) - risk(0,m)`

The additive effect-modification estimand is:

`ΔRD = RD(Q75) - RD(Q25)`

Report `risk(0,m)`, `risk(1,m)` and `RD(m)` at both marker values, followed by ΔRD. Values are proportions; percentage-point displays multiply them by 100 without changing the stored estimand.

No pooled effect is calculated across trials, signatures, cancer contexts or treatment contrasts.

## 6. Bootstrap uncertainty

- Run 5,000 nonparametric replicates per model.
- Resample participants with replacement separately within each frozen randomized treatment arm, preserving both arm sizes.
- Refit the same four-parameter logistic model in each replicate.
- Evaluate ΔRD at the fixed original-sample Q25 and Q75.
- Use a deterministic model-specific seed derived from phase seed `20260913`, trial and claim ID; model order must not change a model's random stream.
- Report the 2.5th and 97.5th percentiles of valid replicate ΔRD values.
- Define the two-sided bootstrap sign-tail P value as `2 × min[(1+n(ΔRD≤0))/(1+Bvalid), (1+n(ΔRD≥0))/(1+Bvalid)]`, capped at 1.

A replicate is invalid if the logistic fit does not converge, yields non-finite coefficients/predictions, has rank below four, or produces a non-finite ΔRD. Invalid replicates are never silently replaced by zero or by a penalized estimate.

Convergence status is classified prospectively:

- `PASS`: at least 4,750 valid replicates (≥95%);
- `WARN_CONDITIONAL_PERCENTILE`: 4,500–4,749 valid replicates (90% to <95%); report the conditional percentile interval with a warning;
- `NON_ESTIMABLE_BOOTSTRAP`: fewer than 4,500 valid replicates; retain the point estimate but do not report a confirmatory interval or multiplicity label.

The number and percentage of invalid replicates are reported for every model.

## 7. Multiplicity families

The absolute-scale sensitivity uses the same trial/contrast families as the frozen binary benchmark:

1. `HER2_TRIO_B07_DUAL_VS_SINGLE` (10 signatures);
2. `HER2_CHERLOB_DUAL_VS_SINGLE` (10 signatures);
3. `TNBC_BRIGHTNESS_IGG14_B_VS_C` (one model);
4. `TNBC_BRIGHTNESS_CIN70_A_VS_C` (one model);
5. `TNBC_DOP_PARPI_IO_VS_CONTROL` (one model).

Apply Benjamini–Hochberg adjustment to the bootstrap sign-tail P values within each family. Single-model family q values equal their P values. The resulting q values are sensitivity labels and do not replace frozen primary q values.

## 8. Diagnostic linear-probability check

Fit `Y ~ 1 + T + M + T×M` by ordinary least squares with HC3 standard errors. Express the interaction across the frozen Q25–Q75 range as `βTM × (Q75-Q25)`, with its transformed Wald interval and P value. This diagnostic is used only to detect coding or sign inconsistencies. It is not used to select the logistic or additive result.

## 9. Interpretation rule

- An additive result is nominal only when its valid percentile CI excludes zero and bootstrap sign-tail P<0.05.
- It is multiplicity-robust only when the preceding conditions hold and its within-family BH q<0.05.
- An additive-only nominal or multiplicity-robust result is labelled **scale-dependent uncertainty**. It is never labelled replication, validation, rescue or proof of treatment selection.
- Lack of significance on both scales is reported as **no multiplicity-robust evidence observed; uncertainty remains**, not equivalence or proof of no effect.
- Wide intervals and bootstrap instability remain visible.

## 10. Deterministic replay and release gate

The complete 5,000-replicate analysis is run twice with the same versioned script, input hashes, environment and seeds. For each model, the ordered validity mask and valid ΔRD vector are hashed. A model passes replay only if both runs have identical hashes and identical summary values. The full sensitivity is complete only if:

- 23/23 frozen row identities and primary estimates reconcile;
- every model has an absolute-risk point estimate and either a valid interval or an explicit non-estimability reason;
- 23/23 deterministic replay digests match;
- within-family BH values are generated only for estimable models;
- the claim-level scale-concordance table preserves the frozen primary labels;
- no frozen primary file is overwritten.

