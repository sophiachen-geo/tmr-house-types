#!/usr/bin/env python3
"""Redact third-party API tokens from saved source pages before they are committed.

Several of the government sites this project archives — the RPCQ in particular —
embed a live Mapbox access token in the HTML they serve. Those pages are kept in
sources/ as the evidence behind each record, but the token is a working
credential belonging to someone else and must not be republished. Run this over
sources/ before every commit; GitHub's push protection will reject the push
otherwise, and it is right to.

Usage:  python3 scrub_secrets.py [--check]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "sources"

PATTERNS = [
    # Mapbox public and secret access tokens (RPCQ map widget)
    (re.compile(r"(sk|pk)\.eyJ[A-Za-z0-9_.-]{20,}"), r"\1.REDACTED-MAPBOX-TOKEN"),
    # Google Maps / generic browser API keys
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "AIza-REDACTED-GOOGLE-API-KEY"),
]


def scan(check_only=False):
    hits = []
    for path in sorted(TARGET.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        new = text
        for pattern, replacement in PATTERNS:
            new = pattern.sub(replacement, new)
        if new != text:
            hits.append(path.relative_to(ROOT))
            if not check_only:
                path.write_text(new, encoding="utf-8")
    return hits


if __name__ == "__main__":
    check = "--check" in sys.argv
    found = scan(check_only=check)
    for f in found:
        print(("would redact " if check else "redacted ") + str(f))
    if check and found:
        sys.exit(f"scrub_secrets.py: {len(found)} file(s) still carry a third-party token")
    print(f"scrub_secrets.py: {len(found)} file(s) {'to redact' if check else 'redacted'}")
