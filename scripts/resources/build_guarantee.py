import random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
G='/usr/share/fonts/truetype/sand-box/google/'
SC=G+'Playfair Display SC/PlayfairDisplaySC-Bold.ttf'; BR=G+'Libre Baskerville/LibreBaskerville-VariableFont_wght.ttf'; BI=G+'Libre Baskerville/LibreBaskerville-Italic-VariableFont_wght.ttf'
f=lambda p,s:ImageFont.truetype(p,s)
W,H=1600,1200; random.seed(11)
INK=(44,34,26); NAVY=(19,41,82); ORNG=(196,84,26); GOLD=(150,112,52)
im=Image.new('RGB',(W,H),(236,222,188))
noise=Image.effect_noise((W,H),28).filter(ImageFilter.GaussianBlur(1.2))
blot=Image.effect_noise((W//8,H//8),60).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(25))
im=Image.composite(Image.new('RGB',(W,H),(214,192,148)),im,Image.eval(blot,lambda v:int(max(0,v-110)*0.9)))
im=Image.blend(im,Image.merge('RGB',[noise]*3),0.06)
vig=Image.new('L',(W,H),0); dv=ImageDraw.Draw(vig)
for i in range(60): dv.rectangle([i*3,i*3,W-i*3,H-i*3],outline=int(150-i*2.5))
im=Image.composite(Image.new('RGB',(W,H),(150,112,70)),im,vig.filter(ImageFilter.GaussianBlur(30)))
d=ImageDraw.Draw(im)
d.rectangle([34,34,W-34,H-34],outline=NAVY,width=6); d.rectangle([50,50,W-50,H-50],outline=ORNG,width=2)
for x,y in ((50,50),(W-50,50),(50,H-50),(W-50,H-50)): d.regular_polygon((x,y,12),4,fill=ORNG)
def star(cx,cy,r,col):
    pts=[(cx+(r if k%2==0 else r*.42)*math.sin(k*math.pi/5),cy-(r if k%2==0 else r*.42)*math.cos(k*math.pi/5)) for k in range(10)]; d.polygon(pts,fill=col)
def ct(y,t,fo,fi,sp=0):
    w=d.textlength(t,font=fo)+sp*(len(t)-1); x=(W-w)/2
    if not sp: d.text((x,y),t,font=fo,fill=fi); return
    for ch in t: d.text((x,y),ch,font=fo,fill=fi); x+=d.textlength(ch,font=fo)+sp
# header: ILLINOIS between rules, with 21 stars (21st state) in a shallow arc
ct(92,'ILLINOIS',f(SC,40),NAVY,8)
d.line([(W/2-420,118),(W/2-210,118)],fill=ORNG,width=3); d.line([(W/2+210,118),(W/2+420,118)],fill=ORNG,width=3)
for k in range(21):
    a=math.radians(-60+k*6); star(W/2-400+k*40,158,9,NAVY if k%2==0 else ORNG)
ct(206,'DID YOU KNOW?',f(SC,40),ORNG,6)
ct(262,'NOT YOUR JOB.',f(SC,108),INK,3); ct(380,'THEIR DUTY.',f(SC,108),NAVY,3)
d.line([(W/2-300,516),(W/2+300,516)],fill=GOLD,width=2); d.regular_polygon((W/2,516,9),4,fill=ORNG)
ct(540,'It is not your job to prove our elections are free and fair.',f(BR,34),INK)
ct(588,'The Guarantee Clause puts that on the government.',f(BR,34),INK)
ct(656,'\u201cThe United States shall guarantee to every State in this Union',f(BI,28),INK)
ct(694,'a Republican Form of Government \u2026\u201d',f(BI,28),INK)
ct(736,'U.S. CONSTITUTION, ART. IV, \u00a7 4',f(SC,24),NAVY,2)
# Chicago skyline silhouette over Lake Michigan
main_d=d; sk=Image.new('RGBA',(1500,420),(0,0,0,0)); d=ImageDraw.Draw(sk)
C=(28,44,80,255); base=360
blds=[(40,90,150),(95,60,210),(160,80,175),(245,55,240),(305,70,195),(380,45,260),(430,85,215),(520,60,300),(585,50,235)]
for x,w,h in blds: d.rectangle([x,base-h,x+w,base],fill=C)
# Willis Tower: stepped bundled tubes with twin antennas
X=650; d.rectangle([X,base-250,X+120,base],fill=C); d.rectangle([X+10,base-300,X+110,base-250],fill=C); d.rectangle([X+25,base-330,X+95,base-300],fill=C)
d.rectangle([X+40,base-345,X+80,base-330],fill=C); d.line([(X+48,base-345),(X+48,base-405)],fill=C,width=5); d.line([(X+72,base-345),(X+72,base-400)],fill=C,width=5)
for x,w,h in [(790,70,220),(870,55,265),(935,85,190),(1030,60,250)]: d.rectangle([x,base-h,x+w,base],fill=C)
# Trump-style setback tower and Aon-style slab
X=1100; d.rectangle([X,base-230,X+70,base],fill=C); d.rectangle([X+10,base-285,X+60,base-230],fill=C); d.rectangle([X+20,base-320,X+50,base-285],fill=C); d.line([(X+35,base-320),(X+35,base-360)],fill=C,width=4)
# Hancock-style tapered tower with antennas
X=1190; d.polygon([(X,base),(X+110,base),(X+95,base-300),(X+15,base-300)],fill=C); d.line([(X+38,base-300),(X+38,base-370)],fill=C,width=5); d.line([(X+72,base-300),(X+72,base-365)],fill=C,width=5)
for x,w,h in [(1310,70,160),(1390,60,120),(1455,40,90)]: d.rectangle([x,base-h,x+w,base],fill=C)
# lit windows as small gaps
for x in range(50,1480,22):
    for y in range(base-220,base-20,26):
        if sk.getpixel((x,y))[3] and random.random()<0.35: d.rectangle([x,y,x+5,y+9],fill=(232,170,90,255))
d.rectangle([0,base,1500,base+8],fill=(196,84,26,255))
for k in range(5): d.line([(60+k*40,base+22+k*10),(1440-k*40,base+22+k*10)],fill=(28,44,80,int(170-k*30)),width=2)
sk=sk.resize((740,207),Image.LANCZOS); im.paste(sk,(W//2-370,H-110-200),sk); d=main_d
L=f(BR,21); LI=f(BI,21)
for i,t in enumerate(['Executive Order 14399','March 31, 2026','91 Fed. Reg. 17125']): d.text((100,830+i*32),t,font=f(SC,24) if not i else L,fill=NAVY if not i else INK)
q=['\u201cThe Federal Government has an','unavoidable duty under Article II \u2026','to enforce Federal law, which','includes \u2026 maintaining public','confidence in election outcomes.\u201d']
for i,t in enumerate(q): d.text((W-90-d.textlength(t,font=LI),800+i*28),t,font=LI,fill=INK)
d.text((W-90-d.textlength('EO 14399, Sec. 1',font=L),944),'EO 14399, Sec. 1',font=L,fill=NAVY)
ct(H-86,'Illinois Election Analysis  \u00b7  a hypothesis, not a verdict',f(BR,19),(90,70,50))
im=im.filter(ImageFilter.SMOOTH)
im.save('/workspace/il_publish/resources/IL_Guarantee_Clause.png',optimize=True)
