# Reference Results

Every value below is taken from `golden_solution/` and is checked by `verifier/verify.py`. The check ID is given in brackets. Tolerance is 0 (exact) unless stated.

## Build

| Quantity | Reference value | Tolerance |
|---|---|---|
| Compiler | pdfLaTeX + BibTeX (natbib, plainnat) | exact |
| LaTeX errors [C01] | 0 | exact |
| Compiled pages [C02] | 44 | ±0 pages |
| Overfull boxes [C03] | 0 | exact (any overfull box fails) |
| Undefined references or citations [C04] | 0 | exact |
| Files `\input` by `main.tex` [S01] | 18, in fixed order | exact |

## Data layer

| File | Lines × columns [D01] | SHA-256 (first 12 hex, LF-normalised) |
|---|---|---|
| `data/species.tsv` | 19 × 9 | `2c046495a12f` |
| `data/localities.tsv` | 13 × 5 | `1f62be617989` |
| `data/specimens.tsv` | 91 × 9 | `46796adbad60` [D03] |
| `data/phenology.tsv` | 19 × 13 | `710f37814321` |
| `data/archive/specimens_export_2023.tsv` (decoy) | 88 × 10 | `3e95c5df6060` (frozen) |

All four active data files end with a newline [D01]. `python tools/make_specimens.py --out regen` regenerates `specimens.tsv` and `phenology.tsv` byte-for-byte (seed 20260927).

Specimen records violating the six data rules [D02]: **0 of 90**. The rules are:
1. altitude equals locality altitude;
2. locality vegetation type listed for the species;
3. date within the collector's period (Harding 1934–1938, Olaniyan 1961–1967, Alade 2019–2025);
4. herbarium matches the collector (OKF, SVN, AUH);
5. `fl`/`fr`/`st` consistent with `phenology.tsv`;
6. collector numbers increase with date and are unique.

Gazetteer rows agreeing with `localities.tsv` [D04]: **12 of 12**.

## Counts in the book

| Quantity | Value |
|---|---|
| Families / species / specimens | 8 / 18 / 90 |
| Localities / references / author abbreviations | 12 / 15 / 25 |

Table 2.1, species and specimens by family [M01]:

| Family | Species | Specimens |
|---|---|---|
| Anacardiaceae | 2 | 10 |
| Combretaceae | 2 | 10 |
| Fabaceae | 3 | 15 |
| Irvingiaceae | 1 | 5 |
| Malvaceae | 3 | 15 |
| Meliaceae | 3 | 15 |
| Moraceae | 2 | 10 |
| Sapotaceae | 2 | 10 |
| **Total** | **18** | **90** |

Table 2.2, specimens by collector [M01]:

| Collector | Herbarium | Flowering | Fruiting | Sterile | Total |
|---|---|---|---|---|---|
| Harding | OKF | 8 | 19 | 5 | 32 |
| Olaniyan | SVN | 11 | 16 | 5 | 32 |
| Alade | AUH | 4 | 12 | 10 | 26 |
| **Total** | | **23** | **47** | **20** | **90** |

Values derived from the decoy export that must **not** appear: 87 specimens; 31 / 31 / 25 per collector; herbarium code ARH [G3, M01].

## Treatments, keys and nomenclature

| Check | Reference value |
|---|---|
| Specimens cited exactly once, in their own treatment [T01] | 90 of 90 |
| Distribution maps equal to the specimens' grid squares [T02] | 18 of 18 |
| Phenology statements agreeing with `phenology.tsv` [T03] | 18 of 18 |
| Phenological calendar [T04] | 18 species × 12 months, 216 of 216 cells agree |
| Key to Families [K01] | couplets 1–9, each has a and b, each of 2–9 reached exactly once, 8 of 8 families reachable |
| Species keys [K02] | 7 of 7 valid |
| Author abbreviations used but not listed in Appendix A [N01] | 0 (25 listed) |
| References cited [N02] | 15 of 15 |
| `config.json` / `submission.yaml` agree with the book [B01] | pages 44, species 18, specimens 90 |
| Review log [L01] | 12 of 12 entries closed with a resolution; R01–R08 unchanged |

## Planted defects: before and after

| ID | File | Starting state (`project_source`) | Reference fix (`golden_solution`) | Measured effect |
|---|---|---|---|---|
| D1 | `families/meliaceae.tex` | `\end{florakye}` | `\end{florakey}` | pdfLaTeX stops: `\begin{florakey} ... ended by \end{florakye}` |
| D2 | `data/specimens.tsv` | S047 altitude 630 | 360 (Ireke Ferry, L08) | 1 violation of data rule 1; SHA-256 differs from generator output |
| D3 | `appendices/phenology_calendar.tex` | full month names, normal size | abbreviated months, `\small`, `\tabcolsep` 3 pt | Overfull \hbox 180.9 pt before; 0 after |
| D4 | `keys/key_to_families.tex` | couplets 6–10, lead 1b points to missing couplet 5 | couplets 1–9 | numbering gap and dangling reference; 0 after |

Accepted alternative fixes for D3: any mitigation inside the table float that keeps all 18 rows and 12 month columns (for example `\resizebox`, smaller type, abbreviations, reduced `\tabcolsep`). Deleting rows or columns fails T04.

## Scores

| State | Score |
|---|---|
| `project_source` (starting state) | 0.6154 |
| `golden_solution` | 1.0000 |
| `variants/variant_B` against its own expected values | 1.0000 |

Milestone progression (ungated raw score): M1 0.1538, M2 0.2051, M3 0.6410, M4 0.7949, final 1.0000. Full oracle results are in `verifier/oracle_report.txt`.

The data are synthetic and demonstrative. They must not be cited as records of real collections.
