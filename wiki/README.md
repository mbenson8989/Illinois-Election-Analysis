# README: Start Here

Welcome. If you've never seen this analysis before, this page is for you. It explains what you're looking at, where the numbers come from, and how to read them.

> **\*2026 figures are marked with an asterisk.** They are unofficial. The Illinois State Board of Elections certifies the 2026 results at its canvass on Dec 4, 2026, so these numbers may still change.

## Where the numbers come from

The 2022 numbers come directly from the **[Illinois State Board of Elections](https://www.elections.il.gov/)** (SBOE), from its official website. Nothing is estimated or made up. The sources are:

- **2022 governor results:** the SBOE's official 2022 general election canvass, for all 102 counties.
- **The Democratic "registration" stand-in:** the SBOE's official primary canvasses (June 28, 2022 and March 17, 2026).
- **2026 governor results (unofficial\*):** the SBOE hasn't posted these yet. Until it does, they come from each county's own election office (the county clerk or election commission), as posted on its official results page. We found usable results for 80 of 102 counties; the other 22 are left out rather than guessed. Every county's source link is listed on [Bottom-Up Reverse Math](Reverse-Math).

**One important difference from other states:** Illinois voters don't register by party. So there is no official count of registered Democrats. Instead we use the next best official number: the share of primary voters who chose a Democratic ballot. Every page calls this a **stand-in**. It is not party registration.

## See the data for yourself

You don't have to take our word for it. Open the **PDF report** in the sidebar, or go straight to the **[Illinois PDF report](https://raw.githubusercontent.com/mbenson8989/Illinois-Election-Analysis/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf)**. It lists every county with its numbers for 2022 and 2026\*. You can check any line against the State Board's own files.

## This is a hypothesis, not a verdict

Please read this part carefully. **What you'll find here is a hypothesis, not settled fact.**

If election manipulation exists, it would not be one simple thing. It would be multifaceted, with several methods working together. This analysis looks through one lens only: how votes line up with each county's Democratic baseline. A gap between the two is a pattern worth checking. It is not proof of anything by itself, and it says nothing about who did what or why. In Illinois the lens is blurrier than usual, because the baseline is a stand-in rather than real registration.

## The story behind the numbers

Numbers make more sense with the story behind them. Morissa tells that story in her hypothesis write-up on Substack: **[The Election Equation. And Plan.](https://moebenson.substack.com/p/the-election-equation-and-plan)** You can find more of her writing on **[Morissa Benson's Substack](https://moebenson.substack.com/)**.

## What you're looking at, in plain terms

**The basic idea.** In each county, we compare two things:

1. What share of the ballots cast went to the Democratic candidate for governor.
2. What share of primary voters chose a Democratic ballot (the stand-in).

The difference between those two is the **surplus** (we call it S). A county where the Democratic candidate did better than the stand-in has a positive surplus; one where he did worse has a negative surplus.

**Why it's called reverse-factoring.** We work backward from the result. We start with the votes that were counted. Then we take out what the county's Democratic baseline would explain. What's left over is the **residual**: the part the baseline doesn't account for.

**A real example: Cook County, 2022.**

- Pritzker got 1,065,445 of 1,458,690 ballots cast, a **73.041222%** share.
- 524,388 of 661,726 primary voters chose a Democratic ballot: **79.245488%**.
- So Cook's surplus is 73.041222 − 79.245488 = **-6.204266 points**. The statewide line below expected -6.797515, so Cook's residual is **0.593249** points.

## How Morissa worked it out

Morissa isn't a mathematician. She sees patterns. Here is what she did:

1. She lined up the official numbers county by county.
2. She graphed all the counties together and drew the line that fit them best.
3. That line gives each state its own fitted numbers: a multiplier and an offset. No two states share them.

For Illinois, using all 102 counties' official 2022 results, the line is the **Surplus Equation**:

**S = -24.769946 × (D/100) + 12.831550**

Here S is the surplus in percentage points, and D is the Democratic primary-ballot share (the stand-in) as a percent. The line explains only part of the county-to-county differences (R² = 0.238576); the average county sits 4.756273 points from it. The details are on the **[Locked Illinois Formula](Locked-Illinois-Formula)** page.

She used AI to speed up the work, but not to decide anything. Every number was computed twice, by two separate programs reading the raw files, and the two had to match to the last decimal before anything was published.

## Where to go next

- [Home](Home): the overview
- [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit): where it started (Nebraska)
- [Floor and Ceiling Counties](Floor-and-Ceiling): the counties at each end
- [Bottom-Up Reverse Math](Reverse-Math): the step-by-step math
- [Graphs](Graphs): the charts
- [PDF report](https://raw.githubusercontent.com/mbenson8989/Illinois-Election-Analysis/main/report/Illinois_Reverse_Factoring_Report_UNOFFICIAL_2026.pdf): the data
- [Locked Illinois Formula](Locked-Illinois-Formula): the equation and a fill-in-the-blank template
