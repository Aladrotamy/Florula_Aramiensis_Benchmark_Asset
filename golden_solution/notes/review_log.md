# Review log

Editorial remarks on Florula Aramiensis, Volume I. Every remark stays in the log. Close a remark only when the fix is in the project and the book compiles cleanly; record what was done.

| ID | Raised by | Location | Remark | Status | Resolution |
|---|---|---|---|---|---|
| R01 | Editor | `frontmatter/` | A second copy of `titlepage.tex` sits outside `frontmatter/`. | Closed | Duplicate confirmed identical and deleted. |
| R02 | Curator | `frontmatter/how_to_use.tex` | "How to use" says the Key to Families is "in the next chapter"; it is not. | Closed | Replaced with a cross-reference to the Key to Families chapter. |
| R03 | Curator | `frontmatter/how_to_use.tex` | Specimen lines use "st." but the abbreviations table does not list it. | Closed | Added "st., sterile" to the abbreviations table. |
| R04 | Editor | `data/*.tsv` | The data files do not end with a newline, so checksums differ from the generator output. | Closed | Final newline added to all four files; checksums now match. |
| R05 | Curator | `families/` | Burkill (1985) is Volume 1, Families A--D, but was about to be cited for families outside that range. | Closed | Cited only for Anacardiaceae and the former Bombacaceae. |
| R06 | Curator | `families/irvingiaceae.tex` | The authority "Vermoesen" is not in Appendix A. | Closed | Name given without authority. |
| R07 | Editor | `keys/key_to_families.tex` | Draft key jumped from couplet 4 to couplet 6. | Closed | Couplets renumbered 1--9. |
| R08 | Editor | `florula.sty` | A specimen paragraph ran 0.8 pt into the margin. | Closed | Added `\emergencystretch` to the house style. |
| R09 | Curator | `families/` | One family chapter no longer builds since its key was last edited. | Closed | Misspelt environment name in the Meliaceae key corrected. |
| R10 | Curator | `data/specimens.tsv` | Methods rule 1 says every specimen altitude equals its locality altitude. One record does not. | Closed | Altitude of S047 corrected from 630 to 360 (Ireke Ferry). |
| R11 | Curator | Appendix C | The phenological calendar runs off the right-hand margin in the PDF. Make it fit; keep every month and every species. | Closed | Month names abbreviated and the table set in small type. |
| R12 | Curator | `keys/key_to_families.tex` | A user reports that the Key to Families cannot be followed after "Leaves simple". | Closed | Couplet numbering restored to 1--9 with no gaps. |