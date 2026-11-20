"""Compare pass A vs pass B cell-by-cell (exact string match), plus a third check of
Dem/Rep governor votes against the official canvass PDF governor table."""
import csv, re, subprocess, json
A=list(csv.DictReader(open('/workspace/illinois/out/pass_a_2022.csv')))
B=list(csv.DictReader(open('/workspace/illinois/out/pass_b_2022.csv')))
assert [r['county_key'] for r in A]==[r['county_key'] for r in B]
cols=[c for c in A[0] if c!='county_key']
match=mis=0; bad=[]
for a,b in zip(A,B):
    for c in cols:
        if a[c]==b[c]: match+=1
        else: mis+=1; bad.append((a['county_key'],c,a[c],b[c]))
# third check vs PDF governor table
txt=subprocess.run(['pdftotext','-layout','/workspace/illinois/raw/2022GEOfficialVote.pdf','-'],capture_output=True,text=True).stdout
s=txt.index('GOVERNOR AND LIEUTENANT GOVERNOR\n'); e=txt.index('ATTORNEY GENERAL',s)
pdfv={}
for line in txt[s:e].splitlines():
    m=re.match(r'^([A-Za-z][A-Za-z. ]*?)\s+[\d,]+\((?:DEM|REP)\)\s+([\d,]+)\s+([\d,]+)',line)
    if m and re.sub(r'[^A-Z]','',m.group(1).upper()) not in pdfv: pdfv[re.sub(r'[^A-Z]','',m.group(1).upper())]=(int(m.group(2).replace(',','')),int(m.group(3).replace(',','')))
pdf_match=pdf_mis=0
for a in A:
    d,r=pdfv[a['county_key']]
    for x,y in ((d,int(a['dem_votes'])),(r,int(a['rep_votes']))):
        if x==y: pdf_match+=1
        else: pdf_mis+=1; bad.append((a['county_key'],'pdf_gov_table',x,y))
rep=dict(counties=len(A),columns_compared=len(cols),cells_compared=match+mis,matched=match,mismatched=mis,
         pdf_gov_table_counties=len(pdfv),pdf_cells_matched=pdf_match,pdf_cells_mismatched=pdf_mis,mismatches=bad[:50],
         ship=(mis==0 and pdf_mis==0 and len(pdfv)==102))
json.dump(rep,open('/workspace/illinois/out/verification_2022.json','w'),indent=1)
print(json.dumps({k:v for k,v in rep.items() if k!='mismatches'}),bad[:5])
