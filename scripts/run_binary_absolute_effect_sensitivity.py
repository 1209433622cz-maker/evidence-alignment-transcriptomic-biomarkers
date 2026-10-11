#!/usr/bin/env python3
"""Run the prespecified 23-model absolute-risk sensitivity without mutating R5A.

The participant-level designs are reconstructed with the versioned R5A loader.
Only aggregate model and bootstrap outputs are written to the A1R2 directory.
The public repository does not redistribute participant-level inputs; supply a
lawfully populated workspace explicitly with --workspace.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import math
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np
import pandas as pd
import scipy
import statsmodels
import statsmodels.api as sm
from scipy.special import expit
from statsmodels.stats.multitest import multipletests


PHASE_SEED = 20260913
EXPECTED_MODELS = 23
DEFAULT_REPLICATES = 5000
RECONCILIATION_TOLERANCE = 1e-8


@dataclass(frozen=True)
class BootstrapResult:
    delta: np.ndarray
    valid: np.ndarray
    reason: np.ndarray
    digest: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workspace",
        type=Path,
        required=True,
        help="Workspace containing lawfully obtained source data and the R5A frozen loader.",
    )
    parser.add_argument(
        "--phase",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Output phase/repository root (default: repository root).",
    )
    parser.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES)
    parser.add_argument("--skip-replay", action="store_true")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_seed(*parts: object) -> int:
    text = "|".join(str(part) for part in parts)
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def write_tsv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, sep="\t", index=False, na_rep="", lineterminator="\n")


def load_r5a_module(workspace: Path):
    path = workspace / "R5A_RP_ReviewerProofRobustness_20260909/scripts/run_r5a_reviewerproof.py"
    spec = importlib.util.spec_from_file_location("r5a_frozen_loader", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load R5A module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, path


def multiplicity_family(trial: str, claim_id: str) -> str:
    if trial == "TRIO-US B07":
        return "HER2_TRIO_B07_DUAL_VS_SINGLE"
    if trial == "CHER-LOB":
        return "HER2_CHERLOB_DUAL_VS_SINGLE"
    if trial == "BrighTNess" and claim_id == "TNBC_01":
        return "TNBC_BRIGHTNESS_IGG14_B_VS_C"
    if trial == "BrighTNess" and claim_id == "TNBC_04":
        return "TNBC_BRIGHTNESS_CIN70_A_VS_C"
    if trial == "I-SPY2 DOP / GSE173839" and claim_id == "TNBC_03":
        return "TNBC_DOP_PARPI_IO_VS_CONTROL"
    raise ValueError(f"unmapped binary multiplicity family: {trial} / {claim_id}")


def logistic_loglik(y: np.ndarray, x: np.ndarray, beta: np.ndarray) -> float:
    eta = x @ beta
    return float(np.sum(y * eta - np.logaddexp(0.0, eta)))


def fit_logistic_irls(
    y: np.ndarray,
    x: np.ndarray,
    start: np.ndarray,
    max_iter: int = 100,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray | None, str]:
    if x.shape[1] != 4 or np.linalg.matrix_rank(x) < 4:
        return None, "RANK_DEFICIENT"
    beta = np.asarray(start, dtype=float).copy()
    if beta.shape != (4,) or not np.isfinite(beta).all():
        beta = np.zeros(4, dtype=float)
    current_ll = logistic_loglik(y, x, beta)
    for _ in range(max_iter):
        eta = np.clip(x @ beta, -40.0, 40.0)
        mu = expit(eta)
        weight = np.clip(mu * (1.0 - mu), 1e-12, None)
        info = x.T @ (weight[:, None] * x)
        score = x.T @ (y - mu)
        try:
            step = np.linalg.solve(info, score)
        except np.linalg.LinAlgError:
            return None, "SINGULAR_INFORMATION"
        if not np.isfinite(step).all():
            return None, "NONFINITE_STEP"
        alpha = 1.0
        accepted = False
        for _ in range(20):
            candidate = beta + alpha * step
            candidate_ll = logistic_loglik(y, x, candidate)
            if np.isfinite(candidate_ll) and candidate_ll >= current_ll - 1e-10:
                accepted = True
                break
            alpha *= 0.5
        if not accepted:
            return None, "LINE_SEARCH_FAILED"
        beta = candidate
        current_ll = candidate_ll
        if not np.isfinite(beta).all():
            return None, "NONFINITE_COEFFICIENT"
        if np.max(np.abs(alpha * step)) < tolerance:
            return beta, "VALID"
        if np.max(np.abs(beta)) > 50.0:
            return None, "DIVERGENT_SEPARATION"
    return None, "NONCONVERGED"


def risks_from_beta(beta: np.ndarray, marker_value: float) -> tuple[float, float, float]:
    x0 = np.asarray([1.0, 0.0, marker_value, 0.0])
    x1 = np.asarray([1.0, 1.0, marker_value, marker_value])
    risk0 = float(expit(x0 @ beta))
    risk1 = float(expit(x1 @ beta))
    return risk0, risk1, risk1 - risk0


def delta_rd_from_beta(beta: np.ndarray, q25: float, q75: float) -> float:
    return risks_from_beta(beta, q75)[2] - risks_from_beta(beta, q25)[2]


def bootstrap_digest(valid: np.ndarray, delta: np.ndarray, reason: np.ndarray) -> str:
    digest = hashlib.sha256()
    digest.update(np.asarray(valid, dtype=np.uint8).tobytes(order="C"))
    digest.update(np.asarray(delta, dtype="<f8").tobytes(order="C"))
    for item in reason.astype(str):
        digest.update(item.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def run_bootstrap(design, point_beta: np.ndarray, q25: float, q75: float, replicates: int) -> BootstrapResult:
    seed = stable_seed(PHASE_SEED, design.trial, design.claim_id, "ABSOLUTE_RD")
    rng = np.random.default_rng(seed)
    arm0 = np.flatnonzero(design.treatment == 0)
    arm1 = np.flatnonzero(design.treatment == 1)
    draw0 = arm0[rng.integers(0, len(arm0), size=(replicates, len(arm0)))]
    draw1 = arm1[rng.integers(0, len(arm1), size=(replicates, len(arm1)))]
    delta = np.full(replicates, np.nan, dtype=np.float64)
    valid = np.zeros(replicates, dtype=bool)
    reason = np.full(replicates, "NOT_RUN", dtype=object)
    for index in range(replicates):
        sample = np.concatenate([draw0[index], draw1[index]])
        y = design.y[sample]
        treatment = design.treatment[sample]
        marker = design.marker_z[sample]
        x = np.column_stack([np.ones(len(sample)), treatment, marker, treatment * marker])
        beta, status = fit_logistic_irls(y, x, point_beta)
        reason[index] = status
        if beta is None:
            continue
        value = delta_rd_from_beta(beta, q25, q75)
        if not np.isfinite(value):
            reason[index] = "NONFINITE_DELTA_RD"
            continue
        delta[index] = value
        valid[index] = True
    return BootstrapResult(delta=delta, valid=valid, reason=reason, digest=bootstrap_digest(valid, delta, reason))


def bootstrap_summary(result: BootstrapResult, requested: int) -> dict[str, object]:
    values = result.delta[result.valid]
    valid_n = int(len(values))
    if valid_n >= math.ceil(0.95 * requested):
        status = "PASS"
    elif valid_n >= math.ceil(0.90 * requested):
        status = "WARN_CONDITIONAL_PERCENTILE"
    else:
        status = "NON_ESTIMABLE_BOOTSTRAP"
    output: dict[str, object] = {
        "bootstrap_requested": requested,
        "bootstrap_valid": valid_n,
        "bootstrap_invalid": int(requested - valid_n),
        "bootstrap_valid_fraction": valid_n / requested,
        "bootstrap_status": status,
        "bootstrap_digest": result.digest,
        "bootstrap_ci_low": np.nan,
        "bootstrap_ci_high": np.nan,
        "bootstrap_sign_p": np.nan,
        "bootstrap_sign_p_mcse": np.nan,
    }
    if valid_n and status != "NON_ESTIMABLE_BOOTSTRAP":
        output["bootstrap_ci_low"] = float(np.quantile(values, 0.025, method="linear"))
        output["bootstrap_ci_high"] = float(np.quantile(values, 0.975, method="linear"))
        lower_tail = (1.0 + float(np.sum(values <= 0.0))) / (1.0 + valid_n)
        upper_tail = (1.0 + float(np.sum(values >= 0.0))) / (1.0 + valid_n)
        sign_p = min(1.0, 2.0 * min(lower_tail, upper_tail))
        output["bootstrap_sign_p"] = sign_p
        output["bootstrap_sign_p_mcse"] = math.sqrt(sign_p * (1.0 - sign_p) / (1.0 + valid_n))
    return output


def lpm_hc3(design, q25: float, q75: float) -> dict[str, float]:
    x = np.column_stack(
        [np.ones(len(design.y)), design.treatment, design.marker_z, design.treatment * design.marker_z]
    )
    fit = sm.OLS(design.y, x).fit(cov_type="HC3")
    span = q75 - q25
    estimate = float(fit.params[3] * span)
    se = float(fit.bse[3] * span)
    return {
        "lpm_hc3_delta_rd": estimate,
        "lpm_hc3_ci_low": estimate - 1.96 * se,
        "lpm_hc3_ci_high": estimate + 1.96 * se,
        "lpm_hc3_p": float(fit.pvalues[3]),
    }


def make_input_manifest(workspace: Path, phase: Path, loader_path: Path) -> pd.DataFrame:
    inputs = [
        ("FROZEN_PRIMARY", phase / "source_data/Table2_local_IPD_primary_interactions_27rows.tsv"),
        ("FROZEN_METHOD", phase / "analysis_plan/binary_effect_scale_sensitivity_SOP_v1.0.md"),
        ("VERSIONED_LOADER", loader_path),
        ("RAW_PARTICIPANT_SCORE", workspace / "HER2_R3B/01_sources/TRIOB07/preTreatment.txt"),
        ("HASH_FROZEN_PARTICIPANT_SCORE", workspace / "HER2_R3B/03_data_processed/CHERLOB_frozen_signature_scores_source_compatible.tsv"),
        ("AUDITED_LABEL", workspace / "HER2_R3B/07_audit/CHERLOB_sample_mapping_audit.tsv"),
        ("PUBLIC_EXPRESSION", workspace / "Predictive_Biomarker_R4B/01_public_ipd/GSE164458/GSE164458_BrighTNess_RNAseq_log2_Processed_ASTOR.txt.gz"),
        ("AUDITED_LABEL", workspace / "Predictive_Biomarker_R4B/sample_linkage/BrighTNess_sample_linkage_audit.tsv"),
        ("FROZEN_GENE_REGISTRY", workspace / "Analyse_Report/CIN70_gene_registry.tsv"),
        ("HASH_FROZEN_PARTICIPANT_SCORE", workspace / "Predictive_Biomarker_R4C2B/09_results/DOP_revisedPARPi7_analysis_rows.tsv"),
    ]
    rows = []
    for role, path in inputs:
        if not path.exists():
            raise FileNotFoundError(path)
        rows.append(
            {
                "role": role,
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return pd.DataFrame(rows)


def classify_row(row: pd.Series) -> str:
    if row["bootstrap_status"] == "NON_ESTIMABLE_BOOTSTRAP":
        return "ABSOLUTE_SCALE_BOOTSTRAP_NON_ESTIMABLE__PRIMARY_UNCHANGED"
    additive_nominal = bool(row["additive_nominal"])
    additive_robust = bool(row["additive_multiplicity_robust"])
    multiplicative_nominal = bool(row["frozen_logit_p"] < 0.05)
    multiplicative_robust = bool(row["frozen_logit_q"] < 0.05)
    if additive_robust and multiplicative_robust:
        return "MULTIPLICITY_ROBUST_ON_BOTH_SCALES"
    if additive_robust and not multiplicative_robust:
        return "SCALE_DEPENDENT_UNCERTAINTY__ADDITIVE_ONLY__NOT_REPLICATION"
    if multiplicative_robust and not additive_robust:
        return "SCALE_DEPENDENT_UNCERTAINTY__MULTIPLICATIVE_ONLY"
    if additive_nominal:
        return "SCALE_DEPENDENT_NOMINAL_UNCERTAINTY__NOT_REPLICATION"
    if multiplicative_nominal:
        return "MULTIPLICATIVE_NOMINAL_ONLY_UNCERTAINTY"
    return "NO_MULTIPLICITY_ROBUST_EVIDENCE_OBSERVED__UNCERTAINTY_REMAINS"


def main() -> None:
    args = parse_args()
    if args.replicates <= 0:
        raise ValueError("replicates must be positive")
    workspace = args.workspace.resolve()
    phase = args.phase.resolve()
    for subdir in ("audit", "results"):
        (phase / subdir).mkdir(parents=True, exist_ok=True)

    r5a, loader_path = load_r5a_module(workspace)
    input_manifest = make_input_manifest(workspace, phase, loader_path)
    write_tsv(input_manifest, phase / "audit/binary_absolute_effect_input_manifest.tsv")

    designs, _ = r5a.load_binary_designs(workspace)
    if len(designs) != EXPECTED_MODELS:
        raise RuntimeError(f"expected {EXPECTED_MODELS} binary models, found {len(designs)}")
    frozen = pd.read_csv(phase / "source_data/Table2_local_IPD_primary_interactions_27rows.tsv", sep="\t")
    frozen = frozen[frozen["model"].astype(str).str.startswith("logistic")].copy()
    if len(frozen) != EXPECTED_MODELS:
        raise RuntimeError(f"frozen table contains {len(frozen)} binary models, expected {EXPECTED_MODELS}")

    result_rows: list[dict[str, object]] = []
    qc_rows: list[dict[str, object]] = []
    replicate_rows: list[dict[str, object]] = []

    for model_number, design in enumerate(designs.values(), 1):
        frozen_match = frozen[(frozen["trial"] == design.trial) & (frozen["claim_id"] == design.claim_id)]
        if len(frozen_match) != 1:
            raise RuntimeError(f"frozen-row match count {len(frozen_match)} for {design.trial}/{design.claim_id}")
        frozen_row = frozen_match.iloc[0]
        point = r5a.fit_logistic_mle(design.y, design.treatment, design.marker_z)
        point_beta = np.asarray(point["params"], dtype=float)
        beta_diff = abs(float(point["beta"]) - float(frozen_row["beta_interaction"]))
        p_diff = abs(float(point["p"]) - float(frozen_row["p_value"]))
        n_match = int(point["n"]) == int(frozen_row["n"])
        events_match = int(point["events"]) == int(frozen_row["events"])
        reconciliation_pass = bool(
            beta_diff <= RECONCILIATION_TOLERANCE
            and p_diff <= RECONCILIATION_TOLERANCE
            and n_match
            and events_match
        )
        if not reconciliation_pass:
            raise RuntimeError(f"frozen primary reconciliation failed for {design.trial}/{design.claim_id}")

        q25, q75 = np.quantile(design.marker_z, [0.25, 0.75], method="linear")
        risk0_q25, risk1_q25, rd_q25 = risks_from_beta(point_beta, float(q25))
        risk0_q75, risk1_q75, rd_q75 = risks_from_beta(point_beta, float(q75))
        delta_rd = rd_q75 - rd_q25
        main_bootstrap = run_bootstrap(design, point_beta, float(q25), float(q75), args.replicates)
        summary = bootstrap_summary(main_bootstrap, args.replicates)

        replay_match = True
        replay_digest = main_bootstrap.digest
        if not args.skip_replay:
            replay = run_bootstrap(design, point_beta, float(q25), float(q75), args.replicates)
            replay_digest = replay.digest
            replay_match = bool(
                main_bootstrap.digest == replay.digest
                and np.array_equal(main_bootstrap.valid, replay.valid)
                and np.array_equal(main_bootstrap.reason, replay.reason)
                and np.array_equal(main_bootstrap.delta, replay.delta, equal_nan=True)
            )
            if not replay_match:
                raise RuntimeError(f"deterministic replay failed for {design.trial}/{design.claim_id}")

        family = multiplicity_family(design.trial, design.claim_id)
        lpm = lpm_hc3(design, float(q25), float(q75))
        model_id = f"{design.trial}::{design.claim_id}"
        result_rows.append(
            {
                "model_id": model_id,
                "context": design.context,
                "trial": design.trial,
                "claim_id": design.claim_id,
                "signature": design.signature,
                "endpoint": "pCR",
                "outcome_favourable_value": 1,
                "multiplicity_family_id": family,
                "n": int(point["n"]),
                "events": int(point["events"]),
                "arm0_n": int(np.sum(design.treatment == 0)),
                "arm1_n": int(np.sum(design.treatment == 1)),
                "marker_q25_frozen_z": float(q25),
                "marker_q75_frozen_z": float(q75),
                "marker_iqr_z": float(q75 - q25),
                "risk_t0_q25": risk0_q25,
                "risk_t1_q25": risk1_q25,
                "rd_q25": rd_q25,
                "risk_t0_q75": risk0_q75,
                "risk_t1_q75": risk1_q75,
                "rd_q75": rd_q75,
                "delta_rd": delta_rd,
                **summary,
                "bootstrap_bh_q_within_family": np.nan,
                "frozen_logit_beta": float(frozen_row["beta_interaction"]),
                "frozen_logit_p": float(frozen_row["p_value"]),
                "frozen_logit_q": float(frozen_row["q_final_context"]),
                "frozen_primary_label": str(frozen_row["evidence_status"]),
                "rerun_logit_beta": float(point["beta"]),
                "rerun_logit_p": float(point["p"]),
                "abs_beta_diff_vs_frozen": beta_diff,
                "abs_p_diff_vs_frozen": p_diff,
                **lpm,
                "scale_sign_concordant": bool(np.sign(delta_rd) == np.sign(float(point["beta"]))),
                "primary_label_unchanged": True,
            }
        )

        counts = pd.Series(main_bootstrap.reason).value_counts(dropna=False).to_dict()
        qc_rows.append(
            {
                "model_id": model_id,
                "reconciliation_pass": reconciliation_pass,
                "n_match": n_match,
                "events_match": events_match,
                "bootstrap_digest_run1": main_bootstrap.digest,
                "bootstrap_digest_replay": replay_digest,
                "deterministic_replay_pass": replay_match,
                "valid_replicates": int(main_bootstrap.valid.sum()),
                "invalid_replicates": int((~main_bootstrap.valid).sum()),
                "invalid_reason_counts_json": json.dumps(counts, sort_keys=True),
            }
        )
        for replicate_index in range(args.replicates):
            replicate_rows.append(
                {
                    "model_id": model_id,
                    "replicate": replicate_index + 1,
                    "valid": bool(main_bootstrap.valid[replicate_index]),
                    "status": str(main_bootstrap.reason[replicate_index]),
                    "delta_rd": main_bootstrap.delta[replicate_index],
                }
            )
        print(
            f"[{model_number:02d}/{EXPECTED_MODELS}] {model_id}: "
            f"delta_RD={delta_rd:.6f}, valid={int(main_bootstrap.valid.sum())}/{args.replicates}, "
            f"replay={replay_match}",
            flush=True,
        )

    results = pd.DataFrame(result_rows)
    for family, indices in results.groupby("multiplicity_family_id", sort=False).groups.items():
        subset = results.loc[indices, "bootstrap_sign_p"]
        valid_indices = subset[subset.notna()].index
        if len(valid_indices):
            results.loc[valid_indices, "bootstrap_bh_q_within_family"] = multipletests(
                results.loc[valid_indices, "bootstrap_sign_p"].to_numpy(float), method="fdr_bh"
            )[1]

    ci_excludes_zero = (results["bootstrap_ci_low"] > 0) | (results["bootstrap_ci_high"] < 0)
    results["additive_nominal"] = (
        results["bootstrap_sign_p"].lt(0.05) & ci_excludes_zero & results["bootstrap_status"].ne("NON_ESTIMABLE_BOOTSTRAP")
    )
    results["additive_multiplicity_robust"] = (
        results["bootstrap_bh_q_within_family"].lt(0.05)
        & ci_excludes_zero
        & results["bootstrap_status"].ne("NON_ESTIMABLE_BOOTSTRAP")
    )
    results["interpretation"] = results.apply(classify_row, axis=1)
    results["sensitivity_can_promote_primary_label"] = False

    qc = pd.DataFrame(qc_rows)
    replicate_frame = pd.DataFrame(replicate_rows)
    write_tsv(results, phase / "results/binary_absolute_effect_23models.tsv")
    write_tsv(qc, phase / "audit/binary_absolute_effect_bootstrap_qc.tsv")
    concordance_columns = [
        "model_id",
        "context",
        "trial",
        "claim_id",
        "signature",
        "frozen_logit_beta",
        "frozen_logit_p",
        "frozen_logit_q",
        "frozen_primary_label",
        "delta_rd",
        "bootstrap_ci_low",
        "bootstrap_ci_high",
        "bootstrap_sign_p",
        "bootstrap_bh_q_within_family",
        "additive_nominal",
        "additive_multiplicity_robust",
        "scale_sign_concordant",
        "interpretation",
        "primary_label_unchanged",
    ]
    write_tsv(results[concordance_columns], phase / "results/binary_effect_scale_concordance_23models.tsv")
    replicate_path = phase / "results/binary_absolute_effect_bootstrap_replicates.tsv.gz"
    with gzip.open(replicate_path, "wt", encoding="utf-8", newline="") as handle:
        replicate_frame.to_csv(handle, sep="\t", index=False, na_rep="", lineterminator="\n")

    summary = {
        "phase": "R5B_A1R2_FORMAL_REFRAME_AND_ABSOLUTE_EFFECT",
        "run_date": "2026-09-13",
        "phase_seed": PHASE_SEED,
        "bootstrap_replicates_per_model": args.replicates,
        "deterministic_replay_executed": not args.skip_replay,
        "models_expected": EXPECTED_MODELS,
        "models_completed": int(len(results)),
        "frozen_primary_reconciled": int(qc["reconciliation_pass"].sum()),
        "deterministic_replay_passed": int(qc["deterministic_replay_pass"].sum()),
        "bootstrap_pass": int(results["bootstrap_status"].eq("PASS").sum()),
        "bootstrap_warn": int(results["bootstrap_status"].eq("WARN_CONDITIONAL_PERCENTILE").sum()),
        "bootstrap_nonestimable": int(results["bootstrap_status"].eq("NON_ESTIMABLE_BOOTSTRAP").sum()),
        "additive_nominal": int(results["additive_nominal"].sum()),
        "additive_multiplicity_robust": int(results["additive_multiplicity_robust"].sum()),
        "frozen_multiplicative_nominal": int(results["frozen_logit_p"].lt(0.05).sum()),
        "frozen_multiplicative_robust": int(results["frozen_logit_q"].lt(0.05).sum()),
        "scale_sign_concordant": int(results["scale_sign_concordant"].sum()),
        "multiplicity_families": int(results["multiplicity_family_id"].nunique()),
        "primary_layer_mutated": False,
        "sensitivity_can_promote_primary_label": False,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": scipy.__version__,
        "statsmodels": statsmodels.__version__,
    }
    (phase / "audit/binary_absolute_effect_run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if summary["models_completed"] != EXPECTED_MODELS:
        raise RuntimeError("model count failed")
    if summary["frozen_primary_reconciled"] != EXPECTED_MODELS:
        raise RuntimeError("frozen primary reconciliation failed")
    if not args.skip_replay and summary["deterministic_replay_passed"] != EXPECTED_MODELS:
        raise RuntimeError("deterministic replay gate failed")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
