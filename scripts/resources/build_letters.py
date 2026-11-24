"""108 Illinois election-authority letters. Figures: verified pass-A county tables (SBOE 2022 general; SBOE 2022/2026 primary canvasses;
2026 UNOFFICIAL county/municipal election-authority postings). Addressees: SBOE Election Authorities list (retrieved 2026-11-24)."""
import csv, json, os, re
O='/workspace/il_publish/out/'; R='/workspace/il-resources/'
EA=list(csv.DictReader(open(R+'raw/sboe/election_authorities_RETRIEVED.csv')))
g22={r['county']:r for r in csv.DictReader(open(O+'il_2022_governor_by_county_VERIFIED.csv'))}
key={r['county']:r['county_key'] for r in csv.DictReader(open(O+'il_governor_reverse_math_2022_2026_VERIFIED.csv'))}
rm={r['county']:r for r in csv.DictReader(open(O+'il_governor_reverse_math_2022_2026_VERIFIED.csv'))}
px={r['county_key']:r for r in csv.DictReader(open(O+'proxy_primary_pass_a.csv'))}
g26={r['county_key']:r for r in csv.DictReader(open(O+'pass_a_2026_raw.csv'))}
EQ={r['Jurisdiction']:r for r in csv.DictReader(open('/workspace/il_publish/IL_108_Authority_Voting_Equipment_VerifiedVoting.csv'))}
REG={'Chicago & Cook County':['Cook'],'Collar Counties':['DuPage','Kane','Lake','McHenry','Will'],
'Northern Illinois':['Boone','Bureau','Carroll','DeKalb','Grundy','Jo Daviess','Kankakee','Kendall','LaSalle','Lee','Ogle','Putnam','Stephenson','Whiteside','Winnebago'],
'Western Illinois':['Adams','Brown','Calhoun','Cass','Fulton','Greene','Hancock','Henderson','Henry','Jersey','Knox','Marshall','Mason','McDonough','Menard','Mercer','Morgan','Peoria','Pike','Rock Island','Schuyler','Scott','Stark','Tazewell','Warren','Woodford'],
'Central Illinois':['Champaign','Christian','Clark','Coles','Cumberland','De Witt','Douglas','Edgar','Ford','Iroquois','Livingston','Logan','Macon','Macoupin','McLean','Montgomery','Moultrie','Piatt','Sangamon','Shelby','Vermilion'],
'Southern Illinois':['Alexander','Bond','Clay','Clinton','Crawford','Edwards','Effingham','Fayette','Franklin','Gallatin','Hamilton','Hardin','Jackson','Jasper','Jefferson','Johnson','Lawrence','Madison','Marion','Massac','Monroe','Perry','Pope','Pulaski','Randolph','Richland','Saline','St. Clair','Union','Wabash','Washington','Wayne','White','Williamson']}
c2r={c:r for r,cs in REG.items() for c in cs}
assert len(c2r)==102 and set(c2r)==set(g22), set(g22)^set(c2r)
CITY={'CITY OF BLOOMINGTON':('Bloomington','McLean','City of Bloomington Board of Election Commissioners'),'CITY OF CHICAGO':('Chicago','Cook','Board of Election Commissioners for the City of Chicago'),
'CITY OF DANVILLE':('Danville','Vermilion','City of Danville Board of Election Commissioners'),'CITY OF EAST ST. LOUIS':('East St. Louis','St. Clair','East St. Louis Board of Election Commissioners'),
'CITY OF GALESBURG':('Galesburg','Knox','City of Galesburg Board of Election Commissioners'),'CITY OF ROCKFORD':('Rockford','Winnebago','City of Rockford Board of Election Commissioners')}
def county_of(j):
    m={c.upper().replace(' ','').replace('.',''):c for c in g22}
    return m[j.upper().replace(' ','').replace('.','')]
def tc(n):
    out=[]
    for w in n.split():
        x='-'.join(p.capitalize() for p in w.split('-'))
        x=re.sub(r"^Mc(\w)",lambda m:'Mc'+m.group(1).upper(),x); x=re.sub(r"^O'(\w)",lambda m:"O'"+m.group(1).upper(),x)
        if re.fullmatch(r'(Ii|Iii|Iv)',x): x=x.upper()
        out.append(x)
    return ' '.join(out)
def last(n):
    t=[w for w in n.split() if w.strip('.,').upper() not in ('JR','SR','II','III','IV')]; return t[-1]
def addr(a):
    parts=[p.strip() for p in a.split('|')]; L=[]
    for p in parts:
        m=re.match(r'^(.*), IL (\d{5})',p)
        L.append(f"{tc(m.group(1))}, IL {m.group(2)}" if m else re.sub(r'\bPo Box\b','PO Box',tc(p)).replace('P.o.','P.O.'))
    return L
f=lambda n:f"{int(n):,}"
def ch(a,b,star=''):
    a,b=int(a),int(b); d=b-a; p=100*d/a; s='+' if d>0 else ''
    return f"{f(a)} → {f(b)}{star} ({s}{d:,}{star}, {s}{p:.1f}%{star})".replace('+-','-')
def pts(a,b,star=''):
    d=b-a; s='+' if d>0 else ''
    return f"{a:.2f}% → {b:.2f}%{star} ({s}{d:.2f} points{star})"
P=list(px.values()); SW=f"Statewide, Democratic primary ballots changed {ch(sum(int(r['gp2022_dem_ballots']) for r in P),sum(int(r['gp2026_dem_ballots']) for r in P))} between the March 2022 and March 2026 primaries."
ROOT=R+'letters/clerk/md/'; os.makedirs(ROOT,exist_ok=True)
rows=[]
for e in EA:
    j=e['jurisdiction']; city=CITY.get(j)
    c=CITY[j][1] if city else county_of(j)
    k=key[c]; p=px[k]; a=g22[c]
    name=tc(e['name']); ttl=tc(e['title'])
    if city: office=city[2]; title_line=f"{ttl}, {office}"; heading=f"{city[0].upper()} BOARD OF ELECTION COMMISSIONERS"; place=f"the City of {city[0]}"; fn=f"City_of_{city[0].replace(' ','_').replace('.','')}_Board_of_Election_Commissioners_Letter"
    elif ttl!='County Clerk': office='Peoria County Election Commission'; title_line=f"{ttl}, {office}"; heading='PEORIA COUNTY ELECTION COMMISSION'; place='Peoria County'; fn='Peoria_County_Election_Commission_Letter'
    else: office=f"{c} County Clerk"; title_line=f"County Clerk, {c} County"; heading=f"{c.upper()} COUNTY CLERK"; place=f"{c} County"; fn=f"{c.replace(' ','_').replace('.','')}_County_Clerk_Letter"
    eq=EQ[city[0] and 'City of '+city[0] if city else c]['ED tabulator equipment']
    R22=100*int(p['gp2022_dem_ballots'])/int(p['gp2022_total_ballots']); R26=100*int(p['gp2026_dem_ballots'])/int(p['gp2026_total_ballots'])
    has26=k in g26
    lines=[f"- Democratic primary ballots (the registration stand-in), March 2022 to March 2026 primaries: {ch(p['gp2022_dem_ballots'],p['gp2026_dem_ballots'])}",
           f"- Democratic share of all primary ballots: {pts(R22,R26)}"]
    if has26:
        b=g26[k]; S22=100*int(a['dem_votes'])/int(a['ballots_cast']); S26=100*int(b['dem_votes'])/int(b['ballots_cast'])
        lines+= [f"- Democratic votes for governor, 2022 to 2026: {ch(a['dem_votes'],b['dem_votes'],'*')}", f"- Total ballots cast, 2022 to 2026: {ch(a['ballots_cast'],b['ballots_cast'],'*')}", f"- Democratic share of ballots cast: {pts(S22,S26,'*')}"]
        dr=R26-R22; ds=S26-S22
        pat=('In this county, the Democratic share of primary ballots fell while the Democratic share of ballots cast for governor rose.' if dr<0 and ds>0 else
             'In this county, the Democratic share of primary ballots and the Democratic share of ballots cast for governor both fell.' if dr<0 and ds<0 else
             'In this county, the Democratic share of primary ballots and the Democratic share of ballots cast for governor both rose.' if dr>0 and ds>0 else
             'In this county, the Democratic share of primary ballots rose while the Democratic share of ballots cast for governor fell.' if dr>0 and ds<0 else 'In this county, at least one of these shares did not change.')
    else:
        lines+= [f"- Democratic votes for governor, 2022: {f(a['dem_votes'])}; total ballots cast, 2022: {f(a['ballots_cast'])}", "- 2026 governor results: not included. When these letters were prepared, usable 2026 county results had not been compiled for this county; the State Board of Elections' official canvass is scheduled for December 4, 2026."]
        pat='The 2026 comparison for this county will be added once usable results are available.'
    cityline=(f"Your board conducts elections for voters in {place}, which is part of {c} County. The figures below are county-wide (they include {place} and the rest of {c} County), because the State Board of Elections' 2022 and primary canvasses report by county.\n\n" if city else '')
    md=f"""# {heading} — Election authority letter (records and preservation request)

Date: ______________________

{name}
{title_line}
{chr(10).join(addr(e['address']))}

Re: November 3, 2026 general election — Freedom of Information Act request for existing election records, request to preserve 2026 election records, and request for additional post-election review, {place}

Dear {ttl} {tc(last(e['name']))}:

I am writing as a member of the public concerning election records for the November 3, 2026 general election in {place}, where your office serves as the election authority. {cityline}Using Illinois State Board of Elections figures for the governor race and the primaries, I compared the 2022 and 2026 elections in {c} County:

{chr(10).join(lines)}

Illinois voters do not register by party, so this analysis uses a clearly labeled stand-in for party registration: the Democratic share of primary ballots, from the State Board of Elections' official primary canvasses. It is a stand-in, not party registration. 2022 general-election figures are the State Board of Elections' official canvass. *2026 general-election figures are unofficial results posted by the county or municipal election authority and are not final until the State Board of Elections' canvass, scheduled for December 4, 2026. These are votes for the Democratic candidate, not a count of any group of voters.

{pat} {SW} I offer these figures as an observation, not an allegation. Candidate choice, turnout, which primaries were contested, and voters crossing party lines can all move them, and county totals alone cannot tell those causes apart. The cast vote record, which shows the ballots in their batches, is the record that could.

**Federal litigation context.** Executive Order 14248 (Mar. 25, 2025) was challenged in *California v. Trump*, No. 1:25-cv-10810 (D. Mass.) (summary-judgment order June 24, 2026; judgment and permanent injunction July 13, 2026), and *LULAC v. Executive Office of the President*, No. 1:25-cv-0946 (D.D.C.) (permanent injunction as to Section 2(a), Oct. 31, 2025). This letter does not rely on that litigation for standing or for any new right to records. I mention it only as context: records requests under Illinois law and your office's statutory duties stand independently, however the litigation resolves.

**Records request.** Under the Illinois Freedom of Information Act, 5 ILCS 140 ("public records" include "electronic data processing records, electronic communications, recorded information and all other documentary materials pertaining to the transaction of public business, regardless of physical form or characteristics," 5 ILCS 140/2(c)), I request copies of the following existing records for the November 3, 2026 general election:

- **Cast vote record export:** the full cast vote record (CVR) export for the election, if your office has generated or retained one, including batch identifiers, ballot sequence or position numbers, and all contests (including down-ballot columns), in electronic form, with any information that could identify a voter removed. Verified Voting lists your election-day tabulator as {eq}; please tell me if that has changed.
- **Ballot images:** any ballot images your tabulation system created and your office retains, with any information that could identify a voter removed.
- **Precinct returns:** the precinct return printed by the tabulating equipment, which "shall constitute the official return of each precinct" under 10 ILCS 5/24B-15.
- **Retabulation records:** the comparison of the 5% retabulation with the original precinct returns under 10 ILCS 5/24B-15 (which provides that "the comparisons shall be open to the public"), and the record of the precincts and early-voting devices the State Board of Elections selected.
- **Equipment test records:** the results of the pre-test, the public test, and the post-count re-run of the tabulating equipment and program under 10 ILCS 5/24B-9.
- **Hash verification:** the hash values for the certified voting system version your office used, and any record of hash verification performed on that system, so they can be compared with the trusted build published for the certified version. If no such record exists, please say so.

**Preservation request.** 10 ILCS 5/17-20 directs election authorities to preserve ballots for 2 months, and 10 ILCS 5/24B-9 provides for retention of test materials for 60 days, after which ballots are destroyed unless a contest is pending. Because the November 3, 2026 general election included federal offices, 52 U.S.C. § 20701 requires that records and papers covered by that statute be kept for 22 months. I respectfully ask that your office keep the ballots, cast vote records, ballot images, test materials, and retabulation records for this election for at least the full 22 months, and that no record in this request be destroyed while the request is pending.

**Review request (a request, not a records demand).** 10 ILCS 5/24B-15 requires retabulation of 5% of precincts and 5% of early-voting devices before the proclamation. I ask that your office consider a further hand count covering ballots from precincts representing at least thirty to forty percent of total ballots, prioritizing the precincts with the highest ballot volume, and that the counted ballots be cross-checked against the cast vote record. This is a request, not a claim of statutory entitlement. I recognize that under 10 ILCS 5/24B-15, "after the proclamation of results, the election authority must obtain a court order to unseal voted ballots except for election contests and discovery recounts," so I ask your office to perform or arrange any such count itself, in public and by whatever lawful means is available, and not to let me inspect ballots. If your office concludes it has no authority to do so, I ask that it say so in writing.

This request is limited to records that already exist. Under 5 ILCS 140/3(d), please respond within 5 business days. If any record is withheld in whole or in part, I ask that you give the written notice described in 5 ILCS 140/9, including the specific exemption claimed and the factual basis for it, tell me whether the record exists, and release the remaining information as 5 ILCS 140/7(1) requires. If a record is held by another office, please tell me where. I will pay any fees the Act allows; please tell me the estimated cost before proceeding. I understand that I may ask the Public Access Counselor in the Office of the Attorney General to review a denial under 5 ILCS 140/9.5.

Please confirm the addressee and mailing address if your office's information has changed since the State Board of Elections' list of election authorities was retrieved on November 24, 2026.

Thank you for your time and for the work your office does to conduct elections.

Signature: _______________________________________________

Printed name: _______________________________________________

Address: _______________________________________________

Phone / email: _______________________________________________
"""
    open(ROOT+fn+'.md','w').write(md)
    rows.append(dict(file=fn,jurisdiction=j,type=('Municipal board' if city else 'County election commission' if ttl!='County Clerk' else 'County clerk'),county=c,region=c2r[c],addressee=name,title=ttl,office=office,address=' | '.join(addr(e['address'])),
        dem_primary_2022=p['gp2022_dem_ballots'],dem_primary_2026=p['gp2026_dem_ballots'],standin_2022_pct=round(R22,6),standin_2026_pct=round(R26,6),dem_votes_2022=a['dem_votes'],ballots_2022=a['ballots_cast'],
        dem_votes_2026_UNOFFICIAL=g26[k]['dem_votes'] if has26 else '',ballots_2026_UNOFFICIAL=g26[k]['ballots_cast'] if has26 else '',ed_equipment=eq))
w=csv.DictWriter(open(R+'out/letter_merge_fields.csv','w',newline=''),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
json.dump(REG,open(R+'out/regions.json','w'),indent=1)
print(len(rows), SW); print(sum(1 for r in rows if r['dem_votes_2026_UNOFFICIAL']))
