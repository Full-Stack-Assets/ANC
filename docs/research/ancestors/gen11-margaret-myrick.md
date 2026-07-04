# "Margaret" — mother of Isaac Myrick — Generation 11

## Overview

The tree records a woman named only "Margaret" (no surname), born 1612 in Newbury, Essex Co., Massachusetts, died 2 April 1708 in Newbury, listed as the mother of one child, Isaac Myrick (b. 6 Jan 1665, Newbury), and as the daughter of Thomas Merrick and Mary Griggs. The audit flagged her as *parent-too-old* (age 53 at Isaac's 1665 birth); her own recorded lifespan (1612–1708, 96 years) is separately worth sanity-checking. External research shows this is neither a misattached child nor a simple birth-year typo, but a **data-conflation**: this record's exact vital dates belong, almost certainly, to Isaac's father — James Merrick (1612–1708) of Newbury — not to his mother.

## Verified facts

- **James Merrick (1612–1708) is a richly documented immigrant ancestor.** Born 1612 in St. Davids, Pembrokeshire, Wales; emigrated to Charlestown, Massachusetts in spring 1636 aboard the ship *James* with three Merrick brothers (ages 16–33); worked as a cooper and fish-monger with a wharf in Charlestown; moved to Newbury before 1657, where most of his children were born; died **2 April 1708 in Newbury, Essex Co., Massachusetts, at about age 96**. Sources: WikiTree (Merrick-91), Familypedia, americanancestors.org (NEHGS *Register*), George Byron Merrick's 1902 *Genealogy of the Merrick-Mirick-Myrick Family of Massachusetts, 1636–1902*, and Savage's *Genealogical Dictionary of the First Settlers of New England*, citing Ipswich Land Records (Vol. IV p.344; Vol. V p.29). [documented]
- **This record's birth year (1612) and death date/place (2 Apr 1708, Newbury) are an exact match to James Merrick's own documented vital dates** — not a coincidence given how specific "2 April" is. [documented, by cross-reference]
- **James Merrick's wife was indeed named Margaret**, surname not preserved ("Margaret [surname unknown]"), married James circa 1648–1653 (sources vary on the exact year). So the *given name* on this tree record is correct for Isaac's mother — only the *vital dates* attached to it appear to be her husband's. [documented for the name; the dates are in question]
- **James and Margaret's children included Isaac Myrick**, confirmed independently: WikiTree Myrick-487 states Isaac "was born at Newbury, Essex, Massachusetts Bay Colony, on January 6, 1664/5, son of James Merrick and Margaret Unknown" — matching this tree's Isaac Myrick record (`I182381536258`) almost exactly (6 Jan 1665, Newbury). Isaac's listed spouse in this tree, Mary Newell, also matches: "married Mary Newell of Charlestown on August 22, 1694." [documented]
- **James's real parents were Rev. John "Sion" Meyrick (1579–1650) and Dorothy Bishop (1570–1650)** of Pembrokeshire, Wales — not Thomas Merrick and Mary Griggs as this tree records for "Margaret." Among James's several siblings (per WikiTree Merrick-91/Merrick-10 and the 1902 Merrick-Mirick-Myrick genealogy) was a brother also named **Thomas Merrick** — one of the four Merrick brothers who crossed together in 1636, born about 1620, died 1704 in Springfield, Hampden Co., Massachusetts (a different death place and slightly different birth year than this tree's Thomas Merrick, b.1600/d.1684 Middletown, CT — so the identification isn't certain, but the sibling relationship, not parent-child, is the well-documented pattern). [documented for James's real parents; inferred/uncertain for this tree's specific Thomas Merrick]

## Corrections to the tree

- **No birth year is being corrected**, because the tree does not actually contain a documented birth year for the real Margaret (Isaac's mother) to correct it *to*. What can be said is that **the 1612/1708 dates currently on her record almost certainly belong to her husband, James Merrick**, and should not be relied on as her own vital dates.
- **The parent link to Thomas Merrick + Mary Griggs is very likely wrong-generation**, not wrong-person: the historically documented Thomas Merrick in this family was James's *brother*, not father. James's real parents (John "Sion" Meyrick and Dorothy Bishop) have no corresponding records in this tree/dataset, so nothing was added — see Open questions.
- Neither correction is applied by rewriting the machine-owned `vitals`/`relationships` fields (per repo convention, those are parser output); both are documented via `manual.notes` on the affected records instead.

## New findings (not in the tree)

- **James Merrick's immigration story**: one of four Merrick brothers who sailed from Bristol to Charlestown, Massachusetts in spring 1636 on the ship *James*, reportedly then dispersing — one to Eastham, one to Newbury, one remaining in Charlestown. This is a well-known thread in New England immigrant genealogy (Savage; the 1902 Merrick-Mirick-Myrick family genealogy) not reflected anywhere in this tree.
- **James's occupation** (cooper and fish-monger, owned a wharf in Charlestown) and his ten children (Sarah, James Jr., Hannah/Amity, John, Abigail, Joseph, Isaac, Timothy, Susanna) are documented externally but not present in this tree beyond Isaac.
- **Isaac Myrick's own record carries conflicting extra events** (birth entries dated 6 Jan 1661 and 6 Jan 1665, and a death dated 5 Mar 1726, all placed in Eastham, Barnstable Co., Massachusetts — a different part of the state from Newbury) that do not match his well-documented Newbury, Essex Co. birth and appear to belong to a distinct, unrelated "Isaac Myrick" of Cape Cod. Flagged on his record for a future cleanup pass; not corrected here since `events[]` is machine-owned.

## Open questions

- **Who transcribed/copied James Merrick's dates onto "Margaret's" record, and when?** Not recoverable from the open web — this looks like a tree-compilation artifact (a common failure mode where a couple's two vital-record entries get cross-attributed) rather than a documented historical claim.
- **The real Margaret's own birth year, birthplace, and death** are unknown from any source located in this pass. If she married James circa 1648–1653 and was still bearing children as late as 1665 (17 years later), a birth in the 1620s–1630s would be typical, but this is inference, not a sourced fact.
- **Is this tree's Thomas Merrick (`I182541960298`, b.1600, d.1684 Middletown, CT) actually James's brother**, or a different, unrelated Thomas Merrick entirely? The externally documented immigrant brother Thomas (b. abt.1620, d.1704, Springfield, MA) does not line up precisely on either birth year or death place/year. Left unresolved — flagged on both records rather than merged or asserted as fact.
- **Where do James's real, externally-documented parents (Rev. John "Sion" Meyrick and Dorothy Bishop) belong in this tree?** No record ids exist for them; not fabricated here.

## Sources

- WikiTree, James Merrick (1612-1708), Merrick-91: https://www.wikitree.com/wiki/Merrick-91 (page itself not directly fetchable on the open web during this research pass; content reflected via aggregated search summaries and a mirrored WikiTree "Family Tree" export)
- Familypedia, James Merrick (1612-1708): https://familypedia.fandom.com/wiki/James_Merrick_(1612-1708)
- Reitz Family Genealogy (Kenneth Robert Reitz), James Merrick b.1612 d.1708-04-02: https://context.kennethreitz.org/html/kennethreitz/1134.html — cites Ipswich Land Records (Vol. IV p.344; Vol. V p.29), George Byron Merrick's 1902 *Genealogy of the Merrick-Mirick-Myrick Family of Massachusetts, 1636-1902*, LDS Ancestral File, and Savage's *Genealogical Dictionary of the First Settlers of New England*
- WikiTree, Isaac Myrick (1665-abt.1731), Myrick-487: https://www.wikitree.com/wiki/Myrick-487 — birth "Newbury...January 6, 1664/5, son of James Merrick and Margaret Unknown"; marriage to Mary Newell of Charlestown, 22 Aug 1694
- WikiTree, Thomas Merrick (abt.1620-1704), Merrick-10: https://www.wikitree.com/wiki/Merrick-10
- Geni, Thomas Merrick (c.1620-1704): https://www.geni.com/people/Thomas-Merrick/6000000000223935237
- The Brownlow Family Tree, Thomas Merrick b.1620 St David's Parish, Pembrokeshire, Wales, d. 7 Sep 1704 Springfield, Hampden Co., MA: https://thebrownlows.com/getperson.php?personID=I3180&tree=brow1
- Family of James Myrick of Newbury, MA (mainegenie rootsweb page): http://freepages.rootsweb.com/~mainegenie/genealogy/MYRICK.htm
