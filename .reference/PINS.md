# PINS.md — pinned reference repos (.reference/ is a working area, not published)

**Why this file is committed while the folder around it is not:** this is
the kit's own reference-clone discipline (graph-kit RITUAL_LADDER, the
"reference-clone directory + pin manifest" add-on) practicing on itself.
The clones themselves are gitignored — they're bulky, they're other
projects' licenses, and they don't belong in this repo's history. The
manifest is the part worth keeping: it records exactly WHAT we studied, at
WHICH commit, under WHAT license, and WHY — so any claim built on that
study is re-verifiable ("re-fetch the pin, check the sha") instead of
"trust our memory of their code."

**Why these pins exist at all:** the README's "Where this fits" landscape
comparison (Spec Kit, BMAD, Task Master, and kin) was not written from
blog posts or training data — we cloned the actual repos and audited them
locally (does BMAD's memlog really append-only? what does Spec Kit's
memory/ directory actually hold?) before making any comparative claim.
These rows are the receipts for that section: if you want to check our
homework, every pin is one `git clone --depth 1` away at a known sha.

Shallow clones (`git clone --depth 1`) pulled for the SOTA-2026-07 landscape
survey. One row per pin: name · upstream · commit · pulled · license · why.

| name | upstream | commit | pulled | license | why pinned |
|---|---|---|---|---|---|
| spec-kit | https://github.com/github/spec-kit | 57cc518d63d6 | 2026-07-20 | MIT | Primary workflow-layer comparator; verify memory/ + constitution mechanics first-hand |
| bmad-method | https://github.com/bmad-code-org/BMAD-METHOD | 8b4da79161f1 | 2026-07-20 | MIT | Second workflow-layer comparator; verify whether v6-era BMAD grew decision-ledger/memory features |
| task-master | https://github.com/eyaltoledano/claude-task-master | c0c98d367c55 | 2026-07-20 | Task Master License (source-available; check terms before reuse) | Task-graph comparator: PRD→tasks with dependency tracking; contrast with DAG.md frontier model |
| 12-factor-agents | https://github.com/humanlayer/12-factor-agents | d20c728368bf | 2026-07-20 | Apache-2.0 | Canonical context-engineering manifesto (24.6k stars); note default branch last commit 2025-09-21, active work moved to follow-on repos |
| agent-os | https://github.com/buildermethods/agent-os | cae8e664fb59 | 2026-07-20 | MIT | Standards-injection + spec workflow comparator (Agent OS 3.0, Jan 2026); indie analog of a standards/profile layer |
