import re,json,html,sys
R='/workspace/il-resources/raw/'
def norm(t): 
    t=html.unescape(t).replace('\u2014','—').replace('\u2019',"'").replace('\u201c','"').replace('\u201d','"')
    return re.sub(r'\s+',' ',t).strip().lower()
src=[]
eo=open(R+'federal/eo14399.txt').read(); eo=re.sub(r'-\s*\n\s*','',eo); src.append(('EO14399',norm(eo)))
c=open(R+'federal/constitution.html',errors='ignore').read(); src.append(('Constitution',norm(re.sub(r'<[^>]+>',' ',c))))
for k,v in json.load(open(R+'statutes/foia.json')).items(): src.append(('5 ILCS 140/'+k,norm(v)))
for k,v in json.load(open(R+'statutes/ec_sections.json')).items(): src.append(('10 ILCS 5/'+k,norm(v)))
out=[];bad=0
for f in sys.argv[1:]:
    t=open(f).read()
    for q in [q for line in t.split('\n') for q in re.findall(r'"([^"]{6,}?)"',line)]:
        qq=norm(q); qq=re.sub(r'\[(\w)\]',r'\1',qq)            # [t]he -> the
        parts=[x.strip(' .,;') for x in re.split(r'\s*(?:…|\.\.\.)\s*',qq) if x.strip(' .,;')]
        parts=[re.sub(r'\[\w+\]$','',x) for x in parts]
        hit=[n for n,s in src if all(p.rstrip(']').replace('[s]','s') in s or p.replace('prohibit[s]','prohibit') in s for p in parts)]
        ok=bool(hit); bad+=not ok; out.append(dict(file=f.split('/')[-1],quote=q[:90],found_in=hit[:3],ok=ok))
for o in out: print('OK ' if o['ok'] else 'XX ',o['found_in'][:2],o['quote'])
print('quotes',len(out),'not found',bad)
json.dump(out,open('/workspace/il-resources/out/quote_check.json','w'),indent=1)
