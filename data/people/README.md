# data/people/

One JSON file per ancestor, keyed by GEDCOM id (`I123.json`), validating against
`schema/person.schema.json`.

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
