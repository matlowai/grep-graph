# RITUAL_LADDER.md — how much ceremony does your project actually need?

The full system in SPEC.md is the top of a ladder, not the entry fee. Ritual
has real costs: every file you promise to maintain is a tax on every session,
and a stale graph is WORSE than no graph, because agents trust it. This file
calibrates the level. Read it before scaffolding anything.

## The tiers

### Tier 0 — Instructions file only
**One file:** `CLAUDE.md` / `AGENTS.md` — what the project is, conventions,
a "do not" list, how to run/test.

For: throwaway and days-scale projects, one human + one agent, nothing worth
remembering between sessions. No IDs, no ledgers. The gotchas in
GOTCHAS.md §B–C still apply (they're about agent mechanics, not ritual).

### Tier 1 — The notebook
**Adds:** `SESSION.md` (rehydration capsule, SPEC §7) and `LEARNINGS.md`
(append-mostly lessons/gotchas log, dated sections).

For: weeks-scale solo projects that outlive a context window. This buys
session continuity and stops re-paying for the same mistakes. Still no
stable IDs — cross-referencing is section headers, file paths, commit SHAs.

What it doesn't buy: **decision archaeology**. In the real Tier-1 specimen
below, recovering *why* any settled choice was made meant grepping a
1,400-line lessons scroll or reading git log — the exact failure Tier 2's
ledger exists to prevent.

### Tier 2 — The ledger (the sweet spot for most serious projects)
**Adds stable IDs and the core graph:** `DECISIONS.md` (or ADR files) +
`DAG.md` (tasks with `blocked-by:`/`evidence:` edges) + `INDEX.md` (thin
router) + `ASSUMPTIONS.md`, plus the code-pointer discipline
(CODE_POINTERS.md) and tombstoning.

For: months-scale projects, anything multi-agent, anything where "wait, why
did we do X?" has been asked twice. This is where the prime directive starts
paying: any agent can grep from any file to full context.

Deliberately NOT included at this tier: question-node families, formal
handoff protocols, authority splits. A solo agent with standing authority
doesn't need a lane fence — one concurrency line suffices ("only the main
session edits the graph docs").

### Tier 3 — The full graph
**Adds:** Q-node question families with tombstoning, versioned forward
handoffs + append-only return logs between a design lane and a build lane
(SPEC §10), contract-amendment tracking, principle nodes, cross-repo
coordination channels, and an operating-procedure pack agents must read at
session start.

For: multi-month, multi-agent, multi-environment projects where design
happens somewhere other than the build repo, contracts/schemas are shared
with other systems, and an agent acting outside its authority causes real
damage. The authority split is the point of this tier: the build lane PARKS
design-owned questions rather than resolving them, even when the answer
seems obvious.

## The three specimens (real projects, honestly characterized)

**Specimen A — Tier 1+, multi-service production stack.** ~400 source files,
~11 weeks, 285 commits, 38 numbered sessions, one build agent coordinating
with a sibling repo's agent. Ritual: instructions file + rehydration file +
lessons scroll + a signed cross-repo channel. Two practices here were BETTER
than the heavyweight specimen's and are folded into this kit:
- **Mode-scaled ceremony:** each session declares a mode (build / audit /
  research / relay), and the mode sets how much open/close ritual is owed. A
  narrow build session pays almost nothing; only audit/relay pay full freight.
- **Machine-verifiable handoff:** a small YAML/JSON state block generated and
  CHECKED by scripts, with provenance on every count. A prose handoff can
  lie; a verified one can't.
Failure modes, equally real: no decision ledger (settled choices re-derived
from prose), session-scoped task labels meaning task history evaporates, and
the lessons scroll narrating the same lesson in three places.

**Specimen B — Tier 2, solo agent at high intensity.** ~60K LOC polyglot
monorepo, 162 commits in 5 days, ONE agent with standing commit authority.
Ritual: full stable-ID graph (project-prefixed IDs, ADR-per-file decisions,
DAG with `evidence:` edges, assumptions ledger with revisit triggers) but no
lanes, no handoff protocol, one concurrency line. The IDs stayed contiguous
and unbroken — proof a solo agent can run a real graph cheaply. Its three
best ideas are adopted in SPEC.md: the `evidence:` edge, the thin
INDEX-as-router (statuses live in ONE file), and the assumption→decision
promotion path. Its failure mode: the rehydration capsule bloated to 71 KB
because no second reader ever forced graduation — solo repos need a size
budget where multi-agent repos have social pressure.

**Specimen C — Tier 3, multi-month contract-driven build.** Dual-lane
(design in chat UI, build in an agent), multiple subagent tiers, shared
contracts with two sibling repos, ~1,700 ID back-references in code, an
operating-procedure pack every session must read. The ritual demonstrably
works — continuity across 25+ sessions, decisions never re-litigated — but
it is EXPENSIVE: session start is a substantial reading list, session end is
a checklist, and statuses mirrored across two files need a verification pass
every session. This tier is justified by its multi-agent, split-authority,
contract-bearing shape; it would crush a solo project.

## Decision table

Score your project; take the HIGHEST tier any row triggers.

| Question | Tier it triggers |
|---|---|
| Will this outlive one context window / one sitting? | 1 |
| Have you re-derived or re-argued a settled decision? | 2 |
| More than one agent (subagents count) writing code? | 2 |
| Has anyone asked "why did we decide X?" and gotten a shrug? | 2 |
| Does work have real dependency structure worth running in parallel? | 2 |
| Do design conversations happen OUTSIDE the build repo (chat UI, docs app)? | 3 |
| Do agents have different authority levels (some decisions off-limits)? | 3 |
| Are schemas/contracts shared with other repos or teams? | 3 |
| Multiple humans steering different lanes? | 3 |

Defaults by shape: throwaway → 0 · solo hobby, weeks → 1 · anything you'd
call "a real project" → 2 · multi-agent + split authority + external
contracts → 3.

## Start low, upgrade on triggers

**Start at Tier 1 unless the table clearly says otherwise.** Upgrading is
cheap (the templates are in this kit; history converts forward — a lessons
entry can become a DEC); maintaining unearned ritual is a per-session tax
forever. Upgrade when you feel the specific pain:

- **You re-derived a settled decision** → add DECISIONS.md, start minting
  DEC IDs. (You don't have to backfill; start from today.)
- **A cleared/expired session cost >10 minutes of reconstruction** → add the
  rehydration file and the checkpoint habit.
- **Two docs disagreed about state** → add INDEX-as-router + the session-end
  verification step, and make one file authoritative per fact.
- **A second agent joined** → Tier 2 minimum, plus the one-writer rule for
  graph docs.
- **An agent resolved something it shouldn't have** → that's the Tier 3
  authority split knocking. Write the lane fence.
- **You coordinate with another repo's agent** → add the signed append-only
  channel file (SPEC §10), whatever your tier.

And the honest downgrade signal: **if a file has been stale for three
sessions and nobody noticed, delete the ritual, not just the staleness.** A
graph nobody feeds is worse than no graph — agents trust it, and it lies.

## Condition-triggered add-ons (orthogonal to the tiers)

Each of these is cheap, pays only under its stated condition, and adds no
per-session tax when the condition is absent. (Their measured token
economics live in portable-pack-style bundles; what earns them a place HERE
is that each also makes the graph more testable or more navigable.)

- **Rehydrate script** — *condition: the session-start reading list is ≥3
  files.* A ~20-line script that emits the whole bundle (handoff,
  assumptions ledger, index, decision gates, live frontier) in one output,
  so a fresh session starts with ONE tool call. The under-appreciated
  benefit is correctness, not just cost: the ritual becomes executable — a
  renamed file or a broken command fails loudly at session start instead of
  silently dropping one document from a ceremony nobody re-tests. Pairs
  with GOTCHAS A9.

- **Reference-corpus router** — *condition: the repo carries reference
  material (paper analyses, vendored research, imported collections) far
  larger than any session could load.* One budgeted doc (about a handoff's
  size) that is the ONLY corpus file sessions load by default. Per source
  it carries: the task/decision ids that source feeds (source→task edges,
  so the grep contract covers the corpus), what each deeper document costs
  to read (size it once, write it down), and an extraction recipe for any
  monolithic file (how to pull one entry, never the whole thing). If an
  imported collection brought its own id scheme, every row carries BOTH
  ids — never rename immutable inputs; bridge them, so either id greps
  through one file. *Incident:* a corpus of paper analyses ~100x a
  reasonable read budget, whose own "index" was itself too large to ever
  load, had zero source→task edges — every corpus-touching task either
  flew blind or grossly overpaid. A 2k-token router fixed both, and the
  id bridge repaired a grep contract that two coexisting id schemes had
  silently broken.

- **Docs-current hash manifest** — *condition: doc drift keeps escaping
  review, or your setting demands high compliance (regulated work, many
  writers, low-trust automation).* Keep a manifest of content hashes for
  the directories/files your docs describe; a checker compares current
  hashes against the manifest and, on any mismatch without a matching
  docs update, the session must go figure out what changed (read the diff
  or the old commit) and update the documentation before the gate passes.
  Be honest with yourself: for most projects this is **overkill ceremony**
  — the checkpoint habit plus review catches the same drift for free. Its
  value is that it's fully *mechanistic*: no judgment, no memory, no good
  intentions required — which makes it the rare ritual you can push down
  into infrastructure (a GitHub Action, a Claude Code hook, a pre-commit
  hook, CI) and forget about. Adopt it as enforcement plumbing when the
  condition really holds, not as daily practice.

- **Reference-clone directory + pin manifest** — *condition: your work
  regularly studies adjacent code you don't own (upstream repos, prior-art
  projects, a vendor SDK).* Keep a **gitignored** `reference/` (or
  `.reference/`) directory for transient shallow clones and study copies —
  they're bulky, they're other people's licenses, and they don't belong in
  your history. What IS committed is a small `reference/PINS.md` manifest:
  one row per pin — name, upstream URL, commit sha, date pulled, license,
  and one line on why it's pinned. The manifest is the graph-visible part
  (a `RES-*` node can cite a pin; "verify at the pinned sha" beats "I
  remember their code"), the clones are disposable and re-fetchable from
  it. Session-end habit: if you consulted a new repo this session, its row
  goes in PINS.md before you close. Two standing rules ride along:
  neighbor clones are READ-ONLY (you study them, never edit them), and a
  license note is mandatory at pin time — "I'll check before shipping" is
  how NC-licensed code ends up load-bearing.
