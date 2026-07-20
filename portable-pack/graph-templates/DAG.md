# DAG.md — Work DAG: parallel tracks and dependencies

The planning view of the grep-graph: every task is a T-Xn node with
`blocked-by:` edges. A task is **FRONTIER** when every `blocked-by:` is
DONE/RESOLVED — frontier tasks in different tracks can run in parallel
(separate sessions, subagents, or worktrees). Statuses: OPEN | FRONTIER |
IN-PROGRESS | DONE | BLOCKED. Update statuses the moment they change; INDEX.md
stays the ID ledger, this file is the execution view.

```
grep -n "blocked-by" DAG.md   → the full dependency frontier
grep -c "FRONTIER" DAG.md     → how much can start right now
```

## {{TRACK_NAME}} track

T-{{TRACK}}1 · DONE · <first task — the scaffold everything hangs off>
blocked-by: DEC-0001
evidence: <what proved it — e.g. "make test green, demo script runs">

T-{{TRACK}}2 · FRONTIER · <a task whose deps are all done — startable now>
blocked-by: T-{{TRACK}}1
evidence: <the observable proof that will mark this DONE — write it at
  minting time; if you can't state it, the task isn't specified yet>
ctx: <where to read first before starting this one>

T-{{TRACK}}3 · BLOCKED · <a task waiting on an open question>
blocked-by: T-{{TRACK}}2, Q-{{FAMILY}}1
reminder: <what to do once unblocked, and the re-entry condition>

—— worked example of a parallel fan-out (after T-{{TRACK}}2, two tracks open) ——

## {{TRACK_NAME_2}} track (frontier ANYTIME, no code deps)

T-{{TRACK2}}1 · FRONTIER · <read-only research that depends on nothing>
blocked-by: —

<!-- HOW TO USE: mint a T-Xn node with its blocked-by edges at CREATION time, not
     later (upskilling 05 rule 1). Flip to IN-PROGRESS when you start, DONE when
     verified. A stale DAG hides the frontier. Tracks whose tasks touch disjoint
     files are safe to run in parallel agents (upskilling 06); tracks that share a
     file are one track. Never let a background agent flip these statuses — graph
     docs are the main session's job. -->
