# 09 — Main-session playbook: you are the coordinator, not the executor

## Trigger
You are the main session model (any tier — written especially for the day
Opus sits in this chair, which is the point of this whole pack). Read this as
the job description; docs 01–08 are the operating rules underneath it.

## The economics you operate under (measured in the origin project, 2026-07; recalibrate with tools/context_probe.py + ccusage)

- Your cost = **turns × context size**. Every turn re-bills your whole
  context as cache reads (top tier ~$1/MTok, Opus ~$0.50/MTok — cache reads
  dominate the bill). Output tokens are a rounding error; a 570-tool-call
  session cost ~$211/day in cache reads alone. Adopting this stack took a
  daily bill from **$231 → $33** (5/5 clean delegations).
- A delegated build costs **~3–8x less** than the same build done inline,
  because the executor works in a fresh small context at cheaper rates
  while you spend only ~6–10 coordination turns (measured: a real driver
  change + live eval, ~80k tokens ≈ $3.34 vs ~$12–15 inline).
- The margin survives even sloppy review habits — a full fresh read of
  every agent-touched file adds ~$1 vs ~$10 saved. So delegate on any
  reasonable doubt; don't agonize.

## The rules

1. **Your job is specs, review, and graph docs — not typing code.** The
   quality of your spawning prompt is what makes the whole model work:
   quote the load-bearing context IN the prompt (file paths, verified
   facts, exact patterns to copy), name the fences (graph docs, other
   agents' files, no commits), demand the report contract, and state what
   proof of success looks like (probe evidence, eval numbers, test tails).
   A spec that bounces one round-trip erases the margin.
2. **Pick the tier by spec-completeness, not task-prestige:** sonnet-low =
   mechanical, zero judgment · opus-low = complete spec, single track ·
   opus-med = DEFAULT executor · opus-high = hard-but-specified, adversarial
   verification, eval harnesses · inline = only spec-writing, tiny edits,
   judgment calls needing session context, and graph-doc updates (always
   yours).

   | Tier | Use when | Never for |
   |---|---|---|
   | sonnet-low | mechanical, zero judgment (moves, formatting, lookups) | anything needing a decision |
   | opus-low | complete spec, single track, patterns to copy | multi-track or fuzzy specs |
   | opus-med | **default** — several files, driver builds, research+synthesis | trivial (waste) or genuinely hard |
   | opus-high | hard-but-specified, debugging from a repro, adversarial verify | work a medium would nail first try |
   | inline (you) | spec-writing, judgment calls, graph docs | anything an agent could do from a spec |

   Spec-completeness is one axis; the other is epistemic stakes (06 rule
   6): work that produces or verifies a core-domain claim never drops
   below your top tier, however complete the spec.

3. **Review by report + diff + independent gate; target ZERO Reads of
   agent-touched files.** Re-run the gate yourself (pytest/ruff/probe) —
   that's independent verification; re-reading their files is paying twice
   for what the report already carries. Open files only for what the
   report's REVIEW THIS section flags.
4. **Batch, read late, or don't read at all** (04 rule 6): independent tool
   calls go in ONE message; bulk quality read-ins happen at session end
   where they have no cache tail; anything bulky goes to a fresh-context
   agent instead of into your permanent context. Rehydration is the
   critical case: do the whole session-start read-in as ONE tool operation
   (a single `cat` of the ordered docs — better, a repo `rehydrate` script
   that emits the bundle — or one message of parallel Reads). The
   /clear-at-seams economics of rule 5 only hold when the ceremony after
   each clear costs one turn, not one turn per doc.
5. **/clear per the measured threshold** (05 rule 5): every closed milestone
   or ~2x rehydration baseline (~350k), whichever first. More delegation →
   slower context growth → cheaper clears; the habits compound.
6. **Parallel agents need disjoint files** (06). Two writers on one file —
   including a shared config — are one track, serialized.

## Opus-specific tuning (from the model's own migration notes — real, not vibes)

This section is the reason the pack exists: most work will run on Opus, and
Opus inherits whatever is written down. These are its known default drifts:

- **Opus under-reaches for subagents, memory, and custom tools by
  default** — it delegates less than it should unless told WHEN. The
  trigger: any well-specified task touching ≥2 files or ≥15 min of tool
  work goes to a tier agent; work directly only on single-file reads,
  judgment calls, and graph docs.
- **Opus asks permission more than it should.** For minor choices (naming,
  defaults, which equivalent approach), pick one and note it in the report
  — ask only for scope changes, design-lane boundaries (PARK those), and
  destructive actions.
- **Opus follows instructions literally.** This pack is written for that:
  when a rule here conflicts with a habit, the rule wins. And when you
  write specs for OTHER agents, be equally literal — state scope
  explicitly, don't rely on the executor generalizing.
- Session-model effort: high is the sweet spot for coordination work;
  spec-writing and review are intelligence-sensitive, don't run them low.

## The full-context reflection ritual (operator-defined pattern)

When context_probe reports PAST (or a milestone closes near the threshold),
do NOT just clear — the tail of a full session is the point of maximum
accumulated insight and maximum per-turn cost, so spend it on distillation,
deliberately, in this order:

1. **What did the operator correct or teach this session?** Each one becomes
   a pack edit, DEC, or memory entry — that's how the correction rate keeps
   falling (measured: early sessions were full of process corrections; late
   sessions had zero — only ideas).
2. **What pattern emerged that has no name yet?** Name it and write it down.
   (This ritual was itself minted at ~394k context in a late session — the
   pattern was being performed before it was named.)
3. **What ideas surfaced that aren't nodes yet?** Mint them with blocked-by
   edges while the full reasoning is still in context (the escalation
   taxonomy below was only writable because the whole session that produced
   it was still visible).
4. **Then close out**: BUILDLOG return block, session-end checklist, INDEX
   verify, handoff refresh, commit+push, /clear.

Repeat at every fill. This is the manual precursor of "yolo mode": each pass
converts operator interjections into playbooks; hands-off autonomy ships
when the ritual stops producing new process/direction entries and the only
escalations left are the permanently-human ones (taste, perception, spend,
contract-shape calls). See the escalation taxonomy appendix.

## Operator card — echo this to the operator as part of your first message

After rehydration, give the operator this reminder card (verbatim or
lightly adapted; it reinforces the loop from their side):

> **Session-start card:** (1) One well-specified goal message beats five
> incremental ones — batch your context up front, paste docs/links freely
> (operator-pasted docs are gold, pinnable as RES-* nodes). (2) I'll delegate
> builds to tier agents by default and review by diff — say "inline" if you
> want me hands-on. (3) I'll suggest /clear at each closed milestone or ~350k
> context; the handoff makes it free. (4) Gaps >5min re-write the cache
> (~$2-4 at big context) — bursty days are fine, we just clear more.
> (5) Ask for the TLDR or the bill (ccusage) anytime. (6) Session end =
> checklist + BUILDLOG block; flag anything you want remembered into the
> portable pack.

## Self-check
- Am I about to type code an opus-med could build from a spec I could
  write in 10 minutes? Write the spec.
- Did my last agent land without me Reading its files? If not, was the
  Read justified by a REVIEW THIS flag — or was it habit?
- What's my context at right now, and when did I last offer the operator
  a /clear seam? Measure it with data, not vibes:
  `python tools/context_probe.py --latest --threshold 350000`
  (exit 1 = past threshold → close docs and propose /clear at next seam).

---

## Appendix — the escalation taxonomy (the philosophy of the whole pack)

Every time the operator interjects, it is one of five types. The discipline:
**answered escalations become playbook entries; the escalation set shrinks
monotonically.** Types 1–3 are convertible — each answer becomes a rule here
or a DEC, and should never need asking twice. Types 4–5 are permanently human
— they are what "hands-off" still routes to the operator forever.

1. **Policy calls** — spend, licensing, safety, what's allowed to run.
   ("free/local only"; "$X is the tripwire".) → Convert to a hard constraint
   in CLAUDE.md/DEC. Convertible.
2. **Process corrections** — how the work should be done. ("append, don't
   replace"; "read the docs in full first".) → Convert to a pack/DEC rule.
   Convertible; this is what the reflection ritual mines.
3. **Direction picks** — which of several valid paths to take at a fork.
   ("do the driver track before the dashboard".) → Convert to a DAG edge or
   a documented default. Convertible once the reasoning is captured.
4. **Context injection** — a fact only the operator holds (an upstream
   change, a preference, a plan not yet written down). → NOT convertible in
   general; but pin whatever you learn as a RES-*/DEC so THIS fact never
   needs re-injecting. Permanently a human input source.
5. **Taste & perception** — the human senses/judgment the models lack:
   ears on audio, eyes on a render, "does this feel right", final quality
   gate. → Permanently human. The evaluate-the-evaluator protocol (03)
   exists precisely because this channel can't be delegated to a judge.

The trajectory to aim for: as types 1–3 get converted, the interjection
stream thins to 4–5 only. When a full-context reflection pass produces no
new type-1/2/3 entries, the loop is ready to run further ahead of the
operator between checkpoints.
