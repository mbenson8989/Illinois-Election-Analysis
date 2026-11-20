"""PASS B 2026 (UNOFFICIAL): independent code path. HTML via BeautifulSoup/lxml DOM; PDFs via pdfplumber words;
JSON via raw-text regex (no json module). Candidate identified by NAME (Pass A used party labels where possible)."""
import re, csv, sys
from bs4 import BeautifulSoup
import pdfplumber
sys.path.insert(0,'/workspace/illinois/scripts')
from manifest_2026 import M
N=lambda s:int(re.sub(r'[^\d]','',s))
def soup(f): return BeautifulSoup(open(f,encoding='utf-8',errors='replace').read(),'lxml')
def b_voteclock(f):
    s=soup(f)
    p=s.find(string=re.compile(r'Turnout:\s*[\d,]+\s+ballots'))
    b=N(re.search(r'Turnout:\s*([\d,]+)',p).group(1))
    h=[h for h in s.find_all('h3') if h.get_text(strip=True)=='Governor and Lieutenant Governor'][0]
    out={}
    for tr in h.find_next('table').find('tbody').find_all('tr'):
        td=[x.get_text(' ',strip=True) for x in tr.find_all('td')]
        if 'Pritzker' in td[0]: out['D']=N(td[-1])
        if 'Bailey' in td[0]: out['R']=N(td[-1])
    return out['D'],out['R'],b
def b_pollresults(f):
    t=open(f).read()
    oi=int(re.search(r'"OverallStatIndex":(\d+)',t).group(1))
    stats=re.findall(r'"TotalBallotsCast":(\d+|null)',t)
    b=int(stats[oi])
    g=t[t.index('GOVERNOR'):]; g=g[:g.index('"Reporting"')]
    cands=re.findall(r'"CandidateName":"([^"]*)","PercentVotesForCandidate":[^,]*,"TotalVotesForCandidate":(\d+)',g)
    D=sum(int(v) for n,v in cands if 'Pritzker' in n); R=sum(int(v) for n,v in cands if 'Bailey' in n)
    return D,R,b
def b_platinum(fs):
    s=soup(fs[0]); lab=s.find(string=re.compile(r'Total Ballots Cast:'))
    b=N(lab.find_parent().find_next(string=re.compile(r'\d')))
    s=soup(fs[1]); h=s.find(string=re.compile('GOVERNOR AND LIEUTENANT'))
    toks=[x for x in h.find_parent('h3').find_all_next(string=True) if x.strip()][:120]
    toks=[x.strip() for x in toks]
    def total(name):
        i=[k for k,x in enumerate(toks) if name in x][0]
        j=toks.index('Total',i)
        return N(toks[j+6])   # Total column = 6th value after the 'Total' header (ED,VBM,EV,Prov,Other,Total)
    return total('Pritzker'),total('Bailey'),b
def b_clarity(f):
    t=open(f).read()
    k=[m.start() for m in re.finditer(r'"C"\s*:\s*"[^"]*GOV',t)][0]
    seg=t[k:t.find('"C"',k+5)]
    P=re.findall(r'"([^"]*)"',re.search(r'"P"\s*:\s*\[(.*?)\]',seg).group(1)); V=[int(x) for x in re.findall(r'\d+',re.search(r'"V"\s*:\s*\[(.*?)\]',seg).group(1))]
    CH=re.findall(r'"([^"]*)"',re.search(r'"CH"\s*:\s*\[(.*?)\]',seg).group(1))
    D=sum(v for c,v in zip(CH,V) if 'Pritzker' in c); R=sum(v for c,v in zip(CH,V) if 'Bailey' in c)
    return D,R,int(re.search(r'"BC"\s*:\s*(\d+)',seg).group(1))
def pl_lines(f,pages=None):
    out=[]
    with pdfplumber.open(f) as pdf:
        for p in (pdf.pages if pages is None else pdf.pages[:pages]):
            rows={}
            for w in p.extract_words(): rows.setdefault(round(w['top']/2),[]).append(w)
            for k in sorted(rows): out.append([w['text'] for w in sorted(rows[k],key=lambda w:w['x0'])])
    return out
def b_cumpdf(f):
    L=pl_lines(f,2)
    hdr=[l for l in L if '=' in l and 'of' in l][0]; b=int(hdr[hdr.index('of')-1])
    i=[k for k,l in enumerate(L) if ' '.join(l).startswith('FOR GOVERNOR')][0]
    def tot(name):
        l=[l for l in L[i:i+20] if any(name.upper() in x.upper() for x in l)][0]
        nums=[x for x in l if re.fullmatch(r'[\d,]+',x)]
        return N(nums[-1])
    return tot('Pritzker'),tot('Bailey'),b
def b_el45(f):
    t=soup(f).get_text('\n') if f.endswith('.html') else soup(f).get_text('\n')
    lines=[l for l in t.split('\n')]
    def firstnum(pred):
        l=[l for l in lines if pred(l)][0]; toks=l.replace('.',' ').split()
        return N([x for x in toks if re.fullmatch(r'\d{1,3}(,\d{3})*',x)][0])
    b=firstnum(lambda l:'BALLOTS CAST - TOTAL' in l)
    return firstnum(lambda l:'Pritzker' in l and 'DEM' in l),firstnum(lambda l:'Bailey' in l and 'REP' in l and 'Jeff' not in l),b
def b_chicago(f):
    L=pl_lines(f,1)
    tr=[l for l in L if l[:4]==['Total','Registration','and','Turnout']][0]; b=N(tr[5])
    d=[l for l in L if 'Pritzker' in l][0]; r=[l for l in L if 'Bailey' in l and 'Darren' in l][0]
    num=lambda l: N([x for x in l if re.fullmatch(r'[\d,]+',x)][0])
    return num(d),num(r),b
def b_radio(f):
    s=soup(f); toks=[x.strip() for x in s.get_text('\n').split('\n') if x.strip()]
    txt=' '.join(toks)
    m=re.search(r'(?:Total Ballots Cast|Ballots Cast:)\s*([\d,]+)',txt) or re.search(r'([\d,]+) ballots cast',txt)
    b=N(m.group(1))
    gi=[k for k,x in enumerate(toks) if x.lower().startswith('governor')][0]
    def v(name):
        k=[k for k in range(gi,gi+30) if name in toks[k]][0]
        return N([y for y in toks[k+1:k+4] if re.fullmatch(r'[\d,]+',y)][0])
    return v('Pritzker'),v('Bailey'),b
P={'voteclock':b_voteclock,'pollresults':b_pollresults,'platinum':b_platinum,'clarity':b_clarity,'cumpdf':b_cumpdf,'el45':b_el45,'chicago_pdf':b_chicago,
   'radio_wmix':b_radio,'radio_webq_a':b_radio,'radio_webq_b':b_radio}
if __name__=='__main__':
    rows=[]
    for c in sorted(M):
        D=R=B=0
        for auth,typ,f,url in M[c]:
            d,r,b=P[typ](f); D+=d; R+=r; B+=b
        rows.append(dict(county_key=c,year='2026',dem_votes=D,rep_votes=R,ballots_cast=B))
    with open('/workspace/illinois/out/pass_b_2026_raw.csv','w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows))
