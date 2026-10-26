---
id: google.technical.target_api_level
store: google
category: technical
severity: REJECTION
policy: Target API level requirements
title: targetSdk below the Google Play requirement
automated: true
sources:
  - https://developer.android.com/google/play/requirements/target-sdk
  - https://support.google.com/googleplay/android-developer/answer/11926878
last_verified: 2026-10-26
---

# targetSdk below the Google Play requirement

Values mirror `references/google/requirements.json`, refreshed weekly by the policy sync.

## What to check

| Since 2026-08-31 | Required `targetSdk` |
|---|---|
| New apps and app updates (phone, tablet, foldable) | **36** (Android 16) |
| Wear OS and Android Automotive OS | **35** |
| Android TV and Android XR | **34** |
| Existing apps, to stay visible to new users on newer Android versions | **35** |

An extension can be requested in Play Console until **2026-11-01**. Raising `targetSdk` turns on
new platform behaviours — test edge-to-edge, predictive back, foreground-service types, exact
alarms, photo picker and notification permission flows.

## How to detect

```bash
grep -rnE "targetSdk(Version)?" --include=*.gradle --include=*.kts --include=*.toml android/ app/ . 2>/dev/null
```

- **Flutter:** `flutter.targetSdkVersion` comes from the Flutter SDK — upgrade Flutter or set a literal.
- **Expo / React Native:** `expo-build-properties` → `android.targetSdkVersion`, or `android/build.gradle` `ext`.
- **Capacitor:** `android/variables.gradle`.
- Confirm in Play Console ▸ App bundle explorer after upload.

## Resolution

Raise `compileSdk` and `targetSdk` to the required level, update AGP/Kotlin/dependencies as needed,
and run the behaviour-change checklist for each skipped Android version.

## Example rejection

> Your app currently targets API level 34 and must target at least API level 36 to ensure it is
> built on the latest APIs optimized for security and performance.
