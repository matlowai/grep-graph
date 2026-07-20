# 04 — Environment discipline: the box is a shared, mortal resource

## Trigger
Before launching anything heavy ({{HEAVY_RESOURCE}} loads, big generation
jobs, training, big batch jobs), and before putting anything you'd mind
losing in a temp directory.

## The rules

1. **Serialize heavy local jobs.** One heavy job at a time on this box.
   Before launching {{HEAVY_RESOURCE}}- or RAM-heavy work, check what's
   already loaded and how much headroom is free (e.g. `nvidia-smi`, `free -h`
   — whatever measures your heavy resource). If a resident service is up,
   that counts as the running heavy job — size accordingly or run on CPU.
2. **Never stack parallel generators.** Parallelism is for I/O-bound and
   remote work. Local compute-heavy tasks queue; they don't fan out.
3. **/tmp dies on reboot.** Anything worth ten minutes of work goes in the
   repo (or another durable path) IMMEDIATELY, not "when it's done".
   Scratch is for genuinely disposable intermediates only.
4. **Background jobs need a liveness story AND a bound.** Every background
   command and test run gets `timeout -k 5 <cap>` — an unbounded test hang
   once cost ~25 minutes. Know how you'll detect hung-vs-working (log
   cadence, output growth) before launching, and monitor with a condition
   that matches ONLY the terminal summary line (e.g. pytest:
   `[0-9]+ (passed|failed|error)`), never a mid-stream substring.
5. **After any crash/reboot, re-verify the world** — services that were up,
   files that were in /tmp, resource state. Don't resume from your pre-crash
   mental model.
6. **Batch independent tool calls into ONE turn** (measured, origin project
   2026-07): every extra assistant turn re-bills the whole context as
   cache-read tokens (~10% of the base input price per token — cheap per
   token, dominant in aggregate because EVERY turn pays it on the FULL
   prefix). Parallel tool calls inside one message count as ONE turn: K
   reads in one message = one re-bill; K serial reads = K re-bills against
   a growing prefix. Inspect a file with a single Read, not serial
   tail/head/grep peeks; independent ls/grep/git-show calls go in one
   message; multiple known files land in one `cat a b c`. Calibration from
   the audit: mid-session batching waste was ~4% of spend — the 10x lever
   is session hygiene (fresh contexts, /clear at seams, delegation), so
   batch as habit but spend real effort on session scope. The one place
   batching IS load-bearing: the post-/clear rehydration read-in (05/09) —
   "clearing is free" assumes the session-start docs arrive in ONE
   operation, not one-file-per-turn ceremony that taxes every clear.

## Why (origin project 2026-07)

Three heavy generation jobs were launched in parallel beside a resident model
server already holding most of the {{HEAVY_RESOURCE}}. The box froze hard
enough to force a reboot. Costs: the reboot itself, /tmp scratch wiped, and
re-verification of every running service. The one harness that survived did
so ONLY because it had already been graduated from scratch into `tools/` in
the repo. Restart-safe services self-healed; the local work didn't.

The underlying error was an optimism default: "these jobs are independent,
parallel is faster." On a shared box with a resident model server,
independent jobs still share the heavy resource, RAM, and I/O — the freeze
was the scheduler telling us what "independent" actually meant.

## Self-check
- Before this launch: what heavy thing is ALREADY running, and did I check
  or am I assuming?
- If the box died right now, what would I lose? (If the answer is more than
  10 minutes of work: commit/copy first.)
