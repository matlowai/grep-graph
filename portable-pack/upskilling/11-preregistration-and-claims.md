# 11 — Preregistration and the claims ledger: append-only evidence

## Trigger
You're about to run anything expensive, irreversible, or empirical — a
benchmark, a migration, an experiment, a perf comparison, an eval sweep —
or you're about to write down "what we now believe" after one. Post-hoc
rationalization is cheap and invisible; this doc is the antidote. It works
at agentic speed: the whole protocol below adds minutes per run.

## The rules

1. **Freeze the protocol BEFORE the run.** A short file, written first:
   what's being tested, the exact hypothesis, the FALSIFICATION condition
   (what result would count against you), the analysis choices (metrics,
   windows, thresholds, seeds), and the mechanics that must pass for the
   run to count at all. Then run. A hypothesis chosen after seeing results
   is a caption, not a finding — and with an agent executing, the gap
   between "decided" and "ran" is seconds, so freezing costs nothing and
   the timestamped file is the only proof of which came first.
2. **Results are append-only.** The protocol file ends with a deviations
   line: "none at freeze; append below, never edit above after the run."
   Outcomes, surprises, and errata get appended with dates. If you need to
   change the frozen text, you didn't freeze it.
3. **Freeze interpretations of ambiguous procedure BEFORE the ambiguous
   step executes.** When a frozen protocol turns out to underdetermine a
   choice mid-run (which rule applies at step k?), stop, write down the
   interpretation you're adopting and why, and only then run the step. A
   recorded interpretation is a decision; an unrecorded one is silent
   flexibility that makes the prereg worthless.
4. **Track runs in a validated registry.** One row per experiment: id,
   status (planned → preregistered → complete), protocol path, hypothesis,
   falsification condition, required controls. A validator checks the
   protocol file exists, the metrics named are real, and at least one
   control class is declared. The registry is what makes "we always
   preregister" checkable instead of aspirational.
5. **Keep a claims ledger — what the project currently believes, and
   exactly why.** One entry per claim: statement, status
   (supported/open/rejected), evidence level AND kind, source ids, scope
   ("true where?"), caveats, related graph nodes — machine-validated so
   every cited source and node actually exists. Two disciplines inside it:
   - **Refine by appending dated caveats, never by editing statements.**
     A claim's history of narrowing is part of its evidence.
   - **Inference is labeled inference.** A design rule synthesized across
     sources is minted as open/hypothesis with the synthesis stated in its
     caveats — never dressed in the same clothes as a measured result.
6. **Propagate errata.** When a later result invalidates earlier phrasing,
   append the erratum to the ORIGINAL result file (numbers unaffected /
   interpretation corrected), then grep the claim ledger and fix every
   claim that cites it — including scoping caveats like "clause X of this
   claim rests on source Y alone." A correction that lives only where you
   happened to be standing isn't a correction.
7. **Verification-surfaced design conflicts become numbered FLAGS that
   block the gated step.** When checking work reveals the spec disagrees
   with itself (section A's plan is unimplementable under section B's
   contract), don't resolve it silently and don't barrel through: record
   numbered flags on the relevant node, stop the step they gate, and
   present options-with-a-recommendation when the human appears. Resolved
   flags get their resolution recorded next to them. This is the empirical
   cousin of "PARK instead of guessing" — the run you didn't freeze
   honestly is worse than the run you delayed a day.

## Why (second field deployment, 2026-07)

An eleven-experiment autonomous run used exactly this protocol: every
experiment frozen before running, zero deviations across all eleven — and
the machinery caught its own overclaim. A control-calibration experiment's
frozen falsification clause fired against the project's OWN earlier
headline: a 10-seed calibration showed the original single-seed baseline
had been a favorable draw, and because the prereg mandated an
"affected-conclusions" pass on falsification, an earlier result was
formally downgraded, its erratum appended, and the claim citing it
corrected — all in the same session, by the same agent that had made the
original claim. Separately, a chain-selection rule turned out ambiguous
mid-sweep; the interpretation was frozen in writing before the next batch
ran and recorded in the result. And the flag pattern converted a
spec-contradiction discovered during verification (a preregistered sweep
that the implemented contract couldn't express) into a 20-second human
decision instead of either a silent redesign or a dishonest freeze.

## Self-check
- Could someone reading only my protocol file predict what result would
  have counted as failure? If not, nothing was at stake.
- Am I about to edit text above a deviations line? Stop — append.
- Does this "finding" I'm writing synthesize sources, or measure one?
  Label it accordingly, and put the synthesis in the caveats.
- The result just invalidated an old phrasing — have I grepped for every
  claim and doc that cites it?
