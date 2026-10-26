# 🍎 Checklist — Every App Store submission

Load this first, then add the app-type checklists that apply. Rule files live in `../rules/`.

## Critical (will reject)

- [ ] **Upload** — built with Xcode 26+ / 26 SDK; iOS deployment target ≥ 13 → `technical/sdk_requirements.md`
- [ ] **2.1(a)** — final build, no crashes, no placeholder content, live backend, demo account → `metadata/review_notes.md`
- [ ] **2.3 / 2.3.7** — metadata within limits and accurate; no prices in name/subtitle/keywords → `metadata/accurate_metadata.md`
- [ ] **2.3.3 / 2.3.4** — screenshots show the app in use; previews without device frames
- [ ] **2.3.10** — no Android / Google Play / other marketplaces anywhere → `metadata/competitor_terms.md`
- [ ] **2.3.14** — creative assets: no pricing, no unverifiable claims, 4+ → `metadata/creative_assets.md`
- [ ] **2.5.19** — no hidden/dormant features; every feature flag disclosed → `design/hidden_features.md`
- [ ] **4.2 / 4.3** — native value beyond a website; no duplicate apps → `design/minimum_functionality.md`
- [ ] **5.1.1** — privacy manifest declares required-reason APIs → `privacy/privacy_manifest.md`
- [ ] **5.1.1(ii)** — every purpose string present and specific → `privacy/purpose_strings.md`
- [ ] **5.1.1(i)** — privacy policy URL in App Store Connect and inside the app
- [ ] **5.1.1(v)** — account deletion in app if accounts exist → `privacy/account_deletion.md`
- [ ] **5.1.2** — ATT prompt shown when tracking; App Privacy answers match SDKs → `privacy/app_tracking_transparency.md`

## Important (common rejections)

- [ ] **2.3.6** — age rating questionnaire answered (incl. 2026 social-media questions)
- [ ] **2.3.12** — What's New lists significant changes
- [ ] **2.4.1** — iPhone app runs acceptably on iPad
- [ ] **2.5.1** — only public APIs; no deprecated frameworks
- [ ] **4.8** — Sign in with Apple (or equivalent) next to social login → `design/sign_in_with_apple.md`
- [ ] **5.1.1(x)** — name/email optional unless essential → `privacy/unnecessary_data.md`
- [ ] **5.2** — rights to all content, music, fonts and trademarks
- [ ] **5.6.1** — review prompts use `SKStoreReviewController` / `RequestReviewAction` only
- [ ] EU — DSA trader status provided
