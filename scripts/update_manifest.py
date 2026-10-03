#!/usr/bin/env python3
"""Refresh local website file hashes after reviewing an intentional source change."""
import json
from check_site import REPOSITORY, revision_hash, source_hashes, validate_site


def main():
    site = REPOSITORY / "site"
    hashes = source_hashes(site)
    pages, links = validate_site(site)
    manifest_path = REPOSITORY / "DEPLOYMENT.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_repository"] = "Oooscar8/alexchaoflow-website"
    manifest["source_directory"] = "site"
    manifest["source_revision"] = {"type": "sha256-file-manifest", "sha256": revision_hash(hashes)}
    manifest["files_sha256"] = hashes
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {len(hashes)} file hashes; {pages} HTML pages and {links} local references checked. No deployment or historical report was changed.")


if __name__ == "__main__":
    main()
