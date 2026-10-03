#!/usr/bin/env python3
"""Check the only website source tree, its local links and recorded SHA-256 hashes."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

REPOSITORY = Path(__file__).resolve().parent.parent
ALLOWED_SUFFIXES = {".html", ".css", ".js", ".json", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico", ".txt", ".xml"}
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.IGNORECASE)


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        for attribute in ("href", "src"):
            if attributes.get(attribute):
                self.links.append(attributes[attribute])
        if attributes.get("style"):
            self.links.extend(CSS_URL.findall(attributes["style"]))
        if attributes.get("srcset"):
            self.links.extend(item.strip().split()[0] for item in attributes["srcset"].split(",") if item.strip())


def source_hashes(root):
    root = Path(root).absolute()
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Site root must be a regular directory")
    hashes = {}
    for path in sorted(root.rglob("*")):
        name = path.relative_to(root).as_posix()
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError(f"Unsupported source entry: {name}")
        if path.is_dir():
            if any(part.startswith(".") for part in Path(name).parts):
                raise ValueError(f"Hidden source directory cannot be published: {name}")
            continue
        if name == "deployment.json":
            # CI generates provenance after source checks, using the actual commit.
            continue
        if name != ".nojekyll" and (path.suffix.lower() not in ALLOWED_SUFFIXES or any(part.startswith(".") for part in Path(name).parts)):
            raise ValueError(f"Only public website assets belong in site/: {name}")
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    if "index.html" not in hashes or ".nojekyll" not in hashes:
        raise ValueError("site/index.html and site/.nojekyll are required")
    return hashes


def revision_hash(hashes):
    payload = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_site(root):
    root = Path(root).resolve()
    pages = {}
    for path in sorted(root.rglob("*.html")):
        parsed = PageLinks()
        parsed.feed(path.read_text(encoding="utf-8"))
        pages[path] = parsed
    references = [(path, link) for path, parsed in pages.items() for link in parsed.links]
    for path in sorted(root.rglob("*.css")):
        references.extend((path, link) for link in CSS_URL.findall(path.read_text(encoding="utf-8")))
    link_count = 0
    for path, link in references:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        if url.path.startswith("/"):
            raise ValueError(f"Root-relative link is not portable: {path.relative_to(root)} → {link}")
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.is_relative_to(root):
            raise ValueError(f"Link leaves site: {path.relative_to(root)} → {link}")
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            raise ValueError(f"Missing link target: {path.relative_to(root)} → {link}")
        if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            raise ValueError(f"Missing fragment: {path.relative_to(root)} → {link}")
        link_count += 1
    return len(pages), link_count


def check_manifest(root, manifest):
    hashes = source_hashes(root)
    recorded = manifest["files_sha256"]
    if hashes != recorded:
        missing = sorted(set(recorded) - set(hashes))
        extra = sorted(set(hashes) - set(recorded))
        changed = sorted(name for name in set(hashes) & set(recorded) if hashes[name] != recorded[name])
        raise ValueError(f"Manifest mismatch: missing={missing}, extra={extra}, changed={changed}. Run scripts/update_manifest.py after reviewing intended changes.")
    if manifest.get("source_repository") != "Oooscar8/alexchaoflow-website" or manifest.get("source_directory") != "site":
        raise ValueError("Current source must be this repository's site/ directory")
    if manifest.get("source_revision") != {"type": "sha256-file-manifest", "sha256": revision_hash(hashes)}:
        raise ValueError("Source revision must match the complete file manifest")
    return hashes


def validate_releases(root):
    root = Path(root).resolve()
    metadata_path = root / "jianshan" / "releases.json"
    if not metadata_path.is_file():
        raise ValueError("Missing jianshan/releases.json")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("schema_version") != 1 or metadata.get("app_id") != "com.oooscar8.AssetTrack":
        raise ValueError("Unsupported release metadata schema or app identifier")
    releases = metadata.get("releases")
    if not isinstance(releases, list) or not releases:
        raise ValueError("At least one truthful release status is required")
    identities = set()
    for release in releases:
        version, build, state = (release.get(key) for key in ("version", "build", "state"))
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("Release version must be a three-component string")
        if not isinstance(build, str) or not re.fullmatch(r"[1-9]\d*", build):
            raise ValueError("Release build must be a positive integer string")
        if state not in {"prepared", "testflight", "published"}:
            raise ValueError("Unknown release state")
        identity = version
        if identity in identities:
            raise ValueError("Each marketing version must have exactly one current build/state record")
        identities.add(identity)
        if release.get("notes_url") != f"https://alexchaoflow.com/jianshan/releases/{version}/":
            raise ValueError("Release notes must use the canonical version path")
        notes = root / "jianshan" / "releases" / version / "index.html"
        if not notes.is_file() or hashlib.sha256(notes.read_bytes()).hexdigest() != release.get("notes_sha256"):
            raise ValueError("Release notes file and notes_sha256 must match")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(release.get("updated_at", ""))):
            raise ValueError("Release updated_at must be YYYY-MM-DD")
        app_store = release.get("app_store_url")
        testflight = release.get("testflight_url")
        if state == "prepared" and (app_store is not None or testflight is not None):
            raise ValueError("Prepared releases cannot advertise download URLs")
        if state == "testflight" and (app_store is not None or (testflight is not None and not re.fullmatch(r"https://testflight\.apple\.com/join/[A-Za-z0-9]+", str(testflight)))):
            raise ValueError("TestFlight releases may only use an Apple public invitation URL")
        if state == "published" and (testflight is not None or not re.fullmatch(r"https://apps\.apple\.com/(?:[A-Za-z]{2}/)?app/(?:[^/?#]+/)?id\d+(?:\?[^#]*)?", str(app_store))):
            raise ValueError("Published releases require a real-format Apple App Store URL")
    return len(releases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=REPOSITORY / "site")
    parser.add_argument("--manifest", type=Path, default=REPOSITORY / "DEPLOYMENT.json")
    args = parser.parse_args()
    try:
        hashes = check_manifest(args.site, json.loads(args.manifest.read_text(encoding="utf-8")))
        pages, links = validate_site(args.site)
        releases = validate_releases(args.site)
    except (OSError, ValueError, KeyError) as error:
        print(f"Site check failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"html_pages": pages, "local_references": links, "files": len(hashes), "releases": releases, "source_revision": revision_hash(hashes)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
