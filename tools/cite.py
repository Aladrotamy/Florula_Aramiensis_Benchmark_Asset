"""Write the specimen-citation block and distribution map of one species.

Used by tools/make_variant.py. The block format is the one printed in every
species treatment:  Locality (grid), altitude~m, phenology., date, \\specimen{}.
"""
import csv, datetime as dt, os

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def load(data_dir):
    rd = lambda f: list(csv.DictReader(open(os.path.join(data_dir, f), encoding="utf-8", newline=""), delimiter="\t"))
    return {r["locality_id"]: r for r in rd("localities.tsv")}, rd("specimens.tsv")


def block(species_id, loc, specimens):
    rs = [r for r in specimens if r["species_id"] == species_id]
    lines = []
    for r in rs:
        l, d = loc[r["locality_id"]], dt.date.fromisoformat(r["date"])
        lines.append(f"{l['locality']} ({l['grid']}), {r['altitude_m']}~m, {r['phenology']}., "
                     f"{d.day}~{MONTHS[d.month - 1]} {d.year}, "
                     f"\\specimen{{{r['collector']}}}{{{r['number']}}}{{{r['herbarium']}}}")
    squares = sorted({loc[r["locality_id"]]["grid"] for r in rs})
    return ("\\field{Specimens examined} " + ";\n".join(lines) + ".\n\n"
            "\\field{Distribution} Grid squares " + ", ".join(squares) + ".\n\n"
            "\\begin{center}\n\\distmap{" + ", ".join(f"{g[0]}/{g[1]}" for g in squares) + "}\n\\end{center}\n")
