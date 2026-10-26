---
id: google.metadata.store_listing
store: google
category: metadata
severity: REJECTION
policy: Metadata · Store listing and promotion
title: Store listing over limits or with misleading/promotional metadata
automated: partial
sources:
  - https://support.google.com/googleplay/android-developer/answer/9898842
  - https://support.google.com/googleplay/android-developer/answer/9859152
last_verified: 2026-10-26
---

# Store listing over limits or with misleading/promotional metadata

## What to check

| Field | Limit |
|---|---|
| App name (title) | 30 |
| Short description | 80 |
| Full description | 4000 |

- Title, icon and developer name don't contain **performance or ranking claims** ("best", "#1",
  "top"), **price or promotion** ("free", "sale", "-50%"), **calls to action** ("download now"),
  emoji, emoticons, repeated special characters, or ALL CAPS (unless part of the brand).
- No keyword stuffing, unattributed user testimonials, or irrelevant references to other platforms
  or stores ("iPhone", "App Store").
- No impersonation of other apps, brands or Google products; trademarks only with permission.
- Screenshots and feature graphic show the actual app; icon follows the icon spec (512×512, no
  misleading badges).
- Content rating questionnaire, target audience and category are accurate.

## How to detect

Run `scripts/preflight_scan.py --metadata <dir>` on per-locale `title.txt`, `short_description.txt`,
`full_description.txt` (pull them with the official
[Google Play Developer API](https://developers.google.com/android-publisher) edits endpoints). Review
graphics manually.

## Resolution

Rewrite fields to describe features plainly, move promotions to promotional content, and replace
non-app screenshots.

## Example rejection

> Metadata policy violation. Your app's title contains words that are prohibited in the title, such
> as "best" or "free".
