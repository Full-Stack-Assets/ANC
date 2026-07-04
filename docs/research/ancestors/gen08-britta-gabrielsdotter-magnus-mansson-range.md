# Britta Gabrielsdotter (1756–1834) and Magnus Månsson Rånge (1744–1822) — Generation 8

> **Duplicate-person resolution.** Both spouses in this couple were flagged by
> `tools/audit_tree.py` as duplicate-person: two records apiece share name and birth
> year. Investigation shows the whole multi-generation branch was imported twice —
> once from a well-sourced per-record chain, once from a thinly-sourced compiled
> "Ancestry Family Trees" submission — and the duplication threads consistently up
> to the grandfather (Måns Månsson Rånge, gen 9) and down to the great-grandson
> (Gustaf Rånge, a separately tracked gen-6 duplicate flag).

## Overview

Magnus Månsson Rånge (b. 4 Mar 1744) and Britta Gabrielsdotter (b. 1756) were a
farming couple at Skattegården/Backgården, Hadäng, in Velinge (also spelled
Velinga) parish, Skaraborg — part of historical Västergötland, in modern Västra
Götaland county, Sweden. Magnus died 18 Nov 1822 and Britta 26 Jan 1834, both at
Hadäng. Their documented line continues through son Johannes Magnusson (1791–1873)
and grandson Gustaf Rånge (1838–1902), who emigrated to Easton, Massachusetts in
1885 and whose daughter Anna Josephina Svenson is the tree owner's direct ancestor
(already the subject of `gen05-simon-swanson-anna-josephina-svenson.md`). Both
Magnus and Britta exist as **two separate person records** in the tree — a
well-sourced "primary" chain and a thinly-sourced "compiled" duplicate chain — a
pattern that repeats at the generation above (their son's family) and the
generation below (their grandson's family), strongly suggesting the whole segment
was imported twice from two different Ancestry.com submissions of the same family
group.

## Verdict

**Both pairs are duplicate-person, not two different couples.** Same names, same
birth years, same parish (Hadäng/Skattegården, Velinge), same spouse pairing, and —
decisively — their son "Johannes Magnusson" appears in *both* chains with the
identical birth date and birthplace (25 Sep 1791, Backgården Hadäng farm, Velinge),
which cannot be coincidence for two distinct families.

- **Britta Gabrielsdotter**: `I182197443408` (canonical) vs. `I182195861021` (duplicate) — same person.
- **Magnus Månsson Rånge**: `I182197443412` (canonical) vs. `I182195861020` (duplicate) — same person.

### Why the "primary" (`...443408`/`...443412`) chain, not the other

- The `...443xxx` chain's descendants carry **specific, per-record Ancestry source
  collections** all the way to a documented US immigrant: son Johannes Magnusson
  (`I182197443344`, Sweden Indexed Death Records 1840-1947; Jönköping Church Records
  1633-1860), grandson Gustaf Rånge (`I182197443234`, Massachusetts Death Records,
  NY Passenger Lists, Swedish household clerical survey, Sweden Emigration
  Registers), great-granddaughter Anna Josephina Svenson (`I182197442975`, ten
  distinct primary-type sources including 1900 US Census, Massachusetts Marriage
  Records, and ELCA Swedish-American Church Records) — the same chain already
  treated as the direct line in `gen05-simon-swanson-anna-josephina-svenson.md`.
- The `...861xxx` chain's every record — Britta, Magnus, their son "Johannes"
  (`I182195860775`), grandson "Gustaf" (`I182195860718`), great-granddaughter "Anna
  Josefina Rånge" (`I182195860382`) — cites nothing but the generic, unsourced-at-
  the-record-level "Ancestry Family Trees" compiled index (`S446914557`), i.e. a
  different Ancestry user's tree submission bundled into this export without
  independent primary citations of its own (bar one shared ELCA baptism record on
  the great-granddaughter).
- This mirrors the house convention already applied to the John Albertson & Ann
  Pine gen-6 duplicate pair (`docs/research/ancestors/` — see commit `148f3ff`):
  designate the better-sourced record primary, keep the thinner duplicate's unique
  facts as cross-annotated `manual.notes` rather than deleting it.

### The cascade (documented, not resolved here)

The same primary/duplicate split repeats one generation up and (at least) two
generations down, each independently flagged by the audit tool:

| Generation | Person | Primary id | Duplicate id |
|---|---|---|---|
| gen 9 | Måns Månsson Rånge (1713–1762) & Maria Persdotter | `I182197444971` / `I182197444935` | `I182195861510` / `I182195861488` |
| **gen 8** | **Magnus Månsson Rånge & Britta Gabrielsdotter (this dossier)** | **`I182197443412` / `I182197443408`** | **`I182195861020` / `I182195861021`** |
| gen 7 | Johannes Magnusson (1791–1873) | `I182197443344` | `I182195860775` (not separately flagged by the audit tool, but identical name/date) |
| gen 6 | Gustaf Rånge (1838–1902) | `I182197443234` | `I182195860718` (flagged separately in `deep_dive_backlog.md`/`audit-2026-07-03.md`) |
| gen 5 | Anna Josephina Svenson / "Anna Josefina Rånge" (1870–1902) | `I182197442975` | `I182195860382` (not separately flagged by the audit tool, but identical name/dates) |

Only the gen-8 (Magnus & Britta) and gen-9 (Måns & Maria) pairs are formally
in-scope for this dossier; the gen-6/gen-7/gen-5 duplicates are noted here for
context and cross-referenced in Open questions, but resolving them is separate work.

## Verified facts

- **Magnus Månsson Rånge, b. 4 Mar 1744, Skattegården, Hadäng, Velinge (Velinga), Västergötland/Skaraborg, Sweden; d. 18 Nov 1822, Backgården, Hädäng, Velinga.** Sourced (as residence 1755–1852, Velinge, Skaraborg) to "Sweden, Church Records, 1451-1943" (S447115812). [documented]
- **Britta Gabrielsdotter, b. 1756, Hadäng, Velinge, Västra Götaland; d. 26 Jan 1834.** Top-level source "Sweden, Select Baptisms, 1611-1920" (S447115815), which most plausibly attaches to a child's baptism rather than her own birth. [documented/inferred — the birth year itself is unsourced at the field level]
- **Couple's documented son, Johannes Magnusson, b. 25 Sep 1791, Backgården Hadäng farm, Velinge; d. 27 Jan 1873, Nya Varv, Skaraborg**, sourced to Sweden Indexed Death Records 1840-1947 and Jönköping Church Records 1633-1860. [documented]
- **Grandson Gustaf Rånge, b. 1838, Dimbo, Sweden; departed Skaraborg 11 May 1885; arrived New York 29 May 1885 via Liverpool/Queenstown; resident Hjo, Skaraborg in the 1880 household survey; died 17 Feb 1902, Easton, Massachusetts**, sourced to Massachusetts Death Records 1841-1915, NY Passenger/Crew Lists 1820-1957, Sweden Selected Household Clerical Surveys 1880-1893, and Sweden Emigrants Registered in Church Books 1783-1991. [documented]
- **Great-granddaughter Anna Josephina Svenson (Gustaf's daughter), b. abt. 1870 Hjo; d. 23 Aug 1902 Easton, MA; m. Simon Swanson 14 May 1898, Easton** — the tree owner's direct ancestor, already independently verified in `gen05-simon-swanson-anna-josephina-svenson.md`. [documented]
- **A Geni.com public tree profile for "Måns Månsson Rånge (1713–1762)"** independently lists him with wife Maria Persdotter and children including Andreas, Johannes, and Gabriel at Skattegården Velinga/Hadäng — matching this family's names, dates, and farm names, and corroborating (as a secondary/compiled source, not a primary parish record) that a Rånge family of this generation and place is attested outside this tree's own Ancestry import. [compiled/secondary — external corroboration only, not independently sourced to a parish record]

## Corrections to the tree

- **The tree contains two full person-records apiece for Magnus Månsson Rånge and Britta Gabrielsdotter** (`I182197443412`/`I182195861020` and `I182197443408`/`I182195861021`) — a duplicate-person data error, not two couples. See Verdict above for the resolution and `manual.notes` added to all four records.
- **Magnus's first "marriage" to Maria Larsdotter (`I182197443441`), 17 Sep 1798, Karlstad, Värmland, with child Anders Christian Magnusson (`I182197443442`, b./d. 1781, Lycke, Göteborg och Bohus), is almost certainly a mis-merge.** The child's birth (1781) predates the cited marriage record (1798) by seventeen years, and neither event's location (Värmland; Bohus county) matches this Magnus's lifelong parish (Hadäng/Velinge, Skaraborg). This looks like records for a different, more common "Magnus Månsson" attached to the wrong person during the original tree compilation. Flagged as unverified, not deleted (see `manual.notes` on `I182197443412`).
- **The duplicate Britta record (`I182195861021`) lists four children** (Stina Magnusdotter b.1789, Johannes Magnusson b.1791, Lisa Mansson b.1794, Gabriel Magnusson b.1799) where the primary record (`I182197443408`) lists only one (Johannes). If the tree is ever cleaned up on Ancestry, Stina, Lisa, and Gabriel should be added to the primary record as full siblings of Johannes — see Re-pointing below.

## New findings (not in the tree)

- **Britta's father may have been named Gabriel** (patronymic-consistent with "Gabrielsdotter"), per a bare, unsourced stub record (`I182195861462`) attached only to the duplicate chain. No vitals, no sources — treat as a plausible naming inference, not a documented parent link.
- **Magnus's father, Måns Månsson Rånge (1713–1762), reportedly died "av huvudsjuka"** (of apoplexy/a stroke) per a note on the duplicate grandfather record (`I182195861510`) — absent from the primary grandfather record (`I182197444971`). Plausible period cause-of-death phrasing, unsourced.
- **External corroboration of the family via Geni.com**: a public Geni profile for "Måns Månsson Rånge (1713–1762)" at Skattegården Velinga/Hadäng, with wife Maria Persdotter and children including a Johannes and a Gabriel, was located via web search — consistent with, but independent evidence for, this being a real, previously-researched Swedish farming family rather than a tree-import artifact. The underlying parish records were not independently viewable (see Open questions).
- **The duplication is structural, not a one-off**: it repeats identically at the generation above (Måns Månsson Rånge/Maria Persdotter) and at least two generations below (Johannes Magnusson, Gustaf Rånge, and Anna Josephina Svenson/"Anna Josefina Rånge" all have unlabeled or separately-flagged twin records with matching names and dates). This is almost certainly two different Ancestry.com tree submissions for the same family, merged into one export without de-duplication.

## Open questions

- **No primary Swedish parish record (kyrkobok/husförhörslängd) for Magnus, Britta, or Måns Månsson Rånge could be independently viewed.** Riksarkivet/ArkivDigital images for Velinge/Hadäng parish, 1740s–1830s, are captcha- and/or subscription-gated and could not be checked on the open web this pass. This would be the definitive way to confirm birth/death dates, Britta's patronymic father, and the couple's full sibling set.
- **Was Britta's father really "Gabriel"?** The only support is an unsourced stub record and the patronymic itself; a baptism or household-examination record naming her parents would settle this.
- **Magnus's supposed first marriage to Maria Larsdotter** (Karlstad, Värmland, 1798) — is this a genuine second marriage attached to the wrong Magnus Månsson, or a total mis-merge? A Karlstad-area marriage record check (if accessible) would resolve whether any "Magnus Månsson" married there in 1798, and whether it's this Magnus or a namesake.
- **The cascading duplicate chain below this couple** (Johannes Magnusson, Gustaf Rånge, Anna Josephina Svenson/Anna Josefina Rånge) has not been formally resolved — only the Gustaf Rånge pair (`I182197443234`/`I182195860718`) is separately tracked in `deep_dive_backlog.md`/`audit-2026-07-03.md`; the Johannes and Anna Josephina/Josefina twin records are not currently flagged by the audit tool at all (their birth years/names apparently didn't trip the exact-match duplicate detector) but are evidently the same underlying merge artifact. Recommend a follow-up pass to formally flag and resolve gen 5–7 of this same branch.
- **Full name of Måns Månsson Rånge's wife, Maria Persdotter, and any documentation for the "Rånge" surname itself** — "Rånge" is unusual for this era/region (possibly a soldier-name/soldatnamn or farm-name rather than a hereditary surname, as already flagged as an open question in `gen05-simon-swanson-anna-josephina-svenson.md`); Sweden's Centrala Soldatregistret (soldatreg.se) was not queried this pass and would be the right place to check.

## Re-pointing needed (if/when the tree is cleaned up)

| Record | Field | Old value | New value |
|---|---|---|---|
| `I182195861464` (Stina Magnusdotter, duplicate-chain child) | `parents` | `["I182195861020","I182195861021"]` | `["I182197443412","I182197443408"]` |
| `I182195861023` (Lisa Mansson, duplicate-chain child) | `parents` | `["I182195861020","I182195861021"]` | `["I182197443412","I182197443408"]` |
| `I182195861463` (Gabriel Magnusson, duplicate-chain child) | `parents` | `["I182195861020","I182195861021"]` | `["I182197443412","I182197443408"]` |
| `I182197443412` (Magnus, primary) | `children` | `["I182197443442","I182197443344"]` | add `"I182195861464"`, `"I182195861023"`, `"I182195861463"` |
| `I182197443408` (Britta, primary) | `children` | `["I182197443344"]` | add `"I182195861464"`, `"I182195861023"`, `"I182195861463"` |
| `I182197443408` (Britta, primary) | `parents` | `[]` | `["I182195861462"]` (Gabriel — unsourced stub; add only as a flagged/low-confidence link) |
| `I182195860775` ("Johannes Magnusson," duplicate-chain child = `I182197443344`) | *(record)* | kept as a distinct id | retire/merge into `I182197443344`; re-point its own child `I182195860718` (Gustaf, duplicate) accordingly — tracked under the separate Gustaf Rånge duplicate-person flag, not executed here |

No records **outside** this couple's own two parallel subtrees were found pointing at
`I182195861020`/`I182195861021` (checked via full-repo id search), so no cross-branch
re-pointing is required beyond the couple's own children/parents listed above.

## Sources

- Data: `data/people/I182197443408.json`, `I182197443412.json` (primary chain);
  `data/people/I182195861021.json`, `I182195861020.json` (duplicate chain);
  `data/people/I182197443344.json`/`I182195860775.json` (son Johannes, both copies);
  `data/people/I182197443234.json`/`I182195860718.json` (grandson Gustaf, both
  copies); `data/people/I182197442975.json`/`I182195860382.json`
  (great-granddaughter Anna Josephina/Anna Josefina, both copies);
  `data/people/I182197444971.json`/`I182195861510.json` and
  `I182197444935.json`/`I182195861488.json` (great-grandparents, both copies);
  `data/people/I182195861462.json` (Britta's putative father "Gabriel," bare stub);
  `data/people/I182197443441.json`/`I182197443442.json` (Magnus's disputed first
  "marriage"/child).
- "Sweden, Church Records, 1451-1943," Ancestry.com Operations, Inc. (S447115812) — Magnus's residence citation.
- "Sweden, Select Baptisms, 1611-1920," Ancestry.com Operations, Inc. (S447115815) — attached to the Britta/Magnus record and to son Anders Christian's baptism.
- "Sweden, Select Marriages, 1630-1920," Ancestry.com Operations, Inc. (S447115848) — Magnus's disputed 1798 Karlstad marriage record.
- "Sweden, Indexed Death Records, 1840-1947" and "Jönköping, Sweden, Church Records, 1633-1860," Ancestry.com Operations, Inc. (S447115802, S447115837) — son Johannes Magnusson.
- "Massachusetts, Death Records, 1841-1915"; "Massachusetts, Death Index, 1901-1980"; "New York, Passenger and Crew Lists ... 1820-1957"; "Sweden, Selected Indexed Household Clerical Surveys, 1880-1893"; "Sweden, Emigrants Registered in Church Books, 1783-1991" — grandson Gustaf Rånge, Ancestry.com Operations, Inc.
- "Ancestry Family Trees," Ancestry.com Operations, Inc. (S446914557) — the sole, generic, compiled source behind every record in the duplicate chain (`I182195861021`, `I182195861020`, `I182195861464`, `I182195861023`, `I182195861463`, `I182195861510`, `I182195861488`, `I182195860775`, `I182195860718`, `I182195860382`).
- Geni.com, "Måns Månsson Rånge (1713–1762)": https://www.geni.com/people/M%C3%A5ns-M%C3%A5nsson-R%C3%A5nge/6000000084079789851 — public compiled profile located via web search, matching name/dates/farm names; page content could not be fully rendered by this session's fetch tool (returned blank), so details are taken from the search-result summary only. [compiled/secondary]
- Negative/inconclusive searches: no independent Swedish-parish or Riksarkivet record was reachable for Britta Gabrielsdotter or Magnus Månsson Rånge specifically (captcha/subscription-gated); no WikiTree, FamilySearch, or Geni profile was found for Britta Gabrielsdotter or Magnus Månsson Rånge by name+date combination beyond the Måns Månsson Rånge profile above; no record was found confirming or refuting the disputed 1798 Karlstad marriage.
- `docs/research/ancestors/gen05-simon-swanson-anna-josephina-svenson.md` — sibling dossier, independently researched, covering this family's documented US-immigrant descendants.
- `docs/research/direct-line-issues.md`, `docs/research/audit-2026-07-03.md`, `docs/research/deep_dive_backlog.md` — audit tool output identifying the duplicate-person flags resolved here.
