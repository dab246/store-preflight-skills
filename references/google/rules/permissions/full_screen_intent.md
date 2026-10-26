---
id: google.permissions.full_screen_intent
store: google
category: permissions
severity: WARNING
policy: Full-screen intent permission
title: USE_FULL_SCREEN_INTENT outside calling and alarm apps
automated: true
sources:
  - https://developer.android.com/about/versions/14/behavior-changes-14
  - https://support.google.com/googleplay/android-developer/answer/16558241
last_verified: 2026-10-26
---

# USE_FULL_SCREEN_INTENT outside calling and alarm apps

## What to check

On Android 14+, Play only grants `USE_FULL_SCREEN_INTENT` by default to apps whose core
functionality is **calling or alarms**, declared in Play Console. Other apps lose the permission and
their full-screen notifications are shown as heads-up notifications.

## How to detect

```bash
grep -rnE "USE_FULL_SCREEN_INTENT|setFullScreenIntent" .
```

## Resolution

Remove it, or declare the calling/alarm use case; check `NotificationManager.canUseFullScreenIntent()`
at runtime.

## Example rejection

> Your app's declared use of the full-screen intent permission does not match its core
> functionality.
