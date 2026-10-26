---
id: google.privacy.data_safety_form
store: google
category: privacy
severity: REJECTION
policy: User Data · Data safety section
title: Data safety form that doesn't match the app and its SDKs
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/10787469
  - https://support.google.com/googleplay/android-developer/answer/10144311
last_verified: 2026-10-26
---

# Data safety form that doesn't match the app

## What to check

- Every data type collected or shared — by your code **and every SDK** (analytics, crash reporting,
  ads, attribution, AI services, payments) — is declared with purpose, optional/required and
  sharing status.
- Precise vs approximate location is declared correctly (Google clarified this in July 2026).
- Encryption in transit and the account-deletion URL are declared accurately.
- A **privacy policy** link is set in Play Console and accessible inside the app; it names the
  developer, the data, the purposes and the deletion process.
- The form is submitted for every track (internal testing excluded) and kept in sync after each
  release that adds an SDK or permission.

## How to detect

List SDKs from `./gradlew :app:dependencies` and `pubspec.lock` / `package-lock.json`, then compare
against each SDK's own Data safety guidance and the current Play Console form. Compare manifest
permissions with declared data types.

## Resolution

Update the form, the privacy policy and the in-app disclosures together; re-submit before
publishing the release that changes data handling.

## Example rejection

> Invalid Data safety section. Your app collects or shares user data that has not been disclosed
> in the Data safety form.
