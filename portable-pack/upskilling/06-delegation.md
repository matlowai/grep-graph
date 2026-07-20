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

## The second axis: named roles (tiers say how much model; roles say what stance)

The tier ladder (rules 2/6, playbook 09) answers "how much capability does
this spec need?" A second, orthogonal axis answers "what STANDING STANCE
should this agent hold?" The origin projects run both at once:

- **Sounding board, on a DIFFERENT model family** (the shipped `intuition`
  definition): a read-only plan critic invoked before committing to anything
  complicated. The different architecture is the point, not a convenience —
  your executor line shares your blind spots, so its agreement is cheap;
  a second family's disagreement is signal (03). Never give it write tools.
- **Scout / bridge**: read-only survey of territory before a build wave — a
  neighbor repo, an unfamiliar dependency, machine state after a power seam.
  Deliverable is a report; it edits nothing.
- **Babysitter**: during an agent wave, a timer-driven coordination pass
  that runs the watchdog, integrates landings (verify-by-diff, gate, named
  commit), and launches the next queue item. Usually a role the MAIN
  session plays on a timer rather than a separate definition.
- **Review specialist**: adversarial verification as a standing default
  (REFUTE-first) pointed at a sibling agent's deliverable.

They compose in one wave: tier executors do the fenced builds · one
babysitter tick integrates each landing · and the plan that launched the
wave was pressure-tested by the sounding board first. *Incidents:* a
design memo bounced off a different model family surfaced four genuinely
new contributions the resident line had missed — adjudicated and ratified
the same day; and a babysitted four-agent wave caught its own watchdog
misclassifying mid-flight agents as finished, before partial work got
committed.

**Mint a role vs reach for a tier:** mint a role when the value is a
standing stance or fence (read-only, different family, adversarial default)
you'd otherwise re-type into every spawn prompt; reach for a tier when the
only variable is capability. Roles are cheap to define — one markdown file
— but each is standing cognitive surface: one more thing the coordinator
must remember exists and choose correctly among. Keep the roster small
(the origin project ran months on four tiers plus ONE role) and retire any
role that goes a month uninvoked.

**Spawning is not your last word.** Where your harness supports messaging a
running agent (Claude Code does — messages queue and land at the agent's
next tool round), three moves open up: spec amendments arrive mid-flight
(a requirement discovered after spawn — from the operator or a sibling's
finding — gets messaged in rather than letting the agent finish wrong);
nudge-recovery beats kill-and-respawn (an agent whose background job
finished but whose completion notification never re-invoked it resumes
cleanly from a message stating the observed disk state — pair with the
disk-first check); and it is NOT a chat channel — each message costs the
agent a context re-read and can derail a mid-task chain, so use it for
redirects, amendments, and recovery, never for check-ins. "How's it going?"
is what the disk is for. *Incidents:* a probe agent was re-aimed mid-flight
when a mid-run finding changed the primary experiment arm, and three
separate notification-gap naps were recovered by a single message quoting
the artifacts already on disk.

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
- Is the agent roster growing? A role nobody has invoked in a month is
  cognitive surface, not capability — retire it.
