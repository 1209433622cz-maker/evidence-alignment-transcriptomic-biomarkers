#!/usr/bin/env python3
"""Fail-closed validation for the RPv4 V4-S2 AVAglio A2 delivery."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


EXPECTED_INPUT_SHA256 = "7d561840758f9a7ea2e897c05789f0414255f008698fc538add1219d9083d707"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def add(checks: list[dict[str, object]], name: str, passed: bool, detail: object) -> None:
    checks.append({"name": name, "pass": bool(passed), "detail": detail})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--baseline-registry", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    checks: list[dict[str, object]] = []
    observed_input_sha = sha256(args.input)
    add(checks, "input_sha256", observed_input_sha == EXPECTED_INPUT_SHA256, observed_input_sha)

    primary = pd.read_csv(args.output_root / "results" / "V4_S2_A2_primary_results.tsv", sep="\t")
    add(checks, "primary_model_identity", len(primary) == 2 and set(primary["claim_id"]) == {"GBM_01", "GBM_02"}, primary[["claim_id", "signature"]].values.tolist())
    add(checks, "primary_row_event_contract", bool((primary["n"] == 333).all() and (primary["events"] == 260).all()), primary[["claim_id", "n", "events"]].values.tolist())
    add(checks, "primary_estimability", bool((primary["design_rank"] == 3).all() and primary["converged"].all()), primary[["claim_id", "design_rank", "converged"]].values.tolist())
    finite_columns = ["interaction_beta", "interaction_se", "interaction_hr", "ci95_low", "ci95_high", "interaction_p"]
    add(checks, "primary_finite", bool(np.isfinite(primary[finite_columns].to_numpy(float)).all()), finite_columns)

    cells = pd.read_csv(args.output_root / "results" / "V4_S2_A2_treatment_marker_cell_counts.tsv", sep="\t")
    cell_summary = cells.groupby("claim_id").agg(rows=("n", "size"), n=("n", "sum"), events=("events", "sum"))
    add(checks, "four_cell_counts", bool((cell_summary["rows"] == 4).all() and (cell_summary["n"] == 333).all() and (cell_summary["events"] == 260).all()), cell_summary.reset_index().to_dict("records"))

    r_results = pd.read_csv(args.output_root / "audit" / "V4_S2_independent_R_cox_results.tsv", sep="\t")
    merged = primary.merge(r_results, on=["claim_id", "signature"], suffixes=("_py", "_r"), validate="one_to_one")
    compare_columns = ["interaction_beta", "interaction_se", "interaction_hr", "ci95_low", "ci95_high", "interaction_p", "log_likelihood"]
    max_diffs = {column: float((merged[f"{column}_py"] - merged[f"{column}_r"]).abs().max()) for column in compare_columns}
    add(checks, "independent_R_numeric_reproduction", all(value <= 2e-6 for value in max_diffs.values()), max_diffs)

    ph_r = pd.read_csv(args.output_root / "diagnostics" / "V4_S2_A2_ph_R_cox_zph.tsv", sep="\t")
    ph_counts = ph_r.groupby("claim_id")["term"].agg(list).to_dict()
    ph_complete = all({"marker", "treatment_binary", "interaction", "GLOBAL"}.issubset(set(terms)) for terms in ph_counts.values())
    add(checks, "R_schoenfeld_terms_and_global", ph_complete and ph_r["p"].between(0, 1).all(), ph_counts)

    influence_r = pd.read_csv(args.output_root / "diagnostics" / "V4_S2_A2_influence_R.tsv", sep="\t")
    expected_threshold = 2 / math.sqrt(333)
    add(checks, "dfbetas_threshold", bool(np.allclose(influence_r["dfbetas_threshold_2_over_sqrt_n"], expected_threshold, atol=1e-12)), expected_threshold)
    add(checks, "influence_terms", set(influence_r["term"]) == {"marker", "treatment_binary", "interaction"} and len(influence_r) == 6, influence_r[["claim_id", "term"]].values.tolist())

    baseline = pd.read_csv(args.baseline_registry, sep="\t", dtype=str, keep_default_na=False)
    ladder = pd.read_csv(args.output_root / "results" / "V4_S2_AVAglio_A0_A4_model_ladder.tsv", sep="\t", dtype=str, keep_default_na=False)
    add(checks, "model_ladder_identity", len(ladder) == 10 and set(ladder["model_id"]) == {"A0", "A1", "A2", "A3", "A4"}, len(ladder))
    historical_columns = ["n", "events", "interaction_hr", "ci95_low", "ci95_high", "interaction_p"]
    old_hist = baseline.loc[baseline["model_id"].ne("A2"), ["claim_id", "model_id"] + historical_columns]
    new_hist = ladder.loc[ladder["model_id"].ne("A2"), ["claim_id", "model_id"] + historical_columns]
    hist_match = old_hist.merge(new_hist, on=["claim_id", "model_id"], suffixes=("_old", "_new"), validate="one_to_one")
    historical_equal = all((hist_match[f"{c}_old"] == hist_match[f"{c}_new"]).all() for c in historical_columns)
    add(checks, "historical_registry_unchanged", historical_equal, historical_columns)
    a2_ladder = ladder.loc[ladder["model_id"].eq("A2")]
    add(checks, "A2_registry_materialized", bool(len(a2_ladder) == 2 and (a2_ladder["status"] == "EXECUTED_V4_S2").all() and (a2_ladder["result_sha256"] != "").all()), a2_ladder[["claim_id", "status"]].values.tolist())

    deltas = pd.read_csv(args.output_root / "results" / "V4_S2_AVAglio_model_ladder_deltas.tsv", sep="\t")
    add(checks, "ladder_deltas_complete", len(deltas) == 8 and set(deltas["comparison"]) == {"A0_TO_A1", "A1_TO_A2", "A2_TO_A3", "A3_TO_A4"}, len(deltas))

    figure_stem = args.output_root / "figures" / "Figure_V4S2_AVAglio_A0_A4_model_ladder"
    figure_files = [figure_stem.with_suffix(ext) for ext in [".png", ".pdf", ".svg"]]
    add(checks, "figure_formats", all(path.is_file() and path.stat().st_size > 1000 for path in figure_files), {path.suffix: path.stat().st_size if path.exists() else 0 for path in figure_files})

    restricted_files = list((args.output_root / "restricted_internal").glob("*.tsv"))
    add(checks, "restricted_influence_files_present", len(restricted_files) == 2, [path.name for path in restricted_files])
    public_tsvs = list((args.output_root / "results").glob("*.tsv")) + list((args.output_root / "diagnostics").glob("*.tsv")) + list((args.output_root / "audit").glob("*.tsv"))
    forbidden_headers = {"geo_accession", "sample_title", "patient_id", "participant_id", "sample_id"}
    leaked = []
    for path in public_tsvs:
        headers = set(pd.read_csv(path, sep="\t", nrows=0).columns)
        if headers & forbidden_headers:
            leaked.append(path.name)
    add(checks, "no_sample_identifiers_in_public_outputs", not leaked, leaked)

    status = "PASS" if all(item["pass"] for item in checks) else "FAIL"
    result = {
        "status": status,
        "checks_passed": sum(bool(item["pass"]) for item in checks),
        "checks_total": len(checks),
        "checks": checks,
    }
    output_path = args.output_root / "audit" / "V4_S2_validation.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

