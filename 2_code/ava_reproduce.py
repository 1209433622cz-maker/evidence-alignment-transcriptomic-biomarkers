#!/usr/bin/env python3
"""Portable GSE84010 metadata -> frozen population rules -> eight A0-A3 Cox fits.

No expression/centroid assay reconstruction, new specification search, bootstrap,
or A4 ridge fit. Participant rows are read locally and never exported.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import importlib.metadata as md
import json
import platform
import sys
import urllib.request
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.duration.hazard_regression import PHReg
from lifelines import CoxPHFitter

GEO_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE84nnn/GSE84010/matrix/GSE84010_series_matrix.txt.gz"
RAW_SHA = "3af8c7a112d6193e79b68d2d768353fa8231cd49d17aa0f18077443db1b8b178"
COV = ["age", "corticosteroids", "surgical_status", "sex", "kps", "mgmt_status", "mmse", "rpa_class", "who"]
REQ = ["geo_accession", "sample_title", "idh1_status", "phillips_subtype", "tcga_subtype", "treatment", *COV,
       "os_time_to_event_(months)", "os_event_type_(0_=_censored)"]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(2**20), b""):
            h.update(b)
    return h.hexdigest()


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def parse_series(path):
    samples, columns = [], {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            row = next(csv.reader([line], delimiter="\t"))
            if not row:
                continue
            if row[0] == "!Sample_geo_accession":
                samples = row[1:]
            elif row[0] == "!Sample_title":
                columns["sample_title"] = row[1:]
            elif row[0] == "!Sample_characteristics_ch1":
                parts = [s.split(": ", 1) for s in row[1:]]
                require(all(len(p) == 2 for p in parts), "Unparseable characteristic")
                name = parts[0][0].lower().replace(" ", "_")
                require(all(p[0].lower().replace(" ", "_") == name for p in parts), "Characteristic key changes within row")
                require(name not in columns, "Duplicate characteristic key: " + name)
                columns[name] = [p[1] for p in parts]
    require(len(samples) == 349 and len(set(samples)) == 349, "Expected 349 unique deposited samples")
    require(all(len(v) == len(samples) for v in columns.values()), "Unequal metadata lengths")
    out = pd.DataFrame(columns, index=samples).rename_axis("geo_accession").reset_index()
    require(set(REQ).issubset(out.columns), "Required metadata fields missing")
    require(out.idh1_status.value_counts().to_dict() == {"Wild type": 339, "Mutant": 10}, "IDH1 census mismatch")
    require(set(out.treatment) == {"Bevacizumab", "Placebo"}, "Unexpected treatment labels")
    require(set(out.phillips_subtype.str.casefold()) == {"proneural", "proliferative", "mesenchymal", "unclassified"}, "Phillips label mismatch")
    require(set(out.tcga_subtype.str.casefold()) == {"proneural", "neural", "classical", "mesenchymal", "unclassified"}, "Verhaak label mismatch")
    for c in ["os_time_to_event_(months)", "os_event_type_(0_=_censored)", "age"]:
        require(np.isfinite(pd.to_numeric(out[c], errors="raise")).all(), "Nonfinite " + c)
    require((pd.to_numeric(out["os_time_to_event_(months)"]) > 0).all(), "Nonpositive OS time")
    require(set(out["os_event_type_(0_=_censored)"]) <= {"0", "1"}, "Death coding changed")
    return out


def populations(source):
    wt = source.loc[source.idh1_status.eq("Wild type")].copy()
    cc = wt.loc[~wt[COV].eq("NA").any(axis=1)].copy()
    # 'Missing' is a genuine deposited MGMT level, NOT pandas NA.
    require(len(cc) == 333, "Frozen literal-NA restriction must yield 333")
    require(int(cc.mgmt_status.eq("Missing").sum()) == 68, "MGMT Missing level not retained")
    frames = {"A0": source, "A1": wt, "A2": cc, "A3": cc}
    for key, expected in {"A0": (349, 270), "A1": (339, 265), "A2": (333, 260), "A3": (333, 260)}.items():
        d = frames[key]
        require((len(d), int(pd.to_numeric(d["os_event_type_(0_=_censored)"]).sum())) == expected, "Population mismatch " + key)
    require(cc.treatment.value_counts().to_dict() == {"Placebo": 171, "Bevacizumab": 162}, "Fixed333 treatment mismatch")
    return frames


def design_for(data, label, adjusted):
    marker = data[label].str.casefold().eq("proneural").astype(float)
    treatment = data.treatment.eq("Bevacizumab").astype(float)
    x = pd.DataFrame({"marker": marker, "treatment": treatment, "interaction": marker * treatment}, index=data.index)
    category_specs = {}
    removed = []
    if adjusted:
        x["age"] = pd.to_numeric(data.age, errors="raise")
        cats = data[COV[1:]].copy()
        require(~cats.eq("").any().any(), "Empty clinical category is not allowed")
        for c in COV[1:]:
            levels = sorted(cats[c].unique())
            category_specs[c] = {"levels_lexicographic": levels, "reference": levels[0]}
            cats[c] = pd.Categorical(cats[c], categories=levels)
        dummy = pd.get_dummies(cats, prefix=COV[1:], drop_first=True, dtype=float)
        removed = [c for c in dummy if dummy[c].nunique() <= 1]
        x = pd.concat([x, dummy.drop(columns=removed)], axis=1)
    arr = x.to_numpy(float)
    require(np.isfinite(arr).all(), "Nonfinite design")
    require(np.linalg.matrix_rank(arr) == arr.shape[1], "Rank deficient design")
    t = pd.to_numeric(data["os_time_to_event_(months)"]).to_numpy(float)
    event = pd.to_numeric(data["os_event_type_(0_=_censored)"]).to_numpy(int)
    membership = hashlib.sha256("\n".join(sorted(data.geo_accession)).encode()).hexdigest()
    spec = {"columns": list(x.columns), "n_parameters": len(x.columns), "rank": int(np.linalg.matrix_rank(arr)),
            "condition_number": float(np.linalg.cond(arr)), "category_encoding": category_specs,
            "constant_dummy_columns_removed": removed, "membership_sha256": membership,
            "ties": "Efron", "penalizer": 0.0, "T1": "Bevacizumab", "T0": "Placebo",
            "M1": "Proneural deposited label", "M0": "All other deposited labels including Unclassified (frozen local coding)",
            "deposited_label_counts": data[label].value_counts().to_dict(), "outcome": "OS months; death=1"}
    return x, t, event, spec


def fit_pair(x, t, event):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        ph = PHReg(t, x.to_numpy(), status=event, ties="efron").fit(method="newton", maxiter=1000, tol=1e-12)
        frame = x.copy()
        frame["duration"], frame["event"] = t, event
        lf = CoxPHFitter(penalizer=0.0)
        lf.fit(frame, duration_col="duration", event_col="event", batch_mode=False, show_progress=False,
               fit_options={"precision": 1e-12, "r_precision": 1e-12, "max_steps": 1000})
    if any("converg" in str(w.message).lower() for w in caught):
        raise RuntimeError("Convergence warning: " + " | ".join(str(w.message) for w in caught))
    b, se = float(ph.params[2]), float(ph.bse[2])
    z = norm.ppf(.975)
    p1 = dict(beta=b, se=se, hr=float(np.exp(b)), ci_low=float(np.exp(b-z*se)), ci_high=float(np.exp(b+z*se)), p=float(2*norm.sf(abs(b/se))))
    row = lf.summary.loc["interaction"]
    p2 = dict(beta=float(row["coef"]), se=float(row["se(coef)"]), hr=float(row["exp(coef)"]),
              ci_low=float(row["exp(coef) lower 95%"]), ci_high=float(row["exp(coef) upper 95%"]), p=float(row["p"]))
    require(np.isfinite(list(p1.values()) + list(p2.values())).all(), "Nonfinite model result")
    diff = max(abs(p1[k]-p2[k]) for k in p1)
    require(diff < 1e-7, "Tight cross-engine mismatch: " + str(diff))
    return p1, p2, diff, [str(w.message) for w in caught]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series-matrix", type=Path, help="Existing gzipped GSE84010 series matrix")
    parser.add_argument("--download", action="store_true", help="Use the official public FTP HTTPS endpoint")
    parser.add_argument("--ack-use-and-no-redistribution", action="store_true")
    parser.add_argument("--frozen-ladder", type=Path, required=True, help="Aggregate avaglio10.tsv; never modified")
    parser.add_argument("--output-dir", type=Path, required=True, help="New/empty directory")
    args = parser.parse_args()
    require(bool(args.series_matrix) != args.download, "Choose exactly one of --series-matrix / --download")
    out = args.output_dir.resolve()
    require(not out.exists() or not any(out.iterdir()), "Output must be new/empty; do not overwrite an old run")
    out.mkdir(parents=True, exist_ok=True)
    try:
        if args.download:
            require(args.ack_use_and_no_redistribution, "Confirm local use/no redistribution")
            raw = out / "LOCAL_INPUT_DO_NOT_RELEASE" / "GSE84010_series_matrix.txt.gz"
            raw.parent.mkdir()
            urllib.request.urlretrieve(GEO_URL, raw)
        else:
            raw = args.series_matrix.resolve()
        require(sha(raw) == RAW_SHA, "Raw release SHA differs; STOP rather than substitute a changed release")
        frozen_hash = sha(args.frozen_ladder)
        source = parse_series(raw)
        frames = populations(source)
        frozen = pd.read_csv(args.frozen_ladder, sep="\t", dtype=str, keep_default_na=False)
        require(len(frozen) == 10, "Expected unchanged ten-model ladder")
        results, specs = [], {}
        for claim, label in [("GBM_01", "phillips_subtype"), ("GBM_02", "tcga_subtype")]:
            for aid, d in frames.items():
                x, t, event, spec = design_for(d, label, aid == "A3")
                p1, p2, diff, fit_warnings = fit_pair(x, t, event)
                r = frozen.loc[frozen.claim_id.eq(claim) & frozen.model_id.eq(aid)]
                require(len(r) == 1, "Ladder key missing/duplicate")
                expected = r.iloc[0]
                keys = {"hr": "current_interaction_hr", "ci_low": "current_ci95_low", "ci_high": "current_ci95_high", "p": "current_interaction_p"}
                hist_diff = max(abs(p1[k]-float(expected[v])) for k,v in keys.items())
                status = "STRICT_HISTORY_NUMERIC_PASS"
                default_diff = None
                if hist_diff >= 1e-5:
                    # Only the previously identified A1 Verhaak optimizer precision
                    # discrepancy is allowed. No post-hoc tolerance relaxation.
                    require((claim, aid) == ("GBM_02", "A1") and hist_diff < 5e-5,
                            "Unexpected historical mismatch; no automatic relabel/replacement")
                    f = x.copy(); f["duration"], f["event"] = t, event
                    default = CoxPHFitter(penalizer=0).fit(f, duration_col="duration", event_col="event")
                    dr = default.summary.loc["interaction"]
                    dk = {"hr": "exp(coef)", "ci_low": "exp(coef) lower 95%", "ci_high": "exp(coef) upper 95%", "p": "p"}
                    default_diff = max(abs(float(dr[dk[k]])-float(expected[v])) for k,v in keys.items())
                    require(default_diff < 1e-9, "Known default-precision qualification not reproduced")
                    status = "QUALIFIED_KNOWN_DEFAULT_OPTIMIZER_PRECISION"
                require(len(d) == int(expected.current_n) and int(event.sum()) == int(expected.current_events), "Historical census mismatch")
                results.append({"claim_id": claim, "model_id": aid, "n": len(d), "events": int(event.sum()),
                                "phreg_interaction_hr": p1["hr"], "phreg_ci95_low": p1["ci_low"], "phreg_ci95_high": p1["ci_high"], "phreg_p": p1["p"],
                                "lifelines_interaction_hr": p2["hr"], "lifelines_ci95_low": p2["ci_low"], "lifelines_ci95_high": p2["ci_high"], "lifelines_p": p2["p"],
                                "cross_engine_max_abs_diff": diff, "historical_max_abs_diff": hist_diff, "historical_status": status,
                                "historical_default_fit_max_abs_diff": default_diff, "fit_warnings": " | ".join(fit_warnings),
                                "interpretation": "SAME_TRIAL_SPECIFICATION_CHECK_NOT_EXTERNAL_VALIDATION"})
                specs[claim+"::"+aid] = spec
                print(claim, aid, len(d), "cross-engine", f"{diff:.3g}", status, flush=True)
        require(sha(raw) == RAW_SHA and sha(args.frozen_ladder) == frozen_hash, "Inputs changed during run")
        pd.DataFrame(results).to_csv(out/"AVA_A0_A3_recipe_results.tsv", sep="\t", index=False, float_format="%.15g")
        (out/"DESIGN_AND_ENCODING.json").write_text(json.dumps(specs, indent=2), encoding="utf-8")
        require(specs["GBM_01::A2"]["membership_sha256"] == specs["GBM_01::A3"]["membership_sha256"], "A2/A3 membership differs")
        status = {"status": "PASS_WITH_KNOWN_HISTORICAL_PRECISION_QUALIFICATION", "at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                  "raw_input_sha256": RAW_SHA, "frozen_ladder_sha256": frozen_hash, "script_sha256": sha(__file__),
                  "official_input_url": GEO_URL, "selected_specifications": 8, "tight_model_fits": 16, "default_precision_diagnostic_fits": 1,
                  "cross_engine_agreement": "8/8 at absolute 1e-7", "strict_vs_historical": "7/8 at 1e-5; one pre-existing qualified A1 Verhaak",
                  "population_n_deaths": {k: [len(d), int(pd.to_numeric(d['os_event_type_(0_=_censored)']).sum())] for k,d in frames.items()},
                  "same_set_A2_A3": True, "MGMT_Missing_retained": 68, "WT_literal_NA_exclusions": 6,
                  "original_centroid_assay_executed": False, "A4_fitted": False, "participant_rows_exported": False,
                  "bootstrap_fits": 0, "historical_files_modified": False,
                  "software": {"python": sys.version, "platform": platform.platform(), **{x: md.version(x) for x in ["numpy","pandas","scipy","statsmodels","lifelines"]}},
                  "outputs_sha256": {p.name: sha(p) for p in out.iterdir() if p.is_file()}}
        (out/"RECIPE_RUN_STATUS.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
        print(json.dumps({k:v for k,v in status.items() if k not in {"software", "outputs_sha256"}}, indent=2))
    except Exception as exc:
        (out/"FAILED_RUN.json").write_text(json.dumps({"type": type(exc).__name__, "error": str(exc), "no_result_promotion": True}, indent=2), encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
