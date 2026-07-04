# Margaret McArthur (b. 1664?, d. 1775) and Alexander Moir — Generation 11

> **Verdict up front:** the `impossible-lifespan` flag (111 years, 1664–1775) is
> real, but the death year is the correct half and the birth year is the error.
> An independent, professionally-researched source — the Clan Arthur/Court of
> the Lord Lyon chief-succession case — confirms a "Margaret MacArthur Moir"
> died about 1775 and traces her father to "John MacArthur of Milton," matching
> this record's father by name and place. No source anywhere gives her actual
> birth year; 1664 is almost certainly a transcription/data-entry error.
> Confidence: **moderate-high** that 1775 is correct and 1664 is wrong;
> **low** on any specific replacement birth year, which is left as an open
> question rather than a guess.

## Overview

Margaret McArthur was born (per the tree, unsourced) in 1664 in Argyllshire, Scotland, married Alexander Moir (b. 1679, d. Feb 1723, also unsourced), and — per the tree — died in 1775, an apparent 111-year lifespan that the audit tool correctly flags as impossible. Her one listed parent is John McArthur (I182381537173, b. abt. 1640/1645/1650, d. 1694/1697, Milton, Dunoon, Argyll — the record's own duplicate GEDCOM events already disagree with themselves on both dates). Her one listed child is James Moir (I182381537144, d. 1784, born in Argyllshire).

External research turned up a striking, independent corroboration: the Clan Arthur (Clan MacArthur) chief-succession case, researched by professional genealogist Hugh Peskett (commissioned 1986) and concluded when the Lord Lyon King of Arms (Scotland's heraldic authority) recognized James Edward Moir MacArthur as Chief of Clan Arthur on 28 August 2002. That case's published history states the petitioner's genealogy was "proved... back to Margaret MacArthur Moir who died about 1775," and that her father was "John MacArthur of Milton" (Dunoon, Cowal, Argyll), who died about 1674. Both the surname pairing (McArthur/MacArthur married to a Moir) and the place (Milton, Dunoon, Argyll) match this tree's record exactly, and the "Moir" name persists three and a half centuries later as the middle name of the 2002-recognized Chief himself — a strong, unlikely-to-be-coincidental thread connecting this record to a real, continuously documented family.

## Verified facts

- **A "Margaret MacArthur Moir" died about 1775**, per the Clan Arthur/Court of the Lord Lyon chief-succession case (clanarthur.org/history, drawing on Hugh Peskett's research). This is the same death year recorded in this tree, arrived at completely independently. [documented — Clan Arthur official history]
- **Her father was "John MacArthur of Milton," who died about 1674** — matching this record's father, John McArthur (I182381537173), by name and by birthplace (Milton, Dunoon, Argyll, per his own tree record). [documented — same source]
- **The "Moir" surname persists as a middle name in the family's own later chief**, James Edward Moir MacArthur (b. 1914, Calgary, Canada; d. 1 Apr 2004), recognized Chief of Clan Arthur in 2002 — consistent with continuous, real descent through a Margaret-McArthur-married-to-a-Moir line, not a coincidental name match. [documented]
- **The wider historical backdrop is plausible**: Argyllshire, and Dunoon/Cowal specifically, is well documented as the ancestral seat of the MacArthurs of Milton (est. 1653, per the same source), and the broader Argyll region is the well-known source of 18th-century Highland emigration (e.g., the 1739 "Argyll Colony" to the Cape Fear valley, NC) — though no direct emigration record for this specific family was found, so this is background context only, not a documented fact about Margaret herself. [inferred]

## Corrections to the tree

- **Margaret's birth year, 1664, is very likely wrong; her death year, 1775, should stand.** No source anywhere (this record's own vitals carry zero citations) supports 1664. Combined with the externally-corroborated ~1775 death, it implies a 111-year lifespan — exactly the pattern the audit tool flags, and matching this repo's house pattern of digit-slip/transcription errors in this data. A `manual.events` placeholder birth ("bet. 1680 and 1695, estimated, unsourced") has been added to supersede it without asserting a fabricated exact year; see Open questions.
- **Her father John McArthur's own recorded death (1694/1697) conflicts with the external source's ~1674.** His own record already carries internally inconsistent duplicate GEDCOM events (birth: 1650 vitals vs. Abt.1640/1645/1640 in events; death: 1697 vitals vs. 1694/Aug 1697 in events) — i.e., the underlying import already had unresolved year disagreements for this small family before this research pass. Not overwritten (not certain this is the identical John MacArthur, since the external source gives no birth year to cross-check), but flagged via `manual.notes` on I182381537173.

## New findings (not in the tree)

- **The Clan Arthur/Court of the Lord Lyon chief-succession case** (1986–2002) is a substantial, independent piece of documented Scottish genealogy naming this exact family (Margaret MacArthur Moir, her father John MacArthur of Milton, and — going the other direction — her connection to Archibald MacArthur Stewart, a "great nephew" who recorded arms in 1775, the same year of her death) and to the House of MacArthur of Milton, founded 1653 by a descendant of John MacArthur of Drissaig (via Charles MacArthur of Tirivadich, 16th century). None of this deeper background (Drissaig, Tirivadich, the 1653 founding) is reflected in this tree and none has been added to the graph — it is offered here as context, not as new tree data, since it does not name Margaret's spouse or child directly.
- **Archibald MacArthur Stewart's 1775 arms recording** — the same year as Margaret's death — is likely why "about 1775" is preserved so precisely in the clan history; it may be the anchor point the whole "died about 1775" claim derives from, rather than a personally-dated record for Margaret herself. This slightly tempers confidence in the exact year without undermining the broad conclusion (she did not live to 111).

## Open questions

- **Margaret's true birth year.** No source found gives it. Given husband Alexander Moir's recorded birth (1679, itself unsourced) and son James Moir's recorded death (1784), a birth in the 1680s–1690s (making her roughly 85–95 at death — long-lived but credible, unlike 111) fits the family's other dates far better than 1664, but this is an estimate, not a fact, and is recorded as such in `manual.events` rather than replacing the tree's machine-owned value.
- **Is this tree's John McArthur (I182381537173, d. 1694/1697) truly "John MacArthur of Milton" (external source, d. abt. 1674)?** The place matches exactly; the death year does not. No birth year is given by the external source to help adjudicate. Left open.
- **Alexander Moir's own dates (b. 1679, d. Feb 1723) are wholly unsourced** in this tree and were not independently corroborated or refuted by this research pass.
- **Did this family actually emigrate, or stay in Scotland?** The prompt's suggestion of Argyll Highland emigration (Carolinas/Cape Fear valley) was not confirmed for this specific family — the Clan Arthur source keeps the line in Scotland (Dunoon/Cowal) through Margaret's death and beyond, into a continuously Scottish-resident chiefly line. No emigration record was found, and none is asserted here.
- **James Moir's own vital details** (no birth date, d. 1784, Argyllshire) were not independently corroborated beyond his parents' records.

## Sources

- Clan Arthur (official clan society), "History": https://clanarthur.org/history/ — states Margaret MacArthur Moir "died about 1775," her father John MacArthur of Milton "died about 1674," Archibald MacArthur Stewart's 1775 arms recording, the 1653 founding of the House of MacArthur of Milton, and the 2002 Lord Lyon recognition of James Edward Moir MacArthur as Chief
- Clan Arthur, "John MacArthur of that Ilk, Chief of Clan Arthur": https://clanarthur.org/chief-of-clan-arthur/
- Web search aggregation citing the same Clan Arthur history content for "John MacArthur of Drissaig," Hugh Peskett's 1986–2002 research commission, and the succession of researchers (Niall 10th Duke of Argyll in the 1930s; Mrs. English; Ian MacArthur; Arthur MacArthur of Philadelphia; Hugh Peskett)
- Internal cross-reference: `data/people/I182381537159.json` (Margaret McArthur), `I182381537173.json` (John McArthur, father), `I182381537165.json` (Alexander Moir, spouse), `I182381537144.json` (James Moir, child)
- Not found / checked without success: a WikiTree, Geni, or FamilySearch profile specifically for this Margaret McArthur or Alexander Moir; the Moir genealogy PDF (electricscotland.com, *Moir genealogy and collateral lines*) was searched in full text and contains no matching entries for this branch (its coverage is Aberdeenshire/Perthshire/Stirlingshire Moirs, not Argyll)
