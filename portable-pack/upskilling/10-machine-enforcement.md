# 10 — Machine enforcement: give the graph an immune system

## Trigger
The graph has more than a handful of nodes, more than one session (or agent)
writes to it, or you just caught yourself fixing a stale ID/status by hand.
Conventions are what you intend; validators are what survives.

## The rules

1. **Every load-bearing convention gets an executable check.** If a rule
   matters — IDs resolve everywhere they're mentioned, `blocked-by:` edges
   point at real nodes, every DONE has proof, registries cross-reference
   real files — write a small validator for it and make it cheap enough to
   run constantly. A convention with no check decays on exactly the day
   you're too busy to notice. Corollary: when you catch a manual fix of
   graph drift, the fix isn't the edit — it's the validator that would have
   caught it.
2. **Encode invariants as tests, not prose.** The strongest version of a
   graph rule is a failing test. Example that paid for itself: "the frontier
   must never be empty" as a unit test — closing the last frontier task
   without nominating a successor breaks the build, so the graph can never
   silently claim there is nothing to do.
3. **One gate command, run at every checkpoint.** Bundle the validators
   (graph, ledgers, registries, linters, corpus hashes, tests) into a single
   command sequence and run it before every commit AND after every accepted
   delegation — not at session end. A gate that runs ten times a day catches
   drift the same hour it happens; incidents then cost minutes, not an
   archaeology session.
4. **If the project has language rules, make them a linter.** Domain
   overclaim patterns (anthropomorphism, causality language for
   correlations, method-conflation — whatever your field's failure mode is)
   go into a lint with concrete banned patterns and suggested replacements,
   run on every touched file. Prose guidelines get skipped under pressure;
   linters don't. Sub-rule learned from an agent's self-audit: **when a
   checker skips your target path by design** (vendored dirs, reference
   corpora), lint an out-of-tree copy so the real rules still run — a
   skipped path is where violations accumulate.
5. **Harden rehydration into one committed script.** The session-start
   read-in ("cat the handoff + conventions + index in one call") decays back
   into serial reads unless it's a script in the repo. Make
   `tools/rehydrate.sh` emit the scratch handoff, the assumptions ledger,
   the index, the open decision gates, and the **computed** live state
   (e.g. the actual frontier, derived from the DAG at run time) in one
   output. Computed state beats recorded state: a script that derives the
   frontier can't disagree with the graph the way a stale handoff line can.
6. **Hash-pin immutable inputs, fail closed.** Anything the project treats
   as read-only ground truth (reference corpora, vendored research, pinned
   clones) gets a manifest with content hashes and a verifier in the gate.
   "Immutable" enforced by intention lasts until the first well-meaning
   edit; enforced by a failing verifier, it lasts.
7. **Big corpora get a router, never a full load.** When a knowledge base
   outgrows the context window (a 100k-token index, a paper collection, a
   vendor API dump), write a small router doc that maps each task type to
   the minimal deep loads with **per-load token prices**, plus a surgical
   extraction recipe (an `awk`/`sed` one-liner that pulls ONE entry). Rule
   of use: default load is the router only; anything deeper must be priced
   by a row in it.
8. **Measured costs live in the tool, not in memory.** Any job that takes
   more than ~10 minutes writes its measured wall-clock, throughput, and
   hardware into its own module docstring after the first real run — future
   budgets then come from measurement at the point of use. Same doctrine
   for context: keep a committed probe (the pack ships one) and measure
   before any decision that hangs on context size; a calibrated feel-based
   estimate in the origin projects once ran 100k tokens under the measured
   value.

## Why (second field deployment, 2026-07)

A research-instrument repo ran this stack through a multi-day autonomous
marathon: ~130-node DAG, six-part validator gate, one-command rehydration.
The validators earned their keep repeatedly — the sharpest instance: the
domain-language linter flagged the MAIN session for quoting a banned
knowledge-attribution phrase *inside a sentence praising a subagent for
having avoided that same phrase*. Nobody is above the linter; that is the
point of having one. The frontier-never-empty test forced successor
nomination at every task closure across dozens of closures. The gate ran
green at every checkpoint for three days of work — and the one time a
"verify by hand" claim drifted from reality (a stale test count), it was a
re-run of the gate, not anyone's memory, that caught it.

## Self-check
- Which of my graph conventions would survive a careless-but-productive
  week? Those are the ones with validators. The rest are wishes.
- Can a fresh session rehydrate with ONE command? If it takes judgment to
  know what to read, that judgment belongs in a script.
- Did I just load a big index whole? Then the router is missing a row —
  add the row, not the tokens.
