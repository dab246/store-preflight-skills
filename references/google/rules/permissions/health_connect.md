---
id: google.permissions.health_connect
store: google
category: permissions
severity: WARNING
policy: Health Connect permissions · Health apps declaration
title: Health data access without matching declarations
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/12991134
  - https://support.google.com/googleplay/android-developer/answer/14738291
last_verified: 2026-10-26
---

# Health data access without matching declarations

## What to check

- Every app must complete the **Health apps declaration** in Play Console ▸ App content (answer
  "no health features" if that's accurate).
- Apps reading/writing Health Connect data request only the data types their features use, submit
  the Health Connect declaration with justification per type, show a privacy policy screen inside the
  Health Connect permission flow, and never use health data for ads or sell it.
- Medical/diagnostic claims require the relevant regulatory clearance and disclaimers.

## How to detect

```bash
grep -rn "android.permission.health." --include=AndroidManifest.xml .
grep -rnE "HealthConnectClient|health_connect|react-native-health-connect" .
```

## Resolution

Trim data types, complete both declarations, add the rationale activity
(`ACTION_SHOW_PERMISSIONS_RATIONALE`), and align the Data safety form.

## Example rejection

> Your app requests Health Connect permissions that are not necessary for the declared features.
