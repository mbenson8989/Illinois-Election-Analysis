"""Builds published CSVs (coverage, sources), updates raw/sources.json with 2026 entries, and draws charts. 2026 = UNOFFICIAL (pre-Dec 4, 2026 canvass)."""
import csv, json, os, sys, datetime, re
sys.path.insert(0,'/workspace/illinois/scripts')
from manifest_2026 import M, EXCLUDED_NOTE
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
I='/workspace/illinois/'; O=I+'out/'
UNOFF='UNOFFICIAL (pre-Dec 4, 2026 canvass)'
STAND='Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration'
T=list(csv.DictReader(open(O+'compute_pass_a.csv')))
comp=list(csv.DictReader(open(O+'pass_a_2026_components.csv')))
src={}
for c in comp: src.setdefault(c['county_key'],[]).append(c)
# published master table = verified pass A table + 2026 source columns
cols=list(T[0])+['source_2026_UNOFFICIAL','source_url_2026','as_of_2026','status_2026']
pub=[]
for r in T:
    k=r['county_key']; s=src.get(k,[])
    st='included (UNOFFICIAL)' if s else 'excluded: '+EXCLUDED_NOTE.get(k,'no posted 2026 governor results located on the county election authority website or its results vendors (pollresults, gbsvote, Platinum, Clarity, LiveVoterTurnout) as of Nov 22, 2026')
    pub.append({**r,'source_2026_UNOFFICIAL':' + '.join(f"{x['authority']} ({x['source_type']})" for x in s),'source_url_2026':' ; '.join(x['url'] for x in s),
                'as_of_2026':' ; '.join(x['as_of'] for x in s),'status_2026':st})
with open(O+'il_governor_reverse_math_2022_2026_VERIFIED.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(pub)
# sources.json: append 2026 component entries (idempotent)
sj=json.load(open(I+'raw/sources.json')); sj=[e for e in sj if e.get('dataset')!='2026GE_county_UNOFFICIAL']
for x in comp:
    files=[f for a,t,f,u in M[x['county_key']] if u==x['url']]
    fl=files[0] if files else None
    fl=fl if isinstance(fl,str) else (fl[0] if fl else None)
    fetched=datetime.datetime.fromtimestamp(os.path.getmtime(fl)).astimezone().isoformat(timespec='seconds') if fl and os.path.exists(fl) else None
    sj.append(dict(dataset='2026GE_county_UNOFFICIAL',label=UNOFF,county=x['county_key'],authority=x['authority'],source_type=x['source_type'],url=x['url'],
        file=os.path.relpath(fl,I) if fl else None,fetched=fetched,as_of=x['as_of'],dem=int(x['dem']),rep=int(x['rep']),ballots=int(x['ballots'])))
sj=[e for e in sj if e.get('dataset')!='2026GE_crosscheck']
sj.append(dict(dataset='2026GE_crosscheck',label=UNOFF,note='civicAPI aggregator used ONLY as a cross-check of D/R votes (no ballots-cast field; never used in computations)',
    url='https://civicapi.org/api/v2/race/87130',file='raw/2026/civic_race_87130.json',disagreements_file='out/il_2026_disagreements_UNOFFICIAL.json'))
json.dump(sj,open(I+'raw/sources.json','w'),indent=1)
# charts
os.makedirs(I+'charts',exist_ok=True)
fit=[r for r in T if r['ballots_cast_2026_UNOFFICIAL']]
S=json.load(open(O+'compute_pass_a_summary.json')); c=float(S['constant']); m=float(S['multiplier'])
x=[float(r['standin_drop_2022_to_2026']) for r in fit]; y=[float(r['share_change_2022_to_2026']) for r in fit]
fig,ax=plt.subplots(figsize=(10,6.5)); ax.scatter(x,y,s=[max(12,int(r['pop_2020'])**0.5/6) for r in fit],alpha=.6,color='#4874a3')
xs=[min(x),max(x)]; ax.plot(xs,[c+m*v for v in xs],color='#c6606b',lw=2,label=f"share change = {S['constant']} + ({S['multiplier']}) x stand-in drop   R² = {S['r_squared']}, n = {S['n_fit']}")
for r in fit:
    if int(r['pop_2020'])>250000 or abs(float(r['residual']))>0.04: ax.annotate(r['county'],(float(r['standin_drop_2022_to_2026']),float(r['share_change_2022_to_2026'])),fontsize=7)
ax.axhline(0,color='grey',lw=.5); ax.axvline(0,color='grey',lw=.5); ax.legend(fontsize=8,loc='lower left')
ax.set_xlabel('Stand-in drop (2022 GP Dem ballot share − 2026 GP Dem ballot share)'); ax.set_ylabel('Dem share of ballots cast: 2026 − 2022')
ax.set_title(f'Illinois governor: share change vs registration stand-in drop — 2026 {UNOFF}',fontsize=10)
fig.text(.01,.01,STAND,fontsize=7); fig.tight_layout(rect=(0,.03,1,1)); fig.savefig(I+'charts/il_fit_share_change_vs_standin_drop_UNOFFICIAL.png',dpi=130); plt.close(fig)
# implied extra votes
fs=sorted(fit,key=lambda r:float(r['implied_extra_votes']))
fig,ax=plt.subplots(figsize=(10,11)); v=[float(r['implied_extra_votes']) for r in fs]
ax.barh([r['county'] for r in fs],v,color=['#4874a3' if a>0 else '#c6606b' for a in v]); ax.tick_params(axis='y',labelsize=6); ax.set_xscale('symlog',linthresh=100)
ax.set_xlabel('Implied extra votes = residual × 2026 ballots cast (symlog scale)'); ax.set_title(f'Implied extra votes by county (n={len(fit)}) — 2026 {UNOFF}',fontsize=10)
fig.text(.01,.005,STAND,fontsize=7); fig.tight_layout(rect=(0,.02,1,1)); fig.savefig(I+'charts/il_implied_extra_votes_UNOFFICIAL.png',dpi=130); plt.close(fig)
# Dem share 2022 vs 2026
fig,ax=plt.subplots(figsize=(9,6.5)); a=[float(r['dem_share_ballots_2022']) for r in fit]; b=[float(r['dem_share_ballots_2026_UNOFFICIAL']) for r in fit]
ax.scatter(a,b,color='#4874a3',alpha=.7); ax.plot([0,1],[0,1],color='grey',lw=.8,ls='--')
for r,p,q in zip(fit,a,b):
    if r['county'] in (S['floor_2022'][0],S['ceiling_2022'][0],S['floor_2026_UNOFFICIAL'][0],S['ceiling_2026_UNOFFICIAL'][0]): ax.annotate(r['county'],(p,q),fontsize=8)
ax.set_xlabel('Dem share of ballots cast, 2022 (SBOE official)'); ax.set_ylabel(f'Dem share of ballots cast, 2026 {UNOFF}')
ax.set_title(f'Dem share of ballots cast 2022 vs 2026 — 2026 {UNOFF}',fontsize=10); fig.text(.01,.01,STAND,fontsize=7); fig.tight_layout(rect=(0,.03,1,1))
fig.savefig(I+'charts/il_dem_share_2022_vs_2026_UNOFFICIAL.png',dpi=130); plt.close(fig)
# gap 2022 vs stand-in
fig,ax=plt.subplots(figsize=(9,6.5)); ax.scatter([float(r['standin_dem_primary_share_2022']) for r in T],[float(r['dem_share_ballots_2022']) for r in T],color='#4874a3',alpha=.6,label='2022 (all 102 counties)')
ax.scatter([float(r['standin_dem_primary_share_2026']) for r in fit],[float(r['dem_share_ballots_2026_UNOFFICIAL']) for r in fit],color='#c6606b',alpha=.6,label=f'2026 {UNOFF} (n={len(fit)})')
ax.plot([0,1],[0,1],color='grey',lw=.8,ls='--'); ax.legend(fontsize=8)
ax.set_xlabel('Registration stand-in: Dem primary ballot share'); ax.set_ylabel('Dem share of general-election ballots cast')
ax.set_title(f'Gap = Dem GE share − stand-in (distance from dashed line) — 2026 {UNOFF}',fontsize=10); fig.text(.01,.01,STAND,fontsize=7); fig.tight_layout(rect=(0,.03,1,1))
fig.savefig(I+'charts/il_gap_standin_vs_dem_share_UNOFFICIAL.png',dpi=130); plt.close(fig)
print(len(pub),len(fit),len(sj))
