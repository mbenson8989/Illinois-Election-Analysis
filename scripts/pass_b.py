"""PASS B — independent code path. Votes: raw/2022GECty.xls (Excel binary, xlrd via pandas).
Ballots cast: pdfplumber word-extraction of raw/2022GEOfficialVote.pdf (token walk, no regex on layout text).
Arithmetic: numpy float64, formatted with format(x,'.6f')."""
import pandas as pd, numpy as np, pdfplumber
RAW='/workspace/illinois/raw/'
norm=lambda s: ''.join(ch for ch in str(s).upper() if 'A'<=ch<='Z')
df=pd.read_excel(RAW+'2022GECty.xls',engine='xlrd')
g=df[df['OfficeName'].astype(str).str.strip()=='GOVERNOR AND LIEUTENANT GOVERNOR'].copy()
g['k']=g['County'].map(norm); g['p']=g['PartyAbbrev'].fillna('').astype(str).str.strip()
g['Votes']=g['Votes'].astype('int64')
piv=g.assign(cls=np.select([g.p=='DEM',g.p=='REP'],['dem','rep'],'oth')).pivot_table(index='k',columns='cls',values='Votes',aggfunc='sum',fill_value=0)
ballots=None
with pdfplumber.open(RAW+'2022GEOfficialVote.pdf') as pdf:
    for page in pdf.pages[:8]:
        t=page.extract_text() or ''
        if 'County Ballots County Ballots' in t:
            words=page.extract_words(keep_blank_chars=False)
            lines={}
            for w in words: lines.setdefault(round(w['top']),[]).append(w)
            cand={}; total=None; in_table=False
            for top in sorted(lines):
                toks=[w['text'] for w in sorted(lines[top],key=lambda w:w['x0'])]
                if toks[:2]==['Total','Ballots']: total=int(toks[3].replace(',','')); continue
                if toks[0] in ('County','Ballots') and set(toks)<={'County','Ballots'}: in_table=True; continue
                if not in_table: continue
                name=[]
                for tk in toks:
                    s=tk.replace(',','')
                    if s.isdigit():
                        nm=' '.join(name)
                        if nm=='Total Ballots Cast': total=int(s)
                        elif nm and nm not in('Total Voters Registered',): cand[norm(nm)]=int(s)
                        name=[]
                    elif tk.endswith('%'): name=[]
                    else: name.append(tk)
            if len(cand)==102 and total: ballots=cand; stated=total; break
assert ballots is not None
assert sum(ballots.values())==stated
assert set(ballots)==set(piv.index)
out=pd.DataFrame({'county_key':sorted(ballots)})
out['year']='2022'
for c in ['dem','rep','oth']: out[c]=out.county_key.map(piv[c]).astype('int64')
out['ballots_cast']=out.county_key.map(ballots).astype('int64')
res=pd.DataFrame({'county_key':out.county_key,'year':out.year,'dem_votes':out.dem,'rep_votes':out.rep,'other_votes':out.oth,
  'gov_total':out.dem+out.rep+out.oth,'ballots_cast':out.ballots_cast,
  'dem_share':[format(x,'.6f') for x in out.dem/out.ballots_cast],
  'rep_share':[format(x,'.6f') for x in out.rep/out.ballots_cast],
  'dem_plus_rep':out.dem+out.rep,'over_ballot':(out.dem+out.rep>out.ballots_cast).map(str),
  'gov_undervote':out.ballots_cast-(out.dem+out.rep+out.oth)})
res.to_csv('/workspace/illinois/out/pass_b_2022.csv',index=False)
print('pass B rows',len(res),'ballots',stated,'dem',res.dem_votes.sum(),'rep',res.rep_votes.sum())
