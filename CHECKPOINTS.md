# Checkpoints

All checks are pass/fail. A milestone is complete only when every check passes.

## M1 — Project Foundation

**Status:** Complete
**Snapshot:** `milestone_1_foundation/`
**Compiler:** pdfLaTeX (MiKTeX, via TeXstudio)

### Work completed
- Created the project structure under `project_source/` with 11 folders: appendices, bib, build, chapters, data, families, figures (maps, plates), frontmatter, keys, notes.
- Created the house style `florula.sty` (packages, path macros, nomenclature macros, treatment macros, key environment, specimen citation macro, running heads).
- Created the master file `main.tex` with front matter, main matter and back matter divisions.
- Created four front-matter files: title page, imprint, preface, and "How to use this Flora".
- Defined the herbarium codes used throughout the volume: AUH, OKF, SVN.
- Stated on the imprint that all specimen data are synthetic.

### Pass/fail checks
| ID | Check | Threshold | Result |
|---|---|---|---|
| C1.1 | `main.tex` compiles with pdfLaTeX | 0 errors | PASS |
| C1.2 | Compiled page count | exactly 8 | PASS (8) |
| C1.3 | `florula.sty` defines `\taxon`, `\authority`, `\sciname`, `\family`, `\species`, `\field`, `\lead`, `\specimen`, and the `florakey` environment | all 9 present | PASS |
| C1.4 | Path macros `\florulaFigures`, `\florulaMaps`, `\florulaPlates` defined | all 3 present | PASS |
| C1.5 | Front-matter files in `frontmatter/`: `titlepage.tex`, `imprint.tex`, `preface.tex`, `how_to_use.tex` | exactly 4, each `\input` once by `main.tex` | PASS |
| C1.6 | Contents lists "Preface" and "How to use this Flora" | both present | PASS |
| C1.7 | Imprint states that specimen records are synthetic | statement present | PASS |
| C1.8 | Herbarium codes defined in "How to use" | exactly 3: AUH, OKF, SVN | PASS |
| C1.9 | No stray copies of front-matter files outside `frontmatter/` | 0 strays | PASS (one duplicate `titlepage.tex` found and removed before commit) |
| C1.10 | Text files stored with LF line endings in the repository | 0 CRLF files | PASS (0) |


## M2 — References & Authority Files

**Status:** Complete
**Snapshot:** `milestone_2_references/`
**Compiler:** pdfLaTeX + BibTeX (natbib, plainnat, author–year)

### Work completed
- Created `bib/florula.bib` with 15 references to published West African botanical literature, floras, timber references, the nomenclatural code and family revisions.
- Wrote accented author and place names as LaTeX escapes (Aubréville, Aké Assi, Genève, Glashütten).
- Created the Introduction chapter (geography, climate, vegetation, history of collecting, scope and sources) with 12 citations.
- Created Appendix A, Author Abbreviations: the authority file for all 25 author abbreviations used in the 18 species names of this volume.
- Created Appendix B, Gazetteer of Localities: 12 localities with grid square, altitude and vegetation type.
- Switched on the bibliography in `main.tex`.

### Facts fixed by this milestone (checked in later milestones)
- Altitude range of the Flora area: 350–900 m.
- Vegetation bands: LSF below 500 m; FSM 500–700 m; GSW above 700 m.
- Collectors and periods: Harding 1934–1938; Olaniyan 1961–1967; Alade 2019–2025.
- Volume scope: 18 species in 8 families.

### Pass/fail checks
| ID | Check | Threshold | Result |
|---|---|---|---|
| C2.1 | Compiles with pdfLaTeX + BibTeX | 0 errors, 0 undefined citations | PASS |
| C2.2 | Compiled page count | exactly 15 | PASS (15) |
| C2.3 | Entries in `bib/florula.bib` | exactly 15, 0 BibTeX warnings | PASS |
| C2.4 | Distinct citation keys used in the Introduction | exactly 12, all defined in the .bib | PASS |
| C2.5 | Non-ASCII characters in `bib/florula.bib` | 0 (accents as LaTeX escapes) | PASS |
| C2.6 | Abbreviations in Appendix A | exactly 25, in alphabetical order | PASS |
| C2.7 | Localities in Appendix B | exactly 12; every altitude within 350–900 m | PASS |
| C2.8 | Gazetteer vegetation code matches altitude band | 12 of 12 consistent | PASS |
| C2.9 | Source files in `project_source/` (.tex, .bib, .sty) | exactly 10, no strays | PASS |
| C2.10 | Text files stored with LF in the repository | 0 CRLF files | PASS (0) |
| C2.11 | Bibliography entries not yet cited (`berg1982`, `pennington1975`, `harris1996`) | to be cited in M4 family treatments | OPEN (by design) |


## M3 — Data Layer & Methods

**Status:** Complete
**Snapshot:** `milestone_3_data_methods/`
**Compiler:** pdfLaTeX + BibTeX

### Work completed
- Created four tab-separated data files in `data/`: `species.tsv` (18 species), `localities.tsv` (12 localities), `specimens.tsv` (90 synthetic specimens) and `phenology.tsv` (monthly flowering and fruiting for 18 species).
- Created the Materials and Methods chapter: the data files, six validation rules, and two summary tables computed from `specimens.tsv`.
- Created the Key to Families (Chapter 3): a dichotomous key of 9 couplets reaching all 8 families.
- Replaced the incorrect phrase "in the next chapter" in `how_to_use.tex` with a cross-reference to the Key to Families (`\ref{ch:key-families}`).
- Specimen data were produced by a seeded generator (seed 20260927); the script is added to `tools/` in M5.

### Data rules (every specimen must satisfy all six)
1. Altitude equals the locality altitude in `localities.tsv`.
2. The locality's vegetation type is listed for the species in `species.tsv`.
3. Date within the collector's period: Harding 1934–1938, Olaniyan 1961–1967, Alade 2019–2025.
4. Herbarium matches the collector: Harding OKF, Olaniyan SVN, Alade AUH.
5. `fl`/`fr` only in months recorded in `phenology.tsv`; `st` only in months with neither.
6. Each collector's numbers increase with date and are unique.

### Pass/fail checks
| ID | Check | Threshold | Result |
|---|---|---|---|
| C3.1 | Compiles with pdfLaTeX + BibTeX | 0 errors, 0 undefined references or citations | PASS |
| C3.2 | Compiled page count | exactly 19 | PASS (19) |
| C3.3 | Data file shapes (lines × tab-separated columns) | species 19×9; localities 13×5; specimens 91×9; phenology 19×13 | PASS |
| C3.4 | Every data file ends with a newline | 4 of 4 | PASS (missing final newlines found and fixed) |
| C3.5 | SHA-256 (first 12 hex) of data files | localities `1f62be617989`; phenology `710f37814321`; species `2c046495a12f`; specimens `46796adbad60` | PASS |
| C3.6 | Specimen records violating data rules 1–6 | 0 of 90 | PASS |
| C3.7 | `localities.tsv` agrees with Appendix B (name, grid, altitude, vegetation) | 12 of 12 rows | PASS |
| C3.8 | Author abbreviations in `species.tsv` versus Appendix A | 25 used = 25 listed; 0 missing, 0 unused | PASS |
| C3.9 | Table 2.1 matches the data | 8 families; 18 species; 90 specimens; per-family counts exact | PASS |
| C3.10 | Table 2.2 matches the data | Harding 32, Olaniyan 32, Alade 26; fl 23, fr 47, st 20 | PASS |
| C3.11 | Key to Families structure | couplets 1–9 with no gaps; each has a and b; each couplet reached exactly once; all 8 families reachable | PASS (a numbering gap from 4 to 6 was found in draft and fixed) |
| C3.12 | Source files in `project_source/` (.tex, .bib, .sty, .tsv, .txt) | exactly 16, no drafts | PASS (4 re-created drafts removed) |
| C3.13 | Text files stored with LF in the repository | 0 CRLF files | PASS (0) |



## M4 — Treatments, Keys & Figures

**Status:** Complete
**Snapshot:** `milestone_4_treatments/`
**Compiler:** pdfLaTeX + BibTeX

### Work completed
- Added 8 family chapters in `families/` (Anacardiaceae, Combretaceae, Fabaceae, Irvingiaceae, Malvaceae, Meliaceae, Moraceae, Sapotaceae) with 18 species treatments.
- Each treatment gives names, status, synonyms where applicable, description, phenology, habitat, uses with citations, specimens examined, and a distribution map.
- Added a key to species in each family with more than one species (7 keys).
- Added the `\distmap` macro (TikZ grid map, rows A–D × columns 1–5) and `\emergencystretch` to `florula.sty`.
- Added "st." (sterile) to the abbreviations in "How to use this Flora".
- Specimen citations and map squares were generated from `data/specimens.tsv`; the generator is added to `tools/` in M5.

### Domain decisions recorded
- Malvaceae is taken in the broad modern sense, including the former Bombacaceae and Sterculiaceae.
- Burkill (1985) is Volume 1, Families A–D. It is cited only for Anacardiaceae and the former Bombacaceae (*Adansonia*, *Ceiba*).
- Synonyms and names are given with an authority only when every author abbreviation is listed in Appendix A; otherwise the name is given without authority (*Irvingia wombolu*, *Chlorophora*, *Butyrospermum*).

### Pass/fail checks
| ID | Check | Threshold | Result |
|---|---|---|---|
| C4.1 | Compiles with pdfLaTeX + BibTeX | 0 errors, 0 undefined references or citations, 0 overfull boxes | PASS (0) |
| C4.2 | Compiled page count | exactly 42 | PASS (42) |
| C4.3 | Family files in `families/`, each `\input` once in alphabetical order | exactly 8 | PASS |
| C4.4 | Species treatments (`\species`), each labelled `sp:<species_id>` from `species.tsv` | exactly 18 | PASS |
| C4.5 | Specimens cited (collector + number) | 90 of 90, each exactly once, in its own species' treatment | PASS |
| C4.6 | Phenology sentence matches `phenology.tsv` | 18 of 18 | PASS |
| C4.7 | Status (native or cultivated) matches `species.tsv` | 18 of 18 | PASS |
| C4.8 | Distribution map squares equal the grid squares of the cited specimens | 18 of 18 maps | PASS |
| C4.9 | Species keys: couplets numbered without gaps, each has a and b, each species of the family reached exactly once | 7 of 7 keys | PASS |
| C4.10 | Author abbreviations in treatments not listed in Appendix A | 0 | PASS |
| C4.11 | Bibliography entries cited at least once | 15 of 15 (closes C2.11) | PASS |
| C4.12 | Species and specimen counts per family match Table 2.1 | 8 of 8 families | PASS |
| C4.13 | Source files in `project_source/` (.tex, .bib, .sty, .tsv, .txt) | exactly 24, no drafts | PASS (24) |
| C4.14 | Text files stored with LF in the repository | 0 CRLF files | PASS (0) |


## M5 — Final Asset

**Status:** Complete
**Snapshot:** `milestone_5_final/` (identical to `golden_solution/`)
**Compiler:** pdfLaTeX + BibTeX (MiKTeX 26.5); Python 3.12.10 for tools and verifier

### Work completed
- Added Appendix C (Phenological Calendar), `notes/review_log.md`, `notes/open_questions.md`, `build/config.json` and `build/submission.yaml`.
- Added two decoys: `data/archive/specimens_export_2023.tsv` (older export, 87 records, code ARH) and `notes/house_style_2019.md` (outdated style guide).
- Created `golden_solution/` from the correct state and planted four defects in `project_source/`, each raised as an open review remark (R09–R12).
- Added `tools/`: data generator, decoy builder, citation writer, variant builder and manifest builder.
- Added `verifier/`: verifier, expected-value builder, oracle, and the recorded oracle and milestone results.
- Built `variants/variant_B/` (seed 20261001, 126 specimens) and verified it.
- Added `task_brief.md`, `reference_results.md`, `verifiers_spec.md`, `README.md`, `ASSET.md`, `TASK_CATALOGUE.md`, and `requirements.pdf` with its source.

### Planted defects (in `project_source/` only)
| ID | Command used to plant it | Reference fix |
|---|---|---|
| D1 | `sed -i 's/\\end{florakey}/\\end{florakye}/' project_source/families/meliaceae.tex` | `\end{florakey}` |
| D2 | `sed -i 's/^\(S047\t.*\tL08\t\)360\t/\1630\t/' project_source/data/specimens.tsv` | altitude 360 |
| D3 | full month names; `\small` and `\tabcolsep` lines removed from the calendar | restore abbreviations, `\small`, `\tabcolsep{3pt}` (or any fix that keeps every cell) |
| D4 | couplets 5–9 of the Key to Families renumbered 6–10 | couplets 1–9 |

### Pass/fail checks
| ID | Check | Threshold | Result |
|---|---|---|---|
| C5.1 | Golden solution compiles | 0 errors, 0 undefined, 0 overfull, 44 pages | PASS |
| C5.2 | Verifier score of `golden_solution/` | exactly 1.0000 | PASS (1.0000) |
| C5.3 | Verifier score of `project_source/` | below 1 | PASS (0.6154) |
| C5.4 | Files differing between `project_source/` and `golden_solution/` | exactly 5 (four defect sites and the review log) | PASS (5) |
| C5.5 | Open review remarks | 4 in `project_source/`, 0 in `golden_solution/` | PASS |
| C5.6 | Data regenerated by `tools/make_specimens.py` | SHA-256 identical (`46796adbad60`, `710f37814321`) | PASS |
| C5.7 | Decoy export checksum | `3e95c5df6060` | PASS |
| C5.8 | Oracle | 14 of 14 cases as required | PASS (ORACLE PASSED) |
| C5.9 | Milestone scores increase | 0.1538 < 0.2051 < 0.6410 < 0.7949 < 1.0000 | PASS |
| C5.10 | Variant B against its own expected values | exactly 1.0000 | PASS (1.0000) |
| C5.11 | Variant B against the main expected values | gate 0 | PASS (0.0000) |
| C5.12 | `milestone_5_final/` verifier score | exactly 1.0000 | PASS |
| C5.13 | Text files stored with LF in the repository | 0 CRLF files | Verified after commit |
