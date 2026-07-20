# 12 — Field lessons, third deployment (verification under fire)

Contributed from a third deployment of the pack — a model-training lab (4 sessions, ~60 commits of
findings, one session death, five same-day bug catches). Everything below is
written GENERIC — no project nouns — so it can be lifted verbatim into the
standalone pack. Suggested homes in the pack are tagged `→ doc`.

## A. Epistemics upgrades

### A1. The two-instruments rule  → 01-verification, 03-evaluate-evaluators
Every load-bearing conclusion needs two INDEPENDENT views of the same quantity
before you act on it: metric + human eyeball, log + database, build-time
telemetry + deployed-artifact behavior, agent report + independently re-run
gate. In one audited day, five real defects were caught — every single one as a
DISAGREEMENT between two views of one number, and zero by either view alone.
Corollary: when two views disagree, neither is "probably right" — the
disagreement IS the finding; chase it to the code before explaining it away.

### A2. Flag names lie; audit the config surface once per dependency  → 02-probe-first
Before designing anything around a dependency's behavior (a trainer knob, a
scheduler option, a library flag), read the CONSUMING code — not the flag name,
not the docs, not your memory of it. Failure modes found in practice, all in
one tool: a knob that is parsed but never read (phantom); a knob read from the
WRONG key (can never be set); a flag whose name suggests the opposite of its
mechanism; a capability that exists but no name hints at. The fix is a
one-time, delegated **config-surface audit** per major dependency: every knob,
default, and consumer, with a SURPRISES section. It costs one agent-run and
retires a whole class of invalidated experiments. A pre-registered experiment
built on a phantom knob measures nothing — and looks exactly like a real
result until audited.

### A3. Seed everything; one unseeded success is one sample  → 01-verification
Any nondeterministic process whose outcomes you compare across runs gets an
explicit seed from day one. Measured case: two identical configs, opposite
outcomes, pure RNG — the "effect" under study was actually a coin-flip race
decided in the first few percent of the run. Replicate a headline result
seeded before building anything on it; retrofit seeds into ALL templates the
day you learn this, not per-experiment.

### A4. Build-time transforms must survive into the artifact  → 01-verification
Any custom transform applied during a build (scaling, normalization, wrapping)
must be explicitly baked into the shipped artifact, and verified by a
ROUND-TRIP test: consume the artifact with the bone-stock standard consumer
and compare against the builder's own output. Builder-side telemetry is not
deployment truth — the gap between them shipped a 8x-wrong artifact that
looked perfect from inside.

## B. Process/infra upgrades

### B1. Sessions are mortal; design for the crash  → 05-docs-discipline, 09-playbook
A session died mid-marathon (upstream infra flag, no warning). What survived:
persistent queues, committed docs, artifacts on disk, detached daemons. What
died: session-local cron/backstops, in-conversation knowledge (including a
design table that had to be reconstructed from operator memory), the close
ceremony itself (no handoff was ever written). Rules that follow:
- **Commit per finding, not per session.** The close ceremony maintains the
  INDEX/status graph; findings land in git the hour they're verified. A
  session that dies after 20 finding-commits loses ceremony; one that batches
  everything for close loses the day.
- Anything that MUST happen (watchdogs, backstops) lives OS-level or in a
  persistent service — never only inside the session's scheduler.
- Anything decision-bearing said in chat gets written to the repo same day;
  conversations are the least durable storage you have.

### B2. Supervisor "done" = output contract, not process state  → 04-environment
A job supervisor must verify the job's OUTPUT (final artifact matches the
configured spec — step count, file set, size) before marking done. Process/DB
liveness states cannot distinguish "completed", "killed by the OOM reaper",
and "not started yet" — measured case: a crashed job was marked done and its
dependents launched against artifacts that didn't exist.

### B3. Name-keyed caches survive artifact replacement  → 04-environment
Replacing an artifact behind a stable name (symlink re-point, file overwrite)
does NOT invalidate long-lived serving processes that cached under that name.
After any such replacement: use a fresh name, or restart/flush the server, and
verify with a probe render/request whose output MUST differ. Pixel-level
forensics to untangle which requests hit which artifact cost ~90 minutes; the
fresh-name habit costs nothing.

### B4. Shared boxes have hostile neighbors  → 04-environment
On a machine shared by multiple agent sessions/projects: your long job WILL
eventually be killed by someone else's memory spike (OOM reapers kill the
biggest process — that's your trainer). Check resource ownership before big
loads; make every long job resumable (true resume verified, not assumed); make
the supervision layer treat sudden process death as EXPECTED input (see B2).

## C. Experiment-culture upgrades (for projects that run experiments)

### C1. Pre-register predictions with explicit gates  → 11-preregistration-and-claims (complement: put the gates INSIDE the launch config)
Write the predicted outcome AND its numeric gates INTO the config/preset that
launches the run, plus "if gate X fails, the lever is Y". Measured payoff: a
failed gate came with its own pre-written interpretation and next step —
the failure was as actionable as a success. Corollary: **launch gates** —
executable checks listed at the point of use (in the preset/config
description), including "read telemetry line Z at startup; abort+adjust if
outside band" for cheap early-abort tuning.

### C2. Fail fast, keep everything  → new material
Stop a run the moment its control points answer the question; a stopped run
with an UNDERSTOOD failure beats a completed run with confounds. Keep all
artifacts (they become the control points for v2). The measured pattern that
makes this cheap: mechanism-level telemetry inside the run (per-step
diagnostics) so "why it failed" is readable without re-running.

### C3. Build the instrument before the experiment  → new material
When a qualitative observation matters (an operator eyeball catch), build the
measuring tool BEFORE the next run and calibrate it on EXISTING artifacts so
its scale is anchored on day one. The gate for the next run then references
measured anchors, not hopes.

### C4. The operator's eyeball is an instrument — log it as data  → 03-evaluate-evaluators
Human qualitative observations ("skin texture degrades on elderly faces")
repeatedly detected axes ALL metrics were blind to. Record them in the
findings ledger with the same rigor as numbers (quoted, dated, attributed),
then build the metric that can see what the human saw (C3).

## D. Delegation-layer upgrades  → 06-delegation, 09-playbook

### D1. Idle ≠ done; the report file is ground truth
Long-running agents emit idle signals at internal turn boundaries. The ONLY
completion signal is the report file on disk (contract-mandated path). Nudge
protocol for idle-without-report: "(1) done? write report now. (2) blocked?
say exactly what. (3) mid-task? continue." — one message, resumes cleanly.

### D2. Resource green-light protocol between concurrent agents
When agents share a scarce resource (GPU, port, service), the coordinator owns
a hold/green-light protocol: agents declare intent, HOLD on the resource until
explicitly green-lit, and the green-light message includes current resource
state ("service already booted at X; your jobs will queue behind mine").
Measured: an agent held cleanly through two service restarts that would have
crashed its work mid-flight, then completed in one sprint when green-lit.

### D3. Tell agents what their siblings own
Every spawn prompt names the files/dirs OTHER active agents own as explicit
fences. Cost: one sentence. Prevents: the two-writers-one-file class entirely,
including the subtle case where a finished agent's uncommitted edits sit in
the tree a new agent is about to modify (commit the finished agent's work
BEFORE spawning the next one into the same area).

### D4. Agents inherit the day's epistemics
Spawn prompts for verification-sensitive work include the standing rules:
"verify the knob exists before designing around it (A2)", "report claims with
code cites", "flag every deviation from spec prominently". An agent given the
A2 rule found a phantom knob in its first hour and corrected the spec it was
handed — the rules compound when the executors carry them too.
