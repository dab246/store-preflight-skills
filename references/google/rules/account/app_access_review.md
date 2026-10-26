---
id: google.account.app_access_review
store: google
category: account
severity: REJECTION
policy: App access · Prepare your app for review
title: Reviewers cannot access restricted parts of the app
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/9859455
last_verified: 2026-10-26
---

# Reviewers cannot access restricted parts of the app

## What to check

Play Console ▸ App content ▸ **App access** contains working instructions for every gated area:

- reusable test credentials that don't expire, don't require 2FA/OTP to a personal device, and aren't
  geo- or IP-restricted (or explain how to bypass);
- membership, invitation or hardware requirements and how to get past them;
- a backend that is live during review.

Also complete every other **App content** declaration (ads, content rating, target audience, news,
health, financial features, data safety, government apps) — incomplete declarations block
publishing.

## Resolution

Create a dedicated review account with full access and document the steps; re-check before each
submission.

## Example rejection

> We were unable to review your app because the login credentials provided in App access were
> invalid or incomplete.
