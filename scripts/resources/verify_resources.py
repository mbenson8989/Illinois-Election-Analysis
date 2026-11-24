"""Pass 2: independent checks of everything on the Resources page (csv module, no pandas)."""
import csv,json,re,os,glob
P='/workspace/il_publish/'; R='/workspace/il-resources/'; O=P+'out/'
res={}; fails=[]
def chk(name,cond,detail=''):
    res.setdefault(name,[0,0]); res[name][0]+=1
    if not cond: res[name][1]+=1; fails.append((name,detail))
# 1 equipment
def rd(f):
    L=list(csv.reader(open(f))); h=L[1]; return [dict(zip(h,r)) for r in L[2:] if r and r[0]]
mach=rd(R+'raw/vv/vv2026/verifier-machines.csv'); jur=rd(R+'raw/vv/vv2026/verifier-jurisdictions.csv')
TAB={'Hand-Fed Optical Scanner','Batch-Fed Optical Scanner','Hybrid BMD/Tabulator'}
mine={r['VV FIPS code']:r for r in csv.DictReader(open(P+'IL_108_Authority_Voting_Equipment_VerifiedVoting.csv'))}
chk('equipment rows',len(mine)==108==len(jur))
vend={}
for j in jur:
    fid=j['FIPS code']; ms=[m for m in mach if m['FIPS code']==fid]
    ed=[m for m in ms if m['Election Day Standard']=='Yes' and m['Equipment Type'] in TAB]
    mail=[m for m in ms if m['Mail Ballot/Absentee Equipment']=='Yes' and m['Equipment Type'] in TAB]
    s=lambda xs:'; '.join(sorted({f"{m['Manufacturer']} {m['Model']} ({m['Equipment Type']})" for m in xs})) or 'Not listed'
    r=mine[fid]
    for col,val in [('ED tabulator equipment',s(ed)),('Mail tabulator equipment',s(mail)),('ED tabulator vendor','; '.join(sorted({m['Manufacturer'] for m in ed})) or 'Not listed'),('Registered voters (VV)',j['Registered Voters']),('Marking method',j['Election Day Marking Method'])]:
        chk('equipment cells',r[col]==val,(fid,col,r[col],val))
    v='; '.join(sorted({m['Manufacturer'] for m in ed})); vend.setdefault(v,[0,0,0]); vend[v][0]+=1; vend[v][1]+=j['Jurisdiction'].endswith(' County'); vend[v][2]+=int(j['Registered Voters'])
page=open(P+'wiki/Resources.md').read()
for v,(na,nc,reg) in vend.items():
    chk('vendor summary',f'**{v}:** {na} election authorities ({nc} counties' in page and f'{reg:,} registered voters' in page,(v,na,nc,reg))
pops=[int(r['Population 2020']) for r in mine.values() if r['Type']=='County']
chk('equipment sort',pops==sorted(pops,reverse=True))
# table rows on page
for r in mine.values(): chk('equipment table rows on page',f"| {r['Jurisdiction']} | " in page and r['ED tabulator equipment'] in page,r['Jurisdiction'])
# 2 letters vs pass B
b22={r['county_key']:r for r in csv.DictReader(open(O+'pass_b_2022.csv'))}; b26={r['county_key']:r for r in csv.DictReader(open(O+'pass_b_2026_raw.csv'))}; bp={r['county_key']:r for r in csv.DictReader(open(O+'pass_b_proxy.csv'))}
EA={r['jurisdiction']:r for r in csv.DictReader(open(R+'raw/sboe/election_authorities_RETRIEVED.csv'))}
mf=list(csv.DictReader(open(R+'out/letter_merge_fields.csv'))); chk('letter count',len(mf)==108)
keymap={r['county']:r['county_key'] for r in csv.DictReader(open(O+'il_governor_reverse_math_2022_2026_VERIFIED.csv'))}
for r in mf:
    md=open(R+f"letters/clerk/md/{r['file']}.md").read(); k=keymap[r['county']]
    num=lambda x:f"{int(x):,}"
    chk('letter figures',f"{num(bp[k]['gp2022_dem_ballots'])} → {num(bp[k]['gp2026_dem_ballots'])}" in md,(r['file'],'primary'))
    R22=100*int(bp[k]['gp2022_dem_ballots'])/int(bp[k]['gp2022_total_ballots']); R26=100*int(bp[k]['gp2026_dem_ballots'])/int(bp[k]['gp2026_total_ballots'])
    chk('letter figures',f"{R22:.2f}% → {R26:.2f}%" in md,(r['file'],'share'))
    if k in b26:
        chk('letter figures',f"{num(b22[k]['dem_votes'])} → {num(b26[k]['dem_votes'])}*" in md,(r['file'],'dem'))
        chk('letter figures',f"{num(b22[k]['ballots_cast'])} → {num(b26[k]['ballots_cast'])}*" in md,(r['file'],'ballots'))
    else: chk('letter figures',f"Democratic votes for governor, 2022: {num(b22[k]['dem_votes'])}" in md and 'not included' in md,(r['file'],'no26'))
    e=EA[r['jurisdiction']]; chk('letter addressee',e['name'].lower() in md.lower().split('\n')[4].lower() or e['name'].lower()==md.split('\n')[4].lower(),(r['file'],e['name'],md.split('\n')[4]))
    zipc=re.search(r'IL (\d{5})',e['address']).group(1); chk('letter address zip',f'IL {zipc}' in md,(r['file'],zipc))
    for f_ in [R+f"letters/clerk/PDF/{r['file']}.pdf",R+f"letters/clerk/Word/{r['file']}.docx"]: chk('letter files exist',os.path.getsize(f_)>5000,f_)
import zipfile
for z in glob.glob(P+'downloads/*.zip'):
    names=zipfile.ZipFile(z).namelist(); chk('zip integrity',zipfile.ZipFile(z).testzip() is None and len([n for n in names if n.startswith('PDF/')])==len([n for n in names if n.startswith('Word/')]),z)
allz=zipfile.ZipFile(P+'downloads/Illinois_Election_Authority_Letters_All_108.zip').namelist(); chk('zip all count',len(allz)==216,len(allz))
regs=[n for z in glob.glob(P+'downloads/*Region_*.zip') for n in zipfile.ZipFile(z).namelist()]; chk('regional zips cover all once',sorted(regs)==sorted(allz),len(regs))
# 3 flip numbers on page vs pass B
FB=json.load(open(R+'out/flip_pass_b.json'))
q=[(k,v) for k,v in FB.items() if v['share_test']]; chk('flip qualifier count',len(q)==4 and sum(v['ks_test'] for v in FB.values())==0)
for k,v in q:
    chk('flip page values',f"**+{round(v['share_value']):,}\\*" in page and f"{v['R22']:.2f}% → {v['R26']:.2f}%" in page and f"{v['S22']:.2f}% → {v['S26']:.2f}%" in page,k)
man=json.load(open(R+'out/flip_manifest.json'))
for m in man: chk('flip graphic files',os.path.exists(P+'resources/'+m['file']),m['file'])
# 4 links
for f in ['wiki/Resources.md','wiki/Home.md','wiki/_Sidebar.md']:
    t=open(P+f).read()
    for u in re.findall(r'https://(?:raw\.githubusercontent\.com/mbenson8989/Illinois-Election-Analysis/main/|github\.com/mbenson8989/Illinois-Election-Analysis/blob/main/)([^)\s]+)',t):
        chk('repo links resolve to files',os.path.exists(P+u),u)
    for u in re.findall(r'\]\(([A-Za-z-]+)\)',t): chk('wiki page links',os.path.exists(P+'wiki/'+u+'.md'),u)
# 5 post
post=page.split('**Post text: DRAFT, NOT POSTED')[1].split('> ')[1].split('\n')[0]; chk('post <=280',len(post)<=280,len(post))
chk('post matches social file',post in open(P+'social/guarantee_clause_post.md').read())
chk('stand-in label on page',page.count('NOT official party registration')>=3); chk('unofficial label',page.count('UNOFFICIAL')>=2)
chk('cedar link trailing hyphen','https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit' in page)
for s in ['the-back-room','who-holds-the-keys','the-election-equation-and-plan']: chk('substack links',f'https://moebenson.substack.com/p/{s}' in page and os.path.exists(R+f'raw/substack/{s}.html'))
H=[l for l in page.split('\n') if l.startswith('## ')]
exp=['## Letter to the Illinois Attorney General','## County clerk letters','## Illinois State Board of Elections data sources','## County-level results','## Voting equipment by county','## Graphics','## Where the method began: the Cedar County audit','## The reverse-factoring method in brief','## Illinois laws cited in the Attorney General letter','## Federal sources cited','## Morissa Benson on Substack']
chk('section order',H==exp,H)
tot=sum(v[0] for v in res.values()); bad=sum(v[1] for v in res.values())
json.dump(dict(checks=res,total=tot,failed=bad,fails=fails[:50]),open(R+'out/verify_resources_pass2.json','w'),indent=1)
for k,v in res.items(): print(f'{k}: {v[0]-v[1]}/{v[0]}')
print('TOTAL',tot-bad,'/',tot); print(fails[:10])
