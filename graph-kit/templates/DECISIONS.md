# DECISIONS.md — append-only decision ledger

<!-- NEVER edit an old entry. To change a decision, append a new DEC with
     `supersedes:`. This file is the project's memory of WHY; edited history
     means the next agent re-litigates settled arguments. If you prefer
     one-file-per-decision (ADR style, docs/adr/ADR-0001-title.md), keep the
     same fields and the same append/supersede invariants. -->

DEC-0001 · ACCEPTED · {{DATE}} · Adopt the grep-graph organization system
ctx: CONVENTIONS.md
informs: everything
reminder: stable IDs = nodes, one-line pointer fields = edges, plain text =
  database. Questions tombstone instead of vanishing. INDEX.md is the entry
  point. Agents follow CONVENTIONS §5. Motivation: agents and future
  sessions arriving without conversational context must be able to grep
  their way to complete context; no external graph tooling, ever.

---

<!-- Entry skeleton — copy for each new decision:

DEC-nnnn · ACCEPTED · YYYY-MM-DD · <imperative title — what was decided>
ctx: <IDs/sections that informed this>
supersedes: <older DEC, if any>     amends: <spec section, if any>
resolved-by-this: <Q- nodes this tombstones, if any>

**Decision.** <what was chosen, concretely.>
**Alternatives.** <what else was considered and why each lost — this is the
  part that stops future re-litigation.>
**Consequences.** <what this commits us to; edits it mandates (apply them
  now, or list the T- tasks that will — unapplied edits must be named).>

--- -->
