---
name: ancestor-deep-dive
description: Build an exhaustive backlog of ancestors in this repo that haven't had a research deep-dive yet, then autonomously work through a user-specified number of them back-to-back with no check-ins unless something is genuinely ambiguous or touches a living person.
---

You're driving the ANC repo's ancestor-verification pipeline. This is real historical research that gets written into a shared family-history dataset — treat every claim like it needs a citation, because it does.

## Phase 1 — Build/refresh the backlog

"Not already existing" work means: a `data/journeys/{id}.json` whose `status` is not `"reviewed"`, AND whose person is not already covered by a dossier in `docs/research/ancestors/*.md` (grep those files for the person's id — dossiers are the durable proof a person was actually researched, not just touched by the parser).

1. Read `docs/research/direct-line-issues.md` — it's a pre-computed, generation-ordered list of flagged problems (`duplicate-person`, `parent-too-young`, `parent-too-old`, `child-after-death`, `child-before-parent`, `impossible-lifespan`) among the ~1,283 direct ancestors of the home person (`I182195856751`). Anything under `### Interpretations` with a `RESOLVED` tag is done; everything else in that file is open.
2. Cross-reference `docs/research/audit-2026-07-03.md` for the same kind of findings across the full 3,242-person tree (not just the direct line).
3. Collect every id already covered by a dossier under `docs/research/ancestors/` (`grep -rho 'I[0-9]\{6,\}' docs/research/ancestors/*.md | sort -u`) — exclude these.
4. Build the ordered backlog:
   - **Tier 1**: distinct people still flagged in `direct-line-issues.md`, ordered by generation ascending (closest to the home person first — these are the ones that most affect the documented family story).
   - **Tier 2**: distinct people flagged in `audit-2026-07-03.md` but not in the direct line.
   - **Tier 3**: remaining `data/journeys/*.json` with `status: "seeded"` that have no flags at all — plain enrichment (transcribe waypoints into a real narrative, verify at least the vitals).
5. Write the backlog to `docs/research/deep_dive_backlog.md` as a checklist (id, name, generation/tier, one-line reason) — this file is the durable queue; re-running Phase 1 should regenerate it idempotently from current repo state, not append.
6. Report the total backlog count and the tier breakdown to the user.

## Phase 2 — Get the number

Ask (or accept from context, e.g. `/ancestor-deep-dive 500`) how many backlog items to run through, `N`. Use `TaskCreate` to add one tracking task: "Ancestor deep-dive: N-item run" — update its status as you go so progress survives context compaction.

## Phase 3 — Execute N items, no check-ins

Work the backlog top-to-bottom in batches (roughly 8–12 concurrent per batch is a good size — enough parallelism to make progress, small enough that you can read and apply every result carefully). Do **not** stop to check in between batches or between individual ancestors. Per batch:

1. For each backlog item, spawn a research agent (`Agent` tool, `general-purpose`, with web search) given: the person's id, name, current `data/people/{id}.json` and `data/journeys/{id}.json` contents, and the specific flagged issue if one exists. Ask it to actually verify externally (FamilySearch, Find A Grave, GRO/vital records, census indexes, archived family-history pages, WikiTree, Geni as a lead not a source) — mirror the depth and citation style of existing files in `docs/research/ancestors/` (see e.g. `gen05-sabina-oldsdotter.md`) — not a guess dressed up as a conclusion.
2. Once a batch's agents return, for each result:
   - Write a dossier at `docs/research/ancestors/{slug}.md` (Overview / Verified facts / Corrections to the tree / New findings / Open questions / Sources — match existing dossiers' structure).
   - Update `data/people/{id}.json`: only touch the `manual` key (`confidence_override`, `manual.notes`, `manual.events` for legend material) — never hand-edit fields outside `manual`, they're machine-owned per the schema (`schema/person.schema.json`).
   - Update `data/journeys/{id}.json`: flip `status` to `"reviewed"`, fill `summary`, add a `narrative` on waypoints where you have one, flip `confidence` per-waypoint appropriately.
   - If the finding resolves an entry in `docs/research/direct-line-issues.md` or `audit-2026-07-03.md`, add/update its `### Interpretations` line with a `RESOLVED <date>` tag and the one-line explanation, per the existing format.
   - Check the item off in `docs/research/deep_dive_backlog.md`.
3. Commit the batch with a descriptive message (this repo's convention: `Add <Name> dossier from research run`, `<Case> resolved: <one-line finding>`, etc. — see `git log` for tone).
4. Update the tracking task's progress note (e.g. "37/500 done").
5. Continue immediately to the next batch. Use the environment's self-pacing loop mechanism (`ScheduleWakeup` with a short reason, or the dynamic `/loop` sentinel) to keep going across turns without waiting on the user, until `N` items are done or the backlog is exhausted.

**Stop and ask the user only for:**
- A record that looks like it might be a living person (privacy rule in the repo's `README.md` — never guess on this, always stop and confirm before writing anything).
- A conflict where two well-sourced hypotheses genuinely contradict and picking one would materially change the family narrative (as opposed to routine "which transcription/spelling is right" calls, which you resolve yourself and note in Corrections).
- Repeated unrecoverable errors (schema violations, missing files) that aren't fixed by re-reading the schema.

## Phase 4 — Wrap-up

When `N` is reached or the backlog is exhausted: report how many were completed, how many remain in `docs/research/deep_dive_backlog.md`, and anything flagged for user review. Mark the tracking task completed (or note how much is left if stopped early).
