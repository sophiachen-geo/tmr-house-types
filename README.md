# Québec Residential Typologies

A structured catalogue of residential building types across Québec, place by
place, built from each locality's own typology documents (design-review
by-laws, inventories, characterisation studies). Part 1 contains the repo
scaffold, the data schema, and the first place: **Town of Mount Royal**
(13 types from PIIA By-law 1449).

**Live site (current):** https://sophiachen-geo.github.io/tmr-house-types/ —
still the single-page TMR catalogue served from `pages/` via the `gh-pages`
branch. The multi-place site below is built to `docs/` and will take over the
URL when it is ready to deploy (Part 11, or on request).

## Layout

- `build.py` — loads and validates `data/`, renders the site into `docs/`
- `data/canon/` — canonical vocabulary: forms, styles, glossary, section essays
- `data/places/<id>/` — place record, phases, sources, prose and one YAML per local type;
  Arvida adds a parsed address list (`models_addresses.csv`) and derived
  `model_families_summary.yaml`
- `assets/places/mount-royal/` — photo strips from By-law 1449
- `templates/` — Jinja2 templates + `base.css` + `app.js`
- `docs/` — generated site (home + timeline, sections, place page, type pages,
  canonical forms, styles, matrix, compare, glossary, methods, `data.json`, `data.csv`)
- `sources/<place>/` — acquired source documents (PDFs, `pdftotext` extractions,
  `MANIFEST.md` with provenance and SHA-256 per file)
- `pages/` — the original single-page TMR site (currently what GitHub Pages serves)

## Build

```
pip install -r requirements.txt   # pyyaml, jinja2, markdown
python build.py                   # validates data/, writes docs/
```

The generated Mount Royal place page (`docs/places/mount-royal/`) is
content-identical to `pages/index.html`; see `docs/methods/` (or the Methods
page on the built site) for what is verbatim vs interpretive and for the
schema-additions log. Later parts add more places as data packs under
`data/places/<id>/` — drop in the YAML, add photos, run `python build.py`, commit.

## Publishing

GitHub Pages serves the `gh-pages` branch, refreshed automatically by the
"Publish website to GitHub Pages" workflow whenever `pages/` changes on `main`
or `claude/website-responsive-github-pages-qnvdpq`. Don't edit `gh-pages` by
hand; it is overwritten on every publish.
