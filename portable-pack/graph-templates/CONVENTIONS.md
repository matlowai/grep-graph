# CONVENTIONS.md — Project Organization Rules (permanent, read me first)

**Purpose:** Every fact, question, decision, and dependency in this project must be
reachable by `grep` alone. We maintain a graph without a graph: stable IDs are the
nodes, one-line pointer fields are the edges, plain text is the database. Any agent
or human dropped into any single file must be able to grep its way to complete
context before acting.

**The prime directive:** `grep -rn "<ID>" .` returns EVERY place that ID matters —
its definition, everything it blocks, everything that informed it, and its
resolution. If you write about a node without using its ID token, you have broken
the graph.

---

## 1. ID namespaces (nodes)

| Prefix | Meaning | Numbering | Example |
|---|---|---|---|
| PRIN-n | Design principle | fixed, append only | PRIN-3 |
| Q-Xn | Open question | letter = section family, never renumbered | Q-G6 |
| DEC-nnnn | Decision | append-only ledger in DECISIONS.md | DEC-0002 |
| ST-n | Stress test / walkthrough | append only | ST-1 |
| RES-topic-n | Research finding | per topic | RES-{{TOPIC}}-1 |
| §n | Spec section anchor | matches SPEC section numbers | §5 |
| T-Xn | Task node (DAG) | letter = track, append only | T-{{TRACK}}1 |

Rules:
- IDs are **immutable**: never reused, never renumbered, never deleted.
- A resolved question is **tombstoned, not removed**: its entry stays where it was,
  status flips to RESOLVED, and it gains `resolved-by: DEC-nnnn`. Future greps for
  the question find the answer in one hop.
- New ID families require a DEC entry adding them to this table.
- TODO items get IDs (T-Xn) only once something else references them; before that
  they live as plain checklist lines under their section.

## 2. Edge vocabulary (one-line, greppable, comma-separated IDs)

```
ctx:          read-these-first pointers (sections, DECs, RES, ST)
blocks:       things that cannot proceed until this resolves
blocked-by:   the inverse
informs:      soft influence (design pressure, not a hard dependency)
resolved-by:  Q → DEC back-pointer (tombstone edge)
supersedes:   DEC → older DEC it replaces
amends:       DEC → the contract/spec section it changes
```

Edges live on the line(s) immediately after a node's header. No other syntax. No
actual graph files, no databases, no link formats that a plain grep can't follow.

## 3. Node format

Every node — question, decision, research finding, stress test — is written as:

```
Q-C4 · OPEN · <short title — what's actually undecided>
ctx: §5, §9, ST-1
blocks: <the DEC or task that cannot proceed until this resolves>
reminder: <the context capsule — enough that an agent seeing ONLY this grep hit
  knows what the node is and how to proceed>
```

Header line: `ID · STATUS · short title`. Statuses: OPEN | RESOLVED | PARKED |
SUPERSEDED. The `reminder:` line is the context capsule.

## 4. Canonical files

```
CONVENTIONS.md        this file. Read first, always.
INDEX.md              flat ledger of every ID: status, location, ctx, one-line
                      reminder. THE entry point for any task. Verify every session.
SPEC.md               the design spec (if any). Sections are §n anchors.
DECISIONS.md          append-only DEC ledger. Never edit old entries; supersede.
DAG.md                the execution view: T-Xn task nodes with blocked-by edges.
SESSION_HANDOFF.md    live rehydration scratch (overwritable; graduate before overwrite).
```

## 5. Agent operating procedure (binding)

1. **On task start:** read CONVENTIONS.md, then grep every ID in your task
   statement across the repo. Read all hits and their `ctx:` targets before
   writing anything.
2. **On writing:** every claim that touches an existing node must cite its ID
   inline. New questions get the next free Q-Xn in their family and an INDEX row
   with ctx + reminder, written at creation time — not later.
3. **On resolving a question (one atomic change, all four steps):**
   a. Append DEC-nnnn to DECISIONS.md (with ctx, amends, and the argument).
   b. Tombstone the Q where it lives (status → RESOLVED, add resolved-by).
   c. Apply the spec edits the DEC mandates (or list them as T- items if deferred).
   d. Update INDEX.md.
4. **On uncertainty:** PARK the question (status PARKED + reminder why), never
   silently drop it. Silence is a decision.
5. **Session end:** verify INDEX.md against reality (every ID present, statuses
   true). A stale INDEX is a broken build.

## 6. Grep contract examples (what "working" looks like)

```
grep -rn "Q-G6" .        → question tombstone + DEC-0002 + spec sections it changed
grep -rn "blocked-by" .  → the live dependency frontier
grep -c "OPEN" INDEX.md  → how much is left
```

<!-- OPTIONAL: if you run design and build in two environments (chat UI ⇄ agent
     repo), add a §7 here recording the crossing protocol: forward handoff
     (HANDOFF-n, versioned, append/supersede) and return handoff (BUILDLOG blocks,
     append-only). Both lanes write to the same grep-graph under these same rules. -->
