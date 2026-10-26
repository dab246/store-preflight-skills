"""Offline tests for scripts/sync/sync_sources.py extractors."""
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "sync"))

try:
    import sync_sources as sync
except SystemExit:  # optional dependencies missing
    sync = None

APPLE_HTML = """<html><body><main>
<ul><li id="safety"><span id="1.1"></span><strong>1.1 Objectionable Content</strong>
<p>Apps should not include offensive content.</p>
<ul><li id="1.1.1"><strong>1.1.1</strong> Defamatory content.</li></ul></li>
{extra}
</ul><p>Last Updated: October 16, 2026</p></main></body></html>"""


@unittest.skipIf(sync is None, "requests/bs4 not installed")
class Extractors(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(sync.parse_date("Starting August 31 2026: New apps"), "2026-08-31")
        self.assertEqual(sync.parse_date("By Aug 31, 2026, all"), "2026-08-31")

    def test_apple_guidelines(self):
        extra = "".join(f'<li id="2.{i}"><strong>2.{i} Item {i}</strong> body {i}</li>' for i in range(60))
        ext = sync.extract_apple_guidelines(APPLE_HTML.format(extra=extra), "2026-10-26")
        self.assertIn("### 1.1 Objectionable Content", ext.text)
        self.assertNotIn("Defamatory", ext.text.split("### 1.1.1")[0])  # nested item stripped
        self.assertEqual(ext.updates[sync.APPLE_REQ]["guidelines_last_updated"], "2026-10-16")

    def test_apple_guidelines_layout_guard(self):
        with self.assertRaises(RuntimeError):
            sync.extract_apple_guidelines(APPLE_HTML.format(extra=""), "2026-10-26")

    def test_changed_guidelines(self):
        old = "### 1.1 A\ntext\n\n### 2.1 B\nold"
        new = "### 1.1 A\ntext\n\n### 2.1 B\nnew\n\n### 2.2 C\nx"
        self.assertEqual(sync.changed_guidelines(old, new), ["**2.1** changed", "**2.2** added"])

    def test_target_sdk(self):
        html = ("<article>Starting August 31 2026: New apps and app updates must target Android 16 "
                "(API level 36) or higher to be submitted to Google Play; except for Wear OS and Android "
                "Automotive OS apps, which must target Android 15 (API level 35) or higher, and Android TV "
                "and Android XR apps, which must target Android 14 (API level 34) or higher. Existing apps "
                "must target Android 15 (API level 35) or higher. You'll be able to request an extension "
                "to November 1, 2026.</article>")
        upd = sync.extract_google_target_sdk(html, "x").updates[sync.GOOGLE_REQ]
        self.assertEqual(upd["target_sdk.new_apps_and_updates"], 36)
        self.assertEqual(upd["target_sdk.tv_and_xr"], 34)
        self.assertEqual(upd["target_sdk.existing_apps"], 35)
        self.assertEqual(upd["target_sdk.extension_until"], "2026-11-01")

    def test_billing(self):
        html = ("<article>Reminder: By Aug 31, 2027, all new apps and updates to existing apps must use "
                "Billing Library version 9 or later. You can request an extension until Nov 1, 2027.</article>")
        upd = sync.extract_google_billing(html, "x").updates[sync.GOOGLE_REQ]
        self.assertEqual(upd["play_billing_library.min_major"], 9)
        self.assertEqual(upd["play_billing_library.extension_until"], "2027-11-01")

    def test_timeline(self):
        html = ("<article><table><tr><th>Date</th><th>Policy Update</th></tr>"
                "<tr><td>January 27, 2027</td><td>Contacts Permissions policy</td></tr></table></article>")
        ext = sync.extract_google_timeline(html, "2026-10-26")
        self.assertEqual(ext.text, "- 2027-01-27 — Contacts Permissions policy")

    def test_redaction_uses_environment(self):
        os.environ["POLICY_SYNC_REDACT_TERMS"] = "Foo, bar baz"
        try:
            self.assertEqual(sync.redactor()("foo and Bar Baz stay"), "[redacted] and [redacted] stay")
        finally:
            del os.environ["POLICY_SYNC_REDACT_TERMS"]


if __name__ == "__main__":
    unittest.main()
