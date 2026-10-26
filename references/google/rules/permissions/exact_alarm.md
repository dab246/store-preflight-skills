---
id: google.permissions.exact_alarm
store: google
category: permissions
severity: WARNING
policy: Exact alarm permission
title: Exact alarms without a user-facing core need
automated: true
sources:
  - https://developer.android.com/develop/background-work/services/alarms/schedule
  - https://support.google.com/googleplay/android-developer/answer/16558241
last_verified: 2026-10-26
---

# Exact alarms without a user-facing core need

## What to check

- `USE_EXACT_ALARM` is granted automatically and is therefore restricted to **alarm clock and
  calendar** apps whose core function needs exact timing.
- `SCHEDULE_EXACT_ALARM` is user-revocable and denied by default on Android 14+; handle denial.
- Most reminders, syncs and timers work with inexact alarms or WorkManager.

## How to detect

```bash
grep -rnE "USE_EXACT_ALARM|SCHEDULE_EXACT_ALARM|setExact|setAlarmClock" .
```

## Resolution

Prefer `setWindow`/WorkManager; keep `SCHEDULE_EXACT_ALARM` with a settings deep link when exact
timing is user-visible; reserve `USE_EXACT_ALARM` for alarm/calendar apps and declare it.

## Example rejection

> Your app uses the USE_EXACT_ALARM permission but its core functionality is not an alarm clock or
> calendar.
