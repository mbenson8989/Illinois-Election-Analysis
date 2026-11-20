# Illinois Election Analysis — Governor 2022 & 2026 (reverse factoring)
> **2026 figures are UNOFFICIAL (pre-Dec 4, 2026 canvass).** 2022 figures are SBOE official canvass.
>
> **Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.**

**PDF report:** [Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf](https://github.com/mbenson8989/Illinois-Election-Analysis/blob/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf)  ·  **Cross-link:** [Cedar Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit)

## Headline results
| Item | Result |
|---|---|
| Registration stand-in | Democratic primary ballot share (SBOE official primary canvass) — **stand-in, NOT official party registration** |
| Locked Illinois formula | **Dem-share change (2022→2026) = 0.000194 + (-0.205049) × stand-in drop**  ·  **R² = 0.432249**  ·  n = 60 counties |
| Floor 2022 (most Republican, lowest Dem share of ballots) | Wayne 9.38% |
| Ceiling 2022 (highest Dem share of ballots) | Cook 73.04% |
| Floor 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass) | Wayne 11.93% |
| Ceiling 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass) | Cook 78.79% |
| Over-ballot flags (D+R > ballots cast) | 2022: 0 of 102 · 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass): 0 of 60 |
| Total implied extra votes (Σ residual × 2026 ballots), UNOFFICIAL (pre-Dec 4, 2026 canvass) | 95,592.15 (positive 102,315.77; negative -6,723.62) |
| 2026 county coverage | 60 of 102 counties with a county-authority ballots-cast figure; 42 excluded (listed on [[Reverse-Math]]) |

## Double verification (two independent passes; every cell to the decimal)
| Check | Cells compared | Matched | Mismatched |
|---|---|---|---|
| 2022 SBOE vote file, Pass A vs Pass B | 1,122 | 1,122 | 0 |
| 2022 vs SBOE PDF governor table | 204 | 204 | 0 |
| Stand-in (2022 & 2026 primary ballots), Pass A vs Pass B | 918 | 918 | 0 |
| 2026 county raw D/R/ballots (UNOFFICIAL (pre-Dec 4, 2026 canvass)), Pass A vs Pass B | 300 | 300 | 0 |
| Full computed table (102 counties × 20 cols), Pass A vs Pass B | 2,040 | 2,040 | 0 |
| Statewide summary (constant, multiplier, R², totals, floor/ceiling, flags) | 15 | 15 | 0 |

One mismatch was found and fixed before publication: Stephenson 2026 Dem share = 6,199 / 16,000 = 0.3874375 exactly (a decimal tie). Pass A rounds the exact fraction half-to-even (0.387438); Pass B's float formatting gave 0.387437. Pass B was changed to exact integer half-to-even rounding for vote ratios; both passes were re-run, and all cells now match.

## Pages
- [[Reverse-Math]] — per-county table: shares, stand-in, gap, delta-G, residual, implied extra votes, 2026 sources
- [[Locked-Illinois-Formula]] — statewide fitted equation with R², stand-in evaluation
- [[Floor-and-Ceiling]] — floor/ceiling counties and the over-ballot check, both years
- [[Graphs]] — charts

## Sources
- 2022: Illinois State Board of Elections (SBOE) official canvass: `2022GECty` vote file and `2022GEOfficialVote.pdf`.
- Stand-in: SBOE official primary canvass PDFs, 2022 GP and 2026 GP.
- 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass): SBOE has not posted it (state canvass Fri Dec 4, 2026). County election authority results: direct authority feeds/PDFs (Chicago Board of Election Commissioners summary PDF, county clerk pollresults/Platinum/Clarity/ES&S/EL45 results), or, where noted, voteclock.org transcriptions of the authority's posted results (Cook suburban and other large counties) and three local-radio reprints of the clerk's unofficial report (Fayette, Gallatin, Hamilton). Recorded per county in `raw/sources.json` and the `source_2026_UNOFFICIAL` column. civicAPI (race 87130) used **only** as a cross-check, never in computations.
- Population (sort order): 2020 Census PL 94-171.

---
Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration. 2026 = UNOFFICIAL (pre-Dec 4, 2026 canvass). Cross-link: [Cedar Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) · [PDF report](https://github.com/mbenson8989/Illinois-Election-Analysis/blob/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf) · Built Thursday, November 19, 2026 (CST).
