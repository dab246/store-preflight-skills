---
id: apple.technical.sdk_requirements
store: apple
category: technical
severity: REJECTION
guideline: "Upload requirements · 2.5.1"
title: Build SDK, Xcode and minimum OS requirements
automated: partial
sources:
  - https://developer.apple.com/news/upcoming-requirements/
last_verified: 2026-10-26
---

# Build SDK, Xcode and minimum OS requirements

Values below mirror `references/apple/requirements.json`, which the weekly policy sync updates.

## What to check

- Since **2026-04-28**, uploads must be built with **Xcode 26+** and the **iOS/iPadOS/tvOS/visionOS/
  watchOS 26 SDK** or later. Older toolchains fail at upload, not at review.
- Since **2026-09-09**, iOS and iPadOS apps must **target iOS 13 or later** (deployment target).
- Age rating questionnaire answers are up to date (required since 2026-01-31 to submit updates).
- EU: DSA trader status is provided.
- macOS: no `com.apple.quarantine` attribute on bundled files.

## How to detect

```bash
xcodebuild -version
grep -rn "IPHONEOS_DEPLOYMENT_TARGET" ios/*.xcodeproj/project.pbxproj *.xcodeproj/project.pbxproj 2>/dev/null
grep -n "platform :ios" ios/Podfile Podfile 2>/dev/null
```

CI images: check the Xcode version selected by your CI provider.

## Resolution

Upgrade Xcode, raise the deployment target in the project, Podfile and Flutter/RN config, and
re-archive.

## Example rejection

> ITMS-90725: SDK version issue - This app was built with the iOS 18.x SDK. All iOS and iPadOS apps
> must be built with the iOS 26 SDK or later, included in Xcode 26 or later.
