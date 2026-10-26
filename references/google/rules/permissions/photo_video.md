---
id: google.permissions.photo_video
store: google
category: permissions
severity: REJECTION
policy: Photo and Video Permissions
title: READ_MEDIA_IMAGES / READ_MEDIA_VIDEO for one-off media access
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/14115180
  - https://developer.android.com/training/data-storage/shared/photopicker
last_verified: 2026-10-26
---

# READ_MEDIA_IMAGES / READ_MEDIA_VIDEO for one-off media access

## What to check

Only apps whose core purpose needs persistent, broad access to photos/videos (galleries, photo
editors, backup) may keep `READ_MEDIA_IMAGES` / `READ_MEDIA_VIDEO` with an approved declaration.
Profile pictures, attachments and one-off uploads must use the **system photo picker**.

## How to detect

```bash
grep -rnE "READ_MEDIA_(IMAGES|VIDEO)|READ_EXTERNAL_STORAGE" --include=AndroidManifest.xml .
grep -rnE "PickVisualMedia|image_picker|expo-image-picker" .
```

## Resolution

Use `ActivityResultContracts.PickVisualMedia` (backported via Google Play services), remove the
permissions (also SDK-merged ones), or submit the declaration if you qualify.

## Example rejection

> Your app's use of the photo and video permissions is not directly related to the core purpose of
> the app. Use the Android photo picker.
