# 03 — Evaluate the evaluator before trusting it

## Trigger
Any time an LLM (or any single automated judge) scores, ranks, or gates
something and a decision hangs on the result — bake-offs, eval harnesses,
regression checks, quality gates.

## The rules

1. **Capability is per-dimension, not per-model.** A judge that is excellent
   at one dimension (word choice, coherence) can be confidently blind on
   another (prosody, timing, tone). Never generalize "it's a good judge"
   across dimensions — validate each dimension it scores.
2. **Unprimed probe first.** Before trusting scores on dimension X, show the
   judge a case where X's ground truth is obvious to you, WITHOUT telling it
   what to look for. If it can't see the obvious, its scores on X are noise
   no matter how fluent its justifications read.
3. **Always pair with one objective co-metric.** Every LLM-judged dimension
   gets one cheap, objective measurement alongside it (audio: acoustic
   f0-variance/RMS; text: length, WER via re-transcription, exact-match
   fields; latency: a timer). The co-metric doesn't need to be great — it
   needs to be INDEPENDENT.
4. **Disagreement is signal, never noise.** When judge and co-metric
   disagree, stop and find out which is wrong before using either. Do not
   average them, and do not pick the one that agrees with your hope.
5. **Blind the judge** to which system produced which sample, and demote any
   dimension that fails validation to "advisory" explicitly in the harness —
   don't quietly keep it in the total score.

## Why (the prosody incident, origin project 2026-07)

A judge model blind-judged a text-to-speech bake-off and scored 9/10
"excellent deadpan delivery" on the objectively MOST-expressive clip —
confidently, with a plausible justification, and it repeated the error even
unprimed. Its word-level judgments were fine; its prosody channel simply
didn't exist, and nothing in its outputs revealed that. The catch chain was:
operator ears noticed → unprimed re-probe confirmed → objective f0/RMS ground
truth settled it. The fix: the harness gained objective acoustic columns and
the delivery-fit dimension was demoted to advisory.

The generalizable danger: a fluent judge FEELS validated by its own
articulate reasoning. Fluency of justification is zero evidence of
perceptual capability.

## Self-check
- For each dimension my judge scores: what's the independent co-metric, and
  have I seen the judge pass an unprimed obvious-case probe on it?
- If the judge is wrong on dimension X, would anything in my pipeline
  notice, or would the wrong score flow straight into the decision?
