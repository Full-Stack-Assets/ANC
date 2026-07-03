# data/dna/

**Derived DNA data only.** The raw autosomal SNP file from Ancestry's DNA download
must never be committed — it cannot be rotated like a leaked credential, and it
partially identifies blood relatives who never consented to being in this repo.
The repo-level `.gitignore` blocks the common raw-file names; don't work around it.

What belongs here:

- `ethnicity.json` — Ancestral Regions percentages, transcribed from the DNA overview.
- Region/community summaries, match-cluster notes (names of living matches redacted).

Keep the raw download itself outside the repo (or encrypted at rest elsewhere).
