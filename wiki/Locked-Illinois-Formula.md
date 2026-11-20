# Locked Illinois Formula
> **2026 figures are UNOFFICIAL (pre-Dec 4, 2026 canvass).** 2022 figures are SBOE official canvass.
>
> **Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.**

## Statewide fitted equation (OLS, unweighted, one point per county)
**Dem-share change (2022→2026) = 0.000194 + (-0.205049) × stand-in drop**  ·  **R² = 0.432249**  ·  n = 60 counties

| Term | Value |
|---|---|
| Constant | 0.000194 |
| Multiplier (per unit of stand-in drop) | -0.205049 |
| R² | 0.432249 |
| n (counties with 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass) data) | 60 |
| Mean stand-in drop | -0.112464 |
| Mean Dem-share change | 0.023255 |
| Σ implied extra votes, UNOFFICIAL (pre-Dec 4, 2026 canvass) | 95,592.15 |

- y = Dem share of ballots cast 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass) − Dem share of ballots cast 2022 (SBOE official).
- x = stand-in drop = Dem primary ballot share 2022 − Dem primary ballot share 2026. *Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.*
- The constant and multiplier are identical to 6 decimals in Pass A (exact rational arithmetic) and Pass B (numpy float64 polyfit).
- The fit will change once the Dec 4, 2026 canvass is certified and the 42 excluded counties are added.

### Registration stand-in evaluation (Morissa's rule: best available comparable number, not the easiest)
Illinois has **no party registration** (SBOE registration file lists only active/inactive voters per authority). Three candidates were evaluated:

| Option | Coverage | Accuracy as a party-strength measure | Defensibility / citability | Verdict |
|---|---|---|---|---|
| 1. SBOE Democratic primary ballot share (Dem ballots ÷ all primary ballots, per county) | All 102 counties, both 2022 and 2026, one uniform official source | Moderate: measures who *chose a Democratic ballot* in that primary; sensitive to which primaries were contested | Highest: SBOE official canvass PDFs (`2022GPOfficialVote.pdf`, `2026GPOfficialVote.pdf`), reproducible by anyone | **CHOSEN** |
| 2. Party of last primary voted, from county voter files | Not statewide: only some of Illinois' 108 election authorities publish D/R/NPP counts (e.g. Kane); others publish nothing or charge for files | Similar signal to option 1 (it is derived from the same primary choices), but mixed vintages and definitions | Low: inconsistent across counties; cannot cover 102 counties uniformly | Rejected |
| 3. Paid modeled party (L2 / Catalist) | Statewide | Modeled estimate, not a recorded act; method proprietary | Low for a public audit: paid, not reproducible, not citable; **not purchased** | Rejected |

**Caveat — 2022→2026 contest-structure jump.** Statewide the Democratic share of primary ballots went from **51.88%** (911,919 of 1,757,872, June 28, 2022) to **67.87%** (1,283,256 of 1,890,699, March 17, 2026). A 16-point move in one cycle reflects *which primaries were contested* (2022: competitive Republican governor primary; 2026: high-profile Democratic primaries), not a real shift in party loyalty. The stand-in **drop** is therefore negative in most counties, and the fitted multiplier measures how general-election share moved relative to that contest-driven swing. Read results as relative (county vs county), not as registration-based absolutes. Small-county primaries can swing on a single local contest (e.g. Gallatin, a high-leverage point on the fit chart).

## Verification
| Check | Cells compared | Matched | Mismatched |
|---|---|---|---|
| 2022 SBOE vote file, Pass A vs Pass B | 1,122 | 1,122 | 0 |
| 2022 vs SBOE PDF governor table | 204 | 204 | 0 |
| Stand-in (2022 & 2026 primary ballots), Pass A vs Pass B | 918 | 918 | 0 |
| 2026 county raw D/R/ballots (UNOFFICIAL (pre-Dec 4, 2026 canvass)), Pass A vs Pass B | 300 | 300 | 0 |
| Full computed table (102 counties × 20 cols), Pass A vs Pass B | 2,040 | 2,040 | 0 |
| Statewide summary (constant, multiplier, R², totals, floor/ceiling, flags) | 15 | 15 | 0 |


---
Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration. 2026 = UNOFFICIAL (pre-Dec 4, 2026 canvass). Cross-link: [Cedar Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) · [PDF report](https://github.com/mbenson8989/Illinois-Election-Analysis/blob/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf) · Built Thursday, November 19, 2026 (CST).
