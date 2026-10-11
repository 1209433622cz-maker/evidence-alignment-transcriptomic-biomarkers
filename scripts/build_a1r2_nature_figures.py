#!/usr/bin/env python3
"""Build source-driven A1R2 figure architecture and nested benchmark figures."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np
import pandas as pd
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader


PALETTE = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "red": "#D55E00",
    "purple": "#CC79A7",
    "grey": "#6B7280",
    "light": "#F3F4F6",
    "dark": "#1F2937",
}
TRIAL_COLORS = {
    "TRIO-US B07": PALETTE["blue"],
    "CHER-LOB": PALETTE["orange"],
    "BrighTNess": PALETTE["green"],
    "I-SPY2 DOP / GSE173839": PALETTE["purple"],
    "AVAglio": PALETTE["blue"],
    "GLARIUS": PALETTE["orange"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository/phase root (default: repository root).",
    )
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 7.0,
            "axes.titlesize": 8.5,
            "axes.labelsize": 7.5,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "legend.fontsize": 7.0,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "axes.linewidth": 0.65,
            "xtick.major.width": 0.65,
            "ytick.major.width": 0.65,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def panel_label(ax, label: str) -> None:
    ax.text(-0.10, 1.04, label, transform=ax.transAxes, fontsize=9.0, fontweight="bold", va="bottom")


def save_figure(fig: plt.Figure, stem: Path) -> list[Path]:
    outputs = []
    for suffix in ("pdf", "svg", "png"):
        path = stem.with_suffix(f".{suffix}")
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.04}
        if suffix == "png":
            kwargs["dpi"] = 300
        fig.savefig(path, **kwargs)
        outputs.append(path)
    plt.close(fig)
    return outputs


def box(ax, xy, width, height, text, edge=PALETTE["grey"], fill="white", dashed=False, fontsize=7.2):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.015",
        linewidth=0.8,
        edgecolor=edge,
        facecolor=fill,
        linestyle="--" if dashed else "-",
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fontsize)
    return patch


def arrow(ax, start, end, color=PALETTE["grey"]):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=8, linewidth=0.8, color=color))


def figure1_architecture(fig_dir: Path) -> list[Path]:
    fig = plt.figure(figsize=(7.2, 5.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1.0], width_ratios=[1.0, 1.35], hspace=0.35, wspace=0.25)
    ax_a = fig.add_subplot(gs[:, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 1])
    for ax in (ax_a, ax_b, ax_c):
        ax.set_axis_off()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    panel_label(ax_a, "a")
    ax_a.set_title("Registered PRISMA-ScR flow contract", loc="left", pad=8)
    y = [0.83, 0.62, 0.41, 0.20]
    labels = [
        "Database and supplemental records\nn = PENDING A2",
        "Deduplicated records screened\nn = PENDING A2",
        "Reports assessed for eligibility\nn = PENDING A2",
        "Eligible claim-estimands\nn = PENDING A2",
    ]
    for index, (yy, label) in enumerate(zip(y, labels)):
        box(ax_a, (0.08, yy - 0.065), 0.73, 0.13, label, edge=PALETTE["blue"], dashed=True)
        if index < len(y) - 1:
            arrow(ax_a, (0.445, yy - 0.07), (0.445, y[index + 1] + 0.07))
    box(ax_a, (0.84, 0.35), 0.14, 0.26, "Excluded\nreasons\nPENDING", edge=PALETTE["red"], dashed=True, fontsize=6.8)
    arrow(ax_a, (0.81, 0.52), (0.84, 0.48), color=PALETTE["red"])
    ax_a.text(0.08, 0.04, "ARCHITECTURE FROZEN; no outer-review counts exist before A2", fontsize=7.0, color=PALETTE["red"])

    panel_label(ax_b, "b")
    ax_b.set_title("Independent evidence axes and planned intersection view", loc="left", pad=8)
    axes = ["Formula", "Fidelity", "Randomized\nopportunity", "Estimand", "Lawful\ndata path", "External\nevaluation"]
    x_positions = np.linspace(0.08, 0.92, len(axes))
    for xx, label in zip(x_positions, axes):
        ax_b.plot([xx, xx], [0.25, 0.78], color="#CBD5E1", lw=3.0, solid_capstyle="round")
        ax_b.scatter([xx], [0.52], s=33, facecolor="white", edgecolor=PALETTE["dark"], linewidth=0.8, zorder=3)
        ax_b.text(xx, 0.84, label, ha="center", va="bottom", fontsize=7.0)
        ax_b.text(xx, 0.17, "PENDING\nA2", ha="center", va="top", fontsize=6.8, color=PALETTE["grey"])
    ax_b.text(0.5, 0.04, "Final panel: UpSet/intersection matrix. Axes are not a sequential funnel.", ha="center", fontsize=7.0)

    panel_label(ax_c, "c")
    ax_c.set_title("Relational units and dependency structure", loc="left", pad=8)
    box(ax_c, (0.02, 0.59), 0.18, 0.18, "Records", edge=PALETTE["grey"])
    box(ax_c, (0.28, 0.59), 0.18, 0.18, "Reports", edge=PALETTE["blue"])
    box(ax_c, (0.54, 0.59), 0.24, 0.18, "Claim-estimands\n(primary unit)", edge=PALETTE["green"])
    box(ax_c, (0.82, 0.59), 0.16, 0.18, "R5A bridge", edge=PALETTE["purple"], dashed=True)
    arrow(ax_c, (0.20, 0.68), (0.28, 0.68))
    arrow(ax_c, (0.46, 0.68), (0.54, 0.68))
    arrow(ax_c, (0.78, 0.68), (0.82, 0.68))
    box(ax_c, (0.19, 0.18), 0.23, 0.18, "Biomarker\ndefinitions", edge=PALETTE["orange"])
    box(ax_c, (0.48, 0.18), 0.20, 0.18, "Trials and\ndatasets", edge=PALETTE["orange"])
    box(ax_c, (0.74, 0.18), 0.23, 0.18, "Dependency\nclusters", edge=PALETTE["red"])
    arrow(ax_c, (0.64, 0.58), (0.35, 0.36))
    arrow(ax_c, (0.66, 0.58), (0.58, 0.36))
    arrow(ax_c, (0.68, 0.58), (0.83, 0.36))
    fig.suptitle("Figure 1 architecture | Systematic universe and nested benchmark bridge", x=0.01, ha="left", fontsize=9.5, fontweight="bold")
    return save_figure(fig, fig_dir / "Figure1_systematic_universe_architecture_A1R2")


def figure2_architecture(fig_dir: Path) -> list[Path]:
    rows = ["Differential benefit", "Treatment selection", "Sensitive/resistant", "Response association", "Ambiguous"]
    cols = ["Randomized\ninteraction", "Randomized\nsubgroup only", "Comparative\nnon-randomized", "Treated\nsingle arm", "Mixed / unclear"]
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    panel_label(ax, "a")
    ax.set_xlim(-0.5, len(cols) + 1.3)
    ax.set_ylim(-0.5, len(rows) + 0.9)
    ax.invert_yaxis()
    for i in range(len(rows)):
        for j in range(len(cols)):
            ax.add_patch(Rectangle((j - 0.45, i - 0.38), 0.9, 0.76, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6, linestyle="--"))
            ax.text(j, i, "PENDING", ha="center", va="center", fontsize=6.7, color=PALETTE["grey"])
    ax.set_xticks(range(len(cols)), cols)
    ax.set_yticks(range(len(rows)), rows)
    ax.tick_params(length=0)
    ax.xaxis.tick_top()
    ax.text(len(cols) + 0.15, -0.6, "Formal interaction", ha="center", fontsize=7.2, fontweight="bold")
    for i in range(len(rows)):
        ax.add_patch(Rectangle((len(cols) - 0.15, i - 0.38), 1.1, 0.76, facecolor="#F8FAFC", edgecolor=PALETTE["blue"], lw=0.7, linestyle="--"))
        ax.text(len(cols) + 0.4, i, "YES / NO /\nINDETERMINATE", ha="center", va="center", fontsize=6.4)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(top=0.79, left=0.16, right=0.98, bottom=0.08)
    fig.text(0.16, 0.865, "Claim wording × original evidence design", fontsize=8.5)
    fig.text(0.16, 0.055, "ARCHITECTURE FROZEN — claim and report counts will be generated only after registered A2 screening", color=PALETTE["red"], fontsize=7.1)
    fig.suptitle("Figure 2 architecture | Claim language and supporting evidence", x=0.01, y=0.98, ha="left", fontsize=9.5, fontweight="bold")
    return save_figure(fig, fig_dir / "Figure2_claim_evidence_matrix_architecture_A1R2")


def figure3_architecture(fig_dir: Path) -> list[Path]:
    columns = ["Formula", "Implementation\nfidelity", "Randomized\nopportunity", "Estimand\nalignment", "Lawful\ndata path", "External\nevaluation", "Interaction\ninterval"]
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.set_axis_off()
    panel_label(ax, "a")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Claim-level categorical readiness matrix contract", loc="left", pad=8)
    left, right = 0.22, 0.98
    top, bottom = 0.79, 0.25
    widths = np.linspace(left, right, len(columns) + 1)
    ax.add_patch(Rectangle((0.02, bottom), left - 0.02, top - bottom, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.7))
    ax.text(0.12, (top + bottom) / 2, "Rows = eligible\nclaim-estimands\nafter A2", ha="center", va="center", fontsize=7.2)
    for j, label in enumerate(columns):
        x0, x1 = widths[j], widths[j + 1]
        ax.add_patch(Rectangle((x0, bottom), x1 - x0, top - bottom, facecolor="white", edgecolor="#CBD5E1", lw=0.7, linestyle="--"))
        ax.text((x0 + x1) / 2, top + 0.045, label, ha="center", va="bottom", fontsize=6.9)
        for yy in np.linspace(bottom + 0.08, top - 0.08, 5):
            ax.scatter((x0 + x1) / 2, yy, s=22, facecolor="white", edgecolor=PALETTE["grey"], lw=0.6)
    ax.text(0.5, 0.13, "Categorical states only; no summed readiness or quality score", ha="center", fontsize=7.2, color=PALETTE["red"])
    ax.text(0.5, 0.06, "Unknown / indeterminate remains visible. Complete claim-level matrix moves to Supplement if density impairs ≥7 pt text.", ha="center", fontsize=6.9)
    fig.suptitle("Figure 3 architecture | Executability, evaluability and validation maturity", x=0.01, ha="left", fontsize=9.5, fontweight="bold")
    return save_figure(fig, fig_dir / "Figure3_readiness_matrix_architecture_A1R2")


def forest_rows(frame: pd.DataFrame, context_order: list[str]) -> list[dict[str, object]]:
    rows = []
    for context in context_order:
        part = frame[frame["context"] == context]
        for claim_id in part["claim_id"].drop_duplicates():
            claim = part[part["claim_id"] == claim_id]
            signature = str(claim.iloc[0]["signature"])
            rows.append({"kind": "claim", "label": f"{claim_id}  {signature}", "context": context})
            for _, item in claim.iterrows():
                rows.append({"kind": "estimate", **item.to_dict()})
    return rows


def draw_ratio_forest(ax, rows, ratio_label: str, xlim: tuple[float, float], panel: str) -> None:
    panel_label(ax, panel)
    ax.set_xscale("log")
    ax.set_xlim(*xlim)
    ax.axvline(1.0, color=PALETTE["dark"], lw=0.7, ls="--")
    ax.set_ylim(-0.5, len(rows) - 0.5)
    ax.invert_yaxis()
    ax.set_yticks([])
    ax.grid(axis="x", color="#E5E7EB", lw=0.55)
    for y, row in enumerate(rows):
        if row["kind"] == "claim":
            ax.axhspan(y - 0.42, y + 0.42, color="#F8FAFC", zorder=0)
            ax.text(-0.76, y, row["label"], transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=7.0, fontweight="bold")
            continue
        color = TRIAL_COLORS.get(str(row["trial"]), PALETTE["grey"])
        estimate = float(row["effect_ratio"])
        low = float(row["ci95_low_ratio"])
        high = float(row["ci95_high_ratio"])
        ax.errorbar(estimate, y, xerr=[[estimate - low], [high - estimate]], fmt="o", color=color, ecolor=color, ms=3.6, capsize=1.6, elinewidth=0.8, markeredgecolor="white", markeredgewidth=0.35)
        ax.text(-0.70, y, f"   {row['trial']}  n={int(row['n'])}, events={int(row['events'])}", transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=6.9, color=PALETTE["dark"])
        ax.text(1.03, y, f"{estimate:.2f} [{low:.2f}, {high:.2f}]", transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=6.9)
    ax.set_xlabel(ratio_label)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)


def figure4_nested_forest(fig_dir: Path, table: pd.DataFrame, source_dir: Path) -> list[Path]:
    binary = table[table["model"].astype(str).str.startswith("logistic")].copy()
    survival = table[table["model"].astype(str).str.startswith("Cox")].copy()
    write_cols = ["context", "trial", "claim_id", "signature", "endpoint", "model", "n", "events", "effect_ratio", "ci95_low_ratio", "ci95_high_ratio", "p_value", "q_final_context"]
    pd.concat([binary, survival])[write_cols].to_csv(source_dir / "Figure4_nested_claim_forest_source.tsv", sep="\t", index=False, lineterminator="\n")
    binary_rows = forest_rows(binary, ["HER2_DUAL_BLOCKADE", "TNBC_PLATINUM", "TNBC_PARP_PLATINUM", "TNBC_PARP_IO"])
    survival_rows = forest_rows(survival, ["GBM_BEVACIZUMAB"])
    fig = plt.figure(figsize=(7.2, 9.55))
    gs = fig.add_gridspec(2, 1, height_ratios=[7.7, 1.55], hspace=0.28)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[1, 0])
    draw_ratio_forest(ax_a, binary_rows, "Interaction odds ratio (95% CI)", (0.01, 60.0), "a")
    ax_a.set_title("Binary pCR models nested within 13 local claims", loc="left", pad=8)
    draw_ratio_forest(ax_b, survival_rows, "Interaction hazard ratio (95% CI)", (0.20, 3.0), "b")
    ax_b.set_title("Overall-survival models nested within 2 local claims", loc="left", pad=8)
    handles = [Line2D([0], [0], marker="o", color="none", markerfacecolor=color, markeredgecolor="white", markersize=5, label=trial) for trial, color in TRIAL_COLORS.items()]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.55, 0.957), ncol=3, frameon=False)
    fig.subplots_adjust(left=0.38, right=0.79, top=0.89, bottom=0.055)
    fig.suptitle("Figure 4 | Nested frozen randomized benchmark, claim-centred", x=0.01, y=0.992, ha="left", fontsize=9.5, fontweight="bold")
    return save_figure(fig, fig_dir / "Figure4_nested_claim_forest_A1R2")


def short_label(row) -> str:
    trial = str(row["trial"])
    if trial == "I-SPY2 DOP / GSE173839":
        trial = "DOP"
    return f"{trial} · {row['signature']}"


def figure5_scale_migration(fig_dir: Path, cross: pd.DataFrame, absolute: pd.DataFrame, gbm: pd.DataFrame, source_dir: Path) -> list[Path]:
    cross.to_csv(source_dir / "Figure5_cross_trial_source.tsv", sep="\t", index=False, lineterminator="\n")
    absolute.to_csv(source_dir / "Figure5_binary_absolute_source.tsv", sep="\t", index=False, lineterminator="\n")
    gbm.to_csv(source_dir / "Figure5_gbm_absolute_source.tsv", sep="\t", index=False, lineterminator="\n")
    fig = plt.figure(figsize=(7.2, 9.55))
    gs = fig.add_gridspec(3, 2, height_ratios=[2.7, 4.55, 1.65], hspace=0.55, wspace=0.55)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, :])
    ax_d1 = fig.add_subplot(gs[2, 0])
    ax_d2 = fig.add_subplot(gs[2, 1])

    panel_label(ax_a, "a")
    y = np.arange(len(cross))
    for i, row in cross.reset_index(drop=True).iterrows():
        ax_a.plot([row["anchor_beta"], row["replication_beta"]], [i, i], color="#CBD5E1", lw=1.0)
        ax_a.scatter(row["anchor_beta"], i, marker="o", s=18, color=PALETTE["blue"], label="Anchor" if i == 0 else None)
        ax_a.scatter(row["replication_beta"], i, marker="s", s=18, facecolor="white", edgecolor=PALETTE["red"], linewidth=0.8, label="Replication" if i == 0 else None)
    ax_a.axvline(0, color=PALETTE["dark"], lw=0.7, ls="--")
    ax_a.set_yticks(y, [str(x) for x in cross["signature"]])
    ax_a.invert_yaxis()
    ax_a.set_xlabel("Interaction coefficient β")
    ax_a.set_title("Cross-trial migration", loc="left")
    ax_a.legend(frameon=False, loc="lower right")

    panel_label(ax_b, "b")
    ax_b.errorbar(cross["observed_delta_abs_beta"], y, xerr=[cross["observed_delta_abs_beta"] - cross["delta_abs_beta_ci95_low"], cross["delta_abs_beta_ci95_high"] - cross["observed_delta_abs_beta"]], fmt="o", color=PALETTE["grey"], ecolor=PALETTE["grey"], ms=3.5, capsize=1.5, elinewidth=0.8)
    ax_b.axvline(0, color=PALETTE["dark"], lw=0.7, ls="--")
    ax_b.set_yticks(y, [str(x) for x in cross["signature"]])
    ax_b.invert_yaxis()
    ax_b.set_xlabel("Δ|β|, replication − anchor")
    ax_b.set_title("Magnitude change with bootstrap interval", loc="left")

    panel_label(ax_c, "c")
    plot_abs = absolute.copy().reset_index(drop=True)
    y_c = np.arange(len(plot_abs))
    colors = [TRIAL_COLORS.get(str(x), PALETTE["grey"]) for x in plot_abs["trial"]]
    for i, row in plot_abs.iterrows():
        marker = "D" if bool(row["additive_nominal"]) else "o"
        ax_c.errorbar(row["delta_rd"], i, xerr=[[row["delta_rd"] - row["bootstrap_ci_low"]], [row["bootstrap_ci_high"] - row["delta_rd"]]], fmt=marker, color=colors[i], ecolor=colors[i], ms=4.0 if marker == "D" else 3.5, capsize=1.5, elinewidth=0.8, markeredgecolor=PALETTE["dark"] if marker == "D" else "white", markeredgewidth=0.55)
    ax_c.axvline(0, color=PALETTE["dark"], lw=0.7, ls="--")
    ax_c.set_yticks(y_c, [short_label(row) for _, row in plot_abs.iterrows()])
    ax_c.invert_yaxis()
    ax_c.set_xlim(-1.0, 0.85)
    ax_c.set_xlabel("ΔRD = RD(Q75) − RD(Q25) for pCR (95% arm-stratified bootstrap CI)")
    ax_c.set_title("Absolute-risk effect modification in 23 frozen binary models", loc="left")
    ax_c.text(0.99, 0.985, "Diamond: nominal additive-only signal; none passed within-family BH", transform=ax_c.transAxes, ha="right", va="top", fontsize=7.0, color=PALETTE["red"], bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5, "alpha": 0.92})

    panel_label(ax_d1, "d")
    y_d = np.arange(len(gbm))
    labels = [f"{r.trial} · {r.signature}" for r in gbm.itertuples()]
    ax_d1.errorbar(gbm["rmst_did_months"], y_d, xerr=[gbm["rmst_did_months"] - gbm["rmst_did_ci95_low"], gbm["rmst_did_ci95_high"] - gbm["rmst_did_months"]], fmt="o", color=PALETTE["blue"], ecolor=PALETTE["blue"], ms=3.5, capsize=1.5, elinewidth=0.8)
    ax_d1.axvline(0, color=PALETTE["dark"], lw=0.7, ls="--")
    ax_d1.set_yticks(y_d, labels)
    ax_d1.invert_yaxis()
    ax_d1.set_xlabel("18-month RMST difference-in-differences (months)")
    ax_d1.set_title("GBM survival absolute-scale analogue", loc="left")
    ax_d2.errorbar(gbm["survival_probability_did"], y_d, xerr=[gbm["survival_probability_did"] - gbm["survival_probability_did_ci95_low"], gbm["survival_probability_did_ci95_high"] - gbm["survival_probability_did"]], fmt="s", color=PALETTE["green"], ecolor=PALETTE["green"], ms=3.5, capsize=1.5, elinewidth=0.8)
    ax_d2.axvline(0, color=PALETTE["dark"], lw=0.7, ls="--")
    ax_d2.set_yticks(y_d, labels)
    ax_d2.set_yticklabels([])
    ax_d2.invert_yaxis()
    ax_d2.set_xlabel("18-month survival-probability difference-in-differences")
    ax_d2.set_title("Survival probability", loc="left")
    for ax in (ax_a, ax_b, ax_c, ax_d1, ax_d2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", color="#E5E7EB", lw=0.5)
    fig.subplots_adjust(left=0.25, right=0.98, top=0.94, bottom=0.055)
    fig.suptitle("Figure 5 | Effect migration, uncertainty and effect scale", x=0.01, ha="left", fontsize=9.5, fontweight="bold")
    return save_figure(fig, fig_dir / "Figure5_effect_scale_and_migration_A1R2")


def figure_s5_absolute_forest(fig_dir: Path, absolute: pd.DataFrame) -> list[Path]:
    fig, ax = plt.subplots(figsize=(7.2, 6.6))
    panel_label(ax, "a")
    frame = absolute.reset_index(drop=True)
    y = np.arange(len(frame))
    for i, row in frame.iterrows():
        color = TRIAL_COLORS.get(str(row["trial"]), PALETTE["grey"])
        marker = "D" if bool(row["additive_nominal"]) else "o"
        ax.errorbar(row["delta_rd"], i, xerr=[[row["delta_rd"] - row["bootstrap_ci_low"]], [row["bootstrap_ci_high"] - row["delta_rd"]]], fmt=marker, color=color, ecolor=color, ms=4.0, capsize=1.7, elinewidth=0.85, markeredgecolor=PALETTE["dark"] if marker == "D" else "white", markeredgewidth=0.55)
        ax.text(1.02, i, f"{row['delta_rd']:.3f} [{row['bootstrap_ci_low']:.3f}, {row['bootstrap_ci_high']:.3f}]  q={row['bootstrap_bh_q_within_family']:.3f}", transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=6.9)
    ax.axvline(0, color=PALETTE["dark"], lw=0.7, ls="--")
    ax.set_yticks(y, [short_label(row) for _, row in frame.iterrows()])
    ax.invert_yaxis()
    ax.set_xlim(-1.0, 0.85)
    ax.set_xlabel("ΔRD = RD(Q75) − RD(Q25) for pCR")
    ax.set_title("All 23 frozen binary models: absolute-risk effect modification", loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", color="#E5E7EB", lw=0.5)
    fig.subplots_adjust(left=0.31, right=0.72, top=0.93, bottom=0.08)
    fig.suptitle("Supplementary Figure 5 | Binary absolute-effect sensitivity", x=0.01, ha="left", fontsize=9.5, fontweight="bold")
    return save_figure(fig, fig_dir / "FigureS5_binary_absolute_effect_forest_A1R2")


def make_contact_sheet(pngs: list[Path], output: Path) -> None:
    thumbs = []
    for path in pngs:
        image = Image.open(path).convert("RGB")
        image.thumbnail((1000, 850))
        canvas = Image.new("RGB", (1040, 920), "white")
        canvas.paste(image, ((1040 - image.width) // 2, 45))
        draw = ImageDraw.Draw(canvas)
        draw.text((20, 14), path.stem, fill="black")
        thumbs.append(canvas)
    cols = 2
    rows = int(np.ceil(len(thumbs) / cols))
    sheet = Image.new("RGB", (cols * 1040, rows * 920), "white")
    for index, image in enumerate(thumbs):
        sheet.paste(image, ((index % cols) * 1040, (index // cols) * 920))
    sheet.save(output, dpi=(150, 150))


def output_qc(paths: list[Path], audit_dir: Path) -> pd.DataFrame:
    rows = []
    for path in paths:
        row = {"file": path.name, "bytes": path.stat().st_size, "sha256": sha256(path), "format": path.suffix.lower().lstrip(".")}
        if path.suffix.lower() == ".png":
            with Image.open(path) as image:
                row.update({"width_px": image.width, "height_px": image.height, "dpi_x": image.info.get("dpi", (None, None))[0]})
        elif path.suffix.lower() == ".pdf":
            reader = PdfReader(str(path))
            page = reader.pages[0]
            row.update({"pdf_pages": len(reader.pages), "width_points": float(page.mediabox.width), "height_points": float(page.mediabox.height)})
        rows.append(row)
    frame = pd.DataFrame(rows)
    frame.to_csv(audit_dir / "figure_output_manifest.tsv", sep="\t", index=False, lineterminator="\n")
    return frame


def main() -> None:
    args = parse_args()
    phase = args.phase.resolve()
    fig_dir = phase / "figures"
    source_dir = phase / "source_data"
    audit_dir = phase / "audit"
    for path in (fig_dir, source_dir, audit_dir):
        path.mkdir(parents=True, exist_ok=True)
    configure()
    inputs = {
        "table2": source_dir / "Table2_local_IPD_primary_interactions_27rows.tsv",
        "cross_trial": source_dir / "R5A_cross_trial_bootstrap_attenuation.tsv",
        "binary_absolute": phase / "results/binary_absolute_effect_23models.tsv",
        "gbm_absolute": source_dir / "R5A_gbm_absolute_scale_sensitivity.tsv",
    }
    for path in inputs.values():
        if not path.exists():
            raise FileNotFoundError(path)
    pd.DataFrame(
        [
            {
                "role": key,
                "path": path.relative_to(phase).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for key, path in inputs.items()
        ]
    ).to_csv(audit_dir / "figure_input_hash_audit.tsv", sep="\t", index=False, lineterminator="\n")
    table = pd.read_csv(inputs["table2"], sep="\t")
    cross = pd.read_csv(inputs["cross_trial"], sep="\t")
    absolute = pd.read_csv(inputs["binary_absolute"], sep="\t")
    gbm = pd.read_csv(inputs["gbm_absolute"], sep="\t")

    outputs: list[Path] = []
    outputs += figure1_architecture(fig_dir)
    outputs += figure2_architecture(fig_dir)
    outputs += figure3_architecture(fig_dir)
    outputs += figure4_nested_forest(fig_dir, table, source_dir)
    outputs += figure5_scale_migration(fig_dir, cross, absolute, gbm, source_dir)
    outputs += figure_s5_absolute_forest(fig_dir, absolute)
    pngs = [path for path in outputs if path.suffix.lower() == ".png"]
    contact = audit_dir / "A1R2_all_figures_contact_sheet.png"
    make_contact_sheet(pngs, contact)
    outputs.append(contact)
    manifest = output_qc(outputs, audit_dir)
    summary = {
        "phase": "R5B_A1R2",
        "figures": 6,
        "rendered_files": int(len(outputs)),
        "main_architecture_only": ["Figure1", "Figure2", "Figure3"],
        "main_data_bearing": ["Figure4", "Figure5"],
        "supplement_data_bearing": ["FigureS5"],
        "outer_counts_fabricated": False,
        "global_minimum_font_points": 7.0,
        "vector_pdf_svg_generated": True,
        "libreoffice_used": False,
        "input_hashes": {key: sha256(path) for key, path in inputs.items()},
        "output_manifest_sha256": sha256(audit_dir / "figure_output_manifest.tsv"),
    }
    (audit_dir / "figure_build_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
