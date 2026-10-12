# V4-S2 diagnostic addendum v1.0

**Frozen before first A2 fit:** 2026-10-11 (Asia/Hong_Kong)  
**Scope:** diagnostic terminology and reporting only  
**Scientific model affected:** none

## Primary A2 model

For each deposited proneural classifier, fit on the same frozen 333-row set:

`Surv(OS_months, OS_event) ~ marker + treatment + marker:treatment`

- treatment: bevacizumab = 1, placebo = 0;
- marker: proneural = 1, all other deposited subtype labels = 0;
- ties: Efron;
- no clinical covariates;
- no penalty;
- no result-dependent row deletion.

The 333-row set is the 339-row IDH1-wild-type set after the prospectively frozen six-row literal-`NA` source-covariate availability exclusion. Deposited `MGMT = Missing` remains an explicit source category and is not an exclusion criterion.

## Pre-fit estimability checks

For each classifier, record before interpreting the fit:

1. sample and event counts in every treatment × marker cell;
2. rank and condition number of the marker/treatment/interaction design matrix;
3. presence of both treatment arms and both marker classes;
4. completeness and coding of OS duration and event.

Failure of rank or the frozen row/event contract stops the relevant fit. Sparse cells are reported, not silently repaired.

## Proportional-hazards diagnostics

Report covariate-specific and global Schoenfeld residual tests using R `survival::cox.zph(transform = "rank")`. Lifelines rank-transform proportional-hazards tests are retained as implementation cross-checks. Diagnostic P values do not replace the prespecified interaction test and do not trigger an alternative primary model in V4-S2.

## Influence diagnostics

The common `2/sqrt(n)` screening threshold applies to standardized **DFBETAS**, not to coefficient-scale DFBETA values.

- retain coefficient-scale DFBETA;
- retain standardized DFBETAS;
- apply `2/sqrt(333)` only to `abs(DFBETAS)`;
- report the maximum absolute value and count above threshold for every coefficient;
- keep the five largest interaction DFBETAS records in a local restricted file;
- do not delete or refit after identifying an influential observation.

The threshold is an exploratory influence flag, not a statistical rejection threshold.

## Interpretation lock

A2 is a same-trial model-specification bridge. A significant or non-significant A2 interaction cannot be called an independent validation, cannot change the historical primary label, and cannot alter the frozen 22-object corpus.

