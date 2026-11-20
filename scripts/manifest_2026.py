"""2026 UNOFFICIAL source manifest: county -> list of (authority, source_type, raw_file, url).
Chosen = most direct county-election-authority publication found; voteclock.org (a transcription that
cites each clerk's own results page) is used only where no direct authority file was retrieved."""
R='/workspace/illinois/raw/2026/'
VC='https://voteclock.org/{}-county-il-election-authority-2026'
def vc(slug,auth): return (auth,'voteclock',R+f'voteclock/{slug}-county-il-election-authority-2026.html',VC.format(slug))
def pr(k,auth): return (auth,'pollresults',R+f'pollresults/{k}.json',f'https://il-{k}.pollresults.net/Home/ElectionData')
def pl(i,auth,host='www'): 
    pre='stclair_' if host=='stclair' else ''
    return (auth,'platinum',(R+f'platinum/{pre}turnout_{i}.html',R+f'platinum/{pre}races_{i}_2.html'),f'https://{host}.platinumelectionresults.com/turnouts/county/{i} + /races/{i}/2')
def cl(n,path,auth): return (auth,'clarity',R+f'clarity/{n}_turnout_sum.json',f'https://results.enr.clarityelections.com/{path}/json/sum.json')
M={
 'ADAMS':[vc('adams','Adams County Clerk')],
 'CHAMPAIGN':[vc('champaign','Champaign County Clerk')],
 'COOK':[vc('cook','Cook County Clerk (suburban Cook)'),('Chicago Board of Election Commissioners','chicago_pdf',R+'county/chicago__summary.pdf','https://results.chicagoelections.gov/results/Summary%20Report%20(2%20Column).pdf')],
 'DUPAGE':[vc('dupage','DuPage County Clerk')],
 'GRUNDY':[vc('grundy','Grundy County Clerk')],
 'KANE':[vc('kane','Kane County Clerk')],
 'KENDALL':[vc('kendall','Kendall County Clerk')],
 'LAKE':[vc('lake','Lake County Clerk')],
 'LASALLE':[vc('lasalle','LaSalle County Clerk')],
 'MADISON':[vc('madison','Madison County Clerk')],
 'MCHENRY':[vc('mchenry','McHenry County Clerk')],
 'MCLEAN':[vc('mclean','McLean County Clerk (outside Bloomington)'),cl('Bloomington','IL/Bloomington/127392/387136','City of Bloomington Board of Election Commissioners')],
 'PEORIA':[vc('peoria','Peoria County Election Commission')],
 'SANGAMON':[vc('sangamon','Sangamon County Clerk')],
 'WILL':[vc('will','Will County Clerk')],
 'WILLIAMSON':[vc('williamson','Williamson County Clerk')],
 'WINNEBAGO':[vc('winnebago','Winnebago County Clerk (outside Rockford)'),cl('Rockford','WRC/Rockford/127559/387148','City of Rockford Board of Election Commissioners')],
 'ROCKISLAND':[vc('rock-island','Rock Island County Clerk')],
 'STCLAIR':[vc('st-clair','St. Clair County Clerk (outside East St. Louis)'),pl(48,'East St. Louis Board of Election Commissioners','stclair')],
 'DEKALB':[pl(66,'DeKalb County Clerk')],
 'CLINTON':[pl(10,'Clinton County Clerk')],'PIKE':[pl(103,'Pike County Clerk')],'RANDOLPH':[pl(13,'Randolph County Clerk')],
 'WAYNE':[pl(14,'Wayne County Clerk')],'MARION':[pl(18,'Marion County Clerk')],'FRANKLIN':[pl(21,'Franklin County Clerk')],'HENRY':[pl(76,'Henry County Clerk')],
 'MACOUPIN':[cl('Macoupin','IL/Macoupin/127399/384594','Macoupin County Clerk')],
 'JACKSON':[('Jackson County Clerk','cumpdf',R+'county/jackson__doc.pdf','https://www.jacksoncounty-il.gov/DocumentCenter/View/1228/Nov3_2026Results?bidId=')],
 'RICHLAND':[('Richland County Clerk','cumpdf',R+'county/richland__doc.pdf','https://richlandcounty.illinois.gov/wp-content/uploads/2026/11/CUMULATIVE-RESULTS-11-3-2026-09-19-55-PM.pdf')],
 'FULTON':[('Fulton County Clerk','cumpdf',R+'county/fulton__doc.pdf','https://fultoncountyilelections.gov/wp-content/uploads/2026/11/Cumulative-Results-11-16-2026-10-14-06-AM.pdf')],
 'JASPER':[('Jasper County Clerk','cumpdf',R+'county/jasper__doc.pdf','https://jaspercountyillinois.gov/wp-content/uploads/2026/11/Cumulative-Results-11-3-2026-08-18-19-PM.pdf')],
 'JERSEY':[('Jersey County Clerk','el45',R+'county/jersey_EL45.HTM','https://www.jerseycountyclerk-il.com/wp-content/2026-elections/26GILJER/EL45.HTM')],
 'WOODFORD':[('Woodford County Clerk','el45',R+'county/woodford_results.html','https://www.woodfordcountyelections.com/results.html')],
 'FAYETTE':[('WMIX radio transcription of Fayette County Clerk results','radio_wmix',R+'radio/wmix94_fayette.html','https://www.wmix94.com/fayette/')],
 'GALLATIN':[('WEBQ radio transcription of Gallatin County Clerk results','radio_webq_a',R+'radio/webqradio_gallatin.html','https://www.webqradio.com/gallatin/')],
 'HAMILTON':[('WEBQ radio transcription of Hamilton County Clerk report','radio_webq_b',R+'radio/webqradio_hamilton.html','https://www.webqradio.com/hamilton/')],
}
for k,a in [('bond','Bond'),('boone','Boone'),('bureau','Bureau'),('carroll','Carroll'),('christian','Christian'),('clark','Clark'),('coles','Coles'),('dewitt','DeWitt'),('edgar','Edgar'),('ford','Ford'),('lee','Lee'),('livingston','Livingston'),('logan','Logan'),('macon','Macon'),('mason','Mason'),('moultrie','Moultrie'),('ogle','Ogle'),('piatt','Piatt'),('putnam','Putnam'),('shelby','Shelby'),('stephenson','Stephenson'),('tazewell','Tazewell'),('whiteside','Whiteside')]:
    M[k.upper()]=[pr(k,a+' County Clerk')]
# Not obtained (excluded from 2026 computations): reason
EXCLUDED_NOTE={'VERMILION':'county clerk file found (pollresults) but City of Danville Election Commission results not retrieved',
 'KNOX':'Galesburg Board file found but Knox County Clerk (outside Galesburg) results not retrieved',
 'DOUGLAS':'county pollresults feed holds no 2026 ballots-cast total',
 'HARDIN':'only local-office results located; no governor contest',
 'BROWN':'county summary PDF is an image scan (no text layer)','JODAVIESS':'county official-results PDF is an image scan (no text layer)'}
