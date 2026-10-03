import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_site import validate_releases


class ReleaseValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        notes = self.root / "jianshan/releases/1.0.0/index.html"
        notes.parent.mkdir(parents=True)
        notes.write_text("Prepared fixture")
        self.record = {"version": "1.0.0", "build": "2", "state": "prepared", "updated_at": "2026-10-03",
                       "notes_url": "https://alexchaoflow.com/jianshan/releases/1.0.0/",
                       "notes_sha256": hashlib.sha256(notes.read_bytes()).hexdigest(),
                       "app_store_url": None, "testflight_url": None}

    def write(self, records=None):
        (self.root / "jianshan/releases.json").write_text(json.dumps({
            "schema_version": 1, "app_id": "com.oooscar8.AssetTrack", "releases": records or [self.record]}))

    def test_prepared_without_download_passes(self):
        self.write()
        self.assertEqual(validate_releases(self.root), 1)

    def test_prepared_cannot_advertise_download(self):
        self.record["app_store_url"] = "https://apps.apple.com/app/id123456"
        self.write()
        with self.assertRaisesRegex(ValueError, "Prepared releases"):
            validate_releases(self.root)

    def test_notes_bytes_must_match(self):
        self.record["notes_sha256"] = "0" * 64
        self.write()
        with self.assertRaisesRegex(ValueError, "notes_sha256"):
            validate_releases(self.root)

    def test_published_requires_apple_download(self):
        self.record.update(state="published", app_store_url="https://example.com/download")
        self.write()
        with self.assertRaisesRegex(ValueError, "App Store URL"):
            validate_releases(self.root)

    def test_one_current_record_per_marketing_version(self):
        later = dict(self.record, build="3", state="testflight")
        self.write([self.record, later])
        with self.assertRaisesRegex(ValueError, "exactly one current"):
            validate_releases(self.root)

    def test_testflight_private_distribution_has_no_public_link(self):
        self.record["state"] = "testflight"
        self.write()
        self.assertEqual(validate_releases(self.root), 1)


if __name__ == "__main__":
    unittest.main()
