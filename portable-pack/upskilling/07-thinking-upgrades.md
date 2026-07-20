# 07 — Thinking upgrades: how to have the ideas you'd otherwise miss

The other docs prevent failures. This one is different: it's the heuristics
that generated the marathon's best ideas — the moves a very strong session
makes by default that you can make deliberately. Run these as explicit
steps; don't wait to "feel" them.

## 1. The 10-minute experiment beats the 2-hour analysis
When two approaches are debatable, ask: "what's the cheapest experiment
that would settle this?" — then run it instead of reasoning further.
Example: instead of debating whether an accent came from the model or the
reference audio, the session cloned a different reference clip and re-ran the
bake-off. Ten minutes; question closed. Reasoning would never have closed it.

## 2. Chain tools across domains (the output-becomes-input move)
Ask of every capability: "what if its OUTPUT became another capability's
INPUT?" Example idea: one engine produced the perfect flat deadpan read →
feed THAT clip as another engine's reference audio → voice identity from one
engine, delivery character from another. Nothing new was built; two existing
things were composed in an unusual direction. Deliberately scan for these
compositions — they don't announce themselves.

## 3. Triangulate with orthogonal signals
One measure of a fuzzy quality is an opinion; three INDEPENDENT measures
are an instrument. Example: output quality = an LLM judge (words/artifacts)
+ an objective acoustic metric (prosody) + re-transcription WER (clarity).
Each is blind to the others' failure modes. When you need to measure
something fuzzy, ask: what are three cheap signals that fail DIFFERENTLY?

## 4. Disagreement is information, not friction
When two sources disagree (judge vs. metric, docs vs. probe, your
expectation vs. output), the disagreement itself is the most valuable data
in view. Never average it away, pick the convenient side, or move on.
Every major discovery of the marathon started as a disagreement someone
chased: operator perception vs. judge scores → the whole
evaluate-the-evaluator protocol.

## 5. The transcript is data (and so is everything else lying around)
Your own session logs, event logs, eval reports, and git history are
datasets nobody is mining. Ask: "what question could this byproduct
answer?" Examples: session JSONLs → the failure-pattern retrospective that
became this pack's doc 08; yesterday's real inputs + a deterministic replay
→ nightly drift detection. Byproducts become instruments when you point a
question at them.

## 6. Existing surfaces, new directions
Before building a new mechanism, ask: "does an existing surface already
reach this, pointed differently?" Example: a system already exposed a
control surface for external clients — handing the system its OWN surface as
tools turned self-awareness into a real tool call. Zero new infrastructure;
one arrow reversed.

## 7. Name what you're deferring, out loud
The weaker failure mode isn't wrong decisions — it's silent ones. When you
narrow scope, skip a check, or pick a default, SAY so in the doc/PR/handoff
("v1 touches NO queue-op semantics"). Silence is a decision, and un-named
deferrals become invisible landmines.

## 8. Ask the sharper question at checkpoints
At every natural pause, run this list:
- What am I assuming that a 30-second probe would test?
- What's the cheapest experiment that would change my plan?
- What byproduct am I generating that could answer a question later?
- What would the operator notice here that I'm not noticing?
- What did I just defer without naming it?

The honest answer to any of these is usually the next best action.
