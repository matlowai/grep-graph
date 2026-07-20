# Portable coordination pack

A self-contained, copy-into-any-repo kit for running an AI coding agent as a
**coordinator** — a main session that writes specs, delegates builds to cheaper
tier-agents, reviews by diff, and keeps a grep-navigable docs graph — instead of
an expensive model typing code inline. Everything here resolves inside this
directory; nothing requires the project it came from.

## The measured evidence for why (origin project, 2026-07)

This stack was not designed on a whiteboard; it was measured into existence over
a multi-session build marathon. The load-bearing numbers, each measured in the
origin project in 2026-07 (recalibrate yours with `tools/context_probe.py` and
`ccusage`): an agent's cost is **turns × context size**, because every turn
re-bills the whole context as cache reads (~$1/MTok at the top tier, ~$0.50/MTok
on Opus — **cache reads dominate the bill**, output tokens are a rounding error);
a 570-tool-call day cost ~$211 in cache reads alone. Delegating a well-specified
build to a fresh-context tier agent costs **~3–8x less** than doing it inline
(one real driver-change-plus-eval: ~$3.34 delegated vs ~$12–15 inline), and the
margin survives sloppy review because a full re-read of an agent's files adds ~$1
against ~$10 saved. A batching audit found tool-call batching waste is only ~4%
of spend — **session scope is the 10x lever, not batching** — so the discipline
that pays is fresh contexts, `/clear` at seams (~350k tokens ≈ 2x a rehydration
baseline), and delegation. One batching case IS load-bearing: the post-/clear
rehydration read-in goes in ONE tool operation (a single `cat` of the
session-start docs), or the clear ceremony itself is taxed once per file —
every turn re-bills the full context at cache-read rates (~10% of base input
price). Adopting the whole stack took a daily bill from
**$231 → $33** with 5/5 clean delegations in a single session — measured
honestly but in ONE deployment; treat every number here as a calibration
starting point, not a promise (the controlled benchmark is an open
workstream in the repo's TODO.md). The pack exists
because that top-tier access is ending: most work will run on Opus, and Opus
inherits whatever is written down — so it is written down here.

## What's in the box

```
README.md            — this file: what/why + install recipe
INSTALL.md           — step-by-step placement in a new repo + placeholder inventory
agents/              — four delegation-tier agents + a sounding-board role + the report contract
upskilling/          — the twelve operating-procedure docs + their README
graph-templates/     — starter CONVENTIONS / INDEX / DAG / SESSION_HANDOFF skeletons
CLAUDE-template.md   — a CLAUDE.md skeleton wiring it all together
tools/context_probe.py — measures a live session's context size + per-turn cost
```

## Install recipe (short form — full steps in INSTALL.md)

1. Copy this directory's contents into a new repo:
   `agents/*` → `.claude/agents/`, `upskilling/` → `docs/upskilling/`,
   `graph-templates/*` → repo root (as `CONVENTIONS.md`, `INDEX.md`, `DAG.md`,
   `SESSION_HANDOFF.md`), `CLAUDE-template.md` → merge into `CLAUDE.md`,
   `tools/context_probe.py` → `tools/`.
2. Fill the `{{PLACEHOLDERS}}` (inventory in INSTALL.md) — a handful, all
   obvious. Decide `{{MOCK_POLICY}}` first: mocks allowed, or real-only?
   Real-only is the recommended default — mocks pass tests while failing
   reality; phase deep work as contracts + honest not-implemented errors
   with pseudocode/design notes before real code, never faked data.
3. **Restart the client** so the new `.claude/agents/` files register.
4. Seed the graph: give your first real task a `T-` node in DAG.md + INDEX.md,
   write a `SESSION_HANDOFF.md`, and start delegating.

The pack is prescriptive, not a reference manual: read `upskilling/README.md`
first, then work the way doc 09 (the main-session playbook) describes.

A second field deployment (2026-07) hardened the pack further: a
research-instrument repo ran the full stack through a multi-day autonomous
marathon and contributed docs 10 (machine enforcement — validators over
conventions) and 11 (preregistration + claims ledger), plus the
exemplar/acceptance/recomputation rules in doc 06. The one-line summary of
what that deployment proved: conventions decay, validators don't — and an
append-only evidence discipline let the system catch and correct its own
overclaim mid-run.
