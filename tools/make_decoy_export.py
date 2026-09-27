"""Build the decoy file data/archive/specimens_export_2023.tsv.

The decoy imitates an older export of the specimen database: three records
that were added later are missing, the Alade herbarium still carries its old
code ARH, and an export_date column is present. It must never be used as the
active dataset. Usage (from the asset root):
    python tools/make_decoy_export.py
"""
import csv, os

SRC = "project_source/data/specimens.tsv"
OUT = "project_source/data/archive/specimens_export_2023.tsv"
MISSING = {"S047", "S063", "S085"}

with open(SRC, encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(list(rows[0].keys()) + ["export_date"])
    n = 0
    for r in rows:
        if r["specimen_id"] in MISSING:
            continue
        if r["herbarium"] == "AUH":
            r["herbarium"] = "ARH"
        w.writerow(list(r.values()) + ["2023-11-30"])
        n += 1
print(f"wrote {n} records to {OUT}")