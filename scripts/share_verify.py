import csv,json
O='/workspace/illinois/out/'
A={r['county_key']:r for r in csv.DictReader(open(O+'share_pass_a.csv'))}; B={r['county_key']:r for r in csv.DictReader(open(O+'share_pass_b.csv'))}
assert set(A)==set(B); n=0; mm=[]
for k in A:
    for c in A[k]:
        n+=1
        if A[k][c]!=B[k][c]: mm.append([k,c,A[k][c],B[k][c]])
sa=json.load(open(O+'share_pass_a_summary.json')); sb=json.load(open(O+'share_pass_b_summary.json'))
fm=[[f,k,sa['fits'][f][k],sb['fits'][f][k]] for f in sa['fits'] for k in sa['fits'][f] if sa['fits'][f][k]!=sb['fits'][f][k]]
nf=sum(len(v) for v in sa['fits'].values())
# graph/table consistency: S = 100*gap and res_C = 100*published residual (from the verified published table)
T={r['county_key']:r for r in csv.DictReader(open(O+'il_governor_reverse_math_2022_2026_VERIFIED.csv'))}
from decimal import Decimal as Dd
g=[];c=[]
for k,r in A.items():
    g.append(abs(Dd(r['S_2022_pp'])-100*Dd(T[k]['gap_2022']))<=Dd('0.00005'))
    if r['res_C']: c.append(abs(Dd(r['res_C'])-100*Dd(T[k]['residual']))<=Dd('0.00005'))
res=dict(table_cells=n,table_matched=n-len(mm),table_mismatches=mm,summary_fields=nf,summary_matched=nf-len(fm),summary_mismatches=fm,
  gap_consistency_S2022_eq_100xgap=[sum(g),len(g)],residual_consistency_resC_eq_100xpublished_residual=[sum(c),len(c)],ship=not mm and not fm and all(g) and all(c))
json.dump(res,open(O+'verification_share_form.json','w'),indent=1); print({k:v for k,v in res.items() if 'mismatch' not in k}, len(mm),len(fm))
