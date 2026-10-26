---
id: apple.metadata.accurate_metadata
store: apple
category: metadata
severity: REJECTION
guideline: "2.3 · 2.3.3 · 2.3.4 · 2.3.7 · 2.3.12"
title: Inaccurate or over-limit App Store metadata
automated: partial
sources:
  - https://developer.apple.com/app-store/review/guidelines/#2.3
  - https://developer.apple.com/app-store/product-page/
last_verified: 2026-10-26
---

# Inaccurate or over-limit App Store metadata

## What to check

| Field | Limit | Notes |
|---|---|---|
| Name | 30 | No generic terms, prices, or other brands (2.3.7) |
| Subtitle | 30 | Same rules as the name |
| Keywords | 100 | Comma-separated, no competitor or trademarked terms, no category names |
| Promotional text | 170 | Can change without a new build |
| Description | 4000 | Must describe what the app actually does; no unverifiable claims |
| What's New | 4000 | List significant changes (2.3.12) |

- **Screenshots (2.3.3)** show the app in use — not only splash, login or marketing slides — and
  match the device class they are uploaded for.
- **App previews (2.3.4)** use screen captures of the app; no device frames, no hands holding phones,
  no footage of features that are not in the build.
- **Prices** are not mentioned in name/subtitle/keywords/screenshots (2.3.7); IAP-gated features are
  marked as such (2.3.2).
- **Age rating (2.3.6)** answers are current (the questionnaire changed in 2026 and now asks about
  social-media capabilities).
- No placeholder text ("Lorem ipsum", "TBD") anywhere, including localizations.

## How to detect

Pull metadata with the official [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
or any tool that writes per-locale text files, then run `scripts/preflight_scan.py --metadata <dir>`
for limits. Review screenshots and previews manually.

## Resolution

Trim fields to the limit, replace marketing slides with real UI, remove device frames from previews,
and keep claims verifiable ("used by 10,000 clinics" needs a source; "#1 app" is not allowed).

## Example rejection

> Guideline 2.3.3 - Performance - Accurate Metadata. Your screenshots do not sufficiently reflect your
> app in use. Specifically, your screenshots only show the login screen.
