---
id: google.permissions.query_all_packages
store: google
category: permissions
severity: REJECTION
policy: Use of the broad package (App) visibility (QUERY_ALL_PACKAGES) permission
title: QUERY_ALL_PACKAGES without a qualifying use case
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/10158779
  - https://developer.android.com/training/package-visibility
last_verified: 2026-10-26
---

# QUERY_ALL_PACKAGES without a qualifying use case

## What to check

Broad package visibility is only allowed when the core feature must discover any installed app
(device search, anti-virus, file managers, browsers, accessibility, financial-security verification).
Most apps only need a `<queries>` element for specific packages or intents.

## How to detect

```bash
grep -rn "QUERY_ALL_PACKAGES" --include=AndroidManifest.xml .
```

## Resolution

Replace with `<queries>` entries (`<package>`, `<intent>`, `<provider>`), remove SDK-merged
declarations with `tools:node="remove"`, or file the declaration if you qualify.

## Example rejection

> Your app uses the QUERY_ALL_PACKAGES permission but it does not meet the requirements for its
> use.
