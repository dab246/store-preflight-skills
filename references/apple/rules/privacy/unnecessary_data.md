---
id: apple.privacy.unnecessary_data
store: apple
category: privacy
severity: REJECTION
guideline: "5.1.1(i)–(iii) · 5.1.1(x)"
title: Requiring personal data that the feature does not need
automated: false
sources:
  - https://developer.apple.com/app-store/review/guidelines/#5.1.1
last_verified: 2026-10-26
---

# Requiring personal data that the feature does not need

## What to check

- Sign-up and onboarding forms only **require** fields essential to the core function. Name,
  email, phone, birthday, gender, etc. must be optional unless the feature truly needs them (5.1.1(x)).
- No "allow notifications / location / tracking to continue" gates (5.1.2).
- Apps that don't need an account let people use non-account features first (5.1.1(v)).
- A privacy policy is linked in App Store Connect **and** inside the app (5.1.1(i)).

## How to detect

Walk through first launch and sign-up. List every field and permission requested before the user
reaches the main feature and justify each one.

## Resolution

Mark non-essential fields optional, defer permission prompts to the moment they are needed, and allow
guest access where possible.

## Example rejection

> Guideline 5.1.1 - Legal - Privacy - Data Collection and Storage. The app requires users to provide
> personal information, such as date of birth and gender, that is not directly relevant to the app's
> core functionality.
