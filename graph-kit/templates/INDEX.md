# INDEX.md — thin router: every ID, one line, where it lives

Verified: {{DATE}} — <one line on what changed, so the next session trusts
the timestamp>. Rule: a stale INDEX is a broken build (CONVENTIONS §5.6).

<!-- This file is a ROUTER, not a status board. Task statuses live in DAG.md
     and ONLY there — do not infer progress from this file. One row per ID,
     appended within its block; tombstone in place, delete nothing. Keeping
     status in one file per node type is what prevents drift. -->

## Decisions
DEC-0001 · DECISIONS.md — adopted the grep-graph organization system.
<!-- append one row per DEC, newest last -->

## Open questions
Q-{{FAMILY}}1 · OPEN · <where it lives> — <one-line reminder>; blocks: T-{{TRACK}}2.
<!-- every OPEN/PARKED question gets a row; flip to RESOLVED + resolved-by
     when tombstoned at its home location -->

## Tasks
See DAG.md — the execution view owns all task state.
`grep -c "FRONTIER" DAG.md` = startable now · `grep -c "DONE" DAG.md` = shipped.

## Assumptions
ASM-1 · PROVISIONAL · ASSUMPTIONS.md — <one-line: what was assumed, pending whose review>.

## Useful greps
```
grep -c "OPEN" INDEX.md          → how much is undecided
grep -rn "<any-ID>" .            → everything that ID touches
```
