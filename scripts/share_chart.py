import csv, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
O='/workspace/illinois/out/'; C='/workspace/illinois/charts/'
UN='UNOFFICIAL (pre-Dec 4, 2026 canvass)'
ST='Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration'
T=list(csv.DictReader(open(O+'share_pass_a.csv'))); F=json.load(open(O+'share_pass_a_summary.json'))['fits']
fig,axs=plt.subplots(1,3,figsize=(16,5.6))
for ax,(fk,dc,sc,ttl,col) in zip(axs,[('A_2022_official','D_2022_pct','S_2022_pp','A: 2022 official (n=102)','#4874a3'),
        ('B_2026_UNOFFICIAL','D_2026_pct_UNOFFICIAL','S_2026_pp_UNOFFICIAL',f'B: 2026 {UN} (n=60)','#c6606b'),
        ('C_deltaG_vs_drop_2026_UNOFFICIAL','D_drop_pp','S_deltaG_pp_UNOFFICIAL',f'C: delta-G vs stand-in drop, 2026 {UN} (n=60)','#6a9c55')]):
    r=[t for t in T if t[sc]]; x=[float(t[dc]) for t in r]; y=[float(t[sc]) for t in r]; f=F[fk]; m=float(f['m']); b=float(f['b'])
    ax.scatter(x,y,s=14,alpha=.65,color=col); xs=[min(x),max(x)]; ax.plot(xs,[m*v/100+b for v in xs],color='k',lw=1.6)
    ax.annotate(f"S = {f['m']} x (D/100) + {f['b']}\nR² = {f['r_squared']}   mean |resid| = {f['mean_abs_residual_pp']} pp",(0.02,0.03),xycoords='axes fraction',fontsize=8)
    t_=[t for t in r if t['county']==f['max_residual_county']][0]; ax.annotate(t_['county'],(float(t_[dc]),float(t_[sc])),fontsize=8,color='darkred')
    ax.axhline(0,color='grey',lw=.5); ax.set_title(ttl,fontsize=9)
    ax.set_xlabel('D (pp): stand-in drop' if fk.startswith('C') else 'D (%): Dem primary ballot share (stand-in)'); ax.set_ylabel('S (pp): 100 x delta-G' if fk.startswith('C') else 'S (pp): Dem share of ballots − stand-in')
fig.suptitle(f'Share-form fits S = m x (D/100) + b — 2026 panels {UN}',fontsize=11); fig.text(.01,.01,ST,fontsize=7)
fig.tight_layout(rect=(0,.03,1,.95)); fig.savefig(C+'il_share_form_fits_UNOFFICIAL.png',dpi=120); print('ok')
