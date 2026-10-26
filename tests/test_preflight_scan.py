"""Tests for scripts/preflight_scan.py. Run: python -m unittest discover -s tests"""
import io
import json
import shutil
import struct
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT / "scripts"))
import preflight_scan  # noqa: E402


def scan(path, *extra):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = preflight_scan.main([str(path), "--format", "json", *extra])
    return code, json.loads(buf.getvalue())


def titles(report, severity=None):
    return [f["title"] for f in report["findings"] if severity in (None, f["severity"])]


def write_elf(path: Path, align: int) -> None:
    """Write a minimal ELF64 little-endian file with one PT_LOAD segment."""
    path.parent.mkdir(parents=True, exist_ok=True)
    header = bytearray(64)
    header[:6] = b"\x7fELF\x02\x01"
    struct.pack_into("<Q", header, 32, 64)        # e_phoff
    struct.pack_into("<HH", header, 54, 56, 1)    # e_phentsize, e_phnum
    phdr = bytearray(56)
    struct.pack_into("<I", phdr, 0, 1)            # PT_LOAD
    struct.pack_into("<Q", phdr, 48, align)       # p_align
    path.write_bytes(bytes(header) + bytes(phdr))


class AndroidFixture(unittest.TestCase):
    def setUp(self):
        self.code, self.report = scan(FIXTURES / "android-app")

    def test_detects_google_only(self):
        self.assertEqual(self.report["stores"], ["google"])

    def test_rejections(self):
        rejections = " | ".join(titles(self.report, "REJECTION"))
        for expected in ("targetSdk 34", "com.example", "Billing Library 7", "debuggable", "title is"):
            self.assertIn(expected, rejections)

    def test_restricted_permissions(self):
        warnings = " | ".join(titles(self.report, "WARNING"))
        for perm in ("READ_SMS", "QUERY_ALL_PACKAGES", "READ_CONTACTS"):
            self.assertIn(perm, warnings)
        self.assertIn("Foreground service types declared: location", warnings)

    def test_generic_ai_endpoint_and_account_deletion(self):
        all_titles = titles(self.report)
        self.assertIn("Generative AI feature detected", all_titles)
        self.assertIn("Account creation found but no account deletion flow", all_titles)

    def test_strict_exit_code(self):
        code, _ = scan(FIXTURES / "android-app", "--strict")
        self.assertEqual(code, 2)

    def test_only_filter(self):
        _, report = scan(FIXTURES / "android-app", "--only", "metadata")
        self.assertTrue(report["findings"])
        self.assertEqual({f["category"] for f in report["findings"]}, {"metadata"})


class IosFixture(unittest.TestCase):
    def setUp(self):
        self.code, self.report = scan(FIXTURES / "ios-app")

    def test_detects_apple_only(self):
        self.assertEqual(self.report["stores"], ["apple"])

    def test_rejections(self):
        rejections = " | ".join(titles(self.report, "REJECTION"))
        for expected in ("PrivacyInfo.xcprivacy", "NSLocationWhenInUseUsageDescription",
                         "deployment target 12", "name is", "mentions \"Android\""):
            self.assertIn(expected, rejections)

    def test_warnings(self):
        warnings = " | ".join(titles(self.report, "WARNING"))
        for expected in ("NSCameraUsageDescription is vague", "ATT is never requested",
                         "Sign in with Apple", "environment detection", "External payment",
                         "com.apple.developer.healthkit", "\"DemoBot\""):
            self.assertIn(expected, warnings)

    def test_push_entitlement_is_used(self):
        self.assertFalse(any("aps-environment" in t for t in titles(self.report)))


class CleanFixture(unittest.TestCase):
    def test_no_findings(self):
        code, report = scan(FIXTURES / "clean-android")
        self.assertEqual(code, 0)
        self.assertEqual(report["findings"], [])

    def test_all_stores_flag(self):
        _, report = scan(FIXTURES / "clean-android", "--store", "all")
        self.assertEqual(report["stores"], ["apple", "google"])


class ElfAndConfig(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(FIXTURES / "clean-android", self.tmp / "app", dirs_exist_ok=True)
        self.libs = self.tmp / "app" / "app" / "src" / "main" / "jniLibs" / "arm64-v8a"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_misaligned_library_is_rejected(self):
        write_elf(self.libs / "libold.so", 4096)
        _, report = scan(self.tmp / "app")
        self.assertIn("1 native library is not 16 KB aligned", titles(report, "REJECTION"))

    def test_aligned_library_passes(self):
        write_elf(self.libs / "libnew.so", 16384)
        _, report = scan(self.tmp / "app")
        self.assertEqual(titles(report, "REJECTION"), [])

    def test_ignore_config(self):
        write_elf(self.libs / "libold.so", 4096)
        (self.tmp / "app" / ".store-preflight.json").write_text(
            json.dumps({"ignore": ["google/technical/sixteen_kb_page_size"]}))
        _, report = scan(self.tmp / "app")
        self.assertEqual(report["findings"], [])


class RuleLinks(unittest.TestCase):
    def test_every_referenced_rule_exists(self):
        text = (ROOT / "scripts" / "preflight_scan.py").read_text()
        import re
        refs = set(re.findall(r'rule\("(apple|google)", "([\w/]+)"\)', text))
        refs |= {("google", p) for p in re.findall(r"\"(permissions/\w+)\"", text)}
        missing = [f"{s}/{p}" for s, p in refs if not (ROOT / "references" / s / "rules" / f"{p}.md").exists()]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
