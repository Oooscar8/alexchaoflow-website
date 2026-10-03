#!/usr/bin/env python3
"""Verify a static Pages deployment using normal curl TLS validation."""
import argparse
import concurrent.futures
import hashlib
import ipaddress
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def check(item, resolve_entries):
    url, expected_url, expected_hash = item
    with tempfile.TemporaryDirectory(prefix="jianshan-domain-check-") as temporary:
        body = Path(temporary) / "body"
        resolve_options = [value for entry in resolve_entries for value in ("--resolve", entry)]
        proxy_options = ["--noproxy", "*"] if resolve_entries else []
        result = subprocess.run(
            ["curl", "-q", "--silent", "--show-error", "--location", "--max-time", "25",
             "--proto", "=http,https", "--proto-redir", "=http,https",
             "--output", str(body), "--write-out", "%{json}"] + proxy_options + resolve_options + [url],
            text=True, capture_output=True, check=False,
        )
        try:
            meta = json.loads(result.stdout)
        except json.JSONDecodeError:
            meta = {}
        digest = hashlib.sha256(body.read_bytes()).hexdigest() if body.exists() else None
        entry = {
            "url": url,
            "expected_final_url": expected_url,
            "curl_exit": result.returncode,
            "http_status": meta.get("http_code"),
            "final_url": meta.get("url_effective"),
            "redirect_count": meta.get("num_redirects"),
            "tls_verify_result": meta.get("ssl_verify_result"),
            "remote_ip": meta.get("remote_ip"),
            "body_sha256": digest,
            "error": result.stderr.strip() or None,
        }
        if expected_hash is not None:
            entry["expected_sha256"] = expected_hash
        entry["passed"] = (
            result.returncode == 0 and meta.get("http_code") == 200
            and meta.get("url_effective") == expected_url
            and expected_url.startswith("https://")
            and meta.get("ssl_verify_result") == 0
            and (expected_hash is None or digest == expected_hash)
            and (url == expected_url or meta.get("num_redirects", 0) > 0)
        )
    return entry


def public_resolve_entry(value):
    try:
        host, port, address = value.split(":", 2)
        parsed = ipaddress.ip_address(address.strip("[]"))
        if not host or "/" in host or not 1 <= int(port) <= 65535 or not parsed.is_global:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError("Expected HOST:PORT:PUBLIC_IP (IPv6 may use brackets)") from None
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parents[1] / "DEPLOYMENT.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--website-commit", required=True)
    parser.add_argument("--resolve", action="append", default=[], type=public_resolve_entry,
                        help="Optional explicit public DNS address; recorded as a diagnostic, not system-DNS success.")
    args = parser.parse_args()
    started_at = datetime.now(timezone.utc).isoformat()
    if args.output.exists():
        parser.error("Output already exists; choose a new name to preserve earlier evidence")
    manifest_bytes = args.manifest.read_bytes()
    manifest = json.loads(manifest_bytes)
    script_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    curl_version = subprocess.run(["curl", "-q", "--version"], text=True,
                                  capture_output=True, check=True).stdout.splitlines()[0]
    origin = "https://alexchaoflow.com/"
    items = []
    for name, digest in manifest["files_sha256"].items():
        path = name[:-len("index.html")] if name.endswith("index.html") else name
        items.append((origin + path, origin + path, digest))
    for path in ("", "jianshan/", "jianshan/privacy/", "jianshan/support/"):
        for prefix in ("http://alexchaoflow.com/", "http://www.alexchaoflow.com/",
                       "https://www.alexchaoflow.com/",
                       "https://oooscar8.github.io/alexchaoflow-website/"):
            items.append((prefix + path, origin + path, manifest["files_sha256"][path + "index.html"]))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda item: check(item, args.resolve), items))
    report = {
        "started_at_utc": started_at,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "website_commit": args.website_commit,
        "source_repository": manifest["source_repository"],
        "source_revision": manifest["source_revision"],
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "verification_script_sha256": script_sha256,
        "curl_version": curl_version,
        "dns_mode": "explicit-public-address" if args.resolve else "system-resolver",
        "resolve_entries": args.resolve,
        "proxy_mode": "disabled-for-explicit-address" if args.resolve else "environment-default",
        "curl_config_file_disabled": True,
        "tls_validation_disabled": False,
        "checks": results,
        "total": len(results),
        "passed": sum(item["passed"] for item in results),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output:
        output.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"total": report["total"], "passed": report["passed"],
                      "failures": [item for item in results if not item["passed"]]}, ensure_ascii=False))
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
