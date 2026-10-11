"""Lossless delimited-text transformation; no workbook, formulas, or statistical changes."""
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAIRS=[
    ("Supplementary_Table_S1_AVAglio_A0_A4_10rows.tsv","Additional_file_1_AVAglio_A0_A4.csv",10),
    ("Supplementary_Table_S2_cross_trial_historical_current_13rows.tsv","Additional_file_2_cross_trial_eligibility.csv",13),
    ("Supplementary_Table_S3_absolute_effect_current_role_23rows.tsv","Additional_file_3_absolute_effect_sensitivity.csv",23),
]
def read(path,delimiter):
    with path.open(encoding="utf-8-sig",newline="") as handle:
        return list(csv.reader(handle,delimiter=delimiter))

def main():
    output=ROOT/"supplementary_csv"
    output.mkdir(exist_ok=True)
    results=[]
    for source_name,target_name,count in PAIRS:
        source=ROOT/"tables"/source_name
        matrix=read(source,"\t")
        target=output/target_name
        with target.open("w",encoding="utf-8-sig",newline="") as handle:
            csv.writer(handle,lineterminator="\r\n").writerows(matrix)
        restored=read(target,",")
        assert len(matrix)-1==count and restored==matrix
        results.append({"source":source.relative_to(ROOT).as_posix(),"csv":target.relative_to(ROOT).as_posix(),
                        "data_rows":count,"columns":len(matrix[0]),"all_parsed_cells_equal":True,
                        "source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
                        "csv_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
                        "interpretation":"Delimiter/quoting only; no number parsing, rounding, missing-value recoding or formula authoring"})
    (ROOT/"audit/V4_S8B_supplementary_csv_equivalence.json").write_text(
        json.dumps({"status":"PASS","files":results},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","files":3,"rows":[x["data_rows"] for x in results]}))

if __name__=="__main__": main()
