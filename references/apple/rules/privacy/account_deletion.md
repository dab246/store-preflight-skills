---
id: apple.privacy.account_deletion
store: apple
category: privacy
severity: REJECTION
guideline: "5.1.1(v)"
title: Account creation without in-app account deletion
automated: partial
sources:
  - https://developer.apple.com/app-store/review/guidelines/#5.1.1
  - https://developer.apple.com/support/offering-account-deletion-in-your-app/
last_verified: 2026-10-26
---

# Account creation without in-app account deletion

## What to check

- If users can create an account, they can **initiate deletion inside the app** (not only by email
  or a support form), and the flow is easy to find (typically Settings ▸ Account).
- Deletion removes the account and associated personal data, not just deactivation. Regulated apps
  may keep records required by law and must say so.
- Sign in with Apple users: revoke tokens with the REST API when the account is deleted.
- Subscriptions: tell users that billing continues until they cancel in the App Store, and link to
  subscription management.
- Account creation is not required for features that don't need it (5.1.1(v)).

## How to detect

```bash
grep -rniE "delete.?account|deleteUser|account.?deletion|removeAccount" --include=*.swift --include=*.dart --include=*.ts --include=*.tsx .
```

## Resolution

Add a **Delete account** entry with a confirmation step, call a backend endpoint that deletes data
(or queues deletion with a stated timeframe), revoke Sign in with Apple tokens, and describe the path
in the Notes for Review.

## Example rejection

> Guideline 5.1.1(v) - Data Collection and Storage. The app supports account creation but does not
> include an option to initiate account deletion.
