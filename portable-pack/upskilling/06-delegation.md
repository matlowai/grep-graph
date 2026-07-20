# 06 — Delegation and parallelism: fence the writers

## Trigger
You're considering spawning a background agent, running work in parallel,
or splitting a task across subagents/worktrees.

## The rules

1. **Background agents get self-contained, fenced work.** The winning
   pattern: a task whose entire output is new files in a named location,
   with an explicit fence in the prompt — "do NOT touch graph docs (INDEX.md,
   DAG.md, DECISIONS.md, SESSION_HANDOFF.md)". Graph-doc updates are the main
   session's job, always.
2. **Never point two writers at shared state.** Two agents editing the same
   config, doc, or module is a merge conflict at best and silent clobbering
   at worst. If tracks share a file, they're one track.
3. **Parallelize by TYPE:** research/read-only fan-out — freely; independent
   code tracks — subagents or worktrees; anything touching graph docs or
   shared config — main session, serially; heavy local compute — NEVER in
   parallel (see 04-environment.md).
4. **Give agents their return format.** An agent told "your final message is
   the deliverable, return the full report" (the report contract) comes back
   useful; one without that instruction comes back with a summary of what it
   did instead.
5. **Verify agent work like your own.** Fences get ignored, prompts get
   misread. When an agent lands, grep its claimed outputs into existence
   and check it didn't touch what it was fenced from (git status is your
   friend).
6. **Domain substance never delegates downward.** Tier choice has a second
   axis besides spec-completeness: epistemic stakes. Mechanical,
   fully-specified chores (formatting, renames, lockfile regeneration,
   running gates and reporting tails) can drop a tier. Anything that
   produces or verifies a claim in the repo's core domain — the science,
   the security posture, the contract semantics — stays at the top tier
   available, no matter how complete the spec looks, because a cheaper
   tier's plausible-but-wrong output in the domain is exactly the failure
   review is worst at catching. Tie-break: not clearly mechanical → don't
   downgrade.
7. **Brief with an exemplar, not a format spec.** When agents produce
   documents in a house format (reviews, digests, reports), the brief
   points at ONE completed, already-accepted exemplar file and says
   "mirror this" — structure, evidence discipline, tone. A format
   description gets interpreted; an exemplar gets matched. And each
   accepted output becomes the next brief's exemplar, so quality ratchets
   instead of regressing to the spec.
8. **Acceptance is a recorded state transition, not a vibe.** Agent
   deliverables land carrying a visible pending status ("agent draft —
   acceptance pending"); the main session READS the work in full and flips
   the stamp to ACCEPTED with a date. Greppable acceptance state means a
   later session can distinguish "an agent wrote this" from "the
   coordinator stands behind this" — and half-reviewed work can never
   masquerade as reviewed.
9. **Verify by recomputation, not by report.** An agent's numbers are
   claims. Before accepting: re-run the gate yourself, and recompute the
   headline numbers from the agent's raw outputs (its files, not its
   prose). Cheap in practice — a few shell lines against artifacts the
   agent already wrote — and it's the only review step that catches
   plausible-but-wrong.
10. **Solo-authority repos can skip the agent files.** If one main agent
   holds standing authority and has an orchestration tool, installing the
   full `.claude/agents/` tier set is unearned ceremony. Write the tier
   policy as a decision entry plus a front-door rule instead: "subagents
   inherit the session model by default; `model:`/`effort:` overrides only
   for mechanical chores per rule 6." The override in a spawn call then
   doubles as a review flag — its presence asserts "this stage is
   mechanical," which the reviewer can check. Install the agent files when
   tiers or writers multiply.

## Why (origin project, 2026-07)

An eval harness, a new driver, and several research sweeps were all built by
background agents and landed clean — every one of them was fenced,
self-contained file work. The near-misses in the same sessions were shared-
state hazards caught by the fences. Meanwhile the costliest parallelism
mistake of the marathon wasn't agents at all — it was parallel heavy LOCAL
jobs (the resource freeze in 04), which is why rule 3 routes compute to
serial. A second field deployment (2026-07) ran ~10 briefed builds and
reviews through rules 7-9: every deliverable was verified by recomputation
before acceptance, and the practice paid immediately — one agent's
reported test count was stale against a baseline that had changed under
it, caught by the receiver's re-run rather than the report; and an
exemplar-anchored review chain self-audited well enough that a reviewer
caught a banned phrase in its own draft before submitting.

## Self-check
- Can I name the exact files this agent will create, and is anything else
  in scope for it? If I can't enumerate its output, the task isn't fenced.
- Do any two of my parallel tracks touch the same file? Then they're not
  parallel.
- Does this task produce or verify a core-domain claim? Then the tier is
  not a cost decision (rule 6).
- Am I about to accept a deliverable whose headline numbers I have not
  recomputed from its artifacts? That's trust, not review (rule 9).
