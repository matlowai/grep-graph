# graph-kit — docs-as-graph discipline for coding agents

A self-contained kit you copy into any repo to teach your coding agents
(Claude Code, Codex, anything that can read files and run grep) to maintain
the project's knowledge as a **plain-text graph**: stable IDs are the nodes
(`DEC-0007`, `T-A3`), one-line pointer fields are the edges (`blocked-by:`,
`resolved-by:`), and `grep` is the query engine. The payoff: sessions end,
context windows fill, new agents arrive — and nobody re-derives a settled
decision, breaks a constraint whose reason lived in a dead chat, or builds
on a plan that changed two sessions ago. Any agent dropped into any single
file can grep its way to complete context before acting.

The system is distilled from three real agent-run projects at three levels
of ceremony — a multi-month multi-agent build with ~1,700 ID references in
its code, a production stack run on a lightweight notebook ritual, and a
solo agent's high-intensity variant — including what each level costs and
where each one failed. You don't adopt all of it; you calibrate
(RITUAL_LADDER.md), which is most of what this kit adds over a conventions
file.

## Quick start

1. Copy this whole folder into your repo (e.g. `docs/graph-kit/`). It is
   standalone — nothing here points outside the folder.
2. Open `KICKOFF_PROMPT.md` and paste its prompt block to your coding agent.
3. The agent reads the kit, asks you 3–4 calibration questions, recommends a
   ritual tier, scaffolds the matching files from `templates/`, seeds them
   with your project's real first nodes, and verifies the graph greps clean.

No dependencies, no tooling, no lock-in: the whole system is markdown
conventions, and deleting it back out is just deleting files.

## What's in the box (reading order)

```
README.md          you are here
KICKOFF_PROMPT.md  the paste-to-your-agent bootstrap (the front door)
SPEC.md            the full generic system: IDs, edges, node format,
                   tombstoning, ledgers, INDEX vs DAG, session handoffs,
                   provisional assumptions, optional dual-lane module
RITUAL_LADDER.md   tiers 0-3: how much ceremony your project actually
                   needs, grounded in three real specimens; decision table
                   + upgrade triggers. Read before scaffolding.
GOTCHAS.md         the paid-for failure catalog: graph hygiene, shell/git
                   traps, false evidence, session continuity, multi-agent
CODE_POINTERS.md   how code cites the graph back (IDs in assert messages,
                   config errors, guard comments) — and when an ID is noise
templates/         ready-to-copy skeletons: CONVENTIONS, INDEX, DAG,
                   DECISIONS, ASSUMPTIONS, SESSION_HANDOFF, AGENTS.md stub
```

Total reading time: ~20 minutes for a human, one pass for an agent.

## Installing into an EXISTING project

The kickoff prompt handles this: the agent merges rather than overwrites,
and you don't backfill history — mint `DEC-0001` today, give your current
in-flight work its first task nodes, and let real usage grow the graph
forward. A lessons-learned file you already have can stay; entries graduate
into DEC nodes when something references them.

## Relationship to fuller bundles

This kit is deliberately ONLY the docs-discipline half of how the origin
project runs its agents. The other half — delegation-tier subagent
definitions, an operating-procedure "upskilling" pack, cost/context
management tooling — lives in portable-pack-style bundles that assume more
about your tooling (specific agent CLIs, model tiers, cost telemetry). If
you find yourself wanting coordinator/worker agent tiers or measured
context-economics rules, ask the person who gave you this kit for their
portable pack; graph-kit stands alone and neither requires nor conflicts
with it.

## The one rule, if you remember nothing else

**`grep -rn "<ID>" .` must return every place that ID matters** — its
definition, everything it blocks, everything that informed it, its
resolution, and the code it governs. Every convention in this kit exists to
keep that one promise true.
