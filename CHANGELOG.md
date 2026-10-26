# Changelog

[![Release](https://img.shields.io/github/v/release/dab246/store-preflight-skills?sort=semver&color=blue)](https://github.com/dab246/store-preflight-skills/releases)
[![Policy sync](https://img.shields.io/github/actions/workflow/status/dab246/store-preflight-skills/policy-sync.yml?label=policy%20sync)](https://github.com/dab246/store-preflight-skills/actions/workflows/policy-sync.yml)

All notable changes to this project are documented here. The format follows the *Keep a Changelog*
convention and the project uses *Semantic Versioning*:

- **MAJOR** — breaking changes to `SKILL.md` flow, rule front matter or scanner CLI/JSON output
- **MINOR** — new rules, checklists, scanner checks or policy sources
- **PATCH** — rule text updates from policy syncs, fixes, false-positive reductions

Each entry is grouped by store: 🍎 App Store · 🤖 Google Play · 🔀 Both / tooling.

## [Unreleased]

### Changed
- _Weekly policy-sync pull requests add their entries here._

## [1.0.0] - 2026-10-26

First public release.

### Added

#### 🔀 Skill & tooling
- `SKILL.md` with flexible scope: **apple**, **google** or **both** stores; auto-detection for native,
  Flutter, React Native/Expo, Capacitor and Kotlin Multiplatform projects; `quick`, `full` and `fix`
  depths; category filters.
- `scripts/preflight_scan.py` — dependency-free scanner with Markdown/JSON output, `--strict` mode for
  CI and per-project configuration through `.store-preflight.json` (`ai_service_terms`,
  `ai_endpoints`, `ignore`).
- Cross-store matrix and report template for both-store reviews.
- Weekly **policy sync** workflow: fetches official Apple and Google sources, diffs normalised
  snapshots, reports changed Apple guideline numbers, refreshes `requirements.json` thresholds,
  regenerates `live-index.md` and `upcoming-deadlines.md`, checks documentation links and opens a
  pull request (or an issue when a source is unreachable).
- CI: knowledge-base validator (front matter, official-source allow-list, broken references), unit
  tests on Python 3.9 and 3.13, scanner smoke tests, and a content guard driven by a repository
  secret.
- Release workflow that publishes the matching changelog section and a ready-to-install zip.
- Issue forms (rejection report, rule request, bug report), pull request template, Dependabot.

#### 🍎 App Store — 19 rules, 10 checklists
- Guidelines synced with Apple's **2026-10-16** revision, including new **2.3.14** (creative assets)
  and **2.5.19** (hidden features), and the expanded scope of **1.2**.
- Upload requirements: Xcode 26 / 26 SDK (since 2026-04-28) and iOS 13 minimum deployment target
  (since 2026-09-09).
- Automated checks: privacy manifest vs required-reason APIs, missing/vague purpose strings, ATT
  mismatches, Sign in with Apple, review-environment detection, external payment SDKs, unused and
  temporary-exception entitlements, Mac sandbox, deployment target, metadata limits, other-platform
  terms and AI terms for the China mainland storefront.
- Checklists: all apps, subscriptions/IAP, social/UGC, kids, health, games, macOS, AI, crypto/finance,
  VPN.

#### 🤖 Google Play — 32 rules, 10 checklists
- Target API level **36** for new apps and updates since 2026-08-31 (Wear OS/Automotive 35,
  TV/XR 34; extension until 2026-11-01).
- Play Billing Library **8+** since 2026-08-31; **16 KB** page-size support (updates blocked from
  2027-02-01) with ELF alignment checks on bundled `.so` files.
- 2026 policy changes: anonymous/random chat apps under Age-Restricted Content, Child Safety
  Standards and Families (2026-08-26); Android developer verification (2026-09-30); Contacts
  Permissions policy, location button, geofencing removed from foreground-service use cases and
  READ_CALL_LOG phone-call verification removed (2027-01-27).
- Automated checks: target SDK per form factor, `com.example` package, debuggable manifest, Billing
  Library version, 12 restricted permission families, foreground-service types, Health Connect,
  precise location, store-listing limits and metadata policy terms, generative-AI and account-deletion
  signals, external payment SDKs.
- Checklists: all apps, subscriptions, social/UGC, kids/families, health, games, AI,
  finance/crypto/loans, VPN, Wear/TV/Auto/XR.

[Unreleased]: https://github.com/dab246/store-preflight-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/dab246/store-preflight-skills/releases/tag/v1.0.0
