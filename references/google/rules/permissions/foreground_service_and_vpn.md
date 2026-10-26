---
id: google.permissions.foreground_service_and_vpn
store: google
category: permissions
severity: WARNING
policy: Foreground service permissions · VpnService
title: Undeclared foreground-service types or VpnService misuse
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/13392821
  - https://support.google.com/googleplay/android-developer/answer/12564964
  - https://developer.android.com/develop/background-work/services/fgs/service-types
last_verified: 2026-10-26
---

# Undeclared foreground-service types or VpnService misuse

## What to check

**Foreground services (Android 14+)**

- Every `<service>` started in the foreground declares `android:foregroundServiceType` and the
  matching `FOREGROUND_SERVICE_*` permission.
- Play Console ▸ App content ▸ **Foreground service permissions**: describe each type, its user
  impact, and attach a video.
- The task is user-noticeable and can't be deferred/interrupted; otherwise use WorkManager or
  user-initiated data transfer jobs.
- **From 2027-01-27 geofencing is removed** as an approved FGS use case — use the Geofence API.

**VpnService**

- Only apps whose core functionality is a VPN may use `VpnService`; declare it in Play Console,
  encrypt traffic, don't collect personal data or manipulate ads, and disclose data handling.

## How to detect

```bash
grep -rnE "foregroundServiceType|FOREGROUND_SERVICE_|startForeground|BIND_VPN_SERVICE|VpnService" .
```

## Resolution

Declare types and permissions, complete the declarations with videos, migrate deferrable work to
WorkManager.

## Example rejection

> Your app uses the foreground service permission FOREGROUND_SERVICE_LOCATION, but the declared use
> case is not permitted for this type.
