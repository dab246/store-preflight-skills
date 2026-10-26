---
id: google.content.anonymous_chat
store: google
category: content
severity: REJECTION
policy: Age-Restricted Content and Functionality · Child Safety Standards · Families
title: Anonymous or random chat apps without age restrictions and child-safety standards
automated: false
sources:
  - https://developer.android.com/distribute/play-policies
  - https://support.google.com/googleplay/android-developer/answer/14747720
last_verified: 2026-10-26
---

# Anonymous or random chat apps

Since **2026-08-26**, Google applies the Age-Restricted Content and Functionality policy and the
Child Safety Standards policy to **anonymous chat and random chat apps**, and the Families policy
prohibits such apps from targeting children.

## What to check

- Target audience in Play Console excludes children; the app is not in the Families program.
- Age restriction/assurance appropriate to the content (Play Age Signals API data may only be used to
  provide age-appropriate experiences in the receiving app — since 2026-01-01).
- Published child sexual abuse and exploitation (CSAE) standards, an in-app feedback mechanism,
  a designated contact, and compliance with reporting laws (Child Safety Standards declaration).
- UGC moderation, reporting and blocking (see `user_generated_content.md`).

## Resolution

Complete the Child Safety Standards declaration, set the target audience to adults, add age
assurance, and publish the standards page.

## Example rejection

> Age-Restricted Content and Functionality policy violation. Your app offers anonymous or random chat
> functionality without appropriate age restrictions.
