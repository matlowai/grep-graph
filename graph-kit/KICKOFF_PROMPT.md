# KICKOFF_PROMPT.md — paste everything below the line to your coding agent

Copy this folder into your repo (e.g. as `docs/graph-kit/`) first, then paste
the block below — as-is — to your coding agent (Claude Code, Codex, whatever)
from the repo root. It works on a fresh repo or an existing one.

---

You are setting up this repository's documentation-as-graph discipline: a
plain-text knowledge graph where stable IDs are nodes, one-line pointer
fields are edges, and `grep` is the query engine — so that any future agent
or human can grep their way to complete context from any single file.

**Step 1 — Read the kit in full.** Read every file in `docs/graph-kit/`
(README.md, SPEC.md, RITUAL_LADDER.md, GOTCHAS.md, CODE_POINTERS.md, and
everything in templates/). Do not skim: the failure catalog and the ritual
ladder change what you build in step 3. **If this repo already carries a
decision ledger** (DECISIONS.md or similar) or other graph docs, read every
decision recorded there IN FULL before proposing anything — recorded
decisions govern; supersede explicitly or follow, never silently
contradict.

**Step 2 — Calibrate before scaffolding.** Do NOT create any files yet.
Using the decision table in RITUAL_LADDER.md, ask me these questions (plus
any the table makes relevant), then tell me which ritual tier (0–3) you
recommend and why, and wait for my confirmation:

1. How long will this project live, and will it outlast single sessions —
   days, weeks, or months+?
2. How many agents will write code here (count subagents), and how many
   humans steer?
3. Are there decisions that are off-limits to the agent — schemas, public
   contracts, spend — that a human must own?
4. Does design/planning happen somewhere outside this repo (a chat UI, a
   docs app), or does everything happen here?
5. Mock policy — may agents ever build mocks, stubs, or synthetic
   stand-ins, or is this repo real-data-only? Real-only is the recommended
   default (GOTCHAS C5: a green test against a mock is evidence about the
   mock). Real-only does NOT mean unphased: complicated work is phased as
   contract/types first + an honest not-implemented error naming the real
   requirement, with heavy thinking done in pseudocode/design notes BEFORE
   real code — the data is never faked, only the sequencing is staged.

6. Subagent policy — will I be delegating work to subagents here, and if
   so, which model tiers / reasoning-effort levels may I use, with what
   spend comfort? Two calibrations if yes: the everyday default tier, and
   what class of work earns your most expensive tier. (Guardrail either
   way: work that produces or verifies a claim in the project's core
   domain never delegates below the top tier available; mechanical chores
   never waste it. If a fuller agent-tier bundle came alongside this kit,
   its definitions carry the patterns to copy — otherwise I'll record the
   policy as a ground rule and spawn ad hoc.)

Also explain to me, before scaffolding, the context strategy this system
assumes: explicit /clear + the rehydration file instead of automatic
compaction — compaction works but degrades performance and burns more
tokens because it summarizes less deliberately than a handoff written at a
seam. Make sure I understand it, because it changes how I'll work with you
day to day.

Recommend the LOWEST tier the answers support — the ladder says start low
and upgrade on named triggers, because unearned ritual is a per-session tax
and a stale graph is worse than no graph. Record the mock-policy answer,
the subagent-tier/budget answers, and the context-strategy acknowledgement
as ground rules in the instructions file (and as DECs at Tier 2+) so no
future session has to re-ask them.

**Step 3 — Scaffold for the confirmed tier.** Copy from
`docs/graph-kit/templates/` into the repo root and adapt — don't invent your
own formats, and don't include files above the confirmed tier:

- Tier 0: `templates/AGENTS.md` only (rename to CLAUDE.md if that's what I
  use), filled in for this project.
- Tier 1: add `SESSION_HANDOFF.md` and a `LEARNINGS.md` (dated `##` sections,
  append-mostly).
- Tier 2: add `CONVENTIONS.md`, `INDEX.md`, `DAG.md`, `DECISIONS.md`,
  `ASSUMPTIONS.md`.
- Tier 3: all of the above, plus enable the dual-lane section (CONVENTIONS §7
  / SPEC §10): HANDOFF.md and an append-only BUILDLOG.

While adapting: fill every `{{PLACEHOLDER}}` from what you can see in the
repo plus my answers (ask me only for ones you genuinely can't infer, like
spend policy); delete worked-example rows and template comments you don't
use; if this repo will ever coordinate with a sibling repo's agents, prefix
all IDs with a short project slug. If any of these files already exist,
MERGE — never blind-overwrite.

**Step 4 — Seed the graph with real nodes, not placeholders.**
- Mint `DEC-0001` in DECISIONS.md: adoption of this system, dated today.
- Put the project's actual next 3–8 pieces of work into DAG.md as T-nodes
  with real `blocked-by:` and `evidence:` lines (if you can't write a task's
  evidence line, tell me it isn't specified yet).
- Write a true SESSION_HANDOFF.md for the current state.
- Fill INDEX.md with rows for every ID you just minted.
- Wire the reading order into AGENTS.md/CLAUDE.md so every future session
  starts with: handoff → conventions → index/DAG → grep the task's IDs.

**Step 5 — Verify (do not skip).**
- `grep -rn "{{" <the files you created>` returns nothing.
- Pick one ID you minted and run `grep -rn "<ID>" .` — confirm it returns
  the node, its INDEX row, and every reference, and nothing dangling.
- Confirm every DAG task has evidence, every question/parked item has a
  reminder capsule, and INDEX matches reality.
- Then report back: the tier, the files created, the IDs minted, and the
  one-line grep contract ("grep any ID to get its full context").

From then on, follow CONVENTIONS.md §5 as binding procedure, consult
GOTCHAS.md before scripted edits / commits / session ends, and apply
CODE_POINTERS.md as code lands: IDs go in assert messages, required-config
errors, and load-bearing comments — not sprinkled everywhere. Upgrade the
tier only when a trigger from RITUAL_LADDER.md actually fires, and tell me
when one does.
