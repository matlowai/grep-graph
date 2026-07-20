# SESSION_HANDOFF.md — live rehydration file (scratch, updated continuously)

Purpose: a fresh session reads this FIRST and continues exactly where the last
one left off — no compaction, no re-derivation. Update at checkpoints and
whenever context grows; overwrite freely (scratch state, unlike DECISIONS.md /
BUILDLOG.md which are append-only). BUT graduate anything worth keeping into a
durable home BEFORE overwriting (upskilling 05 rule 2b).

## Current state ({{DATE}} — <CLEAR-READY | MID-TASK>)

<2-4 sentences: what's true right now that a fresh session must know before
touching anything. The world-state, not a diary.>

## Current task + why
- **Task:** T-{{TRACK}}n — <one line>
- **Why now:** <what makes this the frontier pick>

## Files touched this session
- `path/to/file` — <what changed, why>

## Decisions in flight (not yet DEC'd)
- <anything you're leaning toward but haven't committed to a DEC; PARK design-lane
  calls instead of resolving them>

## Next concrete steps
1. <the literal next action a fresh session should take>
2. <...>

## Gotchas / dead ends (so nobody re-derives them)
- <the thing that wasted time; the assumption that was wrong; the probe result>

<!-- HOW TO USE: this replaces context compaction. Keep it TARGETED — what a fresh
     session needs to continue, not a transcript. Update it AS you work, not just at
     session end (the operator may /clear at any moment). It is scratch, distinct
     from DECISIONS.md (append-only decisions) and any BUILDLOG (append-only
     session-return blocks). Test before overwriting a block: would losing this text
     cost >10 min to re-derive? If yes, graduate it to a durable node first. -->
