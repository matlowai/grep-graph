# CODE_POINTERS.md — how code points back into the graph

The docs graph earns most of its keep the day a test fails or a config
breaks and the error message NAMES the decision that governs it. This file
is the discipline for getting there. It was distilled from a mature specimen
repo with ~1,700 ID references across its code and config; the patterns
below are the ones that carried weight, ranked by value.

## The principle

An ID in code is a **back-edge**: `grep -rn "DEC-0007" .` should surface not
just the decision but every line of code that decision constrains. Put IDs
where a future reader would otherwise *re-litigate a settled argument* or
*"fix" something that isn't broken*. Everywhere else, they're noise.

## Pattern 1 — the ID in the assert message (highest value)

Put the governing ID in the test's failure message, so a red test names the
authority being violated:

```python
assert cfg.device == "cpu", (
    f"GPU is reserved for the inference server (DEC-0015); got device={cfg.device!r}"
)
```

Even stronger: make the decision the *observable contract* — assert that the
runtime error/log string itself carries the ID, so production failures
surface the governing node too:

```python
assert "DEC-0017" in plan.dropped[0], (
    f"drop reasons must cite their decision; got {plan.dropped[0]!r}"
)
```

*Why this ranks first:* the graph pays off at the point of breakage. The
person staring at a failure is exactly the person who needs the context, at
exactly the moment they need it, with zero searching.

## Pattern 2 — the ID in required-config error strings

If your rules say tunables live in config with no code defaults, the error
for a missing key should say which decision made it required:

```python
raise ConfigError(f"{path}: required key 'clips_dir' missing (DEC-0012, no code default)")
```

*Why:* "why won't it just default?" is the first thing a new maintainer asks;
the error answers it before the question forms. Config file comments carry
the same duty — a surprising value gets its ID and date:

```yaml
enabled: true   # flipped for demo day (T-B71, operator direction 2026-07-05)
```

## Pattern 3 — the guard comment at a load-bearing line

A comment citing an ID belongs on any line that *looks wrong but isn't* —
non-obvious ordering, deliberate redundancy, a constraint that would be
"cleaned up" by a well-meaning refactor:

```python
# T-B39 FIELD ORDER (not shape): language is declared BEFORE text so that
# streaming consumers can pick a synthesizer before the text arrives.
```

The test for whether the comment earns its place: **would a reader without
it break something or re-argue something?** If yes, cite the ID. If the code
is self-evident, don't.

## Pattern 4 — the module docstring opener

Every module's docstring opens with the task and/or decision that authorized
it:

```python
"""Avatar transport protocol v1 (DEC-0039, T-B110)."""
```

One line, at most two IDs. This is cheap provenance: `grep -rln "T-B110"`
returns the full footprint of a task, including its code.

## Pattern 5 — scope-fence comments

Where an agent's authority ends mid-file, say so with the ID of the open
question that owns the other side:

```python
# SCOPE FENCE (T-B90): engine-owned stage environment only; creator-mode
# authoring surface is undecided design territory (Q-K5) — do not extend here.
```

*Why:* this is the only pattern that prevents work rather than explaining it,
and it's most valuable in multi-agent repos.

## Commit-message discipline

- **Lead with the ID:** `T-B113: dashboard clip transcriptions + live stream`
  or `DEC-0042 / T-B113: ...` for a decision-plus-build. In the specimen
  repo, 37 of 40 recent commits followed this; `git log --oneline | grep
  T-B113` reconstructs a task's whole history.
- **Mint nodes in their own commit** (`T-B114 minted: worker keep-hot
  controls`), separate from the build commit — the node's birth and its
  completion are then both greppable, and a reverted build doesn't erase the
  plan.
- Non-task commits use a small set of stable prefixes (`Docs:`, `Hooks:`,
  `Session close:`) so the log stays scannable.

## Anti-patterns (IDs as noise)

- **Ancestry chains.** `# T-B93, DEC-0008/DEC-0012; the T-B87 pattern applied
  to rig files` — one ID carries the weight; the rest are lineage the graph
  already links. Cite the node that GOVERNS this line, not its family tree.
- **Inventory decoration.** Tagging every row of a list/table with the task
  that added it. Provenance without a constraint is clutter; the module
  docstring already covers it.
- **Reflexive tagging of self-evident code.** An ID on a line nobody would
  ever question is a maintenance cost with no reader.
- **IDs instead of explanations.** `# DEC-0031` alone forces a doc round-trip
  for every reader. The comment states the constraint in words AND cites the
  ID: the words serve the reader in a hurry, the ID serves the one who needs
  the full argument.

## Calibration

Don't aim for a reference density. Aim for: every *surprising* constraint
cites its authority; every test that enforces a decision names it in the
failure message; every module knows its origin in one line; everything else
stays clean. In a small project that may be a dozen IDs in code, total —
that's fine. The measure of success is not coverage, it's whether the next
confused reader's grep lands them on the answer.
