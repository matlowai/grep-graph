# CONVENTIONS.md — Project organization rules (permanent, read me first)

<!-- Template from graph-kit. Fill {{PLACEHOLDERS}}, delete rows/sections your
     ritual tier doesn't use (see graph-kit RITUAL_LADDER.md), then delete
     these comments. Tier 2 projects typically keep everything except §7. -->

**Purpose:** every fact, question, decision, and dependency in this project
must be reachable by `grep` alone. We maintain a graph without a graph:
stable IDs are the nodes, one-line pointer fields are the edges, plain text
is the database. Any agent or human dropped into any single file must be
able to grep its way to complete context before acting.

**The prime directive:** `grep -rn "<ID>" .` returns EVERY place that ID
matters — its definition, everything it blocks, everything that informed it,
and its resolution. If you write about a node without using its ID token,
you have broken the graph.

---

## 1. ID namespaces (nodes)

<!-- Multi-repo coordination? Prefix IDs with a project slug: {{SLUG}}-T1. -->

| Prefix | Meaning | Numbering | Lives in |
|---|---|---|---|
| DEC-nnnn | Decision | append-only | DECISIONS.md |
| T-Xn | Task (letter = track) | append only | DAG.md |
| ASM-n | Provisional assumption | append only | ASSUMPTIONS.md |
| Q-Xn | Open question (letter = family) | never renumbered | where it arose + INDEX.md |
| §n | Spec/architecture section anchor | matches doc sections | {{SPEC_DOC}} |

Rules:
- IDs are **immutable**: never reused, never renumbered, never deleted.
- A resolved question is **tombstoned, not removed**: status flips to
  RESOLVED and it gains `resolved-by: DEC-nnnn`. Future greps find the
  answer in one hop.
- New ID families require a DEC entry adding them to this table.
- TODO items get task IDs only once something else references them.

## 2. Edge vocabulary (one-line, greppable, comma-separated IDs)

```
ctx:          read-these-first pointers
blocks:       things that cannot proceed until this resolves
blocked-by:   the inverse
informs:      soft influence (not a hard dependency)
resolved-by:  question → decision back-pointer (tombstone edge)
supersedes:   decision → older decision it replaces
amends:       decision → the spec section it changes
evidence:     the observable proof that marks a task DONE
```

Edges live on the line(s) immediately after a node's header. No other link
syntax — nothing a plain grep can't follow.

## 3. Node format

```
Q-C4 · OPEN · <short title — what's actually undecided>
ctx: §5, DEC-0011
blocks: T-B7
reminder: <the context capsule — enough that an agent seeing ONLY this grep
  hit knows what the node is and how to proceed>
```

Header: `ID · STATUS · short title`. Statuses: OPEN | IN-PROGRESS | RESOLVED
| DONE | PARKED | SUPERSEDED (tasks also: FRONTIER | BLOCKED). Every node
gets a `reminder:` capsule — write it for a stranger with zero context.

## 4. Canonical files

```
CONVENTIONS.md      this file. Read first, always.
INDEX.md            thin router: every ID → status-owner file + one-line
                    reminder. THE entry point. Verify every session.
DECISIONS.md        append-only DEC ledger. Never edit old entries; supersede.
DAG.md              execution view: T-Xn nodes with blocked-by/evidence edges.
                    Task statuses live HERE and only here.
ASSUMPTIONS.md      ASM-n provisional calls awaiting human review.
SESSION_HANDOFF.md  live rehydration scratch (overwritable; graduate anything
                    durable BEFORE overwriting).
{{SPEC_DOC}}        the design/architecture doc; sections are §n anchors.
```

## 5. Agent operating procedure (binding)

1. **On task start:** read this file, then grep every ID in your task across
   the repo. Read all hits and their `ctx:` targets before writing anything.
2. **On writing:** every claim touching an existing node cites its ID inline.
   New nodes get their INDEX row at creation time — not later. Mint the task
   node BEFORE building.
3. **On resolving a question (one atomic change):** append the DEC →
   tombstone the Q (RESOLVED + resolved-by) → apply the edits the DEC
   mandates (or list them as tasks in the DEC) → update INDEX.md.
4. **On uncertainty:** PARK (status + reminder + re-entry condition), never
   silently drop. Silence is a decision. If blocked ONLY on pending human
   review with a low-risk default: act + log an ASM-n instead of stalling.
5. **One writer:** during parallel work, only the main session edits the
   graph docs (INDEX/DAG/DECISIONS/ASSUMPTIONS/handoff).
6. **Session end:** verify INDEX.md against reality — every ID present,
   every status true. A stale INDEX is a broken build.

## 6. Grep contract examples (what "working" looks like)

```
grep -rn "Q-C4" .            → the question + its blockers + its resolution
grep -n "blocked-by" DAG.md  → the live dependency frontier
grep -c "OPEN" INDEX.md      → how much is undecided
grep -rn "DEC-0007" src/     → every code line that decision governs
```

<!-- ## 7. OPTIONAL — dual-lane authority (Tier 3 only; see graph-kit SPEC §10)
     If design happens outside this repo: name the two lanes, what each owns,
     the forward-handoff file (versioned HANDOFF-n, supersede never edit) and
     the return log (append-only). Build lane PARKS design-owned questions. -->
