---
id: google.permissions.request_install_packages
store: google
category: permissions
severity: REJECTION
policy: Use of the REQUEST_INSTALL_PACKAGES permission
title: REQUEST_INSTALL_PACKAGES without a qualifying use case
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/12085295
last_verified: 2026-10-26
---

# REQUEST_INSTALL_PACKAGES without a qualifying use case

## What to check

Only apps whose core functionality includes sending, receiving or installing packages (file
managers, browsers, enterprise device management, backup/restore, device migration) may request it.
Self-updating outside Play is prohibited (Device and Network Abuse policy).

## How to detect

```bash
grep -rn "REQUEST_INSTALL_PACKAGES" --include=AndroidManifest.xml .
grep -rnE "application/vnd.android.package-archive|PackageInstaller" --include=*.kt --include=*.java .
```

## Resolution

Remove the permission and any in-app updater; use the Play In-App Updates API instead.

## Example rejection

> Your app requests the REQUEST_INSTALL_PACKAGES permission, but the declared use case is not
> permitted.
