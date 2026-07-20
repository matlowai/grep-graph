# SPEC.md — The docs-as-graph system, in full

This is the complete generic specification. Everything else in this kit is
commentary, calibration, or templates for what's defined here.

## The problem this solves

Coding agents lose context: sessions end, context windows fill, a second agent
arrives knowing nothing. Prose documentation rots because nothing forces it to
stay true, and nothing makes it findable at the moment of need. The result is
the same failure over and over: an agent re-derives a settled decision, breaks
a constraint whose reason lived only in a dead chat transcript, or builds on
top of a plan that changed two sessions ago.

## The idea: a graph without a graph

Maintain the project's knowledge as a graph using no graph tooling at all:

- **Stable IDs are the nodes.** Every decision, task, open question, and
  assumption gets a short immutable token (`DEC-0007`, `T-A3`).
- **One-line pointer fields are the edges.** `blocked-by: T-A2` directly under
  a node's header is a dependency edge anyone — human or agent — can follow.
- **Plain text is the database. `grep` is the query engine.**

**The prime directive:** `grep -rn "<ID>" .` must return EVERY place that ID
matters — its definition, everything it blocks, everything that informed it,
and its resolution. If you write about a node without using its ID token, you
have broken the graph. This single rule is what makes everything else work:
an agent dropped into any one file can grep its way to complete context
before acting.

## 1. ID namespaces (the node types)

Adapt the set to your project; these four are the core, the rest are optional.

| Prefix | Meaning | Lives in |
|---|---|---|
| `DEC-nnnn` | Decision — a choice that was made, with its reasoning | DECISIONS.md (append-only) |
| `T-Xn` | Task — a unit of work with dependencies (letter = track) | DAG.md |
| `ASM-n` | Provisional assumption — a reversible call made to avoid stalling | ASSUMPTIONS.md |
| `Q-Xn` | Open question — something undecided that other work waits on | wherever it arose + INDEX.md |
| `PRIN-n` | Standing principle (optional) | your spec or conventions file |
| `RES-topic-n` | Pinned research finding (optional) | a reference file |
| `§n` | Section anchor in your spec (optional) | SPEC/ARCHITECTURE doc |

Rules:

- **IDs are immutable** — never reused, renumbered, or deleted. A dead node is
  tombstoned (see §4), never erased. *Why:* the moment an ID can change,
  every grep result becomes untrustworthy and the graph is dead.
- **If your agent works across multiple repos, prefix IDs with a project
  slug** (`ACME-T012` instead of `T-12`). *Why:* bare IDs collide when two
  repos coordinate, and a cross-repo grep can't tell whose `DEC-0003` it hit.
  Single-repo projects can skip the prefix.
- **New ID families require a decision entry** adding them to the table in
  your CONVENTIONS.md. *Why:* namespaces that appear ad hoc drift and collide.
- **TODO items get task IDs only once something else references them.**
  Before that, they're plain checklist lines. *Why:* minting IDs for every
  passing thought buries the real nodes in noise.

## 2. Edge vocabulary (the only link syntax allowed)

Edges are one-line fields on the line(s) immediately after a node's header,
with comma-separated ID targets:

```
ctx:          read-these-first pointers before touching this node
blocks:       things that cannot proceed until this resolves
blocked-by:   the inverse — this node waits on those
informs:      soft influence (design pressure, not a hard dependency)
resolved-by:  question → decision back-pointer (the tombstone edge)
supersedes:   decision → older decision it replaces
amends:       decision → the spec/contract section it changes
evidence:     what observable proof marks this task DONE (tasks only)
```

No other link syntax. No wiki-links, no relative-path markdown links between
graph nodes, no databases. *Why:* every one of those breaks under plain grep,
and grep is the only query engine every tool and every agent shares.

`evidence:` deserves a note: putting the done-criterion in the graph itself
("evidence: the demo script exits 0 and the log shows a synthesized reply")
turns "done means proven" from a habit into a checkable field. Projects that
adopted it stopped arguing about whether a task was finished.

## 3. Node format

Every node — decision, task, question, assumption — is written the same way:

```
Q-C4 · OPEN · Multi-tenant rate-limit strategy
ctx: §5, DEC-0011
blocks: T-B7
reminder: per-tenant buckets vs global pool; billing team leans per-tenant;
  decide before the gateway rewrite starts or T-B7 builds the wrong shape.
```

- **Header line:** `ID · STATUS · short title`.
- **Statuses:** `OPEN | IN-PROGRESS | RESOLVED | DONE | PARKED | SUPERSEDED`
  (tasks additionally use `FRONTIER | BLOCKED` — see §6).
- **The `reminder:` line is the context capsule** — enough that an agent
  seeing ONLY this grep hit knows what the node is and how to proceed. Write
  it for a stranger with zero conversational context, because that is
  literally who reads it. A node without a reminder is a mystery token.

## 4. Tombstoning (nothing vanishes)

A resolved question is **tombstoned, not removed**: its entry stays where it
was, status flips to `RESOLVED`, and it gains `resolved-by: DEC-nnnn`. A
replaced decision stays in the ledger; the new one carries `supersedes:`.

*Why:* future greps for the old question must find the answer in one hop.
Deleting resolved nodes recreates the exact problem the graph exists to
solve — "wait, didn't we already decide this?" with no trail. If you are
deleting graph text, you are almost certainly wrong.

## 5. The decision ledger (append-only)

`DECISIONS.md` is append-only. Never edit an old entry; append a new DEC with
`supersedes:` instead. A decision entry carries: what was decided, the
alternatives considered, why, and what it amends.

*Why append-only:* the ledger is the project's memory of *why*. Edited-in-place
decisions silently rewrite history, and the next agent re-litigates a settled
argument because the losing alternatives — and the reasons they lost — are
gone. One real lightweight project kept decisions as prose in a lessons file;
recovering *why* any settled choice was made meant grepping 1,400 lines of
narrative or reading git log.

**Variant:** one-file-per-decision (ADR style, `docs/adr/ADR-0007-*.md` with a
template) works equally well and diffs more cleanly. Pick one; the invariants
are the same: immutable IDs, append/supersede, never edit history.

## 6. INDEX vs DAG — the ledger and the execution view

Two files with different jobs:

- **INDEX.md** — the flat ledger of every ID: one row per node with status,
  location, and a one-line reminder. THE entry point for any task.
  `grep -c "OPEN" INDEX.md` tells you how much is undecided.
- **DAG.md** — the execution view: task nodes with `blocked-by:` edges. A task
  is **FRONTIER** when everything it's blocked by is DONE — frontier tasks in
  independent tracks can run in parallel (separate sessions or subagents).
  `grep -n "blocked-by" DAG.md` is the live dependency map.

**Statuses live in exactly ONE file per node type.** Task statuses live in
DAG.md; INDEX.md rows for tasks either mirror mechanically or — better, for
smaller projects — just point ("tasks: see DAG.md"). *Why:* the mid-size
specimen this kit studied keeps its INDEX as a deliberately tiny router
("do not infer progress from this file") and had zero status drift; the
heavyweight specimen mirrors statuses in both files and must spend a
verification pass every session keeping them honest. Duplicated state is a
standing invitation to disagreement.

Keep the DAG honest in real time: flip a task to IN-PROGRESS when you start,
DONE when *verified* (see `evidence:`). **Mint the node BEFORE building** —
new work gets its T-node with `blocked-by:` edges at creation time, not
retroactively. *Why:* a stale DAG hides the true frontier; work done on
unminted nodes is invisible to every other session and agent.

## 7. Session continuity — the rehydration file

`SESSION_HANDOFF.md` (call it SESSION.md if you like) replaces context
compaction. A fresh session reads it FIRST and continues where the last one
left off. It holds: current state in 2–4 sentences, current task + why, files
touched, decisions in flight, next concrete steps, and gotchas/dead ends.

Rules:

- **Update it as you work** — at checkpoints, not just session end. A session
  can die or be cleared at any moment; the file is only useful if it's true
  right now.
- **It is overwritable scratch — but graduate before you overwrite.** Before
  trimming any block, anything worth keeping MUST first land in a durable
  home (a DEC, a DAG node reminder, a lessons entry). The test: would losing
  this text cost ten minutes of re-derivation? Then it doesn't live only in
  scratch. When in doubt, append now and graduate at the next checkpoint.
- **Keep it targeted** — what a fresh session needs, not a transcript. The
  solo-agent specimen this kit studied let its capsule grow to 71 KB because
  no second reader ever forced graduation; past a few hundred lines the
  capsule stops being a capsule. Budget it (say, 150 lines) and archive
  overflow to a dated file under `docs/sessions/`.

Two upgrades observed working well in a lighter-ritual project, optional here:
a short machine-readable state block at the top (YAML: session number, service
health, next goal) that a script can verify, and a **"Do not" list** — the
3–6 standing prohibitions a fresh agent is most likely to violate.

## 8. Provisional assumptions (the anti-stall valve)

Sometimes the next step is blocked only because a human hasn't reviewed
something yet, and no review is coming this session. Don't stall, and don't
silently decide either. Instead:

1. Pick the best-reasoning-supported option.
2. Act on it.
3. Log an `ASM-n` node in ASSUMPTIONS.md: what you chose, the alternatives,
   why, and a **revisit trigger** ("revisit when the auth provider is chosen").

The underlying question stays OPEN — an ASM substitutes for *stalling*, not
for authority. The human reviews ASSUMPTIONS.md at check-ins, ratifies or
reverses each entry, and a ratified ASM can graduate into a real DEC.
*Why:* the alternative is either dead sessions ("waiting on you") or invisible
unilateral calls baked into code. A logged, reversible assumption is the
opposite of both.

Statuses: `PROVISIONAL | RATIFIED | REVERSED`.

## 9. Agent operating procedure (the binding loop)

1. **On task start:** read CONVENTIONS.md, then grep every ID mentioned in
   your task across the repo. Read all hits and their `ctx:` targets before
   writing anything.
2. **On writing:** every claim that touches an existing node cites its ID
   inline. New nodes get their INDEX row at creation time — not later.
3. **On resolving a question — one atomic change, all steps:** append the
   DEC; tombstone the Q where it lives (`RESOLVED` + `resolved-by:`); apply
   the edits the DEC mandates (or list them as tasks in the DEC — a decision
   with unapplied edits must say so); update INDEX.md.
4. **On uncertainty:** PARK the question (status `PARKED` + a reminder saying
   why and what re-entry looks like) — never silently drop it. **Silence is a
   decision**, and it's the one kind you can't grep for. If the block is
   merely a pending human review, use §8 instead of parking productive work.
5. **Session end:** verify INDEX.md against reality — every ID present, every
   status true. A stale INDEX is a broken build: it's the entry point, and an
   entry point that lies poisons every session that trusts it.

## 10. OPTIONAL MODULE — dual-lane authority (skip unless it describes you)

Most projects have one lane: an agent (or a few) building, a human steering.
Skip this section if that's you.

Some projects genuinely run **two environments with different strengths**:
design happens in a chat UI (long-form reasoning, web research, the human
present), building happens in a repo-attached agent. If that's your shape,
make the crossing explicit or context decays at every handoff:

- **Split authority in writing.** The design lane owns spec/contract changes,
  question resolutions, and principles. The build lane owns implementation
  decisions, code, and tests — and PARKS anything design-owned rather than
  resolving it unilaterally, even when the answer seems obvious.
  Obvious-to-you is how scope boundaries get broken.
- **Forward handoff:** design appends a versioned `HANDOFF-n` block (scope,
  authority granted, what's out) to a HANDOFF.md — superseded, never silently
  edited.
- **Return handoff:** the build lane appends a block to an append-only
  BUILDLOG: summary, new DEC IDs, parked items, "design input needed" flags.
  That block is the literal paste-back that opens the next design session.
- Both lanes write to the same grep-graph under the same rules.

If two agents in different repos coordinate, give them one shared append-only
channel file with signed, dated entries (`### [date · agent-A → agent-B]`),
replies appended never edited, and a standing header: scratch not record —
authoritative state stays in each repo's own graph; never put secrets here.

## The grep contract (what "working" looks like)

```
grep -rn "Q-C4" .          → the question + everything it blocks + its resolution
grep -rn "blocked-by" DAG.md → the live dependency frontier
grep -c "OPEN" INDEX.md    → how much is undecided
grep -rn "DEC-0007" src/   → every line of code that decision governs
```

That last one is the payoff most teams miss — see CODE_POINTERS.md.

## Why plain text, and not an actual graph database

Fair question — this system *is* a graph, so why isn't it in Neo4j (or
SQLite, or a vector store)? The direction was chosen deliberately:

- **The graph lives where the agents already are.** File reads and grep
  are every coding agent's native, zero-setup tools. No server to run, no
  driver to install, no schema migration, no auth — an agent dropped into
  the repo has full query access in its first tool call, and so does a
  human with a text editor.
- **The graph versions WITH the work it describes.** Nodes and edges ride
  the same commits, branches, and PRs as the code. A decision and the code
  it shaped diff together, revert together, and get reviewed together — a
  side-database's history never lines up with the repo's.
- **Write friction is a feature.** Text edits are visible in review;
  database writes are invisible side effects. The discipline (append-only
  ledgers, tombstones, reminder capsules) survives precisely because every
  write is a reviewable diff.
- **The queries you actually need are grep-shaped.** The load-bearing
  query is one-hop reachability: "every place this ID matters." That is
  literally `grep -rn "<ID>" .`. The frontier is a `blocked-by` scan. None
  of the daily queries need traversal, aggregation, or joins — paying a
  database's operational cost for queries grep answers instantly is
  ceremony without a condition.
- **Plain text is the most durable format there is.** It will outlive any
  database engine, driver version, and this document.

**When a real database starts making sense** — honest triggers, not
never: (a) you routinely need queries grep can't express — transitive
closure over long chains ("everything downstream of this decision"),
aggregate analytics across thousands of nodes, similarity search; (b) the
graph outgrows repo scale — many repos' graphs need to be queried as one;
(c) non-agent consumers arrive — dashboards, org-wide search, reporting.

If you get there, **derive the database; don't move the truth.** Keep the
plain-text graph canonical and build a small indexer that parses nodes and
edges into whatever store you need (the strict node/edge format was
designed to be machine-parseable for exactly this reason). The database
becomes a rebuildable materialized view — you gain the query power without
giving up versioning-with-the-code, review-visible writes, or the
zero-setup access agents depend on. A database that becomes the source of
truth quietly deletes every property in the list above.
