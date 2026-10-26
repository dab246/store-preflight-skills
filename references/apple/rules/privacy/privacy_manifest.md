---
id: apple.privacy.privacy_manifest
store: apple
category: privacy
severity: REJECTION
guideline: "5.1.1 · ITMS-91053"
title: Missing or incomplete privacy manifest
automated: true
sources:
  - https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
  - https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api
last_verified: 2026-10-26
---

# Missing or incomplete privacy manifest

## What to check

Every app (and every third-party SDK it embeds) that calls a **required-reason API** must ship a
`PrivacyInfo.xcprivacy` that declares the API category and an approved reason code. App Store
Connect blocks the upload (`ITMS-91053: Missing API declaration`) when a declaration is missing.

| Category key | Typical APIs | Common reason |
|---|---|---|
| `NSPrivacyAccessedAPICategoryUserDefaults` | `UserDefaults`, Flutter `shared_preferences`, RN `AsyncStorage` | `CA92.1` app-only data |
| `NSPrivacyAccessedAPICategoryFileTimestamp` | `creationDate`, `modificationDate`, `stat()` | `C617.1` files in app container |
| `NSPrivacyAccessedAPICategorySystemBootTime` | `systemUptime`, `mach_absolute_time()` | `35F9.1` measure elapsed time |
| `NSPrivacyAccessedAPICategoryDiskSpace` | `volumeAvailableCapacityKey`, `statfs()` | `E174.1` check space before writing |
| `NSPrivacyAccessedAPICategoryActiveKeyboards` | `activeInputModes` | `54BD.1` custom keyboard |

The manifest must also be consistent with the **App Privacy** answers in App Store Connect
(`NSPrivacyTracking`, `NSPrivacyTrackingDomains`, `NSPrivacyCollectedDataTypes`).

## How to detect

```bash
find . -name "PrivacyInfo.xcprivacy" -not -path "*/Pods/*" -not -path "*/build/*"
grep -rnE "UserDefaults|NSUserDefaults|shared_preferences|AsyncStorage" --include=*.swift --include=*.m --include=*.dart --include=*.ts .
grep -rnE "systemUptime|mach_absolute_time|volumeAvailableCapacity|statfs|creationDate|modificationDate" --include=*.swift --include=*.m .
```

`scripts/preflight_scan.py` performs both checks and compares used categories with the declared ones.

## Resolution

1. In Xcode: **File ▸ New ▸ File ▸ App Privacy** and add it to the app target (Flutter:
   `ios/Runner/PrivacyInfo.xcprivacy`; React Native/Expo: `ios/<App>/PrivacyInfo.xcprivacy` or the
   `privacyManifests` key in the Expo config).
2. Declare each category with the narrowest approved reason.
3. Update SDKs listed in Apple's *commonly used third-party SDKs* list to versions that include
   their own signed manifests.
4. Generate a privacy report (**Product ▸ Archive ▸ Generate Privacy Report**) and compare it with
   the App Privacy answers in App Store Connect.

```xml
<key>NSPrivacyAccessedAPITypes</key>
<array>
  <dict>
    <key>NSPrivacyAccessedAPIType</key>
    <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
    <key>NSPrivacyAccessedAPITypeReasons</key>
    <array><string>CA92.1</string></array>
  </dict>
</array>
```

## Example rejection

> ITMS-91053: Missing API declaration — Your app's code references one or more APIs that require
> reasons, including NSPrivacyAccessedAPICategoryUserDefaults, but the app's privacy manifest
> doesn't include a declaration for this category.
