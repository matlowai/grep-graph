# GOTCHAS.md — the failure catalog

Every rule below was paid for. The incidents are anonymized from real
multi-month agent-run projects; each one produced **success-shaped output
while failing** or silently destroyed graph state. That's the pattern to
internalize: exit code 0 and no error text are not verification.

Format: **rule** — trigger — the incident that bought it.

## A. Writing to the graph

**A1. Mint the node before building.**
*Trigger:* you're about to type code for work that has no task ID.
Stop and mint the node with its `blocked-by:` edges first. A productive
streak is exactly when this binds hardest — updating docs feels like
interrupting momentum, so doc-debt accumulates fastest when work is going
well. *Incident:* six sessions of work ran in one long chat; tasks built on
unminted nodes left the DAG hiding the true frontier, and a later session
picked "next" work that was already done.

**A2. Append, don't replace, in living documents.**
*Trigger:* updating a handoff, ledger, or log.
Additions to append-only files use append operations (`cat >>`, or an
editor insert at end); anything that REPLACES text in a living doc gets the
full A3 verification treatment. *Incident:* a scripted "update" of a handoff
file rewrote a whole section and silently dropped a block another session
needed; the operator's standing correction became a rule: "we are appending
there."

**A3. Verify on write — every scripted edit, both directions.**
*Trigger:* any file edit done via script, heredoc, or string replacement.
Assert the old string IS present before replacing (string replace no-ops
silently on a no-match), assert the new token is present after writing, then
re-read in a separate step. If the edit mints a graph ID and you commit,
grep the committed blob (`git show HEAD:<file> | grep -c "<ID>"`).
*Incident:* two freshly-minted task nodes were clobbered by a later scripted
rewrite working from stale text; the commit message claimed the change; the
committed file contained zero occurrences of the IDs. Found weeks of
confusion later, only because a human happened to ask about one of them.

**A4. Tombstone, never delete.**
*Trigger:* you're about to remove a resolved question or an outdated decision.
Status flips, `resolved-by:`/`supersedes:` edges get added, text stays. If
you're deleting graph text, you're almost certainly wrong. *Why:* the next
grep for that ID must find the answer in one hop, or the project re-argues
it from scratch.

**A5. Graduate before you overwrite scratch.**
*Trigger:* trimming or overwriting the session-handoff file.
Anything whose loss would cost ten minutes of re-derivation must land in a
durable home (DEC, node reminder, lessons file) BEFORE the scratch version
is overwritten. *Incident:* a checkpoint's hard-won findings lived only in
the rehydration file, got trimmed in a cleanup, and had to be re-derived.

**A6. A stale INDEX is a broken build.**
*Trigger:* session end.
Verify the ledger against reality: every ID present, every status true. The
INDEX is the entry point every fresh session trusts blindly; if it lies, it
poisons everything downstream. Related: keep each node's status in exactly
ONE file — mirrored statuses in two files WILL drift.

**A7. Silence is a decision — and it's the only kind you can't grep for.**
*Trigger:* you're uncertain and tempted to just move on.
PARK the item with a reminder capsule and a re-entry condition, or log a
provisional assumption (SPEC §8). Dropping it silently means the project
decided something and recorded nothing.

**A8. Two probes, then park.**
*Trigger:* a blocked experiment or a path that keeps failing.
Two real attempts, then it becomes a parked node with a `reminder:` and a
re-entry condition ("when the upstream bug is fixed", "when the bigger
machine arrives") and you move to the next frontier task. *Incident:*
repeated grinding against environment-blocked experiments burned sessions
that parked nodes would have saved.

**A9. Lint the front door: every name it drops must resolve.**
*Trigger:* you wrote or edited the instructions file (CLAUDE.md, AGENTS.md,
CONVENTIONS.md) — or you're a fresh session reading one.
Every file path, command, and convention the front door names gets checked
against reality before the session ends: the file exists, the command runs,
the convention matches what the graph actually does. Fresh sessions follow
the front door literally, so an instruction that lies is worse than none.
Derived numbers (task counts, statuses) are stale the moment the graph
moves: quote the command that computes them, or reconcile them in the same
edit that changes the graph. *Incident:* a front door told sessions to log
assumptions in a file that did not exist, and demanded an `evidence:` field
its own DAG had never used — both written in good faith the session the
front door was minted, and never tested. A fresh-eyes audit found them two
sessions later, along with task counts stale in two documents.

**A10. A re-asked decision is a stress test, not a re-recital.**
*Trigger:* the operator re-opens a settled DEC ("should we have done X
instead?").
Don't quote the ledger back. Re-test the decision against the new frame,
and APPEND whatever the test produces — a sharper rationale, a newly
considered alternative, or a supersession. *Incident:* a settled
adopt-platform-vs-build decision was re-asked under a new frame ("which of
our topics could that platform actually host?"); counting them produced a
stronger, quantified rationale than the original entry carried. The
decision stood, and the appended rationale makes the next re-ask free.

## B. The shell and the repo (agent mechanics)

**B1. The shell working directory RESETS between commands.**
Not "drifts" — resets. Use absolute paths everywhere, including inside
scripts and heredocs, and pin every git command (`git -C /abs/path/repo`).
*Incident:* a relative-path edit ran in the wrong directory, edited nothing,
and exited 0.

**B2. Never `git add -A`. Name the files, every commit.**
*Incidents (two):* a bulk add with the wrong working directory committed a
NEIGHBORING repo's dirty tree under this project's commit message; later, a
bulk add swept a background agent's half-written files into an unrelated
commit. Name the files; after any cross-repo work, check `git -C <each>
log --oneline -1 && git -C <each> status --short` before moving on.

**B3. Read a failed command's output before reacting.**
*Trigger:* a compound command (`A && B && C | tail`) reports failure.
Nonzero exit often means "last pipe stage failed", not "work lost" — one
"failed" call contained fifteen passing tests and complete valid output.
Better: separate mutation, verification, and commit into distinct calls so
each result is unambiguous.

**B4. Read before you edit — and a moved file counts as a new file.**
*Trigger:* editing any file you haven't read this session.
Most agent harnesses enforce this; treat it as a rule, not an error to
discover. If another agent or script has touched a file since you read it,
your in-context copy is stale — re-read before the next edit.

**B5. Every background job gets a timeout.**
*Incident:* an unbounded test run hung silently in the background for 25
minutes. Cap everything (`timeout -k 5 <cap>`); on a hang, kill → rerun
verbose → bisect → extract a standalone repro.

**B6. Serial tool calls re-bill your whole context; batch them — or build a
tool.**
*Trigger:* you're about to run several independent reads/greps/commands one
message at a time, or you notice the same multi-call sequence recurring
across sessions.
Every assistant turn re-bills the entire context prefix at cache-read
rates — cheap per token, dominant in aggregate because every turn pays it
on everything before it. K serial tool calls = K re-bills of a growing
prefix; the same K calls batched in ONE message (parallel calls, or one
`cat a b c` / compound command) = one re-bill. And when a sequence recurs
session after session, stop batching it by hand: graduate it into a small
committed script the repo owns, so it becomes ONE tool call forever — the
session-start rehydrate script is the canonical example, and doing this
also makes the ritual executable (a renamed file fails loudly instead of
being silently skipped). *Incident:* a measured audit found mid-session
batching waste was only ~4% of spend — but the rehydration ceremony, run
one-file-per-turn after every context clear, taxed the exact economics
that make clearing free; one script closed it.

## C. Trusting the wrong evidence

**C1. Training-data "facts" about models, packages, and APIs are hypotheses.**
*Incident:* six wrong-from-memory facts in two days — hallucinated model
IDs, wrong package variants, version pins missing required kernels. Probe
the live thing (curl the model list, `inspect.signature()` the installed
API, run a 5-second smoke call) and write the verification date next to the
value: `verified live 2026-07-14`.

**C2. Answer "is X true about our system?" with a live check, not memory.**
*Incident:* asked whether a policy was violated anywhere, the winning answer
quoted freshly-observed config values; the from-memory answer would have
been confidently wrong.

**C3. Don't verify by memory across steps.**
"I wrote that earlier" is not evidence. If a later step depends on an
earlier edit, re-check the file at the point of dependence. *Incident:* a
cleanup script held content in a variable, edited the file, then a stray
final write pushed the PRE-edit content back — the fix existed for seconds.

**C4. Tests narrate themselves.**
Every assert carries a message with the actual value; multi-stage tests
print stage lines. A green test whose output shows nothing proves nothing
to the next reader — and the next reader is usually an agent deciding
whether to trust the whole suite.

**C5. A green test against a mock is evidence about the mock.**
*Trigger:* you're about to write a mock, stub, or synthetic stand-in for
something real that exists or will exist.
Mocks are paid for twice — once to build, once to replace — and they can
leave a suite that passes while reality fails. Prefer recorded-real
fixtures (small captures from real runs, hash-stamped with provenance) for
determinism, and an honest not-implemented error naming the real
requirement for backends that don't exist yet. Phase the THINKING
(pseudocode notes, contract types first), never the data. *Origin:* an
operator imperative issued as a project's mock-first era ended — the mocks'
lasting products were replacement work and false green.

## D. Sessions and continuity

**D1. Update the handoff at checkpoints, not session end.**
*Incident:* a machine froze mid-session under resource contention and the
session died with it; everything since the last handoff update was gone.
Sessions end without warning. A checkpoint is any point where you'd hate to
re-derive what you just learned.

**D2. A fresh session with a good handoff beats a long session with stale
context.** Prefer clearing at natural seams (a closed milestone) over
pushing a bloated context onward. The rehydration file works — trust it,
and keep it worthy of trust.

**D3. Budget the rehydration file.**
*Incident:* a solo agent's session capsule grew to 71 KB — its "verified
state" section alone was 500 lines — because no second reader ever forced
graduation. Cap it (~150 lines), archive overflow to dated files.

**D4. "No notification" is not "no result" — check the disk first.**
*Incident:* a background job was declared dead (no process, no report,
silent for an hour); it had SUCCEEDED — the completion notification simply
never fired. Before declaring anything dead, inventory expected artifacts
and their timestamps. Corollary for unattended runs: arm a timer-based
wake; don't rely on completion notifications alone — an overnight run once
"took a nap" for hours because the only wake mechanism was the exact thing
that failed.

**D5. When a human correction or tool rejection lands mid-flight, stop and
read it as a redirect** — don't rephrase and retry. *Incident:* every
policy correction in one project's history landed AFTER the wrong
assumption was already baked into code; the cheap moment to catch each one
was the first pushback.

## E. Multi-agent additions

**E1. One writer for the graph docs.** During parallel work, only the main
session edits INDEX/DAG/DECISIONS/handoff. Background agents report;
the coordinator writes. *Why:* concurrent editors of a plain-text graph
produce exactly the silent clobbering A3 describes.

**E2. Fan out only frontier tasks touching disjoint files**, and verify
every agent's output in the main thread before committing it. Tracks that
share a file are one track.

**E3. Neighboring repos are read-only.** If two projects coordinate, all
cross-talk goes through one designated append-only channel file with
signed, dated entries. *Incident:* an uninvited grep-and-edit in a sibling
repo was one of the corrections in D5.

## F. Machine enforcement and evidence (second deployment additions)

**F1. Conventions decay; validators don't.**
*Trigger:* you just hand-fixed a stale ID, status, or cross-reference in
the graph. The fix isn't the edit — it's the executable check that would
have caught it: IDs resolve, edges point at real nodes, registries
cross-reference real files, ledger sources exist. Bundle every check into
one gate command and run it at every checkpoint, not session end.
*Incident:* a multi-day autonomous run kept a ~130-node graph coherent
across dozens of closures only because a six-part validator gate ran green
at every checkpoint; each of its checks had caught real drift earlier —
including the sharpest catch of the run: the project's own language linter
flagging the MAIN session for quoting a banned phrase inside a sentence
that praised a subagent for avoiding it.

**F2. Encode graph invariants as failing tests.**
*Trigger:* a rule like "the frontier must never be empty" or "every DONE
carries proof" lives only in prose. The strongest form of a graph rule is
a unit test that breaks the build. *Incident:* a frontier-never-empty test
forced successor nomination at every frontier-task closure for days of
autonomous operation — the graph could never silently claim there was
nothing to do.

**F3. Preregister expensive runs; append results, never edit them.**
*Trigger:* anything empirical, costly, or irreversible — benchmarks,
migrations, experiments, eval sweeps. Freeze hypothesis + falsification
condition + analysis choices in a file BEFORE running; results and errata
append below a deviations line, never above it. If mid-run the protocol
proves ambiguous, freeze the interpretation in writing before the
ambiguous step executes. *Incident:* eleven preregistered runs completed
with zero deviations, and the discipline caught its own overclaim — a
calibration run's frozen falsification clause fired against an earlier
headline result, forcing a formal downgrade, an appended erratum, and
corrections to every ledger entry citing it, all machine-checkable.

**F4. Accept agent work by recomputation, and record the acceptance.**
*Trigger:* a subagent reports success with numbers. Deliverables land with
a visible "acceptance pending" status; the coordinator re-runs the gate,
recomputes headline numbers from the agent's raw artifacts (not its
prose), then flips a dated ACCEPTED stamp — so reviewed and unreviewed
work are grep-distinguishable forever. *Incident:* an agent's reported
test count was stale against a baseline that had changed beneath it; the
receiver's re-run caught it, the report never would have.
