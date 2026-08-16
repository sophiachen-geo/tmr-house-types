# Source manifest — Westmount

Fetched 2026-08-16 per the Part 5 brief §1.1; all six PDFs download cleanly with `curl`.
`txt/` holds the first pass of `pdftotext -layout` extractions, `txt/bbox.xhtml` the word
coordinates, and `txt/columns.txt` a column-ordered rendering of the 2005 evaluation. See
"Sectors" below for why the 2005 fiche pages were re-extracted for the v2 pass.

| file | bytes | url | sha-256 |
|---|---|---|---|
| `categorie1etoile_cde_en.pdf` | 14,084,165 | https://westmount.org/storage/app/media/travaux-et-urbanisme/construction-et-renovation/informations-generales/EN/hcdeeng120620.pdf | `ada15d5144f4667ed5dd8dd52066d7303e27e0cd04247ffa258bb7bca2c42567` |
| `categorie1etoile_elements_caracteristiques_fr.pdf` | 14,020,468 | https://westmount.org/storage/app/media/travaux-et-urbanisme/construction-et-renovation/informations-generales/hcdefr120620.pdf | `cbd1f662bb290b5eea812b6d6c7c9914cf51e1691d98f06617e9a87540c87f3a` |
| `directive4_portes_et_fenetres.pdf` | 693,046 | https://westmount.org/storage/app/media/travaux-et-urbanisme/construction-et-renovation/informations-generales/4portesetfenetres.pdf | `a7d07d6814fb6e350fc206300eef7bcc408b53c671ccf3f0264e82ba3a20d2a3` |
| `evaluation_patrimoine_westmount_2005.pdf` | 8,079,912 | http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/27_evaluation_patrimoine_wes.pdf | `311f34051a03a918f6f16c1d8fb0af5339b4d27d4584e887e04e683e14e8e281` |
| `fiche3_patrimoine_imagine2040.pdf` | 1,492,031 | https://engage.westmount.org/wp-content/uploads/2020/11/Fiche-3-Patrimoine-VF.pdf | `7c74126c593564a43ec631574b8f6556b2ae7dd3131463ee8e1217684bfd7fda` |
| `gubbay_a_view_of_their_own.pdf` | 29,008,362 | https://westmount.org/storage/app/media/a-view-of-their-own-the-story-of-westmount-aline-gubbay-1579.pdf | `7d1e639f69be8b21ce9b95249065df9e09e02cb62add450d2b7edcf09a2189b9` |
| `sector-map-p3-introduction-aux-directives.jpeg` | 287,682 | supplied to the session (raster of Annexe II, « Introduction aux directives », p. 3) | `6d9fb70d5ff92bf741fb37397c74aa72905f75490328926976d0dbbe18562229` |

## What By-law 1305 material this repository actually holds

**The consolidated By-law 1305 PDF was NOT supplied to this session.** §1.1 of the Part 5 v2 brief
reports it as obtained (161 pp., bilingual) and §2.1 transcribes from it: the adoption and amendment
chain, the works-subject list, the exclusions, the three objectives, the criteria procedure, the
four-category table with its French descriptions and intervention rules, the eleven booklet titles,
the « Murs extérieurs » masonry passage, the « Toitures » roof taxonomy, and the numbering and names
of the 39 sectors. **All of that is encoded here from the brief's own reading of the by-law, not from
a file in this folder, and could not be re-checked during this pass.** Every affected record says so:
each type carries it in `profile_note`, `place.yaml` and `prose.md` say it in prose, and
`sources.yaml` records it under `wm-bylaw-1305`. The codification's own disclaimer is preserved
there too — « Cette codification administrative n'a pas été adoptée officiellement par la Ville de
Westmount… il faut se reporter au règlement original et à ses modifications. »

Three pieces of by-law material *are* held and were read directly for the v2 pass:

- **`directive4_portes_et_fenetres.pdf` is Annexe II, booklet 4, « Portes et fenêtres »** (revised
  6 December 2004, R-RCA04 23020). Its § 4.1 design points, § 4.2 rules for existing buildings and
  **tableau 4.2.2** were read in full. Every line of `conservation_fr` on the twelve type records is
  verbatim from this file, and the English `conservation` bullets are translations of it. The brief's
  summary of the table in §2.1.4 checks out, and two further rules it does not mention are now
  encoded: PVC is not acceptable on category I* or I and PVC and metal are generally not acceptable
  on category II (§ 4.1.6), and new or altered openings in masonry walls are generally unacceptable
  on character-contributing façades of category I and II buildings (§ 4.2.6).
- **The two `categorie1etoile_*` PDFs are Annexe III**, "Étude patrimoniale — Éléments
  caractéristiques : Bâtiments de catégorie 1" (109 pp., FR and EN), each page headed « Annexe III du
  règlement 1305 ». This resolves Part 5b blocker 4 below. Its index (pp. 3–4) lists every category 1*
  building under its **« Secteur patrimonial » number in the by-law's own 1–39 system** — which makes
  it an independent check on the sector numbering, see below. It does **not** contain Annexe I's maps
  as vector or text: the "Carte des secteurs patrimoniaux" on its p. 1 is a raster with no text layer.
- The 2005 evaluation states in its own words (pp. 26 and 36) that its sector text « reproduit
  largement la fiche correspondante » of Westmount's September 2001 sector fiches, which is the
  warrant for using it in place of the fiches themselves.

## Sectors

`sectors.yaml` was rewritten for v2. The by-law's 1–39 is now `code`; the 2005 Ville de Montréal
code is `code_eval2005`. **All 39 rows are filled; no row carries `none` and no `code_eval2005` is
null.** The reason is a finding in its own right: the two numbering systems cover the *same* 39
sectors. The 2005 study's 35 exceptional fiches (23.E.1–35) plus its 4 interesting ones (23.I.1–4)
match the by-law's 39 names one for one, with nothing left over on either side, so the 2005 study
retained every sector the by-law designates.

Seventeen `code_eval2005` values were null in the brief (the brief calls them fifteen; the count in
its own YAML is seventeen). All seventeen are filled, by exact match of the French sector name
against the 2005 fiche headings.

**Two corrections to the brief.** The brief gives sector 38 « Les alentours de la Cour Glen » →
23.I.2 and sector 39 « La Cour Glen » → 23.I.4. The 2005 PDF (p. 36) heads **23.I.2 « LA COUR GLEN »**
(the vacant CP station, the escarpment and the elevated track) and **23.I.4 « LES ALENTOURS DE LA
COUR GLEN »** (Public Works garages, the Westmount Hydro building of 1906). The two are swapped in
the brief and have been matched by name here; both rows carry a `note` saying so.

**Independent corroboration of the by-law numbering.** Annexe III's address index gives a by-law
sector number for each category 1* building. Ten sector numbers are confirmed outright because the
addresses are on the streets the matching 2005 fiche names — 2 (Braemar, 3219 The Boulevard, which
is also the photograph illustrating fiche 23.E.1), 3 (80 Sunnyside), 9 (5 Rosemount), 10 (Daulac and
Ramezay), 11 (41–47 Holton), 13 (Forden and croissant Forden), 15 (561–563 Côte-Saint-Antoine, the
Maison Hurtubise), 22 (Metcalfe and Redfern), 23 (Olivier) and 24 (Greene) — and sector 8 (Clarke and
Mountain) is corroborated. Three do not resolve and carry a `note`: Annexe III puts 523 chemin Argyle
and 88 avenue Church Hill in sector 6 (« Ave. Aberdeen et ses abords »), 519/529 Clarke and 504
Mountain in sector 7 (« Avenue Cedar et ses abords »), and 39 chemin de la Côte-Saint-Antoine in
sector 14 (« Avenue Argyle »). Only Annexe I's own maps can settle these; the names themselves are
used verbatim as supplied and were not altered.

**Fiche text.** Every `summary_en` is now filled from the 2005 fiche text. The earlier extractions in
`txt/` bleed between the two columns and are not safe to write from; for this pass the eleven fiche
pages (PDF pp. 26–36) were re-extracted with a per-page gutter-detecting column split, which returns
clean, unbroken paragraphs for all 39 fiches. The script used is not committed — it is four lines of
`pdftotext -layout` plus a blank-column scan and is described in the header comment of
`sectors.yaml`. Note that the 2005 fiche spells the planner of Priest's Farm « L.E. Schlemn »; the
brief and the Hampstead record spell him Schlemm.

## Sector map — NOT published, licence check failed

The map page of the « Introduction aux directives » booklet was supplied to this session as
`sector-map-p3-introduction-aux-directives.jpeg` (1445 × 1870). **It has not been copied to
`assets/places/westmount/` and `place.yaml` carries no `sector_map` block.**

The brief made publication conditional on the licence permitting it. Checked on 2026-08-16:

- `https://westmount.org/en/terms-of-use/`, `/en/legal-notice/`, `/en/copyright/` and
  `/fr/conditions-dutilisation/` all return **404** — the site publishes no terms of use.
- The footer of both the English and French sites carries only **"© City of Westmount, 2026" /
  "© Ville de Westmount, 2026"**, with two links: navigation cookies and the privacy policy.
- The privacy policy (`/en/city/administration-and-finance/privacy-policy`) was read in full. It
  concerns personal information only and contains no reuse, reproduction or licence clause.
- The page hosting the by-law material
  (`/fr/travaux-et-urbanisme/construction-et-renovation/informations-generales-construction-renovation`)
  carries no reuse statement either.

There is therefore no permission to republish, only an unqualified copyright assertion, so the image
stays out of the repository. Reversing this needs a written grant from the Urban Planning Department
or a City open-data licence; if one is obtained, copy the file to
`assets/places/westmount/sector-map.jpg` and add to `place.yaml`:

```yaml
sector_map:
  file: assets/places/westmount/sector-map.jpg
  credit: "Ville de Westmount, Règlement 1305, Annexe II, livret « Introduction aux directives », p. 3"
```

`build.py` already supports the block (it validates `file` and `credit` and reads the JPEG's
dimensions), and `templates/place.html` already renders it above the sector table. Nothing else needs
to change.

## Still to obtain (Part 5b blockers)

1. ~~By-law 1305 consolidated text~~ — reported obtained by the Part 5 v2 brief, but **not supplied to
   this session**. Until the PDF is in this folder, everything in §2.1 that comes from it is
   single-sourced on the brief. This is now the largest outstanding item, not a closed one.
2. ~~The named list of the 39 sectors~~ — **obtained** via the brief, and cross-checked here against
   the 2005 evaluation (all 39) and Annexe III's address index (14 of them).
3. **Ville de Westmount, *Rénover et construire à Westmount : fiches d'information des secteurs
   patrimoniaux*, September 2001, and Annexe I (maps 1–39).** Still needed. The by-law says the
   per-building defining characteristics, addresses and categories are on the original of each map
   (art. 4.3), and the reverse of each fiche carries « la liste des principaux traits distinctifs que
   partagent les bâtiments de votre secteur ». That reverse-side list is the per-sector five-column
   content; it is in no document held here, and it is what would convert several type cards from
   reconstruction to quotation and populate `characteristics_fr` on the sector rows. Annexe I would
   also settle the three unresolved sector numbers above.
4. ~~**Annexe III**~~ — **resolved.** The two `hcde*` PDFs are Annexe III, complete with the
   conservation-strategy directive and the per-building fiches, each page headed « Annexe III du
   règlement 1305 ». Remaining optional work: build `category1_addresses.csv` from its index (47
   entries across 14 sectors) for a `/places/westmount/category-1-star/` page.
5. **Annexe II booklets other than « Portes et fenêtres ».** Only booklet 4 is held. « Murs
   extérieurs » and « Toitures » are quoted from the brief and are unverified here; the numbered
   eight-roof-form plate in « Toitures » has not been seen, so the form numbers (1)–(8) used on the
   type records rest on the brief alone. « La Cour Glen », cited on sector 39, is likewise unseen.

## Photographs

One image is published, from Wikimedia Commons under a free licence:

| file | source | licence |
|---|---|---|
| `assets/places/westmount/66-chemin-saint-sulpice-commons.jpg` | Commons, `File:66, chemin Saint-Sulpice.JPG` | CC BY-SA 4.0 — © Jeangagnon |

It shows 66 chemin Saint-Sulpice, built 1927, in by-law sector 10 (= 23.E.9) — the sector the Tudor
Revival record cites — and is attached to that record. Parks Canada images are copyright and are not
committed, nor is the Ville de Westmount sector map (above).
