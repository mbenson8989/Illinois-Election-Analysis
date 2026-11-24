"""Pass 1 (pandas): Illinois voting equipment, 108 election authorities, from Verified Voting public CSV export (state FIPS 17)."""
import pandas as pd, json
RAW='/workspace/il-resources/raw/vv/'
TAB=['Hand-Fed Optical Scanner','Batch-Fed Optical Scanner','Hybrid BMD/Tabulator']
def load(y):
    m=pd.read_csv(RAW+f'vv{y}/verifier-machines.csv',skiprows=1,dtype=str,index_col=False,keep_default_na=False)
    j=pd.read_csv(RAW+f'vv{y}/verifier-jurisdictions.csv',skiprows=1,dtype=str,index_col=False,keep_default_na=False)
    return m,j
m26,j26=load(2026); m22,j22=load(2022)
eq=lambda r:f"{r.Manufacturer} {r.Model} ({r['Equipment Type']})"
pop=pd.read_csv('/workspace/il_publish/out/il_2022_governor_by_county_VERIFIED.csv',dtype={'fips':str}).set_index('fips')
rows=[]
for _,jr in j26.iterrows():
    name=jr.Jurisdiction; fid=jr['FIPS code']; g=m26[m26['FIPS code']==fid]
    is_c=name.endswith(' County'); c=pop.loc[fid[:5],'county'] if is_c else name.split(' (')[0]
    if is_c: assert c.replace(' ','').lower()[:5]==name[:-7].replace(' ','').lower()[:5],(c,name)
    ed=g[(g['Election Day Standard']=='Yes')&g['Equipment Type'].isin(TAB)]
    mail=g[(g['Mail Ballot/Absentee Equipment']=='Yes')&g['Equipment Type'].isin(TAB)]
    acc=g[(g['Election Day Accessible']=='Yes')&g['Equipment Type'].isin(['Ballot Marking Device','Hybrid BMD/Tabulator','DRE-Touchscreen'])]
    pb=g[g['Equipment Type'].str.contains('Poll Book')]
    ed22=m22[(m22['FIPS code']==fid)&(m22['Election Day Standard']=='Yes')&m22['Equipment Type'].isin(TAB)]
    vv=sorted(set(g[g['Equipment Type'].isin(TAB+['Ballot Marking Device'])].VVPAT))
    s26=sorted(set(eq(r) for _,r in ed.iterrows())); s22=sorted(set(eq(r) for _,r in ed22.iterrows()))
    k26=sorted(set((r.Model,r['Equipment Type']) for _,r in ed.iterrows())); k22=sorted(set((r.Model,r['Equipment Type']) for _,r in ed22.iterrows()))
    notes=[]
    if not len(m22[m22['FIPS code']==fid]): notes.append('No 2022 Verified Voting record for this jurisdiction.')
    elif not s22: notes.append("Verified Voting's 2022 record lists no election-day tabulator, so no 2022 comparison is possible.")
    elif k26!=k22: notes.append('Election-day tabulator equipment changed from 2022: '+('; '.join(s22) if s22 else '(none listed)')+'.')
    elif s26!=s22: notes.append('Same election-day tabulator model as 2022; manufacturer name changed in Verified Voting from '+'/'.join(sorted(set(ed22.Manufacturer)))+' to '+'/'.join(sorted(set(ed.Manufacturer)))+'.')
    if len(ed) and (ed['Equipment Type']=='Batch-Fed Optical Scanner').all(): notes.append('Election-day ballots are tabulated on a batch-fed (central-count) scanner.')
    if (ed['Equipment Type']=='Hybrid BMD/Tabulator').any(): notes.append('Uses a hybrid ballot-marking device/tabulator on election day.')
    if len(set(ed.Manufacturer))>1: notes.append('More than one election-day tabulator vendor listed.')
    rows.append({'Jurisdiction':c,'Type':'County' if is_c else 'Municipal board of election commissioners','VV FIPS code':fid,
        'Population 2020':int(pop.loc[fid[:5],'pop_2020']) if is_c else '', 'Registered voters (VV)':int(jr['Registered Voters']),
        'Marking method':jr['Election Day Marking Method'],'ED tabulator vendor':'; '.join(sorted(set(ed.Manufacturer))) or 'Not listed',
        'ED tabulator equipment':'; '.join(s26) or 'Not listed','Mail tabulator equipment':'; '.join(sorted(set(eq(r) for _,r in mail.iterrows()))) or 'Not listed',
        'Accessible device':'; '.join(sorted(set(eq(r) for _,r in acc.iterrows()))) or 'Not listed',
        'Paper record / VVPAT':'VVPAT: '+('/'.join(vv) if vv else 'not listed')+(' (Verified Voting does not list a VVPAT for these systems)' if vv==['N/A'] else ''),
        'Software/firmware':'Not listed by Verified Voting',
        'Poll book':'; '.join(sorted(set(f"{r.Manufacturer} {r.Model}".strip() if r.Manufacturer not in ('','Not Applicable') else r['Equipment Type'] for _,r in pb.iterrows()))) or 'Not listed',
        'ED tabulator equipment 2022':'; '.join(s22) or 'Not listed','Status':'Confirmed (Verified Voting 2026 record)' if len(ed) else 'Unconfirmed',
        'Source':'https://verifiedvoting.org/verifier/#mode/navigate/map/ppEquip/mapType/normal/year/2026/state/17'+(f'/county/{fid[2:5]}' if is_c else ''),'Notes':' '.join(notes)})
o=pd.DataFrame(rows)
o['_k']=o['Population 2020'].replace('',-1).astype(int)
o=pd.concat([o[o.Type=='County'].sort_values('_k',ascending=False),o[o.Type!='County'].sort_values('Registered voters (VV)',ascending=False)]).drop(columns='_k').reset_index(drop=True)
assert len(o)==108 and (o.Type=='County').sum()==102
o.to_csv('/workspace/il_publish/IL_108_Authority_Voting_Equipment_VerifiedVoting.csv',index=False)
summ={}
for v,g in o.groupby('ED tabulator vendor'): summ[v]=dict(authorities=len(g),counties=int((g.Type=='County').sum()),registered=int(g['Registered voters (VV)'].sum()))
summ['_total_registered']=int(o['Registered voters (VV)'].sum()); summ['_n_confirmed']=int(o.Status.str.startswith('Confirmed').sum())
summ['_marking']=o['Marking method'].value_counts().to_dict(); summ['_poll']=o['Poll book'].value_counts().to_dict()
summ['_batch_only']=o[o.Notes.str.contains('batch-fed')].Jurisdiction.tolist(); summ['_changed']=o[o.Notes.str.contains('changed from 2022')].Jurisdiction.tolist()
summ['_renamed']=o[o.Notes.str.contains('manufacturer name changed')].Jurisdiction.tolist(); summ['_multi']=o[o.Notes.str.contains('More than one')].Jurisdiction.tolist()
summ['_hybrid']=o[o.Notes.str.contains('hybrid')].Jurisdiction.tolist(); summ['_no2022']=o[o.Notes.str.contains('No 2022')].Jurisdiction.tolist()
summ['_mail_missing']=int(o['Mail tabulator equipment'].eq('Not listed').sum()); summ['_acc_missing']=int(o['Accessible device'].eq('Not listed').sum())
json.dump(summ,open('/workspace/il-resources/out/equipment_summary_pass1.json','w'),indent=1); print(json.dumps(summ,indent=1))
