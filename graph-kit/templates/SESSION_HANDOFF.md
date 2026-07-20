# SESSION_HANDOFF.md — live rehydration file (scratch, updated continuously)

Purpose: a fresh session reads this FIRST and continues exactly where the
last one left off — no compaction, no re-derivation. Update at checkpoints
(any point where you'd hate to re-derive what you just learned), not just at
session end — sessions die without warning. Overwrite freely, BUT graduate
anything worth keeping into a durable home (DEC / node reminder / lessons
entry) BEFORE overwriting — the test: would losing this text cost ten
minutes to re-derive? **Size budget: ~150 lines.** Archive overflow to
docs/sessions/SESSION-nnn-<date>.md; a capsule that needs scrolling has
stopped being a capsule.

<!-- OPTIONAL machine-readable state block — a script can verify these
     claims instead of trusting prose:
```yaml
session: {{N}}
state: CLEAR-READY | MID-TASK
tests: <last known result + when>
next_goal: <one line>
```
-->

## Current state ({{DATE}} — <CLEAR-READY | MID-TASK>)

<2-4 sentences: what's true right now that a fresh session must know before
touching anything. World-state, not a diary.>

## Current task + why
- **Task:** T-{{TRACK}}n — <one line>
- **Why now:** <what makes this the frontier pick>

## Do not
<!-- the 3-6 standing prohibitions a fresh agent is most likely to violate;
     prune to stay short — durable ones belong in CONVENTIONS/AGENTS.md -->
- <e.g. don't regenerate X, the artifacts in out/ are canonical>

## Files touched this session
- `path/to/file` — <what changed, why>

## Decisions in flight (not yet DEC'd)
- <anything you're leaning toward but haven't committed to the ledger>

## Next concrete steps
1. <the literal next action a fresh session should take>
2. <...>

## Gotchas / dead ends (so nobody re-derives them)
- <the thing that wasted time; the assumption that was wrong; the probe result>
