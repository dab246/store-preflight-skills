---
name: store-preflight-skills
description: >
  Pre-submission review for mobile apps on the Apple App Store (iOS, iPadOS, macOS) and Google Play
  (Android, Wear OS, TV, Automotive). Use before submitting a build, after receiving a rejection, or
  when auditing metadata, privacy declarations, permissions, subscriptions, SDK/target API levels or
  AI features. Checks one store or both at once, for native, Flutter, React Native/Expo, Capacitor
  and Kotlin Multiplatform projects.
license: MIT
metadata:
  author: dab246
  version: "1.0.0"
  apple-guidelines-synced: "2026-10-26"
  google-policies-synced: "2026-10-26"
---

# Store Preflight

Catch App Store and Google Play rejection causes **before** you submit. All paths below are relative
to this skill's directory.

## Step 0 — Decide the scope

Work out three things from the request and the project. Ask only if it is genuinely ambiguous.

| Setting | Values | Default |
|---|---|---|
| **Store** | `apple`, `google`, `both` | Auto-detect: `ios/`, `*.xcodeproj`, `Podfile` → apple; `android/`, `build.gradle(.kts)`, `AndroidManifest.xml` → google; both present → both |
| **App types** | subscription, social/UGC, kids, health, games, AI, finance/crypto, VPN, macOS, Wear/TV/Auto | Infer from dependencies, manifests and the user's description |
| **Depth** | `quick` (automated scan only), `full` (scan + checklists + rules), `fix` (full + apply safe fixes) | `full` |

Examples of requests and the scope they map to:

- "Is my app ready for Google Play?" → store `google`, depth `full`
- "Quick check for both stores" → store `both`, depth `quick`
- "Apple rejected us for 5.1.1" → store `apple`, focus on `references/apple/rules/privacy/`
- "Only check permissions and privacy" → pass `--only permissions,privacy` to the scanner and load only those rule folders

## Step 1 — Run the automated scan

Requires Python 3.9+ (standard library only).

```bash
python3 scripts/preflight_scan.py <project-dir> --store <auto|apple|google|all> [--only privacy,metadata] [--metadata <dir>]
```

- `--format json` gives machine-readable output; `--strict` exits with code 2 on any rejection (useful in CI).
- It reads machine-readable thresholds from `references/apple/requirements.json` and
  `references/google/requirements.json` (kept current by the weekly policy sync).
- Optional per-project settings in `<project>/.store-preflight.json`:
  - `ai_service_terms` — brand names of AI services used by the app, checked in China-visible metadata
  - `ai_endpoints` — extra regexes that identify third-party AI calls
  - `ignore` — rule paths (e.g. `google/technical/sixteen_kb_page_size`) to suppress after manual review

Each finding names the rule file that explains it. Treat scanner output as **evidence to verify**,
not as the final verdict: read the cited file/line before reporting.

## Step 2 — Load the checklists

Always load `all_apps.md` for each store in scope, then the app-type checklists that apply.

| App type | 🍎 Apple (`references/apple/checklists/`) | 🤖 Google (`references/google/checklists/`) |
|---|---|---|
| Every app | `all_apps.md` | `all_apps.md` |
| Subscriptions / IAP | `subscription_iap.md` | `subscription_iap.md` |
| Social / UGC / chat | `social_ugc.md` | `social_ugc.md` |
| Kids | `kids.md` | `kids_families.md` |
| Health & fitness | `health_fitness.md` | `health_fitness.md` |
| Games | `games.md` | `games.md` |
| AI / generative AI | `ai_apps.md` | `ai_apps.md` |
| Finance, crypto, loans | `crypto_finance.md` | `finance_crypto_loans.md` |
| VPN | `vpn.md` | `vpn.md` |
| macOS | `macos.md` | — |
| Wear OS / TV / Auto / XR | — | `form_factors.md` |

In `both` mode also load `references/shared/cross_store_matrix.md` so shared concerns (account
deletion, AI consent, paywalls, reviewer access) are checked once and fixed in one change.

Guideline/policy indexes: `references/apple/guidelines/README.md` (curated) and `live-index.md`
(every guideline number, regenerated weekly); `references/google/policies/README.md` and
`upcoming-deadlines.md`.

## Step 3 — Gather metadata (optional but recommended)

Metadata checks need the store listing text as files, one folder per locale.

- **Apple:** export from App Store Connect, or pull through the
  [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
  (`appInfoLocalizations`, `appStoreVersionLocalizations`). Supported layouts: `<dir>/<locale>/name.txt`
  (plus `subtitle.txt`, `keywords.txt`, `description.txt`, `promotional_text.txt`, `release_notes.txt`)
  or JSON files under `<dir>/app-info/` and `<dir>/version/<version>/`.
- **Google:** pull listings through the
  [Google Play Developer API](https://developers.google.com/android-publisher) (`edits.listings`).
  Layout: `<dir>/android/<locale>/title.txt`, `short_description.txt`, `full_description.txt`.

Pass the folder with `--metadata <dir>`. Without metadata, review the listing manually against
`references/apple/rules/metadata/` and `references/google/rules/metadata/`.

## Step 4 — Run the rule checks

For every category in scope, read the rule files and apply **What to check** and **How to detect**.

| Category | 🍎 Apple rules | 🤖 Google rules |
|---|---|---|
| Technical / upload | `references/apple/rules/technical/` | `references/google/rules/technical/` |
| Privacy | `references/apple/rules/privacy/` | `references/google/rules/privacy/` |
| Permissions & entitlements | `references/apple/rules/entitlements/` | `references/google/rules/permissions/` |
| Metadata | `references/apple/rules/metadata/` | `references/google/rules/metadata/` |
| Payments | `references/apple/rules/subscription/` | `references/google/rules/monetization/` |
| Design / content | `references/apple/rules/design/` | `references/google/rules/content/` |
| Account & review access | `references/apple/rules/metadata/review_notes.md` | `references/google/rules/account/` |

Rule files have YAML front matter (`id`, `severity`, `guideline`/`policy`, `sources`,
`last_verified`). When a rule's `last_verified` date is older than the latest sync, double-check the
official source linked in `sources`.

## Step 5 — Report

Use `references/shared/report_template.md`: one section per store, ordered ❌ rejections →
⚠️ warnings → ✅ passed, then **Shared fixes** (both mode) and **Manual follow-ups** (things only
the developer can verify in App Store Connect or Play Console). Every finding includes the
guideline/policy, file and line, a concrete fix, and the rule file.

## Step 6 — Fix and re-validate (depth `fix`)

Safe to apply automatically, after showing the diff:

- metadata over the limit or containing other-platform / promotional terms → propose shortened text;
- missing `PrivacyInfo.xcprivacy` categories, missing or vague purpose strings;
- `targetSdk`, Billing Library and deployment-target bumps (flag behaviour changes to test);
- removing unused permissions/entitlements (`tools:node="remove"` for SDK-merged permissions).

Never auto-apply changes that need product decisions (paywall redesign, removing features, consent
copy, legal text). After any fix, **re-run the scanner and the affected rule checks**; only mark an
item resolved when the re-check passes.

## Gotchas

- **Merged manifests:** Android SDKs add permissions at build time. Check
  `app/build/intermediates/merged_manifests/` or the Play Console bundle explorer, not only `src/main`.
- **Cross-platform defaults:** Flutter's `flutter.targetSdkVersion` and Expo defaults change with the
  framework version — verify the resolved value.
- **Privacy manifests are transitive:** SDKs such as analytics and crash reporters trigger
  required-reason API declarations even if your own code never calls them.
- **Both stores, different copy:** a shared description that mentions "Android" or "iPhone" fails one
  of the two stores. Keep store-specific metadata.
- **Third-party AI:** Apple wants consent that names the provider *before* the first request; Google
  wants an in-app way to report AI output. Ship both.
- **Account deletion:** Google also requires a public web URL for deletion requests.
- **Dates move:** both stores publish deadlines and extensions. Check `requirements.json`,
  `upcoming-deadlines.md` and the official links in each rule before quoting a date to the user.
- **Hidden features (Apple 2.5.19):** feature flags are fine only when every state is in the
  reviewed build and disclosed in the review notes.

## Adding or updating rules

See `CONTRIBUTING.md`. Rule template:

```markdown
---
id: <store>.<category>.<file_name>
store: apple | google
category: <folder name>
severity: REJECTION | WARNING
guideline: "<Apple guideline number>"     # Apple
policy: <Google Play policy name>          # Google
title: <short title>
automated: true | partial | false
sources:
  - <official Apple or Google URL>
last_verified: YYYY-MM-DD
---

# <Title>
## What to check
## How to detect
## Resolution
## Example rejection
```
