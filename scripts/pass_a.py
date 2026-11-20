"""PASS A — stdlib only. Votes: raw/2022GECty.txt (tab-delimited, csv module).
Ballots cast: pdftotext -layout of raw/2022GEOfficialVote.pdf, page ii, regex parse.
Arithmetic: fractions.Fraction (exact), rounded with Decimal ROUND_HALF_EVEN at output."""
import csv, re, subprocess, json
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_EVEN
RAW='/workspace/illinois/raw/'
def key(n): return re.sub(r'[^A-Z]','',n.upper())
def q(fr,places=6):
    d=Decimal(fr.numerator)/Decimal(fr.denominator)
    return str(d.quantize(Decimal(1).scaleb(-places),rounding=ROUND_HALF_EVEN))
# votes
dem,rep,oth={}, {}, {}
with open(RAW+'2022GECty.txt',newline='',encoding='latin-1') as f:
    for r in csv.DictReader(f,delimiter='\t'):
        if r['OfficeName'].strip()!='GOVERNOR AND LIEUTENANT GOVERNOR': continue
        k=key(r['County']); v=int(r['Votes'])
        p=r['PartyAbbrev'].strip()
        tgt=dem if p=='DEM' else rep if p=='REP' else oth
        tgt[k]=tgt.get(k,0)+v
        oth.setdefault(k,0); dem.setdefault(k,0); rep.setdefault(k,0)
# ballots
txt=subprocess.run(['pdftotext','-layout','-f','1','-l','6',RAW+'2022GEOfficialVote.pdf','-'],capture_output=True,text=True).stdout
i=txt.index('Total Ballots Cast',txt.index('Total Voters Registered',txt.index('Total Voters Registered')+5))
block=txt[i:txt.index('CONSTITUTIONAL AMENDMENT',i)]
ballots={}
for line in block.splitlines():
    for name,num in re.findall(r'([A-Za-z][A-Za-z. ]*?)\s+(\d{1,3}(?:,\d{3})*)(?=\s|$)',line):
        if name.strip() in ('Total Ballots Cast','County','Ballots'): continue
        ballots[key(name)]=int(num.replace(',',''))
stated_total=int(re.search(r'Total Ballots Cast\s+([\d,]+)',block).group(1).replace(',',''))
assert len(ballots)==102, len(ballots)
assert sum(ballots.values())==stated_total,(sum(ballots.values()),stated_total)
assert set(ballots)==set(dem), set(ballots)^set(dem)
rows=[]
for k in sorted(ballots):
    b=ballots[k]; d=dem[k]; r=rep[k]; o=oth[k]
    rows.append(dict(county_key=k,year='2022',dem_votes=d,rep_votes=r,other_votes=o,gov_total=d+r+o,ballots_cast=b,
        dem_share=q(Fraction(d,b)),rep_share=q(Fraction(r,b)),dem_plus_rep=d+r,
        over_ballot=str(d+r>b),gov_undervote=b-(d+r+o)))
with open('/workspace/illinois/out/pass_a_2022.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('pass A rows',len(rows),'ballots total',stated_total,'dem',sum(dem.values()),'rep',sum(rep.values()))
