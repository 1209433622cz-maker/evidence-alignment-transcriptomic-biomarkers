#!/usr/bin/env python3
"""Independent audit of the frozen A1R2 binary absolute-effect outputs.

This validator does not call the A1R2 fitting or bootstrap functions. It
reconstructs participant-level designs through the hash-locked R5A loader,
refits point estimates with scipy.optimize, and recalculates bootstrap
summaries directly from the persisted replicate table. The public repository
does not redistribute participant-level inputs; supply a lawfully populated
workspace explicitly with --workspace.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit


EXPECTED_MODELS = 23
POINT_TOLERANCE = 1e-7
SUMMARY_TOLERANCE = 1e-12


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
        help="Repository/phase root (default: repository root).",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_r5a(workspace: Path):
    path = workspace / "R5A_RP_ReviewerProofRobustness_20260909/scripts/run_r5a_reviewerproof.py"
    spec = importlib.util.spec_from_file_location("r5a_loader_for_independent_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fit_logistic_scipy(y: np.ndarray, treatment: np.ndarray, marker: np.ndarray) -> np.ndarray:
    x = np.column_stack([np.ones(len(y)), treatment, marker, treatment * marker])

    def objective(beta: np.ndarray) -> tuple[float, np.ndarray]:
        eta = x @ beta
        value = float(np.sum(np.logaddexp(0.0, eta) - y * eta))
        gradient = x.T @ (expit(eta) - y)
        return value, gradient

    fit = minimize(
        lambda beta: objective(beta)[0],
        np.zeros(4, dtype=float),
        jac=lambda beta: objective(beta)[1],
        method="BFGS",
        options={"gtol": 1e-11, "maxiter": 1000},
    )
    if not np.isfinite(fit.x).all() or np.linalg.norm(objective(fit.x)[1], ord=np.inf) > 1e-6:
        raise RuntimeError(f"independent point fit did not converge: {fit.message}")
    return np.asarray(fit.x, dtype=float)


def risks(beta: np.ndarray, marker: float) -> tuple[float, float, float]:
    p0 = float(expit(beta[0] + beta[2] * marker))
    p1 = float(expit(beta[0] + beta[1] + (beta[2] + beta[3]) * marker))
    return p0, p1, p1 - p0


def bh_adjust(pvalues: np.ndarray) -> np.ndarray:
    values = np.asarray(pvalues, dtype=float)
    order = np.argsort(values)
    ranked = values[order]
    adjusted_ranked = np.minimum.accumulate((ranked * len(values) / np.arange(1, len(values) + 1))[::-1])[::-1]
    adjusted = np.empty_like(adjusted_ranked)
    adjusted[order] = np.minimum(adjusted_ranked, 1.0)
    return adjusted


def close(left: float, right: float, tolerance: float = SUMMARY_TOLERANCE) -> bool:
    if pd.isna(left) and pd.isna(right):
        return True
    return bool(abs(float(left) - float(right)) <= tolerance)


def bootstrap_digest(valid: np.ndarray, delta: np.ndarray, reason: np.ndarray) -> str:
    digest = hashlib.sha256()
    digest.update(np.asarray(valid, dtype=np.uint8).tobytes(order="C"))
    digest.update(np.asarray(delta, dtype="<f8").tobytes(order="C"))
    for item in reason.astype(str):
        digest.update(item.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def main() -> None:
    args = parse_args()
    workspace = args.workspace.resolve()
    phase = args.phase.resolve()
    result_path = phase / "results/binary_absolute_effect_23models.tsv"
    replicate_path = phase / "results/binary_absolute_effect_bootstrap_replicates.tsv.gz"
    manifest_path = phase / "audit/binary_absolute_effect_input_manifest.tsv"
    results = pd.read_csv(result_path, sep="\t")
    replicates = pd.read_csv(replicate_path, sep="\t")
    inputs = pd.read_csv(manifest_path, sep="\t")
    replay_qc = pd.read_csv(phase / "audit/binary_absolute_effect_bootstrap_qc.tsv", sep="\t").set_index("model_id")
    if len(results) != EXPECTED_MODELS or results["model_id"].nunique() != EXPECTED_MODELS:
        raise RuntimeError("23-model identity gate failed")
    if len(replicates) != EXPECTED_MODELS * 5000:
        raise RuntimeError("replicate row-count gate failed")

    input_rows = []
    for row in inputs.itertuples(index=False):
        path = Path(row.path)
        observed = sha256_file(path) if path.exists() else "MISSING"
        input_rows.append({
            "role": row.role,
            "path": row.path,
            "expected_sha256": row.sha256,
            "observed_sha256": observed,
            "hash_pass": observed == row.sha256,
        })
    input_audit = pd.DataFrame(input_rows)

    r5a = load_r5a(workspace)
    designs, _ = r5a.load_binary_designs(workspace)
    design_map = {f"{design.trial}::{design.claim_id}": design for design in designs.values()}
    audit_rows = []
    recomputed_p: dict[str, float] = {}
    for row in results.itertuples(index=False):
        design = design_map[row.model_id]
        q25, q75 = np.quantile(design.marker_z, [0.25, 0.75], method="linear")
        beta = fit_logistic_scipy(design.y, design.treatment, design.marker_z)
        p0_lo, p1_lo, rd_lo = risks(beta, float(q25))
        p0_hi, p1_hi, rd_hi = risks(beta, float(q75))
        delta_point = rd_hi - rd_lo

        block = replicates.loc[replicates["model_id"] == row.model_id].sort_values("replicate")
        valid = block["valid"].astype(bool).to_numpy()
        delta = block["delta_rd"].to_numpy(dtype=float)
        reason = block["status"].astype(str).to_numpy()
        values = delta[valid]
        valid_n = len(values)
        status = (
            "PASS" if valid_n >= 4750 else
            "WARN_CONDITIONAL_PERCENTILE" if valid_n >= 4500 else
            "NON_ESTIMABLE_BOOTSTRAP"
        )
        ci_low = float(np.quantile(values, 0.025, method="linear")) if valid_n >= 4500 else np.nan
        ci_high = float(np.quantile(values, 0.975, method="linear")) if valid_n >= 4500 else np.nan
        if valid_n >= 4500:
            lower = (1.0 + float(np.sum(values <= 0.0))) / (1.0 + valid_n)
            upper = (1.0 + float(np.sum(values >= 0.0))) / (1.0 + valid_n)
            sign_p = min(1.0, 2.0 * min(lower, upper))
        else:
            sign_p = np.nan
        recomputed_p[row.model_id] = sign_p
        persisted_semantic_digest = bootstrap_digest(valid, delta, reason)
        replay_row = replay_qc.loc[row.model_id]

        checks = {
            "n_match": len(design.y) == int(row.n),
            "events_match": int(np.sum(design.y)) == int(row.events),
            "q25_match": close(q25, row.marker_q25_frozen_z),
            "q75_match": close(q75, row.marker_q75_frozen_z),
            "point_beta_match": close(beta[3], row.rerun_logit_beta, POINT_TOLERANCE),
            "risk_t0_q25_match": close(p0_lo, row.risk_t0_q25, POINT_TOLERANCE),
            "risk_t1_q25_match": close(p1_lo, row.risk_t1_q25, POINT_TOLERANCE),
            "risk_t0_q75_match": close(p0_hi, row.risk_t0_q75, POINT_TOLERANCE),
            "risk_t1_q75_match": close(p1_hi, row.risk_t1_q75, POINT_TOLERANCE),
            "delta_rd_match": close(delta_point, row.delta_rd, POINT_TOLERANCE),
            "bootstrap_count_match": valid_n == int(row.bootstrap_valid),
            "bootstrap_status_match": status == row.bootstrap_status,
            "bootstrap_ci_low_match": close(ci_low, row.bootstrap_ci_low),
            "bootstrap_ci_high_match": close(ci_high, row.bootstrap_ci_high),
            "bootstrap_sign_p_match": close(sign_p, row.bootstrap_sign_p),
            "bootstrap_run_replay_digest_match": bool(
                row.bootstrap_digest == replay_row["bootstrap_digest_run1"]
                and row.bootstrap_digest == replay_row["bootstrap_digest_replay"]
                and bool(replay_row["deterministic_replay_pass"])
            ),
            "primary_label_protected": bool(row.primary_label_unchanged) and not bool(row.sensitivity_can_promote_primary_label),
        }
        audit_rows.append({
            "model_id": row.model_id,
            "persisted_semantic_digest": persisted_semantic_digest,
            **checks,
            "all_checks_pass": all(checks.values()),
        })

    audit = pd.DataFrame(audit_rows)
    q_rows = []
    for family, family_frame in results.groupby("multiplicity_family_id", sort=False):
        observed = family_frame["bootstrap_bh_q_within_family"].to_numpy(dtype=float)
        recomputed = bh_adjust(np.asarray([recomputed_p[item] for item in family_frame["model_id"]]))
        for model_id, obs, rec in zip(family_frame["model_id"], observed, recomputed):
            q_rows.append({
                "model_id": model_id,
                "multiplicity_family_id": family,
                "reported_q": obs,
                "recomputed_q": rec,
                "q_match": close(obs, rec),
            })
    q_audit = pd.DataFrame(q_rows)

    claim_checks = {
        "one_nominal_additive": int(results["additive_nominal"].sum()) == 1,
        "zero_robust_additive": int(results["additive_multiplicity_robust"].sum()) == 0,
        "zero_nominal_multiplicative": int((results["frozen_logit_p"] < 0.05).sum()) == 0,
        "all_sign_concordant": int(results["scale_sign_concordant"].sum()) == EXPECTED_MODELS,
        "all_primary_labels_unchanged": bool(results["primary_label_unchanged"].all()),
        "no_sensitivity_promotion": bool((~results["sensitivity_can_promote_primary_label"]).all()),
        "exact_five_families": results["multiplicity_family_id"].nunique() == 5,
        "warn_is_cherlob_esr1": results.loc[results["bootstrap_status"] != "PASS", "model_id"].tolist() == ["CHER-LOB::HER2_01"],
        "nominal_is_trio_stromal_farmer": results.loc[results["additive_nominal"], "model_id"].tolist() == ["TRIO-US B07::HER2_09"],
        "cherlob_geparsixto_not_nominal": not bool(results.loc[results["model_id"] == "CHER-LOB::HER2_10", "additive_nominal"].iloc[0]),
    }
    summary = {
        "phase": "R5B_A1R2",
        "validator": "independent_scipy_point_and_persisted_bootstrap_recalculation",
        "models_checked": len(audit),
        "model_rows_passed": int(audit["all_checks_pass"].sum()),
        "q_rows_checked": len(q_audit),
        "q_rows_passed": int(q_audit["q_match"].sum()),
        "input_hashes_checked": len(input_audit),
        "input_hashes_passed": int(input_audit["hash_pass"].sum()),
        "claim_checks": claim_checks,
    }
    summary["overall_pass"] = bool(
        summary["model_rows_passed"] == EXPECTED_MODELS
        and summary["q_rows_passed"] == EXPECTED_MODELS
        and summary["input_hashes_passed"] == len(input_audit)
        and all(claim_checks.values())
    )

    audit_dir = phase / "audit"
    audit.to_csv(audit_dir / "independent_absolute_effect_validation.tsv", sep="\t", index=False, lineterminator="\n")
    q_audit.to_csv(audit_dir / "independent_absolute_effect_q_validation.tsv", sep="\t", index=False, lineterminator="\n")
    input_audit.to_csv(audit_dir / "independent_input_hash_validation.tsv", sep="\t", index=False, lineterminator="\n")
    (audit_dir / "independent_absolute_effect_validation.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if not summary["overall_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
