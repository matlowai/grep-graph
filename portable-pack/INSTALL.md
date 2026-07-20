# INSTALL.md — placing the portable pack in a new repo

Everything below is copy + fill-placeholders + restart. No file here depends on
the project the pack came from.

## 1. Where each piece goes

| From the pack | Goes to (in the new repo) | Notes |
|---|---|---|
| `agents/sonnet-low.md` etc. (6 files incl. `_report-contract.md`) | `.claude/agents/` | project-level agents; **client restart required** to register (see §3) |
| `upskilling/` (README + 01–09) | `docs/upskilling/` | binding operating procedure; read in full at session start |
| `graph-templates/CONVENTIONS.md` | `CONVENTIONS.md` (repo root) | read-first operating procedure |
| `graph-templates/INDEX.md` | `INDEX.md` (repo root) | flat ID ledger; verify every session |
| `graph-templates/DAG.md` | `DAG.md` (repo root) | execution view of tasks |
| `graph-templates/SESSION_HANDOFF.md` | `SESSION_HANDOFF.md` (repo root) | rehydration scratch |
| `CLAUDE-template.md` | `CLAUDE.md` (repo root) | **merge**, don't blind-overwrite an existing one |
| `tools/context_probe.py` | `tools/context_probe.py` | see §4 — one line to edit |

A one-shot copy from inside the pack directory:

```
mkdir -p ../../.claude/agents ../../docs/upskilling ../../tools
cp agents/*.md            ../../.claude/agents/
cp upskilling/*.md        ../../docs/upskilling/
cp graph-templates/*.md   ../../          # CONVENTIONS/INDEX/DAG/SESSION_HANDOFF
cp tools/context_probe.py ../../tools/
cp CLAUDE-template.md     ../../CLAUDE.md  # or merge by hand if one exists
```

(Adjust `../../` to wherever the pack sits relative to the target repo root.)

## 2. Placeholder inventory (fill these — few and obvious by design)

Grep the copied files for `{{` to find every slot. The full set:

- `{{PROJECT_NAME}}` — the new project's name (CLAUDE.md).
- `{{ONE_LINE_VISION}}` — one sentence describing the project (CLAUDE.md).
- `{{OPUS_MODEL_ID}}` — the exact model id string your CLI uses for the Opus
  tier, in all three of opus-low/opus-med/opus-high (e.g. `claude-opus-4-8`).
- `{{SECOND_OPINION_MODEL_ID}}` — a DIFFERENT high-capability model id for the
  `intuition` sounding-board agent (its value comes from being a second
  architecture; upskilling 03). If you have only one model line, drop this agent.
- `{{HEAVY_RESOURCE}}` — the scarce local resource that must be serialized:
  GPU/VRAM, RAM, a license seat, an API rate pool (upskilling 04, CLAUDE.md).
- `{{SPEND_POLICY}}` — your money/licensing rule (CLAUDE.md operator ground rules).
- `{{MOCK_POLICY}}` — mocks allowed, or real-only (CLAUDE.md operator ground
  rules). Decide this EARLY — it changes how every executor phases its work.
  Recommended: real-only with phased implementation (the template's default
  text; graph-kit GOTCHAS C5).
- `{{DATE}}` — today, wherever a template shows a "Verified:"/"Current state" line.
- `{{TRACK}}` / `{{TRACK_NAME}}` / `{{TRACK2}}` / `{{TRACK_NAME_2}}` — the letter
  and label for your DAG tracks (DAG.md, INDEX.md); pick per project.
- `{{FAMILY}}` — the letter for a question family (INDEX.md worked example).
- `{{TOPIC}}` — a research-topic slug for a RES-* node (CONVENTIONS/INDEX examples).

Rule of thumb: fill what you'll use now, delete the worked-example rows/HTML
comments you don't, and let real nodes replace the placeholders as you work.

## 3. `.claude/agents/` requires a full client restart (hard-won)

New agent-definition files under `.claude/agents/` are read at client startup.
Dropping the files in while a session is live will NOT register them — the
delegate calls silently won't see the new tiers. **Restart the client fully**
after copying, then confirm the tiers are available before relying on them.
(If your CLI renames the intuition agent's file, keep the `name:` frontmatter
matching the filename stem.)

## 4. `tools/context_probe.py` — one line to edit

The script ships verbatim from the origin project. Its `DEFAULT_PROJECT_DIR`
constant points at the origin project's Claude-projects session-log directory;
either edit that constant to your new project's log dir, or always pass the log
dir explicitly:

```
python tools/context_probe.py --latest /path/to/~/.claude/projects/<your-project-dir>/
python tools/context_probe.py --latest <dir> --threshold 350000   # exit 1 = past
```

`RATE_TABLE` maps model-name substrings to $/MTok cache-read rates — adjust if
your rates differ. Everything else (finding the newest JSONL, summing
cache-read + cache-creation + input tokens off the last real assistant usage
record) is project-generic.

## 5. First-run smoke test

After restart, from the new repo root:

1. `grep -c "{{" -r .claude docs/upskilling CONVENTIONS.md INDEX.md DAG.md CLAUDE.md`
   → should be 0 (every placeholder filled or its example deleted).
2. `python tools/context_probe.py --latest <your-log-dir>` → prints a
   `context_tokens=… cost_per_turn_usd=…` line (proves the probe finds your logs).
3. Start a fresh session; it should read the session-start order in CLAUDE.md,
   echo the operator card from upskilling 09, and be ready to delegate.
