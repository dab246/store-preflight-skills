Reminder:
By Aug 31, 2026, all new apps and updates to existing apps must use Billing Library version 8 or later. If you need more time to update your app, you can request an extension until Nov 1, 2026. Learn about
Play Billing Library version deprecation
.
Android Developers
Google Play
Play Monetization
Google Play Billing Library version deprecation
Stay organized with collections
Save and categorize content based on your preferences.
All versions of the Google Play Billing Library have a two-year deprecation
cycle. Google announced this deprecation cycle at Google I/O 2019 and in the
Meet Google Play Billing Library Version 3
blog post.
This page answers common questions about the Google Play
Billing Library version deprecation and migrating to higher versions.
Use the Play Billing Library
Android skill
to automate your upgrade to the latest version.
To install the skill from the
Android CLI
, run:
android skills add play-billing-library-version-upgrade
To activate the skill, try the following prompt:
Help me upgrade my Play Billing Library implementation.
Support timeline for different versions
The following table shows the deprecation and extension deadlines for each
Google Play Billing Library version.
Version
New app and update deadline
Extension deadline
5
August 31, 2024
November 1, 2024
6
August 31, 2025
November 1, 2025
7
August 31, 2026
November 1, 2026
8
August 31, 2027
November 1, 2027
9
August 31, 2028
November 1, 2028
How do you find which APKs use a deprecated Play Billing Library version?
Check your
build.gradle
file. Apps must use a supported version from the
table. These dependencies only appear in APKs that require the
com.android.vending.BILLING
permission.
Do you need to update unmaintained APKs?
We recommend updating maintained APKs. Unmaintained APKs don't need updates;
existing apps still work, but new apps and updates must use supported
versions.
How do you fix a deprecation warning if you've already updated your app to a supported version?
Make sure your
AndroidManifest.xml
file contains
com.google.android.play.billingclient.version
. If it's missing,
check whether
manifest merging
removes this attribute.
How do you upgrade from a lower version of the Google Play Billing Library?
Update the dependency in your release to use a supported version from
the table. To learn what changed between releases, see the
release notes
.
To migrate, see the
migration guide for version 9
.
Where do you find the extension form to continue distributing to users until the extension deadline?
If your app uses an unsupported Google Play Billing Library version, you'll
receive a warning in the Google Play Console. On the warning's details page
on the
Policy status
page,
open the extension form.
