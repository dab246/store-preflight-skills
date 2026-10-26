# 🍎 Checklist — macOS / Mac App Store

- [ ] **2.4.5(i)** — App Sandbox enabled; every temporary exception justified → `../rules/entitlements/unused_entitlements.md`
- [ ] **2.4.5(ii)** — packaged with Xcode tools; no third-party installers
- [ ] **2.4.5(iii)** — no auto-launch at login without consent; no code in other apps
- [ ] **2.4.5(iv)–(vii)** — no license-key screens, no self-updating, runs on the current macOS
- [ ] Universal binary (Apple silicon native) — Rosetta support ends with macOS 27 for most apps
- [ ] No reliance on Full Disk Access for core features (stricter controls announced 2026)
- [ ] No `com.apple.quarantine` attribute on bundled files
