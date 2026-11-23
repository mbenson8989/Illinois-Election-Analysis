"""LOCKED SURPLUS EQUATION, PASS B (pandas/numpy float64 + numpy.polyfit; exact integer rounding for S and D). Reads Pass B parses of the raw SBOE files."""
import pandas as pd, numpy as np, json, re
from math import lcm
O='/workspace/illinois/out/'; R='/workspace/illinois/raw/'
key=lambda s: re.sub('[^A-Z]','',s.upper())
pop=pd.read_csv(R+'census2020_il_county_pop.csv'); pop['county_key']=pop['name'].str.replace(' County','').map(key); pop=pop.rename(columns={'pop_2020_census_P1_001N':'pop_2020'})[['county_key','pop_2020']]
nm=pd.read_csv(O+'il_2022_governor_by_county_VERIFIED.csv')[['county']]; nm['county_key']=nm['county'].map(key)
a=pd.read_csv(O+'pass_b_2022.csv')[['county_key','dem_votes','ballots_cast']]; b=pd.read_csv(O+'pass_b_2026_raw.csv').rename(columns={'dem_votes':'V26','ballots_cast':'B26'})[['county_key','V26','B26']]
p=pd.read_csv(O+'pass_b_proxy.csv')
df=nm.merge(pop,on='county_key',validate='1:1').merge(p,on='county_key',validate='1:1').merge(a,on='county_key',validate='1:1').merge(b,on='county_key',how='left')
assert len(df)==102
def rnd(N,Dn,dp=6):
    neg=(N<0)!=(Dn<0); N,Dn=abs(N),abs(Dn); qq,rr=divmod(N*10**dp,Dn)
    if 2*rr>Dn or (2*rr==Dn and qq%2==1): qq+=1
    s=f"{qq//10**dp}.{qq%10**dp:0{dp}d}"; return ('-'+s) if neg and qq else s
def Sx(v,bb,pd_,pt):  # 100*(v/bb - pd_/pt) exact
    L=lcm(bb,pt); return rnd((v*(L//bb)-pd_*(L//pt))*100,L)
df['D22']=100*df.gp2022_dem_ballots/df.gp2022_total_ballots; df['S22']=100*df.dem_votes/df.ballots_cast-df.D22
df['D26']=np.where(df.B26.notna(),100*df.gp2026_dem_ballots/df.gp2026_total_ballots,np.nan); df['S26']=100*df.V26/df.B26-df.D26
summ={}
for tag,dk,sk,name in [('22','D22','S22','LOCKED_2022_official'),('26','D26','S26','SECONDARY_2026_UNOFFICIAL')]:
    h=df[df[sk].notna()]; x=h[dk].to_numpy()/100; y=h[sk].to_numpy(); m,c=np.polyfit(x,y,1); f=m*x+c; e=y-f
    df.loc[h.index,'f'+tag]=f; df.loc[h.index,'e'+tag]=e; i=int(np.argmax(np.abs(e)))
    summ[name]=dict(n=int(len(h)),multiplier=format(m,'.6f'),offset=format(c,'.6f'),r_squared=format(1-np.sum(e**2)/np.sum((y-y.mean())**2),'.6f'),
        mean_abs_residual_pp=format(np.mean(np.abs(e)),'.6f'),max_residual_county=h.county.iloc[i],max_residual_pp=format(e[i],'.6f'))
df=df.sort_values('pop_2020',ascending=False); F6=lambda s:s.map(lambda v:'' if pd.isna(v) else format(v,'.6f'))
out=pd.DataFrame({'county':df.county,'county_key':df.county_key,'pop_2020':df.pop_2020,
 'D_2022_pct':[rnd(int(n)*100,int(d)) for n,d in zip(df.gp2022_dem_ballots,df.gp2022_total_ballots)],
 'S_2022_pp':[Sx(int(v),int(bb),int(n),int(d)) for v,bb,n,d in zip(df.dem_votes,df.ballots_cast,df.gp2022_dem_ballots,df.gp2022_total_ballots)],
 'fitted_2022':F6(df.f22),'residual_2022':F6(df.e22),
 'D_2026_pct_UNOFFICIAL':['' if pd.isna(bb) else rnd(int(n)*100,int(d)) for bb,n,d in zip(df.B26,df.gp2026_dem_ballots,df.gp2026_total_ballots)],
 'S_2026_pp_UNOFFICIAL':['' if pd.isna(bb) else Sx(int(v),int(bb),int(n),int(d)) for v,bb,n,d in zip(df.V26,df.B26,df.gp2026_dem_ballots,df.gp2026_total_ballots)],
 'fitted_2026':F6(df.f26),'residual_2026':F6(df.e26)})
out.to_csv(O+'surplus_pass_b.csv',index=False); json.dump(summ,open(O+'surplus_pass_b_summary.json','w'),indent=1)
