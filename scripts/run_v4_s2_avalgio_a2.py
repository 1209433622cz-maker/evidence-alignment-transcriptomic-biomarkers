#!/usr/bin/env python3
"""Execute the two frozen RPv4 V4-S2 AVAglio A2 Cox models."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import warnings
from pathlib import Path

import lifelines
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test
from scipy.stats import chi2


EXPECTED_INPUT_SHA256 = "7d561840758f9a7ea2e897c05789f0414255f008698fc538add1219d9083d707"
EXPECTED_INPUT_ROWS = 349
EXPECTED_IDH_COUNTS = {"Wild type": 339, "Mutant": 10}
EXPECTED_A2_ROWS = 333
EXPECTED_A2_EVENTS = 260
EXPECTED_A2_TREATMENT_COUNTS = {"Placebo": 171, "Bevacizumab": 162}
EXPECTED_A2_MGMT_MISSING = 68
SOURCE_COVARIATES = [
    "age",
    "corticosteroids",
    "surgical_status",
    "sex",
    "kps",
    "mgmt_status",
    "mmse",
    "rpa_class",
    "who",
]
SPECIFICATIONS = [
    ("GBM_01", "Phillips_proneural35", "phillips_subtype", "Phillips"),
    ("GBM_02", "Verhaak_proneural", "tcga_subtype", "Verhaak"),
]
Z975 = 1.959963984540054


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_frozen_a2(input_path: Path) -> tuple[pd.DataFrame, dict[str, object]]:
    observed_sha = sha256(input_path)
    require(observed_sha == EXPECTED_INPUT_SHA256, f"Input SHA mismatch: {observed_sha}")
    source = pd.read_csv(input_path, sep="\t", dtype=str, keep_default_na=False)
    require(len(source) == EXPECTED_INPUT_ROWS, f"Expected 349 rows, observed {len(source)}")
    require(source["geo_accession"].is_unique, "geo_accession must be unique")

    idh_counts = source["idh1_status"].value_counts(dropna=False).to_dict()
    require(idh_counts == EXPECTED_IDH_COUNTS, f"Unexpected IDH1 counts: {idh_counts}")
    literal_na_by_covariate = {c: int(source[c].eq("NA").sum()) for c in SOURCE_COVARIATES}
    literal_na_any = source[SOURCE_COVARIATES].eq("NA").any(axis=1)
    a2_mask = source["idh1_status"].eq("Wild type") & ~literal_na_any
    a2 = source.loc[a2_mask].copy()
    a2["source_row_1based"] = a2.index + 1

    a2["duration"] = pd.to_numeric(a2["os_time_to_event_(months)"], errors="raise")
    a2["event"] = pd.to_numeric(a2["os_event_type_(0_=_censored)"], errors="raise").astype(int)
    require((a2["duration"] > 0).all(), "All A2 durations must be positive")
    require(set(a2["event"].unique()) <= {0, 1}, "Event coding must be 0/1")
    require(len(a2) == EXPECTED_A2_ROWS, f"Expected 333 A2 rows, observed {len(a2)}")
    require(int(a2["event"].sum()) == EXPECTED_A2_EVENTS, "A2 event count mismatch")
    treatment_counts = a2["treatment"].value_counts(dropna=False).to_dict()
    require(treatment_counts == EXPECTED_A2_TREATMENT_COUNTS, f"Treatment mismatch: {treatment_counts}")
    mgmt_missing = int(a2["mgmt_status"].eq("Missing").sum())
    require(mgmt_missing == EXPECTED_A2_MGMT_MISSING, f"MGMT Missing mismatch: {mgmt_missing}")

    preflight = {
        "input_file_name": input_path.name,
        "input_sha256": observed_sha,
        "input_rows": int(len(source)),
        "idh1_counts": idh_counts,
        "literal_na_by_covariate": literal_na_by_covariate,
        "excluded_idhwt_literal_na_rows": int((source["idh1_status"].eq("Wild type") & literal_na_any).sum()),
        "a2_rows": int(len(a2)),
        "a2_events": int(a2["event"].sum()),
        "a2_treatment_counts": treatment_counts,
        "a2_mgmt_missing_retained": mgmt_missing,
    }
    return a2, preflight


def fit_classifier(
    a2: pd.DataFrame,
    claim_id: str,
    signature: str,
    label_column: str,
    short_label: str,
) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    data = a2.copy()
    data["marker"] = data[label_column].str.casefold().eq("proneural").astype(int)
    data["treatment_binary"] = data["treatment"].eq("Bevacizumab").astype(int)
    data["interaction"] = data["marker"] * data["treatment_binary"]
    design = data[["duration", "event", "marker", "treatment_binary", "interaction"]].copy()

    cell_counts = (
        data.groupby(["treatment_binary", "marker"], observed=True)
        .agg(n=("event", "size"), events=("event", "sum"))
        .reset_index()
    )
    require(len(cell_counts) == 4, f"{claim_id}: not all treatment×marker cells are present")
    cell_counts.insert(0, "signature", signature)
    cell_counts.insert(0, "claim_id", claim_id)
    cell_counts["treatment_label"] = cell_counts["treatment_binary"].map({0: "Placebo", 1: "Bevacizumab"})
    cell_counts["marker_label"] = cell_counts["marker"].map({0: "Non-proneural", 1: "Proneural"})

    matrix = design[["marker", "treatment_binary", "interaction"]].to_numpy(float)
    rank = int(np.linalg.matrix_rank(matrix))
    condition_number = float(np.linalg.cond(matrix))
    require(rank == 3, f"{claim_id}: design rank is {rank}, expected 3")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fit = CoxPHFitter(penalizer=0.0)
        fit.fit(
            design,
            duration_col="duration",
            event_col="event",
            show_progress=False,
            batch_mode=False,
            fit_options={"precision": 1e-12, "r_precision": 1e-12, "max_steps": 1000},
        )
    warning_text = " | ".join(str(item.message) for item in caught)
    row = fit.summary.loc["interaction"]
    finite_values = np.array(
        [row["coef"], row["se(coef)"], row["exp(coef)"], row["p"]], dtype=float
    )
    require(np.isfinite(finite_values).all(), f"{claim_id}: non-finite interaction estimate")

    ph = proportional_hazard_test(fit, design, time_transform="rank")
    ph_rows: list[dict[str, object]] = []
    for term in ["marker", "treatment_binary", "interaction"]:
        ph_row = ph.summary.loc[term]
        ph_rows.append(
            {
                "claim_id": claim_id,
                "signature": signature,
                "implementation": "lifelines_rank_transform",
                "term": term,
                "chisq": float(ph_row["test_statistic"]),
                "df": 1,
                "p": float(ph_row["p"]),
                "global_status": "TERM_SPECIFIC",
            }
        )
    marginal_sum = float(sum(float(x["chisq"]) for x in ph_rows))
    ph_rows.append(
        {
            "claim_id": claim_id,
            "signature": signature,
            "implementation": "lifelines_rank_transform",
            "term": "GLOBAL_APPROX",
            "chisq": marginal_sum,
            "df": 3,
            "p": float(chi2.sf(marginal_sum, 3)),
            "global_status": "APPROXIMATE_SUM_OF_MARGINAL_TESTS__R_COX_ZPH_IS_AUTHORITATIVE",
        }
    )
    ph_frame = pd.DataFrame(ph_rows)

    delta_beta = fit.compute_residuals(design, kind="delta_beta")
    threshold = 2.0 / math.sqrt(len(design))
    influence_rows: list[dict[str, object]] = []
    for term in ["marker", "treatment_binary", "interaction"]:
        raw = pd.to_numeric(delta_beta[term], errors="raise")
        se = float(fit.standard_errors_.loc[term])
        scaled = raw / se
        influence_rows.append(
            {
                "claim_id": claim_id,
                "signature": signature,
                "implementation": "lifelines_delta_beta_divided_by_model_se",
                "term": term,
                "n": int(len(design)),
                "dfbetas_threshold_2_over_sqrt_n": threshold,
                "max_abs_dfbeta": float(raw.abs().max()),
                "max_abs_dfbetas": float(scaled.abs().max()),
                "count_abs_dfbetas_above_threshold": int((scaled.abs() > threshold).sum()),
            }
        )
    influence_frame = pd.DataFrame(influence_rows)

    interaction_raw = pd.to_numeric(delta_beta["interaction"], errors="raise")
    interaction_scaled = interaction_raw / float(fit.standard_errors_.loc["interaction"])
    top_index = interaction_scaled.abs().nlargest(5).index
    restricted_rows: list[dict[str, object]] = []
    for order, idx in enumerate(top_index, start=1):
        source_row = data.loc[idx]
        key_material = f"{source_row['geo_accession']}|{source_row['sample_title']}"
        restricted_rows.append(
            {
                "claim_id": claim_id,
                "signature": signature,
                "rank_abs_interaction_dfbetas": order,
                "source_row_1based": int(source_row["source_row_1based"]),
                "geo_accession": source_row["geo_accession"],
                "record_key_sha256": hashlib.sha256(key_material.encode("utf-8")).hexdigest(),
                "interaction_dfbeta": float(interaction_raw.loc[idx]),
                "interaction_dfbetas": float(interaction_scaled.loc[idx]),
            }
        )
    restricted_frame = pd.DataFrame(restricted_rows)

    result = {
        "claim_id": claim_id,
        "signature": signature,
        "analysis_id": "V4_A2_FIXED333_UNADJUSTED",
        "population": "333 IDH1-wild-type after frozen six-row literal-NA exclusion",
        "formula": "Surv(OS_months, OS_event) ~ marker + treatment + marker:treatment",
        "ties": "efron",
        "n": int(len(design)),
        "events": int(design["event"].sum()),
        "proneural_n": int(design["marker"].sum()),
        "nonproneural_n": int((design["marker"] == 0).sum()),
        "bevacizumab_n": int(design["treatment_binary"].sum()),
        "placebo_n": int((design["treatment_binary"] == 0).sum()),
        "design_rank": rank,
        "design_condition_number": condition_number,
        "interaction_beta": float(row["coef"]),
        "interaction_se": float(row["se(coef)"]),
        "interaction_hr": float(row["exp(coef)"]),
        "ci95_low": float(row["exp(coef) lower 95%"]),
        "ci95_high": float(row["exp(coef) upper 95%"]),
        "interaction_z": float(row["z"]),
        "interaction_p": float(row["p"]),
        "log_likelihood": float(fit.log_likelihood_),
        "partial_aic": float(fit.AIC_partial_),
        "concordance_index": float(fit.concordance_index_),
        "converged": True,
        "fit_warnings": warning_text,
        "interpretation_lock": "same-trial specification bridge; not independent validation",
        "display_label": short_label,
    }
    return result, cell_counts, ph_frame, influence_frame, restricted_frame


def build_ladder(
    registry_path: Path, primary_results: pd.DataFrame, primary_sha: str
) -> pd.DataFrame:
    ladder = pd.read_csv(registry_path, sep="\t", dtype=str, keep_default_na=False)
    require(len(ladder) == 10, "Baseline A0-A4 registry must contain 10 rows")
    require(set(ladder["model_id"]) == {"A0", "A1", "A2", "A3", "A4"}, "Unexpected model IDs")
    ladder["interaction_beta"] = ""
    ladder["interaction_se"] = ""
    ladder["beta_se_source"] = ""
    ladder["diagnostic_status"] = "HISTORICAL_NOT_RERUN_IN_V4_S2"

    for idx, record in ladder.iterrows():
        if record["model_id"] != "A2":
            hr = float(record["interaction_hr"])
            low = float(record["ci95_low"])
            high = float(record["ci95_high"])
            ladder.loc[idx, "interaction_beta"] = f"{math.log(hr):.12g}"
            ladder.loc[idx, "interaction_se"] = f"{(math.log(high) - math.log(low)) / (2 * Z975):.12g}"
            ladder.loc[idx, "beta_se_source"] = "DERIVED_FROM_FROZEN_HR_AND_WALD_CI"
            continue

        matched = primary_results.loc[primary_results["claim_id"].eq(record["claim_id"])]
        require(len(matched) == 1, f"Missing A2 result for {record['claim_id']}")
        result = matched.iloc[0]
        ladder.loc[idx, "status"] = "EXECUTED_V4_S2"
        ladder.loc[idx, "interaction_hr"] = f"{float(result['interaction_hr']):.12g}"
        ladder.loc[idx, "ci95_low"] = f"{float(result['ci95_low']):.12g}"
        ladder.loc[idx, "ci95_high"] = f"{float(result['ci95_high']):.12g}"
        ladder.loc[idx, "interaction_p"] = f"{float(result['interaction_p']):.12g}"
        ladder.loc[idx, "interaction_beta"] = f"{float(result['interaction_beta']):.12g}"
        ladder.loc[idx, "interaction_se"] = f"{float(result['interaction_se']):.12g}"
        ladder.loc[idx, "beta_se_source"] = "V4_S2_MODEL_OUTPUT"
        ladder.loc[idx, "analysis_id_source"] = "V4_A2_FIXED333_UNADJUSTED"
        ladder.loc[idx, "interpretation_note"] = "executed prospectively under RPv4 S2; same-trial specification bridge"
        ladder.loc[idx, "result_sha256"] = primary_sha
        ladder.loc[idx, "diagnostic_status"] = "V4_S2_DIAGNOSTICS_COMPLETED"

    order = {f"A{i}": i for i in range(5)}
    ladder["_order"] = ladder["model_id"].map(order)
    ladder = ladder.sort_values(["claim_id", "_order"]).drop(columns="_order").reset_index(drop=True)
    return ladder


def build_delta_table(ladder: pd.DataFrame) -> pd.DataFrame:
    comparisons = [
        ("A0", "A1", "IDH1-WT population restriction"),
        ("A1", "A2", "frozen six-row availability restriction"),
        ("A2", "A3", "clinical-covariate adjustment on the same 333 rows"),
        ("A3", "A4", "multiple changes: 333-to-339 rows, missing-level handling, and ridge penalty"),
    ]
    rows: list[dict[str, object]] = []
    for claim_id, group in ladder.groupby("claim_id", sort=False):
        signature = group["signature"].iloc[0]
        keyed = group.set_index("model_id")
        for from_id, to_id, change in comparisons:
            from_row = keyed.loc[from_id]
            to_row = keyed.loc[to_id]
            beta_from = float(from_row["interaction_beta"])
            beta_to = float(to_row["interaction_beta"])
            hr_from = float(from_row["interaction_hr"])
            hr_to = float(to_row["interaction_hr"])
            rows.append(
                {
                    "claim_id": claim_id,
                    "signature": signature,
                    "comparison": f"{from_id}_TO_{to_id}",
                    "single_intended_change": change,
                    "from_n": int(from_row["n"]),
                    "to_n": int(to_row["n"]),
                    "from_events": int(from_row["events"]),
                    "to_events": int(to_row["events"]),
                    "from_hr": hr_from,
                    "to_hr": hr_to,
                    "delta_log_hr": beta_to - beta_from,
                    "hr_ratio_to_over_from": hr_to / hr_from,
                    "from_p": float(from_row["interaction_p"]),
                    "to_p": float(to_row["interaction_p"]),
                    "inferential_test_for_difference": "NOT_PRESPECIFIED__DESCRIPTIVE_ONLY",
                }
            )
    return pd.DataFrame(rows)


def render_ladder(ladder: pd.DataFrame, output_dir: Path) -> None:
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans"],
            "font.size": 8,
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    colors = {"A0": "#7A7A7A", "A1": "#4C78A8", "A2": "#E69F00", "A3": "#D55E00", "A4": "#009E73"}
    markers = {"A0": "o", "A1": "o", "A2": "D", "A3": "s", "A4": "^"}
    labels = {
        "A0": "A0  all 349, unadjusted",
        "A1": "A1  IDH1-WT 339, unadjusted",
        "A2": "A2  frozen 333, unadjusted",
        "A3": "A3  same 333, adjusted",
        "A4": "A4  IDH1-WT 339, ridge",
    }
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.65), sharey=True)
    for panel, (claim_id, group) in zip(["a", "b"], ladder.groupby("claim_id", sort=False)):
        ax = axes[0] if claim_id == "GBM_01" else axes[1]
        group = group.set_index("model_id").loc[["A0", "A1", "A2", "A3", "A4"]].reset_index()
        y = np.arange(5)[::-1]
        for ypos, row in zip(y, group.to_dict("records")):
            hr = float(row["interaction_hr"])
            low = float(row["ci95_low"])
            high = float(row["ci95_high"])
            ax.errorbar(
                hr,
                ypos,
                xerr=[[hr - low], [high - hr]],
                fmt=markers[row["model_id"]],
                color=colors[row["model_id"]],
                ecolor=colors[row["model_id"]],
                markersize=5.2,
                capsize=2.2,
                elinewidth=1.2,
                markeredgecolor="white",
                markeredgewidth=0.45,
                zorder=3,
            )
            ax.text(2.25, ypos, f"{hr:.2f} ({low:.2f}–{high:.2f})", va="center", ha="right", fontsize=7)
        ax.axvline(1.0, color="#333333", lw=0.8, ls="--", zorder=1)
        ax.set_xscale("log")
        ax.set_xlim(0.22, 2.45)
        ax.set_xticks([0.25, 0.5, 1.0, 2.0], labels=["0.25", "0.5", "1", "2"])
        ax.grid(axis="x", color="#E6E6E6", lw=0.6)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_title(("Phillips proneural" if claim_id == "GBM_01" else "Verhaak proneural"), loc="left", fontweight="bold", fontsize=9)
        ax.text(-0.12, 1.05, panel, transform=ax.transAxes, fontsize=10, fontweight="bold")
        ax.set_xlabel("Interaction hazard ratio")
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(np.arange(5)[::-1], [labels[x] for x in ["A0", "A1", "A2", "A3", "A4"]])
    fig.suptitle("AVAglio model ladder: population restriction and model adjustment", x=0.08, ha="left", fontsize=10, fontweight="bold")
    fig.text(0.08, 0.01, "A2 was prospectively frozen before fitting; estimates are same-trial specification comparisons, not independent validation.", fontsize=6.8)
    fig.tight_layout(rect=[0, 0.05, 1, 0.93], w_pad=2.0)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = output_dir / "Figure_V4S2_AVAglio_A0_A4_model_ladder"
    fig.savefig(stem.with_suffix(".png"), dpi=400, bbox_inches="tight", facecolor="white")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--baseline-registry", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    results_dir = args.output_root / "results"
    diagnostics_dir = args.output_root / "diagnostics"
    audit_dir = args.output_root / "audit"
    figures_dir = args.output_root / "figures"
    restricted_dir = args.output_root / "restricted_internal"
    for directory in [results_dir, diagnostics_dir, audit_dir, figures_dir, restricted_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    a2, preflight = load_frozen_a2(args.input)
    primary_rows: list[dict[str, object]] = []
    cell_frames: list[pd.DataFrame] = []
    ph_frames: list[pd.DataFrame] = []
    influence_frames: list[pd.DataFrame] = []
    restricted_frames: list[pd.DataFrame] = []
    for specification in SPECIFICATIONS:
        result, cells, ph, influence, restricted = fit_classifier(a2, *specification)
        primary_rows.append(result)
        cell_frames.append(cells)
        ph_frames.append(ph)
        influence_frames.append(influence)
        restricted_frames.append(restricted)

    primary = pd.DataFrame(primary_rows).drop(columns="display_label")
    primary_path = results_dir / "V4_S2_A2_primary_results.tsv"
    primary.to_csv(primary_path, sep="\t", index=False, float_format="%.12g")
    primary_sha = sha256(primary_path)

    cell_path = results_dir / "V4_S2_A2_treatment_marker_cell_counts.tsv"
    pd.concat(cell_frames, ignore_index=True).to_csv(cell_path, sep="\t", index=False)
    ph_path = diagnostics_dir / "V4_S2_A2_ph_lifelines.tsv"
    pd.concat(ph_frames, ignore_index=True).to_csv(ph_path, sep="\t", index=False, float_format="%.12g")
    influence_path = diagnostics_dir / "V4_S2_A2_influence_lifelines.tsv"
    pd.concat(influence_frames, ignore_index=True).to_csv(influence_path, sep="\t", index=False, float_format="%.12g")
    restricted_path = restricted_dir / "V4_S2_A2_top5_influential_records_lifelines_RESTRICTED.tsv"
    pd.concat(restricted_frames, ignore_index=True).to_csv(restricted_path, sep="\t", index=False, float_format="%.12g")

    ladder = build_ladder(args.baseline_registry, primary, primary_sha)
    ladder_path = results_dir / "V4_S2_AVAglio_A0_A4_model_ladder.tsv"
    ladder.to_csv(ladder_path, sep="\t", index=False)
    delta = build_delta_table(ladder)
    delta_path = results_dir / "V4_S2_AVAglio_model_ladder_deltas.tsv"
    delta.to_csv(delta_path, sep="\t", index=False, float_format="%.12g")
    render_ladder(ladder, figures_dir)

    public_outputs = [primary_path, cell_path, ph_path, influence_path, ladder_path, delta_path]
    public_outputs += sorted(figures_dir.glob("Figure_V4S2_AVAglio_A0_A4_model_ladder.*"))
    metadata = {
        "stage": "V4_S2_TARGETED_AVAGLIO_A2_EXECUTION_AND_MODEL_LADDER_DIAGNOSTICS",
        "preflight": preflight,
        "model_count": int(len(primary)),
        "all_models_converged": bool(primary["converged"].all()),
        "diagnostic_addendum_frozen_before_fit": True,
        "primary_result_sha256": primary_sha,
        "restricted_top5_file_created": True,
        "restricted_top5_file_excluded_from_public_release": True,
        "software": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "lifelines": lifelines.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "public_output_sha256": {path.relative_to(args.output_root).as_posix(): sha256(path) for path in public_outputs},
        "historical_outputs_modified": False,
        "primary_labels_modified": False,
    }
    metadata_path = audit_dir / "V4_S2_run_metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(primary.to_string(index=False))
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

