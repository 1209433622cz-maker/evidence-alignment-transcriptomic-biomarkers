#!/usr/bin/env python3
"""Build RPv4 V4-S5 publication-facing figures and derived tables from frozen inputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import textwrap
from collections import Counter
from pathlib import Path


EXPECTED = {
    "objects22": "081e4da7b7a7855fc14ae31f8e9b427a62839539bd2379e6d27cebcebc393b68",
    "triage10": "b0ed74340a3a769f7b47d10eb61a07a5ce8f896c6ff4fe67cdee65fe8340958a",
    "avaglio10": "96344ec2710a6c4eb628efda4c3c0124db0282146dd62c1471d5cf57014fd445",
    "cross13": "10fb0087b84358fded840253f495d2a43e14e702a1b8aeece8dbbf45cce03512",
    "dual8": "8318b97afcad093d71cb580936486ff724193a9a599bb6c63b3872f9a2b0c82a",
    "panelmap13": "5a8ee74220011fbe492225aea7e1ddc5bca626fa9d2675fe6ba7a47ca158a6ea",
    "claims10": "84d1808c48e0e54ec796e2ca26386a68e916753ee5f5ab834401d13e17e972eb",
    "s4status": "0e71e484674ca26729cdcb866f4af0ac3e3e837aae9752d06f1d45964a27bfa0",
    "absolute23": "cb3829631b2e164b70c12c5a3a2a14b6af15401b196c296004ed97946c562bab",
    "trioarms3": "522e6cf547f27e7e329a900c21a0324515a8c86a5758dd4dec61397e583aee43",
    "triobounds9": "d030ad258844b352126b7b44baaec585adf1de42962bab1fa75c3ac207adf947",
}

NAVY = "#243B53"
BLUE = "#32689A"
TEAL = "#2A9D8F"
ORANGE = "#D97A2B"
PURPLE = "#7A5195"
GREY = "#6B7280"
LIGHT_BLUE = "#E7EFF8"
LIGHT_ORANGE = "#F9E8D7"
LIGHT_GREY = "#F3F4F6"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def save_figure(fig, outdir: Path, stem: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf", "svg"):
        kwargs = {"dpi": 600} if ext == "png" else {}
        fig.savefig(outdir / f"{stem}.{ext}", bbox_inches="tight", facecolor="white", **kwargs)


def panel_label(ax, label: str) -> None:
    ax.text(-0.04, 1.04, label, transform=ax.transAxes, fontsize=11, fontweight="bold", va="top", ha="left", color=NAVY)


def short_claim(value: str) -> str:
    v = value.upper()
    if v.startswith("POSITIVE_"):
        return "POS"
    if v.startswith("PUBLISHED_NEGATIVE") or v.startswith("NEGATIVE_"):
        return "NEG"
    if v.startswith("PRESPECIFIED_"):
        return "MIX"
    if v.startswith("WITHIN_ARM"):
        return "LIM"
    return "EXP"


def short_fidelity(value: str) -> str:
    for code in ("F0", "F1", "F2", "F3", "F4"):
        if value.upper().startswith(code):
            return code
    return "HIST"


def short_population(row: dict[str, str]) -> str:
    if row["current_role"] == "POPULATION_UNVERIFIED":
        return "UNV"
    v = row["randomization_status"].upper()
    if "AGGREGATE" in v:
        return "AGG"
    if "HETEROGENEOUS" in v:
        return "POOL"
    if "RANDOM" in v:
        return "RCT"
    return "OTHER"


def short_estimand(value: str) -> str:
    v = value.upper()
    if "MISMATCH" in v:
        return "MIS"
    if "NOT_LOCATED" in v or "AUDIT_REQUIRED" in v:
        return "AUD"
    if "MEDIUM_TRANSPORTABILITY" in v:
        return "MED"
    if "NOT_INDEPENDENT" in v:
        return "DEP"
    if "NOT_EXECUTABLE" in v or "APPROXIMATE" in v:
        return "IMP"
    return "ALN"


def short_role(value: str) -> str:
    return {
        "POPULATION_UNVERIFIED": "PU",
        "ROLE_REFRAMED": "RF",
        "TARGETED_REANALYSIS": "TR",
        "NOT_CURRENTLY_EVALUABLE": "NE",
        "IMPLEMENTATION_LIMITED": "IL",
    }[value]


def make_figure1(status: dict, dual: list[dict[str, str]], outdir: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    fig = plt.figure(figsize=(7.2, 7.8), constrained_layout=True)
    grid = fig.add_gridspec(3, 1, height_ratios=[1.15, 0.9, 2.25])

    ax = fig.add_subplot(grid[0])
    ax.axis("off")
    panel_label(ax, "a")
    counts = [
        (status["historical_candidates"], "historical\ncandidates", "lineage only"),
        (status["objects"], "claim–estimand\nobjects", "core audit unit"),
        (status["local_numeric_objects"], "local-numeric\nobjects", "potential reanalysis"),
        (status["historical_primary_models"], "historical\nmodel rows", "dependent rows"),
    ]
    x0 = [0.02, 0.265, 0.51, 0.755]
    for x, (n, label, note) in zip(x0, counts):
        ax.add_patch(FancyBboxPatch((x, 0.16), 0.205, 0.70, boxstyle="round,pad=0.012", facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=1.0))
        ax.text(x + 0.1025, 0.68, str(n), ha="center", va="center", fontsize=20, fontweight="bold", color=NAVY)
        ax.text(x + 0.1025, 0.42, label, ha="center", va="center", fontsize=8.5, color=NAVY, linespacing=1.2)
        ax.text(x + 0.1025, 0.22, note, ha="center", va="center", fontsize=7.2, color=GREY)
    ax.text(0.5, 0.02, "Distinct counting units; not a PRISMA flow or prevalence denominator", ha="center", va="bottom", fontsize=7.5, color=ORANGE)

    ax = fig.add_subplot(grid[1])
    ax.axis("off")
    panel_label(ax, "b")
    chain = ["Published\nclaim", "Source\nevidence", "Executable\nimplementation", "Analysis\npopulation", "Target\nestimand", "Current\nrole"]
    xs = [0.01, 0.175, 0.34, 0.505, 0.67, 0.835]
    for idx, (x, label) in enumerate(zip(xs, chain)):
        ax.add_patch(FancyBboxPatch((x, 0.28), 0.145, 0.46, boxstyle="round,pad=0.01", facecolor="white", edgecolor=TEAL if idx in (0, 5) else BLUE, linewidth=1.0))
        ax.text(x + 0.0725, 0.51, label, ha="center", va="center", fontsize=8.0, color=NAVY)
        if idx < 5:
            ax.annotate("", xy=(xs[idx + 1] - 0.008, 0.51), xytext=(x + 0.151, 0.51), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
    ax.text(0.5, 0.11, "Each dimension is retained separately; no composite readiness score", ha="center", fontsize=7.5, color=GREY)

    ax = fig.add_subplot(grid[2])
    ax.axis("off")
    panel_label(ax, "c")
    d = {row["dimension"]: row for row in dual}
    headers = ["Case", "Source finding", "Permitted action", "Current role"]
    colx = [0.02, 0.18, 0.50, 0.76]
    widths = [0.14, 0.29, 0.23, 0.22]
    for x, w, h in zip(colx, widths, headers):
        ax.add_patch(FancyBboxPatch((x, 0.84), w, 0.11, boxstyle="round,pad=0.008", facecolor=NAVY, edgecolor=NAVY))
        ax.text(x + w / 2, 0.895, h, ha="center", va="center", fontsize=8.0, color="white", fontweight="bold")
    rows = [
        ("TRIO-US B07", "Arm 3 participant phase is not recoverable from public rows", "Preserve historical estimates; no pseudo-corrected interaction", d["current_role"]["TRIO"]),
        ("AVAglio", "Source rules recover 349 → 339 → 333 analysis sets", "Separate population restriction from covariate adjustment", d["current_role"]["AVAglio"]),
    ]
    row_y = [0.52, 0.16]
    fills = [LIGHT_ORANGE, LIGHT_BLUE]
    edges = [ORANGE, BLUE]
    for y, fill, edge, row in zip(row_y, fills, edges, rows):
        for x, w, text_value in zip(colx, widths, row):
            ax.add_patch(FancyBboxPatch((x, y), w, 0.25, boxstyle="round,pad=0.008", facecolor=fill, edgecolor=edge, linewidth=0.9))
            ax.text(x + w / 2, y + 0.125, textwrap.fill(text_value, 28), ha="center", va="center", fontsize=7.2, color=NAVY, linespacing=1.2)
    fig.suptitle("Finite study boundary and two correction pathways", fontsize=12, fontweight="bold", color=NAVY)
    save_figure(fig, outdir, "Figure1_finite_boundary_and_correction_pathways")
    plt.close(fig)


def make_figure2(objects: list[dict[str, str]], outdir: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    context_order = {"HER2_DUAL_BLOCKADE": 0, "TNBC_NEOADJUVANT": 1, "RCC_IO_ANGIO": 2, "GBM_BEVACIZUMAB": 3, "RT_PANCANCER": 4, "EXTENDED_ENDOCRINE": 5}
    context_short = {"HER2_DUAL_BLOCKADE": "HER2", "TNBC_NEOADJUVANT": "TNBC", "RCC_IO_ANGIO": "RCC", "GBM_BEVACIZUMAB": "GBM", "RT_PANCANCER": "RT", "EXTENDED_ENDOCRINE": "BCI"}
    rows = sorted(objects, key=lambda r: (context_order.get(r["context"], 99), r["claim_estimand_id"]))
    columns = ["Use", "Claim", "Fidelity", "Population", "Estimand", "Current role"]
    values = []
    for r in rows:
        values.append([r["original_use_class"], short_claim(r["claim_polarity"]), short_fidelity(r["historical_fidelity_class"]), short_population(r), short_estimand(r["estimand_compatibility"]), short_role(r["current_role"])])
    semantic_colours = {
        "U1": LIGHT_BLUE, "U2": "#DDEFEA", "POS": "#CFE8DF", "NEG": "#E5E7EB", "EXP": LIGHT_ORANGE, "MIX": "#F5E1B8", "LIM": "#E8DDF0",
        "F0": "#CFE8DF", "F1": "#D8E8F5", "F2": "#F5E1B8", "F3": "#E8DDF0", "F4": "#E8DDF0", "HIST": "#E5E7EB",
        "RCT": "#CFE8DF", "AGG": "#E8DDF0", "POOL": "#F5E1B8", "UNV": "#F6D5C1", "OTHER": "#E5E7EB",
        "ALN": "#CFE8DF", "MED": "#D8E8F5", "DEP": "#F5E1B8", "MIS": "#F6D5C1", "AUD": "#E8DDF0", "IMP": "#F5E1B8",
        "TR": "#CFE8DF", "RF": "#D8E8F5", "PU": "#F6D5C1", "NE": "#E8DDF0", "IL": "#F5E1B8",
    }
    fig, ax = plt.subplots(figsize=(8.25, 9.2), constrained_layout=False)
    ax.set_xlim(0, len(columns))
    ax.set_ylim(0, len(rows))
    ax.invert_yaxis()
    for i, rowvals in enumerate(values):
        for j, value in enumerate(rowvals):
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=semantic_colours.get(value, "white"), edgecolor="white", linewidth=1.2))
            ax.text(j + 0.5, i + 0.5, value, ha="center", va="center", fontsize=7.2, color=NAVY, fontweight="bold" if j == 5 else "normal")
    labels = [f"{context_short.get(r['context'], r['context'])} | {r['signature']}" for r in rows]
    ax.set_yticks([i + 0.5 for i in range(len(rows))], labels=labels, fontsize=7.0)
    ax.set_xticks([i + 0.5 for i in range(len(columns))], labels=columns, fontsize=8.0, fontweight="bold")
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False, length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i in range(1, len(rows)):
        if rows[i]["context"] != rows[i - 1]["context"]:
            ax.axhline(i, color=NAVY, lw=1.2)
    ax.set_title("Claim–estimand alignment across 22 frozen objects", fontsize=12, fontweight="bold", color=NAVY, pad=24)
    legend = (
        "Claim: POS positive, NEG negative, EXP exploratory, MIX mixed, LIM limited.  "
        "Fidelity: F0–F4 source classes; HIST historical formula status.\n"
        "Population: RCT randomized context, AGG aggregate only, POOL pooled cohorts, UNV phase unverified.  "
        "Estimand: ALN aligned, MED medium transportability, DEP dependent, MIS mismatch, AUD audit required, IMP implementation-limited.\n"
        "Current role: TR targeted reanalysis, RF reframed, PU population-unverified, NE not currently evaluable, IL implementation-limited."
    )
    fig.text(0.02, 0.005, legend, ha="left", va="bottom", fontsize=6.5, color=GREY, linespacing=1.35)
    fig.subplots_adjust(left=0.31, right=0.98, top=0.91, bottom=0.13)
    save_figure(fig, outdir, "Figure2_claim_estimand_alignment_matrix")
    plt.close(fig)


def make_figure3(ladder: list[dict[str, str]], outdir: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    by_claim = {cid: [r for r in ladder if r["claim_id"] == cid] for cid in ("GBM_01", "GBM_02")}
    fig = plt.figure(figsize=(7.2, 8.0), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[0.85, 1.45])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_d = fig.add_subplot(gs[0, 1])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    ax_a.axis("off")
    panel_label(ax_a, "a")
    nodes = [(0.02, "349 / 270", "expression-\nevaluable\nA0"), (0.36, "339 / 265", "IDH1 wild type\nA1"), (0.70, "333 / 260", "fixed complete\ncases\nA2/A3")]
    for x, num, label in nodes:
        ax_a.add_patch(FancyBboxPatch((x, 0.25), 0.25, 0.48, boxstyle="round,pad=0.012", facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=1.0))
        ax_a.text(x + 0.125, 0.56, num, ha="center", fontsize=10, fontweight="bold", color=NAVY)
        ax_a.text(x + 0.125, 0.37, label, ha="center", fontsize=6.8, color=NAVY)
    for x1, x2, note in [(0.27, 0.36, "−10 IDH1-mutant"), (0.61, 0.70, "−6 literal-NA rows")]:
        ax_a.annotate("", xy=(x2, 0.49), xytext=(x1, 0.49), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
        ax_a.text((x1 + x2) / 2, 0.16, note, ha="center", fontsize=5.8, color=GREY)
    ax_a.text(0.03, 0.86, "Analysis-population pathway", fontsize=9, fontweight="bold", color=NAVY)

    def forest(ax, claim_id: str, title: str, label: str) -> None:
        rows = sorted([r for r in by_claim[claim_id] if r["model_id"] in {"A0", "A1", "A2", "A3"}], key=lambda r: r["model_id"])
        y = list(range(len(rows), 0, -1))
        for yy, r in zip(y, rows):
            hr = float(r["current_interaction_hr"]); lo = float(r["current_ci95_low"]); hi = float(r["current_ci95_high"])
            color = TEAL if r["model_id"] == "A3" else BLUE
            ax.plot([lo, hi], [yy, yy], color=color, lw=1.4)
            ax.scatter([hr], [yy], s=28, color=color, edgecolor="white", linewidth=0.5, zorder=3)
            ax.text(2.25, yy, f"P={float(r['current_interaction_p']):.3g}", fontsize=6.5, va="center", ha="right", color=GREY)
        ax.axvline(1, color=GREY, lw=0.9, ls="--")
        ax.set_xscale("log")
        ax.set_xlim(0.2, 2.4)
        ax.set_xticks([0.25, 0.5, 1, 2], labels=["0.25", "0.5", "1", "2"])
        ax.set_yticks(y, labels=[f"{r['model_id']} (n={r['current_n']})" for r in rows], fontsize=7)
        ax.set_xlabel("Interaction HR (log scale)", fontsize=7.5)
        ax.set_title(title, fontsize=9, fontweight="bold", color=NAVY)
        ax.tick_params(axis="x", labelsize=7)
        ax.grid(axis="x", color="#E5E7EB", lw=0.6)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        panel_label(ax, label)

    forest(ax_b, "GBM_01", "Phillips proneural", "b")
    forest(ax_c, "GBM_02", "Verhaak proneural", "c")

    panel_label(ax_d, "d")
    ax_d.axvline(1, color=GREY, lw=0.8, ls="--")
    labels, ys = [], []
    idx = 0
    for claim_id, short in (("GBM_01", "Phillips"), ("GBM_02", "Verhaak")):
        for model in ("A3", "A4"):
            r = next(x for x in by_claim[claim_id] if x["model_id"] == model)
            y = 4 - idx
            hr = float(r["current_interaction_hr"]); lo = float(r["current_ci95_low"]); hi = float(r["current_ci95_high"])
            marker = "o" if model == "A3" else "D"
            face = TEAL if model == "A3" else "white"
            ax_d.plot([lo, hi], [y, y], color=TEAL if model == "A3" else PURPLE, lw=1.1)
            ax_d.scatter([hr], [y], marker=marker, s=25, facecolor=face, edgecolor=TEAL if model == "A3" else PURPLE, linewidth=1.0, zorder=3)
            labels.append(f"{short} {model}")
            ys.append(y)
            idx += 1
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter
    ax_d.set_xscale("log"); ax_d.set_xlim(0.2, 2.0)
    ax_d.xaxis.set_major_locator(FixedLocator([0.25, 0.5, 1, 2]))
    ax_d.xaxis.set_major_formatter(FixedFormatter(["0.25", "0.5", "1", "2"]))
    ax_d.xaxis.set_minor_formatter(NullFormatter())
    ax_d.tick_params(axis="x", labelsize=6.5)
    ax_d.set_yticks(ys, labels=labels, fontsize=6.5)
    ax_d.set_title("A4 alternative branch", fontsize=9, fontweight="bold", color=NAVY)
    ax_d.set_xlabel("Interaction HR", fontsize=6.5)
    ax_d.grid(axis="x", color="#E5E7EB", lw=0.5)
    for side in ("top", "right", "left"):
        ax_d.spines[side].set_visible(False)
    ax_d.text(0.5, -0.23, "A3: fixed 333, adjusted\nA4: 339, ridge + explicit missing levels", transform=ax_d.transAxes, ha="center", fontsize=6.2, color=GREY)

    fig.suptitle("AVAglio population and model-specification ladder", fontsize=12, fontweight="bold", color=NAVY)
    save_figure(fig, outdir, "Figure3_AVAglio_population_model_ladder")
    plt.close(fig)


def make_figure4(cross: list[dict[str, str]], absolute: list[dict[str, str]], bounds: list[dict[str, str]], outdir: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    clusters = Counter(r["dependency_cluster_id"] for r in cross)
    cluster_names = {
        "HER2_TRIO_B07_CHER_LOB": "HER2\nTRIO–CHER-LOB",
        "GBM_AVAGLIO_GLARIUS": "GBM\nAVAglio–GLARIUS",
        "TNBC_CALGB40603_BRIGHTNESS": "TNBC\nIGG14–BrighTNess",
    }
    order = ["HER2_TRIO_B07_CHER_LOB", "GBM_AVAGLIO_GLARIUS", "TNBC_CALGB40603_BRIGHTNESS"]
    fig = plt.figure(figsize=(7.2, 7.7), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1.15])
    ax_a = fig.add_subplot(gs[0, 0]); ax_b = fig.add_subplot(gs[0, 1]); ax_c = fig.add_subplot(gs[1, :])

    ax_a.axis("off"); panel_label(ax_a, "a")
    ax_a.set_title("Historical units are clustered", fontsize=9, fontweight="bold", color=NAVY)
    ys = [0.68, 0.39, 0.10]
    colours = [LIGHT_ORANGE, LIGHT_BLUE, "#E8DDF0"]
    edges = [ORANGE, BLUE, PURPLE]
    for y, key, fc, ec in zip(ys, order, colours, edges):
        ax_a.add_patch(FancyBboxPatch((0.08, y), 0.84, 0.20, boxstyle="round,pad=0.012", facecolor=fc, edgecolor=ec, linewidth=1.0))
        ax_a.text(0.22, y + 0.10, str(clusters[key]), fontsize=18, fontweight="bold", color=NAVY, ha="center", va="center")
        ax_a.text(0.60, y + 0.10, cluster_names[key], fontsize=8.0, color=NAVY, ha="center", va="center")
    ax_a.text(0.5, 0.01, "13 units in 3 dependency clusters; not 13 independent replications", ha="center", fontsize=6.8, color=GREY)

    panel_label(ax_b, "b")
    hist = [clusters[k] for k in order] + [len(cross)]
    current = [0, 0, 0, sum(r["current_verified_strict_denominator_member"].upper() == "TRUE" for r in cross)]
    labels = ["HER2", "GBM", "TNBC", "Total"]
    y = list(range(len(labels)))
    ax_b.barh([v + 0.17 for v in y], hist, height=0.30, color=BLUE, label="Historical member")
    ax_b.barh([v - 0.17 for v in y], current, height=0.30, color=ORANGE, label="Current verified")
    for yy, value in zip([v + 0.17 for v in y], hist):
        ax_b.text(value + 0.2, yy, str(value), va="center", fontsize=7, color=NAVY)
    for yy, value in zip([v - 0.17 for v in y], current):
        ax_b.text(value + 0.2, yy, str(value), va="center", fontsize=7, color=NAVY)
    ax_b.set_yticks(y, labels=labels, fontsize=7.5); ax_b.invert_yaxis(); ax_b.set_xlim(0, 14.5)
    ax_b.set_xlabel("Number of units", fontsize=7.5)
    ax_b.set_title("Membership is version-specific", fontsize=9, fontweight="bold", color=NAVY, pad=30)
    ax_b.legend(frameon=False, fontsize=6.8, loc="upper right")
    ax_b.grid(axis="x", color="#E5E7EB", lw=0.5)
    for side in ("top", "right", "left"):
        ax_b.spines[side].set_visible(False)
    ax_b.text(0.02, 1.015, "Current strict proportion: NOT ESTIMABLE", transform=ax_b.transAxes, ha="left", va="bottom", fontsize=6.6, color=ORANGE, fontweight="bold")

    ax_c.axis("off"); panel_label(ax_c, "c")
    nominal = [r for r in absolute if r["additive_nominal"].strip().lower() == "true"]
    robust = [r for r in absolute if r["additive_multiplicity_robust"].strip().lower() == "true"]
    min_n = min(int(r["randomized_n_in_public_arm3"]) for r in bounds); max_n = max(int(r["randomized_n_in_public_arm3"]) for r in bounds)
    pmin = min(float(r["raw_pcr_proportion_min"]) for r in bounds); pmax = max(float(r["raw_pcr_proportion_max"]) for r in bounds)
    ax_c.add_patch(FancyBboxPatch((0.03, 0.13), 0.45, 0.72, boxstyle="round,pad=0.015", facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=1.0))
    ax_c.add_patch(FancyBboxPatch((0.52, 0.13), 0.45, 0.72, boxstyle="round,pad=0.015", facecolor=LIGHT_ORANGE, edgecolor=ORANGE, linewidth=1.0))
    ax_c.text(0.255, 0.75, "Absolute-effect sensitivity", ha="center", fontsize=9, fontweight="bold", color=NAVY)
    ax_c.text(0.12, 0.52, str(len(absolute)), ha="center", fontsize=24, fontweight="bold", color=BLUE)
    ax_c.text(0.255, 0.52, str(len(nominal)), ha="center", fontsize=24, fontweight="bold", color=ORANGE)
    ax_c.text(0.39, 0.52, str(len(robust)), ha="center", fontsize=24, fontweight="bold", color=TEAL)
    ax_c.text(0.12, 0.38, "models", ha="center", fontsize=7, color=GREY)
    ax_c.text(0.255, 0.38, "nominal", ha="center", fontsize=7, color=GREY)
    ax_c.text(0.39, 0.38, "multiplicity-robust", ha="center", fontsize=7, color=GREY)
    if nominal:
        ax_c.text(0.255, 0.23, f"{nominal[0]['signature']}: q={float(nominal[0]['bootstrap_bh_q_within_family']):.3f}; does not promote replication", ha="center", fontsize=6.8, color=NAVY)
    ax_c.text(0.745, 0.75, "TRIO aggregate compatibility", ha="center", fontsize=9, fontweight="bold", color=NAVY)
    ax_c.text(0.745, 0.56, f"possible randomized Arm 3 n = {min_n}–{max_n}", ha="center", fontsize=10, fontweight="bold", color=ORANGE)
    ax_c.text(0.745, 0.42, f"raw pCR proportion = {100*pmin:.1f}–{100*pmax:.1f}%", ha="center", fontsize=10, fontweight="bold", color=ORANGE)
    ax_c.text(0.745, 0.25, "Conditional integer range only\nNot a confidence interval or interaction bound", ha="center", fontsize=7.2, color=NAVY)
    ax_c.set_title("Supporting sensitivity results retain their inferential boundaries", fontsize=9.5, fontweight="bold", color=NAVY)

    fig.suptitle("Historical replay and current evidentiary eligibility", fontsize=12, fontweight="bold", color=NAVY)
    save_figure(fig, outdir, "Figure4_historical_replay_and_current_eligibility")
    plt.close(fig)


def make_contact_sheet(outdir: Path) -> None:
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    stems = [
        "Figure1_finite_boundary_and_correction_pathways",
        "Figure2_claim_estimand_alignment_matrix",
        "Figure3_AVAglio_population_model_ladder",
        "Figure4_historical_replay_and_current_eligibility",
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 11.0), constrained_layout=True)
    for ax, stem in zip(axes.flat, stems):
        ax.imshow(mpimg.imread(outdir / f"{stem}.png"))
        ax.axis("off")
        ax.set_title(stem.split("_")[0], fontsize=10, fontweight="bold", color=NAVY)
    fig.savefig(outdir / "V4_S5_Figure1_4_contact_sheet.png", dpi=250, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.linewidth": 0.7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })
    parser = argparse.ArgumentParser()
    for key in EXPECTED:
        parser.add_argument("--" + key.replace("_", "-"), dest=key, type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.output_root.resolve()
    for sub in ("source_data", "tables", "figures", "audit"):
        (root / sub).mkdir(parents=True, exist_ok=True)

    paths = {key: getattr(args, key).resolve() for key in EXPECTED}
    manifest = []
    data: dict[str, object] = {}
    for key, path in paths.items():
        observed = digest(path)
        if observed != EXPECTED[key]:
            raise ValueError(f"Hash mismatch for {key}: {observed}")
        if path.suffix.lower() == ".json":
            data[key] = json.loads(path.read_text(encoding="utf-8"))
            rows = 1
        else:
            data[key] = read_tsv(path)
            rows = len(data[key])
        manifest.append({"source_key": key, "rows": rows, "bytes": path.stat().st_size, "sha256": observed, "role": "READ_ONLY_FROZEN_INPUT", "raw_copy_in_delivery": "NO"})
    write_tsv(root / "source_data" / "V4_S5_source_manifest.tsv", manifest)

    objects = data["objects22"]
    ladder = data["avaglio10"]
    cross = data["cross13"]
    absolute = data["absolute23"]
    status = data["s4status"]

    table1_fields = ["claim_estimand_id", "legacy_claim_id", "context", "signature", "original_use_class", "claim_polarity", "historical_fidelity_class", "randomization_status", "estimand_compatibility", "current_role", "main_text_role", "figure_assignments"]
    write_tsv(root / "tables" / "Table1_V4_S5_claim_estimand_summary_22objects.tsv", [{k: r[k] for k in table1_fields} for r in objects], table1_fields)
    write_tsv(root / "tables" / "Supplementary_Table_S1_AVAglio_A0_A4_10rows.tsv", ladder)
    write_tsv(root / "tables" / "Supplementary_Table_S2_cross_trial_historical_current_13rows.tsv", cross)
    abs_current = []
    for r in absolute:
        out = dict(r)
        out["v4_s5_current_role"] = "POPULATION_UNVERIFIED_SCALE_SENSITIVITY" if r["trial"] == "TRIO-US B07" else "STANDALONE_TRIAL_SPECIFIC_SCALE_SENSITIVITY"
        out["v4_s5_primary_label_mutated"] = "FALSE"
        abs_current.append(out)
    write_tsv(root / "tables" / "Supplementary_Table_S3_absolute_effect_current_role_23rows.tsv", abs_current)

    make_figure1(status, data["dual8"], root / "figures")
    make_figure2(objects, root / "figures")
    make_figure3(ladder, root / "figures")
    make_figure4(cross, absolute, data["triobounds9"], root / "figures")
    make_contact_sheet(root / "figures")

    figure_inventory = []
    panel_counts = {"Figure1": 3, "Figure2": 3, "Figure3": 4, "Figure4": 3}
    stems = {
        "Figure1": "Figure1_finite_boundary_and_correction_pathways",
        "Figure2": "Figure2_claim_estimand_alignment_matrix",
        "Figure3": "Figure3_AVAglio_population_model_ladder",
        "Figure4": "Figure4_historical_replay_and_current_eligibility",
    }
    for fig_id, stem in stems.items():
        for ext in ("png", "pdf", "svg"):
            path = root / "figures" / f"{stem}.{ext}"
            figure_inventory.append({"figure_id": fig_id, "panels": panel_counts[fig_id], "format": ext.upper(), "relative_path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)})
    write_tsv(root / "audit" / "V4_S5_figure_inventory.tsv", figure_inventory)

    final = {
        "stage": "V4_S5_MANUSCRIPT_AND_FIGURE_REBUILD",
        "date": "2026-10-11",
        "source_hashes_pass": True,
        "figures": 4,
        "figure_panels": sum(panel_counts.values()),
        "figure_formats_each": ["PNG_600DPI", "PDF_VECTOR", "SVG_VECTOR"],
        "objects": len(objects),
        "avaglio_rows": len(ladder),
        "cross_trial_units": len(cross),
        "absolute_effect_rows": len(absolute),
        "new_statistical_refit": False,
        "historical_labels_mutated": False,
        "trio_corrected_randomized_model": False,
        "submission": "HOLD",
    }
    (root / "audit" / "V4_S5_build_status.json").write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(final, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

