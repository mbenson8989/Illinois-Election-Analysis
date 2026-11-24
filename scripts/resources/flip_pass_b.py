"""Pass B (exact Fractions, independent code path): pass-B parses of the raw SBOE and county files."""
import csv,json
from fractions import Fraction as F
O='/workspace/il_publish/out/'
def load(f): 
    with open(O+f) as h: return {r['county_key']:r for r in csv.DictReader(h)}
a22=load('pass_b_2022.csv'); a26=load('pass_b_2026_raw.csv'); pp=load('pass_b_proxy.csv')
names={r['county_key']:(r['county'],r['pop_2020']) for r in csv.DictReader(open(O+'surplus_pass_b.csv'))} if 'county' in open(O+'surplus_pass_b.csv').readline() else {}
out={}
for k in sorted(a26):
    D22=F(a22[k]['dem_votes']); D26=F(a26[k]['dem_votes']); B22=F(a22[k]['ballots_cast']); B26=F(a26[k]['ballots_cast'])
    P22=F(pp[k]['gp2022_dem_ballots']); P26=F(pp[k]['gp2026_dem_ballots']); T22=F(pp[k]['gp2022_total_ballots']); T26=F(pp[k]['gp2026_total_ballots'])
    r22=100*P22/T22; r26=100*P26/T26; s22=100*D22/B22; s26=100*D26/B26
    rd=lambda x:round(float(x),6)
    out[k]=dict(R22=rd(r22),R26=rd(r26),S22=rd(s22),S26=rd(s26),dR=rd(r26-r22),dS=rd(s26-s22),dG=rd((s26-r26)-(s22-r22)),
        ks_value=rd(D26-D22*P26/P22),share_value=rd(D26-B26*(s22/100)*(r26/r22)),ks_test=bool(P26<P22 and D26>D22),share_test=bool(r26<r22 and s26>s22),
        d22=int(D22),d26=int(D26),B26=int(B26),pd22=int(P22),pd26=int(P26))
json.dump(out,open('/workspace/il-resources/out/flip_pass_b.json','w'),indent=1,sort_keys=True)
print(len(out))
