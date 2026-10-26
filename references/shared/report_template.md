# Preflight report template

Use one section per store. Omit a store when only one was checked.

```markdown
# ✈️ Store Preflight Report — <App name> <version>

**Scope:** 🍎 App Store · 🤖 Google Play  **Checklists:** all_apps, subscription_iap, ai_apps
**Policy snapshot:** Apple guidelines 2026-10-16 · Google Play requirements synced 2026-10-26

## Summary

| Store | ❌ Rejections | ⚠️ Warnings | ✅ Passed |
|---|---|---|---|
| 🍎 App Store | 2 | 3 | 18 |
| 🤖 Google Play | 1 | 4 | 21 |

## 🍎 App Store

### ❌ Rejections (2)
- **[5.1.1 · ITMS-91053] Missing privacy manifest declaration**
  - File: `ios/Runner/PrivacyInfo.xcprivacy`
  - Evidence: `UserDefaults` in `ios/Runner/AppDelegate.swift:12`
  - Fix: add `NSPrivacyAccessedAPICategoryUserDefaults` with reason `CA92.1`
  - Rule: `references/apple/rules/privacy/privacy_manifest.md`

### ⚠️ Warnings (3)
- **[4.8] …**

### ✅ Passed (18)
- Metadata limits, competitor terms, purpose strings, …

## 🤖 Google Play
…

## 🔁 Shared fixes
Issues that need one change for both stores (e.g. account deletion, AI consent + report button).

## 📝 Manual follow-ups
Things the agent could not verify (screenshots, Play Console declarations, App Store Connect answers).
```

Order every list by severity: rejections, warnings, passed. Every finding names the guideline/policy,
the file (and line when known), a concrete fix, and the rule file.
