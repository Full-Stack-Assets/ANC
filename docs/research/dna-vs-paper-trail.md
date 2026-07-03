# DNA estimate vs. paper trail

Comparison of the AncestryDNA Ancestral Regions estimate (`data/dna/ethnicity.json`,
transcribed 2026-07-03) against the pedigree-implied expectation
(`data/dna/pedigree-implied-origins.json`, attributed at each line's emigration point).

| Cluster | DNA estimate | Paper trail | Verdict |
|---|---|---|---|
| Britain (England + Wales + Midlands buckets) | ~47% (29+10+6+2) | 17.3% England + most of the 13.7% colonial-untraced + 0.1% Cornwall | **Consistent.** The colonial NJ/New England lines that the tree never traces overseas (Albertson, Pedrick, Stone, Coffin, Pond, Whitney…) are genetically English — DNA fills in what the paper trail leaves as "colonial American". |
| Ireland (Munster 12 + Leinster 5 + Connacht 3 + Donegal 2) | 22% | 12.7% | **DNA runs higher.** Expected if some "unknown" slots (11.9%) are Irish — e.g. the missing McCue/Murray links — and if Canadian-born Morrow-side ancestors were Scotch-Irish. The Munster dominance + West Cork journey fits the Donahue/Regan/Sheehan/Murphy cluster. |
| Italy + East Mediterranean (Central Italy 7 + Cyprus 2 + Levant 1) | ~10% | 12.5% (Angelo Prospero + Vincenza Minochelli) | **Consistent within recombination variance** — central/southern Italian ancestry routinely reads partly as Cyprus/Levant. Note: this does NOT resolve whether Mary Prosper's mother was Vincenza or a second wife; both scenarios predict roughly this much Italian DNA if the second wife was also Italian (likely, given the Isernia journey). |
| Scandinavia (Norway 6 + Sweden 2) | 8% | 12.5% Sweden | **Consistent-ish.** Recombination variance plus Ancestry's Norway/Sweden boundary being notoriously soft for southern-Swedish DNA (the Holst/Swanson lines are Skåne-adjacent). Slightly low but unremarkable. |
| Germanic (Southern Germanic Europe) | 7% | 6.8% Germany | **Spot on.** The Hohmann/Crist/Fogel lines. |
| French Canada (Quebec) | 4% | 12.5% Canada/French Canada | **Resolves an ambiguity.** The paper bucket lumped all Canadian-born ancestors; DNA says only ~4% is actually French-Canadian (the Drolet line) — the rest of the Canadian-born ancestors (Morrows etc.) were British/Irish stock passing through Canada, which lands in the Britain/Ireland buckets instead. |
| Scotland (Hebrides 1) | 1% | (was 2.8% in the naive count) | Consistent — the Wallace/Lackey/MacDonald traces. |
| Netherlands | 1% | 0 | A pleasing echo: the *debunked* Dutch-origin lore for William Albertson notwithstanding, 1% NL-adjacent signal is normal noise inside the NW-Europe supercluster. Not evidence for Steenwijk. |

## What the journeys pin down

1. **North Isernia Province (Molise)** — the Italian line's home. This is the single
   best new lead in the whole DNA kit: Angelo Prospero and Vincenza Minochelli (and
   Angelo's probable second wife, the real mother of Mary Prosper b. 1918) should be
   searchable in Isernia-province civil registration (Stato Civile, on Antenati).
2. **South West Munster / West Cork** — parish-level target for the Irish lines.
3. **New Jersey Settlers (Camden/Gloucester/Salem + Mercer)** — genetic confirmation
   of the Albertson colonial line, matching Otter Branch and the Trenton move.
4. **Montérégie/Yamaska French Settlers** — localizes the Drolet line southeast of
   Montreal.

## Bottom line

No red flags between DNA and paper: every major tree cluster is genetically supported,
the colonial-English inference is confirmed, and the open Mary Prosper question is
*not* answerable from ethnicity percentages alone (an Italian second wife predicts the
same signal). The decisive next steps are records, not DNA: Isernia civil registration
for the Prospero marriages, and West Cork parishes for the Irish lines. DNA *matches*
(shared-match clustering) could settle the Mary Prosper question — worth capturing
match surnames into `data/dna/` later, with living-person names redacted.
