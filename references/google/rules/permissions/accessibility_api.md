---
id: google.permissions.accessibility_api
store: google
category: permissions
severity: REJECTION
policy: Use of the AccessibilityService API
title: AccessibilityService used for non-accessibility purposes
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/10964491
last_verified: 2026-10-26
---

# AccessibilityService used for non-accessibility purposes

## What to check

- Apps declaring `isAccessibilityTool="true"` must be designed primarily for people with
  disabilities.
- Other uses need a Play Console declaration, a **prominent disclosure and consent** before
  enabling, and must not change settings, bypass privacy controls, or perform remote calls.
- Never used to collect data covertly or to automate other apps without explicit user intent.

## How to detect

```bash
grep -rnE "BIND_ACCESSIBILITY_SERVICE|AccessibilityService|isAccessibilityTool" .
```

## Resolution

Remove the service or document the use case, add the disclosure screen and video, and file the
declaration.

## Example rejection

> Your app uses the AccessibilityService API without the required prominent disclosure and
> declaration.
