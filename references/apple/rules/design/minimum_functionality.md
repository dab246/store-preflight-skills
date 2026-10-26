---
id: apple.design.minimum_functionality
store: apple
category: design
severity: REJECTION
guideline: "4.2 · 4.3 · 4.1"
title: Minimum functionality, spam and copycats
automated: false
sources:
  - https://developer.apple.com/app-store/review/guidelines/#4.2
  - https://developer.apple.com/app-store/review/guidelines/#4.3
last_verified: 2026-10-26
---

# Minimum functionality, spam and copycats

## What to check

- **Web wrappers (4.2):** the app is more than a website in a `WKWebView`. Add native value:
  offline use, push, device features, native navigation.
- **Marketing / link collections (4.2.2)** and apps that need another app to work (4.2.3) are rejected.
- **Spam (4.3(a)):** one Bundle ID per app concept — don't ship white-label copies; use in-app
  configuration or IAP for variations.
- **Saturated categories (4.3(b)):** dating, flashlight, wallpaper, fortune telling, simple timers,
  sound boards need a clearly better experience.
- **Copycats (4.1):** no imitation of popular apps' names, icons or UI.
- **Template apps (4.2.6):** generated from a commercial template service only when submitted by the
  content provider.

## How to detect

```bash
grep -rnE "WKWebView|webview_flutter|react-native-webview|InAppWebView" --include=*.swift --include=*.dart --include=*.tsx .
```

Count native screens versus web screens and describe the native value in the review notes.

## Resolution

Add native features that justify an app, merge duplicate apps, and differentiate design and naming.

## Example rejection

> Guideline 4.2 - Design - Minimum Functionality. Your app provides a limited user experience as it is
> not sufficiently different from a mobile browsing experience.
