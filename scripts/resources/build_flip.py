import json,csv
from PIL import Image, ImageDraw, ImageFont
OUT='/workspace/il_publish/resources/'
FB='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
f=lambda s:ImageFont.truetype(FB,s)
BLUE=(0,66,130); NAVY=(10,30,60); GRAY=(95,95,95); BLK=(0,0,0); WHT=(255,255,255); ORANGE=(232,74,39)
A=json.load(open('/workspace/il-resources/out/flip_pass_a.json'))
cand={c:v for c,v in A.items() if v['share_test']}
top=sorted(cand,key=lambda c:-cand[c]['share_value'])[:10]; N=len(top)
n=lambda x:f'{int(round(x)):,}'
def ctext(d,y,t,font,fill,W=1080): d.text(((W-d.textlength(t,font=font))/2,y),t,font=font,fill=fill)
def fit(d,t,size,mw):
    while d.textlength(t,font=f(size))>mw: size-=2
    return f(size)
def arrow(d,cx,top_,h,w,up,col):
    sw=w*0.42; hh=h*0.42
    pts=[(cx,top_),(cx+w/2,top_+hh),(cx+sw/2,top_+hh),(cx+sw/2,top_+h),(cx-sw/2,top_+h),(cx-sw/2,top_+hh),(cx-w/2,top_+hh)] if up else [(cx,top_+h),(cx+w/2,top_+h-hh),(cx+sw/2,top_+h-hh),(cx+sw/2,top_),(cx-sw/2,top_),(cx-sw/2,top_+h-hh),(cx-w/2,top_+h-hh)]
    d.polygon(pts,fill=col,outline=BLK,width=4)
FOOT1='Source: Illinois State Board of Elections (2022; primaries) + county election authorities (2026*).'
FOOT2='*2026 UNOFFICIAL (SBOE canvass Dec 4, 2026). Stand-in = Dem primary ballot share, NOT registration.'
rows=[];man=[]
for i,c in enumerate(top,1):
    v=A[c]; g=v['share_value']; pct=100*g/v['B26']
    rows.append(dict(rank=i,county=c,pop=v['pop'],R22=v['R22'],R26=v['R26'],dR=v['dR'],S22=v['S22'],S26=v['S26'],dS=v['dS'],d22=v['d22'],d26=v['d26'],dvotes=v['d26']-v['d22'],B26=v['B26'],value=round(g),pct=round(pct,1)))
    im=Image.new('RGB',(1080,1350),WHT); d=ImageDraw.Draw(im)
    d.rectangle([0,0,1080,210],fill=NAVY)
    ctext(d,28,f'#{i} OF {N} ILLINOIS FLIP COUNTIES',f(34),(255,170,120))
    t=c.upper()+' COUNTY'; ctext(d,78,t,fit(d,t,100,1000),WHT)
    arrow(d,130,262,170,130,False,GRAY)
    d.text((240,250),'DEM PRIMARY BALLOT SHARE',font=f(38),fill=BLK); d.text((240,292),'(registration stand-in)',font=f(30),fill=GRAY)
    t=f'{v["R22"]:.2f}% \u2192 {v["R26"]:.2f}%'; d.text((240,330),t,font=fit(d,t,80,800),fill=BLK)
    d.text((240,420),f'\u2212{-v["dR"]:.2f} points  (2022 \u2192 2026)',font=f(42),fill=GRAY)
    arrow(d,130,530,220,150,True,BLUE)
    d.text((240,520),'DEMOCRATIC SHARE OF',font=f(40),fill=BLUE); d.text((240,565),'BALLOTS CAST (GOVERNOR)',font=f(40),fill=BLUE)
    t=f'{v["S22"]:.2f}% \u2192 {v["S26"]:.2f}%*'; d.text((240,620),t,font=fit(d,t,80,800),fill=BLUE)
    dv=v['d26']-v['d22']; d.text((240,712),f'+{v["dS"]:.2f} points*  (votes {n(v["d22"])} \u2192 {n(v["d26"])}*)',font=fit(d,f'+{v["dS"]:.2f} points*  (votes {n(v["d22"])} \u2192 {n(v["d26"])}*)',40,820),fill=BLUE)
    d.rectangle([0,840,1080,1140],fill=BLUE)
    ctext(d,862,'VOTES BEYOND WHAT THE STAND-IN EXPLAINS',f(38),WHT)
    ctext(d,925,f'+{n(g)}*',f(150),WHT)
    d.rectangle([0,1140,1080,1150],fill=ORANGE)
    ctext(d,1165,f'That is {pct:.1f}% of 2026* ballots cast in {c} County.',f(34),BLK)
    ctext(d,1215,'Lower Democratic primary share. Higher Democratic vote share.',f(32),BLK)
    ctext(d,1262,FOOT1,fit(d,FOOT1,22,1040),GRAY); ctext(d,1292,FOOT2,fit(d,FOOT2,22,1040),GRAY)
    ctext(d,1320,'A pattern in the numbers, not a finding about cause.',f(22),GRAY)
    fn=f'IL_Flip_{i:02d}_{c.replace(" ","_").replace(".","")}.png'; im.save(OUT+fn)
    man.append(dict(file=fn,strings=[c.upper()+' COUNTY',f'{v["R22"]:.2f}%',f'{v["R26"]:.2f}%',f'{-v["dR"]:.2f}',f'{v["S22"]:.2f}%',f'{v["S26"]:.2f}%',f'{v["dS"]:.2f}',n(v['d22']),n(v['d26']),n(g),f'{pct:.1f}']))
im=Image.new('RGB',(1080,1350),WHT); d=ImageDraw.Draw(im)
d.rectangle([0,0,1080,200],fill=NAVY)
ctext(d,30,f'{"FOUR" if N==4 else N} ILLINOIS COUNTIES',f(64),WHT); ctext(d,115,'Lower Dem primary share. Higher Dem vote share.',f(36),(255,170,120))
ctext(d,225,'Votes beyond what the stand-in explains, 2022 \u2192 2026*',f(34),BLK)
mx=rows[0]['value']; y=300
for r in rows:
    d.text((40,y+12),f'{r["rank"]}. {r["county"]}',font=f(40),fill=BLK)
    L=int(430*r['value']/mx); d.rectangle([390,y,390+max(L,6),y+70],fill=BLUE)
    d.text((390+max(L,6)+14,y+14),f'+{r["value"]:,}*',font=f(40),fill=BLK); y+=120
y+=10
for t in ['Only these 4 of the 80 counties with 2026* data passed the test:',"the Dem primary ballot share fell AND the Dem share of ballots rose.",'No county had fewer Dem primary ballots AND more Dem votes','(the Kansas headcount test): 0 of 80. 22 counties have no 2026* data yet.']:
    ctext(d,y,t,fit(d,t,28,1020),BLK); y+=42
ctext(d,1170,'Value = 2026 Dem votes \u2212 2026 ballots \u00d7 2022 Dem share \u00d7 (2026 stand-in \u00f7 2022 stand-in)',fit(d,'Value = 2026 Dem votes \u2212 2026 ballots \u00d7 2022 Dem share \u00d7 (2026 stand-in \u00f7 2022 stand-in)',26,1040),GRAY)
ctext(d,1225,FOOT1,fit(d,FOOT1,22,1040),GRAY); ctext(d,1258,FOOT2,fit(d,FOOT2,22,1040),GRAY)
ctext(d,1295,'A pattern in the numbers, not a finding about cause.',f(22),GRAY)
im.save(OUT+'IL_Flip_00_Summary.png')
json.dump(rows,open('/workspace/il-resources/out/flip_rows.json','w'),indent=1); json.dump(man,open('/workspace/il-resources/out/flip_manifest.json','w'),indent=1)
with open(OUT+'IL_Flip_Counties.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['rank','county','population_2020','standin_dem_primary_share_2022_pct','standin_dem_primary_share_2026_pct','standin_change_pts','dem_share_of_ballots_2022_pct','dem_share_of_ballots_2026_pct_UNOFFICIAL','dem_share_change_pts_UNOFFICIAL','dem_gov_votes_2022','dem_gov_votes_2026_UNOFFICIAL','dem_vote_change_UNOFFICIAL','ballots_cast_2026_UNOFFICIAL','value_votes_beyond_standin_UNOFFICIAL','value_pct_of_2026_ballots_UNOFFICIAL'])
    for r in rows: w.writerow([r[k] for k in ['rank','county','pop','R22','R26','dR','S22','S26','dS','d22','d26','dvotes','B26','value','pct']])
print(*[(r['rank'],r['county'],r['dR'],r['dS'],r['value'],r['pct'],r['dvotes']) for r in rows],sep='\n')
