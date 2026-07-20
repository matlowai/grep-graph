# AGENTS.md — {{PROJECT_NAME}} (agent working environment)

<!-- Rename to CLAUDE.md if your tool reads that instead — same content.
     This stub wires the graph docs into your agent's session loop. Fill the
     {{PLACEHOLDERS}}, delete sections below your ritual tier (see graph-kit
     RITUAL_LADDER.md), merge — don't blind-overwrite — any existing file. -->

One-line vision: {{ONE_LINE_VISION}}.

## Who you are here

You are the main agent in {{PROJECT_NAME}}. Implementation decisions are
yours — record them as DEC entries in DECISIONS.md. Anything touching
{{RESERVED_TERRITORY — e.g. "the public API contract, the data schema,
spend policy"}} is decided by the human: PARK it with a reminder, or if
you're blocked only on pending review and a low-risk default exists, act
and log an ASM-n in ASSUMPTIONS.md.

## Session start — read in this order (IN FULL, not skimmed)

A session that skims re-derives settled ground.

1. `SESSION_HANDOFF.md` — live state. If non-empty, it rehydrates you;
   trust it over guesswork.
2. `CONVENTIONS.md` — the binding graph rules.
3. `INDEX.md` — the ID router. `DAG.md` — the execution frontier.
4. Then grep every ID mentioned in your task before writing anything, and
   read the hits plus their `ctx:` targets.

## Standing ground rules

<!-- Seed from your own policy calls; each rule = trigger + one-line why.
     Examples to adapt or delete: -->
- **Tests narrate themselves:** every assert carries a message with the
  actual value — a green test whose output shows nothing proves nothing.
- **Settings live in config, never code defaults:** tunables are required
  config params, so every deployment states its choices explicitly.
- **Verify on write:** scripted edits assert old-string-present before and
  new-token-present after, then re-read (silent no-ops have eaten graph
  nodes). Pin every git command to its repo; name files in every commit.
- **Spend policy:** {{SPEND_POLICY}}.
- **Neighboring repos are read-only** (if any coordinate with this one, all
  cross-talk goes through the designated append-only channel file).

## While working

- Mint the task node (with `blocked-by:` + `evidence:`) BEFORE building.
- Update SESSION_HANDOFF.md at checkpoints, not session end — sessions die
  without warning. Graduate durable findings before overwriting scratch.
- Uncertain? PARK with a reminder. Silence is a decision.
- Only the main session edits the graph docs during parallel work.

## Session end checklist

- [ ] Every new decision is a DEC entry; every parked item has a reminder.
- [ ] INDEX.md verified — every ID present, every status true.
- [ ] DAG.md statuses match reality; DONE tasks have their evidence satisfied.
- [ ] Tests green; the demo/build still runs.
- [ ] SESSION_HANDOFF.md updated (and under its size budget) so the next
      session can rehydrate.
