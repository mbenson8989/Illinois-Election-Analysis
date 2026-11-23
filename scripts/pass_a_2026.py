"""PASS A 2026 (UNOFFICIAL): regex over text. HTML->text via re; PDFs via pdftotext -layout; JSON via json module."""
import re, json, subprocess, html, csv, sys
sys.path.insert(0,'/workspace/illinois/scripts')
from manifest_2026 import M
num=lambda s:int(s.replace(',','').replace('.',''))
def htxt(f):
    t=open(f,encoding='utf-8',errors='replace').read()
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    return [x.strip() for x in html.unescape(re.sub(r'<[^>]+>','\n',t)).splitlines() if x.strip()]
def ptxt(f): return subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True,text=True).stdout
def p_voteclock(f):
    s=re.sub(r'\s+',' ',' '.join(htxt(f)))
    b=num(re.search(r'Turnout: ([\d,]+) ballots cast',s).group(1))
    g=s[s.index('Governor and Lieutenant Governor Candidate'):]
    g=g[:g.index('U.S. Representative') if 'U.S. Representative' in g else 600]
    d=num(re.search(r'JB\s+Pritzker\s+and\s+Christian\s+Mitchell\s+(?:DEM\s+|Democratic\s+|D\s+)?([\d,]+)',g).group(1))
    r=num(re.search(r'Darren\s+Bailey\s+and\s+Aaron\s+B\.\s+Del\s+Mar\s+(?:REP\s+|Republican\s+|R\s+)?([\d,]+)',g).group(1))
    m=re.search(r'current as of (.*?) \(',s); asof=m.group(1) if m else re.search(r'(when read on [^,]*, [A-Za-z]+ \d+, 2026|Turnout)',s,re.I).group(1)
    return d,r,b,asof
def p_pollresults(f):
    d=json.load(open(f)); e=d['Election']; st=e['ElectionStats'][e['OverallStatIndex']]
    race=[x for x in d['Races'] if 'GOVERNOR' in x['RaceName'].upper()][0]
    dem=sum(c['TotalVotesForCandidate'] for c in race['Candidates'] if c['CandidateName'].rstrip().endswith('(DEM)'))
    rep=sum(c['TotalVotesForCandidate'] for c in race['Candidates'] if c['CandidateName'].rstrip().endswith('(REP)'))
    return dem,rep,st['TotalBallotsCast'],e['UpdateTime']+' local; banner '+e['Message'].strip('*').split('*')[0]
def p_platinum(fs):
    T=htxt(fs[0]); b=num(T[T.index('Total Ballots Cast:')+1])
    L=htxt(fs[1]); i=[k for k,x in enumerate(L) if 'GOVERNOR' in x.upper()][0]
    seg=L[i:i+80]; out={}
    for k,x in enumerate(seg):
        if x in('D','R') and x not in out:
            # names then first number = candidate total
            for y in seg[k+1:k+5]:
                if re.fullmatch(r'[\d,]+',y): out[x]=num(y); break
    return out['D'],out['R'],b,'page fetch time (platinum shows no timestamp)'
def p_clarity(f):
    d=json.load(open(f)); c=[x for x in d['Contests'] if re.search(r'GOV',x['C'])][0]
    P=c['P']; V=c['V']
    dem=sum(v for p,v in zip(P,V) if p.upper().startswith('DEM')); rep=sum(v for p,v in zip(P,V) if p.upper().startswith('REP'))
    return dem,rep,c['BC'],'Clarity ENR current version at fetch'
def p_cumpdf(f):
    t=ptxt(f)
    b=num(re.search(r'(\d+) of \d+ = [\d.]+%',t).group(1))
    g=t[t.index('FOR GOVERNOR AND LIEUTENANT GOVERNOR'):]; g=g[:g.index('Cast Votes')]
    tot=lambda pat: num(re.search(pat+r'.*?([\d,]+)\s+[\d.]+%\s*$',g,re.I|re.M).group(1))
    rd=re.search(r'Run Date\s+(\S+)',t).group(1); rt=re.search(r'Run Time\s+([\d:]+ [AP]M)',t).group(1)
    stat='Official Results' if 'Official Results' in t.split('\n')[0] else 'Unofficial Results'
    return tot(r'\(JB Pritzker'),tot(r'\(Darren Bailey'),b,f'run {rd} {rt}; header "{stat}"'
def p_el45(f):
    t='\n'.join(htxt(f)) if f.endswith('.html') else open(f,errors='replace').read()
    b=num(re.search(r'BALLOTS CAST - TOTAL[ .]*?([\d,]+)',t).group(1))
    g=t[re.search(r'\n\s*GOVERNOR',t).start():] if re.search(r'\n\s*GOVERNOR\s*\n',t) else t[t.index('GOV'):]
    d=num(re.search(r'Pritzker[^\n]*?\(DEM\)[ .]*?([\d,]+)',g).group(1)); r=num(re.search(r'Bailey[^\n]*?\(REP\)[ .]*?([\d,]+)',g).group(1))
    rd=re.search(r'RUN DATE:(\S+)',t).group(1); rt=re.search(r'RUN TIME:([\d:]+ [AP]M)',t).group(1)
    return d,r,b,f'run {rd} {rt}; UNOFFICIAL RESULTS'
def p_chicago(f):
    t=ptxt(f)
    b=num(re.search(r'Total Registration and Turnout\s+[\d,]+\s+([\d,]+)',t).group(1))
    d=num(re.search(r'DEM - JB Pritzker & Christian Mitchell\s+([\d,]+)',t).group(1)); r=num(re.search(r'REP - Darren Bailey & Aaron B\. Del Mar\s+([\d,]+)',t).group(1))
    return d,r,b,'CHI 20261103 Ver D, "Summary Report - Unofficial Results"'
def p_radio_wmix(f):
    L=htxt(f); b=num(L[L.index('Total Ballots Cast')+1]); i=L.index('Governor')
    d=num(L[[k for k in range(i,i+20) if 'Pritzker' in L[k]][0]+1]); r=num(L[[k for k in range(i,i+20) if 'Bailey' in L[k]][0]+1])
    return d,r,b,'WMIX page, "Unofficial", Nov 3 2026'
def p_radio_webq_a(f):
    L=htxt(f); b=num(L[L.index('Ballots Cast:')+1]); i=[k for k,x in enumerate(L) if x.startswith('Governor')][0]
    d=num(L[[k for k in range(i,i+20) if 'Pritzker' in L[k]][0]+1]); r=num(L[[k for k in range(i,i+20) if 'Bailey' in L[k]][0]+1])
    return d,r,b,'WEBQ page, "Unofficial Results", Nov 3 2026'
def p_radio_webq_b(f):
    L=htxt(f); b=num(re.search(r'([\d,]+) ballots cast',' '.join(L)).group(1)); i=[k for k,x in enumerate(L) if x.startswith('Governor and Lieutenant')][0]
    def after(name):
        k=[k for k in range(i,i+30) if name in L[k]][0]
        return num([y for y in L[k+1:k+4] if re.fullmatch(r'[\d,]+',y)][0])
    return after('Pritzker'),after('Bailey'),b,'WEBQ page, report printed Nov 3 2026 9:02 p.m., unofficial'
P={'voteclock':p_voteclock,'pollresults':p_pollresults,'platinum':p_platinum,'clarity':p_clarity,'cumpdf':p_cumpdf,'el45':p_el45,'chicago_pdf':p_chicago,
   'radio_wmix':p_radio_wmix,'radio_webq_a':p_radio_webq_a,'radio_webq_b':p_radio_webq_b}

def p_gbsvote(f):
    d=json.load(open(f)); g=[x for x in d['races'] if x['title'].upper().startswith('GOVERNOR')][0]
    dem=sum(c['votes'] for c in g['candidates'] if c['party']=='DEM'); rep=sum(c['votes'] for c in g['candidates'] if c['party']=='REP')
    return dem,rep,d['summary']['ballotsCast'],d['election']['lastUpdated']+' UTC; status '+d['election']['status']
def p_lvt_precinct_sum(f):
    L=htxt(f); b=num(L[L.index('Ballots Counted')+1]); dem=rep=0; n=0
    for k,x in enumerate(L):
        if x.startswith('Precinct:') and x.endswith('Contest: GOVERNOR & LIEUTENANT GOVERNOR'):
            n+=1; seg=L[k:k+20]
            dem+=num(seg[seg.index('Pritzker and Mitchell')+2]); rep+=num(seg[seg.index('Bailey and Del Mar')+2])
    assert n==int(L[L.index('Total Precincts')+1])
    return dem,rep,b,'sum of %d precinct rows; site updated %s'%(n,L[L.index('Website Updated:')+1])
def p_canvass_totals_pdf(f):
    pages=ptxt(f).split('\f'); gp=[p for p in pages if 'FOR GOVERNOR AND LIEUTENANT GOVERNOR' in p]
    tot=[l for p in gp for l in p.splitlines() if l.strip().startswith('Totals')]
    v=[num(x) for x in re.findall(r'[\d,]+(?=\s|$)',tot[0].split('Totals',1)[1])]
    rd=re.search(r'Run Date\s+(\S+)',gp[0]).group(1)
    return v[0],v[1],v[11],'canvass run date '+rd
def p_el45_pdf_text(f):
    t=ptxt(f); fx=lambda pat:num(re.search(pat+r'[ .]*\s+([\d,]+)',t).group(1))
    rd=re.search(r'RUN DATE\s*:\s*(\S+)',t).group(1)+' 9:32 PM (election night)'
    return fx(r'Pritzker and Mitchell \(DEM\)'),fx(r'Bailey and Del Mar \(REP\)'),fx(r'BALLOTS CAST - TOTAL\.'),'run date '+rd
def p_scan_el45(fs):
    """OCR rows (RapidOCR, 300 dpi): find label row, take the TOTAL VOTES column token (x within 820-960) on the same line."""
    O=json.load(open(fs[0]))
    def val(label):
        y=[o[1] for o in O if label in o[2]][0]
        c=[o[2] for o in O if abs(o[1]-y)<25 and 820<=o[0]<=960]
        return int(re.sub(r'[^0-9]','',c[0]))
    return val('Pritzker'),val('Bailey'),val('BALLOTS CAST - TOTAL'),'OCR of scanned OFFICIAL RESULTS run 11/19/26'
P.update({'gbsvote':p_gbsvote,'lvt_precinct_sum':p_lvt_precinct_sum,'canvass_totals_pdf':p_canvass_totals_pdf,'el45_pdf_text':p_el45_pdf_text,'scan_el45':p_scan_el45})
if __name__=='__main__':
    comp=[]; rows=[]
    for c in sorted(M):
        D=R_=B=0; auths=[]
        for auth,typ,f,url in M[c]:
            d,r,b,asof=P[typ](f); D+=d; R_+=r; B+=b
            comp.append(dict(county_key=c,authority=auth,source_type=typ,url=url,dem=d,rep=r,ballots=b,as_of=asof))
            auths.append(auth)
        rows.append(dict(county_key=c,year='2026',dem_votes=D,rep_votes=R_,ballots_cast=B))
    with open('/workspace/illinois/out/pass_a_2026_components.csv','w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(comp[0])); w.writeheader(); w.writerows(comp)
    with open('/workspace/illinois/out/pass_a_2026_raw.csv','w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    for x in comp: print(x['county_key'],x['source_type'],x['dem'],x['rep'],x['ballots'],'|',str(x['as_of'])[:60])
    print(len(rows))
