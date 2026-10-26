---
id: apple.design.user_generated_content
store: apple
category: design
severity: REJECTION
guideline: "1.2 · 1.2.1(a) · 4.7"
title: User-generated and AI-generated content safeguards
automated: false
sources:
  - https://developer.apple.com/app-store/review/guidelines/#1.2
  - https://developer.apple.com/app-store/review/guidelines/#4.7
last_verified: 2026-10-26
---

# User-generated and AI-generated content safeguards

Since 2026-10-16, guideline 1.2 explicitly covers social, UGC, **AI content-creation**, and
random/anonymous chat apps, and failing to remediate violations after notice can be treated as a
Developer Code of Conduct violation.

## What to check

- A method to **filter** objectionable material before it is posted.
- A way to **report** offensive content and timely responses to reports.
- The ability to **block** abusive users.
- Published **contact information**.
- Measures to prevent and remove nonconsensual intimate imagery, including AI-generated.
- Creator apps: a way to flag content above the app's age rating and age-gate it (1.2.1(a)).
- Mini apps, chatbots, plug-ins (4.7): same moderation, privacy and payment rules apply.

## How to detect

Create two test accounts, post content, and confirm report, block and moderation flows work end to
end. Search for report/block UI in code.

## Resolution

Add report/block actions on every content surface, a moderation queue or filter, an EULA with
zero-tolerance terms accepted at sign-up, and a support contact.

## Example rejection

> Guideline 1.2 - Safety - User-Generated Content. Your app enables the display of user-generated
> content but does not have the proper precautions in place.
