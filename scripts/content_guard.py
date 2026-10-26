#!/usr/bin/env python3
"""Fail when tracked files, commit messages or PR text contain blocked terms.

The blocked terms are NOT stored in the repository. They come from the
CONTENT_GUARD_TERMS environment variable (a comma-separated list, set as a
repository secret), so the guard can enforce naming rules without committing
the names themselves.

Usage:
  CONTENT_GUARD_TERMS="term1,term2" python3 scripts/content_guard.py [--text-env VAR ...] [--commits RANGE]
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-env", action="append", default=[],
                    help="name of an env var holding extra text to check (PR title/body)")
    ap.add_argument("--commits", help="git revision range whose messages and authors are checked")
    args = ap.parse_args()

    terms = [t.strip() for t in os.environ.get("CONTENT_GUARD_TERMS", "").split(",") if t.strip()]
    if not terms:
        print("CONTENT_GUARD_TERMS is not set; skipping content guard.")
        return 0
    rx = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(re.escape(t) for t in terms) + r")(?![A-Za-z0-9])", re.I)
    hits: list[str] = []

    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    for name in files.splitlines():
        hits += [f"file name: {name}"] if rx.search(name) else []
        try:
            text = (ROOT / name).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if rx.search(line):
                hits.append(f"{name}:{lineno}")

    if args.commits:
        log = subprocess.run(["git", "log", "--format=%H%n%an <%ae>%n%cn <%ce>%n%B%n---END---", args.commits],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        for chunk in log.split("---END---"):
            if rx.search(chunk):
                hits.append(f"commit {chunk.strip().splitlines()[0][:12]}")

    for var in args.text_env:
        if rx.search(os.environ.get(var, "")):
            hits.append(f"${var}")

    if hits:
        # Print locations only, never the matched term, so logs stay clean too.
        print("❌ Blocked terms found in:\n" + "\n".join(f"  - {h}" for h in hits))
        return 1
    print("✅ Content guard passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
