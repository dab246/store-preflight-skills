---
id: google.monetization.ads
store: google
category: monetization
severity: REJECTION
policy: Ads · Better Ads experiences
title: Disruptive, deceptive or non-compliant ads
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/9857753
last_verified: 2026-10-26
---

# Disruptive, deceptive or non-compliant ads

## What to check

- No full-screen interstitials **at app launch, during gameplay/level start, or during content
  consumption** that can't be closed after a short time; close buttons are visible.
- Ads don't mimic system notifications, app UI or warnings, and aren't placed to cause accidental
  clicks.
- No ads outside the app (lock screen, notifications) unless that is the app's explicit function.
- Rewarded ads are opt-in.
- Ad SDKs are Families-certified when the app targets children.
- `com.google.android.gms.permission.AD_ID` declared only if the advertising ID is used, and the
  Data safety form matches.

## How to detect

Play through the main flows with ads enabled in a release build and record the session.

## Resolution

Reduce interstitial frequency, move ads to natural breaks, and configure SDK settings for families
and consent.

## Example rejection

> Ads policy violation. Your app contains interstitial ads that appear unexpectedly and interfere
> with app usage.
