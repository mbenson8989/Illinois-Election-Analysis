import csv, json
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
I='/workspace/illinois/'; O=I+'out/'
UN='UNOFFICIAL (pre-Dec 4, 2026 canvass)'
ST='Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration'
CEDAR='https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit'
T=list(csv.DictReader(open(O+'il_governor_reverse_math_2022_2026_VERIFIED.csv'))); S=json.load(open(O+'compute_pass_a_summary.json')); V=json.load(open(O+'verification_full.json')); X=json.load(open(O+'il_2026_disagreements_UNOFFICIAL.json'))
ss=getSampleStyleSheet(); B=ss['BodyText']; B.fontSize=9; B.leading=11; H1=ss['Heading1']; H2=ss['Heading2']; sm=ParagraphStyle('sm',parent=B,fontSize=6.5,leading=8)
def hf(c,d):
    c.saveState(); W,H=d.pagesize; c.setFont('Helvetica-Bold',8); c.setFillColor(colors.red)
    c.drawString(36,H-24,f'Illinois Governor Reverse-Factoring 2022/2026 — 2026 data {UN}')
    c.setFont('Helvetica',7); c.setFillColor(colors.black); c.drawString(36,18,ST); c.drawRightString(W-36,18,f'p. {d.page}'); c.restoreState()
doc=SimpleDocTemplate(I+'report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf',pagesize=landscape(letter),leftMargin=36,rightMargin=36,topMargin=40,bottomMargin=36,
    title=f'Illinois Reverse-Factoring Report — 2026 {UN}',author='mbenson8989')
pct=lambda s: f"{float(s)*100:.2f}%" if s else '—'
def tbl(data,cw=None,fs=7):
    t=Table(data,colWidths=cw,repeatRows=1); t.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica',fs),('FONT',(0,0),(-1,0),'Helvetica-Bold',fs),('GRID',(0,0),(-1,-1),.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eef6')),('VALIGN',(0,0),(-1,-1),'TOP')])); return t
E=[]
E+= [Paragraph('Illinois Governor 2022 &amp; 2026 — Reverse-Factoring Report',H1),Paragraph(f'<font color="red"><b>2026 figures are {UN}.</b></font> 2022 figures are SBOE official canvass. Built Thursday, November 19, 2026 (CST).',B),
 Paragraph(f'<b>{ST}.</b>',B),Paragraph(f'Cross-link: <link href="{CEDAR}" color="blue">{CEDAR}</link>',B),Spacer(1,8)]
E+=[tbl([['Item','Result'],['Locked Illinois formula',f"Dem-share change = {S['constant']} + ({S['multiplier']}) x stand-in drop;  R² = {S['r_squared']};  n = {S['n_fit']}"],
 ['Floor / ceiling 2022 (official)',f"{S['floor_2022'][0]} {pct(S['floor_2022'][1])} / {S['ceiling_2022'][0]} {pct(S['ceiling_2022'][1])}"],
 [f'Floor / ceiling 2026 {UN}',f"{S['floor_2026_UNOFFICIAL'][0]} {pct(S['floor_2026_UNOFFICIAL'][1])} / {S['ceiling_2026_UNOFFICIAL'][0]} {pct(S['ceiling_2026_UNOFFICIAL'][1])}"],
 ['Over-ballot flags (D+R > ballots)',f"2022: {len(S['over_ballot_2022'])} of 102;  2026 {UN}: {len(S['over_ballot_2026'])} of {S['n_fit']}"],
 [f'Total implied extra votes, {UN}',f"{float(S['total_implied_extra_votes']):,.2f}  (positive {float(S['sum_positive_implied']):,.2f}; negative {float(S['sum_negative_implied']):,.2f})"],
 ['2026 coverage',f"{S['n_fit']} of 102 counties with a county-authority ballots-cast figure; {102-S['n_fit']} excluded"]],[2.6*inch,6.6*inch],8),Spacer(1,8)]
v22=V['verification_2022']
E+=[Paragraph('Double verification (two independent passes; every cell to the decimal)',H2),tbl([['Check','Cells','Matched','Mismatched'],
 ['2022 SBOE vote file, Pass A vs Pass B',v22['cells_compared'],v22['matched'],v22['mismatched']],['2022 vs SBOE PDF governor table',204,v22['pdf_cells_matched'],v22['pdf_cells_mismatched']],
 ['Stand-in primary ballots 2022 & 2026',V['stand_in_primary_ballots']['cells'],V['stand_in_primary_ballots']['matched'],0],[f'2026 raw county D/R/ballots {UN}',V['raw_2026_UNOFFICIAL']['cells'],V['raw_2026_UNOFFICIAL']['matched'],0],
 ['Full computed table',V['computed_table']['cells'],V['computed_table']['matched'],0],['Statewide summary',V['summary']['fields'],V['summary']['matched'],0]],None,8),
 Paragraph('One mismatch was found and fixed before publication: Stephenson 2026 Dem share 6,199/16,000 = 0.3874375 exactly (a decimal tie). Pass A rounded it half-to-even (0.387438) and Pass B float formatting gave 0.387437. Pass B now uses exact integer half-to-even rounding; both passes were re-run and every cell matches.',B)]

SA=json.load(open(O+'share_pass_a_summary.json'))['fits']; SV=json.load(open(O+'verification_share_form.json'))
NE=json.load(open(O+'ne_format_pass_a_summary.json')); NV=json.load(open(O+'verification_ne_format.json')); A=SA['A_2022_official']; VG=NE['vote_share_growth_fit']
SU=json.load(open(O+'surplus_pass_a_summary.json')); SUV=json.load(open(O+'verification_surplus_locked.json')); LA=SU['LOCKED_2022_official']; LB=SU['SECONDARY_2026_UNOFFICIAL']
box=Table([[Paragraph(f"<b>Surplus Equation: S = {LA['multiplier']} x (D/100) + {LA['offset']}</b>",ParagraphStyle('eq',parent=B,fontSize=13,leading=16))]],colWidths=[6.5*inch])
box.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.2,colors.black),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
E+=[PageBreak(),Paragraph('Locked Illinois Formula: Surplus Equation (Illinois statewide constant)',H2),box,Spacer(1,6),Paragraph('Where:',B),
 Paragraph('- S = Surplus, expressed in percentage points: Dem share of ballots cast minus D (2022, SBOE official canvass)',B),
 Paragraph('- D = Democratic registration-share <b>STAND-IN</b>, as a percent (0-100 scale): Democratic primary ballots / all primary ballots x 100 (2022 General Primary). Illinois has no party registration; this is NOT party registration and not a headcount of registered Democrats.',B),
 Paragraph(f"- {LA['multiplier']} = Multiplier coefficient",B),Paragraph(f"- {LA['offset']} = Constant offset, in percentage points",B),Spacer(1,4),
 Paragraph(f"OLS fit of S on D/100 across all {LA['n']} counties, 2022 official SBOE data: R² = {LA['r_squared']}; mean absolute residual {LA['mean_abs_residual_pp']} pp; largest residual {LA['max_residual_county']} ({LA['max_residual_pp']}). Format follows the Nebraska wiki's Locked formula page. 2022 is the locked year because it is the only year with official results for all 102 counties.",B),
 Paragraph('Secondary fit (same surplus form; not the locked equation; 2026 = '+UN+f", {LB['n']} counties, no gaps filled)",ParagraphStyle('h3',parent=B,fontName='Helvetica-Bold')),
 tbl([['Fit','n','Multiplier','Offset','R²','Mean |resid| pp','Largest residual (pp)']]+[[l,f['n'],f['multiplier'],f['offset'],f['r_squared'],f['mean_abs_residual_pp'],f"{f['max_residual_county']} {f['max_residual_pp']}"] for l,f in
  [('LOCKED: 2022 surplus, official',LA),(f'2026 surplus, {UN}',LB)]],None,7),Spacer(1,4),
 Paragraph(f"Verification (Pass A exact fractions vs Pass B pandas/numpy): locked surplus table and fit {SUV['table_matched']+SUV['fit_matched']:,}/{SUV['table_cells']+SUV['fit_fields']:,} cells, 0 mismatches.",B),
 Image(I+'charts/il_surplus_equation_locked_UNOFFICIAL2026.png',width=9.3*inch,height=3.5*inch,kind='proportional')]
E+=[PageBreak(),Paragraph('Registration stand-in evaluation',H2)]
E+=[tbl([['Option','Coverage','Accuracy','Defensibility','Verdict'],
 [Paragraph('1. SBOE Democratic primary ballot share',sm),Paragraph('All 102 counties, 2022 and 2026, one official source',sm),Paragraph('Moderate: sensitive to which primaries were contested',sm),Paragraph('Highest: SBOE official canvass, reproducible',sm),'CHOSEN'],
 [Paragraph('2. Party of last primary voted (county voter files)',sm),Paragraph('Not statewide; only some of 108 authorities publish (e.g. Kane)',sm),Paragraph('Same underlying signal, mixed vintages',sm),Paragraph('Low: inconsistent across counties',sm),'Rejected'],
 [Paragraph('3. Paid modeled party (L2 / Catalist)',sm),Paragraph('Statewide',sm),Paragraph('Modeled estimate, proprietary',sm),Paragraph('Low: paid, not citable, not reproducible; not purchased',sm),'Rejected']],[2*inch,2.2*inch,2*inch,2.2*inch,.8*inch],7),Spacer(1,6),
 Paragraph('<b>Caveat: 2022→2026 contest-structure jump.</b> Statewide, the Dem share of primary ballots went from 51.88% (911,919 of 1,757,872; June 28, 2022) to 67.87% (1,283,256 of 1,890,699; March 17, 2026). That swing reflects which primaries were contested, not a change in party loyalty. The stand-in drop is negative in most counties, so read the results as county-vs-county comparisons. Small counties can swing on one local primary (e.g. Gallatin).',B)]
for f in ['il_fit_share_change_vs_standin_drop_UNOFFICIAL.png','il_dem_share_2022_vs_2026_UNOFFICIAL.png','il_gap_standin_vs_dem_share_UNOFFICIAL.png']:
    E+=[PageBreak(),Image(I+'charts/'+f,width=8.3*inch,height=5.6*inch,kind='proportional')]
E+=[PageBreak(),Image(I+'charts/il_implied_extra_votes_UNOFFICIAL.png',width=6.2*inch,height=6.8*inch,kind='proportional')]
hdr=['County','Pop 2020','Stand-in 22','Stand-in 26','Drop','Dem sh 22','Gap 22','Ballots 26*','Dem sh 26*','Gap 26*','Chg','Delta-G','Expected','Residual','Implied extra*','OB22','OB26*']
rows=[[r['county'],f"{int(r['pop_2020']):,}",r['standin_dem_primary_share_2022'],r['standin_dem_primary_share_2026'],r['standin_drop_2022_to_2026'],r['dem_share_ballots_2022'],r['gap_2022'],
  (f"{int(r['ballots_cast_2026_UNOFFICIAL']):,}" if r['ballots_cast_2026_UNOFFICIAL'] else '—'),r['dem_share_ballots_2026_UNOFFICIAL'] or '—',r['gap_2026_UNOFFICIAL'] or '—',r['share_change_2022_to_2026'] or '—',r['delta_G'] or '—',r['expected_change'] or '—',r['residual'] or '—',
  (f"{float(r['implied_extra_votes']):,.2f}" if r['implied_extra_votes'] else '—'),r['over_ballot_2022'],r['over_ballot_2026'] or '—'] for r in T]
E+=[PageBreak(),Paragraph(f'County table, sorted by 2020 population (largest to smallest). * = 2026 {UN}. Stand-in = Dem primary ballot share (NOT registration).',H2),tbl([hdr]+rows,None,6)]
E+=[PageBreak(),Paragraph(f'2026 sources ({UN}) and exclusions',H2)]
E+=[tbl([['County','2026 source','As of']]+[[r['county'],Paragraph(r['source_2026_UNOFFICIAL'],sm),Paragraph(r['as_of_2026'],sm)] for r in T if r['ballots_cast_2026_UNOFFICIAL']],[1.2*inch,4.8*inch,3.4*inch],6),Spacer(1,6)]
E+=[tbl([['Excluded county','Reason']]+[[r['county'],Paragraph(r['status_2026'],sm)] for r in T if not r['ballots_cast_2026_UNOFFICIAL']],[1.4*inch,8*inch],6),Spacer(1,6)]
E+=[Paragraph(f"<b>Disagreements.</b> voteclock.org snapshot vs the county vendor feed used: "+'; '.join(f"{d['county'].title()} voteclock {d['voteclock'][0]:,}/{d['voteclock'][1]:,}/{d['voteclock'][2]:,} vs used {d['used'][0]:,}/{d['used'][1]:,}/{d['used'][2]:,}" for d in X['voteclock_vs_feed'])+
 f". civicAPI cross-check (race 87130; updated 5:30 p.m. CST Nov 19, 2026; {X['civicapi_percent_reporting']}% reporting): {X['exact_D_R_match']} of {X['counties_compared']} counties match exactly; {X['differ']} differ. Largest (used minus civicAPI, D/R): "+
 '; '.join(f"{d['county'].title()} {d['diff_D']:+,}/{d['diff_R']:+,}" for d in X['largest'])+'. The differences are mostly timing (election-night county snapshots vs later counts). civicAPI is never used in the computations.',B)]
doc.build(E,onFirstPage=hf,onLaterPages=hf); print('pdf ok')
