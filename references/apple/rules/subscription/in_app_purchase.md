---
id: apple.subscription.in_app_purchase
store: apple
category: subscription
severity: REJECTION
guideline: "3.1.1 · 3.1.1(a) · 3.1.3"
title: Digital goods sold outside In-App Purchase
automated: partial
sources:
  - https://developer.apple.com/app-store/review/guidelines/#3.1.1
  - https://developer.apple.com/in-app-purchase/
last_verified: 2026-10-26
---

# Digital goods sold outside In-App Purchase

## What to check

- Digital content, subscriptions, premium features, virtual currency and "boosts" are sold with
  **In-App Purchase** (3.1.1). License keys, QR codes or crypto cannot unlock features.
- Links or buttons to external purchase pages are only allowed where an entitlement or storefront
  rule permits them (3.1.1(a): StoreKit External Purchase Link entitlement, region-specific; the US
  storefront allows links), and they must go to a permitted destination.
- Exceptions (3.1.3): reader apps, multiplatform services (if IAP is also offered), enterprise,
  person-to-person real-time services, **physical goods and services consumed outside the app**
  (which must *not* use IAP), free companion apps.
- A **Restore Purchases** control exists for non-consumables and subscriptions.
- Loot boxes disclose odds before purchase.

## How to detect

```bash
grep -rnE "Stripe|Braintree|PayPal|razorpay|checkout|/pricing|/upgrade" --include=*.swift --include=*.dart --include=*.ts* .
```

Then classify each purchase: digital (IAP) vs physical/service (external allowed).

## Resolution

Move digital purchases to StoreKit 2; keep external payments for physical goods; apply for the
relevant entitlement before linking out; add a restore button.

## Example rejection

> Guideline 3.1.1 - Business - Payments - In-App Purchase. Your app unlocks or enables additional
> functionality with mechanisms other than In-App Purchase.
