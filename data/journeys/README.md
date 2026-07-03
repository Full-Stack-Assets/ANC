# data/journeys/

One JSON file per ancestor (`I123.json`), validating against `schema/journey.schema.json`.

The parser **seeds** a journey (waypoints derived from dated/placed GEDCOM events) only
when no file exists yet — after that the file is yours and is never overwritten.

Workflow per ancestor:

1. Run the parser with `--seed-journeys` → file appears with `"status": "seeded"`.
2. Open the ancestor's Ancestral Journeys view on Ancestry and transcribe: add missing
   waypoints, reorder, add `narrative` text, coordinates (`lat`/`lng`), and set each
   waypoint's `confidence`. Flip status to `"transcribed"`.
3. Cross-check against sources; flip to `"reviewed"`.

Invented texture is welcome — but it gets `"confidence": "legend"` so the game can
label it on screen.
