---
id: google.monetization.play_billing
store: google
category: monetization
severity: REJECTION
policy: Payments
title: Digital goods sold outside Google Play Billing
automated: partial
sources:
  - https://support.google.com/googleplay/android-developer/answer/9858738
  - https://support.google.com/googleplay/android-developer/answer/15582165
last_verified: 2026-10-26
---

# Digital goods sold outside Google Play Billing

## What to check

- In-app purchases of **digital goods and services** (premium features, subscriptions, virtual
  currency, content) use **Google Play Billing**, unless the app is enrolled in a program that
  permits alternatives in that region (e.g. user choice billing, alternative billing or external
  offers programs) and follows its UX rules.
- **United States:** Google has a separate page for US-specific billing and linking rules following
  the Epic litigation (settlement agreement 2026-03-04); read it before linking to web checkout —
  Google states the current policies and programs remain in effect until it announces changes.
- Physical goods, real-world services, peer-to-peer payments, and some content consumed outside the
  app may use other payment methods.
- Loot boxes and randomized items disclose odds before purchase.

## How to detect

```bash
grep -rnE "Stripe|Braintree|PayPal|razorpay|checkout|/pricing" --include=*.kt --include=*.java --include=*.dart --include=*.ts* .
```

## Resolution

Route digital purchases through Play Billing (PBL 8+), enroll in the relevant program before
offering alternatives, and keep external payments for physical goods/services.

## Example rejection

> Payments policy violation. Your app offers digital goods or services without using Google Play's
> billing system.
