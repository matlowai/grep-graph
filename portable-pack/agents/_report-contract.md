# Shared report contract (referenced by every exec-* agent; not an agent itself)

Why this exists: delegating to a cheaper model only saves money if the parent
(the coordinator/main session) does NOT have to re-read files to find out what
you did — parent input tokens burned on re-reading can exceed the output tokens
saved. Your final message is therefore the ONLY artifact the parent reads. Make
it carry everything.

THE CONTRACT — your final message MUST:
1. Lead with the outcome in one sentence (done/blocked/partial + the verdict).
2. List every file you changed as `path — one-line why`, and QUOTE the
   load-bearing hunks (the 3-15 lines that matter), not "updated successfully".
3. State facts with their actual values: test-output tails (counts, not
   "passed"), measured numbers, resolved IDs, URLs, exact error strings.
4. Give file:line anchors for anything the parent might want to spot-check.
5. Put surprises, deviations from the spec, and anything you're unsure of in
   an explicit "REVIEW THIS" section — that section is the only thing the
   parent should ever need to open files for.
6. Never summarize away information the parent would have to re-derive.

Also binding, always:
- When you make multiple tool calls with no dependency between them, issue
  them in ONE message as parallel tool calls — every extra assistant turn
  re-bills your entire context as cache-read tokens. Inspect a file with a
  single Read, never serial tail/head/grep peeks at the same file.
- If the repo has docs/upskilling/, read 01-verification + 02-probe-first +
  04-environment before touching anything; follow CLAUDE.md if present.
- Verify-on-write; `cd <abs> &&` on every bash call (cwd resets between
  calls); `timeout -k 5 <cap>` on every test run / long command; tests
  narrate themselves (asserts carry actual values).
- Don't re-read files whose relevant content the spawning prompt already
  quotes — trust the spec; probe live systems before building on doc claims.
- Never touch graph docs (the DAG / INDEX / DECISIONS / SESSION_HANDOFF /
  BUILDLOG family) unless the prompt explicitly says to. No commits unless told.
