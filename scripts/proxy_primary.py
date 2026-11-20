"""Documented PROXY CANDIDATE ONLY (not used in any computation): party ballots pulled in the
General Primary, by county, from SBOE official canvass PDFs. Single parse with checksum vs stated statewide total."""
import re, csv
RAW='/workspace/illinois/raw/'
key=lambda n: re.sub(r'[^A-Z]','',n.upper())
def block(txt,label):
    i=txt.index(f'Total Ballots {label}')
    stated=int(re.search(rf'Total Ballots {label}\s+([\d,]+)',txt[i:]).group(1).replace(',',''))
    j=txt.index('County',i); end=re.search(r'\n\s+[ivx]+\s*\n',txt[j:]).start()+j
    d={}
    for line in txt[j:end].splitlines():
        for n,v in re.findall(r'([A-Za-z][A-Za-z. ]*?)\s+(\d{1,3}(?:,\d{3})*)(?=\s|$)',line):
            d[key(n)]=int(v.replace(',',''))
    assert len(d)==102,(label,len(d)); assert sum(d.values())==stated,(label,sum(d.values()),stated)
    return d,stated
def total_block(txt):
    i=txt.index('Total Ballots Cast',txt.index('Total Voters Registered',txt.index('Total Voters Registered')+5))
    stated=int(re.search(r'Total Ballots Cast\s+([\d,]+)',txt[i:]).group(1).replace(',',''))
    j=txt.index('County',i); end=re.search(r'\n\s+[ivx]+\s*\n',txt[j:]).start()+j
    d={}
    for line in txt[j:end].splitlines():
        for n,v in re.findall(r'([A-Za-z][A-Za-z. ]*?)\s+(\d{1,3}(?:,\d{3})*)(?=\s|$)',line): d[key(n)]=int(v.replace(',',''))
    assert len(d)==102 and sum(d.values())==stated; return d,stated
rows={}
summary=[]
for yr,f in (('2022','gp22.txt'),('2026','gp26.txt')):
    t=open(RAW+f).read()
    D,ds=block(t,'DEMOCRATIC'); R,rs=block(t,'REPUBLICAN'); T,ts=total_block(t)
    summary.append((yr,ds,rs,ts))
    for k in D: rows.setdefault(k,{})[yr]=(D[k],R[k],T[k])
with open('/workspace/illinois/out/proxy_primary_pass_a.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['county_key','gp2022_dem_ballots','gp2022_rep_ballots','gp2022_total_ballots','gp2022_dem_pct_of_total',
                                  'gp2026_dem_ballots','gp2026_rep_ballots','gp2026_total_ballots','gp2026_dem_pct_of_total'])
    for k in sorted(rows):
        a=rows[k]['2022']; b=rows[k]['2026']
        w.writerow([k,*a,f'{a[0]/a[2]:.6f}',*b,f'{b[0]/b[2]:.6f}'])
print(summary)
