# DAG.md — work DAG: parallel tracks and dependencies

The execution view of the graph. Every task is a T-Xn node with `blocked-by:`
edges. A task is **FRONTIER** when every `blocked-by:` is DONE/RESOLVED —
frontier tasks in different tracks can run in parallel. Statuses: OPEN |
FRONTIER | IN-PROGRESS | DONE | BLOCKED. **Task statuses live in this file
and only this file.** Flip IN-PROGRESS when you start, DONE when the
`evidence:` line is satisfied — a stale DAG hides the frontier.

```
grep -n "blocked-by" DAG.md   → the full dependency map
grep -c "FRONTIER" DAG.md     → how much can start right now
```

## {{TRACK_NAME}} track

T-{{TRACK}}1 · DONE · <first task — the scaffold everything hangs off>
blocked-by: DEC-0001
evidence: <what proved it — e.g. "make test green, demo script runs">

T-{{TRACK}}2 · FRONTIER · <a task whose deps are all done — startable now>
blocked-by: T-{{TRACK}}1
ctx: <what to read before starting>
evidence: <the observable proof that will mark this DONE — write it at
  minting time; if you can't state it, the task isn't specified yet>

T-{{TRACK}}3 · BLOCKED · <a task waiting on an open question>
blocked-by: T-{{TRACK}}2, Q-{{FAMILY}}1
reminder: <what to do once unblocked, and the re-entry condition>

<!-- HOW TO USE: mint a node with its blocked-by + evidence edges at CREATION
     time, not later (GOTCHAS A1). Tracks touching disjoint files may run in
     parallel agents; tracks sharing a file are one track. Only the main
     session edits this file during parallel work. -->
