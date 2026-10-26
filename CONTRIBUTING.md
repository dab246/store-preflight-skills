# Contributing to Store Preflight

Thanks for helping developers ship without rejections! 🎉 This guide covers everything you need.

## Ground rules

1. **Official sources only.** Every rule cites developer.apple.com, developer.android.com,
   support.google.com or another official Apple/Google page. Blog posts, forums and third-party
   repositories are not accepted as sources (the validator enforces this).
2. **Write in your own words.** Summarise policies; quote at most a sentence when wording matters.
3. **Keep it neutral.** No product promotion, no names of tools or services that aren't needed to
   explain a check. Provider-specific detection belongs in the user's `.store-preflight.json`.
4. **Commits, branches and PR text** follow the same rules as files — the content guard checks them.

## Ways to contribute

| Contribution | Where |
|---|---|
| Share a rejection | Issue form *🚫 Share a rejection* |
| New rule / policy change | Issue form *📚 Rule request*, then a PR |
| Scanner check | `scripts/preflight_scan.py` + fixture + test |
| Policy source | `scripts/sync/sources.json` (+ extractor if structured data is needed) |
| Docs & checklists | `references/**/checklists/*.md`, `README.md` |

## Development setup

```bash
git clone https://github.com/dab246/store-preflight-skills.git
cd store-preflight-skills
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/sync/requirements.txt   # only needed for the sync script and its tests

python3 scripts/validate_rules.py               # knowledge-base checks
python3 -m unittest discover -s tests -v        # unit tests
python3 scripts/preflight_scan.py tests/fixtures/android-app
```

## Adding a rule

1. Pick the folder: `references/<apple|google>/rules/<category>/`.
2. Create `<snake_case_name>.md` with this front matter and sections:

   ```markdown
   ---
   id: google.permissions.my_rule        # <store>.<category>.<file name>
   store: google
   category: permissions
   severity: REJECTION                   # or WARNING
   policy: Exact Google Play policy name # Apple rules use: guideline: "5.1.1"
   title: Short, specific title
   automated: false                      # true | partial | false
   sources:
     - https://support.google.com/googleplay/android-developer/answer/...
   last_verified: 2026-10-26
   ---

   # Short, specific title

   ## What to check
   ## How to detect
   ## Resolution
   ## Example rejection
   ```

3. Reference it from the relevant checklist(s) and, if it is automatable, from the scanner.
4. Add a line to `CHANGELOG.md` under `[Unreleased]`.
5. Run the validator and tests.

## Adding a scanner check

- Keep it **deterministic** and dependency-free (standard library only, Python 3.9+).
- Return a `Finding` with store, severity, category, guideline/policy, title, detail and the rule path.
- Prefer `WARNING` when the scanner cannot know whether a declaration was filed in the console.
- Add or extend a fixture under `tests/fixtures/` and assert the finding in
  `tests/test_preflight_scan.py`. Make sure `clean-android` stays free of findings.

## Policy sync

The weekly workflow opens a `policy-update` pull request. Reviewers should:

1. read the diff in the PR body;
2. update affected rules (`last_verified`, dates, text) and checklists;
3. add a changelog entry under `[Unreleased]`;
4. merge, then cut a release when the change matters to users.

## Commit & PR conventions

- Conventional commits: `feat(google): …`, `fix(scanner): …`, `docs(apple): …`, `chore(policy): …`.
- Branch names: `feature/…`, `fix/…`, `docs/…`, `chore/…`.
- One logical change per PR; fill in the PR template.

## Releasing (maintainers)

1. Move `[Unreleased]` entries into a new version section in `CHANGELOG.md` and update the links.
2. Bump `metadata.version` in `SKILL.md`.
3. `git tag vX.Y.Z && git push origin vX.Y.Z` — the release workflow publishes notes and a zip.

## Code of Conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
