# ASSUMPTIONS.md — provisional calls awaiting human review

<!-- The anti-stall valve (graph-kit SPEC §8). When the only blocker is a
     pending human review/decision AND a low-risk default exists: choose,
     act, log it here. The underlying question stays OPEN — an ASM
     substitutes for STALLING, not for authority. The human reviews this
     file at check-ins; a ratified ASM can graduate into a DEC
     (resolved-by: DEC-nnnn). Statuses: PROVISIONAL | RATIFIED | REVERSED.
     Tombstone reviewed entries in place; never delete. -->

ASM-1 · PROVISIONAL · {{DATE}} · <what was assumed, in one line>
resolves-attempt: <the Q-/T-/review item this substitutes for — stays OPEN>
chosen: <the option taken, and where it's now in effect>
alternatives: <what else was considered, and why each lost>
revisit-trigger: <the event that must force a re-look — "when the auth
  provider is chosen", "before the first external deploy">
resolved-by: <filled at review: human ratification date, or the DEC minted>
