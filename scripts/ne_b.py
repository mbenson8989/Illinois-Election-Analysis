"""NEBRASKA-FORMAT CELLS, PASS B (pandas/numpy float64 for fit; exact integer rounding for rational cells). Inputs: Pass B files."""
import pandas as pd, numpy as np, json, re
from math import lcm
O='/workspace/illinois/out/'; Rw='/workspace/illinois/raw/'
key=lambda s: re.sub('[^A-Z]','',s.upper())
pop=pd.read_csv(Rw+'census2020_il_county_pop.csv'); pop['county_key']=pop['name'].str.replace(' County','').map(key); pop=pop.rename(columns={'pop_2020_census_P1_001N':'pop_2020'})[['county_key','pop_2020']]
nm=pd.read_csv(O+'il_2022_governor_by_county_VERIFIED.csv')[['county']]; nm['county_key']=nm['county'].map(key)
a=pd.read_csv(O+'pass_b_2022.csv')[['county_key','dem_votes','ballots_cast']].rename(columns={'dem_votes':'D22','ballots_cast':'B22'})
b=pd.read_csv(O+'pass_b_2026_raw.csv')[['county_key','dem_votes','ballots_cast']].rename(columns={'dem_votes':'D26','ballots_cast':'B26'})
p=pd.read_csv(O+'pass_b_proxy.csv').rename(columns={'gp2022_dem_ballots':'PD22','gp2022_total_ballots':'PT22','gp2026_dem_ballots':'PD26','gp2026_total_ballots':'PT26'})
df=b.merge(a,on='county_key',validate='1:1').merge(p,on='county_key',validate='1:1').merge(nm,on='county_key').merge(pop,on='county_key')
assert len(df)==80
def rnd(N,Dn,dp):  # exact half-even of N/Dn
    neg=(N<0)!=(Dn<0); N,Dn=abs(N),abs(Dn); qq,rr=divmod(N*10**dp,Dn)
    if 2*rr>Dn or (2*rr==Dn and qq%2==1): qq+=1
    s=(str(qq) if dp==0 else f"{qq//10**dp}.{qq%10**dp:0{dp}d}")
    return ('-'+s) if neg and qq!=0 else s
def lin(terms):  # sum of (coef, num, den) -> (N, Dn) times 100
    L=1
    for c,n_,d_ in terms: L=lcm(L,d_)
    return sum(c*n_*(L//d_) for c,n_,d_ in terms)*100, L
out=[]
for _,r in df.iterrows():
    g={c:int(r[c]) for c in ['D22','B22','D26','B26','PD22','PT22','PD26','PT26']}
    T=dict(S_2022=[(1,g['D22'],g['B22'])],S_2026_UNOFFICIAL=[(1,g['D26'],g['B26'])],R_standin_2022=[(1,g['PD22'],g['PT22'])],R_standin_2026=[(1,g['PD26'],g['PT26'])])
    T['G_2022']=T['S_2022']+[(-1,g['PD22'],g['PT22'])]; T['G_2026_UNOFFICIAL']=T['S_2026_UNOFFICIAL']+[(-1,g['PD26'],g['PT26'])]
    T['dG']=[(1,g['D26'],g['B26']),(-1,g['PD26'],g['PT26']),(-1,g['D22'],g['B22']),(1,g['PD22'],g['PT22'])]
    T['dR']=[(1,g['PD26'],g['PT26']),(-1,g['PD22'],g['PT22'])]
    T['vote_share_growth']=[(1,g['D26'],g['B26']),(-1,g['D22'],g['B22'])]
    row={'county':r['county'],'county_key':r['county_key'],'pop_2020':int(r['pop_2020'])}
    vals={k:lin(v) for k,v in T.items()}
    for k,(N,L) in vals.items(): row[k]=rnd(N,L,6)
    loss=g['PD26']<g['PD22']; row['standin_dem_headcount_fell']=str(loss)
    if loss:
        N1,L1=vals['dG']; N2,L2=vals['dR']; L=lcm(L1,L2); N=N1*(L//L1)-abs(N2)*(L//L2); row['wiki_surplus_dG_minus_abs_dR']=rnd(N,L,6)
    else: row['wiki_surplus_dG_minus_abs_dR']=''
    # gap in votes = D26 - D22*PD26/PD22 = (D26*PD22 - D22*PD26)/PD22
    gvN,gvD=g['D26']*g['PD22']-g['D22']*g['PD26'],g['PD22']
    row['gap_in_votes']=rnd(gvN,gvD,6)
    row['_x']=g['PD26']/g['PT26']; row['_y']=100*(g['D26']/g['B26']-g['D22']/g['B22'])
    for k2,k in [('S_2022_2dp','S_2022'),('S_2026_2dp','S_2026_UNOFFICIAL'),('R_2022_2dp','R_standin_2022'),('R_2026_2dp','R_standin_2026'),('G_2022_2dp','G_2022'),('G_2026_2dp','G_2026_UNOFFICIAL'),('dG_2dp','dG'),('dR_2dp','dR'),('vsg_2dp','vote_share_growth')]:
        row[k2]=rnd(*vals[k],2)
    row['gap_in_votes_0dp']=rnd(gvN,gvD,0); row['_dG']=vals['dG'][0]/vals['dG'][1]
    out.append(row)
o=pd.DataFrame(out)
m,c=np.polyfit(o._x.to_numpy(),o._y.to_numpy(),1); pred=m*o._x+c; res=o._y-pred; r2=1-np.sum(res**2)/np.sum((o._y-o._y.mean())**2)
imax=res.abs().idxmax(); maxc=o.loc[imax,'county']; maxr=format(res.loc[imax],'.6f')
o['pred_vsg']=pred.map(lambda v:format(v,'.6f')); o['res_vsg']=res.map(lambda v:format(v,'.6f'))
o=o.sort_values('pop_2020',ascending=False)
cols=['county','county_key','pop_2020','S_2022','S_2026_UNOFFICIAL','R_standin_2022','R_standin_2026','G_2022','G_2026_UNOFFICIAL','dG','dR','standin_dem_headcount_fell','wiki_surplus_dG_minus_abs_dR','vote_share_growth','pred_vsg','res_vsg','gap_in_votes',
      'S_2022_2dp','S_2026_2dp','R_2022_2dp','R_2026_2dp','G_2022_2dp','G_2026_2dp','dG_2dp','dR_2dp','vsg_2dp','gap_in_votes_0dp']
o[cols].to_csv(O+'ne_format_pass_b.csv',index=False)
srt=o.sort_values('_dG')
summ=dict(vote_share_growth_fit=dict(n=int(len(o)),m=format(m,'.6f'),b=format(c,'.6f'),r_squared=format(r2,'.6f'),mean_abs_residual_pp=format(np.mean(np.abs(res)),'.6f'),
    max_residual_county=maxc,max_residual_pp=maxr),
  loss_counties=o[o.standin_dem_headcount_fell=='True'].sort_values('pop_2020',ascending=False).county.tolist(),n_loss=int((o.standin_dem_headcount_fell=='True').sum()),
  dG_ceiling=[[r.county,r.dG_2dp] for r in srt.iloc[::-1].head(5).itertuples()],dG_floor=[[r.county,r.dG_2dp] for r in srt.head(5).itertuples()],n_dG_positive=int((o._dG>0).sum()))
json.dump(summ,open(O+'ne_format_pass_b_summary.json','w'),indent=1)
