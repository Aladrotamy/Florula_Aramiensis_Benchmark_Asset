# Task Brief: Florula Aramiensis

Read this brief before editing the Overleaf project in `project_source/`.

## The project

*Florula Aramiensis, Volume I: Economic Trees* is a scholarly regional flora of the Arami Uplands, a fictional West African region. It treats 18 real West African tree species in 8 families. The species descriptions follow the published literature; all specimen records, localities and dates are synthetic.

The book is a multi-file LaTeX project compiled with pdfLaTeX and BibTeX. It has a house style (`florula.sty`), front matter, three introductory chapters (Introduction, Materials and Methods, Key to Families), eight family chapters, three appendices (Author Abbreviations, Gazetteer, Phenological Calendar) and a bibliography. Every count, date, locality and map in the book is drawn from four tab-separated data files in `data/`.

## Your task

The book is complete, but the curator has four remarks open in `notes/review_log.md` (R09 to R12). Resolve all four so that the book is correct and compiles cleanly, then close each remark in the log with a one-line resolution.

The remarks say what is wrong, not where the fix belongs. Use the project's own rules to locate and correct each problem:

- The six data rules in the Materials and Methods chapter.
- The Gazetteer (Appendix B) and `data/localities.tsv`.
- The key conventions in "How to use this Flora".
- The house style in `florula.sty`.

## Constraints

1. Fix the cause of each problem. Do not delete specimen records, table rows, table columns, key couplets or review-log entries to make a problem disappear.
2. The book must compile with pdfLaTeX and BibTeX with no errors, no undefined references or citations, and no overfull boxes. The final PDF has 44 pages.
3. Change only what the four remarks require. Every other file must stay as it is.
4. `data/archive/specimens_export_2023.tsv` is an older export of the specimen database. It is not the active dataset and must not be used in place of `data/specimens.tsv`.
5. `notes/house_style_2019.md` is an outdated draft. The current house style is the one defined in `florula.sty` and "How to use this Flora". Do not apply the 2019 draft.
6. Where a question cannot be settled from the project's own sources, record it in `notes/open_questions.md` rather than guessing.
7. Keep the project editable as LaTeX source, with UTF-8 text and the existing folder structure.

## Expected final state

The final state is the one in `golden_solution/`: all four remarks resolved and closed, the book compiling to 44 pages with no errors, undefined references or overfull boxes, and every data rule satisfied. `verifier/verify.py` scores that state 1.0000.
