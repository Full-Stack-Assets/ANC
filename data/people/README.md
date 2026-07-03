# data/people/

One JSON file per ancestor, keyed by GEDCOM id (`I123.json`), validating against
`schema/person.schema.json`.

**Manually-created people use an `M` prefix** (`M0001.json`): individuals proven by
research but absent from the Ancestry export (e.g. Ellen Larkin's mother, née McAlone).
The parser only regenerates `I*.json`, so `M*` records survive re-runs untouched.
When the person is later added to the Ancestry tree and re-exported, migrate the `M`
record's content into the new `I` record's `manual` block and delete the `M` file.

**Machine-owned except for the `manual` key.** The parser regenerates every field on
re-run but preserves each file's `manual` block verbatim. Put all hand-authored
content there:

```jsonc
"manual": {
  "confidence_override": "legend",     // optional record-level override
  "notes": ["Grandma always said he jumped ship in Boston."],
  "events": [                          // same shape as machine events
    { "type": "other", "note": "Jumped ship, per family story", "confidence": "legend", "sources": [] }
  ]
}
```
