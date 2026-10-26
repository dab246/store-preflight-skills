---
id: apple.privacy.purpose_strings
store: apple
category: privacy
severity: REJECTION
guideline: "5.1.1(ii) · ITMS-90683"
title: Missing or vague permission purpose strings
automated: true
sources:
  - https://developer.apple.com/app-store/review/guidelines/#5.1.1
  - https://developer.apple.com/documentation/bundleresources/information-property-list
last_verified: 2026-10-26
---

# Missing or vague permission purpose strings

## What to check

- Every protected resource the app (or an SDK) touches has its `NS…UsageDescription` key in
  `Info.plist`. A missing key fails upload (`ITMS-90683`) and crashes at runtime.
- Each string explains **what** is accessed, **why**, and ideally gives an example. Strings such as
  "Need camera" or "This app requires access" are rejected under 5.1.1(ii).
- The system prompt is not preceded by a custom screen that discourages or forces a choice
  (no "Allow" button that only leads to the system prompt, no blocking the app when denied unless
  the feature is impossible without it).

| Key | Triggered by |
|---|---|
| `NSCameraUsageDescription` | `AVCaptureDevice`, camera pickers |
| `NSPhotoLibraryUsageDescription` / `NSPhotoLibraryAddUsageDescription` | `PHPhotoLibrary` (not needed for `PHPickerViewController`) |
| `NSLocationWhenInUseUsageDescription` (+ `NSLocationAlwaysAndWhenInUseUsageDescription`) | `CLLocationManager` |
| `NSMicrophoneUsageDescription` | `AVAudioRecorder`, recording sessions |
| `NSContactsUsageDescription` | `CNContactStore` |
| `NSCalendarsFullAccessUsageDescription` / `NSCalendarsWriteOnlyAccessUsageDescription` | `EKEventStore` |
| `NSFaceIDUsageDescription` | `LAContext` biometrics |
| `NSBluetoothAlwaysUsageDescription` | CoreBluetooth |
| `NSHealthShareUsageDescription` / `NSHealthUpdateUsageDescription` | HealthKit |
| `NSUserTrackingUsageDescription` | App Tracking Transparency |

## How to detect

```bash
plutil -p ios/Runner/Info.plist | grep UsageDescription
grep -rnE "AVCaptureDevice|CLLocationManager|CNContactStore|EKEventStore|LAContext|PHPhotoLibrary" --include=*.swift .
```

Also check localized `InfoPlist.strings` files: an empty translation is as bad as a missing key.

## Resolution

Write strings that a reviewer can verify in the UI:

> "Scan receipts with your camera so we can fill in the amount and date for you."

## Example rejection

> Guideline 5.1.1(ii) - Legal - Privacy - Data Collection and Storage. The app's permission request
> does not sufficiently explain the use of protected resources. Update the purpose string to clearly
> and completely describe the app's use of the data, including an example.
