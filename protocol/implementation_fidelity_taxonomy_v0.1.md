# Implementation-fidelity taxonomy v0.1

**Status:** frozen candidate for fresh A1H review  
**Date:** 13 September 2026  
**Unit:** biomarker implementation mapped to a `claim_estimand_id` and `trial_dataset_id`

## Purpose

Formula availability and implementation fidelity are related but distinct. A formula may be fully described yet not executable on a target platform, while a source-compatible score may be executable but differ from the original clinical assay. Fidelity is charted to qualify interpretation; it does not determine outer eligibility and cannot be changed after outcomes are viewed.

## Required component audit

Each implementation is assessed on:

- feature/gene identity and completeness;
- weights or coefficient vector;
- transformation and normalization reference;
- aggregation or model rule;
- score orientation;
- cutpoint or category rule, when the claim uses one;
- platform, probe/transcript mapping and alias resolution;
- missing features and prespecified handling;
- bridge rationale and versioned code;
- expected effect on patient ranking or classification;
- independent verification and adjudication status.

Unknown components remain explicit. Absence is never converted to agreement.

## Classes

### F0 — `EXACT_EXECUTABLE_ORIGINAL`

All claim-defining components are available and the original assay or a computationally identical implementation can be executed on the target data without altering feature identity, weights, normalization, orientation, aggregation or cutpoint. Numerical equivalence must be demonstrated when an original reference output is available.

### F1 — `PRESPECIFIED_PLATFORM_BRIDGED_EXACT_FUNCTION`

The mathematical biomarker function is preserved, but a prospectively specified platform bridge is required, such as a documented probe-to-gene or transcript-to-gene mapping. No outcome-informed mapping is allowed. The bridge must preserve all required features and the same weights, orientation, aggregation and cutpoint. Any material ranking or classification change prevents F1.

### F2 — `SOURCE_COMPATIBLE_APPROXIMATION`

The implementation follows the source concept and a documented, outcome-blind reconstruction rule, but one or more claim-defining elements cannot be reproduced exactly. Examples include a subset mean when some signature genes are unavailable, an alternative normalization reference, or an author-released compatible score whose exact clinical-assay transformation is unavailable. F2 is executable evidence but is not the original assay.

### F3 — `PARTIAL_OR_MISSING_COMPONENT`

The report identifies the biomarker, but missing features, weights, normalization, orientation, cutpoint or platform information prevents a prespecified implementation that adequately represents the claim. Exploratory approximations may be logged separately but cannot enter the frozen nested benchmark without a prospective amendment.

### F4 — `NONEXECUTABLE`

The biomarker is proprietary, unavailable, internally contradictory or insufficiently specified such that no lawful and auditable implementation can be produced from the available material.

## Decision order

1. Confirm the claim-specific biomarker definition and version.
2. Audit every required component without viewing the evaluation outcome.
3. Test exact identity/equivalence for F0.
4. If only platform mapping differs, test the prespecified F1 criteria.
5. If an auditable but inexact reconstruction exists, assign F2 and document every divergence.
6. Otherwise assign F3 or F4 according to whether partial technical information exists.
7. Require independent field-by-field verification; unresolved disagreement is `INDETERMINATE` and not forced into F0–F4.

## Interpretation constraints

- F0/F1 does not prove clinical validity.
- F2 does not prove failure of the original assay when an interaction is null or imprecise.
- F3/F4 is an evaluability limitation, not evidence that the biological concept is false.
- Fidelity class does not alter systematic eligibility, evidence class, denominator, marker orientation, endpoint or treatment contrast.
- No weighted fidelity score or rank is calculated.

