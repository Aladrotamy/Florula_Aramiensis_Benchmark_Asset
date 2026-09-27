"""Regenerate the synthetic specimen and phenology data of Florula Aramiensis.

Usage (from the asset root):
    python tools/make_specimens.py --data project_source/data --out regen

Reads species.tsv and localities.tsv from --data and writes specimens.tsv and
phenology.tsv to --out. The generator is deterministic (seed 20260927): the
output is byte-identical to the files shipped in project_source/data.
"""
import argparse, csv, datetime as dt, os, random

SEED = 20260927
PHENOLOGY = {  # species_id: (flowering months, fruiting months)
    "ANA01": ([12, 1, 2, 3], [2, 3, 4, 5]),   "ANA02": ([2, 3, 4], [6, 7, 8, 9]),
    "COM01": ([2, 3, 4], [4, 5, 6]),          "COM02": ([2, 3, 4], [5, 6, 7, 8]),
    "FAB01": ([3, 4, 5], [11, 12, 1, 2]),     "FAB02": ([12, 1, 2], [3, 4, 5]),
    "FAB03": ([12, 1, 2], [2, 3, 4]),         "IRV01": ([3, 4, 5], [6, 7, 8, 9]),
    "MAL01": ([4, 5, 6], [10, 11, 12, 1, 2]), "MAL02": ([12, 1, 2], [2, 3, 4]),
    "MAL03": ([3, 4, 5, 6], [10, 11, 12, 1]), "MEL01": ([3, 4, 5], [11, 12, 1]),
    "MEL02": ([3, 4, 5], [1, 2, 3]),          "MEL03": ([3, 4, 5], [1, 2]),
    "MOR01": ([11, 12, 1, 2], [2, 3, 4]),     "MOR02": ([10, 11], [12, 1, 2]),
    "SAP01": ([3, 4, 5], [12, 1, 2, 3]),      "SAP02": ([1, 2, 3], [5, 6, 7]),
}
COLLECTORS = {  # name: (first year, last year, herbarium, allowed localities)
    "Harding":  (1934, 1938, "OKF", ["L01", "L07", "L08", "L10", "L12"]),
    "Olaniyan": (1961, 1967, "SVN", ["L02", "L03", "L04", "L05", "L06", "L09", "L11"]),
    "Alade":    (2019, 2025, "AUH", None),  # None = any locality
}
FIRST_NUMBER = {"Harding": 1012, "Olaniyan": 208, "Alade": 101}
PER_SPECIES = 5
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="project_source/data")
    ap.add_argument("--out", default="regen")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--per-species", type=int, default=PER_SPECIES)
    a = ap.parse_args()
    random.seed(a.seed)
    species = read_tsv(os.path.join(a.data, "species.tsv"))
    loc = {r["locality_id"]: r for r in read_tsv(os.path.join(a.data, "localities.tsv"))}
    rows = []
    for s in species:
        veg = s["vegetation"].split(";")
        ok = {}
        for c, (_, _, _, allowed) in COLLECTORS.items():
            ok[c] = [l for l in (allowed or list(loc)) if loc[l]["vegetation"] in veg]
        cols = [c for c in COLLECTORS if ok[c]]
        for i in range(a.per_species):
            c = cols[i % len(cols)]
            y0, y1, herb, _ = COLLECTORS[c]
            l = random.choice(ok[c])
            phen = random.choice(["fl", "fr", "fr", "st"])
            fl, fr = PHENOLOGY[s["species_id"]]
            months = fl if phen == "fl" else fr if phen == "fr" else \
                [m for m in range(1, 13) if m not in fl + fr] or [8]
            m = random.choice(months)
            d = dt.date(random.randint(y0, y1), m, random.randint(1, 28))
            rows.append(dict(species_id=s["species_id"], collector=c, date=d, locality_id=l,
                             altitude_m=loc[l]["altitude_m"], herbarium=herb, phenology=phen))
    for c in COLLECTORS:  # numbers increase with date for each collector
        n = FIRST_NUMBER[c]
        for r in sorted((r for r in rows if r["collector"] == c), key=lambda r: r["date"]):
            n += random.randint(3, 40)
            r["number"] = n
    rows.sort(key=lambda r: (r["species_id"], r["date"]))
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "specimens.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["specimen_id", "species_id", "collector", "number", "date",
                    "locality_id", "altitude_m", "herbarium", "phenology"])
        for i, r in enumerate(rows, 1):
            w.writerow([f"S{i:03d}", r["species_id"], r["collector"], r["number"],
                        r["date"].isoformat(), r["locality_id"], r["altitude_m"],
                        r["herbarium"], r["phenology"]])
    with open(os.path.join(a.out, "phenology.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["species_id"] + MONTHS)
        for s in species:
            fl, fr = PHENOLOGY[s["species_id"]]
            w.writerow([s["species_id"]] + ["+".join(k for k, ms in (("fl", fl), ("fr", fr)) if m in ms) or "-"
                                            for m in range(1, 13)])
    print(f"wrote {len(rows)} specimens and {len(species)} phenology rows to {a.out}")


if __name__ == "__main__":
    main()