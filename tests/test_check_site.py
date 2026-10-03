import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_site import check_manifest, revision_hash, source_hashes, validate_site


class SiteValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / ".nojekyll").touch()
        (self.root / "index.html").write_text('<main id="main"><a href="#main">Home</a></main>', encoding="utf-8")

    def test_valid_relative_page_fragment_and_css_image(self):
        (self.root / "app").mkdir()
        (self.root / "app" / "index.html").write_text('<link href="../style.css" rel="stylesheet"><a href="../#main">Home</a>')
        (self.root / "style.css").write_text('body{background:url("image.png")}')
        (self.root / "image.png").write_bytes(b"fixture")
        self.assertEqual(validate_site(self.root), (2, 4))

    def test_missing_file_fails(self):
        (self.root / "index.html").write_text('<img src="missing.png">')
        with self.assertRaisesRegex(ValueError, "Missing link target"):
            validate_site(self.root)

    def test_missing_fragment_fails(self):
        (self.root / "index.html").write_text('<a href="#absent">Broken</a>')
        with self.assertRaisesRegex(ValueError, "Missing fragment"):
            validate_site(self.root)

    def test_encoded_parent_escape_fails(self):
        (self.root / "index.html").write_text('<a href="%2e%2e/outside.html">Escape</a>')
        with self.assertRaisesRegex(ValueError, "Link leaves site"):
            validate_site(self.root)

    def test_symlink_fails_before_upload(self):
        (self.root / "alias.html").symlink_to(self.root / "index.html")
        with self.assertRaisesRegex(ValueError, "Unsupported source entry"):
            source_hashes(self.root)

    def test_unexpected_private_file_fails(self):
        (self.root / "token.pem").write_text("fixture")
        with self.assertRaisesRegex(ValueError, "Only public website assets"):
            source_hashes(self.root)

    def test_unrecorded_file_and_edited_file_fail(self):
        hashes = source_hashes(self.root)
        manifest = {"source_repository": "Oooscar8/alexchaoflow-website", "source_directory": "site",
                    "source_revision": {"type": "sha256-file-manifest", "sha256": revision_hash(hashes)}, "files_sha256": hashes}
        self.assertEqual(check_manifest(self.root, manifest), hashes)
        (self.root / "new.js").write_text("void 0;")
        with self.assertRaisesRegex(ValueError, "Manifest mismatch"):
            check_manifest(self.root, manifest)
        (self.root / "new.js").unlink()
        (self.root / "index.html").write_text("changed")
        with self.assertRaisesRegex(ValueError, "Manifest mismatch"):
            check_manifest(self.root, manifest)


if __name__ == "__main__":
    unittest.main()
