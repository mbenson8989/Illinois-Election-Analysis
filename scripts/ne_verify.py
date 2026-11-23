import csv,json
O='/workspace/illinois/out/'
A={r['county_key']:r for r in csv.DictReader(open(O+'ne_format_pass_a.csv'))}; B={r['county_key']:r for r in csv.DictReader(open(O+'ne_format_pass_b.csv'))}
assert set(A)==set(B) and len(A)==80; n=0; mm=[]
for k in A:
    for c in A[k]:
        n+=1
        if A[k][c]!=B[k][c]: mm.append([k,c,A[k][c],B[k][c]])
sa=json.load(open(O+'ne_format_pass_a_summary.json')); sb=json.load(open(O+'ne_format_pass_b_summary.json'))
def flat(d,p=''):
    out={}
    for k,v in d.items():
        if isinstance(v,dict): out.update(flat(v,p+k+'.'))
        else: out[p+k]=v
    return out
fa,fb=flat(sa),flat(sb); fm=[[k,fa[k],fb.get(k)] for k in fa if fa[k]!=fb.get(k)]
# consistency with already-published verified table: dG = 100*delta_G (6dp table) within rounding
T={r['county_key']:r for r in csv.DictReader(open(O+'il_governor_reverse_math_2022_2026_VERIFIED.csv'))}
from decimal import Decimal as D
cons=sum(abs(D(A[k]['dG'])-100*D(T[k]['delta_G']))<=D('0.00005') and abs(D(A[k]['vote_share_growth'])-100*D(T[k]['share_change_2022_to_2026']))<=D('0.00005') for k in A)
res=dict(table_cells=n,table_matched=n-len(mm),table_mismatches=mm,summary_fields=len(fa),summary_matched=len(fa)-len(fm),summary_mismatches=fm,consistent_with_published_dG_and_share_change=[cons,len(A)],ship=not mm and not fm and cons==len(A))
json.dump(res,open(O+'verification_ne_format.json','w'),indent=1); print({k:v for k,v in res.items()})
