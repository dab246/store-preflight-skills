---
id: google.technical.sixteen_kb_page_size
store: google
category: technical
severity: REJECTION
policy: 16 KB memory page size compatibility
title: Native libraries not aligned for 16 KB page sizes
automated: true
sources:
  - https://developer.android.com/guide/practices/page-sizes
last_verified: 2026-10-26
---

# Native libraries not aligned for 16 KB page sizes

## What to check

Apps targeting **Android 15 (API 35) and higher** must support 16 KB memory pages on 64-bit devices.
From **2027-02-01**, updates that don't support 16 KB page sizes cannot be released. Pure
Kotlin/Java apps are already compatible; any `.so` file — your own or from an SDK (game engines,
media, crypto, ML, database, Flutter/React Native) — must have `PT_LOAD` segments aligned to 16 KB
and be stored uncompressed and 16 KB-zip-aligned.

## How to detect

- Play Console ▸ App bundle explorer ▸ **Memory page size** column.
- Android Studio APK Analyzer shows alignment warnings.
- Command line:

```bash
unzip -o app-release.apk 'lib/*' -d /tmp/apk
for so in /tmp/apk/lib/arm64-v8a/*.so; do
  llvm-objdump -p "$so" | awk '/LOAD/ {print FILENAME": "$NF}' FILENAME="$so"
done   # every value must be 2**14 or larger
zipalign -c -P 16 -v 4 app-release.apk
```

`scripts/preflight_scan.py` reads the ELF headers of `.so` files committed to the repository.

## Resolution

- AGP **8.5.1+** (16 KB zip alignment for uncompressed libraries), NDK **r28+** (16 KB ELF alignment
  by default); for older NDKs add `-Wl,-z,max-page-size=16384`.
- Update SDKs/plugins that ship prebuilt libraries.
- Test on a 16 KB emulator image.

## Example rejection

> Your app does not support 16 KB memory page sizes. Recompile your app with support for 16 KB
> page sizes to release updates.
