---
id: apple.privacy.app_tracking_transparency
store: apple
category: privacy
severity: WARNING
guideline: "5.1.2 · 2.1"
title: App Tracking Transparency mismatches
automated: true
sources:
  - https://developer.apple.com/app-store/review/guidelines/#5.1.2
  - https://developer.apple.com/documentation/apptrackingtransparency
  - https://developer.apple.com/app-store/user-privacy-and-data-use/
last_verified: 2026-10-26
---

# App Tracking Transparency mismatches

## What to check

- If the app or any SDK **tracks** (links app data with third-party data for advertising or
  measurement, or shares it with data brokers), it must call
  `ATTrackingManager.requestTrackingAuthorization` before tracking and respect a denial.
- If App Store Connect's App Privacy says "used for tracking" or `Info.plist` contains
  `NSUserTrackingUsageDescription`, reviewers expect to **see the prompt**. Declared-but-never-shown
  is a common 2.1 rejection.
- No incentives, gating, or pre-prompt screens that mimic the system alert. A neutral explainer is fine.
- EU: starting with iOS 27.2 an alternative ATT prompt is available in the EU and is the only one
  allowed in some member states — the obligation to ask does not change.

## How to detect

```bash
grep -rnE "ATTrackingManager|requestTrackingAuthorization|advertisingIdentifier|ASIdentifierManager" .
plutil -p ios/Runner/Info.plist | grep NSUserTrackingUsageDescription
```

Review the SDK list (ads, attribution, analytics) and their privacy manifests for
`NSPrivacyTracking = true`.

## Resolution

- Tracking: add the purpose string and request authorization at a moment that makes sense, before
  any tracking SDK is initialised; pass the result to SDKs.
- Not tracking: remove the purpose string, set `NSPrivacyTracking` to false, and fix the App
  Privacy answers.
- Tell the reviewer where the prompt appears in the **Notes for Review**.

## Example rejection

> Guideline 2.1 - Information Needed. We're looking forward to completing our review, but we need
> more information to continue. Your app uses the AppTrackingTransparency framework, but we are
> unable to locate the App Tracking Transparency permission request when reviewed on iOS 27.
