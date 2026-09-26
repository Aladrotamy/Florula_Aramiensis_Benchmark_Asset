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
| C1.10 | Text files stored with LF line endings in the repository | 0 CRLF files | Verified after commit with `git ls-files --eol` |