# 02 — Probe live before designing around docs

## Trigger
You are about to build on ANY claim about an external system's behavior —
an API parameter, a model's capability, a library default, a config flag —
that you know from documentation, a README, a model card, or your training
data rather than from this box, today.

## The rule

Run a 30-second live probe FIRST. The probe is a minimal end-to-end call
that would fail or look wrong if your assumption is wrong: one curl, one
python -c, one tiny generation. Only then design or build. If a probe is
genuinely impossible (service down, no key), mark the assumption as
unverified in your notes and build the cheapest thing that would surface
the error early.

## Why (every integration surprise of the marathon was probe-able)

Each of these was a "reasonable assumption from docs" that a 30-second probe
contradicted — and in each case the probe was run only AFTER time was lost:

- A reasoning model was starved by a max-tokens cap (the cap ate the thinking
  budget; answers truncated to nothing).
- A proxy layer silently stripped an `extra_body` field — the flag was
  accepted and ignored.
- A quantized model loaded differently than its model card implied.
- A TTS engine's speaker names were case-sensitive (lowercase only) —
  uppercase didn't error, it just picked a different voice.
- A small model silently DROPPED its instruction input — no warning, output
  just ignored it.
- An engine's "instructions" field was actually attribute tags (identity
  only); free-prose instructions errored.

Note the shape: the failure mode is almost never a clean error. It's silent
acceptance plus wrong behavior. Docs tell you the happy path; only the live
system tells you what it actually does with YOUR input.

## How to probe well
- Probe the exact parameter you'll depend on, not the feature in general.
- Make the probe's output self-evident (print the thing, play the clip,
  diff the two responses) — a probe you have to interpret is half a probe.
- Keep probe one-liners around; you'll re-run them after upgrades.
- When the operator pastes a doc/recipe/model card: treat it as gold, but
  verify 2–3 load-bearing claims live (or by web), pin as a RES-* node, then
  act.

## Self-check
- What am I currently assuming that I have not seen work on this machine?
- If that assumption is wrong, when would I find out — now, or after
  building on it?
