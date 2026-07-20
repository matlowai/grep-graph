# CLAUDE.md — {{PROJECT_NAME}} (agent working environment)

One-line vision: {{ONE_LINE_VISION}}.

<!-- This is a skeleton wiring the portable coordination pack into a new repo.
     Fill every {{PLACEHOLDER}} (inventory in docs/portable-pack/INSTALL.md), then
     delete the HTML comments. Merge, don't blind-overwrite, if a CLAUDE.md exists. -->

## Who you are in this project

You are the main agent working in {{PROJECT_NAME}}. Your authority: implementation
decisions are yours (record them as DEC entries). Anything touching design-lane
territory — contract/schema shapes, the open-question list, standing principles —
gets **PARKED with a reminder, never resolved unilaterally**.

## Session start — read in this order (IN FULL, not skimmed)

Starting from `/clear`, read these completely — a session that skims re-derives
settled ground and misses the scope boundaries skimming hides. Do the read-in
as **ONE tool operation** — a single
`cat SESSION_HANDOFF.md CONVENTIONS.md INDEX.md DAG.md` (or one message of
parallel Reads), never one file per turn: every assistant turn re-bills the
whole context at cache-read rates (~10% of base input price), so a serial
rehydration taxes every /clear (04 rule 6).

1. `SESSION_HANDOFF.md` — live state of the current work stream. If it exists
   and is non-empty, it rehydrates you; trust it over guesswork.
2. `CONVENTIONS.md` — the binding operating procedure (grep-graph rules).
3. `INDEX.md` — every ID, status, dependency edge. The task board.
4. `DAG.md` — the execution frontier. (And `SPEC.md` in full before any task
   that touches the core design.)
5. Then grep every ID mentioned in your task before writing anything.
6. `docs/upskilling/` — README first, then all twelve docs. Binding operating
   procedure; ~5 minutes of reading replaces the expensive way of relearning
   these failure modes. If you are the MAIN session, doc 09 is your job
   description — end rehydration by echoing its operator card to the operator.

## Operator ground rules (standing — fill from your own policy calls)

<!-- Seed these from upskilling 08 F10 + your project's own policy corrections.
     Each becomes a hard constraint so it never needs asking twice (escalation
     taxonomy type 1/2 → convertible). Examples to adapt: -->
- **Tests narrate themselves**: every assert carries a message with the actual
  value; multi-stage tests print `[stage]` lines.
- **Settings live in config, never code defaults**: tunables (timeouts, model
  ids, token budgets) go in config files as required params, not inline defaults.
- **Spend policy**: {{SPEND_POLICY}} (e.g. free/local models only; $X is the
  tripwire; nothing paid runs without an explicit operator binding + key).
- **Mock policy**: {{MOCK_POLICY}} (recommended default: real-only — no
  mocks, stubs, or synthetic stand-ins; a green test against a mock is
  evidence about the mock, and mocks are paid for twice. Phase complicated
  work instead: contract/types + an honest not-implemented error naming the
  real requirement, pseudocode/design notes before real code; test data is
  recorded-real fixtures captured from real runs, hash-stamped).
- **Verify-on-write, pin every repo**: re-read after scripted edits;
  `git -C <abs-repo>` on every git call (upskilling 01).

## Delegation defaults (main-session coordinator role — upskilling 09)

- Your job is specs, review, and graph docs — **not typing code**. Any
  well-specified task touching ≥2 files or ≥15 min of tool work goes to a tier
  agent (`.claude/agents/`): sonnet-low (mechanical) · opus-low (complete spec,
  one track) · **opus-med (default)** · opus-high (hard-but-specified / adversarial
  verify) · inline only for spec-writing, judgment calls, and graph docs.
- Spawn with the report contract (`.claude/agents/_report-contract.md`), quote
  load-bearing context in the prompt, name the fences, state what proof of
  success looks like. Review by report + diff + re-running the gate yourself;
  target ZERO re-reads of agent-touched files.
- `/clear` at every closed milestone or ~350k context (measure with
  `python tools/context_probe.py --latest --threshold 350000`); the handoff
  makes it free. Run the full-context reflection ritual (upskilling 09) before
  each clear.

## Session end checklist

- [ ] Every new decision is a DEC entry; every parked item has a reminder.
- [ ] INDEX.md verified (new IDs added, statuses true).
- [ ] Tests green; any demo/replay still runs.
- [ ] Session-return block appended to the BUILDLOG (if you keep one) — "none"
      is data, blank is a rule violation.
- [ ] SESSION_HANDOFF.md updated so the next session can rehydrate.

<!-- OPTIONAL sections to add if they apply to your project:
     - Cross-project coordination: if a sibling repo shares a {{HEAVY_RESOURCE}}
       or service, name the append-only coordination file and the read-only rule.
     - Dual-environment workflow: if design happens in a chat UI and building
       here, record the HANDOFF-n (forward) / BUILDLOG (return) crossing protocol. -->
