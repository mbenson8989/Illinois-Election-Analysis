"""Builds the 5 wiki pages + _Sidebar.md + README.md from VERIFIED outputs. No numbers are typed by hand except SBOE statewide primary totals quoted from the PDFs."""
import csv, json, sys
sys.path.insert(0,'/workspace/illinois/scripts')
from manifest_2026 import EXCLUDED_NOTE
I='/workspace/illinois/'; O=I+'out/'
UN='UNOFFICIAL (pre-Dec 4, 2026 canvass)'
ST='Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration'
CEDAR='https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit'
REPO='https://github.com/mbenson8989/Illinois-Election-Analysis'
RAW='https://raw.githubusercontent.com/mbenson8989/Illinois-Election-Analysis/main/'
PDF=REPO+'/blob/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf'
RUN='Thursday, November 19, 2026; share-form check added Friday, November 20, 2026 (CST)'
T=list(csv.DictReader(open(O+'il_governor_reverse_math_2022_2026_VERIFIED.csv')))
S=json.load(open(O+'compute_pass_a_summary.json')); V=json.load(open(O+'verification_full.json')); X=json.load(open(O+'il_2026_disagreements_UNOFFICIAL.json'))
G22={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2022.csv'))}
fit=[r for r in T if r['ballots_cast_2026_UNOFFICIAL']]; exc=[r for r in T if not r['ballots_cast_2026_UNOFFICIAL']]

SA=json.load(open(O+'share_pass_a_summary.json'))['fits']; SV=json.load(open(O+'verification_share_form.json'))
def frow(lbl,f): return f"| {lbl} | {f['n']} | {f['m']} | {f['b']} | {f['r_squared']} | {f['mean_abs_residual_pp']} | {f['max_residual_county']} ({f['max_residual_pp']}) | {f['published_applied_mean_abs_residual_pp']} |"
SF=f"""## Share-form check: S = m × (D/100) + b (added Nov 20, 2026, CST)
- **D** = registration stand-in share in percent (Democratic primary ballot share × 100). *{ST}.*
- **S** = surplus in percentage points = 100 × (Dem share of ballots cast − stand-in share) = 100 × gap.
- **Result of the check:** the published change-vs-drop fit above (constant 0.000194, multiplier −0.205049) is in a different form and different units. Applied literally as S = −0.205049 × (D/100) + 0.000194, it does **not** match the data: mean absolute residual {SA['A_2022_official']['published_applied_mean_abs_residual_pp']} pp across all 102 counties in 2022. So the share-form lines below were fitted by OLS from the raw verified data. The change-vs-drop fit above is unchanged and remains the locked formula.
- **Fit C is the published fit, re-expressed.** In share form, delta-G (pp) = {SA['C_deltaG_vs_drop_2026_UNOFFICIAL']['m']} × (drop/100) + {SA['C_deltaG_vs_drop_2026_UNOFFICIAL']['b']}. That is exactly 100 × (1 − 0.205049) and 100 × 0.000194, because delta-G = share change + stand-in drop. Its residuals equal 100 × the published residuals in all {SV['residual_consistency_resC_eq_100xpublished_residual'][1]} counties.

| Fit | n | m | b | R² | Mean abs residual (pp) | Largest residual: county (pp) | Mean abs residual if published m, b applied literally (pp) |
|---|---|---|---|---|---|---|---|
{frow('A: 2022, official, all 102 counties (primary share-form fit)',SA['A_2022_official'])}
{frow(f'B: 2026 {UN}, 60 counties',SA['B_2026_UNOFFICIAL'])}
{frow(f'C: delta-G vs stand-in drop, 2026 {UN}, 60 counties',SA['C_deltaG_vs_drop_2026_UNOFFICIAL'])}

- **Fit A is the primary share-form line** because it is the only one that covers all 102 counties with official data. 2026 cannot cover all 102 counties until the remaining counties report (42 lack a county-authority ballots-cast figure). **No gaps were filled.**
- Per-county S, D, predictions and residuals: [`out/share_pass_a.csv`]({REPO}/blob/main/out/share_pass_a.csv). Chart: [[Graphs]].
- Verification of the share form (Pass A exact fractions vs Pass B numpy): {SV['table_matched']:,} / {SV['table_cells']:,} table cells and {SV['summary_matched']} / {SV['summary_fields']} fit statistics matched, 0 mismatches. S(2022) = 100 × published gap in {SV['gap_consistency_S2022_eq_100xgap'][0]} / {SV['gap_consistency_S2022_eq_100xgap'][1]} counties.
"""
v22=V['verification_2022']
def pct(s): return f"{float(s)*100:.2f}%" if s else '—'
def n(s): return f"{int(s):,}" if s else '—'
HDR=f"> **2026 figures are {UN}.** 2022 figures are SBOE official canvass.\n>\n> **{ST}.**\n"
def foot(): return f"\n---\n{ST}. 2026 = {UN}. Cross-link: [Cedar Audit (Nebraska)]({CEDAR}) · [PDF report]({PDF}) · Built {RUN}.\n"
VER=(f"| Check | Cells compared | Matched | Mismatched |\n|---|---|---|---|\n"
 f"| 2022 SBOE vote file, Pass A vs Pass B | {v22['cells_compared']:,} | {v22['matched']:,} | {v22['mismatched']} |\n"
 f"| 2022 vs SBOE PDF governor table | {v22['pdf_cells_matched']+v22['pdf_cells_mismatched']} | {v22['pdf_cells_matched']} | {v22['pdf_cells_mismatched']} |\n"
 f"| Stand-in (2022 & 2026 primary ballots), Pass A vs Pass B | {V['stand_in_primary_ballots']['cells']:,} | {V['stand_in_primary_ballots']['matched']:,} | {len(V['stand_in_primary_ballots']['mismatches'])} |\n"
 f"| 2026 county raw D/R/ballots ({UN}), Pass A vs Pass B | {V['raw_2026_UNOFFICIAL']['cells']} | {V['raw_2026_UNOFFICIAL']['matched']} | {len(V['raw_2026_UNOFFICIAL']['mismatches'])} |\n"
 f"| Full computed table (102 counties × 20 cols), Pass A vs Pass B | {V['computed_table']['cells']:,} | {V['computed_table']['matched']:,} | {len(V['computed_table']['mismatches'])} |\n"
 f"| Statewide summary (constant, multiplier, R², totals, floor/ceiling, flags) | {V['summary']['fields']} | {V['summary']['matched']} | {len(V['summary']['mismatches'])} |\n")
EQ=f"**Dem-share change (2022→2026) = {S['constant']} + ({S['multiplier']}) × stand-in drop**  ·  **R² = {S['r_squared']}**  ·  n = {S['n_fit']} counties"
EVAL=f"""### Registration stand-in evaluation (Morissa's rule: best available comparable number, not the easiest)
Illinois has **no party registration** (SBOE registration file lists only active/inactive voters per authority). Three candidates were evaluated:

| Option | Coverage | Accuracy as a party-strength measure | Defensibility / citability | Verdict |
|---|---|---|---|---|
| 1. SBOE Democratic primary ballot share (Dem ballots ÷ all primary ballots, per county) | All 102 counties, both 2022 and 2026, one uniform official source | Moderate: measures who *chose a Democratic ballot* in that primary; sensitive to which primaries were contested | Highest: SBOE official canvass PDFs (`2022GPOfficialVote.pdf`, `2026GPOfficialVote.pdf`), reproducible by anyone | **CHOSEN** |
| 2. Party of last primary voted, from county voter files | Not statewide: only some of Illinois' 108 election authorities publish D/R/NPP counts (e.g. Kane); others publish nothing or charge for files | Similar signal to option 1 (it is derived from the same primary choices), but mixed vintages and definitions | Low: inconsistent across counties; cannot cover 102 counties uniformly | Rejected |
| 3. Paid modeled party (L2 / Catalist) | Statewide | Modeled estimate, not a recorded act; method proprietary | Low for a public audit: paid, not reproducible, not citable; **not purchased** | Rejected |

**Caveat — 2022→2026 contest-structure jump.** Statewide the Democratic share of primary ballots went from **51.88%** (911,919 of 1,757,872, June 28, 2022) to **67.87%** (1,283,256 of 1,890,699, March 17, 2026). A 16-point move in one cycle reflects *which primaries were contested* (2022: competitive Republican governor primary; 2026: high-profile Democratic primaries), not a real shift in party loyalty. The stand-in **drop** is therefore negative in most counties, and the fitted multiplier measures how general-election share moved relative to that contest-driven swing. Read results as relative (county vs county), not as registration-based absolutes. Small-county primaries can swing on a single local contest (e.g. Gallatin, a high-leverage point on the fit chart).
"""
# ---- Home
H=f"""# Illinois Election Analysis — Governor 2022 & 2026 (reverse factoring)
{HDR}
**PDF report:** [{PDF.split('/')[-1]}]({PDF})  ·  **Cross-link:** [Cedar Audit (Nebraska)]({CEDAR})

## Headline results
| Item | Result |
|---|---|
| Registration stand-in | Democratic primary ballot share (SBOE official primary canvass) — **stand-in, NOT official party registration** |
| Locked Illinois formula | {EQ} |
| Floor 2022 (most Republican, lowest Dem share of ballots) | {S['floor_2022'][0]} {pct(S['floor_2022'][1])} |
| Ceiling 2022 (highest Dem share of ballots) | {S['ceiling_2022'][0]} {pct(S['ceiling_2022'][1])} |
| Floor 2026 {UN} | {S['floor_2026_UNOFFICIAL'][0]} {pct(S['floor_2026_UNOFFICIAL'][1])} |
| Ceiling 2026 {UN} | {S['ceiling_2026_UNOFFICIAL'][0]} {pct(S['ceiling_2026_UNOFFICIAL'][1])} |
| Over-ballot flags (D+R > ballots cast) | 2022: {len(S['over_ballot_2022'])} of 102 · 2026 {UN}: {len(S['over_ballot_2026'])} of {S['n_fit']} |
| Total implied extra votes (Σ residual × 2026 ballots), {UN} | {float(S['total_implied_extra_votes']):,.2f} (positive {float(S['sum_positive_implied']):,.2f}; negative {float(S['sum_negative_implied']):,.2f}) |
| 2026 county coverage | {len(fit)} of 102 counties with a county-authority ballots-cast figure; {len(exc)} excluded (listed on [[Reverse-Math]]) |

## Double verification (two independent passes; every cell to the decimal)
{VER}
One mismatch was found and fixed before publication: Stephenson 2026 Dem share = 6,199 / 16,000 = 0.3874375 exactly (a decimal tie). Pass A rounds the exact fraction half-to-even (0.387438); Pass B's float formatting gave 0.387437. Pass B was changed to exact integer half-to-even rounding for vote ratios; both passes were re-run, and all cells now match.

## Pages
- [[Reverse-Math]] — per-county table: shares, stand-in, gap, delta-G, residual, implied extra votes, 2026 sources
- [[Locked-Illinois-Formula]] — statewide fitted equation with R², stand-in evaluation
- [[Floor-and-Ceiling]] — floor/ceiling counties and the over-ballot check, both years
- [[Graphs]] — charts

## Sources
- 2022: Illinois State Board of Elections (SBOE) official canvass: `2022GECty` vote file and `2022GEOfficialVote.pdf`.
- Stand-in: SBOE official primary canvass PDFs, 2022 GP and 2026 GP.
- 2026 {UN}: SBOE has not posted it (state canvass Fri Dec 4, 2026). County election authority results: direct authority feeds/PDFs (Chicago Board of Election Commissioners summary PDF, county clerk pollresults/Platinum/Clarity/ES&S/EL45 results), or, where noted, voteclock.org transcriptions of the authority's posted results (Cook suburban and other large counties) and three local-radio reprints of the clerk's unofficial report (Fayette, Gallatin, Hamilton). Recorded per county in `raw/sources.json` and the `source_2026_UNOFFICIAL` column. civicAPI (race 87130) used **only** as a cross-check, never in computations.
- Population (sort order): 2020 Census PL 94-171.
{foot()}"""
# ---- Reverse-Math
rows='\n'.join(f"| {r['county']} | {n(r['pop_2020'])} | {pct(r['standin_dem_primary_share_2022'])} | {pct(r['standin_dem_primary_share_2026'])} | {r['standin_drop_2022_to_2026']} | {pct(r['dem_share_ballots_2022'])} | {r['gap_2022']} | {n(r['ballots_cast_2026_UNOFFICIAL'])} | {pct(r['dem_share_ballots_2026_UNOFFICIAL'])} | {r['gap_2026_UNOFFICIAL'] or '—'} | {r['share_change_2022_to_2026'] or '—'} | {r['delta_G'] or '—'} | {r['expected_change'] or '—'} | {r['residual'] or '—'} | {(f"{float(r['implied_extra_votes']):,.2f}" if r['implied_extra_votes'] else '—')} | {r['source_2026_UNOFFICIAL'] or 'excluded'} |" for r in T)
excl='\n'.join(f"| {r['county']} | {n(r['pop_2020'])} | {r['status_2026'].replace('excluded: ','')} |" for r in exc)
dis_vc='\n'.join(f"| {d['county'].title()} | {d['voteclock'][0]:,} / {d['voteclock'][1]:,} / {d['voteclock'][2]:,} ({d['voteclock_as_of']}) | {d['used'][0]:,} / {d['used'][1]:,} / {d['used'][2]:,} |" for d in X['voteclock_vs_feed'])
dis_cv='\n'.join(f"| {d['county'].title()} | {d['used_D']:,} / {d['used_R']:,} | {d['civicapi_D']:,} / {d['civicapi_R']:,} | {d['diff_D']:+,} / {d['diff_R']:+,} |" for d in X['largest'])
RM=f"""# Reverse Math — county by county (sorted by 2020 population, largest → smallest)
{HDR}
## Definitions
- **Dem share** = Pritzker votes ÷ ballots cast (county total ballots, not the governor-contest total).
- **Stand-in share** = Democratic primary ballots ÷ all primary ballots (SBOE primary canvass). *{ST}.*
- **Gap** = Dem share − stand-in share (same year).
- **Stand-in drop** = stand-in 2022 − stand-in 2026 (negative = the stand-in rose).
- **Share change** = Dem share 2026 − Dem share 2022. **Delta-G** = share change − stand-in change = gap 2026 − gap 2022.
- **Expected change** = {S['constant']} + ({S['multiplier']}) × stand-in drop (see [[Locked-Illinois-Formula]]).
- **Residual** = share change − expected change. **Implied extra votes** = residual × 2026 ballots cast. Positive = more Dem share than the stand-in predicts; negative = less.

{EVAL}
## County table — 2026 columns {UN}
| County | Pop 2020 | Stand-in 2022 | Stand-in 2026 | Stand-in drop | Dem share 2022 | Gap 2022 | Ballots 2026 {UN} | Dem share 2026 {UN} | Gap 2026 | Share change | Delta-G | Expected | Residual | Implied extra votes | 2026 source ({UN}) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{rows}

Full precision, URLs and as-of times: [`out/il_governor_reverse_math_2022_2026_VERIFIED.csv`]({REPO}/blob/main/out/il_governor_reverse_math_2022_2026_VERIFIED.csv).

## 2026 counties excluded ({len(exc)}) — no county-authority ballots-cast figure in hand
No aggregator ballots-cast figures were substituted. These counties have 2022 values only.

| County | Pop 2020 | Reason |
|---|---|---|
{excl}

## 2026 source disagreements ({UN})
Where a voteclock.org transcription of a county page and the county's own vendor feed both existed, the county feed (later timestamp) was used:

| County | voteclock D / R / ballots (as of) | Used: county feed D / R / ballots |
|---|---|---|
{dis_vc}

civicAPI aggregator cross-check (race 87130, last updated {X['civicapi_last_updated_utc']} UTC = 5:30 p.m. CST Nov 19, 2026; {X['civicapi_percent_reporting']}% reporting): {X['exact_D_R_match']} of {X['counties_compared']} counties match exactly on D and R; {X['differ']} differ. Largest differences (used − civicAPI):

| County | Used D / R | civicAPI D / R | Difference D / R |
|---|---|---|---|
{dis_cv}

Most differences are timing: several county snapshots were taken election night (e.g. Will as of Nov 3, 9:41 p.m.) and later counts of mail ballots continue to the Dec 4 canvass. Full list: `out/il_2026_civicapi_crosscheck_UNOFFICIAL.csv`.
{foot()}"""
# ---- Locked
L=f"""# Locked Illinois Formula
{HDR}
## Statewide fitted equation (OLS, unweighted, one point per county)
{EQ}

| Term | Value |
|---|---|
| Constant | {S['constant']} |
| Multiplier (per unit of stand-in drop) | {S['multiplier']} |
| R² | {S['r_squared']} |
| n (counties with 2026 {UN} data) | {S['n_fit']} |
| Mean stand-in drop | {S['mean_standin_drop']} |
| Mean Dem-share change | {S['mean_share_change']} |
| Σ implied extra votes, {UN} | {float(S['total_implied_extra_votes']):,.2f} |

- y = Dem share of ballots cast 2026 {UN} − Dem share of ballots cast 2022 (SBOE official).
- x = stand-in drop = Dem primary ballot share 2022 − Dem primary ballot share 2026. *{ST}.*
- The constant and multiplier are identical to 6 decimals in Pass A (exact rational arithmetic) and Pass B (numpy float64 polyfit).
- The fit will change once the Dec 4, 2026 canvass is certified and the {len(exc)} excluded counties are added.

{SF}
{EVAL}
## Verification
{VER}
{foot()}"""
# ---- Floor & ceiling
def obrows(year):
    out=[]
    for r in T:
        if year=='2022':
            g=G22[r['county_key']]; D,R_,B=int(g['dem_votes']),int(g['rep_votes']),int(g['ballots_cast'])
        else:
            if not r['ballots_cast_2026_UNOFFICIAL']: continue
            D,R_,B=int(r['dem_votes_2026_UNOFFICIAL']),int(r['rep_votes_2026_UNOFFICIAL']),int(r['ballots_cast_2026_UNOFFICIAL'])
        out.append((r['county'],D,R_,B,B-D-R_,D+R_>B))
    return out
ob22=obrows('2022'); ob26=obrows('2026')
c22=sorted(ob22,key=lambda x:x[4])[:5]; c26=sorted(ob26,key=lambda x:x[4])[:5]
tb=lambda L_:'\n'.join(f"| {a} | {b:,} | {c:,} | {b+c:,} | {d:,} | {e:,} | {'**YES**' if f else 'no'} |" for a,b,c,d,e,f in L_)
fc22=sorted(T,key=lambda r:float(r['dem_share_ballots_2022'])); fc26=sorted(fit,key=lambda r:float(r['dem_share_ballots_2026_UNOFFICIAL']))
lst=lambda L_,col:'\n'.join(f"| {r['county']} | {n(r['pop_2020'])} | {pct(r[col])} |" for r in L_)
FC=f"""# Floor and Ceiling counties
{HDR}
Floor = most Republican baseline (lowest Dem share of ballots cast). Ceiling = highest Dem share of ballots cast.

| Year | Floor | Ceiling |
|---|---|---|
| 2022 (SBOE official, 102 counties) | **{S['floor_2022'][0]}** {pct(S['floor_2022'][1])} | **{S['ceiling_2022'][0]}** {pct(S['ceiling_2022'][1])} |
| 2026 {UN} ({S['n_fit']} counties) | **{S['floor_2026_UNOFFICIAL'][0]}** {pct(S['floor_2026_UNOFFICIAL'][1])} | **{S['ceiling_2026_UNOFFICIAL'][0]}** {pct(S['ceiling_2026_UNOFFICIAL'][1])} |

### 2022 — five lowest / five highest Dem share
| County | Pop 2020 | Dem share 2022 |
|---|---|---|
{lst(fc22[:5],'dem_share_ballots_2022')}
| … | | |
{lst(fc22[-5:],'dem_share_ballots_2022')}

### 2026 {UN} — five lowest / five highest Dem share
| County | Pop 2020 | Dem share 2026 {UN} |
|---|---|---|
{lst(fc26[:5],'dem_share_ballots_2026_UNOFFICIAL')}
| … | | |
{lst(fc26[-5:],'dem_share_ballots_2026_UNOFFICIAL')}

## Over-ballot check (D + R votes > ballots cast)
- **2022:** {len(S['over_ballot_2022'])} flags in 102 counties. Closest: {c22[0][0]} ({c22[0][4]:,} under).
- **2026 {UN}:** {len(S['over_ballot_2026'])} flags in {S['n_fit']} counties. Closest: {c26[0][0]} ({c26[0][4]:,} under).

### Closest five, 2022
| County | Dem | Rep | D+R | Ballots cast | Headroom | Over-ballot |
|---|---|---|---|---|---|---|
{tb(c22)}

### Closest five, 2026 {UN}
| County | Dem | Rep | D+R | Ballots cast | Headroom | Over-ballot |
|---|---|---|---|---|---|---|
{tb(c26)}

The registration stand-in is not used in the over-ballot check. *{ST}.*
{foot()}"""
CH=[('il_fit_share_change_vs_standin_drop_UNOFFICIAL.png','Share change vs stand-in drop with the fitted line'),('il_implied_extra_votes_UNOFFICIAL.png','Implied extra votes by county'),
    ('il_dem_share_2022_vs_2026_UNOFFICIAL.png','Dem share of ballots cast, 2022 vs 2026'),('il_gap_standin_vs_dem_share_UNOFFICIAL.png','Stand-in vs Dem share (gap)'),('il_share_form_fits_UNOFFICIAL.png','Share-form fits S = m x (D/100) + b (A 2022 official; B, C 2026)')]
GR=f"# Graphs\n{HDR}\n"+'\n'.join(f"## {t} — 2026 {UN}\n![{t} — 2026 {UN}]({RAW}charts/{f})\n" for f,t in CH)+foot()
SB=f"""**Illinois Election Analysis**
- [[Home]]
- [[Reverse-Math]]
- [[Locked-Illinois-Formula]]
- [[Floor-and-Ceiling]]
- [[Graphs]]
- [PDF report]({PDF})
- [Cedar Audit (Nebraska)]({CEDAR})

2026 = {UN}

{ST}
"""
pages={'Home.md':H,'Reverse-Math.md':RM,'Locked-Illinois-Formula.md':L,'Floor-and-Ceiling.md':FC,'Graphs.md':GR,'_Sidebar.md':SB}
import os, shutil
if os.path.isdir(I+'wiki/images'): shutil.rmtree(I+'wiki/images')
for k,v in pages.items(): open(I+'wiki/'+k,'w').write(v)
RD=f"""# Illinois-Election-Analysis
Reverse-factoring analysis of the Illinois governor races, 2022 (SBOE official) and 2026 (**{UN}**), for all 102 counties.

**{ST}.**

- Wiki: {REPO}/wiki (a copy of the pages is also in [`/wiki`](wiki))
- PDF report: [report/{PDF.split('/')[-1]}](report/{PDF.split('/')[-1]})
- Cross-link: [Cedar Audit (Nebraska)]({CEDAR})

## Result
{EQ}. Floor 2022: {S['floor_2022'][0]} ({pct(S['floor_2022'][1])}); ceiling 2022: {S['ceiling_2022'][0]} ({pct(S['ceiling_2022'][1])}). Over-ballot flags: 2022 {len(S['over_ballot_2022'])}, 2026 {len(S['over_ballot_2026'])}.

## Layout
- `raw/sources.json` — the raw source list: every source URL and fetch time, plus the as-of time for each 2026 county. Bulky raw downloads (SBOE files and 2026 county pages, ~90 MB) are not committed; re-fetch them from the listed URLs into `raw/` to re-run the scripts.
- `scripts/` — `pass_a*.py` (stdlib/regex/pdftotext, exact fractions) and `pass_b*.py` (pandas/BeautifulSoup/pdfplumber, float64): independent passes. `compute_a.py`/`compute_b.py` produce the metrics, and `verify_full.py` compares them cell by cell.
- `out/` — verified tables, pass outputs, `verification_full.json`, the 2026 cross-check and disagreements.
- `charts/`, `report/`, `wiki/`.

## Verification
{VER}
Built {RUN}.
"""
open(I+'README.md','w').write(RD)
print('ok', len(fit), len(exc), c26[0])
