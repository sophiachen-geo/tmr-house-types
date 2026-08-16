# sources/quebec — MANIFEST

Acquisition and parsing record for the Québec City place record (Part 7a). Everything here was
fetched on **2026-08-16** from `www.ville.quebec.qc.ca`, one request per second, with the
User-Agent `tmr-house-types research crawler (educational typology documentation)`.

Reproduce with:

```
python3 crawl.py     # fetch, filter, log        -> html/, crawl_log.tsv, tids_kept.txt
python3 parse.py     # HTML -> structured JSON   -> parsed.json
python3 encode.py    # JSON + curated English    -> data/places/quebec/types/*.yaml
```

`crawl_log.tsv` carries one row per fetch: date, URL, saved path, HTTP status, sha-256, disposition.

---

## 1. Terms of use — the finding, read before any image was touched

The City's copyright page (**read in full before copying anything**, saved as
`html/droits-auteur.html`, last updated *1er février 2022*) says:

> Tout le contenu publié sur le présent site ou autrement accessible par l'entremise de celui-ci est
> protégé par droits d'auteur. […] **Toute utilisation, reproduction, diffusion, traduction,
> publication ou retransmission du contenu, en tout ou en partie, est strictement interdite sans
> l'autorisation écrite et préalable de la Ville de Québec ou du détenteur des droits d'auteur.**

and, under the heading *Photographies*:

> **Les photographies illustrant ce site ne peuvent pas être reproduites.**

<https://www.ville.quebec.qc.ca/apropos/portrait/image-marque/droits-auteur/index.aspx>

**Decision: republication is not permitted, so no Ville de Québec image is in this repository.**
Not one file was copied into `assets/places/quebec/`. Every type record's `photos` list is a single
placeholder of the shape the brief prescribes:

```yaml
photos:
  - {file: null,
     source_url: "https://imagespatrimoine.ville.quebec.qc.ca/thesaurus/{tid}/{n}.jpg",
     credit: "Illustration : Charles-Étienne Brochu, 2022 — © Ville de Québec",
     licence: "permission required", kind: placeholder}
```

The illustration URL is recorded so the drawing can be found, and the credit is carried verbatim,
but no bytes are reproduced. No `assets/places/quebec/` directory was created, because there is nothing lawful to put in it.

**On the text.** The same clause covers text, and the records here quote the fiches' French
verbatim. That is done as attributed documentary quotation for scholarly description, not
republication of the work: every record carries `source_ref` naming the fiche and its tid,
`source_url` linking to it, and `source_generation` naming the City as the source, and each card
links back to the City's page. This is the brief's editorial decision (§1.3 requires the verbatim
`elements_caracteristiques`); the finding is recorded here so it is on the record rather than
assumed. Anyone republishing this material commercially should seek the written permission the
clause requires.

**Wikimedia Commons fallback — checked, not used in 7a.** `Category:Buildings in Quebec City` is
live and its subcategories really are named by street address
(`Category:1084-1088, rue Saint-Jean`, `Category:1087-1091, rue Saint-Jean`, …), which is what makes
an address join to `related_buildings[]` possible. Probe response kept at
`json/commons_categories.json`. No Commons file was ingested here, because Part 7b owns that work
("Photograph or source one Commons image per type, matched by address to `related_buildings` where
possible; record `match_confidence`") and matching each of 28 types to a verified-licence file is
that task, not this one. No image was published whose licence was not read.

---

## 2. What was fetched

### Landing pages, index and the synthesis table

| file | URL | bytes | sha-256 |
|---|---|---|---|
| `html/styles.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/styles.aspx | 33,107 | `830607ecdc46edb1f43b6b72b7776ce091e8a77ad8e76e5f110168fe0218d707` |
| `html/influences-americaines.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/influences-americaines.aspx | 30,785 | `1c069690405d0db225847df3ea927e650548676aa2620467e268b6f95af08c61` |
| `html/influences-britanniques.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/influences-britanniques.aspx | 29,517 | `24818130d70978c610fd1ed36a596eff9175b82a379d100055ecfc6b9918ca12` |
| `html/influences-contemporaines.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/influences-contemporaines.aspx | 31,428 | `6cb2a16bcc14731640413dc055b04c92cd343fb85b8dbe6e332192bab2902618` |
| `html/influences-francaises.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/influences-francaises.aspx | 29,132 | `0c594197240ec3e8b3b926f15896125028baf46b383d50582e13d2d01617f24b` |
| `html/influences-marginales.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/influences-marginales.aspx | 29,166 | `aa63273326096f92a72661b0b643d26d887e93a6454dd21e391a3e7281a39430` |
| `html/influences-modernes.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/influences-modernes.aspx | 32,201 | `680b457f56607fa3edde4fec1d13e1544acc139144d07be9ef6f36e295878cb6` |
| `html/influences-styles-historiques.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/influences-styles-historiques.aspx | 33,230 | `6bd6d3a11521b255e912f73d961febfc32dfc5f8f01a912a19203c5b22cde536` |
| `html/influences-traditionnelles-modernes.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/influences-traditionnelles-modernes.aspx | 30,016 | `7c751fb64b1341e8e9608f28a75de5304838f2e576ca4d5b3d614d81a9fc7ce4` |
| `html/milieu-quebecois.html` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/milieu-quebecois.aspx | 29,300 | `27be841db7853976855ea9dee31398921413ad25ace1e8b71fe14e0ff9bf047e` |
| `html/droits-auteur.html` | https://www.ville.quebec.qc.ca/apropos/portrait/image-marque/droits-auteur/index.aspx | 28,902 | `40cf2b13373c9b7c5c1fb28cb7edb4192ba1e85b378d495d14decabc4bde3fb4` |
| `docs_tableau_styles.pdf` | https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati/docs/tableau_styles_historiques.pdf | 34,853 | `005963a286aa747c5aa675bac9465d8db572f9964bdf1a19a994eeec2f2b8dff` |

### The 53 thesaurus nodes kept

Every row was fetched from `…/bati/thesaurus.aspx?tid=N` on 2026-08-16 and contains the string "Éléments caractéristiques". *Disp.* is how the record is filed: **type** = a residential card, **courant** = a parent node, **non-res** = recorded but outside residential scope.

| tid | name (fiche heading) | courant recorded | bl | rb | disp. | sha-256 (first 16) |
|---|---|---|---|---|---|---|
| 101 | Maison rurale d’inspiration française | Colonial français | 7 | 4 | type | `67ec6384ae853f60` |
| 102 | Maison urbaine d’inspiration française | Colonial français | 6 | 4 | type | `2c0180336702d758` |
| 103 | Classicisme français | Influences françaises | 8 | 4 | non-res | `cbbc48442a147b3d` |
| 105 | Colonial français | — | 5 | 0 | courant | `9102c96c3afcf56a` |
| 201 | Palladien | Influences britanniques | 12 | 4 | type | `721b18494c117c22` |
| 202 | Néoclassique | Influences britanniques | 7 | 4 | courant | `dab077a08abd102a` |
| 203 | Maison londonienne | Néoclassique | 8 | 4 | type | `e79a0f701b3936be` |
| 205 | Cottage Regency | Regency | 11 | 4 | type | `ec7bc5800b16017b` |
| 206 | Villa Regency | Regency | 15 | 4 | type | `8f78f00eb3c4f45f` |
| 301 | Maison néoclassique québécoise | Néoclassique québécois | 9 | 4 | type | `f61b4ce5420f1eb9` |
| 302 | Néoclassique québécois | Milieu québécois | 4 | 4 | courant | `9c0e9eaaf1493566` |
| 303 | Maison de faubourg | Néoclassique québécois | 7 | 4 | type | `236c0d5fd797edc0` |
| 304 | Maison de transition franco-québécoise | Néoclassique québécois | 8 | 4 | type | `01d3f524d1fe6115` |
| 401 | Second Empire | Influence des styles historiques | 9 | 4 | courant | `fdadfb42fb619402` |
| 402 | Maison mansardée | Second Empire | 6 | 4 | type | `41da800084c6b20e` |
| 403 | Éclectisme | Influence des styles historiques | 9 | 4 | courant | `386ecd5c442ab9ae` |
| 404 | Néo-Queen Anne | Influence des styles historiques | 9 | 4 | type | `1eb30407dfe8844f` |
| 405 | Néogothique | Influence des styles historiques | 16 | 4 | type | `3d3f6e3b17a3cb38` |
| 406 | Néo-roman | Influence des styles historiques | 8 | 4 | non-res | `6546528395b3b28c` |
| 407 | Néo-Renaissance | Influence des styles historiques | 9 | 4 | type | `54c031fdbaa9f626` |
| 408 | Néo-baroque | Influence des styles historiques | 10 | 4 | non-res | `b3a78ab68c751195` |
| 409 | Néo-Tudor | Influence des styles historiques | 9 | 4 | type | `2e899d20c847b2df` |
| 410 | Néo-georgien | Influence des styles historiques | 9 | 4 | type | `4720414b3623e673` |
| 411 | Château | Influence des styles historiques | 8 | 4 | non-res | `fb2968a1d23b1d21` |
| 501 | Maison de faubourg à toit plat | Vernaculaire industriel | 7 | 4 | type | `c4b5a4cdf4025a99` |
| 502 | Boomtown | Vernaculaire industriel | 7 | 4 | type | `3238d6d2b182bab5` |
| 503 | Plex | Vernaculaire industriel | 7 | 4 | type | `ebc781ae8a3801db` |
| 504 | Maison cubique | Vernaculaire industriel | 8 | 4 | type | `34600d1d5bbcc05a` |
| 505 | Cottage vernaculaire industriel | Vernaculaire industriel | 8 | 4 | type | `855b8e67962a1117` |
| 506 | Vernaculaire industriel | Influences américaines | 6 | 4 | courant | `3f5008e34f43d914` |
| 507 | Immeubles à logements | Vernaculaire industriel | 8 | 4 | type | `f701415f5c685914` |
| 508 | Maison néocoloniale néerlandaise | Vernaculaire industriel | 10 | 4 | type | `ef4b1d0836dbfbd3` |
| 601 | Rationalisme | Influences traditionnelles et modernes | 8 | 4 | non-res | `2c885b82a1b452ad` |
| 602 | Beaux-arts | Influences traditionnelles et modernes | 8 | 4 | non-res | `d6438671a93d4786` |
| 603 | Art déco | Influences traditionnelles et modernes | 8 | 4 | non-res | `9fe7530b977bd723` |
| 604 | Wartime housing | Cape Cod | 8 | 4 | type | `6443600865a9a1e6` |
| 606 | Camp et chalet de villégiature | Influences traditionnelles et modernes | 7 | 4 | type | `d36414f20b657243` |
| 701 | Arts and Crafts (Arts et Métiers) | Influences marginales | 9 | 4 | type | `5d2b9daac8416312` |
| 702 | Régionalisme québécois | Influences marginales | 7 | 4 | non-res | `14a9d19cf599be6a` |
| 703 | Dom Bellot | Influences marginales | 7 | 4 | non-res | `4e65986928eace29` |
| 801 | Bungalow | Prairie | 19 | 4 | type | `20766edad27ec29e` |
| 802 | Style International | Influences modernes | 7 | 4 | type | `aa1052d65513a528` |
| 803 | Fonctionnalisme | Influences modernes | 7 | 4 | non-res | `0f311e67c18718ec` |
| 804 | Expressionnisme | Influences modernes | 8 | 4 | non-res | `8e5b37b3dedd8b31` |
| 805 | Modernisme | Influences modernes | 7 | 4 | non-res | `7ae4b32652ba03ad` |
| 806 | Brutalisme | Influences modernes | 8 | 4 | non-res | `eec3c18214457897` |
| 808 | Prairie | Influences modernes | 4 | 4 | type | `d3ea4e8f1bd0d289` |
| 809 | Paquebot | — | 2 | 4 | non-res | `bc64d84c70cf5527` |
| 810 | Néo-régionalisme | — | 2 | 4 | non-res | `be1f8210c05c7fc4` |
| 901 | Postmodernisme | Influences contemporaines | 7 | 4 | non-res | `c3699bc85610bf26` |
| 902 | High-tech | Influences contemporaines | 7 | 3 | non-res | `8b71d4f406b128c5` |
| 903 | Minimalisme | Influences contemporaines | 8 | 4 | non-res | `4e1a0bf28300c2b4` |
| 904 | Contemporaine | Influences contemporaines | 6 | 4 | non-res | `a4ad536eafe4dbf5` |

---

## 3. What the crawl could not reach

The §1.2 sweep covered tids 100–110, 200–215, 300–310, 400–420, 500–515, 600–615, 700–715, 800–815
and 900–910 — 134 fetches in all. 53 pages were kept, 81 discarded.

**68 tids returned HTTP 404** (they do not exist):

> 104, 106–110, 207–215, 305–310, 413–420, 509–515, 607–615, 704–715, 811–815, 905–910

**13 tids returned HTTP 200 but carried no "Éléments caractéristiques" list**, so the §1.2 filter
discarded them. They fall into two groups, and the distinction matters:

| tid | what it actually is |
|---|---|
| 100, 200, 300, 400, 500, 600, 700, 800, 900 | the nine **courant landing pages**, served through the thesaurus URL — the same content as `influences-*.aspx`, already captured under its own name |
| **204 Regency**, **605 Cape Cod** | genuine **parent nodes that are empty shells**: a heading, and no description, no characteristics list and no exemplars |
| **412 Néo-style (autre)**, **807 Moderne (autre)** | the two **catch-all nodes** the synthesis table lists at the end of their currents, likewise empty shells |

The four shells were re-fetched and kept as evidence at `html/shell-tid-{204,605,412,807}.html`.
They are **not** encoded as records: there is no French text on them to record, so a record would be
an empty box. Their consequence for the data is that two children have no parent named in their own
heading — Cottage Regency and Villa Regency (tid 205, 206) under **Regency**, and Bungalow (tid 801)
under **Prairie** — so for those the `courant` recorded here is the one
`docs_tableau_styles.pdf` gives. `parse.py` documents this resolution order and `TABLEAU_PARENT`
holds the map.

**One tid the landing pages never link: 105 Colonial français.** It was found only by the range
sweep, and it is the parent of 101 and 102 in the synthesis table — the same shape as 302 and 506.
It is recorded here as a courant.

**Three nodes are in the thesaurus but not in `docs_tableau_styles.pdf`**, which is the older
document: 508 Maison néocoloniale néerlandaise, 606 Camp et chalet de villégiature, and 809 Paquebot
/ 810 Néo-régionalisme. The first two are dwellings and are carded; the last two are not.

**Not attempted in 7a.** The §1.4 regulatory documents — `vision_patrimoine.pdf`, the Beauport and
Charlesbourg plans de conservation, the CUCQ sector list, the guides d'intervention and the trousses
d'accueil — were **not** downloaded. They feed the `conservation` key, and Part 7b owns that join;
`conservation` is empty on every record here, which is a true statement about the thesaurus (§4
below) rather than a gap left by not fetching those PDFs. The RPCQ pages and Données Québec datasets
were likewise not ingested; the sector records cite them from the brief.

---

## 4. Parsing, and the check case

`parse.py` implements §1.3. Three structural variants the CMS actually emits are handled, all of
which broke a naive `<p>`-based reading:

* **tid 501 and most others** — the marker sits inside a `<p>`, bullets are `<br>`-separated, and the
  credit follows in the next `<p>`.
* **tid 105** — the marker is bare text outside any `<p>` and the bullets are written `-Composition …`
  with no space.
* **tid 801 and 606** — the bullet list runs across several `<p>` blocks carrying `<strong>` sub-heads
  ("Bungalow à long pan (modèle populaire au Québec)", "Autres variantes"). Those sub-heads are kept
  verbatim as list entries: they name the variants, and dropping them would silently merge three
  variant groups into one.
* **tid 205 and 206** — the heading carries a qualifier ("Éléments caractéristiques **du Cottage
  Regency** :"), which belongs to the heading and not to the first bullet. Only the heading that
  opens the block is stripped; the second one inside tid 206's list is a sub-head and stays verbatim.

Text normalisation is limited to three changes, and they are the only ones made to the source
French: line-wrap hyphenation is rejoined (`d'amiante- ciment` → `d'amiante-ciment`), the newlines
the CMS emits mid-sentence collapse to a single space, and HTML entities are resolved. The source's
own typography is left alone, including its U+2019 apostrophes and its typos — tid 801 really does
read "revêt-ment de membrane(s)".

**Pattern case, tid 501.** Parses byte-identically to the brief's §2.4 transcription: the same seven
bullets in the same order, the same two description paragraphs, and the same four exemplar buildings
(fiche 1, 88, 95, 120).

**Check case, tid 303 — PASSED.** The parse was compared line by line against §2.4's transcription:

| §2.4 says the bullets should read | tid 303 as parsed |
|---|---|
| rudimentary, with or without symmetry, party-wall or separated by a narrow alley, descended from the French-inspired urban house and the maison néoclassique québécoise | bullet 1, verbatim |
| 1–1½ levels, and after densification or fire "reconstruite, agrandie, surhaussée d'un ou deux étages, munie de lucarnes ou coiffée d'une toiture mansardée" | bullet 2, the quoted clause verbatim |
| pièce-sur-pièce walls clad in vertical or horizontal board, then — "suite à la règlementation pour lutter contre les incendies" — brick, roughcast or stucco | bullet 4, the quoted clause verbatim |
| steep two-slope roof (>45°) in cedar shingle or board, then eaveless with traditional tin | bullet 5 |
| few openings with chambranles, "trois à l'avant incluant la porte à l'extrémité de la façade et deux à l'arrière", no dormer | bullet 6, the quoted clause verbatim |
| ornament limited to planches cornières | bullet 7, "Ornements : planches cornières." |

The only difference is an **addition, not a contradiction**: the fiche carries one further bullet the
brief's summary does not mention — bullet 3, "Fondation peu visible ou visible hors sol." The brief
introduces its transcription as what the bullets "should read", which is a summary; nothing in the
parse conflicts with it. Quartiers Saint-Roch, Saint-Sauveur and Saint-Jean-Baptiste are confirmed in
the fiche's own prose. **No material difference — no stop condition.**

---

## 5. Counts

| | |
|---|---|
| fetches logged | 134 |
| tids kept (contain "Éléments caractéristiques") | **53** |
| tids discarded | 81 (68 × HTTP 404, 13 × no marker) |
| empty shells re-fetched as evidence | 4 (204, 412, 605, 807) |
| landing pages + index + copyright page | 11 |
| records written to `data/places/quebec/types/` | **62** |
| — residential type cards | **28** |
| — parent courants (`is_courant: true`) | **15** = 6 with a tid (105, 202, 302, 401, 403, 506) + the 9 landing pages |
| — non-residential (`is_residential: false`) | **19** |

Every one of the 53 crawled tids has a disposition; `encode.py` fails loudly if any does not.
Every one of the 28 cards has a populated five-column table and a verbatim
`elements_caracteristiques` block — checked after the build, not assumed.

**Why 28 and not the brief's ~21.** The 21 rows of §2.4's table are all carded. §2.4 also says to
"add any type the crawl finds that is missing here, and drop any that turns out to be
non-residential", and lists ten further candidates to "encode if the crawl confirms them as
residential". A node was treated as residential when **both** its own fiche describes a dwelling —
a *niveaux d'occupation* bullet, the thesaurus's own marker for a habitable storey count, or a
dwelling noun as the node name — **and** at least half its linked exemplar buildings are dwellings.
That test admits seven more:

| tid | node | why |
|---|---|---|
| 201 | Palladien | not named in the brief either way; "Deux à trois niveaux d'occupation", exemplars Manoir Kilmarnock, Old Rectory, 1575 chemin Saint-Louis |
| 407 | Néo-Renaissance | brief's candidate list; "Trois à quatre niveaux d'occupation", two of four exemplars are mixed shop-houses on rue Saint-Jean / Sainte-Angèle |
| 409 | Néo-Tudor | brief's candidate list; storey count "privé et confortable pour la maison", exemplars Villa Clermont, Maison Arthur-Jobin |
| 508 | Maison néocoloniale néerlandaise | not in the brief or the synthesis table at all; a "Maison…", 4 of 4 exemplars are Résidences |
| 604 | Wartime housing | brief's candidate list ("Cape Cod / Wartime Housing"); a federal single-family house programme |
| 606 | Camp et chalet de villégiature | not in the brief or the synthesis table; seasonal dwellings, exemplars "Chalet de la famille…", "Camp de la famille Drolet" |
| 701 | Arts and Crafts | brief's candidate list; "Deux à trois niveaux d'occupation", exemplars Maison Alexandre-Boivin, Maison Ernest-Paradis |

The same test **rejected six of the brief's ten candidates** — 406 Néo-roman, 408 Néo-baroque, 411
Château, 602 Beaux-arts, 603 Art déco and 702 Régionalisme québécois. Their fiches carry no
storey-count-for-habitation bullet and their exemplars are churches, chapels, banks, schools and
commercial blocks. 602 and 603 are the closest calls, because their exemplars are street addresses on
rue Saint-Jean; they are excluded because their fiches describe an envelope, never a dwelling, and a
five-column house table built from them would be a fabrication.

---

## 6. `conservation` is empty on every record, and that is a finding

The thesaurus is descriptive. Across all 53 fiches there is **no conservation guidance of any kind** —
no prefer/avoid pairs, no component rules, no per-quartier tables. `conservation: []` on every record
therefore states a fact about the source rather than an unfinished field. The rules that govern work
on these houses live in the CUCQ guides d'intervention and the four ministerial plans de
conservation, and they attach **by geography** — by declared site or CUCQ sector — not by type.
Part 7b joins them spatially. This is note 1 of the place page's `## notes`.

---

## 7. Files

| path | what |
|---|---|
| `crawl.py` | the crawler: landing pages → tid harvest → range sweep → marker filter → log |
| `parse.py` | HTML → `parsed.json`; the §1.3 spec, verified on tid 501 and checked on tid 303 |
| `encode.py` | `parsed.json` + curated English → `data/places/quebec/types/*.yaml` |
| `crawl_log.tsv` | one row per fetch: date, URL, path, HTTP status, sha-256, disposition |
| `tids.txt` | the 52 tids harvested from the landing pages |
| `tids_kept.txt` | the 53 tids kept after the marker filter |
| `parsed.json` | the structured parse of all 53 fiches — the evidence the YAML is built from |
| `html/` | every page kept, as fetched |
| `docs_tableau_styles.pdf` | the synthesis table, used to validate the courant tree |
| `json/commons_categories.json` | the Wikimedia Commons category probe |
