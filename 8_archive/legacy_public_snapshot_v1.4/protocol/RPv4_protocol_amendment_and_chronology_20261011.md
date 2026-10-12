# RPV4 protocol amendment and chronology

**Effective date:** 2026-10-11
**Parent protocol:** `QiTeng_EvidenceAlignment_RPv4_Full_Research_Proposal_20261010.md` (`c0949d021116d2f11d7f74dedd8394e3c9f963594753a4e23f76a8ef76ba6671`)
**Purpose:** freeze the historical baseline, the 22-object role transition and the AVAglio A0–A4 ladder before any A2 model fit.

## Chronology

1. R5/Q2 historical analyses produced 27 interaction models, 23 absolute-effect models and 13 descriptive cross-trial units.
2. Q2-R1/R2 adjudicated TRIO allocation as unverified at row level and propagated the interpretation change without deleting historical numbers.
3. Q2-R3/R3A audited sources and ran AVAglio A0/A1/A3/A4 analyses; A2 was not run.
4. Q2-R4/R5 integrated the finite 22-object manuscript baseline.
5. RPv4 was written on 2026-10-10 and approved for continuation by the research owner on 2026-10-11.
6. This S0/S1 freeze was generated before A2 fitting. A2 contains no coefficient, HR, CI or P value in any current file.

## Prospective amendment

- Keep the 22-object set unchanged.
- Make role transition, not a new positive biomarker, the primary descriptive result.
- Add only A2: the A0 unadjusted Cox interaction formula applied to the already defined 333-row AVAglio set.
- Treat A2 and any diagnostic P values as a new exploratory family. Report both classifiers and every prespecified diagnostic.
- Do not modify historical A0/A1/A3/A4 results or primary labels.
- Do not infer TRIO assignment phase from public numeric identifiers or sample order.

## Frozen A2 rules

Population: IDH1-WT records after the fixed six-row literal-`NA` source-covariate availability exclusion. The deposited MGMT `Missing` category is retained.
Formula: `OS ~ marker + treatment + marker×treatment`, separately for Phillips and Verhaak deposited subtype labels.
Direction: event=1, censor=0; time in months; treatment=1 bevacizumab, 0 placebo; marker=1 proneural.
Diagnostics: convergence, finite estimates, Schoenfeld PH tests, interaction DFBETA flags `|DFBETA| > 2/sqrt(n)` plus top five.
Stopping: if input identity, n=333, events=260, treatment coding or endpoint coding fails, do not fit; report the reason.

## Scientific boundary

This amendment does not make the work prospective or preregistered. It is a dated, result-preserving amendment for an exploratory retrospective methods study. GitHub publication and manuscript submission remain on hold.
