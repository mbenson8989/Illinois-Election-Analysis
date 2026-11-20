"""2026 UNOFFICIAL source notes: per-county source list + disagreements (voteclock snapshot vs direct county feed; civicAPI aggregator vs county authority)."""
import csv, json, re, glob, sys
sys.path.insert(0,'/workspace/illinois/scripts')
from pass_a_2026 import p_voteclock
I='/workspace/illinois/'
norm=lambda s:re.sub('[^A-Z]','',s.upper())
comp=list(csv.DictReader(open(I+'out/pass_a_2026_components.csv')))
tot={r['county_key']:r for r in csv.DictReader(open(I+'out/pass_a_2026_raw.csv'))}
civ=json.load(open(I+'raw/2026/civic_race_87130.json'))
dis=[]
# voteclock vs direct feed (overlaps where the direct vendor feed was used)
for k,slug in [('BOONE','boone'),('DEKALB','dekalb'),('MACON','macon'),('OGLE','ogle'),('TAZEWELL','tazewell'),('WHITESIDE','whiteside')]:
    d,r,b,asof=p_voteclock(I+f'raw/2026/voteclock/{slug}-county-il-election-authority-2026.html')
    t=tot[k]; used=(int(t['dem_votes']),int(t['rep_votes']),int(t['ballots_cast']))
    if (d,r,b)!=used: dis.append(dict(county=k,kind='voteclock snapshot vs county vendor feed (used)',voteclock=[d,r,b],used=list(used),voteclock_as_of=asof,
        diff_D=used[0]-d,diff_R=used[1]-r,diff_ballots=used[2]-b))
cv=[]
for key,reg in civ['region_results'].items():
    k=norm(reg['name'])
    if k not in tot: continue
    D=sum(c['votes'] for c in reg['candidates'] if 'Pritzker' in c['name']); R=sum(c['votes'] for c in reg['candidates'] if 'Bailey' in c['name'])
    t=tot[k]; row=dict(county=k,civicapi_D=D,civicapi_R=R,used_D=int(t['dem_votes']),used_R=int(t['rep_votes']),civicapi_pct_reporting=reg.get('percent_reporting'))
    row['diff_D']=row['used_D']-D; row['diff_R']=row['used_R']-R
    cv.append(row)
with open(I+'out/il_2026_civicapi_crosscheck_UNOFFICIAL.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(cv[0])); w.writeheader(); w.writerows(cv)
summ=dict(civicapi_race='https://civicapi.org/api/v2/race/87130',civicapi_last_updated_utc=civ['last_updated'],civicapi_percent_reporting=civ['percent_reporting'],
  counties_compared=len(cv),exact_D_R_match=sum(1 for r in cv if r['diff_D']==0 and r['diff_R']==0),
  differ=sum(1 for r in cv if r['diff_D'] or r['diff_R']),max_abs_diff_D=max(abs(r['diff_D']) for r in cv),max_abs_diff_R=max(abs(r['diff_R']) for r in cv),
  largest=sorted(cv,key=lambda r:-(abs(r['diff_D'])+abs(r['diff_R'])))[:8],voteclock_vs_feed=dis)
json.dump(summ,open(I+'out/il_2026_disagreements_UNOFFICIAL.json','w'),indent=1)
print(json.dumps({k:v for k,v in summ.items()},indent=0)[:4000])
