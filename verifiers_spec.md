# Verifier Specification

The verifier is `verifier/verify.py`. It takes a project folder, compiles it in a temporary copy (pdflatex, bibtex, pdflatex, pdflatex) and applies the checks below. Expected values are stored in `verifier/expected.json`, which `verifier/build_expected.py` builds from `golden_solution/`.

```
python verifier/verify.py project_source          # score one state
python verifier/verify.py golden_solution         # must print SCORE 1.0000
python verifier/run_oracle.py                     # admission test (14 cases)
```

## Scoring rule

score = gate × (sum of weights of passed checks / 39)

- **gate** is 0 if any invariant G1–G4 fails, otherwise 1. Collateral damage and shortcut solutions therefore score 0, not partial credit.
- There are 20 weighted checks with a total weight of 39. Each check is pass/fail with the threshold stated.
- Text comparisons normalise CRLF to LF and ignore a missing final newline, so the result does not depend on the editor or operating system.

## Invariants (gate)

| ID | Invariant | Threshold |
|---|---|---|
| G1 | Frozen files unchanged: 26 files (`main.tex`, `florula.sty`, bibliography, 4 front-matter files, 2 chapters, appendices A–B, 7 unaffected family files, species/localities/phenology data, both decoys, both build files, open questions) | SHA-256 equal for 26 of 26 |
| G2 | Nothing but whitespace after `\end{document}` in `main.tex` | 0 characters |
| G3 | Decoy conventions absent from all `.tex` files: spaced author initials (`C. C. Berg`, `A. Chev.`, `C. F. Gaertn.`), bracketed herbarium codes (`[AUH]`), dotted dates (`05.04.1934`), decoy code `ARH` | 0 matches |
| G4 | No file flooding | at most 35 source files |

## Weighted checks

| ID | Weight | Check | Threshold |
|---|---|---|---|
| C01 | 3 | Compiles | 0 lines beginning with `!` in the log; PDF produced |
| C02 | 1 | Page count | exactly 44 (±0) |
| C03 | 2 | Overfull boxes | 0 |
| C04 | 1 | Undefined references or citations | 0 |
| S01 | 2 | Files `\input` by `main.tex` | the 18 expected files, each once, in the expected order |
| D01 | 2 | Data file shapes | species 19×9, localities 13×5, specimens 91×9, phenology 19×13; each file ends with a newline |
| D02 | 4 | Six data rules | 0 violations over 90 specimens |
| D03 | 2 | `specimens.tsv` | SHA-256 equals the generator output (`46796adbad60…`) |
| D04 | 1 | Gazetteer | 12 of 12 rows equal to `localities.tsv` |
| T01 | 3 | Specimen citations | 90 of 90 cited exactly once, in their own species treatment |
| T02 | 2 | Distribution maps | 18 of 18 maps equal the set of grid squares of the cited specimens |
| T03 | 2 | Phenology statements | 18 of 18 agree month for month with `phenology.tsv` |
| T04 | 3 | Phenological calendar | 12 month columns in order; 18 rows; 216 of 216 cells agree |
| K01 | 3 | Key to Families | couplets numbered 1..n with no gaps; each has a and b; couplets 2..n each referenced exactly once; all 8 families reachable |
| K02 | 1 | Species keys | 7 of 7 keys pass the same rules; every species of the family reachable |
| N01 | 2 | Author abbreviations | 25 listed in Appendix A; 0 used but not listed |
| N02 | 1 | Bibliography | 15 of 15 entries cited; 0 citations to missing keys |
| M01 | 2 | Methods tables | every row of Tables 2.1 and 2.2 recomputed from the data |
| B01 | 1 | Build files | `config.json` and `submission.yaml` agree: pages 44, species 18, specimens 90, families 8, references 15, abbreviations 25 |
| L01 | 1 | Review log | 12 entries, in order; all closed with a non-empty resolution; R01–R08 text unchanged |

## Defect coverage

| Defect | Detected by | What a correct fix must also preserve |
|---|---|---|
| D1 compile-blocking environment name | C01, C02, C04 | G1: the other seven family files unchanged |
| D2 altitude of S047 | D02, D03 | D01 and T01: the record must be corrected, not deleted |
| D3 overflowing calendar | C03 | T04: all 18 rows and 12 columns kept |
| D4 key numbering | K01 | K01: all 8 families still reachable |
| Review log | L01 | L01: no entry removed or rewritten |

## Oracle (admission test)

`verifier/run_oracle.py` runs five stages. The recorded output is in `verifier/oracle_report.txt`.

| Stage | Requirement | Result |
|---|---|---|
| Null | starting state scores below 1 | 0.6154 |
| Solver | golden solution scores exactly 1 | 1.0000 |
| Monotone | applying D1, D2, D3, D4 in turn never lowers the score | 0.6923, 0.8462, 0.8974, 1.0000 |
| Adversarial | no wrong solution reaches 1 | drop last fix 0.9231; close log only 0.6410; delete calendar columns 0.9231; delete record S047 0.6154; use decoy export 0.6154; apply 2019 style 0.0000; paste after `\end{document}` 0.0000 |
| Alternative | a different valid fix of D3 (`\resizebox`) scores 1 | 1.0000 |

## Milestone progression

`verifier/milestone_progress.txt` records the ungated score of each milestone snapshot: M1 0.1538, M2 0.2051, M3 0.6410, M4 0.7949, final 1.0000. The scores increase at every milestone.

## Second variant

`variants/variant_B/` is a complete second version of the book built by `tools/make_variant.py` (seed 20261001, 7 specimens per species, 126 specimens). Against its own `expected.json` it scores 1.0000; against the main `expected.json` its gate is 0, which shows the verifier detects a changed dataset. Results are in `variants/variant_B/verification.txt`.
