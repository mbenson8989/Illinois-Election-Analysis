# Illinois-Election-Analysis
Reverse-factoring analysis of the Illinois governor races, 2022 (SBOE official) and 2026 (**UNOFFICIAL (pre-Dec 4, 2026 canvass)**), for all 102 counties.

**Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.**

- Wiki: https://github.com/mbenson8989/Illinois-Election-Analysis/wiki (a copy of the pages is also in [`/wiki`](wiki))
- PDF report: [report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf](report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf)
- Cross-link: [Cedar Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit)

## Result
**Dem-share change (2022→2026) = 0.000194 + (-0.205049) × stand-in drop**  ·  **R² = 0.432249**  ·  n = 60 counties. Floor 2022: Wayne (9.38%); ceiling 2022: Cook (73.04%). Over-ballot flags: 2022 0, 2026 0.

## Layout
- `raw/sources.json` — the raw source list: every source URL and fetch time, plus the as-of time for each 2026 county. Bulky raw downloads (SBOE files and 2026 county pages, ~90 MB) are not committed; re-fetch them from the listed URLs into `raw/` to re-run the scripts.
- `scripts/` — `pass_a*.py` (stdlib/regex/pdftotext, exact fractions) and `pass_b*.py` (pandas/BeautifulSoup/pdfplumber, float64): independent passes. `compute_a.py`/`compute_b.py` produce the metrics, and `verify_full.py` compares them cell by cell.
- `out/` — verified tables, pass outputs, `verification_full.json`, the 2026 cross-check and disagreements.
- `charts/`, `report/`, `wiki/`.

## Verification
| Check | Cells compared | Matched | Mismatched |
|---|---|---|---|
| 2022 SBOE vote file, Pass A vs Pass B | 1,122 | 1,122 | 0 |
| 2022 vs SBOE PDF governor table | 204 | 204 | 0 |
| Stand-in (2022 & 2026 primary ballots), Pass A vs Pass B | 918 | 918 | 0 |
| 2026 county raw D/R/ballots (UNOFFICIAL (pre-Dec 4, 2026 canvass)), Pass A vs Pass B | 300 | 300 | 0 |
| Full computed table (102 counties × 20 cols), Pass A vs Pass B | 2,040 | 2,040 | 0 |
| Statewide summary (constant, multiplier, R², totals, floor/ceiling, flags) | 15 | 15 | 0 |

Built Thursday, November 19, 2026; share-form check added Friday, November 20, 2026 (CST).
