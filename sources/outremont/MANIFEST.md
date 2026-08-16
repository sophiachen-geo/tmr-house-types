# Source manifest — Outremont

Fetched 2026-08-16 per the Part 6a brief §1.1.

| file | bytes | url | sha-256 |
|---|---|---|---|
| `evaluation_patrimoine_outremont_2005.pdf` | 8,385,351 | http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/17_evaluation_patrimoine_out.pdf | `f695682c93db30610cf45cc9a4db6daefe9f8aeb5f5535e133e782d5b5b38459` |
| `guide_comprehension_piia_outremont_2021.pdf` | 10,467,732 | https://montreal.ca/articles/guide-de-comprehension-du-reglement-sur-les-piia-doutremont-19363 | `ba39640cec737b78255f84cb40f164bd7846ed9c05e86215368ec0e63234ab90` |
| `data/outremont-bisson-cat-1-2.csv` | 241,235 | https://donnees.montreal.ca/dataset/patrimoine-architectural-outremont-fiches-immeubles-inventaire-bisson | `0dce957df294914d85234d99e79bae0318bb520ff4b4e80082e72e7ebd390e72` |

## Sector codes — the `17_` filename versus the `16.` codes

The 2005 evaluation is published as `17_evaluation_patrimoine_out.pdf`, but the sector fiches inside it
are numbered **16.E.1–16.E.8** (valeur patrimoniale exceptionnelle) and **16.I.1–16.I.6** (valeur
patrimoniale intéressante). The `17_` prefix belongs to the series numbering of the evaluation volumes,
not to the sectors. The brief's seed entries carried `code: TBD.E.n` pending exactly this check; the
codes printed inside the document have been followed, and all fourteen are encoded.

## How the two-column fiches were extracted

`pdftotext -layout` interleaves the two columns onto single lines, and a single global column split
fails because the gutter moves from page to page. The working method, recorded here because it is the
same problem Westmount hit and did not solve:

1. `pdftotext -bbox-layout` for word coordinates, then per page find the widest empty vertical band
   between x = 100 and x = W − 80 — that page's gutter.
2. Re-run `pdftotext -f n -l n -layout -x … -y 0 -W … -H …` twice per page, once per column, so each
   column is extracted as its own page-region.
3. Carry the heading context across the column break, since a sector's text routinely starts in the
   right column of one page and continues in the left column of the next.

The result is `txt/sectors_final.json`: fourteen entries of clean verbatim French, keyed by code.
Intermediate stages are kept (`txt/sectors.json`, `txt/sectors_clean.json`, `txt/columns.txt`,
`txt/columns_clean.txt`, `txt/bbox.xhtml`) so the extraction can be re-checked.

Two artefacts of the source layout are recorded on the sector rows themselves rather than silently
fixed: a figure caption set inside the running text of 16.E.5 splits the word « stylistique », and the
fiche for 16.I.6 runs on without a break into the document's next section. Hyphenation lost at line
breaks in extraction (`Côte-SainteCatherine`, `MontRoyal`, `SaintGermain`, `JésusMarie`) is restored in
`summary_fr`; every such repair is a hyphen, never a word.

## English summaries

Each of the fourteen French texts was translated and then independently checked against the source by a
second pass. The checks changed the encoded text in six places: « bâtiment cité en 2000 » is rendered as
municipal heritage designation rather than "cited"; « toit en terrasse » is kept as terrace roof rather
than flattened to "flat"; the concessive « bien que … un certain nombre » is kept as a minority rather
than promoted to a co-dominant form (16.E.1, 16.E.2); parks and a cemetery named as boundaries were
removed from the street lists (16.E.3, 16.E.7, 16.I.3); and the run-on tail of 16.I.6, with the two
addresses it names, was cut. One ambiguity was left standing and flagged on the row instead: in 16.E.4,
« maisons isolées de deux étages … avec rez-de-chaussée surélevé » does not settle whether the raised
ground floor counts inside the two étages, so the verbatim French is printed beside the English.

## The Bisson dataset

`data/outremont-bisson-cat-1-2.csv` is the Ville de Montréal / arrondissement d'Outremont open dataset
"Patrimoine architectural de l'arrondissement Outremont — Fiches d'immeubles de l'inventaire Bisson",
**CC BY 4.0**, and it is therefore reusable with attribution. It lists 671 buildings from Pierre-Richard
Bisson's 1992 inventory: 331 Catégorie 1 (*bâtiment remarquable*) and 340 Catégorie 2 (*bâtiment
intéressant*), across 62 streets, 165 of them carrying a building name, one recorded as demolished, and
668 with a link to a scanned fiche. The `STATUT_INV_PRE_40_2025` column records which were retained in
the agglomeration's pre-1940 inventory adopted 28 August 2025 (621 of 671). A trimmed copy of the
columns used is committed at `data/places/outremont/bisson_inventory.csv` and published with the site's
data exports; the derived totals are in `bisson_summary.yaml`. The dataset's own caveat is carried onto
the page: the data reflect the state of knowledge in 1992 and have not been updated since.

## Photographs

One image is published, from Wikimedia Commons under a free licence:

| file | source | licence |
|---|---|---|
| `assets/places/outremont/avenue-bernard-commons.jpg` | Commons, `File:Avenue Bernard, Outremont.jpg` | CC BY-SA 4.0 — © Intermedichbo (Milorad Dimic M.D.) |

It shows avenue Bernard — sector 16.E.6 — with the three-storey multi-family blocks over ground-floor
shops and summer terraces that the 2005 fiche names as the sector's dominant type, and is attached to
the *conciergerie* record. The other five type records carry placeholders.

## Not retrieved (Part 6b blockers)

1. **L'Enclume, Étude typomorphologique et synthèse historique (11 June 2020)** — the document that
   names the 4 *aires* and 29 *unités de paysage*. Not published at a retrievable URL; the project page
   at enclume.ca describes it without linking the report.
2. **The PIIA annexes**, in particular the *tableaux des éléments caractéristiques par unité* and the
   *témoins architecturaux significatifs* list. These are the tables that would give Outremont real
   per-unit profiles and supersede the six reconstructed type records.
3. **The by-law number.** Legacy listings give 1189; the 2020–21 consolidation appears to use an AO-###
   series (AO-530 reported). Neither is asserted; both are recorded in `place.yaml` with the doubt
   marked.
