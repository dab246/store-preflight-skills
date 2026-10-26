#!/usr/bin/env python3
"""Deterministic preflight scanner for App Store (iOS/macOS) and Google Play (Android).

Runs the checks that do not need judgement - SDK levels, manifests, plists,
privacy manifests, ELF alignment, metadata limits - and prints findings that
point at the rule file explaining each one. The skill (SKILL.md) runs this
first, then performs the judgement-based checks from the checklists.

Works on native, Flutter, React Native / Expo, Capacitor and KMP projects.
Standard library only (Python 3.9+).

Usage:
  python3 scripts/preflight_scan.py [PROJECT_DIR]
      [--store auto|apple|google|all]   which store(s) to check (default: auto-detect)
      [--only CAT[,CAT]]                 limit to categories, e.g. privacy,permissions
      [--metadata DIR]                   extra store-listing metadata folder
      [--format md|json]                 output format (default: md)
      [--strict]                         exit 2 when any REJECTION is found
"""
from __future__ import annotations

import argparse
import json
import plistlib
import re
import struct
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git", "node_modules", "build", ".gradle", "Pods", "DerivedData", ".build", ".dart_tool",
    "vendor", "dist", ".idea", ".next", "intermediates", ".cxx", ".expo", "Carthage",
    ".symlinks", "ephemeral", "__pycache__", ".venv", "venv", "tests", "test", "androidTest",
}
SOURCE_EXT = {".swift", ".m", ".mm", ".h", ".kt", ".kts", ".java", ".dart", ".js", ".jsx",
              ".ts", ".tsx", ".gradle", ".toml", ".yaml", ".yml", ".xml", ".plist", ".properties",
              ".entitlements", ".xcprivacy", ".pbxproj", ".json", ".txt", ".podspec", ".cs"}
MAX_FILE_BYTES = 2_000_000
SEVERITY_ORDER = {"REJECTION": 0, "WARNING": 1, "INFO": 2}
ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


@dataclass
class Finding:
    store: str          # apple | google | both
    severity: str       # REJECTION | WARNING | INFO
    category: str
    guideline: str
    title: str
    detail: str
    rule: str           # path of the rule file relative to the skill root
    file: str = ""
    line: int = 0


# --------------------------------------------------------------------------- #
# Project model
# --------------------------------------------------------------------------- #
class Project:
    def __init__(self, root: Path, extra_metadata: Path | None):
        self.root = root
        self.extra_metadata = extra_metadata
        self.config = load_config(root)
        self.files: list[Path] = []
        self.binaries: list[Path] = []
        self._text: dict[Path, str] = {}
        for path in self._walk(root):
            if path.suffix == ".so":
                self.binaries.append(path)
            elif path.suffix in SOURCE_EXT or path.name in {"Podfile", "Info.plist", "Gemfile"}:
                self.files.append(path)

    def _walk(self, folder: Path):
        try:
            entries = sorted(folder.iterdir())
        except OSError:
            return
        for entry in entries:
            if entry.is_dir():
                if entry.name not in SKIP_DIRS and not entry.name.endswith((".xcassets", ".lproj")):
                    yield from self._walk(entry)
            elif entry.is_file():
                yield entry

    def text(self, path: Path) -> str:
        if path not in self._text:
            try:
                data = path.read_bytes()[:MAX_FILE_BYTES]
                self._text[path] = data.decode("utf-8", errors="ignore")
            except OSError:
                self._text[path] = ""
        return self._text[path]

    def rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)

    def by_suffix(self, *suffixes: str) -> list[Path]:
        return [p for p in self.files if p.suffix in suffixes]

    def by_name(self, *names: str) -> list[Path]:
        return [p for p in self.files if p.name in names]

    def code_files(self, store: str) -> list[Path]:
        common = (".dart", ".js", ".jsx", ".ts", ".tsx", ".cs")
        native = (".swift", ".m", ".mm", ".h") if store == "apple" else (".kt", ".java")
        build = (".pbxproj", ".podspec") if store == "apple" else (".gradle", ".kts", ".toml")
        files = self.by_suffix(*(common + native + build))
        files += self.by_name("Podfile", "pubspec.yaml", "package.json", "Package.swift")
        return [f for f in files if not self._other_platform(f, store)]

    def _other_platform(self, path: Path, store: str) -> bool:
        parts = set(path.relative_to(self.root).parts) if self.root in path.parents else set()
        return ("android" in parts) if store == "apple" else ("ios" in parts or "macos" in parts)

    def search(self, pattern: str, files: list[Path], flags=re.I):
        """Return (path, line) of the first match of pattern in files, else None."""
        rx = re.compile(pattern, flags)
        for path in files:
            text = self.text(path)
            m = rx.search(text)
            if m:
                return path, text.count("\n", 0, m.start()) + 1
        return None

    # ---- platform detection ------------------------------------------------
    def detect(self) -> dict:
        info = {"android": False, "apple": False, "framework": "native"}
        if self.by_name("pubspec.yaml"):
            info["framework"] = "flutter"
        elif any('"react-native"' in self.text(p) for p in self.by_name("package.json")):
            info["framework"] = "react-native"
        elif any(p.name.startswith("capacitor.config") for p in self.files):
            info["framework"] = "capacitor"
        if self.by_name("AndroidManifest.xml") or any(
                "com.android.application" in self.text(p) for p in self.by_suffix(".gradle", ".kts")):
            info["android"] = True
        if any(p.suffix == ".pbxproj" for p in self.files) or self.by_name("Info.plist", "Podfile"):
            info["apple"] = True
        return info


def load_config(root: Path) -> dict:
    """Optional per-project settings in <project>/.store-preflight.json.

    {
      "ai_service_terms": ["BrandA", "BrandB"],   # AI brand names to flag in China-visible metadata
      "ai_endpoints": ["api\\.example-ai\\.com"],  # extra regexes that indicate a third-party AI call
      "ignore": ["apple/design/hidden_features"]  # rule paths to suppress after manual review
    }
    """
    path = root / ".store-preflight.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        sys.exit(f"Invalid {path}: {exc}")


def ai_endpoint_pattern(project: "Project") -> str:
    extra = [p for p in project.config.get("ai_endpoints", []) if p]
    return "|".join([AI_ENDPOINTS] + extra)


def ai_terms_pattern(project: "Project") -> re.Pattern:
    terms = [re.escape(t) for t in project.config.get("ai_service_terms", []) if t]
    return re.compile("|".join([GENERIC_AI_TERMS] + [rf"\b{t}\b" for t in terms]), re.I)


def load_requirements(store: str) -> dict:
    path = SKILL_ROOT / "references" / store / "requirements.json"
    return json.loads(path.read_text(encoding="utf-8"))


def rule(store: str, path: str) -> str:
    return f"references/{store}/rules/{path}.md"


# --------------------------------------------------------------------------- #
# Google Play checks
# --------------------------------------------------------------------------- #
RESTRICTED_PERMISSIONS = {
    # permission: (title, rule, detail)
    "READ_SMS": ("SMS permission", "permissions/sms_call_log",
                 "Only default SMS/Phone/Assistant handlers or approved exceptions may use SMS permissions."),
    "RECEIVE_SMS": ("SMS permission", "permissions/sms_call_log",
                    "Use the SMS Retriever / SMS User Consent API for OTP instead."),
    "SEND_SMS": ("SMS permission", "permissions/sms_call_log",
                 "Only default SMS handlers or approved exceptions may send SMS directly."),
    "RECEIVE_MMS": ("SMS permission", "permissions/sms_call_log", "Restricted to default SMS handlers."),
    "RECEIVE_WAP_PUSH": ("SMS permission", "permissions/sms_call_log", "Restricted to default SMS handlers."),
    "READ_CALL_LOG": ("Call Log permission", "permissions/sms_call_log",
                      "From 2027-01-27 phone-call account verification is no longer an allowed use case."),
    "WRITE_CALL_LOG": ("Call Log permission", "permissions/sms_call_log", "Restricted to default Phone handlers."),
    "PROCESS_OUTGOING_CALLS": ("Call Log permission", "permissions/sms_call_log",
                               "Restricted to default Phone handlers."),
    "MANAGE_EXTERNAL_STORAGE": ("All files access", "permissions/all_files_access",
                                "Only file managers, backup, anti-virus and similar core use cases qualify."),
    "QUERY_ALL_PACKAGES": ("Broad package visibility", "permissions/query_all_packages",
                           "Declare <queries> for the specific packages you need instead."),
    "REQUEST_INSTALL_PACKAGES": ("Install packages", "permissions/request_install_packages",
                                 "Only apps whose core purpose is installing packages qualify."),
    "ACCESS_BACKGROUND_LOCATION": ("Background location", "permissions/location",
                                   "Needs a declaration, prominent disclosure and a video demo."),
    "READ_CONTACTS": ("Contacts access", "permissions/contacts",
                      "Contacts Permissions policy (2027-01-27): use the Contact Picker unless broad access is core."),
    "WRITE_CONTACTS": ("Contacts access", "permissions/contacts",
                       "Contacts Permissions policy (2027-01-27) requires a declaration for broad access."),
    "READ_MEDIA_IMAGES": ("Photo & video access", "permissions/photo_video",
                          "Apps with one-off/infrequent needs must use the system photo picker."),
    "READ_MEDIA_VIDEO": ("Photo & video access", "permissions/photo_video",
                         "Apps with one-off/infrequent needs must use the system photo picker."),
    "USE_EXACT_ALARM": ("Exact alarms", "permissions/exact_alarm",
                        "USE_EXACT_ALARM is reserved for alarm clock and calendar apps."),
    "SCHEDULE_EXACT_ALARM": ("Exact alarms", "permissions/exact_alarm",
                             "Prefer inexact alarms; exact alarms need a user-facing core reason."),
    "USE_FULL_SCREEN_INTENT": ("Full-screen intents", "permissions/full_screen_intent",
                               "Only calling and alarm apps get this by default on Android 14+."),
    "BIND_ACCESSIBILITY_SERVICE": ("Accessibility API", "permissions/accessibility_api",
                                   "Needs a declaration, prominent disclosure and isAccessibilityTool or approval."),
    "BIND_VPN_SERVICE": ("VpnService", "permissions/foreground_service_and_vpn",
                         "Only apps whose core functionality is a VPN may use VpnService."),
}


def manifests(project: Project) -> list[Path]:
    return [p for p in project.by_name("AndroidManifest.xml")
            if "debug" not in p.parts and "androidTest" not in p.parts]


def check_google(project: Project, req: dict, findings: list[Finding]) -> None:
    add = findings.append
    gradle = project.by_suffix(".gradle", ".kts", ".toml", ".properties")
    mans = manifests(project)

    # ---- target SDK ---------------------------------------------------------
    required = req["target_sdk"]["new_apps_and_updates"]
    form_factor = "phone/tablet"
    for m in mans:
        t = project.text(m)
        if "android.hardware.type.watch" in t or "android.hardware.type.automotive" in t:
            required, form_factor = req["target_sdk"]["wear_os_and_automotive"], "Wear OS / Automotive"
        elif "android.software.leanback" in t:
            required, form_factor = req["target_sdk"]["tv_and_xr"], "Android TV"
    found = False
    rx = re.compile(r"targetSdk(?:Version)?\s*(?:=|:)?\s*\(?\s*[\"']?(\d{2})\b")
    for path in gradle:
        for m in rx.finditer(project.text(path)):
            found = True
            level = int(m.group(1))
            if level < required:
                line = project.text(path).count("\n", 0, m.start()) + 1
                add(Finding("google", "REJECTION", "technical", "Target API level",
                            f"targetSdk {level} is below the required API {required}",
                            f"Since {req['target_sdk']['effective']}, new apps and updates ({form_factor}) must "
                            f"target API {required}+ (extension window ends {req['target_sdk']['extension_until']}).",
                            rule("google", "technical/target_api_level"), project.rel(path), line))
    if not found:
        hit = project.search(r"flutter\.targetSdkVersion|targetSdk\s*=\s*\w+\.", gradle)
        add(Finding("google", "WARNING", "technical", "Target API level",
                    "targetSdk is not a literal - verify the resolved value",
                    f"Could not read a numeric targetSdk. Confirm the merged value is >= {required} "
                    "(Flutter: check your Flutter SDK default; Expo: check expo-build-properties).",
                    rule("google", "technical/target_api_level"),
                    project.rel(hit[0]) if hit else "", hit[1] if hit else 0))

    # ---- applicationId ------------------------------------------------------
    hit = project.search(r"applicationId\s*=?\s*[\"']com\.example\.", gradle, 0)
    if hit:
        add(Finding("google", "REJECTION", "technical", "Package name",
                    "applicationId uses the reserved com.example prefix",
                    "Google Play rejects uploads whose package name starts with com.example.",
                    rule("google", "technical/app_bundle_and_signing"), project.rel(hit[0]), hit[1]))

    # ---- Play Billing Library ----------------------------------------------
    min_major = req["play_billing_library"]["min_major"]
    billing_rx = re.compile(
        r"com\.android\.billingclient:billing(?:-ktx)?:(\d+)|billing(?:Client|-ktx|Ktx)?\s*=\s*[\"'](\d+)\.")
    for path in gradle:
        for m in billing_rx.finditer(project.text(path)):
            major = int(m.group(1) or m.group(2))
            if major < min_major:
                add(Finding("google", "REJECTION", "monetization", "Play Billing Library",
                            f"Play Billing Library {major}.x is deprecated",
                            f"Since {req['play_billing_library']['effective']} new apps and updates must use "
                            f"Billing Library {min_major}+ (extension ends "
                            f"{req['play_billing_library']['extension_until']}).",
                            rule("google", "technical/play_billing_library_version"), project.rel(path),
                            project.text(path).count("\n", 0, m.start()) + 1))
    hit = project.search(r"in_app_purchase|purchases_flutter|react-native-iap|react-native-purchases|"
                         r"cordova-plugin-purchase|@capacitor-community/in-app-purchase|flutter_inapp_purchase",
                         project.by_name("pubspec.yaml", "package.json"))
    if hit:
        add(Finding("google", "INFO", "monetization", "Play Billing Library",
                    "Cross-platform purchase plugin detected",
                    f"Make sure the plugin version bundles Play Billing Library {min_major}+.",
                    rule("google", "technical/play_billing_library_version"), project.rel(hit[0]), hit[1]))

    # ---- Manifest permissions & flags --------------------------------------
    seen = set()
    for path in mans:
        try:
            tree = ET.fromstring(project.text(path))
        except ET.ParseError:
            continue
        perms = []
        for tag in ("uses-permission", "uses-permission-sdk-23"):
            perms += [e.get(f"{ANDROID_NS}name", "") for e in tree.iter(tag)]
        perms += [e.get(f"{ANDROID_NS}permission", "") for e in tree.iter("service")]
        for perm in perms:
            short = perm.rsplit(".", 1)[-1]
            if short in RESTRICTED_PERMISSIONS and short not in seen:
                seen.add(short)
                title, rpath, detail = RESTRICTED_PERMISSIONS[short]
                add(Finding("google", "WARNING", "permissions", "Permissions & APIs that access sensitive info",
                            f"{title}: {short}", detail + " A Play Console declaration is required.",
                            rule("google", rpath), project.rel(path), _line_of(project.text(path), short)))
            if perm.startswith("android.permission.health.") and "health" not in seen:
                seen.add("health")
                add(Finding("google", "WARNING", "permissions", "Health Connect",
                            "Health Connect permissions requested",
                            "Complete the Health apps declaration and Health Connect permission declaration; "
                            "only request data types your core feature uses.",
                            rule("google", "permissions/health_connect"), project.rel(path),
                            _line_of(project.text(path), perm)))
        fgs = [e.get(f"{ANDROID_NS}foregroundServiceType", "") for e in tree.iter("service")]
        fgs = [t for t in fgs if t]
        if fgs and "fgs" not in seen:
            seen.add("fgs")
            add(Finding("google", "WARNING", "permissions", "Foreground service types",
                        f"Foreground service types declared: {', '.join(sorted(set(fgs)))}",
                        "Each type needs a Play Console foreground-service declaration with a video. "
                        "Geofencing stops being an approved use case on 2027-01-27 (use the Geofence API).",
                        rule("google", "permissions/foreground_service_and_vpn"), project.rel(path),
                        _line_of(project.text(path), "foregroundServiceType")))
        if "ACCESS_FINE_LOCATION" in "".join(perms) and "fine" not in seen:
            seen.add("fine")
            add(Finding("google", "INFO", "permissions", "Location Permissions",
                        "Precise location requested",
                        "From 2027-01-27 the location button is the recommended minimum scope for precise "
                        "location; request ACCESS_COARSE_LOCATION unless precision is essential.",
                        rule("google", "permissions/location"), project.rel(path),
                        _line_of(project.text(path), "ACCESS_FINE_LOCATION")))
        app = tree.find("application")
        if app is not None and app.get(f"{ANDROID_NS}debuggable") == "true":
            add(Finding("google", "REJECTION", "technical", "App bundle requirements",
                        "android:debuggable=\"true\" in a shipped manifest",
                        "Play Console refuses debuggable bundles. Remove the attribute; build types set it.",
                        rule("google", "technical/app_bundle_and_signing"), project.rel(path),
                        _line_of(project.text(path), "debuggable")))

    # ---- 16 KB page size ------------------------------------------------------
    check_elf_alignment(project, req, findings)

    # ---- Store listing --------------------------------------------------------
    check_play_listing(project, req, findings)


def _line_of(text: str, needle: str) -> int:
    idx = text.find(needle)
    return text.count("\n", 0, idx) + 1 if idx >= 0 else 0


def elf_max_load_align(path: Path) -> int | None:
    """Smallest p_align of PT_LOAD segments for a 64-bit ELF, None if not ELF64."""
    try:
        with path.open("rb") as fh:
            ident = fh.read(64)
            if ident[:4] != b"\x7fELF" or ident[4] != 2:
                return None
            endian = "<" if ident[5] == 1 else ">"
            phoff, = struct.unpack(endian + "Q", ident[32:40])
            phentsize, phnum = struct.unpack(endian + "HH", ident[54:58])
            aligns = []
            for i in range(phnum):
                fh.seek(phoff + i * phentsize)
                ph = fh.read(56)
                p_type, = struct.unpack(endian + "I", ph[:4])
                if p_type == 1:  # PT_LOAD
                    aligns.append(struct.unpack(endian + "Q", ph[48:56])[0])
            return min(aligns) if aligns else None
    except (OSError, struct.error):
        return None


def check_elf_alignment(project: Project, req: dict, findings: list[Finding]) -> None:
    date = req["page_size_16kb"]["updates_blocked_from"]
    bad = []
    for so in project.binaries:
        if not any(abi in so.parts for abi in ("arm64-v8a", "x86_64")):
            continue
        align = elf_max_load_align(so)
        if align is not None and align < 16384:
            bad.append(f"{project.rel(so)} (p_align={align})")
    if bad:
        findings.append(Finding(
            "google", "REJECTION", "technical", "16 KB page size",
            f"{len(bad)} native librar{'y is' if len(bad) == 1 else 'ies are'} not 16 KB aligned",
            f"Apps targeting API 35+ must support 16 KB pages; from {date} updates that don't are blocked. "
            "Rebuild with NDK r28+ or update the SDK that ships: " + "; ".join(bad[:5]),
            rule("google", "technical/sixteen_kb_page_size"), bad[0].split(" ")[0]))
        return
    native = project.search(r"externalNativeBuild|ndkVersion|cmake\s*\{", project.by_suffix(".gradle", ".kts"))
    framework = project.detect()["framework"]
    if native or framework in {"flutter", "react-native"}:
        findings.append(Finding(
            "google", "INFO", "technical", "16 KB page size",
            "Native code is bundled - verify 16 KB alignment of the final AAB",
            "Check Play Console > App bundle explorer > Memory page size, or run "
            "`zipalign -c -P 16 -v 4 app.apk` and `check_elf_alignment.sh`.",
            rule("google", "technical/sixteen_kb_page_size"),
            project.rel(native[0]) if native else "", native[1] if native else 0))


PLAY_TITLE_BANNED = re.compile(
    r"\b(best|#1|no\.?\s?1|top|number one|free|new|hot|sale|discount|download now|install now|"
    r"million downloads|app of the year)\b", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
APPLE_TERMS = re.compile(r"\b(iOS|iPhone|iPad|App Store|Apple Watch|TestFlight)\b")
ANDROID_TERMS = re.compile(r"\b(Android|Google Play|Play Store|Galaxy Store|Samsung Galaxy|Pixel)\b", re.I)


def check_play_listing(project: Project, req: dict, findings: list[Finding]) -> None:
    limits = req["listing_limits"]
    roots = [p for p in project.root.glob("**/metadata/android/*")
             if p.is_dir() and not SKIP_DIRS & set(p.relative_to(project.root).parts)]
    if project.extra_metadata:
        roots += [p for p in project.extra_metadata.glob("android/*") if p.is_dir()]
    for loc in roots:
        for name, limit in (("title", limits["title"]), ("short_description", limits["short_description"]),
                            ("full_description", limits["full_description"])):
            f = loc / f"{name}.txt"
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8", errors="ignore").strip()
            rel = project.rel(f)
            if len(text) > limit:
                findings.append(Finding("google", "REJECTION", "metadata", "Store listing",
                                        f"{name} is {len(text)} chars (max {limit})",
                                        "Play Console rejects listings over the character limit.",
                                        rule("google", "metadata/store_listing"), rel))
            if name in ("title", "short_description"):
                m = PLAY_TITLE_BANNED.search(text)
                if m:
                    findings.append(Finding("google", "WARNING", "metadata", "Metadata policy",
                                            f"{name} contains promotional term \"{m.group(0)}\"",
                                            "Titles, icons and developer names must not use ranking, price or "
                                            "promotional claims or calls to action.",
                                            rule("google", "metadata/store_listing"), rel))
                if EMOJI.search(text):
                    findings.append(Finding("google", "WARNING", "metadata", "Metadata policy",
                                            f"{name} contains emoji",
                                            "Emoji, emoticons and repeated special characters are not allowed "
                                            "in the title or short description.",
                                            rule("google", "metadata/store_listing"), rel))
                if re.search(r"\b[A-Z]{4,}\b.*\b[A-Z]{4,}\b", text):
                    findings.append(Finding("google", "WARNING", "metadata", "Metadata policy",
                                            f"{name} uses ALL CAPS",
                                            "All-caps words are only allowed when they are part of your brand.",
                                            rule("google", "metadata/store_listing"), rel))
            m = APPLE_TERMS.search(text)
            if m:
                findings.append(Finding("google", "WARNING", "metadata", "Metadata policy",
                                        f"{name} mentions \"{m.group(0)}\"",
                                        "References to other platforms or stores in a Play listing are "
                                        "misleading or irrelevant metadata.",
                                        rule("google", "metadata/store_listing"), rel))


# --------------------------------------------------------------------------- #
# Apple checks
# --------------------------------------------------------------------------- #
REQUIRED_REASON_APIS = {
    "NSPrivacyAccessedAPICategoryUserDefaults": r"\bUserDefaults\b|NSUserDefaults|shared_preferences|"
                                                r"AsyncStorage|@capacitor/preferences",
    "NSPrivacyAccessedAPICategoryFileTimestamp": r"creationDate|modificationDate|NSFileCreationDate|"
                                                 r"NSFileModificationDate|\bstat\(|getattrlist|lastModified",
    "NSPrivacyAccessedAPICategorySystemBootTime": r"systemUptime|mach_absolute_time",
    "NSPrivacyAccessedAPICategoryDiskSpace": r"volumeAvailableCapacity|NSFileSystemFreeSize|statfs|statvfs",
    "NSPrivacyAccessedAPICategoryActiveKeyboards": r"activeInputModes",
}
USAGE_KEYS = {
    "NSCameraUsageDescription": r"AVCaptureDevice|UIImagePickerController.*camera|image_picker|camera:|"
                                r"react-native-vision-camera|expo-camera",
    "NSPhotoLibraryUsageDescription": r"PHPhotoLibrary|PHPickerViewController.*library|photo_manager",
    "NSMicrophoneUsageDescription": r"AVAudioRecorder|AVAudioSession.*record|requestRecordPermission|record:",
    "NSLocationWhenInUseUsageDescription": r"CLLocationManager|requestWhenInUseAuthorization|geolocator|"
                                          r"expo-location|react-native-geolocation",
    "NSContactsUsageDescription": r"CNContactStore|flutter_contacts|react-native-contacts|expo-contacts",
    "NSCalendarsFullAccessUsageDescription": r"EKEventStore|device_calendar|expo-calendar",
    "NSBluetoothAlwaysUsageDescription": r"CBCentralManager|CBPeripheralManager|flutter_blue|react-native-ble",
    "NSFaceIDUsageDescription": r"LAContext|evaluatePolicy|local_auth|react-native-biometrics",
    "NSHealthShareUsageDescription": r"HKHealthStore|\bhealth:\s|react-native-health",
    "NSMotionUsageDescription": r"CMMotionActivityManager|CMPedometer",
    "NSSpeechRecognitionUsageDescription": r"SFSpeechRecognizer|speech_to_text",
}
GENERIC_PURPOSE = re.compile(r"^(this app|app|we)?\s*(needs|requires|uses|wants)\s+(access|permission)"
                             r"(\s+to\s+(your\s+)?\w+)?\.?$|^(required|needed|permission|access)\.?$", re.I)
TRACKING_SDKS = r"ASIdentifierManager|advertisingIdentifier|FBAudienceNetwork|AppsFlyer|Adjust\b|" \
                r"GoogleMobileAds|google_mobile_ads|AppLovin|ironSource|UnityAds"
THIRD_PARTY_LOGIN = r"GoogleSignIn|google_sign_in|FBSDKLoginKit|FacebookLogin|flutter_facebook_auth|" \
                    r"react-native-fbsdk|@react-native-google-signin|LineSDK|KakaoSDK|TwitterKit"
SIWA = r"ASAuthorizationAppleIDProvider|sign_in_with_apple|AppleAuthentication|apple-authentication|" \
       r"SignInWithAppleButton|@invertase/react-native-apple-authentication"
# Generic shapes of hosted generative-AI APIs. Provider-specific hosts or SDK names
# can be added per project through `ai_endpoints` in .store-preflight.json.
AI_ENDPOINTS = r"/v1/chat/completions|/v1/completions|/v1/responses\b|/v1/messages\b|:generateContent|" \
               r":streamGenerateContent|/v1/embeddings|\bLLM(Client|Service|Api|Provider)\b|" \
               r"\b(llm|genai|generative[_-]?ai)[_-]?(client|service|sdk|api)\b|firebase_ai|firebase-ai|FirebaseAI"
EXTERNAL_PAYMENTS = r"\bStripe(Payments|PaymentSheet|SDK)?\b|flutter_stripe|@stripe/stripe-react-native|" \
                    r"Braintree|PayPalCheckout|razorpay|paystack"
REVIEW_DETECTION = r"sandboxReceipt|appStoreReceiptURL[^\n]{0,80}sandbox|isTestFlight|isRunningInTestFlight|" \
                   r"isReviewMode|reviewMode\s*[=:]|isAppReview|inReview\s*[=:]"
ACCOUNT_SIGNUP = r"createUser(WithEmailAndPassword)?|signUp\(|registerUser|createAccount|/register\b|/signup\b"
ACCOUNT_DELETE = r"delete[_ ]?account|deleteAccount|deleteUser|account[_ ]?deletion|removeAccount|" \
                 r"user\.delete\(|\.delete\(\)\s*//\s*account"
# Generic wording; brand names of AI services are supplied per project via
# `ai_service_terms` in .store-preflight.json (see README > Configuration).
GENERIC_AI_TERMS = r"\bAI (chat|chatbot|assistant|companion)\b|\bLLM\b|large language model|generative AI"
ENTITLEMENT_USAGE = {
    "com.apple.developer.healthkit": r"HKHealthStore|\bhealth\b",
    "com.apple.developer.homekit": r"HMHomeManager",
    "com.apple.developer.icloud-container-identifiers": r"CKContainer|NSUbiquitous|ubiquity|CloudKit",
    "com.apple.developer.nfc.readersession.formats": r"NFCNDEFReaderSession|NFCTagReaderSession|nfc_manager",
    "com.apple.developer.siri": r"INExtension|INIntent|AppIntent",
    "com.apple.developer.applesignin": SIWA,
    "aps-environment": r"registerForRemoteNotifications|firebase_messaging|messaging\(\)|"
                       r"UNUserNotificationCenter|expo-notifications|OneSignal",
    "com.apple.developer.associated-domains": r"userActivity|NSUserActivity|continue\s+userActivity|"
                                              r"universal|app_links|uni_links|Linking",
    "com.apple.developer.in-app-payments": r"PKPaymentAuthorization|ApplePay|pay\b",
}


def plist_load(project: Project, path: Path) -> dict:
    try:
        return plistlib.loads(path.read_bytes())
    except Exception:  # noqa: BLE001 - malformed or templated plist
        return {}


def check_apple(project: Project, req: dict, findings: list[Finding]) -> None:
    add = findings.append
    code = project.code_files("apple")
    plists = [p for p in project.by_name("Info.plist") if "Tests" not in str(p)]
    info: dict = {}
    for p in plists:
        info.update(plist_load(project, p))
    plist_rel = project.rel(plists[0]) if plists else ""

    # ---- Privacy manifest (5.1.1 / ITMS-91053) -----------------------------
    manifests_ = project.by_suffix(".xcprivacy")
    declared = set()
    for m in manifests_:
        for entry in plist_load(project, m).get("NSPrivacyAccessedAPITypes", []) or []:
            declared.add(entry.get("NSPrivacyAccessedAPIType"))
    for category, pattern in REQUIRED_REASON_APIS.items():
        hit = project.search(pattern, code)
        if not hit:
            continue
        if not manifests_:
            add(Finding("apple", "REJECTION", "privacy", "5.1.1 / ITMS-91053",
                        "Required-reason API used but no PrivacyInfo.xcprivacy",
                        f"{category} usage detected. Uploads without a privacy manifest that declares an "
                        "approved reason are rejected.", rule("apple", "privacy/privacy_manifest"),
                        project.rel(hit[0]), hit[1]))
            break
        if category not in declared:
            add(Finding("apple", "WARNING", "privacy", "5.1.1 / ITMS-91053",
                        f"{category} not declared in PrivacyInfo.xcprivacy",
                        "Add the category with an approved reason code (e.g. CA92.1 for UserDefaults).",
                        rule("apple", "privacy/privacy_manifest"), project.rel(hit[0]), hit[1]))

    # ---- Purpose strings (5.1.1(ii)) ----------------------------------------
    if plists:
        for key, pattern in USAGE_KEYS.items():
            value = info.get(key)
            alt = key.replace("WhenInUse", "AlwaysAndWhenInUse").replace("FullAccess", "")
            hit = project.search(pattern, code)
            if hit and value is None and info.get(alt) is None:
                add(Finding("apple", "REJECTION", "privacy", "5.1.1(ii) / ITMS-90683",
                            f"{key} missing from Info.plist",
                            "The app references an API that needs a purpose string; the upload is rejected "
                            "and the app crashes when the permission is requested.",
                            rule("apple", "privacy/purpose_strings"), project.rel(hit[0]), hit[1]))
        for key, value in info.items():
            if key.endswith("UsageDescription") and isinstance(value, str):
                v = value.strip()
                if len(v) < 20 or GENERIC_PURPOSE.match(v):
                    add(Finding("apple", "WARNING", "privacy", "5.1.1(ii)",
                                f"{key} is vague: \"{v}\"",
                                "Explain what the data is used for with a concrete example.",
                                rule("apple", "privacy/purpose_strings"), plist_rel))

    # ---- ATT (5.1.2) ---------------------------------------------------------
    tracking = project.search(TRACKING_SDKS, code)
    att_prompt = project.search(r"ATTrackingManager|requestTrackingAuthorization|app_tracking_transparency|"
                                r"expo-tracking-transparency|react-native-tracking-transparency", code)
    if tracking and "NSUserTrackingUsageDescription" not in info and plists:
        add(Finding("apple", "WARNING", "privacy", "5.1.2",
                    "Tracking/ads SDK without NSUserTrackingUsageDescription",
                    "If the SDK tracks users you must request App Tracking Transparency permission first.",
                    rule("apple", "privacy/app_tracking_transparency"), project.rel(tracking[0]), tracking[1]))
    if "NSUserTrackingUsageDescription" in info and not att_prompt:
        add(Finding("apple", "WARNING", "privacy", "2.1 / 5.1.2",
                    "NSUserTrackingUsageDescription present but ATT is never requested",
                    "Reviewers reject apps that declare tracking but never show the ATT prompt.",
                    rule("apple", "privacy/app_tracking_transparency"), plist_rel))

    # ---- Sign in with Apple / login services (4.8) ---------------------------
    login = project.search(THIRD_PARTY_LOGIN, code)
    if login and not project.search(SIWA, code):
        add(Finding("apple", "WARNING", "design", "4.8",
                    "Third-party login without Sign in with Apple (or equivalent)",
                    "Apps offering third-party/social login must also offer an equivalent privacy-focused "
                    "login option such as Sign in with Apple.",
                    rule("apple", "design/sign_in_with_apple"), project.rel(login[0]), login[1]))

    # ---- Hidden features (2.5.19) -------------------------------------------
    hit = project.search(REVIEW_DETECTION, code)
    if hit:
        add(Finding("apple", "WARNING", "design", "2.5.19",
                    "Review/TestFlight environment detection in code",
                    "Changing behaviour for reviewers is bait-and-switch. Make sure this only affects "
                    "diagnostics, never feature availability.",
                    rule("apple", "design/hidden_features"), project.rel(hit[0]), hit[1]))

    # ---- Third-party payments for digital goods (3.1.1) ----------------------
    hit = project.search(EXTERNAL_PAYMENTS, code)
    if hit:
        add(Finding("apple", "WARNING", "subscription", "3.1.1 / 3.1.3",
                    "External payment SDK detected",
                    "Digital content and features must use In-App Purchase. External payments are fine for "
                    "physical goods and services consumed outside the app.",
                    rule("apple", "subscription/in_app_purchase"), project.rel(hit[0]), hit[1]))

    # ---- Entitlements (2.4.5 / unused) ---------------------------------------
    is_mac = project.search(r"SDKROOT\s*=\s*macosx", project.by_suffix(".pbxproj")) is not None
    for ent in project.by_suffix(".entitlements"):
        data = plist_load(project, ent)
        for key in data:
            if key.startswith("com.apple.security.temporary-exception"):
                add(Finding("apple", "WARNING", "entitlements", "2.4.5(i)",
                            f"Temporary exception entitlement {key}",
                            "Apple asks you to justify every temporary exception; remove it if unused.",
                            rule("apple", "entitlements/unused_entitlements"), project.rel(ent)))
            pattern = ENTITLEMENT_USAGE.get(key)
            if pattern and not project.search(pattern, code):
                add(Finding("apple", "WARNING", "entitlements", "2.4.5(i) / 2.5.1",
                            f"Entitlement {key} has no matching code",
                            "Remove capabilities the app does not use; reviewers ask about unused ones.",
                            rule("apple", "entitlements/unused_entitlements"), project.rel(ent)))
        if is_mac and "macos" in str(ent).lower() and not data.get("com.apple.security.app-sandbox"):
            add(Finding("apple", "REJECTION", "entitlements", "2.4.5(i)",
                        "Mac app is not sandboxed",
                        "Mac App Store apps must enable com.apple.security.app-sandbox.",
                        rule("apple", "entitlements/unused_entitlements"), project.rel(ent)))

    # ---- Deployment target ----------------------------------------------------
    min_ios = req["deployment_target_minimum"]["ios"]
    rx = re.compile(r"IPHONEOS_DEPLOYMENT_TARGET\s*=\s*(\d+)(?:\.\d+)?|platform\s+:ios,\s*['\"](\d+)")
    for path in project.by_suffix(".pbxproj") + project.by_name("Podfile"):
        for m in rx.finditer(project.text(path)):
            ver = int(m.group(1) or m.group(2))
            if ver < min_ios:
                add(Finding("apple", "REJECTION", "technical", "Upload requirements",
                            f"iOS deployment target {ver} is below the minimum iOS {min_ios}",
                            f"Since {req['deployment_target_minimum']['effective']} uploads must target "
                            f"iOS {min_ios} or later. Also build with Xcode {req['sdk_minimum']['xcode']}+.",
                            rule("apple", "technical/sdk_requirements"), project.rel(path),
                            project.text(path).count("\n", 0, m.start()) + 1))
                break

    # ---- Metadata ---------------------------------------------------------------
    check_apple_metadata(project, req, findings)


def _apple_metadata_fields(project: Project):
    """Yield (locale, field, text, path) from per-locale text files or App Store Connect JSON exports."""
    names = {"name", "subtitle", "keywords", "promotional_text", "description", "release_notes"}
    roots = [p for p in project.root.glob("**/metadata")
             if p.is_dir() and not SKIP_DIRS & set(p.relative_to(project.root).parts)]
    if project.extra_metadata:
        roots.append(project.extra_metadata)
    for base in roots:
        for f in base.glob("*/*.txt"):
            if f.parent.name in {"android", "review_information", "trade_representative_contact_information"}:
                continue
            if f.stem in names:
                yield f.parent.name, f.stem, f.read_text(encoding="utf-8", errors="ignore").strip(), f
        for f in list(base.glob("app-info/*.json")) + list(base.glob("version/*/*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for key, value in data.items():
                k = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
                k = "release_notes" if k == "whats_new" else k
                if k in names and isinstance(value, str):
                    yield f.stem, k, value.strip(), f


def check_apple_metadata(project: Project, req: dict, findings: list[Finding]) -> None:
    limits = dict(req["metadata_limits"], release_notes=req["metadata_limits"]["whats_new"])
    ai_terms = ai_terms_pattern(project)
    for locale, field_, text, path in _apple_metadata_fields(project):
        rel = project.rel(path)
        if field_ in limits and len(text) > limits[field_]:
            findings.append(Finding("apple", "REJECTION", "metadata", "2.3.7",
                                    f"[{locale}] {field_} is {len(text)} chars (max {limits[field_]})",
                                    "App Store Connect rejects metadata over the limit.",
                                    rule("apple", "metadata/accurate_metadata"), rel))
        m = ANDROID_TERMS.search(text)
        if m:
            findings.append(Finding("apple", "REJECTION", "metadata", "2.3.10",
                                    f"[{locale}] {field_} mentions \"{m.group(0)}\"",
                                    "Metadata must not reference other mobile platforms or marketplaces.",
                                    rule("apple", "metadata/competitor_terms"), rel))
        m = ai_terms.search(text)
        if m:
            findings.append(Finding("apple", "WARNING", "metadata", "5 (China)",
                                    f"[{locale}] {field_} mentions \"{m.group(0)}\"",
                                    "Unlicensed generative-AI services are blocked in China mainland; Apple "
                                    "checks every locale shown on that storefront.",
                                    rule("apple", "metadata/china_storefront"), rel))
        if field_ in {"name", "subtitle", "keywords"} and re.search(r"[$€£¥₫]\s?\d|\bfree\b|\bsale\b", text, re.I):
            findings.append(Finding("apple", "WARNING", "metadata", "2.3.7",
                                    f"[{locale}] {field_} contains pricing/promotional terms",
                                    "Don't put prices or promotions in the name, subtitle or keywords.",
                                    rule("apple", "metadata/accurate_metadata"), rel))


# --------------------------------------------------------------------------- #
# Checks that apply to both stores
# --------------------------------------------------------------------------- #
def check_shared(project: Project, store: str, findings: list[Finding]) -> None:
    code = project.code_files(store)
    signup = project.search(ACCOUNT_SIGNUP, code)
    if signup and not project.search(ACCOUNT_DELETE, code):
        if store == "apple":
            g, r = "5.1.1(v)", rule("apple", "privacy/account_deletion")
        else:
            g, r = "User Data - account deletion", rule("google", "privacy/account_deletion")
        findings.append(Finding(store, "WARNING", "privacy", g,
                                "Account creation found but no account deletion flow",
                                "Apps that let users create accounts must let them delete the account (and "
                                "data) from within the app" + (" and via a web link." if store == "google" else "."),
                                r, project.rel(signup[0]), signup[1]))
    ai = project.search(ai_endpoint_pattern(project), code)
    if ai:
        if store == "apple":
            findings.append(Finding("apple", "WARNING", "privacy", "5.1.2(i)",
                                    "Third-party AI service detected",
                                    "Name the AI provider and get explicit consent before sending personal data.",
                                    rule("apple", "privacy/third_party_ai_consent"), project.rel(ai[0]), ai[1]))
        else:
            findings.append(Finding("google", "WARNING", "content", "AI-Generated Content",
                                    "Generative AI feature detected",
                                    "Provide in-app reporting of offensive AI output, prevent restricted content, "
                                    "and disclose AI data sharing in the Data safety form.",
                                    rule("google", "content/ai_generated_content"), project.rel(ai[0]), ai[1]))
    if store == "google":
        pay = project.search(EXTERNAL_PAYMENTS, code)
        if pay:
            findings.append(Finding("google", "WARNING", "monetization", "Payments",
                                    "External payment SDK detected",
                                    "Digital goods must use Google Play Billing unless an alternative-billing or "
                                    "external-offers program applies in that region.",
                                    rule("google", "monetization/play_billing"), project.rel(pay[0]), pay[1]))


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
ICON = {"REJECTION": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}
STORE_NAME = {"apple": "🍎 App Store", "google": "🤖 Google Play"}


def render_md(findings: list[Finding], stores: list[str], info: dict) -> str:
    out = ["# Preflight scan (automated checks)", "",
           f"- **Project:** {info['framework']} · Android: {'yes' if info['android'] else 'no'} · "
           f"Apple: {'yes' if info['apple'] else 'no'}",
           f"- **Stores checked:** {', '.join(STORE_NAME[s] for s in stores)}", ""]
    for store in stores:
        items = sorted((f for f in findings if f.store == store), key=lambda f: SEVERITY_ORDER[f.severity])
        counts = {s: sum(1 for f in items if f.severity == s) for s in SEVERITY_ORDER}
        out += [f"## {STORE_NAME[store]}", "",
                f"❌ {counts['REJECTION']} rejection · ⚠️ {counts['WARNING']} warning · ℹ️ {counts['INFO']} info", ""]
        if not items:
            out += ["✅ No automated findings. Continue with the manual checklist.", ""]
        for f in items:
            loc = f" — `{f.file}{':' + str(f.line) if f.line else ''}`" if f.file else ""
            out.append(f"- {ICON[f.severity]} **[{f.guideline}] {f.title}**{loc}")
            out.append(f"  - {f.detail}")
            out.append(f"  - Rule: `{f.rule}`")
        out.append("")
    out.append("_Automated checks cover only what can be detected statically. "
               "Run the manual checklist in SKILL.md before submitting._")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", nargs="?", default=".", type=Path)
    ap.add_argument("--store", choices=["auto", "apple", "google", "all"], default="auto")
    ap.add_argument("--only", help="comma-separated categories")
    ap.add_argument("--metadata", type=Path, help="extra metadata directory")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--strict", action="store_true", help="exit 2 if any REJECTION is found")
    args = ap.parse_args(argv)

    root = args.project.resolve()
    if not root.is_dir():
        ap.error(f"{root} is not a directory")
    project = Project(root, args.metadata.resolve() if args.metadata else None)
    info = project.detect()
    if args.store == "auto":
        stores = [s for s, k in (("apple", "apple"), ("google", "android")) if info[k]] or ["apple", "google"]
    elif args.store == "all":
        stores = ["apple", "google"]
    else:
        stores = [args.store]

    findings: list[Finding] = []
    if "apple" in stores:
        check_apple(project, load_requirements("apple"), findings)
        check_shared(project, "apple", findings)
    if "google" in stores:
        check_google(project, load_requirements("google"), findings)
        check_shared(project, "google", findings)
    ignored = {i.strip().removesuffix(".md").removeprefix("references/").replace("/rules/", "/")
               for i in project.config.get("ignore", [])}
    findings = [f for f in findings
                if f.rule.removesuffix(".md").removeprefix("references/").replace("/rules/", "/") not in ignored]
    if args.only:
        cats = {c.strip() for c in args.only.split(",")}
        findings = [f for f in findings if f.category in cats]

    if args.format == "json":
        print(json.dumps({"project": info, "stores": stores,
                          "findings": [asdict(f) for f in findings]}, indent=2, ensure_ascii=False))
    else:
        print(render_md(findings, stores, info))
    if args.strict and any(f.severity == "REJECTION" for f in findings):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
