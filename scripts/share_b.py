"""SHARE-FORM CHECK, PASS B (pandas/numpy float64, numpy.polyfit, exact-int rounding only for pure vote ratios).
Inputs are the Pass B files: pass_b_2022.csv, pass_b_2026_raw.csv, pass_b_proxy.csv."""
import pandas as pd, numpy as np, json, re
O='/workspace/illinois/out/'; R='/workspace/illinois/raw/'
key=lambda s: re.sub('[^A-Z]','',s.upper())
pop=pd.read_csv(R+'census2020_il_county_pop.csv'); pop['county_key']=pop['name'].str.replace(' County','').map(key); pop=pop.rename(columns={'pop_2020_census_P1_001N':'pop_2020'})[['county_key','pop_2020']]
nm=pd.read_csv(O+'il_2022_governor_by_county_VERIFIED.csv')[['county']]; nm['county_key']=nm['county'].map(key)
a=pd.read_csv(O+'pass_b_2022.csv'); b=pd.read_csv(O+'pass_b_2026_raw.csv'); p=pd.read_csv(O+'pass_b_proxy.csv')
df=nm.merge(pop,on='county_key',validate='1:1').merge(p,on='county_key',validate='1:1').merge(a[['county_key','dem_votes','ballots_cast']],on='county_key',validate='1:1')
df=df.merge(b.rename(columns={'dem_votes':'D26v','ballots_cast':'B26'})[['county_key','D26v','B26']],on='county_key',how='left')
def rq(num,den):  # exact half-even of num/den at 6 dp, ints
    q_,r_=divmod(num*10**6,den)
    if 2*r_>den or (2*r_==den and q_%2==1): q_+=1
    s='-' if q_<0 else ''; q_=abs(q_); return f"{s}{q_//10**6}.{q_%10**6:06d}"
def exact_pp(terms):
    # terms: list of (sign, num, den); returns 100*sum as rational -> 6dp string
    from math import lcm
    L=1
    for s,n_,d_ in terms: L=lcm(L,d_)
    N=sum(s*n_*(L//d_) for s,n_,d_ in terms)*100
    if N<0: return '-'+rq(-N,L).lstrip('-') if rq(-N,L)!='0.000000' else '0.000000'
    return rq(N,L)
s22=df.gp2022_dem_ballots/df.gp2022_total_ballots; s26=df.gp2026_dem_ballots/df.gp2026_total_ballots
d22=df.dem_votes/df.ballots_cast; d26=df.D26v/df.B26
df['D22']=100*s22; df['S22']=100*(d22-s22); df['D26']=100*s26; df['S26']=100*(d26-s26); df['DC']=100*(s22-s26); df['SC']=100*((d26-d22)-(s26-s22))
PM=-0.205049; PB=0.000194
fits={}
for name,(dk,sk) in {'A_2022_official':('D22','S22'),'B_2026_UNOFFICIAL':('D26','S26'),'C_deltaG_vs_drop_2026_UNOFFICIAL':('DC','SC')}.items():
    h=df[df[dk].notna() & df[sk].notna()]; x=h[dk].to_numpy()/100; y=h[sk].to_numpy()
    m,c=np.polyfit(x,y,1); pred=m*x+c; res=y-pred; r2=1-np.sum(res**2)/np.sum((y-y.mean())**2)
    df.loc[h.index,'pred_'+name]=pred; df.loc[h.index,'res_'+name]=res
    pub=y-(PM*x+PB); df.loc[h.index,'pub_'+name]=pub
    i=np.argmax(np.abs(res)); j=np.argmax(np.abs(pub))
    f=lambda v: format(v,'.6f')
    fits[name]=dict(n=int(len(h)),m=f(m),b=f(c),r_squared=f(r2),mean_abs_residual_pp=f(np.mean(np.abs(res))),max_residual_county=h.county.iloc[i],max_residual_pp=f(res[i]),
        published_applied_mean_abs_residual_pp=f(np.mean(np.abs(pub))),published_applied_max_residual_county=h.county.iloc[j],published_applied_max_residual_pp=f(pub[j]),
        mean_S_pp=f(y.mean()),mean_D_pct=f(x.mean()*100))
df=df.sort_values('pop_2020',ascending=False)
F6=lambda s: s.map(lambda v:'' if pd.isna(v) else format(v,'.6f'))
def ex(row,which):
    g=lambda c:int(row[c])
    if which=='D22': return exact_pp([(1,g('gp2022_dem_ballots'),g('gp2022_total_ballots'))])
    if which=='S22': return exact_pp([(1,g('dem_votes'),g('ballots_cast')),(-1,g('gp2022_dem_ballots'),g('gp2022_total_ballots'))])
    if pd.isna(row['B26']): return ''
    if which=='D26': return exact_pp([(1,g('gp2026_dem_ballots'),g('gp2026_total_ballots'))])
    if which=='S26': return exact_pp([(1,g('D26v'),g('B26')),(-1,g('gp2026_dem_ballots'),g('gp2026_total_ballots'))])
    if which=='DC': return exact_pp([(1,g('gp2022_dem_ballots'),g('gp2022_total_ballots')),(-1,g('gp2026_dem_ballots'),g('gp2026_total_ballots'))])
    if which=='SC': return exact_pp([(1,g('D26v'),g('B26')),(-1,g('dem_votes'),g('ballots_cast')),(-1,g('gp2026_dem_ballots'),g('gp2026_total_ballots')),(1,g('gp2022_dem_ballots'),g('gp2022_total_ballots'))])
out=pd.DataFrame({'county':df.county,'county_key':df.county_key,'pop_2020':df.pop_2020})
for col,w in [('D_2022_pct','D22'),('S_2022_pp','S22')]: out[col]=[ex(r,w) for _,r in df.iterrows()]
out['pred_A']=F6(df.pred_A_2022_official); out['res_A']=F6(df.res_A_2022_official); out['res_published_2022']=F6(df.pub_A_2022_official)
for col,w in [('D_2026_pct_UNOFFICIAL','D26'),('S_2026_pp_UNOFFICIAL','S26')]: out[col]=[ex(r,w) for _,r in df.iterrows()]
out['pred_B']=F6(df.pred_B_2026_UNOFFICIAL); out['res_B']=F6(df.res_B_2026_UNOFFICIAL); out['res_published_2026']=F6(df.pub_B_2026_UNOFFICIAL)
for col,w in [('D_drop_pp','DC'),('S_deltaG_pp_UNOFFICIAL','SC')]: out[col]=[ex(r,w) for _,r in df.iterrows()]
out['pred_C']=F6(df.pred_C_deltaG_vs_drop_2026_UNOFFICIAL); out['res_C']=F6(df.res_C_deltaG_vs_drop_2026_UNOFFICIAL); out['res_published_C']=F6(df.pub_C_deltaG_vs_drop_2026_UNOFFICIAL)
out.to_csv(O+'share_pass_b.csv',index=False)
json.dump(dict(published=dict(m='-0.205049',b='0.000194',form='share change = b + m x stand-in drop (fractions), R2 0.432249, n=60'),fits=fits),open(O+'share_pass_b_summary.json','w'),indent=1)
