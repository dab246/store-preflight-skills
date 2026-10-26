#!/usr/bin/env python3
"""Validate the skill's knowledge base.

Checks:
  * every rule file has complete front matter, a matching id/store/category and required sections
  * every rule's sources point to official Apple or Google documentation
  * every external link in Markdown files uses an allowed domain
  * every rule path referenced from checklists, SKILL.md and the scanner exists
  * requirements.json files contain the keys the scanner needs

Exit code 1 on any error. Standard library only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL = ("developer.apple.com", "apple.com", "support.google.com", "developer.android.com",
            "developers.google.com", "play.google", "play.google.com", "source.android.com",
            "android-developers.googleblog.com")
# Badges, the repository itself and GitHub docs are allowed in project docs (README, CONTRIBUTING...).
PROJECT_LINKS = ("img.shields.io", "github.com/dab246/store-preflight-skills", "docs.github.com")
REQUIRED_KEYS = ("id", "store", "category", "severity", "title", "automated", "sources", "last_verified")
SECTIONS = ("## What to check", "## Resolution", "## Example rejection")
SEVERITIES = {"REJECTION", "WARNING"}
LINK = re.compile(r"https?://[^\s)>\]\"'`]+")

errors: list[str] = []


def err(path: Path, msg: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def host_ok(url: str, allowed: tuple[str, ...]) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    full = host + parsed.path
    return any(host == a or host.endswith("." + a) or full.startswith(a) for a in allowed)


def front_matter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\s+- ", line) and key:
            data.setdefault(key, []).append(line.strip()[2:].strip())
        elif ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip().strip('"')
            data[key] = value if value else []
    return data


def check_rules() -> None:
    for store in ("apple", "google"):
        for path in sorted((ROOT / "references" / store / "rules").rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            fm = front_matter(text)
            if not fm:
                err(path, "missing YAML front matter")
                continue
            for key in REQUIRED_KEYS:
                if key not in fm or fm[key] in ("", []):
                    err(path, f"front matter is missing '{key}'")
            category = path.parent.name
            expected = f"{store}.{category}.{path.stem}"
            if fm.get("id") != expected:
                err(path, f"id should be '{expected}'")
            if fm.get("store") != store or fm.get("category") != category:
                err(path, "store/category do not match the folder")
            if fm.get("severity") not in SEVERITIES:
                err(path, f"severity must be one of {sorted(SEVERITIES)}")
            if store == "apple" and "guideline" not in fm:
                err(path, "Apple rules need 'guideline'")
            if store == "google" and "policy" not in fm:
                err(path, "Google rules need 'policy'")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(fm.get("last_verified", ""))):
                err(path, "last_verified must be YYYY-MM-DD")
            for src in fm.get("sources", []) if isinstance(fm.get("sources"), list) else []:
                if not host_ok(src, OFFICIAL):
                    err(path, f"source is not official Apple/Google documentation: {src}")
            for section in SECTIONS:
                if section not in text:
                    err(path, f"missing section '{section}'")


def check_links() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", "node_modules", "snapshots", "fixtures"} for part in path.parts):
            continue
        allowed = OFFICIAL if "references" in path.parts or path.name == "SKILL.md" else OFFICIAL + PROJECT_LINKS
        for url in LINK.findall(path.read_text(encoding="utf-8")):
            url = url.rstrip(".,;:")
            if not host_ok(url, allowed):
                err(path, f"link to non-allowed domain: {url}")


def check_references() -> None:
    rule_dirs = {s: ROOT / "references" / s / "rules" for s in ("apple", "google")}
    for store in ("apple", "google"):
        for path in (ROOT / "references" / store / "checklists").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for ref in re.findall(r"`((?:\.\./rules/)?[a-z_]+/[a-z0-9_]+\.md)`", text):
                rel = ref.removeprefix("../rules/")
                if not (rule_dirs[store] / rel).exists():
                    err(path, f"references missing rule {ref}")
    for path in [ROOT / "SKILL.md", ROOT / "README.md"]:
        if not path.exists():
            continue
        for ref in re.findall(r"(references/[\w/.-]+\.(?:md|json))", path.read_text(encoding="utf-8")):
            if not (ROOT / ref).exists():
                err(path, f"references missing file {ref}")
    scanner = (ROOT / "scripts" / "preflight_scan.py").read_text(encoding="utf-8")
    refs = set(re.findall(r'rule\("(apple|google)", "([\w/]+)"\)', scanner))
    refs |= {("google", p) for p in re.findall(r'"(permissions/\w+)"', scanner)}
    for store, rel in sorted(refs):
        if not (rule_dirs[store] / f"{rel}.md").exists():
            errors.append(f"scripts/preflight_scan.py: references missing rule {store}/{rel}")


def check_requirements() -> None:
    needed = {
        "apple": ["guidelines_last_updated", "sdk_minimum.xcode", "deployment_target_minimum.ios",
                  "metadata_limits.name"],
        "google": ["target_sdk.new_apps_and_updates", "play_billing_library.min_major",
                   "page_size_16kb.updates_blocked_from", "listing_limits.title"],
    }
    for store, keys in needed.items():
        path = ROOT / "references" / store / "requirements.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for dotted in keys:
            node = data
            for key in dotted.split("."):
                node = node.get(key) if isinstance(node, dict) else None
            if node in (None, ""):
                err(path, f"missing '{dotted}'")


def check_skill() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not re.search(r"^name: store-preflight-skills$", text, re.M):
        err(ROOT / "SKILL.md", "front matter name must be 'store-preflight-skills'")
    if not re.search(r"^description: ", text, re.M):
        err(ROOT / "SKILL.md", "front matter needs a description")


def main() -> int:
    check_rules()
    check_links()
    check_references()
    check_requirements()
    check_skill()
    if errors:
        print("❌ Validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
        return 1
    rules = len(list((ROOT / "references").rglob("rules/**/*.md")))
    print(f"✅ Knowledge base valid ({rules} rules)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
