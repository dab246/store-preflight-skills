---
id: google.content.ai_generated_content
store: google
category: content
severity: REJECTION
policy: AI-Generated Content
title: Generative AI without safeguards or user reporting
automated: partial
sources:
  - https://support.google.com/googleplay/android-developer/answer/13985936
last_verified: 2026-10-26
---

# Generative AI without safeguards or user reporting

## What to check

Apps that generate content with AI (text, image, audio, video, chat companions) must:

- Prevent generation of **restricted content**: sexual content involving minors, nonconsensual
  intimate imagery, content that facilitates deception or harm, and anything else prohibited by
  Play's content policies.
- Provide **in-app reporting/flagging** of offensive output without leaving the app, and use reports
  to improve filtering.
- Not market prohibited uses (e.g. "undress" apps) in metadata or ads.
- Disclose data sent to AI processors in the Data safety form and privacy policy, with prominent
  disclosure where users wouldn't expect it.
- Anonymous/random AI chat features also follow the Age-Restricted Content rules (see
  `anonymous_chat.md`).

## How to detect

The scanner flags generic hosted-model API shapes; add provider hosts in
`.store-preflight.json → ai_endpoints`. Then locate every AI surface in the UI and confirm a report
action exists on each.

## Resolution

Add a "Report" action on each AI response/asset, apply input and output safety filters, and document
both in the review notes.

## Example rejection

> AI-Generated Content policy violation. Your app does not provide an in-app mechanism for users to
> report or flag offensive AI-generated content.
