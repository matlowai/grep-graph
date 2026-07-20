# 08 — Failure catalog (evidence-backed, mined from session transcripts)

Source: a retrospective agent processed the actual Claude Code JSONL
transcripts of the origin project's marathon (2026-07; ~4% overall tool-error
rate, but the errors cluster into a handful of shapes). Each entry: what
happened → evidence → the rule. Where a rule duplicates docs 01–07, this is
the receipts file; the rule still binds.

## F1 — Edit-without-Read was the #1 Edit failure (6 occurrences)
Edit was attempted on files not yet Read in the session — always the hub
docs (INDEX.md, DECISIONS.md, the memory file, a config file, CLAUDE.md) —
failing with "File has not been read yet", all session long.
**Rule:** any file not Read THIS session gets Read (at least the target
region) before Edit. Treat Edit-without-prior-Read as a banned move, not
something you discover via the error. Note: a rename/move counts as a new
path — re-Read after moving a file.

## F2 — The shell cwd RESETS between every Bash call
Not "drifts" — resets. Python heredocs using relative `Path("DAG.md")`
threw FileNotFoundError whenever they ran in a fresh call; `git add`
hit "pathspec did not match" after a prior call's `cd` evaporated.
**Rule:** every command starts `cd <abs-repo> &&` or uses absolute paths
throughout (including inside heredocs) and `git -C <repo>` for every git
invocation. No exceptions for one-liners.

## F3 — Silent loss #1: `git add -A` in the wrong repo
A scripted DAG edit ran with a sibling repo as cwd; its trailing
`git add -A && commit` committed that repo's dirty tree under the wrong
commit message.
**Rule:** never combine `git add -A` with anything cwd-dependent. Pin the
repo AND name the files (`git -C /abs/repo add DAG.md INDEX.md`). After any
cross-repo work: `git -C <each repo> log --oneline -1 && status --short`
before moving on.

## F4 — Silent loss #2: `str.replace` no-ops silently and ate graph nodes
Freshly-minted DAG nodes were clobbered by a later scripted rewrite working
from stale text. The commit CLAIMED the change;
`git show <sha>:DAG.md | grep -c "<ID>"` returned 0. Found only because the
operator happened to ask a question about the lost node.
**Rule:** scripted doc edits must (1) assert the old string IS present
before replacing, (2) assert the new content after writing, (3) re-read/
grep in a separate call, (4) if the edit mints a graph ID, grep the
COMMITTED blob (`git show HEAD:<file> | grep -c "<ID>"`). And whenever any
agent or second script has touched a file, your in-context copy is stale —
re-read before the next edit.

## F5 — Compound mega-commands make success ambiguous
`A && B && C | tail` chains exited nonzero when only a cosmetic last stage
failed: 15 tests passed but ruff's exit code marked the call an "error";
a "failed" call actually contained the complete valid output.
**Rule:** read a failed command's OUTPUT before reacting — nonzero exit
often means "last pipe stage failed", not "work lost". Better: separate
mutation, verification, and commit into distinct calls so each result is
unambiguous.

## F6 — Polling with `sleep N; tail` is blocked; loose Monitor regexes lie
The harness blocked sleep-chains twice; the first Monitor replacement
matched ruff's output line instead of pytest's and fired early.
**Rule:** background the job and monitor with an until-condition whose
regex matches ONLY the terminal summary line (pytest:
`[0-9]+ (passed|failed|error)`), never a substring that appears mid-stream.

## F7 — Unbounded test runs hang; the debugging ladder that worked
A full test suite hung in the background (~25 min lost; a sampling profiler
dead-ended twice on this box — not installed, then needs sudo). What worked:
kill → rerun with `timeout -k 5 <cap>` and `-v` → bisect to the single test →
extract it into a standalone repro with `[stage]` prints.
**Rule:** every test run and background job gets `timeout -k`. On a hang,
go straight to the ladder above; skip the fancy profiler on an unfamiliar
box — stage-print instrumentation is faster and matches "tests narrate
themselves".

## F8 — Heavy-resource contention killed the whole session, not just the jobs
Multiple generators launched beside a resident model server (most of the
heavy resource already in use). The box froze; the session itself died
mid-run and restarted to orphaned background jobs. The recovery that worked:
inventory artifacts already on disk FIRST, check service/resource state,
regenerate only what's missing.
**Rule:** the resident server owns the heavy resource. Check utilization
before any heavy launch; ONE heavy generator at a time; small jobs go to
CPU. After any crash/restart, audit disk artifacts before regenerating
anything.

## F9 — Training-data "facts" about models/packages were wrong six times
in two days: a hallucinated model id (wrong version number); the wrong model
variant (operator had to correct it); a pinned dependency lacking kernels for
the box's hardware; an engine rejecting an input mode for a subset of models;
a container image missing a codec library; a small model silently dropping an
instruction field.
**Rule:** model IDs, package APIs, quant availability, and hardware support
are hypotheses until probed: curl the live model list,
`inspect.signature()` the installed API, run a 5-second smoke generation.
Write the verification date next to the value ("verified live YYYY-MM-DD").

## F10 — Operator policy corrections all landed AFTER assumptions were
baked into code: a too-small token cap on a thinking model; paid-model names
as code defaults; a session that skimmed the doc-reading order; uninvited
grepping in a sibling repo.
**Rule:** turn each correction into a hard constraint in CLAUDE.md/DEC once,
so it never recurs (examples from the origin project: a floor on thinking-
model token budgets · tunables only in config, never code defaults ·
free/local models only · read the session-start doc list IN FULL from
/clear · other repos read-only except an explicit coordination file). And
when a tool call is rejected mid-flight, that's a redirect — stop and read
it as one, don't rephrase and retry.

## F11 — When the operator disputes an eval result, suspect the EVALUATOR
first. The operator flagged a clip the judge had scored 9/10 "excellent
deadpan" as obviously not deadpan — the rubric was leading; the judge heard
words, not prosody.
**Rule:** first suspects are rubric leakage and judge capability gaps, not
the sample. Recovery template (replicate exactly): admit the leading
rubric → unprimed re-probe ("describe only the prosody you hear") →
objective co-metric (an acoustic f0/rms variance) → demote the invalid
dimension EXPLICITLY in the harness → mint the follow-up node.

## F12 — What made background agents the biggest throughput win
Waves of agents on disjoint DAG-frontier tracks returned verified,
integrable work while the main thread kept building — 10 in one session.
The anti-patterns, seen once each: background jobs without timeouts (the
test hang) and orphaned jobs at the crash restart.
**Rule:** fan out only frontier tasks touching disjoint files; verify every
agent's output in the main thread before committing; every background
command gets `timeout -k`; on restart, reconcile orphaned outputs before
relaunching.

## F13 — Answer "is X true about our system?" with live evidence
Asked whether paid models were in use anywhere, the winning answer was a
live check quoting observed bindings — not a recollection.
**Rule:** never answer configuration/state questions from context alone;
run the check and quote the values.

## F14 — Two probes max, then PARK
Blocked experiments (a model too big for the box's memory, quants not
serving-ready, an upstream bug) were parked as graph nodes with re-entry
conditions instead of ground against.
**Rule:** two probe attempts on a blocked path, then it becomes a node with
a `reminder:` and a re-entry condition ("when bigger hardware lands / when
upstream fixes X") and you move to the next frontier task.

## F15 — Appends must be appends
The operator, on updating the handoff: "just dont accidentally replace
something important... so we are appending there."
**Rule:** handoff/BUILDLOG additions use `cat >>` or an assert-guarded
append script; anything that REPLACES text in a living doc gets the full
F4 treatment. And update the handoff at checkpoints — F8 proves sessions
die without warning.
