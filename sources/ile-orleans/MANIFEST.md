# sources/ile-orleans — acquisition manifest

Everything here was fetched on **17 August 2026** unless a different date is given. Checksums are
sha-256 of the file **as it now stands on disk**; the eight RPCQ building fiches were passed through
`scrub_secrets.py` after download, which redacted a live Mapbox access token embedded in each page,
so their hashes differ from the bytes the server sent.

## 1. Documents fetched

| file | URL | bytes | sha-256 |
|---|---|---|---|
| `inventaire_synthese.pdf` | `https://mrc.iledorleans.com/stock/fra/rapport_synthese_io_050919_maj2025.pdf` | 3,660,626 | `d3308d239c96940b537dcf14ef4c3f6220858e95ce7ea3d0ce2a43c41e65f241` |
| `inventaire_immobilier_2026.pdf` | `https://mrc.iledorleans.com/stock/fra/inventaire-du-patrimoine-immobilier_3-mars-2026.pdf` | 447,895 | `c810f69db5e7999e34b160889946ec752f0dd89b245f04d161b864d40e43a1da` |
| `pc_ile_orleans.pdf` | `https://cpcq.gouv.qc.ca/app/uploads/2020/05/pc_orlean.pdf` | 17,105,178 | `7348dc3e5a9d29772498ba58fdea5fc6a3e92283bcd06b9e77f3f272de9c2870` |
| `mesures_assouplissement.pdf` | `https://www.patrimoine-culturel.gouv.qc.ca/document/rpcq_bien_93521_344296.PDF?id=344296` | 311,845 | `4a423900a000ba5fe0c787294673ecf31ade124e01400aa03e048431e675a299` |
| `rpcq_93521.html` | `https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&id=93521&type=bien` | 83,968 | `1a9d49e6f5993912fcb05f34e12a81622efaddee8b53bf83b799982962e73614` |

All five returned HTTP 200 on the first attempt. `pdftotext -layout` was run on each PDF, producing
the `.txt` beside it.

RPCQ building fiches, all `…/rpcq/detail.do?methode=consulter&id=<ID>&type=bien`:

| file | id | sha-256 |
|---|---|---|
| `rpcq/b92670.html` | 92670 manoir Mauvide-Genest | `1bb2e6facaee2c0eb535d40e16e3ad8e08280bacdf0bb67273a92150ba0bd424` |
| `rpcq/b102270.html` | 102270 maison Drouin | `def36902d88aafc85d797b4dbe8b9b6f12f7801a2d667c361514cdf735850e66` |
| `rpcq/b92491.html` | 92491 maison Gendreau | `6e764c57ef13bd37a1e18213bdc4de8846e9f90f9d4cf2b4cf4cb3791745c671` |
| `rpcq/b92490.html` | 92490 maison Louis-Pouliotte | `db5ac12ca64dbc5e9386e316a78359bc8721720f9072e19c413be22ee5a44b76` |
| `rpcq/b92475.html` | 92475 maison Morisset | `4df384646ecd4c71a603657d6a4c2dcc59a0e36a0352db465a4c9efc0a926cc5` |
| `rpcq/b92667.html` | 92667 maison Gagnon | `0fe2a574a2234504e2e1287e0e498c62699d57cc0435511691ea8a69cf7e3980` |
| `rpcq/b92660.html` | 92660 maison Joseph-Canac-Dit-Marquis | `66be671deb58f1ee0dd3f3c00f4ccce68b69632b9864441fa7af797772ac571e` |
| `rpcq/b235048.html` | 235048 maison Canac-Marquis | `15310f45c3f6383bc3d8ec104ec3e219398ec15d93c149ca7f51d6088d29b9a9` |
| `rpcq/search_maison-morisset.html` | keyword search, `type=IMMOB` | `25a6c3a049fa2e07a1b731f9a44c1115e5301f16a350e1a7aae89f295a21061f` |

## 2. What parsed

`parse.py` reads `inventaire_synthese.txt` (79 pages) and writes `parsed.json`. It prints
**11/11 courant blocks parsed with a characteristics list.**

* All eleven "Principaux éléments caractéristiques" lists, verbatim, 4–10 bullets each.
* The distribution sentence in each of the eleven blocks.
* 65 example addresses from the ten facing photo plates plus the one inline caption on p. 46.
* Table 1 on p. 47, the composition of the inventory, by municipality and by cote.

`emit_types.py` writes `data/places/ile-orleans/types/*.yaml` from `parsed.json` plus hand-authored
English, so no French is ever retyped. `emit_types.py --check` re-reads the eleven files on disk and
compares every `profile_fr` string and every `example_addresses` entry against the parse; it
currently prints `OK — 11 records, 0 problem(s)`.

### Page anchors: three of the brief's are off

The PDF's page images and its printed folios agree throughout, so "page 26" means both. Three of the
anchors in the Part 9 brief do not match this file:

| courant | brief | actual |
|---|---|---|
| cottage vernaculaire américain | 35 | **36** |
| maison Boomtown | 39 | **40** |
| régionalisme québécois | 43 | **44** |

The other eight (26, 28, 30, 32, 34, 38, 42, 46) are correct. Page 35 is the éclectisme victorien
photo plate, 39 the maison cubique plate and 43 the Arts & Crafts plate — i.e. the brief's three
wrong anchors each name the *preceding* courant's plate page.

### Verification of the pattern record (p. 26)

The brief transcribes `maison-inspiration-francaise` in full. Parsed against the PDF, the
transcription **matches** — the same eight bullets in the same order and the same wording, merely
grouped by the brief into five column-sized strings rather than kept as separate bullets. The
distribution sentence ("relativement abondantes", "toutes les municipalités") and all six example
addresses (3463, 4657 Sainte-Famille; 1347 Saint-Jean; 313 Saint-Pierre; 155A Saint-François; 960
Saint-Laurent) also match. Nothing about this file differs from what the brief read.

### The two gaps the brief left open — both closed

**(a) Modernisme, p. 46.** Parsed in full. The block's decisive sentence: *« À l'île d'Orléans, nous
n'avons répertorié qu'une résidence issue de l'architecture moderne. »* One house out of 659, named
in the caption below the list: *« La maison Paul-Brunet située au 37, chemin de l'Église témoigne de
l'architecture moderne. Son architecture s'inspire notamment d'un paquebot. »* The caption gives no
municipality. The five characteristics are: *Volumétrie simple et dépouillée d'ornements; Plans
libres qui créent des formes très variées; Toits plats ou de formes sculpturales; Matériaux modernes
tels que le béton et l'acier, alors que l'expressivité des matériaux remplace les éléments
d'ornementation; Grandes surfaces vitrées dont des fenêtres en bandeau horizontal.* The record is
therefore published with real content, not with `profile_note: "Block not yet transcribed"`.

**(b) The quantitative diagnostic, pp. 47–50.** Table 1 parsed:

| municipality | A | B | C | D | E | total | supprimé |
|---|---|---|---|---|---|---|---|
| Sainte-Famille | 6 | 11 | 40 | 26 | 2 | 85 | 6 |
| Sainte-Pétronille | 1 | 17 | 64 | 36 | 0 | 118 | 5 |
| Saint-François | 7 | 11 | 25 | 18 | 0 | 61 | 2 |
| Saint-Jean | 5 | 32 | 90 | 51 | 1 | 179 | 4 |
| Saint-Laurent | 5 | 10 | 77 | 36 | 3 | 131 | 2 |
| Saint-Pierre | 3 | 14 | 55 | 10 | 3 | 85 | 0 |
| **total** | **27** | **95** | **351** | **177** | **9** | **659** | **19** |

Cross-checked against the report's own prose on p. 48, which gives the same five figures with
percentages (4 %, 15 %, 53.5 %, 26 %, 1.5 %) and states that the 27 exceptional buildings include
"les 13 bâtiments déjà classés immeubles patrimoniaux". Composition: 28 buildings added, 19 removed
(9 burnt, 10 demolished since the 1970 inventory), giving 659. These fill the `grading` counts that
the brief left null.

### Date flag, confirmed

The file is served as `…maj2025.pdf` and its PDF ModDate is 2025-06-20, but page 1 reads **"Août
2014"** and the methodology section says *« L'essentiel du travail sur le terrain s'est échelonné des
mois d'octobre à décembre 2013. Les travaux ont repris au mois de mai 2014 »*. Recorded in every type
record's `source_generation` and in `## notes` (d).

## 3. What did not parse, or was not attempted

* **`inventaire_immobilier_2026.pdf`** — held as the current statutory inventory but not parsed into
  records. It is a 44-page tabular list printed from a spreadsheet, not a typology.
* **Per-courant counts.** The inventory gives the cote distribution by municipality but never says
  how many buildings belong to each of the eleven courants, so `count_in_place` is null everywhere
  except `modernisme`, where the text states there is exactly one.
* **Sector assignment for six of the eleven types.** The inventory does not map courants to unités de
  paysage. `sectors` is filled only where a source sentence supports it — the plan de conservation
  for the neoclassical house (village sectors) and the Regency cottage (villégiature), the inventory
  itself for Arts & Crafts and régionalisme (Sainte-Pétronille), and both for the French-inspiration
  house. The other six carry `sectors: null` rather than an inferred value.
* **`conservation` per type** — left null; the plan's orientations are organised by intervention and
  by landscape unit, not by house type. That join is Part 9b.
* **The RPCQ keyword search endpoint.** `rechercheProduit.do` 404s and `rechercheMotCle.do` needs
  `motCle=` and `type=IMMOB`; the working form is recorded above.
* **A source typo, left as found.** The p. 39 caption for the maison cubique at 3492 chemin Royal
  reads "à **Sainte**-Jean". The parse reproduces it and the encoded `example_addresses` entry keeps
  the caption's wording with a `note` recording the error; it is not silently corrected.
* **Two registers of municipality name.** The photo captions print short parish names
  (Saint-Jean, Saint-Laurent); the RPCQ and `place.yaml` use the legal ones
  (Saint-Jean-de-l'Île-d'Orléans). `example_addresses[].municipality` keeps the caption's wording;
  the derived `municipalities[]` index on each type record is normalised to the legal names so it
  joins to `place.yaml`.

## 4. Licence findings

### Nothing from RPCQ, the MRC, Patri-Arch or a municipality is in `assets/`

The synthesis states its own terms on p. 3: *« Patri-Arch cède à la MRC de l'Île-d'Orléans les droits
d'utilisation pour l'ensemble des textes, des photographies et des illustrations réalisés dans le
cadre de ce mandat … Advenant l'utilisation pour des fins de publications (impressions ou web) …
la mention "© Patri-Arch" doit se retrouver en tout temps dans les crédits associés aux textes et
dans la légende accompagnant chacune des photographies et illustrations. »* That is a credit
requirement attached to a rights transfer between two named parties, not a public licence. The
inventory's ten photo plates are therefore recorded as `photos[]` entries with `file: null`,
`kind: placeholder`, `licence: "permission required"` and a `source_url` pointing at the PDF — one
per type record, naming the page and what it shows. RPCQ images are © Gouvernement du Québec and the
fiche pages carry `data-flagtousdroitsreserves="true"`; none were downloaded.

### Wikimedia Commons — every file checked individually before download

Checked through the MediaWiki API (`action=query&prop=imageinfo&iiprop=url|extmetadata`) on
17 August 2026. Licence, author and file URL go into each `credit` string.

| file in `assets/` | Commons file | author | licence | `Restrictions` |
|---|---|---|---|---|
| `ferme-saint-pierre-commons.jpg` | Arrondissement historique de l'Île-d'Orléans, Ferme à Saint-Pierre… | Marc-Lautenbacher | CC BY-SA 4.0 | none |
| `maison-morisset-commons.jpg` | Maison Morisset, Sainte-Famille, île d'Orléans, Québec.JPG | Benoit Rochon | CC BY-SA 3.0 | none |
| `manoir-mauvide-genest-commons.jpg` | Lieu historique national du Canada du Manoir Mauvide-Genest, vue du chemin du Roy.jpg | Marc-Lautenbacher | CC BY-SA 4.0 | none |
| `7327-chemin-royal-cuisine-ete-commons.jpg` | 7327, Chemin Royal, Saint-Laurent-de-l'Île-d'Orléans 01.jpg | Thomas1313 | CC BY-SA 4.0 | none |

**Checked and rejected.** `Maison Drouin - 23 juin 2018.jpg` is CC BY-SA 4.0 and the uploader
(RaphaëlFFL) declares "own work", but the file description also reads *« crédit photo Sébastien
Girard »*. Two different people are named as the author of the same photograph, so the attribution
cannot be written correctly and the file is not used. The maison Drouin is still cited as a
`related_buildings` anchor with its RPCQ id; only the photograph is dropped.

All four are in `assets/places/ile-orleans/`, resized to 1600–1920 px on the long edge. The author,
the licence and the Commons file URL are written into each `credit` string, which is what CC BY-SA
attribution requires.

**Rate limiting, and the route that works.** Direct requests to `upload.wikimedia.org` — both the
`/thumb/…` path and the original — returned HTTP 429 with *"Your request does not comply with our
robot policy"* for every file after the first, and kept doing so through a long retry loop with a
descriptive User-Agent. The `commons.wikimedia.org/wiki/Special:FilePath/<file>?width=N` route
succeeds where the direct one does not, though it is also intermittently throttled and needs
retrying. The `api.php` endpoint was never throttled, which is why every licence check went through
it. Anyone re-running this should use `Special:FilePath` and expect to retry.

### Anchor houses — ids verified, ids dropped

Verified against the fiche, and published:

| building | RPCQ id | municipality | statut |
|---|---|---|---|
| Manoir Mauvide-Genest | 92670 | Saint-Jean-de-l'Île-d'Orléans | Classement 1971-12-08; LHN Canada 1993-01-01 |
| Maison Drouin | 102270 | Sainte-Famille | Classement 2010-02-11 |
| Maison Gendreau | 92491 | Saint-Laurent-de-l'Île-d'Orléans | Classement 1964-08-12 |
| Maison Louis-Pouliotte | 92490 | Saint-Laurent-de-l'Île-d'Orléans | Classement 1973-11-28 |
| Maison Morisset ("La Brimbale") | 92475 | Sainte-Famille | Classement 1962-06-07 |
| Maison Gagnon ("Maison L'Âtre") | 92667 | Sainte-Famille | Classement 1961-12-06 |

Dropped, exactly as the brief warned:

* **maison Ferland** — the register's only *Maison Ferland* is **206873, Sorel-Tracy, Montérégie**.
  Nothing of the name on this island. "Chemin Ferland" is a street in Saint-Laurent, and the
  inventory prints an example address at 130 chemin Ferland, which is how a name-match would have
  produced a false positive.
* **maison Beaulieu** — no record on the island. The six *Beaulieu* houses in the register are in
  Montréal, Mauricie, Bas-Saint-Laurent and the Laurentides. "Pointe de Beaulieu" and the fief de
  Beaulieu are place-names.
* **maison Canac-Marquis** — both records exist and neither is here. **92660** *Maison
  Joseph-Canac-Dit-Marquis* is in **Québec** city; **235048** *Maison Canac-Marquis* is in
  **Saint-André, Bas-Saint-Laurent**. The Canac dit Marquis family connection to the maison Drouin is
  real, but it is a family, not a building record.

Independent confirmation: the RPCQ fiche for the site names all nineteen classed immeubles, and
Ferland, Beaulieu and Canac-Marquis are not among them. The maison Morisset build date of 1678 that
circulates in secondary sources is also not what the fiche says — it gives *« construite avant 1699
et agrandie avant 1727 »*, which is what is encoded.

## 5. Reproducing

```bash
cd sources/ile-orleans
pdftotext -layout inventaire_synthese.pdf inventaire_synthese.txt
python3 parse.py                 # human-readable dump; prints 11/11
python3 parse.py --json > parsed.json
cd ../.. && python3 sources/ile-orleans/emit_types.py         # rewrite the eleven type records
python3 sources/ile-orleans/emit_types.py --check             # confirm no drift
python3 scrub_secrets.py --check                              # no live tokens in sources/
python3 build.py
```
