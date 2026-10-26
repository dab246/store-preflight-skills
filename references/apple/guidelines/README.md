# App Store Review Guidelines — Curated Summary

> Source: [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) ·
> Apple revision **2026-10-16** · full numbered list: [live-index.md](./live-index.md) (regenerated weekly)

Short, preflight-oriented summaries of the guidelines that cause most rejections. Always defer to
Apple's text when in doubt.

## 1 · Safety

| Guideline | Topic | What reviewers look for |
|---|---|---|
| 1.1 | Objectionable content | No hateful, violent, sexual or exploitative content; no false features |
| 1.2 | User-generated content | Filter, report, block, contact info. Covers social, UGC, AI content creation and random/anonymous chat; NCII prevention |
| 1.2.1(a) | Creator content | Let users flag content above the age rating; age-restrict it |
| 1.3 | Kids Category | No external links/purchases without parental gate; no third-party ads/analytics |
| 1.4 | Physical harm | Medical claims need methodology; no risky challenges |
| 1.5 | Developer information | Easy way to contact you |
| 1.6 | Data security | Appropriate protection of user data |

## 2 · Performance

| Guideline | Topic | What reviewers look for |
|---|---|---|
| 2.1(a)/(b) | Completeness | Final build, demo account, live backend; IAP complete and visible |
| 2.3 | Accurate metadata | Description, screenshots, previews and privacy info match the app |
| 2.3.1(a) | Review notes | New features described specifically |
| 2.3.6 | Age rating | Honest questionnaire answers (social-media questions added 2026) |
| 2.3.7 | Name & keywords | ≤ 30 chars, no prices, no trademark stuffing |
| 2.3.10 | Platform focus | No other platforms or marketplaces |
| 2.3.14 | Creative assets | Header/search assets: on-brand, 4+, no pricing or unverifiable claims (**new 2026-10-16**) |
| 2.4.5 | Mac App Store | Sandboxed, self-contained, no installers or license screens |
| 2.5.1–2.5.2 | Software | Public APIs only; no downloaded executable code |
| 2.5.18 | Advertising | Ads in main binary, age-appropriate, closable, reportable |
| 2.5.19 | Hidden features | No hidden/dormant/undocumented features or obfuscation (**new 2026-10-16**) |

## 3 · Business

| Guideline | Topic | What reviewers look for |
|---|---|---|
| 3.1.1 | In-App Purchase | Digital goods via IAP; loot box odds; restore |
| 3.1.1(a) | Links to other purchase methods | Only with StoreKit External Purchase Link entitlement (incl. music streaming) or where storefront rules allow; permitted destinations only |
| 3.1.2 | Subscriptions | ≥ 7 days, ongoing value, clear terms, ToS/PP links |
| 3.1.3 | Exceptions | Reader, multiplatform, enterprise, person-to-person, physical goods |
| 3.1.5 | Cryptocurrencies | Org wallets, no on-device mining, licensed exchanges |
| 3.2.2 | Unacceptable | No store-like interfaces, binary options, forced reviews; loan limits |

## 4 · Design

| Guideline | Topic | What reviewers look for |
|---|---|---|
| 4.1 | Copycats | No imitation; no others' brands in name/icon |
| 4.2 | Minimum functionality | More than a website or marketing app |
| 4.3 | Spam | One app per concept; saturated categories need clear value |
| 4.7 | Mini apps, chatbots, plug-ins, emulators | Same rules as native; index; consent; age restriction |
| 4.8 | Login services | Privacy-focused login option alongside social login |
| 4.10 | Built-in capabilities | Don't charge for OS features |

## 5 · Legal

| Guideline | Topic | What reviewers look for |
|---|---|---|
| 5 | Legal | Comply with local law (e.g. AI service licensing in China mainland) |
| 5.1.1 | Data collection | Privacy policy, consent, minimization, purpose strings, account deletion, regulated entities |
| 5.1.2 | Data use & sharing | Consent before sharing incl. **third-party AI**; ATT for tracking |
| 5.1.3–5.1.5 | Health, kids, location | Health data never for ads; COPPA; location only when relevant |
| 5.2 | Intellectual property | Rights to all content; no Apple endorsement claims |
| 5.3 | Gaming & gambling | Licensed real-money gaming only |
| 5.4 | VPN | NEVPNManager, org accounts, disclosure, no data selling |
| 5.6 | Code of Conduct | No review manipulation; accurate developer info |

## Recent changes

| Date | Change |
|---|---|
| 2026-10-16 | 1.2 scope (AI content creation, NCII, Code of Conduct); new 2.3.14 and 2.5.19; 3.1.1(a) merged music streaming bullet; 5 trafficking/child exploitation |
| 2026-06-08 | Guidelines and Developer Program License Agreement update |

The weekly [policy-sync workflow](../../../.github/workflows/policy-sync.yml) opens a pull request
whenever Apple publishes a new revision, listing exactly which guideline numbers changed.
