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

## Tasks
See DAG.md — the execution view OWNS all task state (statuses live in ONE
file per node type; a mirrored status here is drift waiting to happen).
`grep -c "FRONTIER" DAG.md` = startable now · `grep -c "DONE" DAG.md` = shipped.

## Research findings
RES-{{TOPIC}}-1 · PINNED · reference/ — <the fact, with "verified live {{DATE}}">.

<!-- HOW TO USE: a thin ROUTER — one row per non-task ID, newest appended within
     its block; task state lives in DAG.md only. `grep -c "OPEN" INDEX.md` = how
     much is undecided. Verify against reality at the end of EVERY session. Delete
     nothing; tombstone in place (status flips, edges gain resolved-by). -->
