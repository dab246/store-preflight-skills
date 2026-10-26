---
id: google.content.user_generated_content
store: google
category: content
severity: REJECTION
policy: User Generated Content
title: UGC without terms, moderation, reporting and blocking
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/9876937
last_verified: 2026-10-26
---

# UGC without terms, moderation, reporting and blocking

## What to check

- Users accept terms of use/policy that define objectionable content **before** creating or uploading
  UGC.
- Robust, ongoing moderation proportionate to the content.
- In-app **reporting** of content and users, and **blocking** of users.
- Safeguards against monetizing objectionable content; extra measures where minors can be present.
- Apps whose primary purpose is objectionable UGC are not allowed.

## How to detect

With two test accounts, post content, report it and block the other user.

## Resolution

Add terms acceptance at sign-up, a moderation pipeline, and report/block actions on every content
surface.

## Example rejection

> User Generated Content policy violation. Your app does not have an in-app system for reporting
> objectionable UGC and users.
