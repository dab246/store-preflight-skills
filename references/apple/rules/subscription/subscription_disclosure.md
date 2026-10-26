---
id: apple.subscription.subscription_disclosure
store: apple
category: subscription
severity: REJECTION
guideline: "3.1.2 · 3.1.2(a) · 3.1.2(c) · 5.1.1(i)"
title: Incomplete subscription disclosure, misleading pricing, missing Terms/Privacy links
automated: false
sources:
  - https://developer.apple.com/app-store/review/guidelines/#3.1.2
  - https://developer.apple.com/app-store/subscriptions/
last_verified: 2026-10-26
---

# Incomplete subscription disclosure and misleading pricing

## What to check

**Paywall (in app)**

- Subscription title, length of each period, and price (plus price per unit if shown).
- The **billed amount is the most prominent price**. A calculated monthly price may appear only as
  secondary text ("$59.99/year — that's $5.00/month").
- Free trials state duration, what happens at the end and the price charged afterwards.
- Functional links to **Terms of Use (EULA)** and **Privacy Policy**.
- A close button that is visible and works; no fake countdowns; no pre-selected upsells that hide the
  cheaper option.
- Restore Purchases.

**Metadata (App Store Connect)**

- Privacy Policy URL field filled.
- Terms of Use link in the description, or a custom EULA in App Store Connect.

**Model rules (3.1.2(a))**

- Minimum period 7 days; ongoing value; works on all of the user's devices where the app is available.
- Don't remove features people already paid for when switching to subscriptions.

## How to detect

Screenshot the paywall and check each item. Search the description for "Terms" and "Privacy".

## Resolution

Restructure the paywall price hierarchy, add both links in the app and in metadata, and describe the
trial terms clearly.

## Example rejection

> Guideline 3.1.2 - Business - Payments - Subscriptions. The submission did not include all the
> required information for apps offering auto-renewable subscriptions: a functional link to the Terms
> of Use (EULA) in the app's metadata.
