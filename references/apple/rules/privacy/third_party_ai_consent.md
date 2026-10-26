---
id: apple.privacy.third_party_ai_consent
store: apple
category: privacy
severity: REJECTION
guideline: "5.1.2(i)"
title: Personal data sent to a third-party AI service without consent
automated: partial
sources:
  - https://developer.apple.com/app-store/review/guidelines/#5.1.2
last_verified: 2026-10-26
---

# Personal data sent to a third-party AI service without consent

## What to check

Guideline 5.1.2(i) requires apps to **clearly disclose where personal data will be shared with
third parties, including third-party AI**, and to obtain explicit permission first.

- Prompts, chat history, photos, voice, documents or any user content that leaves the device for a
  hosted model counts — even when it goes through your own backend first.
- The disclosure names the provider (or provider category) and what is sent, and appears **before
  the first request**, not only in the privacy policy.
- Users can decline and still use non-AI parts of the app.
- The App Privacy answers and privacy policy list the AI processor.

## How to detect

The scanner flags generic hosted-model API shapes (`/v1/chat/completions`, `:generateContent`,
`/v1/messages`, LLM client classes). Add provider-specific hosts and SDK names for your project in
`.store-preflight.json → ai_endpoints`. Then trace every call site back to the UI that triggers it
and confirm a consent step precedes it.

## Resolution

1. Add a one-time consent sheet: provider, data sent, purpose, retention, a link to the policy, and
   **Allow / Not now** buttons. Persist the choice and offer a toggle in Settings.
2. Gate every AI request on that consent.
3. Mention the consent screen and its location in the Notes for Review.

## Example rejection

> Guideline 5.1.2(i) - Legal - Privacy - Data Use and Sharing. The app shares the user's personal
> data with a third-party AI service but the app does not clearly explain what data is sent, identify
> who the data is sent to, and ask the user's permission before sharing the data.
