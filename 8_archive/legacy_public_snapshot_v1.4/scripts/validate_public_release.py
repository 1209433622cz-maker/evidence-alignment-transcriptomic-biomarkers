#!/usr/bin/env python3
"""Fail-closed validator for the current aggregate-only public repository."""

from __future__ import annotations

import csv
import ast
import gzip
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST_SHA256.tsv"
TEXT_SUFFIXES = {".cff", ".csv", ".json", ".md", ".ps1", ".py", ".r", ".svg", ".tsv", ".txt", ".yaml", ".yml"}
TEXT_FILENAMES = {".gitignore", ".gitattributes", "LICENSE"}
FORBIDDEN_DIRS = {"raw_data", "participant_level", "patient_level", "restricted_internal", "node_modules", ".venv", "__pycache__"}
FORBIDDEN_PATH = re.compile(r"(?i)(?:(?<![A-Za-z0-9])[A-Z]:[\\/]|/mnt/data/|Users\\Administrator|sandbox:/mnt/data)")
SECRET = re.compile(r"\b(?:gh[opusr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b")
IDENTIFIER_COLUMNS = {"patient_id", "participant_id", "sample_id", "subject_id", "mrn"}


def canonical_bytes(path: Path) -> bytes:
    payload = path.read_bytes()
    if path.suffix.casefold() in TEXT_SUFFIXES or path.name in TEXT_FILENAMES:
        payload = payload.replace(b"\r\n", b"\n")
    return payload


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def close(a: str, b: float, tolerance: float = 1e-9) -> bool:
    return math.isclose(float(a), b, rel_tol=tolerance, abs_tol=tolerance)


def add(checks: list[dict[str, object]], name: str, passed: bool, detail: object) -> None:
    checks.append({"name": name, "pass": bool(passed), "detail": detail})


def check_manifest(checks: list[dict[str, object]]) -> None:
    rows = read_tsv(MANIFEST)
    failures = []
    for row in rows:
        path = ROOT / row["relative_path"]
        if not path.is_file():
            failures.append(f"missing:{row['relative_path']}")
            continue
        payload = canonical_bytes(path)
        if len(payload) != int(row["size_bytes"]):
            failures.append(f"size:{row['relative_path']}")
        if hashlib.sha256(payload).hexdigest() != row["sha256"]:
            failures.append(f"hash:{row['relative_path']}")
    add(checks, "manifest", not failures, {"rows": len(rows), "failures": failures[:10]})
    excluded={".git", "__pycache__", ".pytest_cache", ".venv", "node_modules"}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p!=MANIFEST and not any(x in excluded for x in p.relative_to(ROOT).parts) and p.suffix.casefold()!=".pyc"}
    listed={r["relative_path"] for r in rows}
    add(checks,"manifest_full_coverage",actual==listed and len(listed)==len(rows),{"unlisted":sorted(actual-listed),"missing":sorted(listed-actual),"duplicate_rows":len(rows)-len(listed)})


def main() -> None:
    checks: list[dict[str, object]] = []
    if not MANIFEST.is_file():
        raise FileNotFoundError("MANIFEST_SHA256.tsv missing; run scripts/build_manifest.py")
    check_manifest(checks)

    files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts and p.suffix.casefold() != ".pyc"]
    forbidden_paths = [p.relative_to(ROOT).as_posix() for p in files if any(part.casefold() in FORBIDDEN_DIRS for part in p.relative_to(ROOT).parts)]
    add(checks, "no_forbidden_directories", not forbidden_paths, forbidden_paths[:10])

    path_leaks: list[str] = []
    secret_hits: list[str] = []
    for path in files:
        if path.suffix.casefold() not in TEXT_SUFFIXES and path.name not in TEXT_FILENAMES:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        if path.name != "validate_public_release.py" and FORBIDDEN_PATH.search(text):
            path_leaks.append(path.relative_to(ROOT).as_posix())
        if SECRET.search(text):
            secret_hits.append(path.relative_to(ROOT).as_posix())
    add(checks, "no_local_absolute_paths", not path_leaks, path_leaks)
    add(checks, "no_embedded_secrets", not secret_hits, secret_hits)

    bad_headers = []
    for directory in (ROOT / "results", ROOT / "source_data", ROOT / "supplementary_csv", ROOT / "public_reproduction_v1_4"):
        for path in directory.rglob("*"):
            if not path.is_file() or path.suffix.casefold() not in {".tsv", ".csv"}:
                continue
            with path.open(encoding="utf-8-sig", newline="") as handle:
                header = next(csv.reader(handle, delimiter="\t" if path.suffix.casefold()==".tsv" else ","), [])
            overlap = IDENTIFIER_COLUMNS.intersection(h.casefold() for h in header)
            if overlap:
                bad_headers.append(f"{path.relative_to(ROOT).as_posix()}:{sorted(overlap)}")
    add(checks, "aggregate_only_headers", not bad_headers, bad_headers)

    forbidden_names = {"GSE84010_sample_characteristics.tsv", "V4_S2_A2_top5_influential_records_R_RESTRICTED.tsv", "V4_S2_A2_top5_influential_records_lifelines_RESTRICTED.tsv"}
    restricted_present = [p.relative_to(ROOT).as_posix() for p in files if p.name in forbidden_names]
    add(checks, "restricted_inputs_absent", not restricted_present, restricted_present)
    add(checks, "private_docx_absent", not list(ROOT.rglob("*.docx")), [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.docx")])

    historical = read_tsv(ROOT / "results" / "binary_absolute_effect_23models.tsv")
    pass_n = sum(r["bootstrap_status"] == "PASS" for r in historical)
    warn_n = sum(r["bootstrap_status"] == "WARN_CONDITIONAL_PERCENTILE" for r in historical)
    nominal_n = sum(r["additive_nominal"].casefold() == "true" for r in historical)
    robust_n = sum(r["additive_multiplicity_robust"].casefold() == "true" for r in historical)
    changed_n = sum(r["primary_label_unchanged"].casefold() != "true" for r in historical)
    add(checks, "historical_absolute_effect_freeze", (len(historical), pass_n, warn_n, nominal_n, robust_n, changed_n) == (23, 22, 1, 1, 0, 0), [len(historical), pass_n, warn_n, nominal_n, robust_n, changed_n])

    role_table = read_tsv(ROOT / "source_data" / "V4_claim_role_transition_22.tsv")
    role_counts = Counter(row["current_role"] for row in role_table)
    expected_roles = {"POPULATION_UNVERIFIED": 10, "ROLE_REFRAMED": 7, "TARGETED_REANALYSIS": 2, "NOT_CURRENTLY_EVALUABLE": 2, "IMPLEMENTATION_LIMITED": 1}
    add(checks, "rpv4_role_table", len(role_table) == 22 and len({r["claim_estimand_id"] for r in role_table}) == 22 and dict(role_counts) == expected_roles and all(r["primary_label_mutated"] == "FALSE" for r in role_table), {"rows": len(role_table), "counts": dict(role_counts)})

    a2 = read_tsv(ROOT / "results" / "V4_S2_A2_primary_results.tsv")
    a2_by_claim = {row["claim_id"]: row for row in a2}
    a2_ok = len(a2) == 2 and set(a2_by_claim) == {"GBM_01", "GBM_02"}
    if a2_ok:
        a2_ok = all(row["n"] == "333" and row["events"] == "260" for row in a2)
        a2_ok = a2_ok and close(a2_by_claim["GBM_01"]["interaction_hr"], 0.612401785931) and close(a2_by_claim["GBM_01"]["interaction_p"], 0.0776784765423)
        a2_ok = a2_ok and close(a2_by_claim["GBM_02"]["interaction_hr"], 0.513355342457) and close(a2_by_claim["GBM_02"]["interaction_p"], 0.0177822204946)
    add(checks, "v4_s2_primary_results", a2_ok, [{k: row.get(k) for k in ("claim_id", "n", "events", "interaction_hr", "interaction_p")} for row in a2])

    s2 = json.loads((ROOT / "audit" / "V4_S2_final_status.json").read_text(encoding="utf-8"))
    add(checks, "v4_s2_acceptance", s2["status"] == "ACCEPT_V4_S2_AVAGLIO_A2" and s2["validation"]["checks_passed"] == s2["validation"]["checks_total"] == 17 and s2["validation"]["independent_R_reproduction"] == "PASS" and not s2["historical_results_modified"] and not s2["primary_labels_modified"], s2["validation"])

    s3 = json.loads((ROOT / "audit" / "V4_S3_final_status.json").read_text(encoding="utf-8"))
    add(checks, "v4_s3_identifiability", s3["public_counts"]["n"] == 110 and not s3["raw_assignment_phase_field_present"] and not s3["participant_level_phase_mapping_recovered"] and s3["design_level_partial_identifiability"] and s3["conditional_arm3_randomized_n_range"] == [30, 38] and not s3["aggregate_bound_is_confidence_interval"] and not s3["aggregate_bound_identifies_marker_treatment_interaction"] and not s3["pseudo_corrected_model_run"] and not s3["simulation_run"], {k: s3[k] for k in ("raw_assignment_phase_field_present", "participant_level_phase_mapping_recovered", "conditional_arm3_randomized_n_range", "pseudo_corrected_model_run")})

    integrated = read_tsv(ROOT / "results" / "V4_S4_22object_evidence_integration.tsv")
    s4_rows = read_tsv(ROOT / "results" / "V4_S4_cross_trial_historical_vs_current.tsv")
    add(checks, "v4_s4_integrated_objects", len(integrated) == 22 and len({r["claim_estimand_id"] for r in integrated}) == 22, len(integrated))
    current_members = [r.get("current_verified_strict_denominator_member", "").casefold() for r in s4_rows]
    current_proportions = [r.get("current_strict_replication_proportion", "") for r in s4_rows]
    add(checks, "v4_s4_cross_trial_current_status", len(s4_rows) == 13 and all(x == "false" for x in current_members) and all(x == "NOT_ESTIMABLE" for x in current_proportions), {"members": Counter(current_members), "proportions": Counter(current_proportions)})

    table1 = read_tsv(ROOT / "results" / "Table1_V4_S5_claim_estimand_summary_22objects.tsv")
    supp1 = read_tsv(ROOT / "results" / "Supplementary_Table_S1_AVAglio_A0_A4_10rows.tsv")
    supp2 = read_tsv(ROOT / "results" / "Supplementary_Table_S2_cross_trial_historical_current_13rows.tsv")
    supp3 = read_tsv(ROOT / "results" / "Supplementary_Table_S3_absolute_effect_current_role_23rows.tsv")
    add(checks, "submission_table_rows", [len(table1), len(supp1), len(supp2), len(supp3)] == [22, 10, 13, 23], [len(table1), len(supp1), len(supp2), len(supp3)])

    current_bases = ["Figure1_finite_boundary_and_correction_pathways", "Figure2_claim_estimand_alignment_matrix", "Figure3_AVAglio_population_model_ladder", "Figure4_historical_replay_and_current_eligibility"]
    missing_formats = [f"{base}.{ext}" for base in current_bases for ext in ("svg", "pdf", "png") if not (ROOT / "figures" / f"{base}.{ext}").is_file()]
    add(checks, "current_figure_formats", not missing_formats, missing_formats)

    manuscript_path = ROOT / "manuscript" / "QiTeng_RPv4_BMC_MRM_submission_candidate_v1.4_20261011.md"
    manuscript = manuscript_path.read_text(encoding="utf-8")
    manuscript_checks = [
        manuscript.startswith("# From reproducible estimates to defensible inference"),
        "0.612" in manuscript and "0.0777" in manuscript,
        "0.513" in manuscript and "0.0178" in manuscript,
        "30–38" in manuscript,
        "48.5–60.0%" in manuscript,
        "not estimable" in manuscript.casefold(),
        manuscript.count("[[") >= 10,
    ]
    forbidden_claims = ["all published biomarkers failed randomized validation", "two independent positive validations", "new additive-scale replication", "13 independent replications were performed", "TRIO 48.5–60.0% confidence interval"]
    add(checks, "current_manuscript_scientific_bounds", all(manuscript_checks) and not any(x in manuscript for x in forbidden_claims), {"required": manuscript_checks, "forbidden_present": [x for x in forbidden_claims if x in manuscript]})

    s6h1 = json.loads((ROOT / "audit" / "V4_S6H1_final_status.json").read_text(encoding="utf-8"))
    add(checks, "v4_s6h1_machine_status", s6h1["validation"] == "32/32 PASS" and s6h1["truth_value_categories_open"] == 11 and s6h1["wps_pages"] == 17 and s6h1["wps_visual_qa"] == "PASS" and s6h1["libreoffice_used"] is False and s6h1["submission"] == "HOLD", {k: s6h1[k] for k in ("validation", "truth_value_categories_open", "wps_pages", "wps_visual_qa", "libreoffice_used", "submission")})

    current=json.loads((ROOT/"audit/V4_S9_public_status_20261012.json").read_text(encoding="utf-8"))
    add(checks,"v1_4_current_status",current["manuscript_version"]=="1.4" and current["author_truth_categories_open"]==11 and current["submission"]=="HOLD" and current["statistical_refit_in_s9"] is False and current["current_main_figures"]==4 and current["actual_panels"]==11, current)
    supplement_pairs=[("Additional_file_1_AVAglio_A0_A4.csv","Supplementary_Table_S1_AVAglio_A0_A4_10rows.tsv",10),
                      ("Additional_file_2_cross_trial_eligibility.csv","Supplementary_Table_S2_cross_trial_historical_current_13rows.tsv",13),
                      ("Additional_file_3_absolute_effect_sensitivity.csv","Supplementary_Table_S3_absolute_effect_current_role_23rows.tsv",23)]
    equivalence=[]
    for csv_name,tsv_name,n in supplement_pairs:
        with (ROOT/"supplementary_csv"/csv_name).open(encoding="utf-8-sig",newline="") as f:
            csv_rows=list(csv.DictReader(f))
        tsv_rows=read_tsv(ROOT/"results"/tsv_name)
        equivalence.append({"file":csv_name,"rows":len(csv_rows),"equal":csv_rows==tsv_rows and len(csv_rows)==n})
    add(checks,"current_supplement_csv_equivalence",all(x["equal"] for x in equivalence),equivalence)
    recipe=ROOT/"public_reproduction_v1_4/scripts/build_v4_s8_figures.py"
    tree=ast.parse(recipe.read_text(encoding="utf-8"))
    assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="EXPECTED" for t in n.targets))
    frozen_expected=ast.literal_eval(assignment.value)
    frozen_results=[]
    for key,expected in frozen_expected.items():
        source=ROOT/"public_reproduction_v1_4/source_data"/(key+(".json" if key=="s4status" else ".tsv"))
        observed=hashlib.sha256(source.read_bytes()).hexdigest()
        frozen_results.append({"source":key,"raw_sha256_match":observed==expected})
    add(checks,"current_figure_frozen_input_raw_bytes",len(frozen_results)==11 and all(x["raw_sha256_match"] for x in frozen_results),frozen_results)

    with gzip.open(ROOT / "results" / "binary_absolute_effect_bootstrap_replicates.tsv.gz", "rt", encoding="utf-8") as handle:
        replicate_rows = sum(1 for _ in handle) - 1
    add(checks, "historical_bootstrap_rows", replicate_rows == 115000, replicate_rows)

    passed = sum(bool(c["pass"]) for c in checks)
    output = {"status": "PASS" if passed == len(checks) else "FAIL", "checks_passed": passed, "checks_total": len(checks), "checks": checks}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if passed != len(checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
