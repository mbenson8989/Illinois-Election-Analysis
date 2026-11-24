# Illinois 2022 vs 2026 Governor Race: ΔG Method

**Version 2, built Sunday, November 22, 2026, 11:59 PM CST (2026 county data refreshed Nov 22)**

> **\*2026 figures are UNOFFICIAL (pre-Dec 4, 2026 canvass), not certified by the Illinois State Board of Elections.** Governor race unless a page says otherwise. Votes are votes for the Democratic candidate. **Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration:** R and D on these pages are Democratic primary ballots ÷ all primary ballots × 100 (SBOE official primary canvass), not a count of registered Democrats. These pages measure a pattern; they make no claim about intent, fraud or cause.

Method: Morissa Benson's ΔG reverse-factoring method, as built out on the [Nebraska wiki](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki). Data: Illinois State Board of Elections (SBOE) official 2022 general and 2022/2026 primary canvasses; 2026\* county election-authority results (UNOFFICIAL (pre-Dec 4, 2026 canvass)).

> **[Resources](Resources): the draft Attorney General letter, letters for all 108 Illinois election authorities, voting equipment for every county, four flip-county graphics and a Guarantee Clause graphic.**

**PDF report:** [Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf](https://github.com/mbenson8989/Illinois-Election-Analysis/blob/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf)

## Contents

Illinois has no party registration, so every page uses a labeled stand-in: Democratic primary ballot share. The pages build from one county up to the statewide formula.

1. [Cedar County Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit): where the method began
2. [Bottom-Up Reverse Math](Reverse-Math): Cook → all counties with 2026\* data → excluded counties and sources
3. [Locked Illinois Formula](Locked-Illinois-Formula): the Surplus Equation, with a blank fill-in template
4. [Floor and Ceiling Counties](Floor-and-Ceiling): the counties at the top and bottom of ΔG, plus the baseline floor/ceiling and the over-ballot check
5. [Graphs](Graphs): share-form fits, stand-in vs Dem share, change-vs-drop fit, 2022 vs 2026, implied extra votes

## Statewide at a glance

| Item | Result |
|---|---|
| Registration stand-in | Democratic primary ballot share (SBOE official primary canvass): **stand-in, NOT official party registration** |
| **Surplus Equation (locked)** | **S = -24.769946 × (D/100) + 12.831550** (2022 official, n = 102, R² = 0.238576) |
| Original change-vs-drop fit | **Dem-share change (2022→2026) = 0.000204 + (-0.197856) × stand-in drop**  ·  **R² = 0.440899**  ·  n = 80 counties |
| ΔG ceiling / floor, 2026\* | Gallatin +23.01\* / McHenry -22.05\* |
| Baseline floor / ceiling 2022 (Dem share of ballots) | Wayne 9.38% / Cook 73.04% |
| Baseline floor / ceiling 2026\* | Wayne 11.93% / Cook 78.79% |
| Over-ballot flags (D+R > ballots cast) | 2022: 0 of 102 · 2026\*: 0 of 80 |
| Total implied extra votes (Σ residual × 2026 ballots)\* | 99,653.31 (positive 107,048.43; negative -7,395.12) |
| 2026 county coverage | 80 of 102 counties with a county-authority ballots-cast figure; 22 excluded (listed on [Bottom-Up Reverse Math](Reverse-Math)) |

## Double verification (two independent passes; every cell to the decimal)
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

Two mismatches were caught and fixed before any publication:
- **Stephenson, 2026 Dem share:** 6,199 / 16,000 = 0.3874375 exactly. Pass B's float rounding gave 0.387437; it now uses exact half-even rounding.
- **Kendall, 2026 G:** Pass A printed −0.00 where Pass B printed 0.00. Pass A now drops the sign on a rounded zero.

## Sources
- 2022: SBOE official canvass, the `2022GECty` vote file and `2022GEOfficialVote.pdf`.
- Stand-in: SBOE official primary canvass PDFs, 2022 GP and 2026 GP.
- 2026 (UNOFFICIAL (pre-Dec 4, 2026 canvass)): not yet posted by SBOE; the state canvass is Fri Dec 4, 2026. County results come from the election authorities:
  - direct feeds and PDFs (the Chicago Board of Election Commissioners summary PDF, and county clerks' pollresults, gbsvote, Platinum, Clarity, LiveVoterTurnout, ES&S, EL45 and canvass results; Jefferson's scanned official summary was read by OCR in Pass A and by an independent visual transcription in Pass B);
  - where noted, voteclock.org transcriptions of the authority's posted results;
  - three local-radio reprints of the clerk's unofficial report (Fayette, Gallatin, Hamilton).

  Each county's source is recorded in `raw/sources.json` and in the source column of the county tables. civicAPI (race 87130) was used **only** as a cross-check.
- Population (sort order): 2020 Census PL 94-171.

---
**Related:** [Bottom-Up Reverse Math](Reverse-Math) · [Locked Illinois Formula](Locked-Illinois-Formula) · [Floor and Ceiling Counties](Floor-and-Ceiling) · [Graphs](Graphs) · [Cedar County Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) · [PDF report](https://github.com/mbenson8989/Illinois-Election-Analysis/blob/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf)

Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration. 2026 = UNOFFICIAL (pre-Dec 4, 2026 canvass). Built Sunday, November 22, 2026, 11:59 PM CST (2026 county data refreshed Nov 22).
