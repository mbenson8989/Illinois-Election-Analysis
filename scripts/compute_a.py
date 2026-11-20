"""COMPUTE PASS A (stdlib, exact rational arithmetic via fractions.Fraction; Decimal ROUND_HALF_EVEN output).
Inputs: out/pass_a_2022.csv, out/pass_a_2026_raw.csv, out/proxy_primary_pass_a.csv (Pass A stand-in parse), census CSV.
2026 = UNOFFICIAL (pre-Dec 4, 2026 canvass). Registration stand-in: Democratic primary ballot share - NOT official party registration."""
import csv, json
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
getcontext().prec=60
O='/workspace/illinois/out/'; R='/workspace/illinois/raw/'
norm=lambda s:''.join(ch for ch in s.upper() if 'A'<=ch<='Z')
def q(x,dp=6):
    if x is None: return ''
    d=Decimal(x.numerator)/Decimal(x.denominator)
    return str(d.quantize(Decimal(1).scaleb(-dp),rounding=ROUND_HALF_EVEN))
pop={norm(r['name'].replace(' County','')):int(r['pop_2020_census_P1_001N']) for r in csv.DictReader(open(R+'census2020_il_county_pop.csv'))}
names={norm(r['county']):r['county'] for r in csv.DictReader(open(O+'il_2022_governor_by_county_VERIFIED.csv'))}
g22={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2022.csv'))}
g26={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2026_raw.csv'))}
px={r['county_key']:r for r in csv.DictReader(open(O+'proxy_primary_pass_a.csv'))}
assert len(g22)==len(px)==len(pop)==102 and set(g22)==set(px)==set(pop), 'key mismatch'
rows={}
for k in g22:
    a=g22[k]; p=px[k]
    s22=F(int(p['gp2022_dem_ballots']),int(p['gp2022_total_ballots'])); s26=F(int(p['gp2026_dem_ballots']),int(p['gp2026_total_ballots']))
    d22=F(int(a['dem_votes']),int(a['ballots_cast']))
    r=dict(k=k,s22=s22,s26=s26,drop=s22-s26,d22=d22,gap22=d22-s22,ob22=int(a['dem_votes'])+int(a['rep_votes'])>int(a['ballots_cast']),b22=int(a['ballots_cast']))
    if k in g26:
        b=g26[k]; D,Rr,B=int(b['dem_votes']),int(b['rep_votes']),int(b['ballots_cast'])
        d26=F(D,B); r.update(d26=d26,gap26=d26-s26,chg=d26-d22,dg=(d26-d22)-(s26-s22),B26=B,D26=D,R26=Rr,ob26=D+Rr>B)
    rows[k]=r
fit=[r for r in rows.values() if 'd26' in r]; n=len(fit)
mx=sum(r['drop'] for r in fit)/n; my=sum(r['chg'] for r in fit)/n
sxx=sum((r['drop']-mx)**2 for r in fit); sxy=sum((r['drop']-mx)*(r['chg']-my) for r in fit); syy=sum((r['chg']-my)**2 for r in fit)
m=sxy/sxx; c=my-m*mx
sse=0
for r in fit:
    r['exp']=c+m*r['drop']; r['res']=r['chg']-r['exp']; r['iev']=r['res']*r['B26']; sse+=r['res']**2
R2=1-sse/syy
tot=sum(r['iev'] for r in fit)
cols=['county','county_key','pop_2020','standin_dem_primary_share_2022','standin_dem_primary_share_2026','standin_drop_2022_to_2026',
 'dem_share_ballots_2022','gap_2022','dem_votes_2026_UNOFFICIAL','rep_votes_2026_UNOFFICIAL','ballots_cast_2026_UNOFFICIAL','dem_share_ballots_2026_UNOFFICIAL','gap_2026_UNOFFICIAL',
 'share_change_2022_to_2026','delta_G','expected_change','residual','implied_extra_votes','over_ballot_2022','over_ballot_2026']
out=[]
for k in sorted(rows,key=lambda k:-pop[k]):
    r=rows[k]; h='d26' in r
    out.append([names[k],k,pop[k],q(r['s22']),q(r['s26']),q(r['drop']),q(r['d22']),q(r['gap22']),
        r.get('D26',''),r.get('R26',''),r.get('B26',''),q(r.get('d26')),q(r.get('gap26')),q(r.get('chg')),q(r.get('dg')),q(r.get('exp')),q(r.get('res')),q(r.get('iev'),2),
        r['ob22'], r['ob26'] if h else ''])
with open(O+'compute_pass_a.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(cols); w.writerows(out)
f22=min(rows.values(),key=lambda r:r['d22']); c22=max(rows.values(),key=lambda r:r['d22'])
f26=min(fit,key=lambda r:r['d26']); c26=max(fit,key=lambda r:r['d26'])
summ=dict(n_fit=n,constant=q(c),multiplier=q(m),r_squared=q(R2),total_implied_extra_votes=q(tot,2),
  sum_positive_implied=q(sum(r['iev'] for r in fit if r['iev']>0),2),sum_negative_implied=q(sum(r['iev'] for r in fit if r['iev']<0),2),
  floor_2022=[names[f22['k']],q(f22['d22'])],ceiling_2022=[names[c22['k']],q(c22['d22'])],
  floor_2026_UNOFFICIAL=[names[f26['k']],q(f26['d26'])],ceiling_2026_UNOFFICIAL=[names[c26['k']],q(c26['d26'])],
  over_ballot_2022=[names[r['k']] for r in rows.values() if r['ob22']],over_ballot_2026=[names[r['k']] for r in fit if r['ob26']],
  mean_standin_drop=q(mx),mean_share_change=q(my))
json.dump(summ,open(O+'compute_pass_a_summary.json','w'),indent=1); print(json.dumps(summ,indent=1))
