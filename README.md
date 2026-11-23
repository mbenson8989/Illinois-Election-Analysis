# Illinois-Election-Analysis
Reverse-factoring (ΔG method) analysis of the Illinois governor races, 2022 (SBOE official) and 2026 (**UNOFFICIAL (pre-Dec 4, 2026 canvass)**), for all 102 counties. Wiki pages follow the Nebraska wiki format.

**Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.**

- Wiki: https://github.com/mbenson8989/Illinois-Election-Analysis/wiki (a copy of the pages is also in [`/wiki`](wiki))
- PDF report: [report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf](report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf)
- Cross-link: [Cedar Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit)

## Result
**Surplus Equation (locked): S = -24.769946 × (D/100) + 12.831550**. This is the 2022 official fit across n = 102 counties, R² = 0.238576; S = Dem share of ballots cast − D, in points; D = stand-in share in percent. Original change-vs-drop fit: **Dem-share change (2022→2026) = 0.000204 + (-0.197856) × stand-in drop**  ·  **R² = 0.440899**  ·  n = 80 counties. Baseline floor 2022: Wayne (9.38%); ceiling 2022: Cook (73.04%). ΔG ceiling/floor 2026*: Gallatin / McHenry. Over-ballot flags: 2022 0, 2026 0.

## Layout
- `raw/sources.json`: the raw source list. It has every source URL and fetch time, plus the as-of time for each 2026 county. Bulky raw downloads (~90 MB) are not committed; re-fetch them from the listed URLs into `raw/` to re-run the scripts.
- `scripts/`: the independent passes, `pass_a*.py` / `compute_a.py` / `share_a.py` / `ne_a.py` (stdlib, exact fractions) and `pass_b*.py` / `compute_b.py` / `share_b.py` / `ne_b.py` (pandas/BeautifulSoup/pdfplumber, float64), plus the `verify*.py` cell-by-cell comparisons.
- `out/`: verified tables, the pass outputs, the `verification*.json` files, and the 2026 cross-check and disagreements.
- `charts/`, `report/`, `wiki/`.

## Verification
| Check | Cells compared | Matched | Mismatched |
|---|---|---|---|
| 2022 SBOE vote file, Pass A vs Pass B | 1,122 | 1,122 | 0 |
| 2022 vs SBOE PDF governor table | 204 | 204 | 0 |
| Stand-in (2022 & 2026 primary ballots), Pass A vs Pass B | 918 | 918 | 0 |
| 2026 county raw D/R/ballots (UNOFFICIAL (pre-Dec 4, 2026 canvass)), Pass A vs Pass B | 400 | 400 | 0 |
| Full computed table (102 counties × 20 cols), Pass A vs Pass B | 2,040 | 2,040 | 0 |
| Statewide summary (constant, multiplier, R², totals, floor/ceiling, flags) | 15 | 15 | 0 |
| Share-form fits (S = m × (D/100) + b), Pass A vs Pass B | 1,872 | 1,872 | 0 |
| Nebraska-format template lines (S, R, G, ΔG, ΔR, surplus, gap in votes; 80 counties) and vote-share-growth fit, Pass A vs Pass B | 2,172 | 2,172 | 0 |

Built Sunday, November 22, 2026, 11:59 PM CST (2026 county data refreshed Nov 22).
