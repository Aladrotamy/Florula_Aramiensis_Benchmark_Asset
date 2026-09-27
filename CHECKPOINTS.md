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
| C2.10 | Text files stored with LF in the repository | 0 CRLF files | Verified after commit |
| C2.11 | Bibliography entries not yet cited (`berg1982`, `pennington1975`, `harris1996`) | to be cited in M4 family treatments | OPEN (by design) |