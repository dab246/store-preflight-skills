---
id: google.permissions.all_files_access
store: google
category: permissions
severity: REJECTION
policy: Use of All files access (MANAGE_EXTERNAL_STORAGE)
title: All files access without a qualifying core use case
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/10467955
last_verified: 2026-10-26
---

# All files access without a qualifying core use case

## What to check

`MANAGE_EXTERNAL_STORAGE` is restricted to apps whose core purpose needs broad file access: file
managers, backup and restore, anti-virus, document management, on-device search, disk/file
encryption, device migration. Media apps, editors and downloaders do **not** qualify.

## How to detect

```bash
grep -rn "MANAGE_EXTERNAL_STORAGE" --include=AndroidManifest.xml .
```

## Resolution

Use the Storage Access Framework, MediaStore or the photo picker, or app-specific storage. If you
qualify, complete the declaration in Play Console ▸ App content.

## Example rejection

> Your app does not qualify for use of the All files access permission. Remove the permission or
> submit a declaration demonstrating a qualifying use case.
