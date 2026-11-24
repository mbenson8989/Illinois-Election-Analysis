import csv,json,zipfile,os,shutil
R='/workspace/il-resources/'; P='/workspace/il_publish/'; D=P+'downloads/'; os.makedirs(D,exist_ok=True)
rows=list(csv.DictReader(open(R+'out/letter_merge_fields.csv'))); REG=json.load(open(R+'out/regions.json'))
shutil.copy(R+'letters/ag/Illinois_Attorney_General_Letter.pdf',P); shutil.copy(R+'letters/ag/Illinois_Attorney_General_Letter.docx',P)
def mk(name,rs):
    z=zipfile.ZipFile(D+name,'w',zipfile.ZIP_DEFLATED)
    for r in rs:
        z.write(R+f"letters/clerk/PDF/{r['file']}.pdf",f"PDF/{r['file']}.pdf"); z.write(R+f"letters/clerk/Word/{r['file']}.docx",f"Word/{r['file']}.docx")
    z.close(); return dict(file=name,letters=len(rs),counties=len({r['county'] for r in rs}),mb=round(os.path.getsize(D+name)/1e6,1))
info=[mk('Illinois_Election_Authority_Letters_All_108.zip',rows)]
slug={'Chicago & Cook County':'1_Chicago_and_Cook','Collar Counties':'2_Collar_Counties','Northern Illinois':'3_Northern','Western Illinois':'4_Western','Central Illinois':'5_Central','Southern Illinois':'6_Southern'}
for reg in REG: info.append(dict(region=reg,**mk(f'Illinois_Election_Authority_Letters_Region_{slug[reg]}.zip',[r for r in rows if r['region']==reg])))
with open(D+'Illinois_County_to_Region_Lookup.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['county','region','election_authorities_in_county','letter_files'])
    for reg,cs in REG.items():
        for c in sorted(cs):
            rr=[r for r in rows if r['county']==c]; w.writerow([c,reg,'; '.join(r['office'] for r in rr),'; '.join(r['file'] for r in rr)])
json.dump(info,open(R+'out/zip_info.json','w'),indent=1); print(json.dumps(info,indent=1))
assert sum(i['letters'] for i in info[1:])==108
