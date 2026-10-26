---
id: apple.metadata.competitor_terms
store: apple
category: metadata
severity: REJECTION
guideline: "2.3.10 · 2.3.7 · 4.1(c)"
title: Other platforms, stores or brands in App Store metadata
automated: true
sources:
  - https://developer.apple.com/app-store/review/guidelines/#2.3.10
  - https://developer.apple.com/app-store/review/guidelines/#4.1
last_verified: 2026-10-26
---

# Other platforms, stores or brands in App Store metadata

## What to check

- No names, icons or imagery of other mobile platforms or alternative app marketplaces in the
  name, subtitle, keywords, description, What's New, screenshots, previews or in-app UI shown to
  reviewers (2.3.10). Typical offenders: "Android", "Google Play", "Play Store", "Galaxy Store",
  Android-styled status bars in screenshots, "Get it on Google Play" badges.
- No third-party brand names in the keywords field to borrow traffic (2.3.7).
- No other developer's icon, brand or product name in your name or icon without approval (4.1(c)).

## How to detect

```bash
grep -rniE "android|google play|play store|galaxy store" metadata/ 2>/dev/null
```

Also search localized strings shown in onboarding and help screens, and inspect screenshots.

## Resolution

Replace with platform-neutral wording ("available on your other devices") or remove; regenerate
screenshots from an iOS build.

## Example rejection

> Guideline 2.3.10 - Performance - Accurate Metadata. Your app or its metadata contains irrelevant
> third-party platform information. Specifically, your app's description references Android.
