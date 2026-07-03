# data/gedcom/

Raw GEDCOM exports from Ancestry (*Tree → Tree Settings → Export Tree*).

- Source of truth — **never hand-edit** these files.
- Keep every export, dated in the filename: `tree-2026-07-03.ged`.
- Export with Ancestry's privatize-living-people option enabled.

Regenerate the structured data from the newest export with:

```sh
python3 tools/gedcom_to_people.py data/gedcom/<file>.ged --seed-journeys
```
