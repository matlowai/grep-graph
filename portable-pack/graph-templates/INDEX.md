# INDEX.md — Flat ID ledger (entry point for every task)

Verified: {{DATE}} — <one line on what changed this session, so the next session
trusts the timestamp>. Rule: CONVENTIONS.md §5.5 — a stale INDEX is a broken build.
Format: `ID · STATUS · location — reminder` with ctx/edges where non-obvious.

## Principles
PRIN-1..n · FIXED · SPEC §0 — <one-line-per-principle list of the standing
design principles, so any grep for PRIN-n lands here first>.

## Decisions & Amendments
DEC-0001 · ACCEPTED · DECISIONS.md — grep-graph org system adopted.
<!-- worked example row; append one line per DEC, newest at the bottom of its block -->

## Open questions
Q-{{FAMILY}}1 · OPEN · <location> — <one-line reminder>; ctx: §n; blocks: T-{{TRACK}}2.
<!-- worked example: every OPEN/PARKED question gets a row here with its edges -->

## Tasks (mirror of DAG.md statuses — DAG.md is the execution view)
T-{{TRACK}}1 · DONE · DAG.md — <what it was>; blocked-by: DEC-0001.
T-{{TRACK}}2 · FRONTIER · DAG.md — <what it is>; blocked-by: T-{{TRACK}}1.

## Research findings
RES-{{TOPIC}}-1 · PINNED · reference/ — <the fact, with "verified live {{DATE}}">.

<!-- HOW TO USE: this is a flat mirror of every ID in the repo. A row per ID,
     newest appended within its block. `grep -c "OPEN" INDEX.md` tells you how much
     is left; `grep "T-" INDEX.md` is the task board. Verify it against reality at
     the end of EVERY session — walk the repo's IDs and confirm each status here is
     true. Delete nothing; tombstone in place (status flips, edges gain resolved-by). -->
