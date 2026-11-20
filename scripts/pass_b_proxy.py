"""PASS B for the registration STAND-IN (primary ballot pulls): pdfplumber word tokens, token walk (Pass A used pdftotext+regex)."""
import pdfplumber, re, csv
RAW='/workspace/illinois/raw/'
norm=lambda s:''.join(ch for ch in s.upper() if 'A'<=ch<='Z')
def tables(f):
    res={}
    with pdfplumber.open(f) as pdf:
        for p in pdf.pages[:12]:
            words=p.extract_words(); rows={}
            for w in words: rows.setdefault(round(w['top']/2),[]).append(w)
            lines=[[w['text'] for w in sorted(rows[k],key=lambda w:w['x0'])] for k in sorted(rows)]
            label=None; stated=None
            for l in lines:
                j=' '.join(l)
                m=re.match(r'Total Ballots (DEMOCRATIC|REPUBLICAN) ([\d,]+)',j) or re.fullmatch(r'Total Ballots (Cast) ([\d,]+) [\d.]+%',j)
                if m: label={'Cast':'TOTAL'}.get(m.group(1),m.group(1)); stated=int(m.group(2).replace(',',''))
            if label is None: continue
            if label in res: continue
            d={}; started=False
            for l in lines:
                if l and all(x=='Ballots' for x in l): started=True; continue
                if not started: continue
                name=[]
                for tk in l:
                    if re.fullmatch(r'[\d,]+',tk):
                        if name: d[norm(' '.join(name))]=int(tk.replace(',',''))
                        name=[]
                    else: name.append(tk)
            if len(d)==102: res[label]=(d,stated)
    return res
out={}
for yr,f in (('2022','2022GPOfficialVote.pdf'),('2026','2026GPOfficialVote.pdf')):
    T=tables(RAW+f); assert set(T)=={'DEMOCRATIC','REPUBLICAN','TOTAL'},(yr,list(T))
    for lab,(d,s) in T.items(): assert sum(d.values())==s,(yr,lab)
    for k in T['TOTAL'][0]: out.setdefault(k,{})[yr]=(T['DEMOCRATIC'][0][k],T['REPUBLICAN'][0][k],T['TOTAL'][0][k])
with open('/workspace/illinois/out/pass_b_proxy.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['county_key','gp2022_dem_ballots','gp2022_rep_ballots','gp2022_total_ballots','gp2022_dem_pct_of_total','gp2026_dem_ballots','gp2026_rep_ballots','gp2026_total_ballots','gp2026_dem_pct_of_total'])
    for k in sorted(out):
        a=out[k]['2022']; b=out[k]['2026']; w.writerow([k,*a,format(a[0]/a[2],'.6f'),*b,format(b[0]/b[2],'.6f')])
print(len(out))
