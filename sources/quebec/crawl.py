#!/usr/bin/env python3
"""Crawl the Ville de Québec thésaurus (Répertoire du patrimoine bâti → Styles architecturaux).

Per PART 7 §1.2: fetch the nine courant landing pages + styles.aspx, harvest every tid they
reference, fetch each `thesaurus.aspx?tid=N`, then sweep the known-populated ranges as a safety
net. A page is kept only if it contains the string "Éléments caractéristiques"; anything else is
a 404 shell and is deleted.

One request per second, descriptive User-Agent. Every fetched URL is logged with its date to
crawl_log.tsv, which MANIFEST.md is generated from.
"""
import hashlib
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
HTML = HERE / "html"
BASE = "https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati"
UA = "tmr-house-types research crawler (educational typology documentation)"
MARKER = "Éléments caractéristiques"
LOG = HERE / "crawl_log.tsv"

RANGES = (list(range(100, 111)) + list(range(200, 216)) + list(range(300, 311))
          + list(range(400, 421)) + list(range(500, 516)) + list(range(600, 616))
          + list(range(700, 716)) + list(range(800, 816)) + list(range(900, 911)))


def log(url, path, status, note=""):
    sha = ""
    if path and Path(path).exists():
        sha = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"{date.today().isoformat()}\t{url}\t{path or ''}\t{status}\t{sha}\t{note}\n")


def fetch(url, dest):
    """curl -sSL with a descriptive UA. Returns the HTTP status as an int."""
    out = subprocess.run(
        ["curl", "-sSL", "-A", UA, "-o", str(dest), "-w", "%{http_code}", url],
        capture_output=True, text=True)
    try:
        return int(out.stdout.strip()[-3:])
    except ValueError:
        return 0


def keep(path):
    """A valid type page contains the Éléments caractéristiques marker."""
    try:
        return MARKER in path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def main():
    HTML.mkdir(parents=True, exist_ok=True)
    tids = [int(x) for x in (HERE / "tids.txt").read_text().split()]
    seen, kept, dropped = set(), [], []

    for t in tids + [x for x in RANGES if x not in tids]:
        if t in seen:
            continue
        seen.add(t)
        dest = HTML / f"tid-{t}.html"
        url = f"{BASE}/thesaurus.aspx?tid={t}"
        if dest.exists() and keep(dest):
            kept.append(t)
            continue
        code = fetch(url, dest)
        time.sleep(1)
        if code == 200 and keep(dest):
            kept.append(t)
            log(url, str(dest.relative_to(HERE)), code, "kept")
        else:
            note = "no Éléments caractéristiques marker" if code == 200 else f"http {code}"
            dropped.append((t, note))
            log(url, "", code, "discarded: " + note)
            dest.unlink(missing_ok=True)
        print(f"tid={t} http={code} {'KEEP' if t in kept else 'drop'}", flush=True)

    print(f"\nkept {len(kept)}: {sorted(kept)}")
    print(f"dropped {len(dropped)}")
    (HERE / "tids_kept.txt").write_text("\n".join(str(t) for t in sorted(kept)) + "\n")


if __name__ == "__main__":
    sys.exit(main())
