"""COMPUTE PASS B (pandas/numpy float64; numpy.polyfit for OLS; format '.6f').
Inputs: out/pass_b_2022.csv, out/pass_b_2026_raw.csv, out/pass_b_proxy.csv (pdfplumber stand-in parse), census CSV."""
import pandas as pd, numpy as np, json, re
O='/workspace/illinois/out/'; R='/workspace/illinois/raw/'
key=lambda s: re.sub('[^A-Z]','',s.upper())
pop=pd.read_csv(R+'census2020_il_county_pop.csv'); pop['county_key']=pop['name'].str.replace(' County','').map(key); pop=pop.rename(columns={'pop_2020_census_P1_001N':'pop_2020'})[['county_key','pop_2020']]
nm=pd.read_csv(O+'il_2022_governor_by_county_VERIFIED.csv')[['county']]; nm['county_key']=nm['county'].map(key)
a=pd.read_csv(O+'pass_b_2022.csv'); b=pd.read_csv(O+'pass_b_2026_raw.csv'); p=pd.read_csv(O+'pass_b_proxy.csv')
df=nm.merge(pop,on='county_key',validate='1:1').merge(p,on='county_key',validate='1:1').merge(a[['county_key','dem_votes','rep_votes','ballots_cast']],on='county_key',validate='1:1')
df=df.merge(b.rename(columns={'dem_votes':'D26','rep_votes':'R26','ballots_cast':'B26'})[['county_key','D26','R26','B26']],on='county_key',how='left')
assert len(df)==102
df['s22']=df.gp2022_dem_ballots/df.gp2022_total_ballots; df['s26']=df.gp2026_dem_ballots/df.gp2026_total_ballots; df['drop']=df.s22-df.s26
df['d22']=df.dem_votes/df.ballots_cast; df['gap22']=df.d22-df.s22
df['d26']=df.D26/df.B26; df['gap26']=df.d26-df.s26; df['chg']=df.d26-df.d22; df['dg']=df.chg-(df.s26-df.s22)
fit=df[df.B26.notna()]
m,c=np.polyfit(fit['drop'].to_numpy(),fit['chg'].to_numpy(),1)
df['exp']=np.where(df.B26.notna(),c+m*df['drop'],np.nan); df['res']=df.chg-df.exp; df['iev']=df.res*df.B26
r2=float(np.corrcoef(fit['drop'],fit['chg'])[0,1]**2)
df['ob22']=(df.dem_votes+df.rep_votes)>df.ballots_cast; df['ob26']=(df.D26+df.R26)>df.B26
df=df.sort_values('pop_2020',ascending=False)
def ratio6(n,d):
    # exact integer round-half-even of n/d to 6 dp (fix for exact decimal ties, e.g. Stephenson 6199/16000=0.3874375)
    if pd.isna(n) or pd.isna(d): return ''
    n=int(n); d=int(d); q_,r_=divmod(n*10**6,d)
    if 2*r_>d or (2*r_==d and q_%2==1): q_+=1
    return f"{q_//10**6}.{q_%10**6:06d}"
f6=lambda x: '' if pd.isna(x) else format(x,'.6f'); f2=lambda x: '' if pd.isna(x) else format(x,'.2f'); fi=lambda x:'' if pd.isna(x) else str(int(x))
out=pd.DataFrame({'county':df.county,'county_key':df.county_key,'pop_2020':df.pop_2020,
 'standin_dem_primary_share_2022':[ratio6(n,d) for n,d in zip(df.gp2022_dem_ballots,df.gp2022_total_ballots)],'standin_dem_primary_share_2026':[ratio6(n,d) for n,d in zip(df.gp2026_dem_ballots,df.gp2026_total_ballots)],'standin_drop_2022_to_2026':df['drop'].map(f6),
 'dem_share_ballots_2022':[ratio6(n,d) for n,d in zip(df.dem_votes,df.ballots_cast)],'gap_2022':df.gap22.map(f6),'dem_votes_2026_UNOFFICIAL':df.D26.map(fi),'rep_votes_2026_UNOFFICIAL':df.R26.map(fi),'ballots_cast_2026_UNOFFICIAL':df.B26.map(fi),
 'dem_share_ballots_2026_UNOFFICIAL':[ratio6(n,d) for n,d in zip(df.D26,df.B26)],'gap_2026_UNOFFICIAL':df.gap26.map(f6),'share_change_2022_to_2026':df.chg.map(f6),'delta_G':df.dg.map(f6),
 'expected_change':df.exp.map(f6),'residual':df.res.map(f6),'implied_extra_votes':df.iev.map(f2),'over_ballot_2022':df.ob22,
 'over_ballot_2026':[('' if pd.isna(b_) else str(bool(o))) for b_,o in zip(df.B26,df.ob26)]})
out.to_csv(O+'compute_pass_b.csv',index=False)
fit=df[df.B26.notna()]
summ=dict(n_fit=int(len(fit)),constant=f6(c),multiplier=f6(m),r_squared=f6(r2),total_implied_extra_votes=f2(fit.iev.sum()),
 sum_positive_implied=f2(fit.iev[fit.iev>0].sum()),sum_negative_implied=f2(fit.iev[fit.iev<0].sum()),
 floor_2022=[df.loc[df.d22.idxmin(),'county'],f6(df.d22.min())],ceiling_2022=[df.loc[df.d22.idxmax(),'county'],f6(df.d22.max())],
 floor_2026_UNOFFICIAL=[fit.loc[fit.d26.idxmin(),'county'],f6(fit.d26.min())],ceiling_2026_UNOFFICIAL=[fit.loc[fit.d26.idxmax(),'county'],f6(fit.d26.max())],
 over_ballot_2022=df.county[df.ob22].tolist(),over_ballot_2026=fit.county[fit.ob26.astype(bool)].tolist(),
 mean_standin_drop=f6(fit['drop'].mean()),mean_share_change=f6(fit.chg.mean()))
json.dump(summ,open(O+'compute_pass_b_summary.json','w'),indent=1)
