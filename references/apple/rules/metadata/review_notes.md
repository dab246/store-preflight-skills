---
id: apple.metadata.review_notes
store: apple
category: metadata
severity: REJECTION
guideline: "2.1(a) · 2.3.1(a)"
title: Incomplete App Review information
automated: false
sources:
  - https://developer.apple.com/app-store/review/guidelines/#2.1
  - https://developer.apple.com/distribute/app-review/
last_verified: 2026-10-26
---

# Incomplete App Review information

## What to check

- **Demo account** with full access (and a way past 2FA / OTP / geo-restrictions), or a built-in demo
  mode, plus a live backend during review (2.1(a)).
- **Notes for Review** describe new features *with specificity* — generic notes are rejected
  (2.3.1(a)). Mention every feature flag that can be switched on (see 2.5.19).
- For hardware, region-locked or B2B apps: a screen recording on a real device showing the full flow.
- Regulated apps (banking, health, gambling, crypto, VPN, loans): licenses/documentation and the
  legal entity name (5.1.1(ix)).
- External services the reviewer will meet (payments, SSO, invitation codes) are explained.
- Contact phone and email are monitored during review.

## Resolution

Fill in the Notes for Review using this template:

```text
WHAT THE APP DOES: one or two sentences.
HOW TO TEST: 1) Log in with demo@example.com / Passw0rd! 2) Tap "Scan" ... 3) ...
WHAT'S NEW IN THIS VERSION: specific list of features/changes.
FEATURE FLAGS: list every remotely switchable feature and its state in this build.
PERMISSIONS: where each permission prompt appears and why.
PURCHASES: product IDs, where they appear, sandbox notes.
THIRD-PARTY AI / DATA SHARING: where consent is collected.
REGULATORY: license numbers, attached documents.
VIDEO: link to a screen recording (for hardware/region-restricted flows).
```

## Example rejection

> Guideline 2.1 - Information Needed. We are unable to successfully access all or part of the app.
> To continue the review, provide a demo account and password with full access.
