# Security Policy

## Supported versions

Only the latest release receives fixes. Policy data is refreshed weekly on `main`.

## Reporting a vulnerability

Please **do not open a public issue**. Use GitHub's
[private vulnerability reporting](https://github.com/dab246/store-preflight-skills/security/advisories/new)
and include steps to reproduce. You can expect an initial response within 7 days.

Relevant areas include the scanner reading untrusted project files, the policy-sync workflow
(which fetches remote content and opens pull requests), and the release workflow.

## Scope notes

- The scanner only reads files; it never executes project code or sends data anywhere.
- Never paste App Store Connect keys, Play service-account JSON or other credentials into issues,
  fixtures or `.store-preflight.json`.
