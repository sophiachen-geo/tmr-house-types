# Source manifest — Westmount

Fetched 2026-08-16 per the Part 5 brief §1.1; all six documents download cleanly with `curl`.
`txt/` holds `pdftotext -layout` extractions, `txt/bbox.xhtml` the word coordinates, and
`txt/columns.txt` a column-ordered rendering of the 2005 evaluation.

| file | bytes | url | sha-256 |
|---|---|---|---|
| `categorie1etoile_cde_en.pdf` | 14,084,165 | https://westmount.org/storage/app/media/travaux-et-urbanisme/construction-et-renovation/informations-generales/EN/hcdeeng120620.pdf | `ada15d5144f4667ed5dd8dd52066d7303e27e0cd04247ffa258bb7bca2c42567` |
| `categorie1etoile_elements_caracteristiques_fr.pdf` | 14,020,468 | https://westmount.org/storage/app/media/travaux-et-urbanisme/construction-et-renovation/informations-generales/hcdefr120620.pdf | `cbd1f662bb290b5eea812b6d6c7c9914cf51e1691d98f06617e9a87540c87f3a` |
| `directive4_portes_et_fenetres.pdf` | 693,046 | https://westmount.org/storage/app/media/travaux-et-urbanisme/construction-et-renovation/informations-generales/4portesetfenetres.pdf | `a7d07d6814fb6e350fc206300eef7bcc408b53c671ccf3f0264e82ba3a20d2a3` |
| `evaluation_patrimoine_westmount_2005.pdf` | 8,079,912 | http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/27_evaluation_patrimoine_wes.pdf | `311f34051a03a918f6f16c1d8fb0af5339b4d27d4584e887e04e683e14e8e281` |
| `fiche3_patrimoine_imagine2040.pdf` | 1,492,031 | https://engage.westmount.org/wp-content/uploads/2020/11/Fiche-3-Patrimoine-VF.pdf | `7c74126c593564a43ec631574b8f6556b2ae7dd3131463ee8e1217684bfd7fda` |
| `gubbay_a_view_of_their_own.pdf` | 29,008,362 | https://westmount.org/storage/app/media/a-view-of-their-own-the-story-of-westmount-aline-gubbay-1579.pdf | `7d1e639f69be8b21ce9b95249065df9e09e02cb62add450d2b7edcf09a2189b9` |

## Sectors

All **39** sector codes (35 exceptional, 23.E.1–35, and 4 interesting, 23.I.1–4) appear in the 2005
evaluation, and every French name in `data/places/westmount/sectors.yaml` is transcribed from that
document's fiche headings. The English summaries and street lists for 22 of them come from the Part 5
brief's own transcription; the other 17 carry `summary_en: null`.

The reason is worth recording rather than papering over: the fiches are set in two columns whose body
text bleeds between columns under every extraction method tried here — `-layout` interleaves the
columns onto single lines, and a coordinate-based column split still mixes stray words from the
neighbouring column into the paragraph text (sectors 23.E.6 and 23.E.7 are clear cases), while five
headings sit mid-line and are not recoverable by pattern alone. Writing English summaries from that
text would risk silently mistranscribing the source, so those cells stay empty and the page says so.
Completing them is a Part 5b task, alongside By-law 1305 Annex I.

## Still to obtain (Part 5b blockers)

1. **By-law 1305 consolidated text**, with the objectives-and-criteria tables by work category and
   Annex I (the 39 sectors with boundaries). Not published as a single PDF; the numbered Directives are
   posted individually — Directive 4 (portes et fenêtres) is in this folder, and the Category 1*
   character-defining-elements documents (FR and EN) are the Annex III material. Directives 1, 2, 3 and 5
   were not located at the paths tried.
2. **Rénover et construire à Westmount : fiches d'information des secteurs patrimoniaux** (Sept 2001) —
   a confirmation source; the 2005 evaluation reproduces it largely verbatim.

## Photographs

One image is published, from Wikimedia Commons under a free licence:

| file | source | licence |
|---|---|---|
| `assets/places/westmount/66-chemin-saint-sulpice-commons.jpg` | Commons, `File:66, chemin Saint-Sulpice.JPG` | CC BY-SA 4.0 — © Jeangagnon |

It shows 66 chemin Saint-Sulpice, built 1927, in sector 23.E.9 — the sector the Tudor Revival record
cites — and is attached to that record. Parks Canada images are copyright and are not committed.
