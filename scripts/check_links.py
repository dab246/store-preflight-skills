#!/usr/bin/env python3
"""Check that every official documentation link in the knowledge base still resolves.

Run weekly by the policy-sync workflow; broken links are appended to the sync
report so maintainers can update rule sources. Standard library only.

Usage: python3 scripts/check_links.py [--report links.md]
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"https?://[^\s)>\]\"'`]+")
SKIP_HOSTS = ("img.shields.io", "github.com")
HEADERS = {"User-Agent": "Mozilla/5.0 (store-preflight-skills link check)"}


def collect() -> dict[str, list[str]]:
    urls: dict[str, list[str]] = {}
    candidates = [ROOT / "SKILL.md", ROOT / "README.md", *sorted((ROOT / "references").rglob("*.md"))]
    for path in (p for p in candidates if p.exists()):
        for url in LINK.findall(path.read_text(encoding="utf-8")):
            url = url.rstrip(".,;:").split("#", 1)[0]  # anchors share one request
            if "{" in url or "…" in url or any(h in url for h in SKIP_HOSTS):
                continue
            urls.setdefault(url, []).append(str(path.relative_to(ROOT)))
    return urls


def status(url: str) -> tuple[str, int | str]:
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return url, resp.status
        except urllib.error.HTTPError as exc:
            if method == "GET" or exc.code not in (403, 405, 501):
                return url, exc.code
        except Exception as exc:  # noqa: BLE001 - DNS, TLS, timeouts
            if method == "GET":
                return url, type(exc).__name__
    return url, "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    urls = collect()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(status, urls))
    broken = [(u, s) for u, s in results if not (isinstance(s, int) and s < 400)]
    lines = [f"### 🔗 Link check — {len(urls)} links, {len(broken)} broken", ""]
    lines += [f"- `{s}` {u} (in {', '.join(sorted(set(urls[u])))})" for u, s in broken] or ["All links resolve."]
    text = "\n".join(lines) + "\n"
    print(text)
    if args.report:
        with args.report.open("a", encoding="utf-8") as fh:
            fh.write("\n" + text)
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
