import sys,re,requests,subprocess,os,datetime,json
# usage: peek.py name url
name,url=sys.argv[1],sys.argv[2]
r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'},timeout=60)
ext='.pdf' if r.content[:4]==b'%PDF' else '.html'
fn=f'/workspace/illinois/raw/2026/county/{name}{ext}'
open(fn,'wb').write(r.content)
log='/workspace/illinois/raw/2026/county/fetch_log.json'
L=json.load(open(log)) if os.path.exists(log) else []
L=[x for x in L if x['file']!=os.path.basename(fn)]
L.append(dict(county=name.split('__')[0],file=os.path.basename(fn),url=url,status=r.status_code,fetched=datetime.datetime.now().astimezone().isoformat(timespec='seconds')))
json.dump(L,open(log,'w'),indent=1)
if ext=='.pdf': txt=subprocess.run(['pdftotext','-layout',fn,'-'],capture_output=True,text=True).stdout
else:
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',r.text,flags=re.S); txt='\n'.join(l.strip() for l in re.sub(r'<[^>]+>','\n',t).splitlines() if l.strip())
lines=txt.splitlines()
print('##',name,r.status_code,ext,len(r.content))
for i,l in enumerate(lines):
    if re.search(r'ballots cast|ballots counted|turnout|pritzker|bailey|governor|run date|as of|updated|unofficial|official|precincts',l,re.I) and not re.search(r'jeff bailey',l,re.I):
        print(i,l[:160])
