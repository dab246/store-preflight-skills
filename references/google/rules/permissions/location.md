---
id: google.permissions.location
store: google
category: permissions
severity: WARNING
policy: Location Permissions (incl. background location)
title: Location access broader than the feature needs
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/9799150
  - https://developer.android.com/distribute/play-policies
last_verified: 2026-10-26
---

# Location access broader than the feature needs

## What to check

- **Background location** (`ACCESS_BACKGROUND_LOCATION`): needs a Play Console declaration, a
  short video of the feature, an in-app **prominent disclosure** before the runtime prompt, and a
  core feature that clearly benefits users (navigation, family safety, fitness tracking, etc.).
- **Precise vs approximate:** request `ACCESS_COARSE_LOCATION` unless precision is essential.
  From **2027-01-27** the Location Permissions policy introduces the **location button** as the
  recommended minimum scope for precise location.
- **Geofencing:** from 2027-01-27 geofencing is no longer an approved foreground-service use case —
  use the Geofence API.
- Data safety declarations distinguish precise from approximate location (clarified July 2026).

## How to detect

```bash
grep -rnE "ACCESS_(FINE|COARSE|BACKGROUND)_LOCATION" --include=AndroidManifest.xml .
grep -rnE "requestLocationUpdates|FusedLocationProvider|GeofencingClient" --include=*.kt --include=*.java .
```

## Resolution

Downgrade to coarse/foreground location where possible, add the prominent disclosure, record the
declaration video, and align the Data safety form.

## Example rejection

> Your app's declared feature does not meet the requirements for access to location in the
> background.
