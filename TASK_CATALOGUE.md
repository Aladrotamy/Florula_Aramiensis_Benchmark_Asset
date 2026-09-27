# Task Catalogue

Each task is seeded by making one change to `golden_solution/` (the seed), is described to the agent by one instruction, and is scored by the named verifier checks. Every seed site is independent of the others, so tasks can be composed. Difficulty follows the Turing report: base 1.0; +1.0 computed answer; +0.5 multi-file; +0.5 implicit (not named in the instruction); +0.5 beyond typing.

## Single-step tasks

| # | Family | Seed (change to the golden state) | Instruction (short form) | Checks | d |
|---|---|---|---|---|---|
| 1 | Compile | Misspell one environment end in any family file | "One family chapter no longer builds; fix it." | C01 | 1.5 |
| 2 | Compile | Remove `\input{families/X}` from `main.tex` | "A family is missing from the book." | S01, T01 | 1.5 |
| 3 | Compile | Break one `\cite` key | "A citation prints as ?; correct it." | C04, N02 | 2.0 |
| 4 | Data | Change one specimen altitude | "Rule 1 fails for one record; correct it." | D02, D03 | 2.5 |
| 5 | Data | Change one specimen herbarium code | "Rule 4 fails for one record; correct it." | D02, D03 | 2.5 |
| 6 | Data | Swap two collector numbers of one collector | "Rule 6 fails; restore the order." | D02, D03 | 2.5 |
| 7 | Data | Move a specimen date outside the collector's period | "Rule 3 fails for one record." | D02, D03 | 2.5 |
| 8 | Data | Delete the final newline of a data file | "The data files must end with a newline." | D01 | 1.0 |
| 9 | Data | Change one gazetteer altitude | "Appendix B disagrees with the data." | D04 | 2.0 |
| 10 | Computed | Replace one count in Table 2.1 with `XX` | "Fill in the placeholder from the data." | M01 | 2.0 |
| 11 | Computed | Replace the collector totals in Table 2.2 | "Recompute Table 2.2 from the data." | M01 | 2.0 |
| 12 | Computed | Set `pages` in `submission.yaml` to a wrong value | "Make the build files agree with the book." | B01 | 2.5 |
| 13 | Computed | Remove one row of the phenological calendar | "Complete the calendar from the data." | T04 | 2.0 |
| 14 | Treatments | Remove one `\specimen{...}` line | "One specimen is not cited; cite it." | T01 | 2.5 |
| 15 | Treatments | Move one specimen line to the wrong species | "A specimen is cited under the wrong species." | T01 | 2.5 |
| 16 | Treatments | Remove one square from a `\distmap` | "A distribution map disagrees with its specimens." | T02 | 2.5 |
| 17 | Treatments | Change one month in a phenology sentence | "A phenology statement disagrees with the data." | T03 | 2.0 |
| 18 | Layout | Full month names in the calendar (D3) | "The calendar runs off the page; keep every cell." | C03, T04 | 3.0 |
| 19 | Layout | Remove `\emergencystretch` from `florula.sty` | "A specimen paragraph overflows the margin." | C03 | 3.0 |
| 20 | Keys | Renumber couplets with a gap (D4) | "The Key to Families cannot be followed." | K01 | 2.0 |
| 21 | Keys | Point one lead to a wrong couplet in a species key | "A species key sends users in a loop." | K02 | 2.0 |
| 22 | Nomenclature | Use an authority not in Appendix A | "Every author abbreviation must be listed." | N01 | 2.0 |
| 23 | Nomenclature | Delete one abbreviation from Appendix A | "Appendix A is missing an author." | N01 | 2.0 |
| 24 | Nomenclature | Write `C. C. Berg` (2019 style) in one place | "Author initials must follow the house style." | G3 | 1.5 |
| 25 | Bibliography | Remove the only citation of one reference | "Every reference must be cited." | N02 | 2.0 |
| 26 | Bibliography | Replace `{\'e}` by `e` in an author name | "Restore the accented author name." | G1 | 1.5 |
| 27 | Review log | Reopen any closed remark whose fix is present | "Close the remarks that are already resolved." | L01 | 1.5 |
| 28 | Open questions | Ask the agent to add a fact it cannot verify | "Record it as an open question instead of guessing." | task-specific: one new row in `open_questions.md`; all `.tex` files unchanged | 1.5 |
| 29 | Decoy | Instruction mentions "the export" ambiguously | "Recompute Table 2.2 from the specimen data." | M01, G3 | 2.5 |
| 30 | Regeneration | Ask for a new variant | "Build the flora with 6 specimens per species." | full verifier on the variant | 3.0 |

## Composed tasks

Seeds at different sites do not interact, so any combination is admissible. Examples:

| Name | Components | Why it is hard |
|---|---|---|
| `COMPOSE__data_altitude__calendar_overflow` | 4 + 18 | One fix is in data, one only visible in the PDF |
| `COMPOSE__key_gap__authority_unlisted__log_close` | 20 + 22 + 27 | Logic, nomenclature and bookkeeping in three files |
| `COMPOSE__decoy_recompute__yaml_pages` | 29 + 12 | Must choose the right data file and read the page count from the build |
| The starting state of this asset | 1 + 4 + 18 + 20 + 27 | All four defect kinds plus the review log |

## Instruction registers

Each task can be phrased in three registers without changing what the verifier checks:
- **Specification:** "In `data/specimens.tsv`, correct the altitude of S047 to match its locality."
- **Curator's remark:** "Methods rule 1 says every specimen altitude equals its locality altitude. One record does not."
- **Colleague:** "One of the Ireke Ferry specimens has the wrong height in the data. Can you fix it?"
