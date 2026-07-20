# grep-graph

Your coding agents forget everything between sessions. This repo makes plain
text their memory and `grep` their database — a project-organization system
for agent-driven development where **stable IDs are the nodes, one-line
pointer fields are the edges, and any agent dropped into any file can grep
its way to complete context before acting.**

It was extracted from live projects that run this way daily: multi-agent
builds, multi-day autonomous runs, and three independent field deployments
(a performer engine, a research instrument, a model-training lab) whose
hard-won lessons are folded back in. Nothing here is theory; every rule
carries the incident that minted it.

## Two kits, pick your door

**[graph-kit/](graph-kit/)** — the documentation discipline, standalone.
IDs, edges, decision ledgers, session handoffs, and a **ritual ladder** that
calibrates how much ceremony your project actually needs (a weekend script
does not want a dependency DAG). Start here. The
[KICKOFF_PROMPT](graph-kit/KICKOFF_PROMPT.md) is the front door: paste it to
your coding agent and it will interview you, recommend the lightest tier
that fits, and scaffold your repo.

**[portable-pack/](portable-pack/)** — the full operating stack for teams
running serious agent fleets: delegation-tier agent definitions, the
twelve-doc upskilling pack (verification discipline, probe-first,
judge-validation, machine enforcement, preregistration, field lessons),
measured token economics, and a context probe. Install this when you have
multiple agents, real budgets, and work you cannot afford to re-derive.

## The one-paragraph pitch

`grep -rn "<ID>" .` must return every place that ID matters — its
definition, everything it blocks, everything that informed it, and its
resolution. Decisions are append-only and superseded, never edited.
Resolved questions are tombstoned, never deleted. A living handoff file
makes session death boring. Conventions that matter become executable
checks, because conventions decay and validators don't. That's the whole
system; the rest is calibration.

## Quick start

```
# gentle: docs discipline only
copy graph-kit/ into your repo as docs/graph-kit/
paste graph-kit/KICKOFF_PROMPT.md to your coding agent

# full stack: agent tiers + operating procedure
follow portable-pack/INSTALL.md
```

## Provenance & license

Distilled 2026 from real deployments; incidents are anonymized but real.
MIT — see [LICENSE](LICENSE). Contributions that generalize (new field
lessons, new gotchas with receipts) are welcome; project-specific war
stories should be genericized the way
[the field-lessons doc](portable-pack/upskilling/12-field-lessons-third-deployment.md)
does it.
