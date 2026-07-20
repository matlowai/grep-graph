# 05 — Graph-doc discipline under pressure

## Trigger
Always — but especially when the work is going WELL. Doc-debt accumulates
fastest during productive streaks, because updating feels like interrupting
momentum. That's exactly when these rules bind.

## The rules

1. **Mint the node BEFORE building.** New work gets its T-Xn / DEC / Q node
   with `blocked-by:` edges at creation time. If you're typing code for
   something with no ID, stop and mint it. (Full conventions: CONVENTIONS.md
   — this doc is about compliance under pressure, not the format.)
2. **Update docs BEFORE acting and AFTER each milestone**, not at session
   end. Before: mint/flip the node, note the plan in the handoff. After: flip
   status, record numbers, park findings — while they're still cheap to
   write. The operator may /clear at any moment; the handoff is only useful
   if it's true RIGHT NOW. A checkpoint = any point where you'd hate to
   re-derive what you just learned.
2b. **Graduate before you overwrite:** SESSION_HANDOFF.md is overwritable
   scratch — so before overwriting or trimming any block of it, anything
   worth keeping MUST first land in a durable home (DAG/DEC/INDEX node,
   BUILDLOG block, an upskilling doc, or persistent memory). Same test as
   /tmp: if losing the text would cost ten minutes of re-derivation, it
   doesn't live only in scratch. When in doubt, append rather than replace
   and graduate at the next checkpoint.
3. **Tombstone, never delete.** Resolved questions get status → RESOLVED +
   `resolved-by:`; superseded decisions get a new DEC + `supersedes:`. If
   you're deleting graph text, you're almost certainly wrong.
4. **PARK instead of guessing.** Anything touching design-lane territory
   (contract shapes, the open-question list, principles) gets PARKED with a
   reminder capsule — never resolved unilaterally, even when the answer
   seems obvious. Obvious-to-you is how scope boundaries get broken.
5. **Prefer /clear at natural seams.** A long chat with stale context loses
   to a fresh session with a good handoff. The rehydration file works —
   trust it, keep it worthy of trust. Calibration (measured in the origin
   project, 2026-07; recalibrate with tools/context_probe.py and ccusage):
   rehydration cost ~$2-3 and rebuilt a ~170k baseline; every turn re-bills
   the whole context (~$1/MTok at the top tier), so at ~350k context ONE
   remaining delegated task (~6-10 turns) already pays for the clear. Rule:
   /clear after every closed milestone (~2-4 delegated tasks + doc closure)
   or past ~2x the rehydration baseline (~350k), whichever first; never carry
   >500k into a new task. Interactive gaps >5min re-WRITE the whole context
   at higher input rates — bursty days mean clear MORE, not less.
6. **Verify INDEX.md before ending.** A stale INDEX is a broken build. And
   an empty BUILDLOG return-block is a rule violation — "none" is data.

## Why (origin project, 2026-07)

~6 build-sessions of work ran in one chat, and doc-debt hurt twice: work
proceeded on nodes that hadn't been minted (so the DAG hid the true
frontier), and a checkpoint's learnings had to be re-derived after context
grew stale. Meanwhile every time the handoff WAS kept current, /clear +
rehydrate was seamless — the marathon's continuity across six sessions is
itself the proof the system works when fed.

## Self-check
- Does everything I'm currently building have a live node with true status?
- If the operator /cleared right now, what would the next session have to
  re-derive? Whatever you just thought of — write it into the handoff now.
