"""Nebraska-format rebuild of the 5 Illinois wiki pages + sidebar (format reference: Nebraska-Election-Analysis- wiki, read-only).
Reuses every verified definition from wiki_build.py (executed up to page assembly), then overrides the pages."""
src=open('/workspace/illinois/scripts/wiki_build.py').read()
exec(src[:src.index("pages={'Home.md'")])
RUN='Sunday, November 22, 2026, 11:59 PM CST (2026 county data refreshed Nov 22)'
NE=json.load(open(O+'ne_format_pass_a_summary.json')); NV=json.load(open(O+'verification_ne_format.json'))
PX={r['county_key']:r for r in csv.DictReader(open(O+'proxy_primary_pass_a.csv'))}
NT={r['county_key']:r for r in csv.DictReader(open(O+'ne_format_pass_a.csv'))}
A=SA['A_2022_official']; Bf=SA['B_2026_UNOFFICIAL']; Cf=SA['C_deltaG_vs_drop_2026_UNOFFICIAL']; VG=NE['vote_share_growth_fit']
ck=NT['COOK']; P=lambda s: s if s.startswith('-') else '+'+s
DISC=(f"> **\\*2026 figures are {UN}, not certified by the Illinois State Board of Elections.** Governor race unless a page says otherwise. Votes are votes for the Democratic candidate. "
      f"**{ST}:** R and D on these pages are Democratic primary ballots ÷ all primary ballots × 100 (SBOE official primary canvass), not a count of registered Democrats. "
      "These pages measure a pattern; they make no claim about intent, fraud or cause.\n")
REL=lambda here: "\n---\n**Related:** "+' · '.join(f"[{t}]({p})" for t,p in [('Bottom-Up Reverse Math','Reverse-Math'),('Locked Illinois Formula','Locked-Illinois-Formula'),('Floor and Ceiling Counties','Floor-and-Ceiling'),('Graphs','Graphs'),('Home','Home')] if p!=here)+f" · [Cedar County Audit (Nebraska)]({CEDAR}) · [PDF report]({PDF})\n\n{ST}. 2026 = {UN}. Built {RUN}.\n"
VERN=VER+(f"| Share-form fits (S = m × (D/100) + b), Pass A vs Pass B | {SV['table_cells']+SV['summary_fields']:,} | {SV['table_matched']+SV['summary_matched']:,} | {len(SV['table_mismatches'])+len(SV['summary_mismatches'])} |\n"
          f"| Nebraska-format template lines (S, R, G, ΔG, ΔR, surplus, gap in votes; 80 counties) and vote-share-growth fit, Pass A vs Pass B | {NV['table_cells']+NV['summary_fields']:,} | {NV['table_matched']+NV['summary_matched']:,} | {len(NV['table_mismatches'])+len(NV['summary_mismatches'])} |\n")
# ---------------- Locked (surplus form only; t4u: no delta-G form on this page)
SU=json.load(open(O+'surplus_pass_a_summary.json')); SUV=json.load(open(O+'verification_surplus_locked.json'))
LA=SU['LOCKED_2022_official']; from decimal import Decimal,ROUND_HALF_EVEN; CKSH=str((Decimal(int(G22['COOK']['dem_votes'])*100)/Decimal(int(G22['COOK']['ballots_cast']))).quantize(Decimal('0.000001'),ROUND_HALF_EVEN)); LB=SU['SECONDARY_2026_UNOFFICIAL']
SUR={r['county_key']:r for r in csv.DictReader(open(O+'surplus_pass_a.csv'))}; cs=SUR['COOK']
VERL='\n'.join(l for l in VERN.split('\n') if 'Nebraska-format template lines' not in l)+(f"| Locked surplus equation (S, D, fitted, residual for 102 counties; fit statistics), Pass A vs Pass B | {SUV['table_cells']+SUV['fit_fields']:,} | {SUV['table_matched']+SUV['fit_matched']:,} | {len(SUV['table_mismatches'])+len(SUV['fit_mismatches'])} |\n")
L=f"""# Locked Illinois Formula

{DISC}
## The equation

- **Dem share** = Democratic governor votes ÷ total ballots cast × 100
- **D** (registration-share **STAND-IN**) = Democratic primary ballots ÷ all primary ballots × 100, from the SBOE official primary canvass (2022 General Primary, June 28, 2022; 2026 General Primary, March 17, 2026). *{ST}.*
- **S** (surplus) = Dem share − D, in percentage points

Illinois has no party registration, so D is a stand-in, never official registration. Illinois uses total ballots cast as the denominator.

## Illinois's equation in final form

### Surplus Equation (Illinois statewide constant)

**Surplus Equation: S = {LA['multiplier']} × (D/100) + {LA['offset']}**

Where:
- S = Surplus, expressed in percentage points: the county's Democratic share of ballots cast minus D (2022, SBOE official canvass)
- D = Democratic registration-share **STAND-IN**, as a percent (0–100 scale): Democratic primary ballots ÷ all primary ballots × 100 (2022 General Primary). This is **not** party registration and not a headcount of registered Democrats.
- {LA['multiplier']} = Multiplier coefficient
- {LA['offset']} = Constant offset, in percentage points

Illinois's multiplier and offset come from an ordinary least-squares fit of S on D/100 across **all {LA['n']} counties**, 2022 official SBOE data: **R² = {LA['r_squared']}**, **mean absolute residual {LA['mean_abs_residual_pp']} points**, largest residual {LA['max_residual_county']} ({LA['max_residual_pp']}). It was verified in two independent passes. 2022 is the locked year because it is the only year with official results for all 102 counties.

### County-level surplus

**S = Dem share − D**, and the county's **residual = S − [{LA['multiplier']} × (D/100) + {LA['offset']}]**

Cook County plugged in (2022):

**S = {CKSH} − {cs['D_2022_pct']} = {cs['S_2022_pp']}**; fitted = {cs['fitted_2022']}; residual = **{cs['residual_2022']}** points.

### Secondary fit (not the locked equation)

Same surplus form, S = m × (D/100) + b. 2026 is {UN} and covers only the {LB['n']} counties with a county-authority ballots-cast figure. No gaps were filled.

| Fit | n | Multiplier | Offset | R² | Mean abs residual (pp) | Largest residual |
|---|---|---|---|---|---|---|
| **Locked: 2022 official** | {LA['n']} | {LA['multiplier']} | {LA['offset']} | {LA['r_squared']} | {LA['mean_abs_residual_pp']} | {LA['max_residual_county']} ({LA['max_residual_pp']}) |
| 2026 surplus, {UN} | {LB['n']} | {LB['multiplier']} | {LB['offset']} | {LB['r_squared']} | {LB['mean_abs_residual_pp']} | {LB['max_residual_county']} ({LB['max_residual_pp']}) |

![Illinois Surplus Equation: locked 2022 fit and secondary 2026 UNOFFICIAL fit](https://raw.githubusercontent.com/mbenson8989/Illinois-Election-Analysis/main/charts/il_surplus_equation_locked_UNOFFICIAL2026.png)

Every county's S, D, fitted value and residual (both years) is in [`out/surplus_pass_a.csv`]({REPO}/blob/main/out/surplus_pass_a.csv).

## Blank template

| Line | Item | 2022 | 2026* |
|---|---|---|---|
| 1 | Democratic governor votes | ______ | ______ |
| 2 | Total ballots cast | ______ | ______ |
| 3 | Dem share = line 1 ÷ line 2 × 100 | ______ | ______ |
| 4 | Democratic primary ballots (stand-in; SBOE primary canvass) | ______ | ______ |
| 5 | All primary ballots (SBOE primary canvass) | ______ | ______ |
| 6 | D = line 4 ÷ line 5 × 100 (stand-in, NOT registration) | ______ | ______ |
| 7 | S = line 3 − line 6 | ______ | ______ |
| 8 | D ÷ 100 | ______ | ______ |
| 9 | Multiplier × line 8 | ______ | ______ |
| 10 | Expected S = line 9 + offset | ______ | ______ |
| 11 | Residual = line 7 − line 10 | ______ | ______ |
| 12 | Residual in votes = line 11 ÷ 100 × line 2 | ______ | ______ |

## Rules for using this formula

1. **Use the locked multiplier and offset above for every Illinois county.** Do not refit per county.
2. **The starting point is different in every state. Don't assume Nebraska's numbers carry over.** Illinois's D is primary-ballot share, not registration. Its 2022→2026 statewide jump (51.88% → 67.87%) reflects which primaries were contested. Compare Illinois counties only against Illinois's own range.
3. **Always pull out the floor and ceiling counties.** See [Floor and Ceiling Counties](Floor-and-Ceiling).

## Worked example: Cook

| Line | Item | 2022 | 2026* |
|---|---|---|---|
| 1 | Democratic governor votes | {int(G22['COOK']['dem_votes']):,} | {int(fit[0]['dem_votes_2026_UNOFFICIAL']):,}* |
| 2 | Total ballots cast | {int(G22['COOK']['ballots_cast']):,} | {int(fit[0]['ballots_cast_2026_UNOFFICIAL']):,}* |
| 4 | Democratic primary ballots (stand-in) | {int(PX['COOK']['gp2022_dem_ballots']):,} | {int(PX['COOK']['gp2026_dem_ballots']):,} |
| 5 | All primary ballots | {int(PX['COOK']['gp2022_total_ballots']):,} | {int(PX['COOK']['gp2026_total_ballots']):,} |
| 6 | D (stand-in) | {cs['D_2022_pct']} | {cs['D_2026_pct_UNOFFICIAL']} |
| 7 | S | {cs['S_2022_pp']} | {cs['S_2026_pp_UNOFFICIAL']}* |
| 10 | Expected S (locked line for 2022; 2026 line for 2026*) | {cs['fitted_2022']} | {cs['fitted_2026']}* |
| 11 | Residual | {cs['residual_2022']} | {cs['residual_2026']}* |

Cook 2026\\* = Chicago Board of Election Commissioners + Cook County Clerk (suburban Cook).

{EVAL}
## Verification

Every computed cell was produced by two independent passes (Pass A: exact fractions; Pass B: pandas/numpy). Each pass read the raw files separately, and the cells were compared to the decimal.

{VERL}
{REL('Locked-Illinois-Formula')}"""
assert fit[0]['county_key']=='COOK'
# ---------------- Floor and Ceiling
srt=sorted(NT.values(),key=lambda r:-float(r['dG']))
def dgrow(r):
    p=PX[r['county_key']]; t=[x for x in T if x['county_key']==r['county_key']][0]
    return f"| {r['county']} | {P(r['G_2022_2dp'])} | {P(r['G_2026_2dp'])} | {P(r['dG_2dp'])} | {r['R_2026_2dp']}% | {int(p['gp2022_dem_ballots']):,} → {int(p['gp2026_dem_ballots']):,} | {int(G22[r['county_key']]['dem_votes']):,} → {int(t['dem_votes_2026_UNOFFICIAL']):,} |"
FC=f"""# Floor and Ceiling Counties

{DISC}
## How to read floor and ceiling counties

Look for the pattern at both ends. The ceiling counties have the highest ΔG; the floor counties have the lowest. These are the 80 counties with 2026\\* data.

- **The floor** is the single county with the lowest ΔG in the state. In Illinois that's {NE['dG_floor'][0][0]}, at {NE['dG_floor'][0][1]}\\*.
- **The ceiling** is the single county with the highest ΔG in the state. In Illinois that's {NE['dG_ceiling'][0][0]}, at {P(NE['dG_ceiling'][0][1])}\\*.

Every state will have its own floor and ceiling. Those two extremes set the range the rest of that state's counties fall within. ΔG is positive in {NE['n_dG_positive']} of 80 Illinois counties, because the stand-in (R) rose in most counties.

## Terminology

- **Ceiling counties** have the highest ΔG: """+', '.join(f"{c} {P(v)}\\*" for c,v in NE['dG_ceiling'])+f""". Gallatin's ΔG is driven by its stand-in collapsing from 44.69% to 21.56%; its 2022 Democratic primary ran unusually high for the county.
- **Floor** counties have the lowest ΔG: """+', '.join(f"{c} {v}\\*" for c,v in NE['dG_floor'])+f""".
- **Non-loss counties** (also called **share-gain counties**) had no stand-in Democratic headcount loss. They get raw numbers only, with no residual step. That is {80-NE['n_loss']} of 80 counties; the exceptions are {', '.join(NE['loss_counties'])}.
- **Baseline floor and ceiling** (original Illinois spec): the lowest and highest Democratic share of ballots cast. See below.

## Ceiling and floor detail

| County | G 2022 | G 2026* | ΔG* | Stand-in share 2026 | Dem primary ballots 2022 → 2026 | Dem gov votes 2022 → 2026* |
|---|---|---|---|---|---|---|
"""+'\n'.join(dgrow(r) for r in srt[:5])+"\n| … | | | | | | |\n"+'\n'.join(dgrow(r) for r in srt[-5:][::-1])+f"""

## Baseline floor and ceiling (Democratic share of ballots cast)

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
{REL('Floor-and-Ceiling')}"""
# ---------------- Reverse Math
RMn=f"""# Bottom-Up Reverse Math

{DISC}
The same arithmetic at three levels: one county, then every county with 2026\\* data, then the excluded counties and the sources. Denominator: total ballots cast. Tables are sorted by 2020 population, largest to smallest.

## Step 1: Cook County

| Step | Value |
|---|---|
| Democratic vote share | {ck['S_2022_2dp']}% (2022) → {ck['S_2026_2dp']}%* (2026): **{P(ck['vsg_2dp'])} points*** |
| Stand-in share (Dem primary ballot share; NOT registration) | {ck['R_2022_2dp']}% → {ck['R_2026_2dp']}%: **{P(ck['dR_2dp'])} points** |
| ΔG = vote-share growth − stand-in share change | {ck['vsg_2dp']} − ({P(ck['dR_2dp'])}) = **{P(ck['dG_2dp'])} points*** |
| Reverse step | Not applied: Cook's Democratic primary ballots rose ({int(PX['COOK']['gp2022_dem_ballots']):,} → {int(PX['COOK']['gp2026_dem_ballots']):,}), so it is a non-loss county |
| Gap in votes | {int(fit[0]['dem_votes_2026_UNOFFICIAL']):,}* − {int(G22['COOK']['dem_votes']):,} × ({int(PX['COOK']['gp2026_dem_ballots']):,} ÷ {int(PX['COOK']['gp2022_dem_ballots']):,}) = **about {int(ck['gap_in_votes_0dp']):+,}*** |
| Change-vs-drop residual × 2026 ballots (implied extra votes) | **{float(fit[0]['implied_extra_votes']):+,.2f}*** |

## Step 2: all {len(fit)} counties with 2026\\* data (and 2022 for all 102)

**Definitions**
- **Dem share** = Pritzker votes ÷ ballots cast (county total ballots, not the governor-contest total).
- **Stand-in share** = Democratic primary ballots ÷ all primary ballots (SBOE primary canvass). *{ST}.*
- **Gap** = Dem share − stand-in share (same year). In the Nebraska-format pages this is G, in points.
- **Stand-in drop** = stand-in 2022 − stand-in 2026 (negative = the stand-in rose).
- **Share change** = Dem share 2026 − Dem share 2022. **Delta-G** = share change − stand-in change = gap 2026 − gap 2022.
- **Expected change** = {S['constant']} + ({S['multiplier']}) × stand-in drop (the original change-vs-drop fit; see [Locked Illinois Formula](Locked-Illinois-Formula)).
- **Residual** = share change − expected change. **Implied extra votes** = residual × 2026 ballots cast.

### County table — 2026 columns {UN}
| County | Pop 2020 | Stand-in 2022 | Stand-in 2026 | Stand-in drop | Dem share 2022 | Gap 2022 | Ballots 2026 {UN} | Dem share 2026 {UN} | Gap 2026 | Share change | Delta-G | Expected | Residual | Implied extra votes | 2026 source ({UN}) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{rows}

Full precision, URLs and as-of times: [`out/il_governor_reverse_math_2022_2026_VERIFIED.csv`]({REPO}/blob/main/out/il_governor_reverse_math_2022_2026_VERIFIED.csv). Nebraska-template lines (S, R, G, ΔG, surplus, gap in votes) for each county: [`out/ne_format_pass_a.csv`]({REPO}/blob/main/out/ne_format_pass_a.csv).

## Step 3: excluded counties and 2026 sources

### 2026 counties excluded ({len(exc)}): no county-authority ballots-cast figure in hand
No aggregator ballots-cast figures were substituted. These counties have 2022 values only.

| County | Pop 2020 | Reason |
|---|---|---|
{excl}

### 2026 source disagreements ({UN})
Where a voteclock.org transcription of a county page and the county's own vendor feed both existed, the county feed (later timestamp) was used:

| County | voteclock D / R / ballots (as of) | Used: county feed D / R / ballots |
|---|---|---|
{dis_vc}

civicAPI aggregator cross-check (race 87130, last updated {X['civicapi_last_updated_utc']} UTC = 5:30 p.m. CST Nov 19, 2026; {X['civicapi_percent_reporting']}% reporting): {X['exact_D_R_match']} of {X['counties_compared']} counties match exactly on D and R; {X['differ']} differ. Largest differences (used − civicAPI):

| County | Used D / R | civicAPI D / R | Difference D / R |
|---|---|---|---|
{dis_cv}

Most differences are timing. Several county snapshots were taken election night (e.g. Will as of Nov 3, 9:41 p.m.), and mail ballots keep being counted up to the Dec 4 canvass. Full list: `out/il_2026_civicapi_crosscheck_UNOFFICIAL.csv`.

{EVAL}
> **Hypothesis label.** Turning ΔG or a residual into "implied extra votes" and calling them injected or offset votes is a hypothesis the arithmetic cannot test. The same number reflects turnout changes, crossover voting, which primaries were contested (which moves the stand-in), and any other cause. Candidate votes are not turnout.
{REL('Reverse-Math')}"""
# ---------------- Graphs (numbered, italic captions)
CAP={'il_fit_share_change_vs_standin_drop_UNOFFICIAL.png':'Each dot is one county (n = 80). Line: the original change-vs-drop fit. Vertical distance from the line = residual.',
 'il_implied_extra_votes_UNOFFICIAL.png':'Residual × 2026 ballots cast, by county (symlog scale). Hypothesis label applies (see Bottom-Up Reverse Math).',
 'il_dem_share_2022_vs_2026_UNOFFICIAL.png':'Each dot is one county; dashed line = no change. Floor and ceiling counties labeled.',
 'il_gap_standin_vs_dem_share_UNOFFICIAL.png':'Vertical distance from the dashed line = G (the surplus S on the locked equation), 2022 in blue, 2026\\* in red.',
 'il_share_form_fits_UNOFFICIAL.png':f'Panel A is the locked Surplus Equation (2022, n = 102): S = {A["m"]} × (D/100) + {A["b"]}. Panels B and C are secondary 2026\\* fits.'}
GRn=f"# Graphs\n\n{DISC}\n"+'\n'.join(f"## {i}. {t}\n\n![{t} — 2026 {UN}]({RAW}charts/{f})\n\n*{CAP[f]} 2026 = {UN}. {ST}.*\n" for i,(f,t) in enumerate([CH[4],CH[3],CH[0],CH[2],CH[1]],1))+REL('Graphs')
# ---------------- Home
Hn=f"""# Illinois 2022 vs 2026 Governor Race: ΔG Method

**Version 2, built {RUN}**

{DISC}
Method: Morissa Benson's ΔG reverse-factoring method, as built out on the [Nebraska wiki](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki). Data: Illinois State Board of Elections (SBOE) official 2022 general and 2022/2026 primary canvasses; 2026\\* county election-authority results ({UN}).

**PDF report:** [{PDF.split('/')[-1]}]({PDF})

## Contents

Illinois has no party registration, so every page uses a labeled stand-in: Democratic primary ballot share. The pages build from one county up to the statewide formula.

1. [Cedar County Audit (Nebraska)]({CEDAR}): where the method began
2. [Bottom-Up Reverse Math](Reverse-Math): Cook → all counties with 2026\\* data → excluded counties and sources
3. [Locked Illinois Formula](Locked-Illinois-Formula): the Surplus Equation, with a blank fill-in template
4. [Floor and Ceiling Counties](Floor-and-Ceiling): the counties at the top and bottom of ΔG, plus the baseline floor/ceiling and the over-ballot check
5. [Graphs](Graphs): share-form fits, stand-in vs Dem share, change-vs-drop fit, 2022 vs 2026, implied extra votes

## Statewide at a glance

| Item | Result |
|---|---|
| Registration stand-in | Democratic primary ballot share (SBOE official primary canvass): **stand-in, NOT official party registration** |
| **Surplus Equation (locked)** | **S = {A['m']} × (D/100) + {A['b']}** (2022 official, n = {A['n']}, R² = {A['r_squared']}) |
| Original change-vs-drop fit | {EQ} |
| ΔG ceiling / floor, 2026\\* | {NE['dG_ceiling'][0][0]} {P(NE['dG_ceiling'][0][1])}\\* / {NE['dG_floor'][0][0]} {NE['dG_floor'][0][1]}\\* |
| Baseline floor / ceiling 2022 (Dem share of ballots) | {S['floor_2022'][0]} {pct(S['floor_2022'][1])} / {S['ceiling_2022'][0]} {pct(S['ceiling_2022'][1])} |
| Baseline floor / ceiling 2026\\* | {S['floor_2026_UNOFFICIAL'][0]} {pct(S['floor_2026_UNOFFICIAL'][1])} / {S['ceiling_2026_UNOFFICIAL'][0]} {pct(S['ceiling_2026_UNOFFICIAL'][1])} |
| Over-ballot flags (D+R > ballots cast) | 2022: {len(S['over_ballot_2022'])} of 102 · 2026\\*: {len(S['over_ballot_2026'])} of {S['n_fit']} |
| Total implied extra votes (Σ residual × 2026 ballots)\\* | {float(S['total_implied_extra_votes']):,.2f} (positive {float(S['sum_positive_implied']):,.2f}; negative {float(S['sum_negative_implied']):,.2f}) |
| 2026 county coverage | {len(fit)} of 102 counties with a county-authority ballots-cast figure; {len(exc)} excluded (listed on [Bottom-Up Reverse Math](Reverse-Math)) |

## Double verification (two independent passes; every cell to the decimal)
{VERN}
Two mismatches were caught and fixed before any publication:
- **Stephenson, 2026 Dem share:** 6,199 / 16,000 = 0.3874375 exactly. Pass B's float rounding gave 0.387437; it now uses exact half-even rounding.
- **Kendall, 2026 G:** Pass A printed −0.00 where Pass B printed 0.00. Pass A now drops the sign on a rounded zero.

## Sources
- 2022: SBOE official canvass, the `2022GECty` vote file and `2022GEOfficialVote.pdf`.
- Stand-in: SBOE official primary canvass PDFs, 2022 GP and 2026 GP.
- 2026 ({UN}): not yet posted by SBOE; the state canvass is Fri Dec 4, 2026. County results come from the election authorities:
  - direct feeds and PDFs (the Chicago Board of Election Commissioners summary PDF, and county clerks' pollresults, gbsvote, Platinum, Clarity, LiveVoterTurnout, ES&S, EL45 and canvass results; Jefferson's scanned official summary was read by OCR in Pass A and by an independent visual transcription in Pass B);
  - where noted, voteclock.org transcriptions of the authority's posted results;
  - three local-radio reprints of the clerk's unofficial report (Fayette, Gallatin, Hamilton).

  Each county's source is recorded in `raw/sources.json` and in the source column of the county tables. civicAPI (race 87130) was used **only** as a cross-check.
- Population (sort order): 2020 Census PL 94-171.
{REL('Home')}"""
SBn=f"""**Illinois Election Analysis**

**[README: Start Here](README)** · **[All States — Election Analysis Index](https://github.com/mbenson8989/Election-Integrity-Research/wiki/All-States-Election-Analysis-Index)**

1. [Home](Home)
2. [Cedar County Audit (Nebraska)]({CEDAR})
3. [Floor and Ceiling Counties](Floor-and-Ceiling)
4. [Bottom-Up Reverse Math](Reverse-Math)
5. [Graphs](Graphs)
6. [PDF report]({PDF})
7. [Locked Illinois Formula](Locked-Illinois-Formula)

\\*2026 = {UN}

{ST}
"""
# ---------------- README (plain language; t6u)
PDFRAW='https://raw.githubusercontent.com/mbenson8989/Illinois-Election-Analysis/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf'
EXC=sorted(EXCLUDED_NOTE) if 'EXCLUDED_NOTE' in dir() else []
RMD=f"""# README: Start Here

Welcome. If you've never seen this analysis before, this page is for you. It explains what you're looking at, where the numbers come from, and how to read them.

> **\\*2026 figures are marked with an asterisk.** They are unofficial. The Illinois State Board of Elections certifies the 2026 results at its canvass on Dec 4, 2026, so these numbers may still change.

## Where the numbers come from

The 2022 numbers come directly from the **[Illinois State Board of Elections](https://www.elections.il.gov/)** (SBOE), from its official website. Nothing is estimated or made up. The sources are:

- **2022 governor results:** the SBOE's official 2022 general election canvass, for all 102 counties.
- **The Democratic "registration" stand-in:** the SBOE's official primary canvasses (June 28, 2022 and March 17, 2026).
- **2026 governor results (unofficial\\*):** the SBOE hasn't posted these yet. Until it does, they come from each county's own election office (the county clerk or election commission), as posted on its official results page. We found usable results for {LB['n']} of 102 counties; the other {102-LB['n']} are left out rather than guessed. Every county's source link is listed on [Bottom-Up Reverse Math](Reverse-Math).

**One important difference from other states:** Illinois voters don't register by party. So there is no official count of registered Democrats. Instead we use the next best official number: the share of primary voters who chose a Democratic ballot. Every page calls this a **stand-in**. It is not party registration.

## See the data for yourself

You don't have to take our word for it. Open the **PDF report** in the sidebar, or go straight to the **[Illinois PDF report]({PDFRAW})**. It lists every county with its numbers for 2022 and 2026\\*. You can check any line against the State Board's own files.

## This is a hypothesis, not a verdict

Please read this part carefully. **What you'll find here is a hypothesis, not settled fact.**

If election manipulation exists, it would not be one simple thing. It would be multifaceted, with several methods working together. This analysis looks through one lens only: how votes line up with each county's Democratic baseline. A gap between the two is a pattern worth checking. It is not proof of anything by itself, and it says nothing about who did what or why. In Illinois the lens is blurrier than usual, because the baseline is a stand-in rather than real registration.

## The story behind the numbers

Numbers make more sense with the story behind them. Morissa tells that story in her hypothesis write-up on Substack: **[The Election Equation. And Plan.](https://moebenson.substack.com/p/the-election-equation-and-plan)** You can find more of her writing on **[Morissa Benson's Substack](https://moebenson.substack.com/)**.

## What you're looking at, in plain terms

**The basic idea.** In each county, we compare two things:

1. What share of the ballots cast went to the Democratic candidate for governor.
2. What share of primary voters chose a Democratic ballot (the stand-in).

The difference between those two is the **surplus** (we call it S). A county where the Democratic candidate did better than the stand-in has a positive surplus; one where he did worse has a negative surplus.

**Why it's called reverse-factoring.** We work backward from the result. We start with the votes that were counted. Then we take out what the county's Democratic baseline would explain. What's left over is the **residual**: the part the baseline doesn't account for.

**A real example: Cook County, 2022.**

- Pritzker got {int(G22['COOK']['dem_votes']):,} of {int(G22['COOK']['ballots_cast']):,} ballots cast, a **{CKSH}%** share.
- {int(PX['COOK']['gp2022_dem_ballots']):,} of {int(PX['COOK']['gp2022_total_ballots']):,} primary voters chose a Democratic ballot: **{cs['D_2022_pct']}%**.
- So Cook's surplus is {CKSH} − {cs['D_2022_pct']} = **{cs['S_2022_pp']} points**. The statewide line below expected {cs['fitted_2022']}, so Cook's residual is **{cs['residual_2022']}** points.

## How Morissa worked it out

Morissa isn't a mathematician. She sees patterns. Here is what she did:

1. She lined up the official numbers county by county.
2. She graphed all the counties together and drew the line that fit them best.
3. That line gives each state its own fitted numbers: a multiplier and an offset. No two states share them.

For Illinois, using all 102 counties' official 2022 results, the line is the **Surplus Equation**:

**S = {LA['multiplier']} × (D/100) + {LA['offset']}**

Here S is the surplus in percentage points, and D is the Democratic primary-ballot share (the stand-in) as a percent. The line explains only part of the county-to-county differences (R² = {LA['r_squared']}); the average county sits {LA['mean_abs_residual_pp']} points from it. The details are on the **[Locked Illinois Formula](Locked-Illinois-Formula)** page.

She used AI to speed up the work, but not to decide anything. Every number was computed twice, by two separate programs reading the raw files, and the two had to match to the last decimal before anything was published.

## Where to go next

- [Home](Home): the overview
- [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit): where it started (Nebraska)
- [Floor and Ceiling Counties](Floor-and-Ceiling): the counties at each end
- [Bottom-Up Reverse Math](Reverse-Math): the step-by-step math
- [Graphs](Graphs): the charts
- [PDF report]({PDFRAW}): the data
- [Locked Illinois Formula](Locked-Illinois-Formula): the equation and a fill-in-the-blank template
"""

pages={'README.md':RMD,'Home.md':Hn,'Reverse-Math.md':RMn,'Locked-Illinois-Formula.md':L,'Floor-and-Ceiling.md':FC,'Graphs.md':GRn,'_Sidebar.md':SBn}
for k,v in pages.items(): open(I+'wiki/'+k,'w').write(v)
RD=f"""# Illinois-Election-Analysis
Reverse-factoring (ΔG method) analysis of the Illinois governor races, 2022 (SBOE official) and 2026 (**{UN}**), for all 102 counties. Wiki pages follow the Nebraska wiki format.

**{ST}.**

- Wiki: {REPO}/wiki (a copy of the pages is also in [`/wiki`](wiki))
- PDF report: [report/{PDF.split('/')[-1]}](report/{PDF.split('/')[-1]})
- Cross-link: [Cedar Audit (Nebraska)]({CEDAR})

## Result
**Surplus Equation (locked): S = {A['m']} × (D/100) + {A['b']}**. This is the 2022 official fit across n = {A['n']} counties, R² = {A['r_squared']}; S = Dem share of ballots cast − D, in points; D = stand-in share in percent. Original change-vs-drop fit: {EQ}. Baseline floor 2022: {S['floor_2022'][0]} ({pct(S['floor_2022'][1])}); ceiling 2022: {S['ceiling_2022'][0]} ({pct(S['ceiling_2022'][1])}). ΔG ceiling/floor 2026*: {NE['dG_ceiling'][0][0]} / {NE['dG_floor'][0][0]}. Over-ballot flags: 2022 {len(S['over_ballot_2022'])}, 2026 {len(S['over_ballot_2026'])}.

## Layout
- `raw/sources.json`: the raw source list. It has every source URL and fetch time, plus the as-of time for each 2026 county. Bulky raw downloads (~90 MB) are not committed; re-fetch them from the listed URLs into `raw/` to re-run the scripts.
- `scripts/`: the independent passes, `pass_a*.py` / `compute_a.py` / `share_a.py` / `ne_a.py` (stdlib, exact fractions) and `pass_b*.py` / `compute_b.py` / `share_b.py` / `ne_b.py` (pandas/BeautifulSoup/pdfplumber, float64), plus the `verify*.py` cell-by-cell comparisons.
- `out/`: verified tables, the pass outputs, the `verification*.json` files, and the 2026 cross-check and disagreements.
- `charts/`, `report/`, `wiki/`.

## Verification
{VERN}
Built {RUN}.
"""
open(I+'README.md','w').write(RD)
print('ok')
