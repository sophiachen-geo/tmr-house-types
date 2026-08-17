# sources/rosemont — acquisition manifest

Arrondissement de Rosemont–La Petite-Patrie, Ville de Montréal. Part 10a.
All fetches 17 August 2026 unless stated.

---

## 1. The arrondissement code — read from inside the document

**The code is 26.** Read from the sector codes printed inside the cahier, not from anything else.

```
$ grep -ho '\b[0-9]\{1,2\}\.\(E\|I\|N\|U\|AP\)\.[0-9]\{1,2\}\b' \
      txt/21_evaluation_patrimoine_rose.txt | sort -u
26.E.1 … 26.E.11   26.I.1 … 26.I.7   26.N.1   26.U.1 … 26.U.4   26.AP.1 … 26.AP.3
14.AP.1
```

The memo's claim that Rosemont is code 26 in file 21 is **confirmed**. Two independent traps in this
one document show why the code must never be inferred:

| Signal | Says | Truth |
|---|---|---|
| Filename `21_evaluation_patrimoine_rose.pdf` | 21 | code is 26 |
| PDF `Title` metadata | `maq1_CŽte StLuc Hampstead` | not this arrondissement at all — leftover from the QuarkXPress template the series was built from |
| Sector codes printed in the body | 26 | **authoritative** |

Filenames lie in this series (the brief's own case: Le Sud-Ouest is code 22 in file 12). This cahier
adds that the *file metadata* lies too. Only the printed codes count.

**Bonus verification for another borough.** The cahier cites `14.AP.1` when describing the terrasse
de Montréal, which independently confirms **Villeray–Saint-Michel–Parc-Extension = code 14**, as the
memo had it. No claim is made here about any other borough's code.

---

## 2. The E-sector list — the flag was correct, and the list is now complete

The Part 10 memo carried three E sectors (26.E.1 marché Jean-Talon, 26.E.2 cœur de la Petite-Italie,
26.E.3 rue Saint-Denis + Saint-Édouard) and flagged the list as incomplete. **It was. The cahier
carries eleven.** Enumerated from pages 27–33:

| code | name |
|---|---|
| 26.E.1 | Le secteur du marché Jean-Talon |
| 26.E.2 | Le cœur de la Petite-Italie |
| 26.E.3 | La rue Saint-Denis (A) et l'ensemble institutionnel Saint-Édouard (B) |
| 26.E.4 | L'ensemble institutionnel Saint-Ambroise |
| 26.E.5 | Le parc Molson |
| 26.E.6 | Centre civique et autres bâtiments institutionnels |
| 26.E.7 | Site du patrimoine de l'église Saint-Esprit de Rosemont |
| 26.E.8 | Secteur Angus |
| 26.E.9 | Le Jardin botanique |
| 26.E.10 | La Cité-Jardin du Tricentenaire |
| 26.E.11 | Les pyramides olympiques |

Part 10b asked for the I / N / U sectors as follow-up work; they were in the same document, so they
are enumerated here too rather than deferred — **7 I sectors** (pp. 34–37), **4 U ensembles urbains**
(pp. 37–39), **1 N ensemble industriel** (p. 39) and **3 AP archaeological sectors** (pp. 46–47).
`sectors.yaml` therefore holds **26 coded records**.

The cahier's one **tracé fondateur d'intérêt patrimonial**, la rue des Carrières (p. 25), is
deliberately *not* one of them. It is a route, not a sector; it sits outside the E/I/N/U/AP grammar in
the cahier's own structure (section 3.2.1 against 3.2.2); it has no code; and no value in the schema's
`SECTOR_VALUES` set fits it. The nearest, `parcel-system`, renders as "elements of the seigneurial
parcel system", which would put a false statement about a Montréal quarry road into the sector tally.
It is carried in `prose.md` instead, with the reason stated in a comment at the foot of `sectors.yaml`.
Adding a `trace-fondateur` value to the schema is the right fix and belongs to whoever owns `build.py`.

Note also that **26.E.7 carries two statuses** — an E sector in the Évaluation and a municipal *site
du patrimoine* cited in its own right. It is ranked `exceptional` so that the tally of E sectors comes
to eleven and matches the code list; the citation is carried in `governing_instruments` and in the
sector's own note.

**One error in the source, recorded not fixed.** The text of 26.I.5 refers the reader to "26.E.4" for
the site du patrimoine de l'église Saint-Esprit. That site is 26.E.7; 26.E.4 is Saint-Ambroise. The
cahier's building list (p. 40) also dates the citation `29-01-91` where the 26.E.7 fiche says the site
was constituted in 1990. Both are noted in `sectors.yaml`.

---

## 3. Files acquired

| file | bytes | status |
|---|---|---|
| `21_evaluation_patrimoine_rose.pdf` | 8,723,434 | 200. 60 pp. QuarkXPress 6.0, created 6 June 2005. |
| `shoebox_depliant.pdf` | 590,541 | 200 from `portail-m4s.s3.montreal.ca`. 2 pp. |
| `rosemont_annexe_caracterisation_shoebox.pdf` | 23,756 | 200. **Annexe F**, 8 pp., 561 rows. Recovered — see §4. |
| `reglement_urbanisme_01-279_codification.pdf` | 3,680,854 | 200. 295 pp., codification to 01-279-78, 23 May 2024. Recovered — see §4. |

Text extracted with `pdftotext -layout` into `txt/`. The cahier is a two-column layout that `-layout`
interleaves badly across the full document, so sector text was re-extracted page by page
(`pdftotext -f N -l N -layout`) before being read.

`annexe_f_parsed.json` holds all 561 Annexe F rows as parsed, so the counts in `place.yaml` are
reproducible rather than asserted.

### Fetches that failed

Both of these URLs are still in Google's index and both are **dead**: the old
`ville.montreal.qc.ca/pls/portal` document portal now returns a 404 HTML page (35,152 bytes,
`text/html`) for them, with or without a browser User-Agent.

| brief URL | result |
|---|---|
| `…/ARROND_RPP_FR/…/PROJET _REGLEMENT_SHOEBOX_DOC_EXPLICATIF.PDF` — the borough's explanatory document | **404** |
| `…/ARROND_VSP_FR/…/MAISONS SHOEBOX_ ÉTUDE_ÉVALUATION PATRIMONIALE_WEB.PDF` — VSP's shoebox heritage evaluation (Isabelle Bouchard, 29 Nov 2018) | **404** |

Recovery attempted and failed: `archive.org/wayback/available` returned 502; the Wayback **CDX API is
blocked by this environment's egress policy** on http and resets the connection on https, so no
snapshot enumeration was possible. Guessed `portail-m4s.s3.montreal.ca` filenames returned 403.

The two 404 response bodies are kept as `FAILED_*.404.html`, deliberately **not** with a `.pdf`
extension — curl will happily write an error page to whatever filename you give it, and a 35 KB
"PDF" that is really HTML is exactly the kind of thing that gets parsed as an empty document and
silently believed. `file(1)` every download before trusting it.

**Not left as a hole.** The substance of both documents was recovered from better sources:

* the explanatory document's payload — the value classes, their counts, their percentages and the
  dwelling limits — from the **Annexe F table itself** (§4) plus the Ville's own article page;
* the by-law's operative text from the **codification administrative of 01-279** (§4), which is
  stronger evidence than an explanatory document because it is the enacted instrument.

Still outstanding for a Part 10b revisit: **VSP's shoebox heritage evaluation study**, which is VSP's
source rather than Rosemont's but is the scholarly basis of the two-phase split that VSP applies and
Rosemont does not; and the borough's **2009 PIIA for the Cité-Jardin du Tricentenaire**, without which
three of the five profile columns on `maison-cite-jardin.yaml` stay empty.

---

## 4. Two recoveries worth recording

**Annexe F.** The Ville's article page for the borough links the characterisation annexe as a bare
numeric portal document, `…/pls/portal/docs/1/89503139.PDF`. That path still works where the named
paths do not. It is the December 2018 spreadsheet (`Annexe F _ décembre 2018.xls`, PDF ModDate
21 January 2019) — the primary list, address by address.

**By-law 01-279.** The Ville's own page for the by-law links into a regulations search portal rather
than to a file. A stable copy of the codification administrative is served by the **Office de
consultation publique de Montréal** in dossier P131, and that is what was fetched and kept.

---

## 5. The grading counts — a memo figure corrected against the primary document

The memo gave the three architectural-value classes as **69 / 258 / 235**. That sums to 562.
Parsing Annexe F row by row gives **561 rows** and:

| valeur architecturale | count | share |
|---|---|---|
| 1 — fewest characteristics of interest | **170** | 30.30 % |
| 2 | **233** | 41.53 % |
| 3 — most characteristics of interest | **158** | 28.16 % |
| **total** | **561** | |

These agree exactly with the percentages the Ville de Montréal publishes on montreal.ca
(30.3 / 41.5 / 28.2). **The memo's 69 / 258 / 235 is not published on this site.**

The memo's other Annexe F figure is **confirmed exactly**: `Construite en fonds de lot` = **56**,
which is 9.98 % — "just under 10 %". Two further columns that no summary mentions were also counted:
`Couronnement de qualité` = **118**, and `Adjacente à une autre maison shoebox` = **232**. 77 distinct
streets appear in the table.

Reproduce with `annexe_f_parsed.json`, or re-parse `txt/rosemont_annexe_caracterisation_shoebox.txt`
page by page using each page's own column offsets (the header indents shift from page to page, so a
single fixed offset mis-reads the `x` columns).

---

## 6. Primary-source confirmation of the thirty-nine zones

The memo said contested provisions in "~39 zones" triggered signature registers. The codification's
own citation footers settle it and make the number exact: the shoebox by-law **01-279-58** is followed
through the text by **`01-279-58-01` … `01-279-58-39`** — thirty-nine separate zone by-laws, one per
zone, verified by `grep -o '01-279-58-[0-9]\{2\}' | sort -u | wc -l` → **39**. The by-law series *is*
the register outcome.

---

## 7. Photographs — licence decisions

Every candidate's licence was checked through the Commons API **before** any download: `extmetadata`
for `LicenseShortName`, `LicenseUrl`, `UsageTerms` and `Artist`, and the raw file-page **wikitext**
for the licence template itself. Nothing was published whose terms were not read.

### Published

| file | author | licence | verified as |
|---|---|---|---|
| `shoebox-rosemont-commons.jpg` | Guerinf | CC BY-SA 4.0 | `{{self|cc-by-sa-4.0}}`, own work |
| `shoebox-rosemont-rue-commons.jpg` | Guerinf | CC BY-SA 4.0 | extmetadata + category `CC-BY-SA-4.0` |
| `shoebox-rosemont-couronnement-commons.jpg` | Guerinf | CC BY-SA 4.0 | extmetadata |
| `duplexes-rosemont-1948-poirier-banq.jpg` | Conrad Poirier, 28 Jul 1948 | PD | `{{PD-Canada}}` + `{{PD-1996|Canada}}`; **uploaded by BAnQ itself**, fonds Conrad Poirier P48,S1,P16539 |
| `cite-jardin-tricentenaire-commons.jpg` | Cossette.phil | CC BY-SA 3.0 | `{{self|cc-by-sa-3.0}}`, own work |
| `rue-saint-denis-triplex-commons.jpg` | Gene.arboit | CC BY-SA 3.0 | extmetadata + file page |

Author, licence and file URL are in every credit in the type YAML, with a `match_confidence` and a
note saying what the match rests on. All but the Poirier photograph are `visual`: the uploader's own
category and caption place them in the borough and identify the type, but no civic address is given,
so none could be joined to an Annexe F row.

**The Poirier photograph was reassigned after it was looked at.** It was first placed on the
exterior-stair duplex record on the strength of its title, *Feature. Duplexes. Rosemont*. Opening the
image shows a row of paired two-storey brick buildings with flat roofs, every front door at ground
level under a small suspended marquise, and **no exterior stair anywhere in the frame** — which is
the 26.U.2 semi-detached Art déco duplex, not the contiguous plex of the 26.I sectors. BAnQ's own
caption had said so all along: *duplex **jumelés***. It now sits on `duplex-jumele-art-deco.yaml`,
where it independently corroborates four things that sector fiche names — paired, two storeys, flat
roof, brick, doors at grade under marquises hung on chains — and where its date, 1948, falls inside
the fiche's own span of *les années 1940-1950*. `match_confidence: documented` for the type;
the sector match is by form and date, not by address. The exterior-stair duplex record keeps a
placeholder and says why. A title is not a match.

### Rejected

* **`File:Avenue Louis-Hebert 01.jpg` and `02.jpg`** — tempting, because 26.E.5's illustrated example
  in the cahier is *6564-6566, avenue Louis-Hébert* and these are captioned as triplexes on that
  avenue c. 1925. Licence templates are `{{PD-1996|Canada}}{{PD-Canada}}`, but `|source=` is a
  **Facebook group post** and `|author=` is a Facebook display name, i.e. the person who posted a scan
  rather than the 1925 photographer. The public-domain claim is plausible on date and unsupported on
  provenance. **Not published.**

### The two categories the brief named

Both were listed in full through the API, and the brief's warning about `Category:Staircases` was
respected — only `Category:External staircases` was opened.

* **`Category:Multiplexes (buildings)`** — 22 files, almost all American (Portland, Savannah,
  Jeannette PA, New Orleans, Ybor). Its four Montréal files are in Ville-Marie, Saint-Léonard and
  Verdun. **Nothing in this borough.**
* **`Category:External staircases`** — a very large, mostly non-Montréal category (Helsinki, Madrid,
  São Paulo, Rotterdam fire escapes). **Nothing in this borough** in the pages listed.

What actually served this borough is **`Category:Style Shoebox`** (100 files, many explicitly
Rosemont) crossed with **`Category:Rosemont–La Petite-Patrie`**. That is a finding worth carrying into
the other four Part 10 boroughs: the type-tagged category the brief predicts would be scarce exists
for the shoebox and is rich, while the plex categories it names are not usable.

Four type records therefore keep `kind: placeholder` photos rather than a weak match — the interior-
stair duplex (26.I.7), the Art déco semi-detached duplex (26.U.1/26.U.2), the bungalow (26.U.3) and
the conciergerie. No image was published whose location could not be established from the file page.

### No commercial real-estate sources

Per the brief, `equipels`, `yanicksarrazin`, `absolumentmontreal`, `montrealguidecondo`,
`balconsverdun`, `centris` and `duproprio` were excluded from every search that fed a date or a count,
and none is cited anywhere in this place's data.

---

## 8. Press, labelled as press

Two figures on this page come from *La Presse* and are labelled press in `prose.md`, never presented
as municipal:

* the island-wide estimate — about a thousand shoebox houses in Montréal, roughly half in
  Rosemont–La Petite-Patrie — from the report of **19 October 2018**;
* the **September 2019** case of a couple who paid $500,000 for an uninhabited Rosemont shoebox to
  demolish it and build a single-family house of over $700,000, the project reaching about
  $1.3 million.

Neither article could be fetched: `lapresse.ca` returns **403** to automated requests. Both are cited
from search-index summaries carrying their headlines, dates and URLs, and both are used only for the
attributed claims above. The municipal record supports only the borough figure, **561**, and that one
is exact because it is a list of addresses rather than an estimate.

---

## 9. Not implemented

* **VSP's shoebox heritage evaluation study** — 404, no Wayback access from this environment.
* **The borough's explanatory document** — 404; its content recovered from Annexe F and 01-279.
* **The Cité-Jardin's 2009 PIIA** — not fetched; three profile columns on the Cité-Jardin type stay
  empty in consequence, and the record says so rather than filling them from other garden suburbs.
* **`data/canon/montreal_arrondissement_codes.csv`** — outside this agent's write scope
  (`data/canon/**` is off limits). The two verified rows for it are recorded here instead:
  `21_evaluation_patrimoine_rose.pdf → 26 → Rosemont–La Petite-Patrie`, and, from a cross-reference
  inside that same cahier, `→ 14 → Villeray–Saint-Michel–Parc-Extension`.
* **`TYPOLOGIE_SPECIFIQUE` open-data join** — Part 10b work, not attempted.
