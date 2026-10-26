---
id: apple.design.hidden_features
store: apple
category: design
severity: REJECTION
guideline: "2.5.19 · 2.3.1"
title: Hidden, dormant or review-dependent features
automated: partial
sources:
  - https://developer.apple.com/app-store/review/guidelines/#2.5.19
last_verified: 2026-10-26
---

# Hidden, dormant or review-dependent features

Guideline 2.5.19 (added 2026-10-16) makes explicit that apps must not contain hidden, dormant or
undocumented features, and must not obfuscate functionality or change behaviour after approval.
Violations can lead to removal and **termination of the developer account**.

## What to check

- Code that detects App Review, TestFlight or the sandbox environment (`sandboxReceipt`,
  `isTestFlight`, reviewer IP/region checks) and changes **what features exist**.
- Remote config / feature flags that unlock functionality not described in the Notes for Review.
- Date-based "time bombs", hidden menus, or gestures that unlock unrelated content (e.g. a calculator
  that becomes a casino).
- Server-driven UI or downloaded code that adds features after approval (also 2.5.2).

Feature flags are fine when every possible state is present in the reviewed build, reachable by the
reviewer and listed in the review notes.

## How to detect

```bash
grep -rnE "sandboxReceipt|isTestFlight|isReviewMode|reviewMode|isAppReview" .
grep -rnE "RemoteConfig|remote_config|featureFlag|FeatureFlag" .
```

## Resolution

Use environment detection only for diagnostics; list every flag and its purpose in the Notes for
Review; ship features in the binary and describe them.

## Example rejection

> Guideline 2.5.19 - Performance - Software Requirements. Your app includes hidden features that were
> not disclosed to App Review.
