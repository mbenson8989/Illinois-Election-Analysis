"""Cell-by-cell comparison of Pass A vs Pass B (all CSV cells + summary + stand-in + 2026 raw). Writes out/verification_full.json"""
import csv, json
O='/workspace/illinois/out/'
def cmp(fa,fb,key):
    A={r[key]:r for r in csv.DictReader(open(O+fa))}; B={r[key]:r for r in csv.DictReader(open(O+fb))}
    assert set(A)==set(B)
    n=0; mm=[]
    for k in A:
        assert set(A[k])==set(B[k])
        for c in A[k]:
            n+=1
            if A[k][c]!=B[k][c]: mm.append([k,c,A[k][c],B[k][c]])
    return dict(file_a=fa,file_b=fb,rows=len(A),cells=n,matched=n-len(mm),mismatches=mm)
res={'stand_in_primary_ballots':cmp('proxy_primary_pass_a.csv','pass_b_proxy.csv','county_key'),
     'raw_2026_UNOFFICIAL':cmp('pass_a_2026_raw.csv','pass_b_2026_raw.csv','county_key'),
     'computed_table':cmp('compute_pass_a.csv','compute_pass_b.csv','county_key')}
a=json.load(open(O+'compute_pass_a_summary.json')); b=json.load(open(O+'compute_pass_b_summary.json'))
res['summary']=dict(fields=len(a),matched=sum(a[k]==b.get(k) for k in a),mismatches=[[k,a[k],b.get(k)] for k in a if a[k]!=b.get(k)])
res['verification_2022']=json.load(open(O+'verification_2022.json'))
res['ship']=all(not v['mismatches'] for k,v in res.items() if isinstance(v,dict) and 'mismatches' in v) and res['verification_2022'].get('ship') is True
json.dump(res,open(O+'verification_full.json','w'),indent=1)
for k,v in res.items():
    if isinstance(v,dict) and 'mismatches' in v: print(k,v.get('cells',v.get('fields')),v.get('matched'),len(v['mismatches']))
print('SHIP',res['ship'])
