# grep-graph

You probably already give your coding agents *something* — a CLAUDE.md, a
notes file, memory features, compaction. That works right up until the
project outgrows it: sessions re-derive settled ground, agents confidently
contradict decisions you made two weeks ago, and nobody — human or model —
can answer *why* the code is the way it is without an archaeology dig.

This repo is the structure for that next stage: a project-organization
system for agent-driven development where **stable IDs are the nodes,
one-line pointer fields are the edges, and `grep` is the query engine** —
so any agent dropped into any file can grep its way to complete context
before acting, and the answer to "why?" is always one hop away.

It was extracted from live projects that run this way daily: the origin
build (a multi-month, multi-agent project), two further independent field
deployments of the pack (a research instrument, a model-training lab), and
two sibling projects run at deliberately lighter ceremony — the ritual
ladder's three "specimens" are drawn from across that set, not a separate
trio. Nothing here is theory; every rule carries the incident that minted
it.

## If you are an agent reading this: start here

A human probably just pointed you at this repo — hi. The advice in here
works best as a whole, so the ideal first move is to read all of it and
*then* talk it through with your operator: that way you can give them a
recommendation mapped to their actual project instead of a summary of the
first file you opened.

**Size, measured:** the entire repo is ~48k tokens (o200k_base; Claude-
family tokenizers run a little higher, so budget ~55k). That fits
comfortably in one modern context. If your context budget for this is
tighter, read in this priority order:

- **~55k+ to spare** — read everything, both kits. Recommended.
- **~30k** — this README plus all of [graph-kit/](graph-kit/) except
  `templates/` (~18k together); defer portable-pack until your operator
  wants the full stack.
- **~15k** — this README, graph-kit's
  [SPEC](graph-kit/SPEC.md) + [RITUAL_LADDER](graph-kit/RITUAL_LADDER.md) +
  [KICKOFF_PROMPT](graph-kit/KICKOFF_PROMPT.md) (~11k); pull
  [GOTCHAS](graph-kit/GOTCHAS.md) and
  [CODE_POINTERS](graph-kit/CODE_POINTERS.md) on demand, and open
  `templates/` only when you actually scaffold.

However deep you read, cover these when you talk with your operator:

1. **How this system would best help THEIR project** — map the ritual
   ladder to what they're actually doing; don't recite the docs back.
2. There are **`{{PLACEHOLDERS}}` throughout** (inventory in
   [portable-pack/INSTALL.md](portable-pack/INSTALL.md)) that must be
   customized to their project before anything here is load-bearing.
3. If the repo you're installing into **already has a decision ledger**
   (DECISIONS.md or similar), read the decisions recorded there before
   proposing anything — recorded decisions govern; supersede them
   explicitly or follow them, never silently contradict them.
4. The two conversations below (subagent tiers, context strategy) are
   **operator decisions, not yours** — raise them, don't decide them.

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

**Prefer a managed install?** Fork this repo, then add your fork as a git
submodule instead of copying:

```
git submodule add https://github.com/<your-fork>/grep-graph docs/grep-graph
```

The kit stays a tracked dependency: improvements land in your fork once and
`git submodule update --remote` propagates them to every project using it.
Your per-project customizations never collide with updates, because
templates are **copied out and adapted** (scaffolded docs live at your repo
root), never edited inside the kit. Honest caveat: submodules add a little
collaborator friction (`git clone --recurse-submodules`, one more concept
to know), so the plain copy stays the zero-friction default — reach for
the submodule when you run several projects and want kit updates to reach
all of them from one place.

## Subagent tiers, and Fable-class effort levels

[portable-pack/agents/](portable-pack/agents/) ships delegation-tier
subagent definitions (mechanical → default executor → hard-but-specified,
plus a read-only sounding board) and the report contract they share. If the
operator's stack includes a **top-tier model with selectable reasoning
effort** (low / medium / high / xhigh / max — we shorthand this
"Fable-class" after the frontier tier we run; substitute your provider's
top line), the installing
agent should ASK the operator whether they want those as subagent options
too — and if yes, create the `fable-low` … `fable-max` definitions
following the exact patterns in the referenced agents (same frontmatter,
same report contract, same fences; only model and effort change).

Have the budget conversation explicitly, don't assume it: top-tier
subagents are the right call for **domain-substance work** — anything that
produces or verifies a claim in the project's core domain (upskilling doc
06, rule 6) — and a waste on mechanical chores. Ask the operator their
comfort level on spend, which effort level should be the everyday default,
and what class of work justifies xhigh/max. Record the answers as a
decision entry so no future session re-litigates them.

## Context strategy: /clear over compaction, deliberately

This system is built around **explicit `/clear` + a rehydration file**
(SESSION_HANDOFF.md) rather than automatic context compaction — and the
operator should understand why, because it shapes daily workflow.

Compaction works, and you can use it. But it summarizes mid-flight,
choosing what to keep by algorithm at a moment you didn't pick — so
performance degrades (the model continues from a lossy summary of its own
reasoning) and token burn runs **higher**, not lower, because the
compacted session keeps re-billing a larger, less relevant context than a
fresh one would. A deliberate handoff inverts every one of those defaults:
*you* choose the seam (a closed milestone, a natural pause), *you* write
what the next session actually needs while it's still cheap to know, and
`/clear` then costs one small rehydration read into a clean context.
Measured in the origin projects, the handoff pattern made session death
boring — crashes, resets, and multi-day gaps all resume cleanly from the
same file. Treat compaction as the fallback for a session that must not
stop, and as the expensive, lossy path — never the default.

## Where this fits (the 2026 landscape, honestly)

Verified against the field in July 2026 — these are composition notes, not
a takedown:

- **An AGENTS.md / CLAUDE.md** (now the emerging cross-tool standard) *is*
  Tier 0 of the ritual ladder. If yours is still working, keep it — this
  repo is what you upgrade to when it stops scaling.
- **Spec-driven workflow layers** (GitHub Spec Kit, BMAD-METHOD, and kin)
  organize how work *enters* a project — specify, plan, stories. They
  compose with this system rather than compete: accepted plans mint task
  nodes with edges, a constitution maps to your CONVENTIONS, and their
  working logs (some are even append-only now) hold material that
  *graduates* into decision entries. What they don't ship is the other end
  of the timeline: structured archaeology you can grep from the code.
- **Memory layers** (fact stores, platform auto-memory) remember *what* —
  state, preferences, entities. This system is the *why* layer — decisions
  with alternatives, tombstoned questions, IDs cited from the code that
  enforces them. Run both; they don't overlap.
- Two things we could not find anywhere else as of this writing: **ritual
  calibration** (ceremony sized to project weight, with downgrade
  triggers) and the **closed grep loop** (one grep returning a decision's
  definition, dependents, resolution, and the code it governs). The
  ingredients exist scattered across ADR tooling and enforcement hooks;
  the closed loop is the product here. Token-economics *measurement* now
  exists as bolt-on analyzers elsewhere; what this repo teaches is
  economics as daily method.

## Provenance & license

Distilled 2026 from real deployments; incidents are anonymized but real.
MIT — see [LICENSE](LICENSE). Open workstreams live in [TODO.md](TODO.md) —
including benchmarking the kit itself honestly.

## Make it better

This is a let's-make-it-better project, not a finished artifact. If it
helped you, **star it** so other people find it. **Fork it** and bend it to
your project — that's literally the install instruction. And if you found
something — a gotcha we're missing, a rule that didn't survive contact with
your repo, a deployment story, a better way to say any of this — open an
issue or PR. The best contributions are field lessons with receipts:
genericize the war story the way
[the field-lessons doc](portable-pack/upskilling/12-field-lessons-third-deployment.md)
does it (no project nouns, one anonymized incident per rule, the rule the
incident minted). Every doc in here started life as somebody's bad
afternoon; yours are welcome too.
