---
id: google.permissions.sms_call_log
store: google
category: permissions
severity: REJECTION
policy: Use of SMS or Call Log permission groups
title: SMS and Call Log permissions without an approved use case
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/10208820
  - https://developer.android.com/distribute/play-policies
last_verified: 2026-10-26
---

# SMS and Call Log permissions without an approved use case

## What to check

`READ_SMS`, `RECEIVE_SMS`, `SEND_SMS`, `RECEIVE_MMS`, `RECEIVE_WAP_PUSH`, `READ_CALL_LOG`,
`WRITE_CALL_LOG`, `PROCESS_OUTGOING_CALLS` are only allowed when the app is the **default SMS,
Phone or Assistant handler**, or qualifies for a listed exception, and the Permissions Declaration
Form is approved.

- **From 2027-01-27:** account verification via phone call is **no longer** an allowed use case for
  `READ_CALL_LOG`. Use the Digital Credentials API (directly or through a verification provider) or
  the SMS Retriever API.
- OTP auto-fill never justifies SMS permissions — use SMS Retriever or SMS User Consent.
- Permissions pulled in by SDKs count; check the **merged** manifest.

## How to detect

```bash
./gradlew :app:processReleaseManifest && grep -E "SMS|CALL_LOG|OUTGOING_CALLS" app/build/intermediates/merged_manifests/release/*/AndroidManifest.xml
```

## Resolution

Remove the permissions (use `tools:node="remove"` for SDK-merged ones) or become the default
handler and submit the declaration form.

## Example rejection

> Your app is requesting access to SMS or Call Log permissions, but your declared core functionality
> is not an approved use case for this access.
