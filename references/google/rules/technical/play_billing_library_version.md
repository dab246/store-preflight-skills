---
id: google.technical.play_billing_library_version
store: google
category: technical
severity: REJECTION
policy: Play Billing Library version deprecation
title: Deprecated Google Play Billing Library
automated: true
sources:
  - https://developer.android.com/google/play/billing/deprecation-faq
  - https://developer.android.com/google/play/billing/release-notes
last_verified: 2026-10-26
---

# Deprecated Google Play Billing Library

## What to check

| PBL version | New apps & updates blocked after | Extension until |
|---|---|---|
| 6 | 2025-08-31 | 2025-11-01 |
| 7 | **2026-08-31** | **2026-11-01** |
| 8 | 2027-08-31 | 2027-11-01 |

Since 2026-08-31 every new app and update that sells through Play must use **PBL 8 or later**.
Cross-platform purchase plugins bundle their own PBL — check the plugin's changelog.

## How to detect

```bash
grep -rnE "com.android.billingclient:billing" --include=*.gradle --include=*.kts .
grep -rnE "billing" gradle/libs.versions.toml 2>/dev/null
./gradlew :app:dependencies --configuration releaseRuntimeClasspath | grep billingclient
```

## Resolution

Upgrade to PBL 8+, then handle the API changes (e.g. removal of deprecated query methods, required
`enablePendingPurchases` parameters, one-time product changes). Re-test purchases, restores and
subscription upgrades with license testers.

## Example rejection

> Your app uses a version of Google Play Billing Library that is no longer supported. Update to Play
> Billing Library version 8.0.0 or newer to publish this release.
