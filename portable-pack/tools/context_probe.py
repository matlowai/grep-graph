#!/usr/bin/env python3
"""Report a Claude Code session's CURRENT context size from its JSONL.

Usage:
    python tools/context_probe.py <session.jsonl>          # one session file
    python tools/context_probe.py <project-dir>            # newest .jsonl inside
    python tools/context_probe.py --latest <project-dir>   # same, explicit
    python tools/context_probe.py --latest                 # DEFAULT_PROJECT_DIR
    [--threshold N]   exit 1 when context_tokens > N

The path argument auto-detects: a directory means "use the newest .jsonl in
it", a file is used directly. Edit DEFAULT_PROJECT_DIR (below) to make bare
--latest work without an argument.
"""

import argparse
import json
import os
import sys

DEFAULT_PROJECT_DIR = os.path.expanduser(
    "~/.claude/projects/<your-project-slug>/"
)

RATE_TABLE = [
    ("fable", 1.0),
    ("opus", 0.50),
    ("sonnet", 0.30),
    ("haiku", 0.10),
]
DEFAULT_RATE = 1.0


def find_latest_jsonl(project_dir):
    entries = []
    for name in os.listdir(project_dir):
        if not name.endswith(".jsonl"):
            continue
        full = os.path.join(project_dir, name)
        if not os.path.isfile(full):
            continue
        entries.append((os.path.getmtime(full), full))
    if not entries:
        raise FileNotFoundError(f"no .jsonl files found in {project_dir}")
    entries.sort(key=lambda pair: pair[0])
    return entries[-1][1]


def find_last_usage_record(path):
    last_record = None
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except Exception:
                continue
            if record.get("type") != "assistant":
                continue
            message = record.get("message", {})
            usage = message.get("usage")
            if not usage:
                continue
            if message.get("model") == "<synthetic>":
                continue
            last_record = message
    if last_record is None:
        raise ValueError(f"no assistant usage records found in {path}")
    return last_record


def rate_for_model(model):
    lowered = model.lower()
    for substring, rate in RATE_TABLE:
        if substring in lowered:
            return rate
    return DEFAULT_RATE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="session .jsonl file, or a project dir (newest .jsonl inside is used)",
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="with no path: search DEFAULT_PROJECT_DIR for the newest .jsonl",
    )
    parser.add_argument("--threshold", type=int, default=None, help="token threshold")
    args = parser.parse_args()

    try:
        target = args.path or (DEFAULT_PROJECT_DIR if args.latest else None)
        if target is None:
            parser.error("must provide a path (file or dir), or --latest")
            return 2
        jsonl_path = find_latest_jsonl(target) if os.path.isdir(target) else target

        message = find_last_usage_record(jsonl_path)
        usage = message.get("usage", {})
        model = message.get("model", "unknown")
        context_tokens = (
            usage.get("cache_read_input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
            + usage.get("input_tokens", 0)
        )
        rate = rate_for_model(model)
        cost_per_turn = context_tokens * rate / 1_000_000

        print(
            f"context_tokens={context_tokens} model={model} "
            f"cost_per_turn_usd={cost_per_turn:.4f}"
        )

        if args.threshold is not None:
            verdict = "PAST" if context_tokens > args.threshold else "OK"
            print(f"threshold={args.threshold} verdict={verdict}")
            if verdict == "PAST":
                return 1
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
