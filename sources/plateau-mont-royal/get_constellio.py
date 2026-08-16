#!/usr/bin/env python3
"""Part 2 §1.1 — fetch the règlement 01-277 annexes from the Constellio GED.

The GED is a JavaScript (Vaadin) portal, so this needs a real browser. Run on a
machine with ordinary network access (Claude Code's remote sandbox resets
browser TLS connections; curl works there but Constellio needs JS):

    pip install playwright && playwright install chromium
    python sources/plateau-mont-royal/get_constellio.py

Files land in this directory; add their SHA-256 to MANIFEST.md afterwards.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

DEST = Path(__file__).resolve().parent
BASE = "https://mtl.ged.montreal.ca/constellio/?collection=mtlca&portal=REPDOCVDM#!displayDocument/"
DOCS = {
    "00000107954": "annexe-c-typologies-architecturales.pdf",
    "00000107949": "annexe-b-caracteristiques-par-unite-de-paysage.pdf",
    "00000106196": "annexe-a-plan-aires-unites-de-paysage.pdf",
    "00000106200": "annexe-a-plan-immeubles-interet-patrimonial.pdf",
    "00000107958": "annexe-f-portes-fenetres-par-typologie.pdf",
    "00000118639": "guide-travaux-exterieurs.pdf",
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(accept_downloads=True)
    for doc_id, name in DOCS.items():
        out = DEST / name
        if out.exists():
            print(f"skip {name} (exists)")
            continue
        page.goto(BASE + doc_id, wait_until="domcontentloaded")
        page.wait_for_timeout(8000)  # let the Vaadin view build
        clicked = False
        for sel in ('text=Télécharger', '[title*="élécharger"]', 'a[href*="download"]'):
            loc = page.locator(sel).first
            if loc.count():
                with page.expect_download() as dl:
                    loc.click()
                dl.value.save_as(out)
                print(f"OK   {name} ({out.stat().st_size:,} bytes)")
                clicked = True
                break
        if not clicked:
            print(f"FAIL {name}: no download control found — click it manually from {BASE}{doc_id}")
    browser.close()
