---
id: google.privacy.account_deletion
store: google
category: privacy
severity: REJECTION
policy: User Data · Account deletion requirements
title: Account creation without in-app and web account deletion
automated: partial
sources:
  - https://support.google.com/googleplay/android-developer/answer/13327111
last_verified: 2026-10-26
---

# Account creation without in-app and web account deletion

## What to check

- Apps that let users create an account must let them **request account deletion inside the app**
  and via a **publicly reachable web URL** (so people who uninstalled can still delete).
- The URL is entered in Play Console ▸ App content ▸ Data safety and clearly describes the steps.
- Deleting the account deletes associated user data; deactivation or "contact support" is not
  enough. Data kept for legal reasons is disclosed with retention periods.

## How to detect

Search for sign-up code and a deletion flow; open the declared URL in a private browser window.

## Resolution

Add a Settings ▸ Delete account flow, a web page/form for out-of-app requests, and the URL in Play
Console.

## Example rejection

> Your app allows users to create an account but does not provide a way for users to request account
> and data deletion from within the app and online.
