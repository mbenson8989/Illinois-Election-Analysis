"""LOCKED SURPLUS EQUATION, PASS A (stdlib exact Fractions; Decimal ROUND_HALF_EVEN). Reads Pass A parses of the raw SBOE files.
S = m x (D/100) + b ; D = 100 x Dem primary ballots / all primary ballots (STAND-IN; NOT party registration; IL has no party registration);
S = 100 x (Dem votes / ballots cast) - D, in pp. LOCKED: 2022 official, all 102 counties. SECONDARY: 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass), 80 counties."""
import csv, json
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
getcontext().prec=60
O='/workspace/illinois/out/'; R='/workspace/illinois/raw/'
norm=lambda s:''.join(ch for ch in s.upper() if 'A'<=ch<='Z')
def q(x,dp=6):
    if x is None: return ''
    v=(Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal(1).scaleb(-dp),rounding=ROUND_HALF_EVEN); return str(abs(v) if v==0 else v)
pop={norm(r['name'].replace(' County','')):int(r['pop_2020_census_P1_001N']) for r in csv.DictReader(open(R+'census2020_il_county_pop.csv'))}
names={norm(r['county']):r['county'] for r in csv.DictReader(open(O+'il_2022_governor_by_county_VERIFIED.csv'))}
g22={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2022.csv'))}; g26={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2026_raw.csv'))}
px={r['county_key']:r for r in csv.DictReader(open(O+'proxy_primary_pass_a.csv'))}
assert len(g22)==len(px)==102
H=F(100); rows={}
for k in g22:
    p=px[k]; r={'k':k}
    r['D22']=H*F(int(p['gp2022_dem_ballots']),int(p['gp2022_total_ballots'])); r['S22']=H*F(int(g22[k]['dem_votes']),int(g22[k]['ballots_cast']))-r['D22']
    if k in g26:
        r['D26']=H*F(int(p['gp2026_dem_ballots']),int(p['gp2026_total_ballots'])); r['S26']=H*F(int(g26[k]['dem_votes']),int(g26[k]['ballots_cast']))-r['D26']
    rows[k]=r
def fit(dk,sk,tag):
    h=[r for r in rows.values() if sk in r]; n=len(h); x=[r[dk]/H for r in h]; y=[r[sk] for r in h]
    mx=sum(x)/n; my=sum(y)/n; m=sum((a-mx)*(b-my) for a,b in zip(x,y))/sum((a-mx)**2 for a in x); b=my-m*mx
    for r,a in zip(h,x): r['f'+tag]=m*a+b; r['e'+tag]=r[sk]-r['f'+tag]
    r2=1-sum(r['e'+tag]**2 for r in h)/sum((v-my)**2 for v in y); mx_=max(h,key=lambda r:abs(r['e'+tag]))
    return dict(n=n,multiplier=q(m),offset=q(b),r_squared=q(r2),mean_abs_residual_pp=q(sum(abs(r['e'+tag]) for r in h)/n),max_residual_county=names[mx_['k']],max_residual_pp=q(mx_['e'+tag]))
summ={'LOCKED_2022_official':fit('D22','S22','22'),'SECONDARY_2026_UNOFFICIAL':fit('D26','S26','26')}
with open(O+'surplus_pass_a.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['county','county_key','pop_2020','D_2022_pct','S_2022_pp','fitted_2022','residual_2022','D_2026_pct_UNOFFICIAL','S_2026_pp_UNOFFICIAL','fitted_2026','residual_2026'])
    for k in sorted(rows,key=lambda k:-pop[k]):
        r=rows[k]; g=lambda c:q(r.get(c)); w.writerow([names[k],k,pop[k],g('D22'),g('S22'),g('f22'),g('e22'),g('D26'),g('S26'),g('f26'),g('e26')])
json.dump(summ,open(O+'surplus_pass_a_summary.json','w'),indent=1); print(json.dumps(summ,indent=1))
