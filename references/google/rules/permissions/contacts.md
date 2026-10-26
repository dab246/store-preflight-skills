---
id: google.permissions.contacts
store: google
category: permissions
severity: WARNING
policy: Contacts Permissions
title: Broad contacts access instead of the Contact Picker
automated: true
sources:
  - https://support.google.com/googleplay/android-developer/answer/16935362
  - https://developer.android.com/distribute/play-policies
last_verified: 2026-10-26
---

# Broad contacts access instead of the Contact Picker

## What to check

The Contacts Permissions policy (announced 2026-04-15, listed for **2027-01-27** on Google's
deadline page; check Play Console for the date that applies to your target API) governs
`READ_CONTACTS` / `WRITE_CONTACTS`:

- Apps that don't need broad access must use the **Android Contact Picker**
  (`Intent.ACTION_PICK_CONTACTS`, Android 17+) or Sharesheet.
- Apps that keep `READ_CONTACTS` submit a declaration form in Play Console and pass an access review.
- Device-management and enterprise private apps are exempt.

## How to detect

```bash
grep -rnE "READ_CONTACTS|WRITE_CONTACTS" --include=AndroidManifest.xml .
grep -rnE "ContactsContract|contacts_service|flutter_contacts|react-native-contacts" .
```

## Resolution

Switch "invite a friend" and "pick a recipient" flows to the picker; keep broad access only for
contacts-centric apps and submit the declaration.

## Example rejection

> Your app requests READ_CONTACTS but its core functionality does not require broad access to the
> user's contacts. Use the Android Contact Picker.
