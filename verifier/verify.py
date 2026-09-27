"""Verifier for the Florula Aramiensis benchmark asset.

Usage (from the asset root):
    python verifier/verify.py golden_solution            # compile and score
    python verifier/verify.py project_source --no-compile
    python verifier/verify.py milestone_3_data_methods --no-gate
    python verifier/verify.py variants/variant_B --expected variants/variant_B/expected.json

Score = gate x (passed weight / total weight), in [0, 1].
The gate is 0 if any invariant (frozen files, decoys, anti-shortcut rules)
is broken. Expected values live in verifier/expected.json, which is built
from golden_solution/ by verifier/build_expected.py.
"""
import argparse, csv, hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
FULL = ["january", "february", "march", "april", "may", "june", "july",
        "august", "september", "october", "november", "december"]


# ---------------------------------------------------------------- helpers
def norm_bytes(b):
    """Normalise line endings and the final newline before hashing."""
    return b.replace(b"\r\n", b"\n").rstrip(b"\n") + b"\n"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(norm_bytes(f.read())).hexdigest()


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n")


def tsv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def strip_comments(tex):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", l) for l in tex.split("\n"))


def args_of(tex, macro, n):
    """All occurrences of \\macro{...}{...} with n brace-balanced arguments."""
    out, i = [], 0
    pat = "\\" + macro + "{"
    while True:
        i = tex.find(pat, i)
        if i < 0:
            return out
        j, got = i + len(pat) - 1, []
        for _ in range(n):
            while j < len(tex) and tex[j] in " \n":
                j += 1
            if j >= len(tex) or tex[j] != "{":
                break
            depth, k = 0, j
            while k < len(tex):
                depth += {"{": 1, "}": -1}.get(tex[k], 0)
                if depth == 0:
                    break
                k += 1
            got.append(tex[j + 1:k])
            j = k + 1
        if len(got) == n:
            out.append((i, got))
        i += len(pat)


def ws(s):
    return re.sub(r"\s+", " ", s).strip()


def month_range(a, b):
    i, j = FULL.index(a.lower()), FULL.index(b.lower())
    r = [i]
    while i != j:
        i = (i + 1) % 12
        r.append(i)
    return {m + 1 for m in r}


# ---------------------------------------------------------------- compile
def compile_project(root):
    """Build in a temporary copy: pdflatex, bibtex, pdflatex, pdflatex."""
    tmp = tempfile.mkdtemp(prefix="florula_")
    dst = os.path.join(tmp, "p")
    shutil.copytree(root, dst, ignore=shutil.ignore_patterns(
        "*.aux", "*.log", "*.bbl", "*.blg", "*.toc", "*.out", "*.pdf", "*.synctex.gz"))
    run = lambda c: subprocess.run(c, cwd=dst, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, timeout=300)
    tex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    run(tex); run(["bibtex", "main"]); run(tex); run(tex)
    log = read(os.path.join(dst, "main.log")) if os.path.exists(os.path.join(dst, "main.log")) else ""
    shutil.rmtree(tmp, ignore_errors=True)
    return log


# ---------------------------------------------------------------- checks
class Checker:
    def __init__(self, root, exp):
        self.root, self.exp, self.results, self.gate_fail = root, exp, [], []

    def p(self, *parts):
        return os.path.join(self.root, *parts)

    def check(self, cid, weight, desc, fn):
        try:
            ok, detail = fn()
        except Exception as e:  # a missing file or unparsable input fails the check
            ok, detail = False, f"{type(e).__name__}: {e}"
        self.results.append((cid, weight, desc, ok, detail))

    def gate(self, gid, desc, fn):
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"{type(e).__name__}: {e}"
        if not ok:
            self.gate_fail.append((gid, desc, detail))
        self.results.append((gid, 0, desc, ok, detail))

    # -- data
    def data(self):
        d = self.p("data")
        return (tsv(os.path.join(d, "species.tsv")), tsv(os.path.join(d, "localities.tsv")),
                tsv(os.path.join(d, "specimens.tsv")), tsv(os.path.join(d, "phenology.tsv")))

    def tex_all(self):
        main = strip_comments(read(self.p("main.tex")))
        files = re.findall(r"\\input\{([^}]+)\}", main)
        return main, files, {f: strip_comments(read(self.p(f + ".tex"))) for f in files}


def run_checks(root, exp, do_compile):
    C = Checker(root, exp)
    E = exp

    # ---------- invariants (gate)
    def frozen():
        bad = [f for f, h in E["frozen"].items()
               if not os.path.exists(C.p(f)) or sha(C.p(f)) != h]
        return not bad, f"{len(E['frozen']) - len(bad)}/{len(E['frozen'])} frozen files unchanged" + (f"; changed: {bad[:5]}" if bad else "")
    C.gate("G1", "Frozen files (decoys, data, unaffected sources) unchanged", frozen)

    def nothing_after():
        t = read(C.p("main.tex"))
        return t.split("\\end{document}", 1)[1].strip() == "", "only whitespace after \\end{document}"
    C.gate("G2", "Nothing after \\end{document} in main.tex", nothing_after)

    def old_style():
        hits = []
        for dp, _, fs in os.walk(root):
            for f in fs:
                if f.endswith(".tex"):
                    t = read(os.path.join(dp, f))
                    for pat in (r"C\. C\. Berg", r"A\. Chev\.", r"C\. F\. Gaertn\.", r"\[(AUH|OKF|SVN)\]", r"\b\d\d\.\d\d\.(19|20)\d\d\b", r"\bARH\b"):
                        if re.search(pat, t):
                            hits.append(f"{f}:{pat}")
        return not hits, "no decoy house-style or decoy-export conventions" + (f"; found {hits[:4]}" if hits else "")
    C.gate("G3", "Decoy house style (2019) and decoy export not applied", old_style)

    def file_count():
        n = sum(1 for dp, _, fs in os.walk(root) for f in fs
                if f.endswith((".tex", ".bib", ".sty", ".tsv", ".md", ".json", ".yaml")))
        return n <= E["max_source_files"], f"{n} source files (max {E['max_source_files']})"
    C.gate("G4", "No file flooding", file_count)

    # ---------- compile
    log = compile_project(root) if do_compile else (read(C.p("main.log")) if os.path.exists(C.p("main.log")) else "")
    pages = re.search(r"Output written on main\.pdf \((\d+) pages?", log)
    C.check("C01", 3, "Compiles: 0 LaTeX errors",
            lambda: (bool(log) and not re.search(r"^!", log, re.M) and pages is not None,
                     "no log" if not log else f"{len(re.findall(r'^!', log, re.M))} errors"))
    C.check("C02", 1, f"Page count equals {E['pages']} (tolerance 0)",
            lambda: (pages is not None and int(pages.group(1)) == E["pages"], pages.group(1) if pages else "no PDF"))
    C.check("C03", 2, "0 overfull boxes",
            lambda: (bool(log) and "Overfull" not in log, f"{log.count('Overfull')} overfull"))
    C.check("C04", 1, "0 undefined references or citations",
            lambda: (bool(log) and not re.search(r"undefined", log), f"{len(re.findall('undefined', log))} undefined"))

    # ---------- structure
    def inputs():
        _, files, _ = C.tex_all()
        return files == E["inputs"], f"{len(files)} inputs" + ("" if files == E["inputs"] else f"; expected {len(E['inputs'])} in fixed order")
    C.check("S01", 2, "main.tex inputs every chapter file once, in the expected order", inputs)

    # ---------- data
    def shapes():
        bad = []
        for f, (rows, cols) in E["shapes"].items():
            raw = open(C.p("data", f), "rb").read()
            lines = raw.replace(b"\r\n", b"\n").split(b"\n")
            if not raw.endswith(b"\n"):
                bad.append(f + " (no final newline)")
            lines = [l for l in lines if l]
            if len(lines) != rows or any(len(l.split(b"\t")) != cols for l in lines):
                bad.append(f)
        return not bad, "all data files have expected shape" if not bad else f"bad: {bad}"
    C.check("D01", 2, "Data file shapes and final newlines", shapes)

    def rules():
        sp, lo, S, _ = C.data()
        spd = {r["species_id"]: r for r in sp}; lod = {r["locality_id"]: r for r in lo}
        ph = {r["species_id"]: r for r in C.data()[3]}
        per = {c: tuple(v) for c, v in E["collectors"].items()}
        viol = []
        for r in S:
            l = lod[r["locality_id"]]; m = int(r["date"][5:7]); y = int(r["date"][:4])
            cell = ph[r["species_id"]][MONTHS[m - 1]]
            if r["altitude_m"] != l["altitude_m"]: viol.append((r["specimen_id"], 1))
            if l["vegetation"] not in spd[r["species_id"]]["vegetation"].split(";"): viol.append((r["specimen_id"], 2))
            y0, y1, h = per[r["collector"]]
            if not y0 <= y <= y1: viol.append((r["specimen_id"], 3))
            if r["herbarium"] != h: viol.append((r["specimen_id"], 4))
            if (r["phenology"] == "st" and cell != "-") or (r["phenology"] in ("fl", "fr") and r["phenology"] not in cell.split("+")):
                viol.append((r["specimen_id"], 5))
        for c in per:
            L = sorted((r for r in S if r["collector"] == c), key=lambda r: r["date"])
            ns = [int(r["number"]) for r in L]
            if ns != sorted(ns) or len(set(ns)) != len(ns): viol.append((c, 6))
        return not viol and len(S) == E["specimens"], f"{len(S)} specimens, {len(viol)} rule violations {viol[:4]}"
    C.check("D02", 4, "All specimens satisfy the six data rules", rules)

    def specimens_hash():
        h = sha(C.p("data", "specimens.tsv"))
        return h == E["specimens_sha256"], h[:12]
    C.check("D03", 2, "specimens.tsv matches the generator output (SHA-256)", specimens_hash)

    def gazetteer():
        t = strip_comments(read(C.p("appendices", "gazetteer.tex")))
        body = t.split("\\endfoot", 1)[1]
        rows = [[ws(c) for c in r.split("&")] for r in body.split("\\\\") if "&" in r]
        lo = C.data()[1]
        want = [[r["locality"], r["grid"], r["altitude_m"], r["vegetation"]] for r in lo]
        return sorted(rows) == sorted(want), f"{len(rows)} gazetteer rows vs {len(want)} data rows"
    C.check("D04", 1, "localities.tsv agrees with Appendix B", gazetteer)

    # ---------- treatments
    def sections():
        sp, lo, S, ph = C.data()
        byname = {f"{r['genus']} {r['epithet']}": r["species_id"] for r in sp}
        _, files, texs = C.tex_all()
        out = {}
        for f in files:
            if not f.startswith("families/"):
                continue
            t = texs[f]
            occ = args_of(t, "species", 2)
            for k, (pos, (name, auth)) in enumerate(occ):
                end = occ[k + 1][0] if k + 1 < len(occ) else len(t)
                out[byname[name]] = (f, t[pos:end], auth)
        return out

    def cited():
        S = C.data()[2]
        secs = sections()
        seen = {}
        for sid, (_, body, _) in secs.items():
            for coll, num, _h in [a for _, a in args_of(body, "specimen", 3)]:
                seen.setdefault((coll, num), []).append(sid)
        bad = [r["specimen_id"] for r in S if seen.get((r["collector"], r["number"])) != [r["species_id"]]]
        extra = sum(len(v) for v in seen.values()) - len(S)
        return not bad and extra == 0, f"{len(S) - len(bad)}/{len(S)} specimens cited exactly once in their own treatment"
    C.check("T01", 3, "Every specimen cited exactly once, in its own species treatment", cited)

    def maps():
        sp, lo, S, _ = C.data()
        lod = {r["locality_id"]: r["grid"] for r in lo}
        secs, bad = sections(), []
        for sid, (_, body, _) in secs.items():
            want = {lod[r["locality_id"]] for r in S if r["species_id"] == sid}
            got = set()
            for _, (a,) in args_of(body, "distmap", 1):
                got |= {x.replace("/", "").strip() for x in a.split(",")}
            if got != want:
                bad.append(sid)
        return not bad and len(secs) == E["species"], f"{len(secs) - len(bad)}/{E['species']} maps agree with the specimens"
    C.check("T02", 2, "Distribution maps equal the grid squares of the cited specimens", maps)

    def phen_text():
        ph = {r["species_id"]: r for r in C.data()[3]}
        bad = []
        for sid, (_, body, _) in sections().items():
            m = re.search(r"\\field\{Phenology\}\s*Flowering (\w+) to (\w+); fruiting (\w+) to (\w+)\.", ws(body))
            fl = {i + 1 for i, k in enumerate(MONTHS) if "fl" in ph[sid][k].split("+")}
            fr = {i + 1 for i, k in enumerate(MONTHS) if "fr" in ph[sid][k].split("+")}
            if not m or month_range(m.group(1), m.group(2)) != fl or month_range(m.group(3), m.group(4)) != fr:
                bad.append(sid)
        return not bad, f"{E['species'] - len(bad)}/{E['species']} phenology statements agree" + (f"; {bad}" if bad else "")
    C.check("T03", 2, "Phenology statements agree with phenology.tsv", phen_text)

    def calendar():
        t = strip_comments(read(C.p("appendices", "phenology_calendar.tex")))
        body = t.split("\\midrule", 1)[1].split("\\bottomrule", 1)[0]
        head = t.split("\\toprule", 1)[1].split("\\midrule", 1)[0]
        cols = [ws(c) for c in head.replace("\\\\", "").split("&")][1:]
        ok_head = len(cols) == 12 and all(c.lower().startswith(MONTHS[i].lower()) for i, c in enumerate(cols))
        rows = [[ws(c) for c in r.split("&")] for r in body.split("\\\\") if "&" in r]
        code = {"fl": "F", "fr": "R", "fl+fr": "F+R", "-": "--"}
        want = [[code[r[m]] for m in MONTHS] for r in C.data()[3]]
        got = [r[1:] for r in rows]
        return ok_head and got == want, f"header ok={ok_head}; {len(rows)} rows x {len(rows[0]) - 1 if rows else 0} months"
    C.check("T04", 3, "Phenological calendar keeps all 18 species x 12 months and agrees with the data", calendar)

    # ---------- keys
    def key_ok(tex, terminals):
        leads = [(a[0], a[2]) for _, a in args_of(tex, "lead", 3)]
        nums = {}
        for lab, dest in leads:
            m = re.fullmatch(r"(\d+)([ab])", lab.strip())
            if not m:
                return False, f"bad label {lab}"
            nums.setdefault(int(m.group(1)), []).append(m.group(2))
        n = max(nums)
        if sorted(nums) != list(range(1, n + 1)) or any(sorted(v) != ["a", "b"] for v in nums.values()):
            return False, f"couplets {sorted(nums)} not 1..{n} with a and b"
        refs = [int(d.strip()) for _, d in leads if d.strip().isdigit()]
        if any(r not in nums for r in refs) or sorted(refs) != list(range(2, n + 1)):
            return False, f"references {sorted(refs)} do not reach 2..{n} exactly once"
        dests = ws(" ".join(d for _, d in leads if not d.strip().isdigit()))
        missing = [x for x in terminals if x not in dests]
        return not missing, f"{n} couplets" + (f"; unreachable {missing}" if missing else "")

    C.check("K01", 3, "Key to Families: couplets 1..n, each reached once, all 8 families reachable",
            lambda: key_ok(strip_comments(read(C.p("keys", "key_to_families.tex"))), E["families"]))

    def species_keys():
        sp = C.data()[0]
        bad = []
        _, files, texs = C.tex_all()
        for f in files:
            if not f.startswith("families/"):
                continue
            fam = [r for r in sp if f.endswith(r["family"].lower())]
            if len(fam) < 2:
                continue
            ok, d = key_ok(texs[f], [f"{r['genus']} {r['epithet']}" for r in fam])
            if not ok:
                bad.append(f"{f}: {d}")
        return not bad, "7/7 species keys valid" if not bad else "; ".join(bad)
    C.check("K02", 1, "Species keys valid in every family with 2+ species", species_keys)

    # ---------- nomenclature and bibliography
    def authorities():
        t = strip_comments(read(C.p("appendices", "author_abbreviations.tex")))
        listed = {ws(r.split("&")[0]) for r in t.split("\\endfoot", 1)[1].split("\\\\") if "&" in r}
        _, files, texs = C.tex_all()
        used = set()
        for f, t in texs.items():
            auths = [a[1] for _, a in args_of(t, "species", 2)] + [a[1] for _, a in args_of(t, "sciname", 2)] + \
                    [a[0] for _, a in args_of(t, "authority", 1)]
            for a in auths:
                if a.startswith("#"):
                    continue
                for piece in re.split(r"\s+ex\s+|\\&|&|[()]", ws(a)):
                    used |= {x for x in piece.split() if x}
        unlisted = sorted(used - listed)
        return not unlisted and len(listed) == E["author_abbreviations"], f"{len(listed)} listed, {len(used)} used, unlisted {unlisted}"
    C.check("N01", 2, "Every author abbreviation used is listed in Appendix A (25 listed)", authorities)

    def bib():
        keys = set(re.findall(r"@\w+\{([^,]+),", read(C.p("bib", "florula.bib"))))
        _, _, texs = C.tex_all()
        cited = set()
        for t in texs.values():
            for grp in re.findall(r"\\cite[tp]?\{([^}]+)\}", t):
                cited |= {k.strip() for k in grp.split(",")}
        return cited == keys and len(keys) == E["references"], f"{len(keys)} entries, {len(cited & keys)} cited, undefined {sorted(cited - keys)}"
    C.check("N02", 1, "All 15 references cited; no citation undefined", bib)

    # ---------- methods tables and build files
    def methods():
        sp, _, S, _ = C.data()
        t = strip_comments(read(C.p("chapters", "methods.tex")))
        fam = {}
        for r in sp:
            fam.setdefault(r["family"], [0, 0])[0] += 1
        fid = {r["species_id"]: r["family"] for r in sp}
        for r in S:
            fam[fid[r["species_id"]]][1] += 1
        bad = [f for f, (a, b) in fam.items() if not re.search(rf"{f}\s*&\s*{a}\s*&\s*{b}\s*\\\\", t)]
        if not re.search(rf"Total\s*&\s*{len(sp)}\s*&\s*{len(S)}\s*\\\\", t):
            bad.append("family total")
        for c, (_, _, h) in E["collectors"].items():
            n = [sum(1 for r in S if r["collector"] == c and r["phenology"] == p) for p in ("fl", "fr", "st")]
            if not re.search(rf"{c}\s*&[^&]*&\s*{n[0]}\s*&\s*{n[1]}\s*&\s*{n[2]}\s*&\s*{sum(n)}\s*\\\\", t):
                bad.append(c)
        return not bad, "tables 2.1 and 2.2 agree with the data" if not bad else f"mismatch: {bad}"
    C.check("M01", 2, "Methods tables recomputed from the data", methods)

    def build_files():
        cfg = json.load(open(C.p("build", "config.json"), encoding="utf-8"))
        y = {}
        for line in read(C.p("build", "submission.yaml")).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                y[k.strip()] = v.strip().strip('"')
        bad = []
        for k, want in (("pages", E["pages"]), ("species", E["species"]), ("specimens", E["specimens"])):
            if str(y.get(k)) != str(want): bad.append("yaml." + k)
        if cfg.get("pages") != E["pages"]: bad.append("json.pages")
        for k in ("species", "specimens", "families", "references", "author_abbreviations"):
            if cfg["counts"].get(k) != E[k if k != "families" else "n_families"]: bad.append("json." + k)
        return not bad, "config.json and submission.yaml agree with the book" if not bad else f"mismatch: {bad}"
    C.check("B01", 1, "Build files agree with the book", build_files)

    def review_log():
        rows = [r for r in read(C.p("notes", "review_log.md")).splitlines() if re.match(r"\|\s*R\d\d", r)]
        ids = [r.split("|")[1].strip() for r in rows]
        closed = {r.split("|")[1].strip(): r.split("|")[5].strip() == "Closed" and r.split("|")[6].strip() != "" for r in rows}
        keep = [ws(r) for r in rows if r.split("|")[1].strip() in E["log_frozen"]]
        ok = ids == E["log_ids"] and all(closed.values()) and \
            [hashlib.sha256(k.encode()).hexdigest() for k in keep] == E["log_frozen_hashes"]
        return ok, f"{sum(closed.values())}/{len(ids)} entries closed with a resolution; R01-R08 unchanged={len(keep) == 8}"
    C.check("L01", 1, "Review log: all 12 entries closed with a resolution, none removed or rewritten", review_log)

    return C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--no-compile", action="store_true", help="read main.log instead of compiling")
    ap.add_argument("--no-gate", action="store_true", help="report the ungated score (milestone progress)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--expected", default=os.path.join(HERE, "expected.json"),
                    help="expected values (default: verifier/expected.json)")
    a = ap.parse_args()
    exp = json.load(open(a.expected, encoding="utf-8"))
    C = run_checks(a.project, exp, not a.no_compile)
    scored = [r for r in C.results if r[1] > 0]
    total = sum(r[1] for r in scored)
    got = sum(r[1] for r in scored if r[3])
    raw = got / total
    gate = 0 if (C.gate_fail and not a.no_gate) else 1
    if a.json:
        print(json.dumps({"project": a.project, "raw": round(raw, 4), "gate": gate, "score": round(gate * raw, 4),
                          "results": [dict(id=i, weight=w, check=d, passed=o, detail=t) for i, w, d, o, t in C.results]}, indent=1))
        return
    for cid, w, desc, ok, detail in C.results:
        print(f"{'PASS' if ok else 'FAIL'}  {cid:4s} w={w}  {desc}  [{detail}]")
    print(f"\nraw {raw:.4f}   gate {gate}   SCORE {gate * raw:.4f}   ({a.project})")


if __name__ == "__main__":
    main()
