"""Chart for the LOCKED surplus equation (surplus form only; no delta-G). Reads verified out/surplus_pass_a.csv + summary."""
import csv,json,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
O='/workspace/illinois/out/'; R=list(csv.DictReader(open(O+'surplus_pass_a.csv'))); S=json.load(open(O+'surplus_pass_a_summary.json'))
fig,ax=plt.subplots(1,2,figsize=(14,5.2))
for a,(lab,dk,sk,f) in zip(ax,[('LOCKED: 2022 official, all 102 counties','D_2022_pct','S_2022_pp',S['LOCKED_2022_official']),('Secondary: 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass)','D_2026_pct_UNOFFICIAL','S_2026_pp_UNOFFICIAL',S['SECONDARY_2026_UNOFFICIAL'])]):
    pts=[(float(r[dk]),float(r[sk])) for r in R if r[sk]]
    a.scatter([p[0] for p in pts],[p[1] for p in pts],s=14,alpha=.7)
    m,b=float(f['multiplier']),float(f['offset']); xs=[0,100]
    a.plot(xs,[m*x/100+b for x in xs],color='crimson',label=f"S = {f['multiplier']} x (D/100) + {f['offset']}\nR² = {f['r_squared']}, mean |resid| = {f['mean_abs_residual_pp']} pp, n = {f['n']}")
    a.set_xlim(0,100); a.axhline(0,color='gray',lw=.6); a.set_title(lab,fontsize=10); a.legend(fontsize=8,loc='upper right')
    a.set_xlabel('D = Dem primary-ballot share, % (registration STAND-IN, not registration)'); a.set_ylabel('S = Dem share of ballots cast − D (points)')
fig.suptitle('Illinois Surplus Equation, S = multiplier × (D/100) + offset',fontsize=12); fig.tight_layout()
fig.savefig('/workspace/illinois/charts/il_surplus_equation_locked_UNOFFICIAL2026.png',dpi=130); print('ok')
