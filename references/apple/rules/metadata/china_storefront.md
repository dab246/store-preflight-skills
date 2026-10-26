---
id: apple.metadata.china_storefront
store: apple
category: metadata
severity: WARNING
guideline: "5 · 5.1.1(ix)"
title: Unlicensed generative-AI services visible on the China mainland storefront
automated: partial
sources:
  - https://developer.apple.com/app-store/review/guidelines/#legal
last_verified: 2026-10-26
---

# Unlicensed generative-AI services on the China mainland storefront

## What to check

Apps distributed in China mainland must comply with local law (guideline 5). Generative-AI features
need the relevant government approval, and apps that reference or integrate foreign generative-AI
services that are not licensed there are removed or rejected for that storefront.

- The China storefront displays **every localization you ship**, not only `zh-Hans`, so check all
  locales.
- Check name, subtitle, keywords, description, What's New, screenshots and in-app text.
- Apps whose core feature is generative AI need the approval number (or must exclude China mainland
  in **Pricing and Availability**).

## How to detect

The scanner flags generic wording ("LLM", "AI chatbot", "generative AI"). Add the brand names of the
AI services your app uses to `.store-preflight.json → ai_service_terms` so they are checked across
all locales.

## Resolution

- Remove third-party AI brand names from metadata (describe the feature instead), **or**
- remove China mainland from availability until the required approval is obtained.

## Example rejection

> Guideline 5 - Legal. Your app includes features related to generative AI that do not have the
> necessary permits in China mainland.
