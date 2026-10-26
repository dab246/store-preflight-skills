---
id: google.content.minimum_functionality_spam
store: google
category: content
severity: REJECTION
policy: Spam and Minimum Functionality · Impersonation
title: Broken, low-value, duplicate or impersonating apps
automated: false
sources:
  - https://support.google.com/googleplay/android-developer/answer/9898783
last_verified: 2026-10-26
---

# Broken, low-value, duplicate or impersonating apps

## What to check

- The app installs, launches and works without crashing on recent Android versions; features in the
  listing exist.
- It provides a stable, engaging experience — not just a webview of a website you don't own, a
  single static page, or a link collection.
- No duplicate apps with minor changes, template/white-label spam, or keyword-stuffed variants.
- No impersonation of other developers, brands or Google; no misleading icons.

## How to detect

Install the release build on a clean device, run the pre-launch report in Play Console, and review
Android vitals for crashes/ANRs.

## Resolution

Fix crashes, add native value, consolidate duplicates into one app with in-app configuration.

## Example rejection

> Minimum Functionality policy violation. Your app does not provide a stable, responsive, and
> engaging user experience.
