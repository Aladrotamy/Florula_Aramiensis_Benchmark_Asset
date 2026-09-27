"""Build verifier/expected.json from golden_solution/.

Usage (from the asset root):
    python verifier/build_expected.py golden_solution
    python verifier/build_expected.py variants/variant_B --out variants/variant_B/expected.json

Every source file of the golden solution is frozen (SHA-256 after line-ending
normalisation) except the files the task is expected to change: the four
defect sites and the review log.
"""
import argparse, csv, hashlib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify import sha, read, tsv, strip_comments, ws

EDITABLE = {
    "families/meliaceae.tex",           # D1 compile-blocking environment name
    "data/specimens.tsv",               # D2 altitude of S047
    "appendices/phenology_calendar.tex",  # D3 overflowing table
    "keys/key_to_families.tex",         # D4 couplet numbering
    "notes/review_log.md",              # R09-R12 to be closed
}
SOURCE = (".tex", ".bib", ".sty", ".tsv", ".md", ".json", ".yaml")

ap = argparse.ArgumentParser()
ap.add_argument("root", nargs="?", default="golden_solution")
ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json"))
A = ap.parse_args()
root = A.root
frozen, count = {}, 0
for dp, _, fs in os.walk(root):
    for f in sorted(fs):
        if not f.endswith(SOURCE):
            continue
        count += 1
        rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
        if rel not in EDITABLE:
            frozen[rel] = sha(os.path.join(dp, f))

sp = tsv(os.path.join(root, "data", "species.tsv"))
S = tsv(os.path.join(root, "data", "specimens.tsv"))
cfg = json.load(open(os.path.join(root, "build", "config.json"), encoding="utf-8"))
shapes = {}
for f in ("species.tsv", "localities.tsv", "specimens.tsv", "phenology.tsv"):
    rows = tsv(os.path.join(root, "data", f))
    shapes[f] = [len(rows) + 1, len(rows[0])]
log = [r for r in read(os.path.join(root, "notes", "review_log.md")).splitlines() if re.match(r"\|\s*R\d\d", r)]
log_ids = [r.split("|")[1].strip() for r in log]
frozen_ids = [i for i in log_ids if i <= "R08"]

exp = {
    "pages": cfg["pages"],
    "species": len(sp),
    "specimens": len(S),
    "n_families": len({r["family"] for r in sp}),
    "families": sorted({r["family"] for r in sp}),
    "references": cfg["counts"]["references"],
    "author_abbreviations": cfg["counts"]["author_abbreviations"],
    "collectors": {"Harding": [1934, 1938, "OKF"], "Olaniyan": [1961, 1967, "SVN"], "Alade": [2019, 2025, "AUH"]},
    "inputs": re.findall(r"\\input\{([^}]+)\}", strip_comments(read(os.path.join(root, "main.tex")))),
    "shapes": shapes,
    "specimens_sha256": sha(os.path.join(root, "data", "specimens.tsv")),
    "log_ids": log_ids,
    "log_frozen": frozen_ids,
    "log_frozen_hashes": [hashlib.sha256(ws(r).encode()).hexdigest() for r in log if r.split("|")[1].strip() in frozen_ids],
    "max_source_files": count + 4,
    "frozen": frozen,
}
out = A.out
with open(out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(exp, f, indent=1, sort_keys=True)
    f.write("\n")
print(f"wrote {out}: {len(frozen)} frozen files, {count} source files, pages {exp['pages']}")
