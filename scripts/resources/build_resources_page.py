import csv,json
P='/workspace/il_publish/'; R='/workspace/il-resources/'
RAW='https://raw.githubusercontent.com/mbenson8989/Illinois-Election-Analysis/main/'; BLOB='https://github.com/mbenson8989/Illinois-Election-Analysis/blob/main/'; WIKI='https://github.com/mbenson8989/Illinois-Election-Analysis/wiki/'
Z=json.load(open(R+'out/zip_info.json')); REG=json.load(open(R+'out/regions.json'))
L=list(csv.DictReader(open(R+'out/letter_merge_fields.csv')))
EQ=list(csv.DictReader(open(P+'IL_108_Authority_Voting_Equipment_VerifiedVoting.csv'))); S=json.load(open(R+'out/equipment_summary_pass1.json'))
FL=json.load(open(R+'out/flip_rows.json')); FV=json.load(open(R+'out/flip_verify.json'))
vvdate=open(R+'raw/vv/RETRIEVED.txt').read().strip()
n=lambda x:f'{int(x):,}'
o=[]; a=o.append
a('# Resources\n')
a("> **\\*2026 figures are UNOFFICIAL (pre-Dec 4, 2026 canvass).** The Illinois State Board of Elections (SBOE) has not yet posted 2026 general-election results; its official canvass is scheduled for December 4, 2026, so 2026 figures come from the results each county or municipal election authority posted. 2022 figures are the SBOE official canvass. **Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.** Wherever this wiki says D or \"registration,\" it means Democratic primary ballots ÷ all primary ballots × 100, from the SBOE official 2022 and 2026 primary canvasses.\n")
a('This page collects the documents, data sources, laws, equipment records, and graphics behind the Illinois Election Analysis in one place. Everything here is offered as analysis and as draft correspondence. Nothing on this page is an accusation against any county, election authority, official, or vendor.\n')
a('## Letter to the Illinois Attorney General\n')
a('A draft letter to Attorney General Kwame Raoul asking his office to say publicly whether cast vote records and ballot images from the November 3, 2026 general election are open to the public under the Illinois Freedom of Information Act (5 ILCS 140) once the canvass is complete, how the Act\'s exemption for information "specifically prohibited from disclosure by federal or State law" and its duty to release the remaining information (5 ILCS 140/7(1)) apply to a cast vote record that names no voter, and to help make sure 2026 election records are kept for the full 22-month federal period (52 U.S.C. § 20701), longer than the Election Code\'s 2-month ballot period (10 ILCS 5/17-20) and 60-day test-material period (10 ILCS 5/24B-9). It also asks the Public Access Counselor in his office to review any denial a member of the public brings to it (5 ILCS 140/9.5). It cites the Guarantee Clause (U.S. Const. art. IV, § 4) and the Article II enforcement-duty language in Executive Order 14399. It is respectful and non-accusatory, and it presents the Illinois analysis as a hypothesis, not proof. It is a draft for Morissa to review and send herself; it has not been sent.\n')
a(f'- [Download the Attorney General letter (PDF)]({RAW}Illinois_Attorney_General_Letter.pdf)')
a(f'- [Download the Attorney General letter (Word)]({RAW}Illinois_Attorney_General_Letter.docx)\n')
a('Every quotation in the letter was checked word for word against the official text of the statute, order, or constitutional provision it quotes (Illinois General Assembly, ilga.gov; Federal Register / GovInfo; National Archives). The addressee and office address are from the [Office of the Illinois Attorney General](https://illinoisattorneygeneral.gov/) website (Chicago office, 115 S. LaSalle St., Chicago, IL 60603), retrieved November 24, 2026.\n')
a('## County clerk letters\n')
a('Illinois elections are run by **108 election authorities**, not 102. The [SBOE Election Authorities page](https://www.elections.il.gov/ElectionOperations/ElectionAuthorities.aspx) lists them: the county clerk in 101 counties, one county election commission (the **Peoria County Election Commission**, which runs elections for all of Peoria County), and **six municipal boards of election commissioners** that run elections inside their cities instead of the county clerk: **Chicago** (Cook County), **Rockford** (Winnebago), **Bloomington** (McLean), **Galesburg** (Knox), **Danville** (Vermilion), and **East St. Louis** (St. Clair). So there is one letter for each of the 108 authorities: 101 county clerk letters, 1 Peoria County Election Commission letter, and 6 board of election commissioners letters, in both PDF and Word. Voters in those six cities are served by the city board, so a county clerk letter alone would miss them. Each ZIP has a `PDF` folder and a `Word` folder. Pick your region, or download everything at once.\n')
z0=Z[0]; a(f'- **[Download all 108 Illinois election-authority letters (ZIP, 102 counties, {z0["mb"]} MB)]({RAW}downloads/{z0["file"]})**\n')
a('By region:\n')
for z in Z[1:]: a(f'- [Download {z["region"]} letters (ZIP, {z["counties"]} {"county" if z["counties"]==1 else "counties"}, {z["letters"]} letters, {z["mb"]} MB)]({RAW}downloads/{z["file"]})')
a(f'\nNot sure which region your county is in? [Download the county-to-region lookup (CSV)]({RAW}downloads/Illinois_County_to_Region_Lookup.csv), or use the table below.\n')
a('**How the counties are grouped.** The SBOE does not divide Illinois into election regions; each election authority runs its own elections. These six regions are an informal geographic grouping chosen for convenience, covering all 102 counties exactly once. The grouping has nothing to do with how the letters or the analysis were built.\n')
a('**What each letter contains.** The letters follow Morissa\'s Nebraska cast-vote-record request letter, in the same tone and structure as the Kansas and Texas clerk letters, rewritten for Illinois law: the county\'s own 2022 and 2026\\* figures for Democratic primary ballots and the Democratic primary share (the labeled stand-in), Democratic votes for governor, and total ballots cast (municipal-board letters use the county-wide figures for the county the city sits in, and say so); federal litigation context (no standing claimed); a Freedom of Information Act request for existing records only (cast vote record export, ballot images, precinct returns under 10 ILCS 5/24B-15, the 5% retabulation comparisons under 10 ILCS 5/24B-15, the test records under 10 ILCS 5/24B-9, and hash-verification records); a request to preserve 2026 records for the full 22-month federal period; a request, not a demand, for wider hand-count coverage that acknowledges the court-order rule for unsealing ballots after the proclamation; and blank date, signature, and sender lines. For the 22 counties without usable 2026\\* results yet, the letter gives the 2022 and primary figures and says the 2026 comparison will follow. Addressees and mailing addresses come from the SBOE Election Authorities list, retrieved November 24, 2026. All 108 authorities had a name and address on that list, so no addressee is a placeholder. Please confirm each addressee against the authority\'s own website before sending, because officials change. Nothing has been mailed or emailed.\n')
a('| Region | Counties | Letters | County list |'); a('|---|---|---|---|')
for i,(reg,cs) in enumerate(REG.items(),1):
    nl=sum(1 for r in L if r['region']==reg); a(f'| {i}. {reg} | {len(cs)} | {nl} | {", ".join(sorted(cs))} |')
a('\nMunicipal boards (letters included in their county\'s region): Chicago (Cook), Rockford (Winnebago), Bloomington (McLean), Galesburg (Knox), Danville (Vermilion), East St. Louis (St. Clair).\n')
a('## Illinois State Board of Elections data sources\n')
a('Every 2022 and primary number on this wiki comes from the Illinois State Board of Elections:\n')
a('- **2022 general election (official):** [SBOE Download Vote Totals](https://www.elections.il.gov/ElectionOperations/DownloadVoteTotals.aspx): the 2022 General Election county vote file (`2022GECty`) and the official canvass PDF (`2022GEOfficialVote.pdf`); also browsable on [SBOE Election Vote Totals](https://www.elections.il.gov/ElectionOperations/ElectionVoteTotals.aspx)')
a('- **Registration stand-in (official):** the SBOE official canvasses of the June 28, 2022 and March 17, 2026 general primaries (`2022GPCty`, `2022GPOfficialVote.pdf`, `2026GPOfficialVote.pdf`), from the same Download Vote Totals page. Democratic primary ballots ÷ all primary ballots, per county. *Stand-in, NOT official party registration; Illinois has no party registration.*')
a('- **2026 general election (unofficial\\*):** not yet posted by the SBOE (canvass December 4, 2026). County figures come from each election authority\'s own posted results; the source for every county is in the source column of [Bottom-Up Reverse Math](' + WIKI + 'Reverse-Math) and in [`raw/sources.json`](' + BLOB + 'raw/sources.json).')
a('- **Election authorities:** [SBOE Election Authorities](https://www.elections.il.gov/ElectionOperations/ElectionAuthorities.aspx) ("All Election Authorities" view), used for the letter addressees')
a('\nCounty populations (used only to sort the tables) are 2020 Census (PL 94-171) counts.\n')
a('## County-level results\n')
a(f'- [Download the PDF report]({RAW}report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf): every county\'s stand-in, Democratic share, surplus, and change, 2022 vs 2026\\*, with the locked equation and verification')
a(f'- [2022 governor results by county, verified (CSV)]({RAW}out/il_2022_governor_by_county_VERIFIED.csv): SBOE official 2022 governor votes and ballots cast, all 102 counties')
a(f'- [2022 vs 2026\\* reverse math by county, verified (CSV)]({RAW}out/il_governor_reverse_math_2022_2026_VERIFIED.csv): stand-in, Democratic shares, gaps, residuals and each county\'s 2026 source')
a(f'- [Surplus-form county table (CSV)]({RAW}out/surplus_pass_a.csv): S, D and residuals for the [Locked Illinois Formula]({WIKI}Locked-Illinois-Formula)')
a(f'- Step-by-step county arithmetic: [Bottom-Up Reverse Math]({WIKI}Reverse-Math); top and bottom counties: [Floor and Ceiling Counties]({WIKI}Floor-and-Ceiling)\n')
# equipment
tot=S['_total_registered']
a('## Voting equipment by county\n')
a('This table lists the in-person and mail-ballot equipment Verified Voting records for each of Illinois\'s 108 election authorities: the 102 counties and the six municipal boards of election commissioners. It is offered as background on how ballots are marked and counted. **Equipment information is context only. It is not evidence of wrongdoing, and a vendor name does not imply a problem with any jurisdiction\'s results.**\n')
a(f'**Source.** [Verified Voting\'s Verifier](https://verifiedvoting.org/verifier/): the public CSV download for Illinois (state FIPS 17), years 2026 and 2022, retrieved {vvdate.replace("CST","CST (America/Chicago)")}. Verified Voting\'s 2026 Illinois export is labeled *The Verifier - November 2026 / Illinois. Data as of November 24, 2026.* It lists 108 Illinois jurisdictions, the same 108 election authorities the SBOE lists. Verified Voting\'s "Cook County" record is the suburban Cook County Clerk\'s jurisdiction; Chicago is its own record, and the same split applies to the other five cities. Counties are sorted by 2020 Census population, largest to smallest, like the other Illinois tables; the six city boards follow, sorted by Verified Voting\'s registered-voter count.\n')
a(f'**Confirmed vs. unconfirmed.** A jurisdiction is marked *Confirmed* when Verified Voting\'s 2026 record lists an election-day tabulator for it. All {S["_n_confirmed"]} meet that test; **{108-S["_n_confirmed"]} are unconfirmed**.\n')
a('### Statewide vendor summary (2026 election-day tabulators)\n')
a('Counts use the election-day tabulator Verified Voting lists for each jurisdiction. Ballot-marking devices, poll books, and the remote ballot-marking systems for military, overseas, and disabled voters are not counted as the election-day tabulator. Registered voters are Verified Voting\'s figures, so the city boards and the rest of their counties are not double-counted.\n')
for v,d in sorted(((k,v) for k,v in S.items() if not k.startswith('_')),key=lambda x:-x[1]['authorities']):
    a(f'- **{v}:** {d["authorities"]} election authorities ({d["counties"]} counties{"" if d["authorities"]==d["counties"] else " and " + str(d["authorities"]-d["counties"]) + " city " + ("board" if d["authorities"]-d["counties"]==1 else "boards")}); {n(d["registered"])} registered voters ({100*d["registered"]/tot:.1f}% of the {n(tot)} Verified Voting lists statewide)')
mk=S['_marking']; a(f'\nNo jurisdiction lists more than one election-day tabulator vendor. Marking method: {mk.get("Hand marked paper ballots and BMDs",0)} jurisdictions use hand-marked paper ballots with ballot-marking devices (BMDs) available, and {mk.get("Ballot Marking Devices for all voters",0)} uses BMDs for all voters ({", ".join(r["Jurisdiction"] for r in EQ if r["Marking method"]=="Ballot Marking Devices for all voters")}).\n')
a('The downloadable CSV also records each jurisdiction\'s poll book, 2022 election-day tabulator equipment, status, source link, and notes.\n')
a('### Download the full table\n')
a(f'- CSV (all 108 election authorities and all columns): [IL_108_Authority_Voting_Equipment_VerifiedVoting.csv]({RAW}IL_108_Authority_Voting_Equipment_VerifiedVoting.csv) (raw download link)\n')
cols=['Jurisdiction','Population 2020','Registered voters (VV)','Marking method','ED tabulator vendor','ED tabulator equipment','Mail tabulator equipment','Accessible device','Paper record / VVPAT','Software/firmware','Status','Source','Notes']
def row(r):
    v=[r[c] for c in cols]; v[1]=n(v[1]) if v[1] else '—'; v[2]=n(v[2]); v[11]=f'[Verifier]({r["Source"]})'; return '| '+' | '.join(x.replace('|','/') for x in v)+' |'
a('### All 102 counties, largest to smallest\n'); a('| '+' | '.join(cols)+' |'); a('|'+' --- |'*len(cols))
for r in EQ:
    if r['Type']=='County': a(row(r))
a('\n### The six municipal boards of election commissioners\n'); a('| '+' | '.join(cols)+' |'); a('|'+' --- |'*len(cols))
for r in EQ:
    if r['Type']!='County': a(row(r))
ch=S['_changed']; none22=[r['Jurisdiction'] for r in EQ if "lists no election-day tabulator" in r['Notes']]
a('\n### Gaps and what Verified Voting does not list\n')
a('- **SBOE county equipment list:** no county-by-county voting-system list from the SBOE was retrieved for this page, so the table relies on Verified Voting alone. If the SBOE publishes one, this table should be cross-checked against it.')
a('- **Software and firmware versions:** Verified Voting\'s public county API has hardware, firmware and software version fields, but they are empty for every machine in all 102 county records retrieved November 24, 2026 (the API call for the Danville board returned a different jurisdiction\'s record, so it was not used). Every row shows "Not listed by Verified Voting." Versions were not inferred from anywhere else.')
a('- **Post-election audit codes:** the county API\'s audit fields are blank in this retrieval. Illinois\'s post-election check is the 5% retabulation in 10 ILCS 5/24B-15 (see the laws table below).')
a(f'- **Missing election-day tabulator:** none. **Missing mail-ballot tabulator:** {S["_mail_missing"] or "none"}. **No accessible device listed:** {S["_acc_missing"] or "none"}.')
a('- **Multiple tabulator vendors in one jurisdiction:** none. **Election-day ballots counted only on a central (batch-fed) scanner:** none. **Hybrid ballot-marking device/tabulator on election day:** none.')
a(f'- **Election-day tabulator changed from 2022 to 2026 in Verified Voting:** {len(ch)} jurisdictions ({", ".join(ch)}). The 2022 model is in each row\'s Notes.' + (f' In {len(none22)} more ({", ".join(none22)}), Verified Voting\'s 2022 record lists no election-day tabulator, so no comparison is possible.' if none22 else ''))
a(f'- **Vendor renamed, same model:** in {len(S["_renamed"])} jurisdictions ({", ".join(S["_renamed"])}) the 2022 record lists "Dominion" and the 2026 record lists "Liberty Vote (Dominion)" for the same tabulator model. That is a change in how the vendor is named, not a change in equipment.')
pb=S['_poll']; a(f'- **Paper poll books:** {pb.get("Paper Poll Book",0)} jurisdictions list a paper poll book rather than an electronic one.')
a('- Nearly every jurisdiction also lists a remote ballot-marking system (Democracy Live) for military, overseas, and voters with disabilities. That is a special-purpose channel, not the ordinary in-person or mail tabulator, and is omitted from the vendor counts above.\n')
# graphics
a('## Graphics\n')
a(f'Charts and shareable graphics built from this wiki\'s data. Tap an image to open it full size. The full chart set, with captions, is on [Graphs]({WIKI}Graphs).\n')
a('### The locked Surplus Equation\n')
a(f'[![Illinois Surplus Equation, locked 2022 fit]({RAW}charts/il_surplus_equation_locked_UNOFFICIAL2026.png)]({RAW}charts/il_surplus_equation_locked_UNOFFICIAL2026.png)\n')
a('*S = -24.769946 × (D/100) + 12.831550, fitted on all 102 counties, 2022 SBOE official data (R² = 0.238576). D is the Democratic primary ballot share stand-in, not registration. The 2026\\* line is unofficial and shown for comparison only.*\n')
a('### Charts from the Graphs page\n')
for t,fn in [('Share-form fits, 2022 and 2026*','il_share_form_fits_UNOFFICIAL.png'),('Stand-in vs Democratic share of ballots','il_gap_standin_vs_dem_share_UNOFFICIAL.png'),('Democratic share 2022 vs 2026*','il_dem_share_2022_vs_2026_UNOFFICIAL.png'),('Change-vs-drop fit (original form, kept for reference)','il_fit_share_change_vs_standin_drop_UNOFFICIAL.png'),('Implied extra votes by county*','il_implied_extra_votes_UNOFFICIAL.png')]:
    a(f'- [{t.replace("*","\\*")}]({RAW}charts/{fn})')
a('\n### Flip counties: lower Democratic primary share, higher Democratic vote share\n')
a('Morissa asked for graphics of the ten highest vote-flip counties, ranked the way the Kansas Resources page ranks them. **Illinois does not have ten.** Here is exactly what the data show, for the 80 counties with usable 2026\\* results:\n')
a('- **The Kansas test, applied literally (0 of 80 counties).** Kansas ranks counties where the number of registered Democrats went down while Democratic votes went up. Illinois has no registered Democrats, so the literal analog is the number of Democratic primary ballots. Only 4 of the 80 counties cast fewer Democratic primary ballots in 2026 than in 2022 (Mercer, Moultrie, Hamilton, Gallatin), and in all 4 the Democratic vote for governor also fell. **No Illinois county passes the Kansas headcount test.**')
a('- **The stand-in test (4 of 80 counties).** Illinois\'s stand-in is a share, not a headcount, so the matching test is: the Democratic primary ballot share went **down** while the Democratic share of ballots cast for governor went **up**. Four counties pass. They are shown below, ranked by the value.\n')
a('**How they are ranked.** The ranking value is the number of Democratic votes **beyond what the change in the stand-in would predict**, the Kansas formula with shares in place of headcounts:\n')
a('`Value = D votes 2026* − ballots cast 2026* × Dem share of ballots 2022 × (stand-in 2026 ÷ stand-in 2022)`\n')
a('In plain terms: if the county\'s 2022 Democratic share of ballots had risen or fallen by the same percentage as its Democratic primary share, how many Democratic votes would 2026 have had? The value is how many more there actually were. Value is rounded to the nearest vote. 22 counties have no usable 2026\\* results yet and could not be tested; they are listed on [Bottom-Up Reverse Math](' + WIKI + 'Reverse-Math).\n')
a(f'[![Flip-county summary]({RAW}resources/IL_Flip_00_Summary.png)]({RAW}resources/IL_Flip_00_Summary.png)\n')
a('| Rank | County | Population (2020) | Dem primary share (stand-in) 2022 → 2026 | Dem share of ballots 2022 → 2026\\* | Dem governor votes 2022 → 2026\\* | Value (votes beyond the stand-in)\\* | Share of 2026\\* ballots | Graphic |')
a('|---|---|---|---|---|---|---|---|---|')
fn=lambda r:f'IL_Flip_{r["rank"]:02d}_{r["county"].replace(" ","_").replace(".","")}.png'
for r in FL:
    a(f'| {r["rank"]} | {r["county"]} | {n(r["pop"])} | {r["R22"]:.2f}% → {r["R26"]:.2f}% ({r["dR"]:+.2f} pts) | {r["S22"]:.2f}% → {r["S26"]:.2f}%\\* ({r["dS"]:+.2f} pts\\*) | {n(r["d22"])} → {n(r["d26"])}\\* ({r["dvotes"]:+,}\\*) | **+{n(r["value"])}\\*** | {r["pct"]:.1f}% | [PNG]({RAW}resources/{fn(r)}) |')
a(f'\nData file: [IL_Flip_Counties.csv]({BLOB}resources/IL_Flip_Counties.csv). Two independent passes (Pass A from the verified county tables in floating point; Pass B from the separately parsed raw files in exact fractions) agreed on all {n(FV["cells"])} cells for the 80 counties, with {FV["mismatches"]} mismatches. In Mercer and Edgar the Democratic vote count itself fell; only its share of ballots rose. This is an observation about the numbers. Candidate choice, turnout, which primaries were contested, and voters crossing party lines can all move the value, and the arithmetic cannot separate those from other causes.\n')
a('#### The four graphics\n')
for r in FL:
    a(f'**{r["rank"]}. {r["county"]} County**: Democratic primary share {r["R22"]:.2f}% → {r["R26"]:.2f}% ({r["dR"]:+.2f} points); Democratic share of ballots {r["S22"]:.2f}% → {r["S26"]:.2f}%\\* ({r["dS"]:+.2f} points\\*); value +{n(r["value"])}\\*.\n')
    a(f'[![{r["county"]} County]({RAW}resources/{fn(r)})]({RAW}resources/{fn(r)})\n')
post=open(P+'social/guarantee_clause_post.md').read().split('> ')[1].split('\n')[0]
a('### Did you know? The Guarantee Clause\n')
a(f'[![Guarantee Clause graphic]({RAW}resources/IL_Guarantee_Clause.png)]({RAW}resources/IL_Guarantee_Clause.png)\n')
a(f'**Post text: DRAFT, NOT POSTED ({len(post)} characters; X\'s limit is 280):**\n')
a(f'> {post}\n')
a(f'Draft and citation check: [social/guarantee_clause_post.md]({BLOB}social/guarantee_clause_post.md).\n')
a('**Sources**\n')
a('- U.S. Constitution, Article IV, Section 4: "The United States shall guarantee to every State in this Union a Republican Form of Government, and shall protect each of them against Invasion; and on Application of the Legislature, or of the Executive (when the Legislature cannot be convened) against domestic Violence."')
a('- [Executive Order 14399, "Ensuring Citizenship Verification and Integrity in Federal Elections"](https://www.federalregister.gov/documents/2026/04/03/2026-06601/ensuring-citizenship-verification-and-integrity-in-federal-elections), signed March 31, 2026, published April 3, 2026 at 91 FR 17125 ([official PDF](https://www.govinfo.gov/content/pkg/FR-2026-04-03/pdf/2026-06601.pdf)). Its opening cites "the Federal Government\'s constitutional obligation to guarantee a republican form of Government to every State in the Union, U.S. Const. Art. IV, Sec. 4." Section 1 says: "The Federal Government has an unavoidable duty under Article II of the Constitution of the United States to enforce Federal law." The "unavoidable duty" language is tied to Article II, not to the Guarantee Clause itself.')
a('- Morissa Benson\'s write-up: [The Election Equation. And Plan.](https://moebenson.substack.com/p/the-election-equation-and-plan)\n')
a('## Where the method began: the Cedar County audit\n')
a('The method was first worked out in Morissa Benson\'s [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) in her Nebraska Election Analysis wiki. This Illinois wiki applies the same approach using Illinois\'s own numbers only.\n')
a('## The reverse-factoring method in brief\n')
a('1. **Two shares per county, per year.** For each of the 102 counties, in 2022 and in 2026\\*, take (a) the Democratic share of all ballots cast (Pritzker votes ÷ total ballots cast) and (b) **D**, the Democratic share of primary ballots in that year\'s general primary. Illinois has no party registration, so D is a **stand-in for Democratic registration share, NOT official party registration**.')
a('2. **The surplus, S.** S = (a) − D, in percentage points: the Democratic share of ballots cast minus the Democratic primary share.')
a('3. **The Illinois line.** Graph every county\'s surplus against its D and fit one straight line: **S = multiplier × (D/100) + offset**. Illinois\'s own counties, weighted equally, give:')
a('   - **2022 (locked, official, all 102 counties):** S = -24.769946 × (D/100) + 12.831550, R² 0.238576, mean absolute residual 4.756273 points')
a('   - **2026\\* (unofficial, 80 counties):** S = -23.943680 × (D/100) + 7.950292, R² 0.569513. The 2026 line uses unofficial figures and will be refit after the December 4 canvass.')
a(f'4. **Residuals, floor and ceiling.** A county\'s residual is its actual surplus minus the surplus the line predicts. See [Floor and Ceiling Counties]({WIKI}Floor-and-Ceiling) and [Locked Illinois Formula]({WIKI}Locked-Illinois-Formula).')
a('5. **Checked against the source.** Two independent programs rebuilt every county figure from the raw SBOE and county files and agreed, with 0 mismatches.\n')
a(f'The [README]({WIKI}README) explains it all in plain language. This is an analytical model, with evidence for and against. It is not proof of anything.\n')
a('## Illinois laws cited in the Attorney General letter\n')
I='https://www.ilga.gov/legislation/ilcs/documents/'
a('| Law | What it covers | Official text |'); a('|---|---|---|')
for law,what,u in [('5 ILCS 140/1','Freedom of Information Act policy: all persons are entitled to full and complete information regarding the affairs of government','000501400K1.htm'),
 ('5 ILCS 140/1.2','All records of a public body are presumed open; the public body must prove an exemption by clear and convincing evidence','000501400K1.2.htm'),
 ('5 ILCS 140/2(c)','"Public records" include electronic data processing records and recorded information, regardless of physical form','000501400K2.htm'),
 ('5 ILCS 140/3(d)','Comply with or deny a request within 5 business days, unless properly extended','000501400K3.htm'),
 ('5 ILCS 140/7(1)','Exemptions, including information specifically prohibited from disclosure by federal or State law; exempt information may be redacted and the rest must be released. No exemption names ballots or cast vote records','000501400K7.htm'),
 ('5 ILCS 140/9','Written denial with reasons, a detailed factual basis, and notice of the right to Public Access Counselor review','000501400K9.htm'),
 ('5 ILCS 140/9.5','Public Access Counselor in the Attorney General\'s office: requests for review, binding opinions, advisory opinions to public bodies','000501400K9.5.htm'),
 ('10 ILCS 5/17-20','Election authority preserves ballots for 2 months, subject to discovery recount, then destroys them unless a contest is pending','001000050K17-20.htm'),
 ('10 ILCS 5/24B-9','Pre-election and public testing of precinct optical-scan equipment; post-count re-run; test materials and programs sealed and retained 60 days','001000050K24B-9.htm'),
 ('10 ILCS 5/24B-15','Printed precinct return is the official return; 5% retabulation of precincts and early-voting devices; comparisons open to the public; court order needed to unseal ballots after the proclamation','001000050K24B-15.htm')]:
    a(f'| {law} | {what} | [{law}]({I}{u}) |')
a('\n## Federal sources cited\n')
a('- [U.S. Constitution](https://www.archives.gov/founding-docs/constitution-transcript): Article IV, § 4 (Guarantee Clause) and Article II, § 3 (Take Care)')
a('- Executive Order 14399, "Ensuring Citizenship Verification and Integrity in Federal Elections," signed March 31, 2026, 91 Fed. Reg. 17125: [Federal Register](https://www.federalregister.gov/documents/2026/04/03/2026-06601/ensuring-citizenship-verification-and-integrity-in-federal-elections) · [official PDF](https://www.govinfo.gov/content/pkg/FR-2026-04-03/pdf/2026-06601.pdf)')
a('- 52 U.S.C. § 20701 (22-month retention of federal election records): [Cornell LII](https://www.law.cornell.edu/uscode/text/52/20701)')
a('- Clerk letters, litigation context: *California v. Trump*, No. 1:25-cv-10810 (D. Mass.) [judgment and permanent injunction, July 13, 2026 (PDF)](https://storage.courtlistener.com/recap/gov.uscourts.mad.282905/gov.uscourts.mad.282905.194.0.pdf); *LULAC v. Executive Office of the President*, No. 1:25-cv-0946 (D.D.C.) [order of Oct. 31, 2025 (PDF)](https://storage.courtlistener.com/recap/gov.uscourts.dcd.279032/gov.uscourts.dcd.279032.217.0.pdf)\n')
a('## Morissa Benson on Substack\n')
a('- [The Back Room](https://moebenson.substack.com/p/the-back-room)')
a('- [Who Holds The Keys](https://moebenson.substack.com/p/who-holds-the-keys)')
a('- [The Election Equation. And Plan.](https://moebenson.substack.com/p/the-election-equation-and-plan)')
a('- [Morissa Benson\'s Substack](https://moebenson.substack.com/) (home page)\n')
a('---')
a('*2026 figures are UNOFFICIAL until the Illinois State Board of Elections completes its canvass (scheduled for December 4, 2026). Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.*')
open(P+'wiki/Resources.md','w').write('\n'.join(o)+'\n'); print(len(o))
