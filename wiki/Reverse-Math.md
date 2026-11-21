# Reverse Math — county by county (sorted by 2020 population, largest → smallest)
> **2026 figures are UNOFFICIAL (pre-Dec 4, 2026 canvass).** 2022 figures are SBOE official canvass.
>
> **Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.**

## Definitions
- **Dem share** = Pritzker votes ÷ ballots cast (county total ballots, not the governor-contest total).
- **Stand-in share** = Democratic primary ballots ÷ all primary ballots (SBOE primary canvass). *Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration.*
- **Gap** = Dem share − stand-in share (same year).
- **Stand-in drop** = stand-in 2022 − stand-in 2026 (negative = the stand-in rose).
- **Share change** = Dem share 2026 − Dem share 2022. **Delta-G** = share change − stand-in change = gap 2026 − gap 2022.
- **Expected change** = 0.000194 + (-0.205049) × stand-in drop (see [[Locked-Illinois-Formula]]).
- **Residual** = share change − expected change. **Implied extra votes** = residual × 2026 ballots cast. Positive = more Dem share than the stand-in predicts; negative = less.

### Registration stand-in evaluation (Morissa's rule: best available comparable number, not the easiest)
Illinois has **no party registration** (SBOE registration file lists only active/inactive voters per authority). Three candidates were evaluated:

| Option | Coverage | Accuracy as a party-strength measure | Defensibility / citability | Verdict |
|---|---|---|---|---|
| 1. SBOE Democratic primary ballot share (Dem ballots ÷ all primary ballots, per county) | All 102 counties, both 2022 and 2026, one uniform official source | Moderate: measures who *chose a Democratic ballot* in that primary; sensitive to which primaries were contested | Highest: SBOE official canvass PDFs (`2022GPOfficialVote.pdf`, `2026GPOfficialVote.pdf`), reproducible by anyone | **CHOSEN** |
| 2. Party of last primary voted, from county voter files | Not statewide: only some of Illinois' 108 election authorities publish D/R/NPP counts (e.g. Kane); others publish nothing or charge for files | Similar signal to option 1 (it is derived from the same primary choices), but mixed vintages and definitions | Low: inconsistent across counties; cannot cover 102 counties uniformly | Rejected |
| 3. Paid modeled party (L2 / Catalist) | Statewide | Modeled estimate, not a recorded act; method proprietary | Low for a public audit: paid, not reproducible, not citable; **not purchased** | Rejected |

**Caveat — 2022→2026 contest-structure jump.** Statewide the Democratic share of primary ballots went from **51.88%** (911,919 of 1,757,872, June 28, 2022) to **67.87%** (1,283,256 of 1,890,699, March 17, 2026). A 16-point move in one cycle reflects *which primaries were contested* (2022: competitive Republican governor primary; 2026: high-profile Democratic primaries), not a real shift in party loyalty. The stand-in **drop** is therefore negative in most counties, and the fitted multiplier measures how general-election share moved relative to that contest-driven swing. Read results as relative (county vs county), not as registration-based absolutes. Small-county primaries can swing on a single local contest (e.g. Gallatin, a high-leverage point on the fit chart).

## County table — 2026 columns UNOFFICIAL (pre-Dec 4, 2026 canvass)
| County | Pop 2020 | Stand-in 2022 | Stand-in 2026 | Stand-in drop | Dem share 2022 | Gap 2022 | Ballots 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass) | Dem share 2026 UNOFFICIAL (pre-Dec 4, 2026 canvass) | Gap 2026 | Share change | Delta-G | Expected | Residual | Implied extra votes | 2026 source (UNOFFICIAL (pre-Dec 4, 2026 canvass)) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cook | 5,275,541 | 79.25% | 88.29% | -0.090407 | 73.04% | -0.062043 | 1,579,770 | 78.79% | -0.094935 | 0.057515 | -0.032893 | 0.018732 | 0.038783 | 61,267.59 | Cook County Clerk (suburban Cook) (voteclock) + Chicago Board of Election Commissioners (chicago_pdf) |
| DuPage | 932,877 | 43.53% | 68.52% | -0.249812 | 55.45% | 0.119156 | 342,060 | 62.45% | -0.060656 | 0.070000 | -0.179812 | 0.051418 | 0.018582 | 6,356.31 | DuPage County Clerk (voteclock) |
| Lake | 714,342 | 56.34% | 76.37% | -0.200347 | 59.81% | 0.034743 | 231,342 | 66.14% | -0.102379 | 0.063225 | -0.137122 | 0.041275 | 0.021950 | 5,078.01 | Lake County Clerk (voteclock) |
| Will | 696,355 | 45.95% | 63.49% | -0.175412 | 50.02% | 0.040694 | 231,160 | 57.10% | -0.063939 | 0.070779 | -0.104633 | 0.036162 | 0.034617 | 8,002.06 | Will County Clerk (voteclock) |
| Kane | 516,522 | 46.38% | 66.58% | -0.202022 | 53.11% | 0.067367 | 170,356 | 61.37% | -0.052070 | 0.082586 | -0.119437 | 0.041618 | 0.040967 | 6,979.00 | Kane County Clerk (voteclock) |
| McHenry | 310,229 | 33.22% | 61.02% | -0.278044 | 47.11% | 0.138907 | 115,305 | 52.86% | -0.081615 | 0.057522 | -0.220522 | 0.057207 | 0.000316 | 36.39 | McHenry County Clerk (voteclock) |
| Winnebago | 285,350 | 37.86% | 54.58% | -0.167174 | 47.24% | 0.093765 | 90,584 | 53.05% | -0.015307 | 0.058101 | -0.109072 | 0.034473 | 0.023628 | 2,140.35 | Winnebago County Clerk (outside Rockford) (voteclock) + City of Rockford Board of Election Commissioners (clarity) |
| Madison | 265,859 | 34.54% | 51.52% | -0.169776 | 40.36% | 0.058138 | 99,363 | 45.81% | -0.057112 | 0.054526 | -0.115250 | 0.035006 | 0.019519 | 1,939.50 | Madison County Clerk (voteclock) |
| St. Clair | 257,400 | 49.52% | 66.42% | -0.169042 | 50.27% | 0.007535 | 92,772 | 55.60% | -0.108281 | 0.053227 | -0.115815 | 0.034856 | 0.018371 | 1,704.34 | St. Clair County Clerk (outside East St. Louis) (voteclock) + East St. Louis Board of Election Commissioners (platinum) |
| Champaign | 205,865 | 46.40% | 66.64% | -0.202367 | 58.27% | 0.118660 | 69,919 | 63.54% | -0.030956 | 0.052751 | -0.149616 | 0.041689 | 0.011062 | 773.44 | Champaign County Clerk (voteclock) |
| Sangamon | 196,343 | 34.49% | 44.98% | -0.104886 | 47.41% | 0.129254 | 79,457 | 49.83% | 0.048587 | 0.024219 | -0.080667 | 0.021701 | 0.002518 | 200.08 | Sangamon County Clerk (voteclock) |
| Peoria | 181,830 | 39.00% | 60.20% | -0.212043 | 49.08% | 0.100842 | 61,789 | 54.44% | -0.057613 | 0.053588 | -0.158455 | 0.043673 | 0.009915 | 612.64 | Peoria County Election Commission (voteclock) |
| McLean | 170,954 | 34.19% | 57.55% | -0.233636 | 48.84% | 0.146530 | 67,469 | 55.20% | -0.023524 | 0.063581 | -0.170054 | 0.048101 | 0.015481 | 1,044.46 | McLean County Clerk (outside Bloomington) (voteclock) + City of Bloomington Board of Election Commissioners (clarity) |
| Rock Island | 144,672 | 60.71% | 72.03% | -0.113174 | 52.85% | -0.078654 | 48,250 | 58.81% | -0.132163 | 0.059665 | -0.053509 | 0.023400 | 0.036265 | 1,749.77 | Rock Island County Clerk (voteclock) |
| Kendall | 131,869 | 36.47% | 56.95% | -0.204893 | 48.80% | 0.123310 | 49,422 | 56.95% | -0.000004 | 0.081579 | -0.123314 | 0.042207 | 0.039372 | 1,945.86 | Kendall County Clerk (voteclock) |
| Tazewell | 131,343 | 21.59% | 41.20% | -0.196084 | 33.69% | 0.120990 | 51,456 | 36.70% | -0.044998 | 0.030096 | -0.165988 | 0.040401 | -0.010305 | -530.25 | Tazewell County Clerk (pollresults) |
| LaSalle | 109,658 | 31.40% | 50.54% | -0.191405 | 41.48% | 0.100804 | 38,577 | 42.92% | -0.076223 | 0.014378 | -0.177027 | 0.039441 | -0.025064 | -966.88 | LaSalle County Clerk (voteclock) |
| Kankakee | 107,502 | 27.82% | 52.59% | -0.247741 | 37.23% | 0.094157 | — | — | — | — | — | — | — | — | excluded |
| Macon | 103,998 | 25.54% | 38.55% | -0.130110 | 38.68% | 0.131370 | 33,974 | 41.50% | 0.029444 | 0.028185 | -0.101925 | 0.026873 | 0.001312 | 44.58 | Macon County Clerk (pollresults) |
| DeKalb | 100,420 | 38.18% | 58.52% | -0.203413 | 49.12% | 0.109388 | 36,547 | 54.64% | -0.038775 | 0.055250 | -0.148163 | 0.041904 | 0.013346 | 487.77 | DeKalb County Clerk (platinum) |
| Vermilion | 74,188 | 19.84% | 27.96% | -0.081263 | 30.34% | 0.105033 | — | — | — | — | — | — | — | — | excluded |
| Williamson | 67,153 | 20.14% | 21.74% | -0.015983 | 26.93% | 0.067905 | 24,345 | 29.29% | 0.075508 | 0.023586 | 0.007604 | 0.003471 | 0.020115 | 489.70 | Williamson County Clerk (voteclock) |
| Adams | 65,737 | 11.80% | 19.22% | -0.074206 | 20.04% | 0.082329 | 24,600 | 23.02% | 0.037960 | 0.029837 | -0.044369 | 0.015410 | 0.014427 | 354.91 | Adams County Clerk (voteclock) |
| Whiteside | 55,691 | 35.20% | 51.97% | -0.167737 | 41.12% | 0.059205 | 19,498 | 42.11% | -0.098641 | 0.009890 | -0.157846 | 0.034588 | -0.024698 | -481.56 | Whiteside County Clerk (pollresults) |
| Boone | 53,448 | 17.96% | 44.35% | -0.263915 | 38.21% | 0.202490 | 17,962 | 45.46% | 0.011041 | 0.072466 | -0.191449 | 0.054309 | 0.018156 | 326.12 | Boone County Clerk (pollresults) |
| Jackson | 52,974 | 50.26% | 62.75% | -0.124961 | 47.84% | -0.024157 | 18,047 | 52.01% | -0.107397 | 0.041721 | -0.083241 | 0.025817 | 0.015903 | 287.01 | Jackson County Clerk (cumpdf) |
| Grundy | 52,533 | 23.82% | 41.84% | -0.180188 | 35.56% | 0.117437 | 18,671 | 38.51% | -0.033253 | 0.029499 | -0.150690 | 0.037141 | -0.007643 | -142.70 | Grundy County Clerk (voteclock) |
| Ogle | 51,788 | 18.91% | 33.62% | -0.147172 | 33.18% | 0.142680 | 19,641 | 35.11% | 0.014804 | 0.019296 | -0.127876 | 0.030371 | -0.011076 | -217.54 | Ogle County Clerk (pollresults) |
| Knox | 49,967 | 37.80% | 46.32% | -0.085243 | 42.21% | 0.044152 | — | — | — | — | — | — | — | — | excluded |
| Henry | 49,284 | 24.70% | 41.32% | -0.166160 | 35.00% | 0.102980 | 19,508 | 36.72% | -0.045952 | 0.017229 | -0.148932 | 0.034265 | -0.017036 | -332.34 | Henry County Clerk (platinum) |
| Coles | 46,863 | 16.31% | 34.48% | -0.181728 | 33.20% | 0.168917 | 16,885 | 35.29% | 0.008030 | 0.020841 | -0.160887 | 0.037457 | -0.016616 | -280.56 | Coles County Clerk (pollresults) |
| Macoupin | 44,967 | 30.43% | 27.94% | 0.024869 | 30.45% | 0.000213 | 17,599 | 29.64% | 0.016951 | -0.008131 | 0.016737 | -0.004905 | -0.003226 | -56.77 | Macoupin County Clerk (clarity) |
| Stephenson | 44,630 | 24.61% | 31.32% | -0.067148 | 37.23% | 0.126155 | 16,000 | 38.74% | 0.074191 | 0.015184 | -0.051964 | 0.013963 | 0.001221 | 19.54 | Stephenson County Clerk (pollresults) |
| Woodford | 38,467 | 12.55% | 30.14% | -0.175911 | 25.43% | 0.128777 | 16,366 | 27.26% | -0.028832 | 0.018301 | -0.157609 | 0.036264 | -0.017963 | -293.98 | Woodford County Clerk (el45) |
| Franklin | 37,804 | 18.34% | 23.91% | -0.055707 | 21.27% | 0.029280 | 13,157 | 22.14% | -0.017735 | 0.008692 | -0.047015 | 0.011617 | -0.002924 | -38.48 | Franklin County Clerk (platinum) |
| Marion | 37,729 | 12.58% | 19.93% | -0.073553 | 21.82% | 0.092466 | 13,462 | 22.09% | 0.021604 | 0.002691 | -0.070863 | 0.015276 | -0.012586 | -169.43 | Marion County Clerk (platinum) |
| Jefferson | 37,113 | 15.08% | 23.79% | -0.087091 | 21.16% | 0.060863 | — | — | — | — | — | — | — | — | excluded |
| Clinton | 36,899 | 13.62% | 17.64% | -0.040176 | 20.80% | 0.071839 | 14,671 | 21.49% | 0.038532 | 0.006870 | -0.033306 | 0.008432 | -0.001562 | -22.92 | Clinton County Clerk (platinum) |
| Livingston | 35,815 | 8.43% | 19.15% | -0.107124 | 24.97% | 0.165324 | 12,602 | 25.85% | 0.066977 | 0.008777 | -0.098347 | 0.022160 | -0.013382 | -168.65 | Livingston County Clerk (pollresults) |
| Monroe | 34,962 | 20.16% | 25.68% | -0.055193 | 29.12% | 0.089550 | — | — | — | — | — | — | — | — | excluded |
| Effingham | 34,668 | 8.30% | 15.37% | -0.070712 | 16.24% | 0.079440 | — | — | — | — | — | — | — | — | excluded |
| Lee | 34,145 | 19.81% | 39.91% | -0.201052 | 37.34% | 0.175277 | 12,270 | 37.89% | -0.020239 | 0.005536 | -0.195516 | 0.041419 | -0.035884 | -440.30 | Lee County Clerk (pollresults) |
| Christian | 34,032 | 19.15% | 20.64% | -0.014961 | 27.38% | 0.082340 | 11,808 | 26.30% | 0.056602 | -0.010777 | -0.025738 | 0.003262 | -0.014039 | -165.77 | Christian County Clerk (pollresults) |
| Fulton | 33,609 | 34.86% | 39.66% | -0.048077 | 37.11% | 0.022503 | 12,163 | 36.36% | -0.033075 | -0.007501 | -0.055578 | 0.010052 | -0.017553 | -213.50 | Fulton County Clerk (cumpdf) |
| Bureau | 33,244 | 25.18% | 40.03% | -0.148483 | 36.01% | 0.108354 | 12,195 | 35.69% | -0.043395 | -0.003266 | -0.151749 | 0.030640 | -0.033906 | -413.49 | Bureau County Clerk (pollresults) |
| Morgan | 32,915 | 15.97% | 27.86% | -0.118944 | 31.08% | 0.151138 | — | — | — | — | — | — | — | — | excluded |
| Randolph | 30,163 | 15.95% | 23.30% | -0.073551 | 25.94% | 0.099918 | 10,749 | 23.65% | 0.003470 | -0.022897 | -0.096448 | 0.015276 | -0.038173 | -410.32 | Randolph County Clerk (platinum) |
| Montgomery | 28,288 | 19.82% | 33.52% | -0.136995 | 27.90% | 0.080831 | — | — | — | — | — | — | — | — | excluded |
| Logan | 27,987 | 12.14% | 22.26% | -0.101195 | 27.71% | 0.155763 | 9,665 | 27.45% | 0.051924 | -0.002643 | -0.103839 | 0.020944 | -0.023587 | -227.97 | Logan County Clerk (pollresults) |
| McDonough | 27,238 | 23.38% | 22.65% | 0.007270 | 34.14% | 0.107624 | — | — | — | — | — | — | — | — | excluded |
| Iroquois | 27,077 | 8.23% | 16.95% | -0.087220 | 18.39% | 0.101589 | — | — | — | — | — | — | — | — | excluded |
| Saline | 23,768 | 20.50% | 13.71% | 0.067871 | 21.03% | 0.005307 | — | — | — | — | — | — | — | — | excluded |
| Jo Daviess | 22,035 | 30.01% | 46.50% | -0.164881 | 39.20% | 0.091952 | — | — | — | — | — | — | — | — | excluded |
| Jersey | 21,512 | 14.81% | 23.07% | -0.082629 | 22.83% | 0.080191 | 8,821 | 24.24% | 0.011649 | 0.014087 | -0.068542 | 0.017137 | -0.003050 | -26.91 | Jersey County Clerk (el45) |
| Fayette | 21,488 | 8.69% | 13.72% | -0.050239 | 15.82% | 0.071308 | 7,774 | 14.97% | 0.012555 | -0.008514 | -0.058753 | 0.010496 | -0.019009 | -147.78 | WMIX radio transcription of Fayette County Clerk results (radio_wmix) |
| Shelby | 20,990 | 11.29% | 14.24% | -0.029480 | 19.18% | 0.078828 | 9,317 | 17.74% | 0.035005 | -0.014344 | -0.043823 | 0.006239 | -0.020583 | -191.77 | Shelby County Clerk (pollresults) |
| Perry | 20,945 | 19.74% | 19.98% | -0.002447 | 23.07% | 0.033299 | — | — | — | — | — | — | — | — | excluded |
| Douglas | 19,740 | 10.78% | 17.45% | -0.066634 | 23.74% | 0.129576 | — | — | — | — | — | — | — | — | excluded |
| Crawford | 18,679 | 13.09% | 14.80% | -0.017135 | 19.44% | 0.063543 | — | — | — | — | — | — | — | — | excluded |
| Hancock | 17,620 | 11.55% | 12.27% | -0.007218 | 19.70% | 0.081501 | — | — | — | — | — | — | — | — | excluded |
| Union | 17,244 | 19.67% | 28.05% | -0.083786 | 25.92% | 0.062553 | — | — | — | — | — | — | — | — | excluded |
| Edgar | 16,866 | 13.06% | 10.14% | 0.029199 | 21.94% | 0.088782 | 5,854 | 22.45% | 0.123020 | 0.005040 | 0.034238 | -0.005793 | 0.010833 | 63.42 | Edgar County Clerk (pollresults) |
| Warren | 16,835 | 24.07% | 21.75% | 0.023163 | 33.83% | 0.097638 | — | — | — | — | — | — | — | — | excluded |
| Bond | 16,725 | 19.87% | 25.17% | -0.052997 | 25.79% | 0.059181 | 6,297 | 25.39% | 0.002203 | -0.003981 | -0.056978 | 0.011061 | -0.015042 | -94.72 | Bond County Clerk (pollresults) |
| Piatt | 16,673 | 19.37% | 35.63% | -0.162677 | 33.58% | 0.142180 | 7,485 | 35.14% | -0.004961 | 0.015536 | -0.147141 | 0.033551 | -0.018015 | -134.84 | Piatt County Clerk (pollresults) |
| Wayne | 16,179 | 4.89% | 6.34% | -0.014469 | 9.38% | 0.044863 | 6,638 | 11.93% | 0.055929 | 0.025536 | 0.011067 | 0.003161 | 0.022375 | 148.53 | Wayne County Clerk (platinum) |
| Richland | 15,813 | 13.94% | 20.42% | -0.064725 | 18.66% | 0.047218 | 5,859 | 21.64% | 0.012266 | 0.029773 | -0.034952 | 0.013466 | 0.016308 | 95.55 | Richland County Clerk (cumpdf) |
| Carroll | 15,702 | 21.94% | 23.73% | -0.017925 | 30.77% | 0.088353 | 6,205 | 30.25% | 0.065183 | -0.005245 | -0.023170 | 0.003869 | -0.009114 | -56.56 | Carroll County Clerk (pollresults) |
| Mercer | 15,699 | 33.32% | 27.17% | 0.061449 | 33.59% | 0.002721 | — | — | — | — | — | — | — | — | excluded |
| De Witt | 15,516 | 13.70% | 15.07% | -0.013677 | 25.85% | 0.121443 | 5,970 | 27.37% | 0.122980 | 0.015215 | 0.001538 | 0.002999 | 0.012216 | 72.93 | DeWitt County Clerk (pollresults) |
| Clark | 15,455 | 11.64% | 24.76% | -0.131193 | 18.94% | 0.072974 | 6,378 | 20.90% | -0.038606 | 0.019613 | -0.111580 | 0.027095 | -0.007482 | -47.72 | Clark County Clerk (pollresults) |
| Lawrence | 15,280 | 8.43% | 23.68% | -0.152459 | 17.63% | 0.091978 | — | — | — | — | — | — | — | — | excluded |
| Pike | 14,739 | 11.69% | 13.92% | -0.022280 | 15.90% | 0.042093 | 5,881 | 15.64% | 0.017273 | -0.002540 | -0.024820 | 0.004763 | -0.007303 | -42.95 | Pike County Clerk (platinum) |
| Moultrie | 14,526 | 14.79% | 21.83% | -0.070488 | 23.39% | 0.086005 | 5,065 | 23.47% | 0.016401 | 0.000885 | -0.069603 | 0.014648 | -0.013763 | -69.71 | Moultrie County Clerk (pollresults) |
| Massac | 14,169 | 12.63% | 12.22% | 0.004082 | 21.23% | 0.086003 | — | — | — | — | — | — | — | — | excluded |
| White | 13,877 | 10.48% | 9.12% | 0.013586 | 15.13% | 0.046454 | — | — | — | — | — | — | — | — | excluded |
| Washington | 13,761 | 12.41% | 15.07% | -0.026567 | 19.26% | 0.068499 | — | — | — | — | — | — | — | — | excluded |
| Ford | 13,534 | 9.85% | 18.61% | -0.087622 | 23.63% | 0.137808 | 4,872 | 24.98% | 0.063716 | 0.013529 | -0.074093 | 0.018161 | -0.004632 | -22.57 | Ford County Clerk (pollresults) |
| Johnson | 13,308 | 9.79% | 10.60% | -0.008018 | 17.77% | 0.079781 | — | — | — | — | — | — | — | — | excluded |
| Clay | 13,288 | 6.18% | 11.50% | -0.053227 | 13.30% | 0.071233 | — | — | — | — | — | — | — | — | excluded |
| Mason | 13,086 | 28.47% | 37.58% | -0.091033 | 29.06% | 0.005899 | 4,931 | 27.82% | -0.097530 | -0.012396 | -0.103429 | 0.018860 | -0.031256 | -154.12 | Mason County Clerk (pollresults) |
| Cass | 13,042 | 28.25% | 24.88% | 0.033676 | 27.23% | -0.010208 | — | — | — | — | — | — | — | — | excluded |
| Menard | 12,297 | 13.32% | 21.24% | -0.079198 | 29.30% | 0.159770 | — | — | — | — | — | — | — | — | excluded |
| Greene | 11,985 | 16.31% | 14.15% | 0.021598 | 20.48% | 0.041660 | — | — | — | — | — | — | — | — | excluded |
| Marshall | 11,742 | 15.83% | 29.05% | -0.132242 | 30.59% | 0.147624 | — | — | — | — | — | — | — | — | excluded |
| Wabash | 11,361 | 13.09% | 16.56% | -0.034638 | 17.80% | 0.047073 | — | — | — | — | — | — | — | — | excluded |
| Cumberland | 10,450 | 10.39% | 11.47% | -0.010805 | 17.97% | 0.075741 | — | — | — | — | — | — | — | — | excluded |
| Jasper | 9,287 | 10.31% | 15.21% | -0.048950 | 13.73% | 0.034134 | 4,639 | 13.06% | -0.021447 | -0.006632 | -0.055581 | 0.010231 | -0.016863 | -78.23 | Jasper County Clerk (cumpdf) |
| Hamilton | 7,993 | 14.53% | 15.35% | -0.008209 | 16.39% | 0.018594 | 3,379 | 15.74% | 0.003955 | -0.006431 | -0.014640 | 0.001877 | -0.008308 | -28.07 | WEBQ radio transcription of Hamilton County Clerk report (radio_webq_b) |
| Schuyler | 6,902 | 13.91% | 18.72% | -0.048064 | 24.92% | 0.110021 | — | — | — | — | — | — | — | — | excluded |
| Henderson | 6,387 | 19.05% | 17.00% | 0.020531 | 29.43% | 0.103797 | — | — | — | — | — | — | — | — | excluded |
| Edwards | 6,245 | 5.27% | 9.32% | -0.040524 | 10.43% | 0.051673 | — | — | — | — | — | — | — | — | excluded |
| Brown | 6,244 | 11.53% | 14.47% | -0.029469 | 15.64% | 0.041142 | — | — | — | — | — | — | — | — | excluded |
| Putnam | 5,637 | 37.75% | 53.91% | -0.161660 | 37.93% | 0.001876 | 2,482 | 39.08% | -0.148317 | 0.011467 | -0.150193 | 0.033342 | -0.021875 | -54.29 | Putnam County Clerk (pollresults) |
| Stark | 5,400 | 10.92% | 26.25% | -0.153330 | 25.28% | 0.143581 | — | — | — | — | — | — | — | — | excluded |
| Alexander | 5,240 | 66.28% | 56.50% | 0.097872 | 40.47% | -0.258087 | — | — | — | — | — | — | — | — | excluded |
| Pulaski | 5,193 | 26.59% | 24.57% | 0.020248 | 28.50% | 0.019105 | — | — | — | — | — | — | — | — | excluded |
| Scott | 4,949 | 10.65% | 8.67% | 0.019748 | 17.67% | 0.070225 | — | — | — | — | — | — | — | — | excluded |
| Gallatin | 4,946 | 44.69% | 21.56% | 0.231355 | 19.38% | -0.253130 | 2,088 | 19.25% | -0.023061 | -0.001287 | 0.230069 | -0.047245 | 0.045958 | 95.96 | WEBQ radio transcription of Gallatin County Clerk results (radio_webq_a) |
| Calhoun | 4,437 | 41.52% | 31.91% | 0.096080 | 23.86% | -0.176556 | — | — | — | — | — | — | — | — | excluded |
| Pope | 3,763 | 11.17% | 11.55% | -0.003809 | 17.87% | 0.067011 | — | — | — | — | — | — | — | — | excluded |
| Hardin | 3,649 | 10.50% | 22.21% | -0.117006 | 16.44% | 0.059398 | — | — | — | — | — | — | — | — | excluded |

Full precision, URLs and as-of times: [`out/il_governor_reverse_math_2022_2026_VERIFIED.csv`](https://github.com/mbenson8989/Illinois-Election-Analysis/blob/main/out/il_governor_reverse_math_2022_2026_VERIFIED.csv).

## 2026 counties excluded (42) — no county-authority ballots-cast figure in hand
No aggregator ballots-cast figures were substituted. These counties have 2022 values only.

| County | Pop 2020 | Reason |
|---|---|---|
| Kankakee | 107,502 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Vermilion | 74,188 | county clerk file found (pollresults) but City of Danville Election Commission results not retrieved |
| Knox | 49,967 | Galesburg Board file found but Knox County Clerk (outside Galesburg) results not retrieved |
| Jefferson | 37,113 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Monroe | 34,962 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Effingham | 34,668 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Morgan | 32,915 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Montgomery | 28,288 | no county-authority 2026 ballots-cast figure collected before cutoff |
| McDonough | 27,238 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Iroquois | 27,077 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Saline | 23,768 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Jo Daviess | 22,035 | county official-results PDF is an image scan (no text layer) |
| Perry | 20,945 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Douglas | 19,740 | county pollresults feed holds no 2026 ballots-cast total |
| Crawford | 18,679 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Hancock | 17,620 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Union | 17,244 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Warren | 16,835 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Mercer | 15,699 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Lawrence | 15,280 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Massac | 14,169 | no county-authority 2026 ballots-cast figure collected before cutoff |
| White | 13,877 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Washington | 13,761 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Johnson | 13,308 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Clay | 13,288 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Cass | 13,042 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Menard | 12,297 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Greene | 11,985 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Marshall | 11,742 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Wabash | 11,361 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Cumberland | 10,450 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Schuyler | 6,902 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Henderson | 6,387 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Edwards | 6,245 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Brown | 6,244 | county summary PDF is an image scan (no text layer) |
| Stark | 5,400 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Alexander | 5,240 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Pulaski | 5,193 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Scott | 4,949 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Calhoun | 4,437 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Pope | 3,763 | no county-authority 2026 ballots-cast figure collected before cutoff |
| Hardin | 3,649 | only local-office results located; no governor contest |

## 2026 source disagreements (UNOFFICIAL (pre-Dec 4, 2026 canvass))
Where a voteclock.org transcription of a county page and the county's own vendor feed both existed, the county feed (later timestamp) was used:

| County | voteclock D / R / ballots (as of) | Used: county feed D / R / ballots |
|---|---|---|
| Boone | 8,071 / 9,022 / 17,830 (Tuesday, November 3, 2026, 9:24 p.m.) | 8,165 / 9,051 / 17,962 |
| Dekalb | 19,905 / 14,868 / 36,449 (when read on the night of Sunday, November 15, 2026) | 19,971 / 14,888 / 36,547 |
| Macon | 14,025 / 18,459 / 33,837 (When read on the night of Sunday, November 15, 2026) | 14,098 / 18,510 / 33,974 |
| Tazewell | 18,665 / 30,200 / 51,109 (When read on the night of Sunday, November 15, 2026) | 18,882 / 30,310 / 51,456 |
| Whiteside | 8,176 / 10,374 / 19,434 (Tuesday, November 3, 2026, 9:22 p.m.) | 8,210 / 10,397 / 19,498 |

civicAPI aggregator cross-check (race 87130, last updated 2026-11-19T23:30:10.834Z UTC = 5:30 p.m. CST Nov 19, 2026; 90.9% reporting): 43 of 60 counties match exactly on D and R; 17 differ. Largest differences (used − civicAPI):

| County | Used D / R | civicAPI D / R | Difference D / R |
|---|---|---|---|
| Will | 131,990 / 89,187 | 137,102 / 90,645 | -5,112 / -1,458 |
| Cook | 1,244,743 / 274,181 | 1,249,535 / 274,852 | -4,792 / -671 |
| Lake | 152,998 / 68,149 | 155,317 / 68,790 | -2,319 / -641 |
| Mchenry | 60,953 / 48,338 | 62,733 / 49,076 | -1,780 / -738 |
| Peoria | 33,639 / 25,431 | 32,784 / 25,036 | +855 / +395 |
| Dupage | 213,617 / 111,004 | 214,238 / 111,152 | -621 / -148 |
| Winnebago | 48,055 / 38,127 | 48,227 / 38,307 | -172 / -180 |
| Mclean | 37,242 / 27,427 | 36,993 / 27,344 | +249 / +83 |

Most differences are timing: several county snapshots were taken election night (e.g. Will as of Nov 3, 9:41 p.m.) and later counts of mail ballots continue to the Dec 4 canvass. Full list: `out/il_2026_civicapi_crosscheck_UNOFFICIAL.csv`.

---
Registration stand-in: Democratic primary ballot share - NOT official party registration; Illinois has no party registration. 2026 = UNOFFICIAL (pre-Dec 4, 2026 canvass). Cross-link: [Cedar Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) · [PDF report](https://github.com/mbenson8989/Illinois-Election-Analysis/blob/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf) · Built Thursday, November 19, 2026; share-form check added Friday, November 20, 2026 (CST).
