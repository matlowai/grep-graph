# 01 — Verification discipline: nothing is done until you've read it back

## Trigger
Any time you write, edit, move, or commit anything — especially via a script,
a heredoc, or any indirection where you don't see the resulting bytes.

## The rules

1. **Verify-on-write.** Every scripted file edit asserts BOTH ways: the old
   string is present before replacing (`str.replace` no-ops silently on a
   no-match), and the new token is present after writing (`assert TOKEN in
   Path(f).read_text()`, or `grep -c` failing on 0) — then re-read in a
   SEPARATE call. The token is something that could ONLY exist if the edit
   landed. If the edit mints a graph ID, also grep the committed blob:
   `git show HEAD:<file> | grep -c "<ID>"`.
2. **Git commands pin their repo.** Every git invocation either starts with
   `cd <absolute-repo-path> &&` or uses `git -C <repo>`. The shell cwd
   RESETS between every Bash call — it doesn't persist from your last `cd`.
   Same rule inside python heredocs: absolute paths only. Never combine
   `git add -A` with anything cwd-dependent; name the files.
3. **After a commit, confirm it.** `git -C <repo> log --oneline -1` and check
   the message and repo are the ones you intended.
4. **Tests narrate themselves.** Every assert carries a message with the
   actual value; multi-stage tests print `[stage]` lines. A green test whose
   output shows nothing proves nothing to the next reader.
5. **Don't verify by memory.** "I wrote that earlier" is not evidence. If a
   later step depends on an earlier edit, re-check the file at the point of
   dependence, not the point of writing.

## Why (real incidents, origin project 2026-07)

- A cleanup script held file content in a variable, edited it, then a stray
  `p.write_text(t)` re-wrote the PRE-edit content — the edit existed for
  seconds and silently vanished. Discovered much later, cost a re-derivation.
- A heredoc edit ran with the wrong cwd and edited nothing at all; the
  command exited 0. Nothing looked wrong until a grep came back empty.
- cwd drifted between two sibling repos and a commit landed in the wrong repo
  with the wrong message.

All three produced **success-shaped output while failing**. That's the
pattern to internalize: exit code 0 and no error text are not verification.

## Self-check (ask at every checkpoint)
- Did any write in the last stretch of work end WITHOUT a read-back?
- Could I, right now, name the grep that proves my last edit is on disk?
- Is there any git command in my recent history that didn't pin its repo?
