# TODO — open workstreams (help welcome)

<!-- Dogfood note: when someone actually picks one of these up, it stops
     being a TODO line and becomes a real node with blocked-by/evidence
     edges — exactly as graph-kit/SPEC.md prescribes. Until then, plain
     checklist lines are the honest tier for this repo's size. -->

- [ ] **Benchmark the kit itself (A/B harness).** Wire this system into a
  simple agentic-coding bench project as an *addendum harness*: run
  standard coding benchmarks with and without the kit installed and see
  whether scores move. The honest hypothesis cuts both ways — the ritual
  may pay off only past a certain task length/session count, and a
  single-shot benchmark may show nothing (which would itself be a finding
  worth publishing here). Preregister the protocol before running it —
  upskilling doc 11 applies to us too.

- [ ] **Find (or build) the benchmark that measures what we actually
  refine.** Standard benches measure single-session task completion; this
  kit's claims live elsewhere — continuity across session death,
  cost-per-completed-task over days, decision archaeology ("can a fresh
  agent answer WHY in one grep?"), drift caught per validator-hour. Strive
  toward an eval that measures *those*, refining it as the kit itself
  evolves. Candidate shapes: multi-session resumption tasks with induced
  /clears, a "rehydration fidelity" probe, same-repo-different-agent
  handoff scoring.

- [ ] **Field-deployment intake, standing.** Each new project that adopts
  the kit and reports back gets its lessons genericized into the
  upskilling/GOTCHAS docs the way deployments two and three already did.
