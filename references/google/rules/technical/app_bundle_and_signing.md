---
id: google.technical.app_bundle_and_signing
store: google
category: technical
severity: REJECTION
policy: App bundle, signing and upload requirements
title: Upload blockers (AAB, signing, debuggable, package name, 64-bit)
automated: partial
sources:
  - https://developer.android.com/guide/app-bundle
  - https://support.google.com/googleplay/android-developer/answer/9842756
last_verified: 2026-10-26
---

# Upload blockers

## What to check

- New apps are published as **Android App Bundles** (`.aab`) with **Play App Signing**.
- The release is not **debuggable** (`android:debuggable="true"` or a debug-signed bundle is refused).
- The package name does not start with `com.example`, `com.android`, `android` or other reserved
  prefixes, and never changes after the first upload.
- `versionCode` is higher than every previous upload on every track.
- Native code ships **64-bit** ABIs (`arm64-v8a`, plus `x86_64` if you ship `x86`).
- The upload key matches the one registered with Play.

## How to detect

```bash
grep -rnE "applicationId|versionCode|debuggable|abiFilters" --include=*.gradle --include=*.kts .
bundletool dump manifest --bundle app-release.aab | grep -E "package=|debuggable"
```

## Resolution

Build with `./gradlew bundleRelease`, configure `signingConfigs.release`, remove manifest-level
`debuggable`, and choose a reverse-domain package name you control.

## Example rejection

> You uploaded a debuggable APK or Android App Bundle. For security reasons you need to disable
> debugging before it can be published in Google Play.
