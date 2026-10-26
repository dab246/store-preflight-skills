# Cross-store matrix (App Store ↔ Google Play)

Use this in **both-stores** mode to avoid checking the same concern twice and to spot places where
one store is stricter.

| Concern | 🍎 App Store | 🤖 Google Play | Stricter / notes |
|---|---|---|---|
| Build toolchain | Xcode 26 / 26 SDK, iOS ≥ 13 | targetSdk 36, PBL 8, 16 KB pages | Both block at upload |
| Privacy declarations | App Privacy + `PrivacyInfo.xcprivacy` | Data safety form | Keep one source of truth per SDK |
| Purpose of permissions | `NS…UsageDescription` strings | Prominent disclosure + declarations | Google needs declarations/videos for restricted permissions |
| Tracking | ATT prompt | Advertising ID declaration, Data safety | Apple stricter (prompt required) |
| Account deletion | In app | In app **and** web URL | Google stricter |
| Third-party AI | Consent naming the provider (5.1.2(i)) | Report/flag AI output, Data safety | Implement both: consent + report button |
| UGC | Filter, report, block, contact (1.2) | Terms, moderation, report, block | Equivalent |
| Anonymous/random chat | 1.2 applies in full | Age-restricted + Child Safety (2026-08-26) | Google requires declaration |
| Digital purchases | IAP; links only with entitlement/US | Play Billing; alt programs by region | Region-specific on both |
| Subscription disclosure | Billed amount most prominent, ToS/PP links | Price, period, trial terms, cancel link | Same paywall can satisfy both |
| Social login | Must offer privacy-focused option (4.8) | No equivalent | Apple only |
| Metadata mentions | No Android/Google Play (2.3.10) | No iOS/App Store (Metadata policy) | Keep store-specific copy |
| Title length | 30 | 30 | Same |
| Reviewer access | Demo account in Review Notes | App access instructions | Same credentials can be used |
| Kids | Kids Category rules | Families policy | Both forbid most third-party SDKs |
| Testing before launch | TestFlight optional | 12 testers × 14 days (new personal accounts) | Google only |
