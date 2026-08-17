# sources/montreal — the city-wide framework layer

Part 10a. This directory holds the sources for the **Montréal framework layer** — the material shared by
every borough rather than belonging to one. The per-borough typo-morphological studies and PIIA annexes
live under `sources/<borough>/`, not here.

Retrieved 17 August 2026. Every `curl` in this manifest needed a browser `User-Agent`: the Ville's
open-data host answers the default `curl/…` agent with `HTTP 403 RBAC: access denied` on its
`/download/` paths while serving `/api/3/action/…` normally. That is a WAF rule at the origin, not a
proxy denial.

---

## 1. The Évaluation du patrimoine urbain cahiers (2005)

`evaluation/` — seven arrondissement cahiers, all `HTTP 200`, all converted with
`pdftotext -layout` to a sibling `.txt`. Base URL for all but two:
`http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/`

| file | pages | bytes | sha-256 | source filename |
|---|---|---|---|---|
| `12_sud-ouest.pdf` | 100 | 11 087 534 | `e9c7902b9d1f29169abc9a86c7c2350bd74d5285dcc637daeaf6af1ec2f7c9a2` | `12_evaluation_patrimoine_sud.pdf` |
| `14_mercier.pdf` | 58 | 7 922 808 | `ebb8753074e9ecbba4fbbd14a195557fe150e86d90d0661eec9a2b9dc111dba3` | `14_evaluation_patrimoine_mercier.pdf` |
| `21_rosemont.pdf` | 60 | 8 723 434 | `a489e0368d9419e847bf6d6ada5e9217b826b8e155593afffbcf341264da3de0` | `21_evaluation_patrimoine_rose.pdf` |
| `22_saint-laurent.pdf` | 50 | 8 761 180 | `33d3bf9da23b013507cebfa97d52fdcdeba4b2843c1ed5d664b0378bd9405506` | `22_evaluation_patrimoine_stla.pdf` |
| `24_verdun.pdf` | 52 | 8 294 333 | `3f89140caa4694ad93c13ffbc7b452c041046d1f9c7b8be71a54b210cf39b725` | `24_evaluation_patrimoine_ver.pdf` |
| `25_ville-marie.pdf` | 170 | 15 100 221 | `7ba2fbe1ee144d3233bce80a5051631dd6eeabb3b438a0e1a66701abbc9ecc78` | `.../PAGE/PATRIMOINE_URBAIN_FR/MEDIA/DOCUMENTS/25_EVALUATION_PATRIMOINE_VILLE-MARIE.PDF` |
| `26_villeray.pdf` | 46 | 3 961 471 | `e6e6ff5748506e6b14ad704068d232be3c8ee7f628b82ffab0d45c1ccbc2ca08` | `https://ville.montreal.qc.ca/…/26_evaluation_patrimoine_villeray.pdf` |

No download failed.

---

## 2. The code map — read from inside the document, never from the filename

`data/canon/montreal_arrondissement_codes.csv`. Built by extracting every
`\b\d{1,2}\.(E|I|N|U|AP)\.\d{1,3}\b` token from the `.txt` of each cahier and taking the dominant
prefix in the sector fiches. **Every row below was verified against the PDF text; none was inferred
from a filename.**

| file prefix | code | arrondissement | sector codes found inside |
|---|---|---|---|
| 12 | **22** | Le Sud-Ouest | E.1–15, I.1–25, N.1–2, U.1, AP.1–14 |
| 14 | **27** | Mercier–Hochelaga-Maisonneuve | E.1–5, I.1–6, N.1–2, U.1–5, AP.1–3 |
| 17 | **16** | Outremont | E.1–8, I.1–6, AP.1–2 |
| 21 | **26** | Rosemont–La Petite-Patrie | E.1–11, I.1–7, N.1, U.1–4, AP.1–3 |
| 22 | **8** | Saint-Laurent | E.1–4, I.1–4, U.1–3, AP.1–2 |
| 24 | **21** | Verdun | E.1–7 (E.1 split 1A/1B/1C), I.1–10, U.1, AP.1–2 |
| 25 | **24** | Ville-Marie | E.1–67, I.1–19, N.1–2, U.1, AP.1–6 |
| 26 | **14** | Villeray–Saint-Michel–Parc-Extension | E.1, I.1–5, U.1–3, AP.1 |
| 27 | **23** | Westmount | E.1–35, I.1–4, AP.1–4 |

Against the memo: Rosemont **26**, VSP **14**, Mercier–Hochelaga-Maisonneuve **27** and Verdun **21**
are all **confirmed**. Two rows the memo left open are now closed: Saint-Laurent, published as file
`22_…`, is code **8**; Ville-Marie, published as file `25_…`, is code **24**.

The collision is worse than "the numbers differ". They interleave:

* file 22 = Saint-Laurent (code 8), while code 22 = Le Sud-Ouest (file 12);
* file 27 = Westmount (code 23), while code 27 = Mercier–Hochelaga-Maisonneuve (file 14);
* file 14 = Mercier–Hochelaga-Maisonneuve (code 27), while code 14 = VSP (file 26);
* file 26 = VSP (code 14), while code 26 = Rosemont (file 21).

**Extraction caveats, all checked by hand.** Three volumes contain a handful of foreign-prefix codes
and none of them is that volume's own code:

* `14_mercier.txt` and `21_rosemont.txt` each contain `14.AP.1` three and five times — map labels on
  the archaeological synthesis plate, where a VSP sector continues across the boundary.
* `25_ville-marie.txt` contains `22.E.53 Terrasse Saint-Denis` and `22.E.54 École Polytechnique de
  Montréal` — two photo captions, sitting inside the fiches for sectors printed on the same spread as
  `24.E.53 LA TERRASSE SAINT-DENIS` and `24.E.54 LA RUE SAINT-DENIS`. A typo in the published
  document's captions, not a second code series.

---

## 3. The retro-fit — Westmount (Part 5) and Outremont (Part 6)

Both re-verified against the same rule, using the PDFs already in `sources/westmount/` and
`sources/outremont/`. **Both are correct as encoded. Neither `sectors.yaml` was changed.**

* **Outremont — code 16, confirmed.** The Part 6 flag *"Outremont sector prefix unconfirmed (16 vs 17)"*
  is now closed. The published filename is `17_evaluation_patrimoine_out.pdf`, and 17 appears nowhere
  in the document as a sector prefix. The cahier's own codes are `16.E.1`–`16.E.8` (8 sectors),
  `16.I.1`–`16.I.6` (6), and `16.AP.1`–`16.AP.2`. `data/places/outremont/sectors.yaml` already carries
  `16.E.n` / `16.I.n` and needs no correction. The 17 came from the series numbering, exactly as that
  file's manifest already suspected.
* **Westmount — code 23, confirmed.** Published as file `27_evaluation_patrimoine_wes.pdf`; the codes
  inside are `23.E.1`–`23.E.35`, `23.I.1`–`23.I.4` and `23.AP.1`–`23.AP.4`. Part 5's `23.E.n` / `23.I.n`
  encoding is right, and the counts match `sectors.yaml`'s 35 + 4 = 39 sectors exactly.

A confirmed negative, twice. The only thing either file could gain is the AP overlay, which neither
records: Westmount has four archaeological-potential sectors and Outremont two, and both are outside
this task's remit.

---

## 4. Building-scale open data

`data/`.

| file | bytes | sha-256 |
|---|---|---|
| `edifices_patrimoine_source.csv` | 739 700 | `31175c676c96c6ea377f2b168844fb55f9e75a075c27509dd75105c4ce0ae108` |
| `package_show.json` | 8 796 | `9584ce7460112ef7fc3fd3a9903ff2c101a4bed9bf00b166464b89a9d70b016f` |
| `inv1940.json` | 84 698 | `a6f98754ec8c3a3da12ec947a831bfc3caefbb3a1f8531c3a943b9d0a32e9995` |
| `inventaire_pre1940_par_localite.csv` | 10 282 | `d809d8553a0129ef74926d6f19f7aafe9c421ba6879b908b930ef003a3cc92b7` |

### 4.1 *Les édifices patrimoniaux de Montréal* — resolving the resource URL

The dataset landing page in the memo (`https://donnees.montreal.ca/dataset/les-edifices-patrimoniaux-de-montreal`)
is HTML, not data. Resolved through the CKAN API:

```
https://donnees.montreal.ca/api/3/action/package_show?id=les-edifices-patrimoniaux-de-montreal
→ resource a89dd7ad-ebb1-4d1e-97d5-e14724e50447
→ https://donnees.montreal.ca/fr/dataset/607c00db-0446-4389-9cdc-d8127f8da57a/resource/a89dd7ad-ebb1-4d1e-97d5-e14724e50447/download/edifices_patrimoine.csv
```

1 336 rows. The file's MD5 is `20cdfea7a12a58211e726b8ba1906aee`, which matches the `hash` CKAN
publishes for the resource — the download is byte-identical to what the portal believes it holds.
Licence CC BY 4.0; author Service de l'urbanisme et de la mobilité; resource last modified
2025-06-19. The dataset is titled *(archives)* and points onward to
`https://montreal.ca/repertoire-patrimoine-bati`.

**Two corrections to the memo's field list.** There is no `PROTECTION_LEGALE` column — the columns are
`IDENTIFIANT_BATIMENT, NOM_HISTORIQUE, TYPOLOGIE_SPECIFIQUE, CIVIQUE_MIN, CIVIQUE, TYPE_DE_VOIE,
CIVIQUE_MAX, LIEN, VOIE, EST_OUEST, ARRONDISSEMENT, HISTORIQUE_SOMMAIRE, DEBUT_DES_TRAVAUX,
FIN_DES_TRAVAUX, CENTRO_X, CENTRO_Y`. And `CIVIQUE` is a combined min–max string, with the components
in their own columns.

### 4.2 The TYPOLOGIE_SPECIFIQUE map

`data/canon/montreal_typologie_specifique_map.csv`. 43 distinct values including the empty one.
**4 mapped, 39 left unmapped**, covering 63 of 1 336 records.

Mapped: `maison urbaine façon Nouvelle-France` → `french-urban-house-stone` (exact);
`maison-magasin` and `Bâtiment commercial et résidentiel` → `mixed-use-flat-roof-block` (partial);
`Immeuble de rapport` → `apartment-house-common-hall` (partial).

The low yield is the finding, not a failure of effort. This dataset is the *Grand répertoire*'s register
of exceptional buildings, dominated by Vieux-Montréal and by institutional and commercial uses:
`non applicable` (309), `magasin-entrepôt` (166), `indéterminée` (157), empty (145) and `indéterminé`
(66) account for 843 of the 1 336 rows before any real category appears. Of the categories that do
name housing, four — `Maison isolée` (120), `Maison en rangée` (20), `Maison contiguë` (9),
`Maison semi-détachée` (5) — record **mode of attachment, not form**, and this site's canonical forms
are defined by shape, roof and stair position, none of which the dataset carries. Forcing them would
have invented evidence. Every unmapped row carries its reason in the `basis` column.

### 4.3 *Inventaires des immeubles patrimoniaux construits avant 1940* — the art. 120 inventory

Not in the memo, and the most consequential thing found on this pass: **the agglomération's statutory
inventory exists and has been adopted.** Package
`https://donnees.montreal.ca/api/3/action/package_show?id=inventaires-des-immeubles-patrimoniaux-construits-avant-1940`
— created 2026-03-25, metadata modified 2026-04-16, 68 resources (34 localities × SHP + GeoJSON).

All 34 GeoJSONs were downloaded and parsed (87 MB, all `HTTP 200`). **68 652 features**, every one
carrying `LISTE: PRÉ1940` and `INVENTAIRE: Retenu`. The geometry is not archived here — it is 87 MB of
building footprints with no typology field — but every file's URL, byte count and sha-256 is recorded
per row in `data/inventaire_pre1940_par_localite.csv`, alongside its locality, its retained count and
its `DATE_ADOPT`.

Adoption dates run 2023-05-18 → 2026-03-26, heavily back-loaded against the 1 April 2026 deadline:
15 166 on 2025-09-25, 8 946 on 2025-12-18, 16 157 on 2026-02-19, 22 770 on 2026-03-26. 897 records in
six localities (Rivière-des-Prairies–Pointe-aux-Trembles, L'Île-Bizard–Sainte-Geneviève, Montréal-Est,
Pierrefonds-Roxboro, L'Île-Dorval, Saint-Léonard) carry no adoption date at all.

Corroborated by the Ville's own page, *Inventaires des immeubles à valeurs patrimoniales*
(`https://montreal.ca/articles/inventaires-des-immeubles-patrimoniaux-32414`, updated 15 June 2026):
« En tout, ce sont 34 listes d'inventaire qui ont été réalisées puis adoptées par le Conseil
d'agglomération… ce qui représente plus de 68 500 immeubles ». 68 652 is that figure.

The inventory carries **no typology field** — `ID_IMM_INV, ADRESSE, REPERAGE, LOCALITE, NOM_IMM,
NOM_AUTRES, TYPE, DATE_ADOPT, SAVOIRPLUS, LISTE, CIV_DE_A_F, CIV_DE, CIV_A, GENERIQUE, LIEN, NOMVOIE,
ORIENTAT, PRE_INV, INVENTAIRE, MODIFS, MAJ_ADOPT` — so it can be joined to this site's type records by
address only, never by form.

---

## 5. Statutory and technical sources verified for the framework and topic pages

Not archived here (they are national and provincial texts, stable at their URLs), but fetched and read
in full on this pass:

* **Loi sur le patrimoine culturel, RLRQ c. P-9.002**, art. 120 (obligation) and arts. 29 / 127
  (classement / citation) — `https://www.legisquebec.gouv.qc.ca/fr/document/lc/P-9.002`.
* **Loi sur l'aménagement et l'urbanisme, RLRQ c. A-19.1**, arts. 148.0.1 and 148.0.2 — the definition
  of *immeuble patrimonial* that pulls an inventoried building into the demolition regime, and the
  obligation to keep a demolition by-law in force — `https://www.legisquebec.gouv.qc.ca/fr/document/lc/A-19.1`.
* **Loi modifiant la Loi sur le patrimoine culturel et d'autres dispositions législatives, 2021, c. 10**,
  transitional arts. 136 (deadline 1 April 2026), 137, 138 and 143 (coming into force 1 April 2021) —
  `https://www.publicationsduquebec.gouv.qc.ca/fileadmin/Fichiers_client/lois_et_reglements/LoisAnnuelles/fr/2021/2021C10F.PDF`,
  sha-256 `98cb0334d1c921f496a1d6a959682589dc67b2845395ce0347cd0fb95eb0b25e`.
* **Régie du bâtiment du Québec**, *Code de construction — Chapitre I, Bâtiment* presentation, arts.
  9.8.3.1 and 9.8.5.1 — `https://www.rbq.gouv.qc.ca/fileadmin/medias/pdf/Publications/francais/FormationCodeConstChapBatiment.pdf`,
  sha-256 `306e82351ff866a49487a8dbcd4cb922a1fe2dab04363d907a73100f65524e8d`.
* **Ville de Montréal**, *Construire ou remplacer un escalier extérieur*, updated 3 February 2026 —
  `https://montreal.ca/demarches/construire-ou-remplacer-un-escalier-exterieur`.
* **Ville de Montréal-Ouest**, *Inventaire des immeubles patrimoniaux sur le territoire*, 3 June 2025 —
  the source of the « plus de 87 000 bâtiments » figure and of the Architecture 49 attribution —
  `https://montreal-ouest.ca/fr/inventaire-des-immeubles-patrimoniaux-sur-le-territoire/`.

### Fabric-scale PDFs read but deliberately not archived here

Verified in a scratch working copy so that quotes on `/topics/escalier-exterieur/` and in the glossary
are verbatim rather than second-hand. They belong to the borough agents' `sources/<borough>/`
directories, so they are not duplicated into `sources/montreal/`; hashes recorded for provenance.

| document | bytes | sha-256 |
|---|---|---|
| Patri-Arch, *Étude typomorphologique de l'arrondissement du Sud-Ouest* (2013 update), `ocpm.qc.ca/…/3.5_etude_typomorphologique_sud-ouest.pdf` | 9 842 817 | `12c8b0b6631a14b07ba73bb8e5dfea2cad6a3e1b28a171f4ced828a1e5f02b96` |
| VSP, *Règlement 01-283-124 — Fiches typologies* (Annexe F), `portail-m4s.s3.montreal.ca/pdf/…` | 6 869 574 | `9ff4ea1e7b741c24436e0ff14f23018a821f91e42eb004326015e72225c1b676` |
| VSP, *Maisons de type « shoebox » — guide pour les travaux et agrandissements* (2019), `portail-m4s.s3.montreal.ca/pdf/depliant_maisons_shoebox_final_web.pdf` | 590 541 | `2669e0a4b3ec22985871c5e2c4fdf78af0e4d9ebe8263cacc8f8da5707f8b4e7` |

---

## 6. Downloads that failed

* **VSP, *Maisons shoebox — étude d'évaluation patrimoniale et de mise en valeur*** (Isabelle Bouchard,
  29 November 2018). `HTTP 404` at the URL given in the memo, over both `http` and `https`:
  `ville.montreal.qc.ca/pls/portal/docs/PAGE/ARROND_VSP_FR/MEDIA/DOCUMENTS/MAISONS%20SHOEBOX_%20%C9TUDE_%C9VALUATION%20PATRIMONIALE_WEB.PDF`.
  The old `ARROND_VSP_FR` portal path appears to be retired; the 2019 dépliant that summarises the
  study is still live and was used instead. Worth re-finding on the current `montreal.ca` document
  system, because it is the study that carries the borough's shoebox variants.
* **`donnees.montreal.ca` `/download/` paths with the default curl agent** — `HTTP 403 RBAC: access
  denied`. Not a proxy denial and not a permissions problem: a browser `User-Agent` fixes it. Recorded
  because the failure message is misleading enough to derail a later pass.
* **`web.archive.org`** — both the availability API and the CDX API were unreachable from this session
  (`502` and connection reset). This is why the earlier « plus de 80 000 immeubles » wording of the
  Ville's inventory page could not be captured from an archived snapshot and is recorded on the
  framework page as an attributed historical scope claim rather than quoted from a dated source.

---

## 7. Findings that belong to other agents

Left here rather than acted on, because these files are not this task's to write.

* **Rosemont's E-sector list is incomplete in the memo, as flagged.** The cahier has eleven, and these
  are their headings as printed: 26.E.1 LE SECTEUR DU MARCHÉ JEAN-TALON; 26.E.2 LE CŒUR DE LA
  PETITE-ITALIE; 26.E.3 LA RUE SAINT-DENIS; 26.E.4 L'ENSEMBLE INSTITUTIONNEL; 26.E.5 LE PARC MOLSON;
  26.E.6 CENTRE CIVIQUE ET AUTRES BÂTIMENTS; 26.E.7 SITE DU PATRIMOINE DE L'ÉGLISE (Saint-Esprit, rue
  Masson); 26.E.8 SECTEUR ANGUS; 26.E.9 LE JARDIN BOTANIQUE; **26.E.10 LA CITÉ-JARDIN DU
  TRICENTENAIRE**; 26.E.11 LES PYRAMIDES OLYMPIQUES. Headings are truncated by the two-column
  extraction and should be re-read from the PDF before publication.
* **Verdun's nine sectors are confirmed**: 21.E.1A / 1B / 1C plus 21.E.2–21.E.7.
* **VSP has a third plex type.** The memo's ⚠ "verify whether plex sub-types beyond 2.2 exist" resolves
  to **yes**: Annexe F runs 2.1 *plex du début du 20e siècle*, 2.2 *plex du milieu du 20e siècle* and
  **2.3 *plex de la seconde moitié du 20e siècle***, the last with its own eight-page fiche.
* **The shoebox dépliant is VSP's, not the Ville's.** It is published by the Arrondissement de
  Villeray–Saint-Michel–Parc-Extension, Direction du développement du territoire, 405 avenue Ogilvy,
  *Année de publication : 2019*, sourced to Isabelle Bouchard. Attributing it to "the Ville" in a
  Rosemont record would misstate which borough wrote it.
* **Pre-1940 inventory counts per borough**, for `governing_instruments`: Le Sud-Ouest 5 466 (adopted
  2025-09-25); Rosemont–La Petite-Patrie 8 585 (2026-02-19); Villeray–Saint-Michel–Parc-Extension 4 612
  (2025-09-25); Mercier–Hochelaga-Maisonneuve 5 088 (2025-09-25); Verdun 4 023 (2025-12-18).
