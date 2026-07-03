# ANC — Family History Data Repo

Structured family-history data exported from Ancestry, transcribed and enriched by hand,
and consumed downstream (eventually by the ancestor-journey game).

There is no public Ancestry API, so the flow is **export → parse → enrich**:

```
Ancestry GEDCOM export ──► tools/gedcom_to_people.py ──► data/people/{id}.json   (machine-generated skeleton)
                                                     └─► data/journeys/{id}.json (seeded once, then hand-edited)
Ancestral Journeys views ──► manual transcription   ──► data/journeys/{id}.json
DNA raw download          ──► derived data only     ──► data/dna/  (raw genotype file is NEVER committed)
```

## Layout

| Path | Contents | Edited by |
|---|---|---|
| `data/gedcom/` | Raw `.ged` exports from Ancestry. Source of truth. | Never hand-edited |
| `data/people/{id}.json` | One record per ancestor: vitals, relationships, events, sources, confidence. | Parser (regenerated on re-run); hand edits go in the `manual` key only |
| `data/journeys/{id}.json` | Migration path as ordered waypoints, transcribed from Ancestral Journeys. | Parser seeds once; yours after that — never overwritten |
| `data/dna/` | Ethnicity breakdown and other **derived** DNA data. | Hand-edited |
| `data/generated/game_bundle.json` | Privacy-reviewed, direct-ancestor-only export for game consumption. | Generator (`tools/build_game_bundle.py`); never hand-edited |
| `schema/` | JSON Schemas for the record types. | Hand-edited |
| `tools/` | GEDCOM parser + emitter + game bundle generator (Python 3.9+, stdlib only + `jsonschema` for validation). | Hand-edited |

## Workflow

1. Export the tree from Ancestry: *Tree → Tree Settings → Export Tree*. Drop the `.ged` into `data/gedcom/`.
2. Regenerate people records (and seed any new journeys):

   ```sh
   python3 tools/gedcom_to_people.py data/gedcom/<your-export>.ged --seed-journeys
   ```

3. Enrich by hand:
   - `data/journeys/{id}.json` — add waypoints from the Ancestral Journeys views, narratives, coordinates. Flip `status` from `seeded` → `transcribed` → `reviewed` as you go.
   - `data/people/{id}.json` — anything hand-authored goes under the `manual` key (notes, legend events, `confidence_override`). Everything **outside** `manual` is machine-owned and will be overwritten on the next parser run.
4. Re-running the parser after a fresh export is safe: `manual` blocks are preserved, journey files are never touched once they exist.

## Confidence model

Every event and record carries a `confidence` flag that must survive all the way into game text:

- `documented` — backed by at least one source citation in the GEDCOM.
- `inferred` — in the tree but uncited (the parser's default for unsourced facts).
- `legend` — family story, invented texture, or embellishment. **Manual only** — the parser never emits it. Add legend material under `manual.events` in a person file or as `confidence: "legend"` waypoints in a journey file.

## Game bundle (for the ancestor-journey game)

`tools/build_game_bundle.py` walks the direct ancestors of a home person (default: the
tree owner, `I182195856751`) and exports `data/generated/game_bundle.json` — a single,
versioned, privacy-reviewed artifact the game consumes instead of loading raw
`data/people/`/`data/journeys/` files directly. Re-run it any time; it never modifies
source records, only regenerates its own output.

```sh
python3 tools/build_game_bundle.py
```

Per ancestor, the bundle records:

- **generation / side / lineage_path** — distance from the home person, which
  grandparent line (paternal/maternal), and the name chain connecting them.
- **privacy_status** — `public_safe` (has a recorded death year), `possibly_living`
  (no death year and either close-generation or recently-born — needs a human check
  before use), or `living_confirmed` (the home person themself).
- **content_readiness** / **readiness_score** — whether the journey is actually
  game-ready (`reviewed` status, every waypoint narrated) vs. still a `draft` or
  `not_ready` machine-seeded skeleton, so the game (and content-pipeline tooling) know
  which ancestors are safe to build a chapter around.
- **canonical_id** — resolves known duplicate records (both hand-confirmed pairs and a
  same-name/same-birth-year heuristic scoped to just the ancestor set) so game code
  never has to deduplicate at runtime.

The bundle also includes a **source_provenance** table classifying every cited source
as a proprietary Ancestry-hosted collection (cite the fact, don't reproduce the
transcription), a public-domain historical record/publication, or research this project
generated itself — licensing guidance for what the game is actually allowed to do with
each fact.

## Testing

```sh
python3 tools/tests/test_parser.py
```

Runs the parser against `tools/tests/fixture.ged` (also works under pytest).

## Privacy

This repo must stay **private**.

- The raw autosomal SNP file (AncestryDNA download) is ignored by `.gitignore` and must never be committed — it cannot be rotated like a credential, and it partially identifies blood relatives who never consented to being in a repo.
- Commit only *derived* DNA data (ethnicity percentages, region summaries) to `data/dna/`.
- GEDCOM exports contain living people. Ancestry marks them `Living` in exports made with the privatize option — use it, or prune living people before committing.
