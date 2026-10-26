---
id: apple.design.sign_in_with_apple
store: apple
category: design
severity: REJECTION
guideline: "4.8 · 5.1.1(x)"
title: Login services and Sign in with Apple
automated: partial
sources:
  - https://developer.apple.com/app-store/review/guidelines/#4.8
  - https://developer.apple.com/sign-in-with-apple/
last_verified: 2026-10-26
---

# Login services and Sign in with Apple

## What to check

- Apps that offer a third-party or social login for the primary account must also offer an
  equivalent option that limits data collection to name and email, lets users keep their email
  private, and does not track — Sign in with Apple satisfies this (4.8). Exemptions: your own
  account system only, education/enterprise accounts, government ID, or clients for a specific
  third-party service.
- After Sign in with Apple succeeds, **do not ask again for name or email** that Apple already
  provided or that the user chose to hide.
- Handle relay addresses: Apple announced a new relay domain in 2026 in addition to
  `privaterelay.appleid.com`; don't hard-code a single domain in email validation or allow-lists.
- The button follows the Human Interface Guidelines (same size/prominence as other login buttons).
- Account deletion revokes tokens (see `privacy/account_deletion.md`).

## How to detect

```bash
grep -rnE "GoogleSignIn|google_sign_in|FBSDKLoginKit|FacebookLogin|LineSDK|KakaoSDK" .
grep -rnE "ASAuthorizationAppleIDProvider|sign_in_with_apple|AppleAuthentication" .
grep -rn "privaterelay.appleid.com" .
```

## Resolution

Add Sign in with Apple next to the other providers, use the credential's name/email (first sign-in
only), and accept any relay domain.

## Example rejection

> Guideline 4.8 - Design - Login Services. The app uses a third-party login service, but does not
> appear to offer an equivalent login option with the required privacy features.
