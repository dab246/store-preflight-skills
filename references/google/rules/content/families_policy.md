---
id: google.content.families_policy
store: google
category: content
severity: REJECTION
policy: Families policy · Teacher Approved
title: Apps for children that break Families requirements
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/9893335
last_verified: 2026-10-26
---

# Apps for children that break Families requirements

## What to check

When the target audience includes children:

- Only **Families self-certified** ad SDKs and SDKs approved for child-directed use; no
  personalized ads, no advertising ID/`AD_ID` collection from children.
- No transmission of device identifiers, precise location or other restricted data for children.
- Content, ads and IAP prompts are appropriate; no deceptive purchase flows.
- Accurate target audience and content rating; metadata doesn't target children if the app isn't
  designed for them.
- Augmented-reality, social and chat features follow the extra safety rules.

## Resolution

Audit every SDK against the Families list, disable identifiers for child users, and fix the target
audience declaration.

## Example rejection

> Families policy violation. Your app targets children and uses an SDK that is not approved for use
> in child-directed services.
