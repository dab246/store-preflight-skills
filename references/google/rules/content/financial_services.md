---
id: google.content.financial_services
store: google
category: content
severity: REJECTION
policy: Financial Services · Personal loans · Crypto
title: Financial features without declarations, licenses or required disclosures
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/9876821
last_verified: 2026-10-26
---

# Financial features without declarations, licenses or required disclosures

## What to check

- The **Financial features declaration** in Play Console is complete for every app (even with no
  financial features).
- **Personal loans:** listing discloses minimum/maximum repayment period, maximum APR, a
  representative total-cost example, and a privacy policy; in some countries a license and extra
  documentation are required; access to contacts/photos is prohibited for loan apps.
- **US personal loans:** APR ≤ 36%; no full repayment due in 60 days or less.
- **Crypto exchanges and wallets:** licensed in the regions served; no on-device mining.
- Binary options and similar products are prohibited.

## Resolution

Complete the declaration, attach licenses, and add the required disclosures to the listing and app.

## Example rejection

> Financial Services policy violation. Your personal loan app does not disclose the maximum Annual
> Percentage Rate (APR) in the app description.
