import csv,json
O='/workspace/illinois/out/'
A={r['county_key']:r for r in csv.DictReader(open(O+'surplus_pass_a.csv'))}; B={r['county_key']:r for r in csv.DictReader(open(O+'surplus_pass_b.csv'))}
assert set(A)==set(B)==set(A) and len(A)==102
mm=[[k,c,A[k][c],B[k][c]] for k in A for c in A[k] if A[k][c]!=B[k][c]]; n=sum(len(A[k]) for k in A)
sa=json.load(open(O+'surplus_pass_a_summary.json')); sb=json.load(open(O+'surplus_pass_b_summary.json'))
fm=[[f,k,sa[f][k],sb[f][k]] for f in sa for k in sa[f] if sa[f][k]!=sb[f][k]]; nf=sum(len(v) for v in sa.values())
res=dict(table_cells=n,table_matched=n-len(mm),table_mismatches=mm,fit_fields=nf,fit_matched=nf-len(fm),fit_mismatches=fm,ship=not mm and not fm)
json.dump(res,open(O+'verification_surplus_locked.json','w'),indent=1); print({k:v for k,v in res.items()})
