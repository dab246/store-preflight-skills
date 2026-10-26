---
id: google.privacy.prominent_disclosure
store: google
category: privacy
severity: REJECTION
policy: User Data · Prominent disclosure and consent
title: Personal or sensitive data collected without prominent disclosure
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/10144311
  - https://support.google.com/googleplay/android-developer/answer/11150561
last_verified: 2026-10-26
---

# Personal or sensitive data collected without prominent disclosure

## What to check

When data collection is not reasonably expected by users (background location, contacts upload,
installed apps list, accessibility data, sending content to third-party AI, SMS/call logs), the app
shows an **in-app disclosure before the runtime prompt** that:

- appears during normal use, not only in the privacy policy or settings;
- describes the data, how it is used and shared;
- requires an affirmative action ("Agree") — dismissing or navigating away is not consent;
- does not bundle unrelated disclosures or include other content.

## How to detect

Walk through each permission request and data upload; record the screen preceding each one.

## Resolution

Add a dedicated disclosure dialog per data type and gate collection on explicit consent.

## Example rejection

> Your app collects personal and sensitive user data without a prominent in-app disclosure and
> consent.
