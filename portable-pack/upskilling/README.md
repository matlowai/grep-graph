# Upskilling Pack — read in full at every session start

Purpose: operating instructions distilled from a multi-session build marathon
in the origin project (2026-07) — how those sessions went well and exactly how
they went wrong. EVERY session reads this pack, whatever model is running it:
the failure modes here are situational, not capability-tier — the strongest
model of the marathon made most of these mistakes once, and these docs exist
so nobody (including it) makes them twice. This is NOT a lessons journal;
every doc is prescriptive: trigger → rule → one concrete incident (the why)
→ self-check.

## How to use this pack

- **If you are the session model reading this**: read every doc below in
  full — it's a step of the CLAUDE.md session-start order. They are short
  on purpose. Treat them as binding operating procedure, same weight as
  CONVENTIONS.md. If you are the MAIN session (not a subagent), 09 is your
  job description — end your rehydration by echoing its operator card.
- **If you are the operator**: it's wired into CLAUDE.md already; for
  sessions outside this repo's flow, one line suffices — "read
  docs/upskilling/ in full before starting."

## The one-paragraph version

Verify every write by reading it back. Probe the live system before building
on any documented behavior. Never trust a single evaluator — pair every LLM
judge with one objective measurement. Run one heavy local job at a time.
Anything worth ten minutes goes in the repo, not /tmp. Mint the graph node
before building the thing. When stuck or surprised, your first move is a
30-second probe, not a longer think. Make every load-bearing convention an
executable check, freeze protocols before expensive runs, and append —
never edit — evidence. And at every checkpoint, ask the self-check
questions in each doc — the difference between a strong and a weak session
is mostly whether these questions get asked at all.

## The docs

1. [01-verification.md](01-verification.md) — verify-on-write, pinned-repo
   git, narrating tests. The two silent-loss incidents and the discipline
   that ended them.
2. [02-probe-first.md](02-probe-first.md) — live probes beat docs and
   training data; the integration surprises that prove it; how to probe.
3. [03-evaluate-evaluators.md](03-evaluate-evaluators.md) — the LLM-judge
   protocol: unprimed probe + objective co-metric; disagreement is signal.
4. [04-environment.md](04-environment.md) — serialize heavy jobs, /tmp dies
   on reboot, check resources first, resource-contention symptoms.
5. [05-docs-discipline.md](05-docs-discipline.md) — grep-graph hygiene under
   pressure: mint nodes first, close docs continuously, update the handoff
   as you go, /clear at seams.
6. [06-delegation.md](06-delegation.md) — when background agents shine, how
   to fence them, and the parallelism that's actually safe.
7. [07-thinking-upgrades.md](07-thinking-upgrades.md) — the heuristics that
   generate the non-obvious ideas: cross-domain chaining, the 10-minute
   experiment, disagreement-as-signal, the transcript-is-data move.
8. [08-failure-catalog.md](08-failure-catalog.md) — evidence-backed catalog
   mined from the actual session transcripts: what failed, what the recovery
   was, what rule prevents it.
9. [09-main-session-playbook.md](09-main-session-playbook.md) — the
   coordinator role: measured delegation economics, tier selection,
   review-by-diff, the /clear threshold, Opus-specific tuning, the operator
   card, and the escalation taxonomy.
10. [10-machine-enforcement.md](10-machine-enforcement.md) — validators over
   conventions: executable checks for every load-bearing graph rule, one
   gate command, domain-language linting, one-script rehydration, corpus
   routers, measured costs in docstrings.
11. [11-preregistration-and-claims.md](11-preregistration-and-claims.md) —
   append-only evidence: freeze protocols before expensive runs, the
   claims ledger, errata propagation, and numbered flags that block gated
   steps on spec conflicts.
12. [12-field-lessons-third-deployment.md](12-field-lessons-third-deployment.md) — verification under fire: the two-instruments rule, config-surface
   audits (flag names lie), seed discipline, session mortality +
   commit-per-finding, supervisor output-contracts, name-keyed cache
   staleness, fail-fast experiment culture, and delegation upgrades
   (idle≠done, resource green-lights, sibling fences).

## Provenance

Sources: the origin project's session-handoff lessons block, persistent
memory notes (verify-scripted-edits, evaluate-the-evaluator,
tests-narrate-themselves, et al.), and a transcript retrospective over the
session JSONLs. Docs 10-11 and delegation rules 7-9 come from a second
field deployment (2026-07): a research-instrument repo that ran this stack
through a multi-day autonomous marathon — ~130-node DAG, a six-part
validator gate, eleven preregistered experiment runs with zero protocol
deviations, and one machine-forced self-correction. Where a doc cites an incident, it really
happened in the deployment it names; the numbers are measured there —
recalibrate them in your own project with tools/context_probe.py and
ccusage. Doc 12 comes from a third deployment (2026-07): a GPU
model-training lab running audit-heavy experiment sessions — five
same-day defect catches, every one via two independent views of one
number disagreeing; one session death survived losslessly by
commit-per-finding; and a config-surface audit that retired a
pre-registered experiment built on a phantom knob.
