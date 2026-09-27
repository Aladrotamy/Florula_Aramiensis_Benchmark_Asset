"""Build a complete, compiled variant of the Flora from regenerated data.

Usage (from the asset root):
    python tools/make_variant.py --name variant_B --seed 20261001 --per-species 7

Copies golden_solution/ to variants/<name>/, regenerates specimens.tsv with the
given seed and number of specimens per species, rewrites every specimen block
and distribution map, recomputes the Methods tables, updates config.json and
submission.yaml, compiles the book and writes variants/<name>/expected.json.
"""
import argparse, csv, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "verifier"))
from cite import block, load
from verify import compile_project, read, tsv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="variant_B")
    ap.add_argument("--seed", type=int, default=20261001)
    ap.add_argument("--per-species", type=int, default=7)
    a = ap.parse_args()
    src = os.path.join(ROOT, "golden_solution")
    dst = os.path.join(ROOT, "variants", a.name)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.aux", "*.log", "*.bbl", "*.blg",
                                                            "*.toc", "*.out", "*.pdf", "*.synctex.gz"))
    data = os.path.join(dst, "data")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "make_specimens.py"), "--data", data,
                    "--out", data, "--seed", str(a.seed), "--per-species", str(a.per_species)], check=True)
    loc, S = load(data)
    sp = tsv(os.path.join(data, "species.tsv"))
    names = {f"{r['genus']} {r['epithet']}": r["species_id"] for r in sp}

    # 1. specimen blocks and maps in every family chapter
    fam_dir = os.path.join(dst, "families")
    for f in sorted(os.listdir(fam_dir)):
        p = os.path.join(fam_dir, f)
        t = read(p)
        parts = re.split(r"(\\species\{[^}]+\})", t)
        for i in range(1, len(parts), 2):
            sid = names[re.match(r"\\species\{([^}]+)\}", parts[i]).group(1)]
            parts[i + 1] = re.sub(r"\\field\{Specimens examined\}.*?\\end\{center\}\n?",
                                  lambda m: block(sid, loc, S), parts[i + 1], flags=re.S)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("".join(parts))

    # 2. Methods chapter: counts in text and both tables
    p = os.path.join(dst, "chapters", "methods.tex")
    t = read(p)
    fam = {}
    fid = {r["species_id"]: r["family"] for r in sp}
    for r in sp:
        fam.setdefault(r["family"], [0, 0])[0] += 1
    for r in S:
        fam[fid[r["species_id"]]][1] += 1
    for f, (n, m) in fam.items():
        t = re.sub(rf"({f}\s*&\s*{n}\s*&\s*)\d+(\s*\\\\)", rf"\g<1>{m:2d}\2", t)
    t = re.sub(r"(Total\s*&\s*\d+\s*&\s*)\d+(\s*\\\\)", rf"\g<1>{len(S)}\2", t, count=1)
    tot = [0, 0, 0]
    for c in ("Harding", "Olaniyan", "Alade"):
        n = [sum(1 for r in S if r["collector"] == c and r["phenology"] == ph) for ph in ("fl", "fr", "st")]
        tot = [x + y for x, y in zip(tot, n)]
        t = re.sub(rf"({c}\s*&[^&]*&)[^\\]*\\\\", rf"\g<1> {n[0]:2d} & {n[1]:2d} & {n[2]:2d} & {sum(n):2d} \\\\", t)
    t = re.sub(r"(Total\s*&\s*&)[^\\]*\\\\", rf"\g<1> {tot[0]:2d} & {tot[1]:2d} & {tot[2]:2d} & {sum(tot):2d} \\\\", t)
    t = t.replace("The 90 specimens on which", f"The {len(S)} specimens on which")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(t)

    # 3. compile, then record page count in the build files
    log = compile_project(dst)
    pages = int(re.search(r"Output written on main\.pdf \((\d+) pages?", log).group(1))
    cfgp = os.path.join(dst, "build", "config.json")
    cfg = json.load(open(cfgp, encoding="utf-8"))
    cfg["pages"], cfg["counts"]["specimens"] = pages, len(S)
    with open(cfgp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cfg, fh, indent=2)
        fh.write("\n")
    yp = os.path.join(dst, "build", "submission.yaml")
    y = read(yp)
    y = re.sub(r"(?m)^pages: \d+", f"pages: {pages}", y)
    y = re.sub(r"(?m)^specimens: \d+", f"specimens: {len(S)}", y)
    with open(yp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(y)

    # 4. compiled PDF for the variant (pdflatex, bibtex, pdflatex x2 in place)
    tex = ["pdflatex", "-interaction=nonstopmode", "main.tex"]
    for c in (tex, ["bibtex", "main"], tex, tex):
        subprocess.run(c, cwd=dst, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for ext in ("aux", "log", "bbl", "blg", "toc", "out"):
        q = os.path.join(dst, "main." + ext)
        if os.path.exists(q):
            os.remove(q)

    # 5. expected values for the variant
    subprocess.run([sys.executable, os.path.join(ROOT, "verifier", "build_expected.py"), dst,
                    "--out", os.path.join(dst, "expected.json")], check=True)
    print(f"{a.name}: {len(S)} specimens, {pages} pages -> {dst}")


if __name__ == "__main__":
    main()
