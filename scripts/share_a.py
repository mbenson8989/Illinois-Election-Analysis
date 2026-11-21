"""SHARE-FORM CHECK, PASS A (stdlib, exact Fractions, Decimal ROUND_HALF_EVEN).
S = m*(D/100) + b ; D = registration STAND-IN share in percent (Dem primary ballot share x100 - NOT official party registration);
S = surplus in percentage points = 100 x (Dem share of ballots cast - stand-in share)  [= 100 x gap].
Fits: A = 2022 (official, 102 counties); B = 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass), 60 counties, no gap filling;
C = delta-G form: S = 100 x delta-G, D = 100 x stand-in drop (algebraic re-expression of the published change-vs-drop fit), 60 counties.
Also applies the PUBLISHED m=-0.205049, b=0.000194 literally in the share form."""
import csv, json
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
getcontext().prec=60
O='/workspace/illinois/out/'; R='/workspace/illinois/raw/'
norm=lambda s:''.join(ch for ch in s.upper() if 'A'<=ch<='Z')
def q(x,dp=6):
    if x is None: return ''
    return str((Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal(1).scaleb(-dp),rounding=ROUND_HALF_EVEN))
pop={norm(r['name'].replace(' County','')):int(r['pop_2020_census_P1_001N']) for r in csv.DictReader(open(R+'census2020_il_county_pop.csv'))}
names={norm(r['county']):r['county'] for r in csv.DictReader(open(O+'il_2022_governor_by_county_VERIFIED.csv'))}
g22={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2022.csv'))}
g26={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2026_raw.csv'))}
px={r['county_key']:r for r in csv.DictReader(open(O+'proxy_primary_pass_a.csv'))}
PM=F('-0.205049'); PB=F('0.000194')   # as published on Locked-Illinois-Formula.md
H=F(100)
rows={}
for k in g22:
    p=px[k]; a=g22[k]
    s22=F(int(p['gp2022_dem_ballots']),int(p['gp2022_total_ballots'])); s26=F(int(p['gp2026_dem_ballots']),int(p['gp2026_total_ballots']))
    d22=F(int(a['dem_votes']),int(a['ballots_cast']))
    r=dict(k=k,D22=H*s22,S22=H*(d22-s22))
    if k in g26:
        b=g26[k]; d26=F(int(b['dem_votes']),int(b['ballots_cast']))
        r.update(D26=H*s26,S26=H*(d26-s26),DC=H*(s22-s26),SC=H*((d26-d22)-(s26-s22)))
    rows[k]=r
def ols(pts):
    n=len(pts); mx=sum(x for x,y in pts)/n; my=sum(y for x,y in pts)/n
    sxx=sum((x-mx)**2 for x,y in pts); sxy=sum((x-mx)*(y-my) for x,y in pts); syy=sum((y-my)**2 for x,y in pts)
    m=sxy/sxx; b=my-m*mx
    return m,b,1-sum((y-(m*x+b))**2 for x,y in pts)/syy,n
fits={}
for name,(dk,sk) in {'A_2022_official':('D22','S22'),'B_2026_UNOFFICIAL':('D26','S26'),'C_deltaG_vs_drop_2026_UNOFFICIAL':('DC','SC')}.items():
    have=[r for r in rows.values() if dk in r]
    # share form S = m*(D/100)+b  -> regress S on D/100
    m,b,r2,n=ols([(r[dk]/H,r[sk]) for r in have])
    for r in have: r['pred_'+name]=m*(r[dk]/H)+b; r['res_'+name]=r[sk]-r['pred_'+name]
    mae=sum(abs(r['res_'+name]) for r in have)/n; mx_=max(have,key=lambda r:abs(r['res_'+name]))
    # published m,b applied literally
    for r in have: r['pub_'+name]=r[sk]-(PM*(r[dk]/H)+PB)
    pmae=sum(abs(r['pub_'+name]) for r in have)/n; pmx=max(have,key=lambda r:abs(r['pub_'+name]))
    fits[name]=dict(n=n,m=q(m),b=q(b),r_squared=q(r2),mean_abs_residual_pp=q(mae),max_residual_county=names[mx_['k']],max_residual_pp=q(mx_['res_'+name]),
        published_applied_mean_abs_residual_pp=q(pmae),published_applied_max_residual_county=names[pmx['k']],published_applied_max_residual_pp=q(pmx['pub_'+name]),
        mean_S_pp=q(sum(r[sk] for r in have)/n),mean_D_pct=q(sum(r[dk] for r in have)/n))
cols=['county','county_key','pop_2020','D_2022_pct','S_2022_pp','pred_A','res_A','res_published_2022',
      'D_2026_pct_UNOFFICIAL','S_2026_pp_UNOFFICIAL','pred_B','res_B','res_published_2026',
      'D_drop_pp','S_deltaG_pp_UNOFFICIAL','pred_C','res_C','res_published_C']
with open(O+'share_pass_a.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(cols)
    for k in sorted(rows,key=lambda k:-pop[k]):
        r=rows[k]; g=lambda x:q(r.get(x))
        w.writerow([names[k],k,pop[k],g('D22'),g('S22'),g('pred_A_2022_official'),g('res_A_2022_official'),g('pub_A_2022_official'),
          g('D26'),g('S26'),g('pred_B_2026_UNOFFICIAL'),g('res_B_2026_UNOFFICIAL'),g('pub_B_2026_UNOFFICIAL'),
          g('DC'),g('SC'),g('pred_C_deltaG_vs_drop_2026_UNOFFICIAL'),g('res_C_deltaG_vs_drop_2026_UNOFFICIAL'),g('pub_C_deltaG_vs_drop_2026_UNOFFICIAL')])
json.dump(dict(published=dict(m=str(PM),b=str(PB),form='share change = b + m x stand-in drop (fractions), R2 0.432249, n=60'),fits=fits),open(O+'share_pass_a_summary.json','w'),indent=1)
print(json.dumps(fits,indent=1))
