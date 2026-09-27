"""Oracle for the Florula Aramiensis asset: admission checks on the verifier.

Usage (from the asset root):
    python verifier/run_oracle.py

Stage 1  null         the untouched starting state (project_source) scores < 1
Stage 2  solver       the golden solution scores exactly 1
Stage 3  monotone     applying the four fixes one by one never lowers the score
Stage 4  adversarial  wrong or shortcut solutions never reach 1
Stage 5  alternative  a different valid fix of the overflow (resizebox) scores 1
"""
import os, re, shutil, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from verify import run_checks

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = json.load(open(os.path.join(HERE, "expected.json"), encoding="utf-8"))
GOLD, START = "golden_solution", "project_source"
FIXES = ["families/meliaceae.tex", "data/specimens.tsv",
         "appendices/phenology_calendar.tex", "keys/key_to_families.tex"]


def score(path):
    C = run_checks(path, EXP, True)
    s = [r for r in C.results if r[1] > 0]
    raw = sum(r[1] for r in s if r[3]) / sum(r[1] for r in s)
    return (0 if C.gate_fail else 1) * raw


def copy(src):
    d = tempfile.mkdtemp(prefix="oracle_")
    dst = os.path.join(d, "p")
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.aux", "*.log", "*.pdf", "*.bbl", "*.blg", "*.toc", "*.out"))
    return dst


def edit(root, rel, fn):
    p = os.path.join(root, rel)
    with open(p, encoding="utf-8", newline="") as f:
        t = f.read()
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(fn(t))


def take(root, rel):
    shutil.copy(os.path.join(GOLD, rel), os.path.join(root, rel))


def take_from_start(root, rel):
    shutil.copy(os.path.join(START, rel), os.path.join(root, rel))


def close_log(root):
    take(root, "notes/review_log.md")


rows, ok = [], True
s0 = score(START); rows.append(("null", "project_source (4 planted defects)", s0, s0 < 1))
s1 = score(GOLD); rows.append(("solver", "golden_solution", s1, abs(s1 - 1) < 1e-9))

p = copy(START); prev = s0; mono = True
for i, rel in enumerate(FIXES, 1):
    take(p, rel)
    if i == len(FIXES):
        close_log(p)
    s = score(p); mono &= s >= prev - 1e-9; prev = s
    rows.append(("monotone", f"prefix {i}: fixed {rel}", s, mono))

def adv(name, build, must_fail=True):
    p = copy(GOLD); build(p); s = score(p)
    rows.append(("adversarial" if must_fail else "alternative", name, s, (s < 1) if must_fail else abs(s - 1) < 1e-9))

adv("drop_last: D1-D3 fixed, key left broken", lambda p: take_from_start(p, "keys/key_to_families.tex"))
adv("close_log_only: review log closed, no defect fixed",
    lambda p: [take_from_start(p, r) for r in FIXES])
adv("delete_columns: calendar made to fit by dropping Sep-Dec",
    lambda p: edit(p, "appendices/phenology_calendar.tex",
                   lambda t: "\n".join(" & ".join(l.split(" & ")[:9]) + (" \\\\" if " & " in l and "\\\\" in l else "") if " & " in l else l
                                       for l in t.split("\n"))))
adv("delete_record: S047 removed instead of corrected",
    lambda p: edit(p, "data/specimens.tsv", lambda t: "\n".join(l for l in t.split("\n") if not l.startswith("S047"))))
adv("use_decoy: archived export copied over specimens.tsv",
    lambda p: shutil.copy(os.path.join(p, "data/archive/specimens_export_2023.tsv"), os.path.join(p, "data/specimens.tsv")))
adv("old_house_style: author abbreviations spaced as in the 2019 note",
    lambda p: edit(p, "families/moraceae.tex", lambda t: t.replace("C.C.Berg", "C. C. Berg")))
adv("paste_after_end: text parked after \\end{document}",
    lambda p: edit(p, "main.tex", lambda t: t + "\nFixed: 360 m; couplets 1--9.\n"))
adv("resizebox: overflowing calendar fixed by scaling to the text block",
    lambda p: take_from_start(p, "appendices/phenology_calendar.tex") or edit(p, "appendices/phenology_calendar.tex",
                   lambda t: t.replace("\\begin{tabular}", "\\resizebox{\\textwidth}{!}{\\begin{tabular}").replace("\\end{tabular}", "\\end{tabular}}")),
    must_fail=False)



print(f"{'stage':12s} {'case':62s} {'score':>7s}  ok")
for st, name, s, good in rows:
    ok &= good
    print(f"{st:12s} {name:62s} {s:7.4f}  {'yes' if good else 'NO'}")
print("\nORACLE", "PASSED" if ok else "FAILED")
