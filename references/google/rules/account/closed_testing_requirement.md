---
id: google.account.closed_testing_requirement
store: google
category: account
severity: REJECTION
policy: App testing requirements for new personal developer accounts
title: Production access requested before the closed test requirement is met
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/14151465
last_verified: 2026-10-26
---

# Closed testing requirement for new personal accounts

## What to check

Newly created **personal** developer accounts must run a **closed test with at least 12 testers who
have been opted in for at least the last 14 days continuously** before applying for production
access. Organization accounts are not subject to this requirement.

- Testers actually install and use the app; collect feedback.
- The production-access application describes the test, feedback received and changes made.

## Resolution

Start the closed test early in the release plan; keep at least 12 opted-in testers for the whole
window; answer the application questions with specifics.

## Example rejection

> Your app doesn't meet the requirements for production access. Make sure your closed test has at
> least 12 testers who have been opted in for the last 14 days.
