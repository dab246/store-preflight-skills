# 🤖 Checklist — Every Google Play release

Load this first, then add the app-type checklists that apply. Rule files live in `../rules/`.

## Critical (will reject or block publishing)

- [ ] **Target API** — targetSdk 36 (Wear/Auto 35, TV/XR 34) → `technical/target_api_level.md`
- [ ] **Play Billing Library** — version 8+ if selling digital goods → `technical/play_billing_library_version.md`
- [ ] **16 KB pages** — native libraries 16 KB aligned (updates blocked from 2027-02-01) → `technical/sixteen_kb_page_size.md`
- [ ] **Upload** — AAB, Play App Signing, not debuggable, no `com.example` → `technical/app_bundle_and_signing.md`
- [ ] **Data safety** — form matches code and every SDK; privacy policy in console and app → `privacy/data_safety_form.md`
- [ ] **Account deletion** — in-app and web URL → `privacy/account_deletion.md`
- [ ] **Sensitive permissions** — each restricted permission removed or declared → `permissions/*.md`
- [ ] **Prominent disclosure** before unexpected data collection → `privacy/prominent_disclosure.md`
- [ ] **Store listing** — limits, no promo terms/emoji/caps/other platforms → `metadata/store_listing.md`
- [ ] **App access** — working reviewer credentials; all App content declarations complete → `account/app_access_review.md`
- [ ] **Developer verification** — app registered to a verified developer → `account/developer_verification.md`

## Important

- [ ] New personal account — 12 testers × 14 days closed test → `account/closed_testing_requirement.md`
- [ ] Content rating, target audience, ads declaration, news declaration, health apps declaration, financial features declaration
- [ ] Minimum functionality: no crashes in pre-launch report; native value → `content/minimum_functionality_spam.md`
- [ ] Upcoming deadlines reviewed → `../policies/upcoming-deadlines.md`
