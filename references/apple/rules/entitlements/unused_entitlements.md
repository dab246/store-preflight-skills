---
id: apple.entitlements.unused_entitlements
store: apple
category: entitlements
severity: WARNING
guideline: "2.4.5(i) · 2.5.1"
title: Unused, unjustified or missing entitlements (incl. Mac sandbox)
automated: partial
sources:
  - https://developer.apple.com/app-store/review/guidelines/#2.4.5
  - https://developer.apple.com/documentation/bundleresources/entitlements
  - https://developer.apple.com/documentation/security/app-sandbox
last_verified: 2026-10-26
---

# Unused, unjustified or missing entitlements

## What to check

- Every capability in `*.entitlements` is used by shipped code (HealthKit, HomeKit, iCloud, NFC,
  Siri, push, associated domains, Apple Pay). Reviewers ask why unused capabilities exist; HealthKit
  without a visible health feature is a common rejection.
- **Mac App Store:** `com.apple.security.app-sandbox` is enabled; every
  `com.apple.security.temporary-exception.*` is justified in the review notes; no Full Disk Access
  dependence for core features (Apple announced stricter Full Disk Access controls in 2026).
- Mac apps are universal (Apple silicon native) — macOS 27 is the last release to support Rosetta for
  most apps.

## How to detect

```bash
find . -name "*.entitlements" -not -path "*/Pods/*" -exec plutil -p {} \;
```

The scanner maps common entitlements to the code that uses them and flags ones with no match.

## Resolution

Remove capabilities in **Signing & Capabilities** that the app does not use; justify the rest in the
Notes for Review.

## Example rejection

> Guideline 2.4.5(i) - Performance. Your app includes entitlements that are not used by the app's
> functionality: com.apple.security.temporary-exception.files.absolute-path.read-write.
