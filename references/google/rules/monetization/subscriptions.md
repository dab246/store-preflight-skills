---
id: google.monetization.subscriptions
store: google
category: monetization
severity: REJECTION
policy: Subscriptions
title: Unclear subscription offers, trials or cancellation
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/9900533
last_verified: 2026-10-26
---

# Unclear subscription offers, trials or cancellation

## What to check

- The offer clearly states **price, billing frequency, what's included**, and that it auto-renews.
- Free trials and intro offers state the **duration, the price after the trial**, and how to cancel.
- The billed price is more prominent than any per-period equivalent or "savings".
- The paywall can be dismissed; no misleading designs (hidden close button, pre-checked upsells).
- Users can manage/cancel easily — link to the Play subscription center
  (`https://play.google.com/store/account/subscriptions?sku=…&package=…`).
- Content that users paid for is not removed without notice.

## How to detect

Screenshot every paywall variant (A/B tests, regions) and check each item above.

## Resolution

Rework the paywall copy and layout; add a "Manage subscription" link in Settings.

## Example rejection

> Subscriptions policy violation. Your app's subscription offer does not clearly disclose the terms
> of the subscription, including the price and billing frequency.
