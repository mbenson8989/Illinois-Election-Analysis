"""Pass A (float): Illinois flip test, Kansas Resources definition adapted to the stand-in. Inputs: verified pass-A outputs."""
import csv,json
O='/workspace/il_publish/out/'
ne={r['county_key']:r for r in csv.DictReader(open(O+'ne_format_pass_a.csv'))}
px={r['county_key']:r for r in csv.DictReader(open(O+'proxy_primary_pass_a.csv'))}
g22={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2022.csv'))}
g26={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2026_raw.csv'))}
res={}
for k,n in ne.items():
    p=px[k]; a=g22[k]; b=g26[k]
    d22,d26=int(a['dem_votes']),int(b['dem_votes']); B22,B26=int(a['ballots_cast']),int(b['ballots_cast'])
    pd22,pd26=int(p['gp2022_dem_ballots']),int(p['gp2026_dem_ballots']); pt22,pt26=int(p['gp2022_total_ballots']),int(p['gp2026_total_ballots'])
    R22=100*pd22/pt22; R26=100*pd26/pt26; S22=100*d22/B22; S26=100*d26/B26
    ks_value=d26-d22*(pd26/pd22)                 # Kansas formula, headcount stand-in
    share_value=d26-B26*(S22/100)*(R26/R22)      # share adaptation
    res[n['county']]=dict(key=k,pop=int(n['pop_2020']),d22=d22,d26=d26,B22=B22,B26=B26,pd22=pd22,pd26=pd26,R22=round(R22,6),R26=round(R26,6),S22=round(S22,6),S26=round(S26,6),
        dR=round(R26-R22,6),dS=round(S26-S22,6),dG=round((S26-R26)-(S22-R22),6),ks_value=round(ks_value,6),share_value=round(share_value,6),
        ks_test=(pd26<pd22 and d26>d22), share_test=(R26<R22 and S26>S22))
json.dump(res,open('/workspace/il-resources/out/flip_pass_a.json','w'),indent=1,sort_keys=True)
print('ks_test',[c for c,v in res.items() if v['ks_test']]); print('share_test',sorted([(c,v['share_value']) for c,v in res.items() if v['share_test']],key=lambda x:-x[1]))
