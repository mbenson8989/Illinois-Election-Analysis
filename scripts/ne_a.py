"""NEBRASKA-FORMAT CELLS, PASS A (stdlib Fractions, Decimal ROUND_HALF_EVEN).
For the 80 counties with 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass) data. R = registration STAND-IN (Dem primary ballot share; NOT registration).
Nebraska-template lines: S (Dem share of ballots cast, pp), R (stand-in, pp), G=S-R, dG, dR, stand-in headcount fell?, wiki surplus dG-|dR| (loss only),
gap in votes = D2026 - D2022 x (standin Dem 2026 / standin Dem 2022); vote-share growth fit: (S26-S22) = m x (R26/100) + b."""
import csv, json
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
getcontext().prec=60
O='/workspace/illinois/out/'; Rw='/workspace/illinois/raw/'
norm=lambda s:''.join(ch for ch in s.upper() if 'A'<=ch<='Z')
def q(x,dp=6):
    if x is None or x=='': return ''
    if isinstance(x,int): x=F(x)
    v=(Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal(1).scaleb(-dp),rounding=ROUND_HALF_EVEN)
    return str(abs(v) if v==0 else v)  # no '-0.00'
pop={norm(r['name'].replace(' County','')):int(r['pop_2020_census_P1_001N']) for r in csv.DictReader(open(Rw+'census2020_il_county_pop.csv'))}
names={norm(r['county']):r['county'] for r in csv.DictReader(open(O+'il_2022_governor_by_county_VERIFIED.csv'))}
g22={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2022.csv'))}
g26={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2026_raw.csv'))}
px={r['county_key']:r for r in csv.DictReader(open(O+'proxy_primary_pass_a.csv'))}
H=F(100); rows=[]
for k in g26:
    a=g22[k]; b=g26[k]; p=px[k]
    D22,B22=int(a['dem_votes']),int(a['ballots_cast']); D26,B26=int(b['dem_votes']),int(b['ballots_cast'])
    PD22,PT22,PD26,PT26=int(p['gp2022_dem_ballots']),int(p['gp2022_total_ballots']),int(p['gp2026_dem_ballots']),int(p['gp2026_total_ballots'])
    S22,S26=H*F(D22,B22),H*F(D26,B26); R22,R26=H*F(PD22,PT22),H*F(PD26,PT26)
    G22,G26=S22-R22,S26-R26; dG=G26-G22; dR=R26-R22; loss=PD26<PD22
    rows.append(dict(k=k,D22=D22,B22=B22,D26=D26,B26=B26,PD22=PD22,PT22=PT22,PD26=PD26,PT26=PT26,S22=S22,S26=S26,R22=R22,R26=R26,G22=G22,G26=G26,dG=dG,dR=dR,
        VSG=S26-S22,loss=loss,WS=(dG-abs(dR)) if loss else None,GV=D26-D22*F(PD26,PD22)))
n=len(rows); x=[r['R26']/H for r in rows]; y=[r['VSG'] for r in rows]
mx=sum(x)/n; my=sum(y)/n; sxx=sum((v-mx)**2 for v in x); sxy=sum((u-mx)*(v-my) for u,v in zip(x,y)); syy=sum((v-my)**2 for v in y)
m=sxy/sxx; b=my-m*mx
for r,u in zip(rows,x): r['pred']=m*u+b; r['res']=r['VSG']-r['pred']
r2=1-sum(r['res']**2 for r in rows)/syy; mae=sum(abs(r['res']) for r in rows)/n; mxr=max(rows,key=lambda r:abs(r['res']))
cols=['county','county_key','pop_2020','S_2022','S_2026_UNOFFICIAL','R_standin_2022','R_standin_2026','G_2022','G_2026_UNOFFICIAL','dG','dR','standin_dem_headcount_fell','wiki_surplus_dG_minus_abs_dR','vote_share_growth','pred_vsg','res_vsg','gap_in_votes',
      'S_2022_2dp','S_2026_2dp','R_2022_2dp','R_2026_2dp','G_2022_2dp','G_2026_2dp','dG_2dp','dR_2dp','vsg_2dp','gap_in_votes_0dp']
with open(O+'ne_format_pass_a.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(cols)
    for r in sorted(rows,key=lambda r:-pop[r['k']]):
        w.writerow([names[r['k']],r['k'],pop[r['k']],q(r['S22']),q(r['S26']),q(r['R22']),q(r['R26']),q(r['G22']),q(r['G26']),q(r['dG']),q(r['dR']),r['loss'],q(r['WS']),q(r['VSG']),q(r['pred']),q(r['res']),q(r['GV']),
            q(r['S22'],2),q(r['S26'],2),q(r['R22'],2),q(r['R26'],2),q(r['G22'],2),q(r['G26'],2),q(r['dG'],2),q(r['dR'],2),q(r['VSG'],2),q(r['GV'],0)])
summ=dict(vote_share_growth_fit=dict(n=n,m=q(m),b=q(b),r_squared=q(r2),mean_abs_residual_pp=q(mae),max_residual_county=names[mxr['k']],max_residual_pp=q(mxr['res'])),
  loss_counties=[names[r['k']] for r in sorted(rows,key=lambda r:-pop[r['k']]) if r['loss']],n_loss=sum(r['loss'] for r in rows),
  dG_ceiling=[[names[r['k']],q(r['dG'],2)] for r in sorted(rows,key=lambda r:-r['dG'])[:5]],dG_floor=[[names[r['k']],q(r['dG'],2)] for r in sorted(rows,key=lambda r:r['dG'])[:5]],
  n_dG_positive=sum(r['dG']>0 for r in rows))
json.dump(summ,open(O+'ne_format_pass_a_summary.json','w'),indent=1); print(json.dumps(summ,indent=1))
