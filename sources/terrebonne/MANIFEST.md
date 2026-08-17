# sources/terrebonne — acquisition manifest

Crawled 16 August 2026 for Part 8a (Vieux-Terrebonne). All fetches with
`curl -sSL -A "Mozilla/5.0 (compatible; heritage-research/1.0)"`, 0.5 s between requests on the
225-record crawl. Checksums are sha-256 of the file as saved.

## What was fetched

| File | URL | sha-256 | bytes |
|---|---|---|---|
| `html/rpcq_231571.html` | `https://www.patrimoine-culturel.gouv.qc.ca/detail.do?id=231571&methode=consulter&type=bien` | `39bf887fc88f106d2508b747c1aab144661d61fe484a319f2bb12d77333a997b` | 67 693 |
| `rpcq_231571.txt` | *(text rendering of the above)* | `7e24803e7cbb3f391f349a1173bb036e57eb72aa502e68c02f666b6c38192f32` | 20 780 |
| `html/assoc_immo_231571_all.html` | `…/lightBox.do;jsessionid=<SID>?methode=afficher&type=immo&id=231571&typeElement=BIEN&style=ajax&d-12771-p=1&nb=300` | `93d414dd490939e4078d66bb13100cefc7ed8884431e5591e559ed8a5049f5fb` | 191 915 |
| `html/assoc_immo_231571.html` | same, first page only (17 rows) — kept as the intermediate | `638bd318ef8e98e43e33e44beaa3b5a4fbb366a6c34237fef09d7fc3c61a7e7e` | 22 687 |
| `assoc/<id>.html` ×225 | `…/detail.do?methode=consulter&id=<id>&type=bien` | per file in `assoc_sha256.txt`; concatenation `10dcd206451d5431697e905ae346fcfb0998b8dcb78e5e6d9fa6b87a0b58ec32` | 7.4 MB |
| `html/cpcq_vieux_terrebonne.html` | `https://cpcq.gouv.qc.ca/consultations-publiques/archivees/projet-de-declaration-du-site-patrimonial-du-vieux-terrebonne/` | `2601e9c23886ff00c78dd0fa8398fd6770941a073355f21ddfd34a201d99f0a8` | 75 150 |
| `cpcq_vieux_terrebonne.txt` | *(text rendering of the above)* | `bee44cb9674058a7ed0c8910761fa9322822c6adaeafa392c449eac2c0472000` | 14 126 |
| `liste_inventaire_patrimonial_2024.pdf` | `https://terrebonne.ca/wp-content/uploads/2026/01/Liste-biens-immeubles-inventaire-patrimonial-2024.pdf` | `2f9edea01093ba877f2283f8fa83a6d1c85f239445fea3a198fd38384b80ea61` | 263 926 |
| `liste_inventaire_patrimonial_2024.txt` | *(pdftotext -layout of the above)* | `d22676961533f569e6f0e9647a8e18c53b92299ecb530cd70f5e37475048104f` | 33 722 |
| `rpcq_92501.txt` | Maison Bélisle, `…/detail.do?methode=consulter&id=92501&type=bien` | `d920735f2b1427f78ad1d75ce3c2fd971d74c202448e70ef738f91cdf8e9ab77` | 10 707 |
| `rpcq_92502.txt` | Maison Roussil, `…&id=92502…` | `3d71d44ad09cb55e7caed2cbbdc88d9d723172ea6f21fb75bf3497522c7c8fd0` | 12 611 |
| `rpcq_110132.txt` | Maison Alexandre et Joseph Roussil, `…&id=110132…` | `70f16a165475d6e249929a39025d75c2d38af2e37eda6024631120c238c4919b` | 6 554 |
| `photos/commons_licences.json` | Commons API `imageinfo` for the five published photographs | `749d78804587d43447c77b9456d405a35a319e3e99de3fb09b79eed2db3e43c5` | — |
| `assoc_sha256.txt` | per-file checksums of the 225 associated-record pages | — | 225 lines |

The three `rpcq_9*.txt` / `rpcq_110132.txt` files are text renderings of pages already stored in full
under `assoc/`; the HTML originals are `assoc/92501.html`, `assoc/92502.html`, `assoc/110132.html`.

## Counts

- **225 / 225 associated immovable records fetched. Zero failures.** The list itself was read from
  `<ul class="listeBiens">` in `assoc_immo_231571_all.html`, which contains exactly 225 `<li>` rows
  with 225 distinct RPCQ ids and no blank names — matching the fiche header "Patrimoine immobilier
  associé (225)" exactly. (Counting `<div class="contenuListeBien">` instead gives 246 because
  eleven rows carry a nested second block; the `<li>` count is the authoritative one.)
- Reduced to `data/places/terrebonne/inventory.csv`, 225 data rows, columns
  `rpcq_id, name, category, date, address, municipality, statut, statuts_anterieurs, in_registre, url`.
- Statut tally across the 225: **4 Classement — Immeuble patrimonial**, 6 further
  "Classement — Situé dans un immeuble patrimonial" (components of the Île-des-Moulins ensemble,
  id 92594), 28 Citation (Municipalité de Terrebonne, all dated 2021-09-13), 149 Inventorié,
  120 Délimitation, 225 Déclaration (2026-05-20). The four classed immeubles are id 92594
  (Ensemble de l'Île-des-Moulins), 92501 (Maison Bélisle), 92500 (Maison Joseph-Augé) and 92502
  (Maison Roussil) — confirming the fiche's "Il compte quatre immeubles patrimoniaux classés".
- Genuine gaps in the source, not parser failures (each re-checked against the saved HTML): 1 record
  with no `Usage` block (238762), 4 with no `Adresse` (105690, 105693, 105694, 238800), 17 with no
  `Date`.
- 2024 MRC list PDF: 10 pages, fiches numbered 1–609 with none missing, 104 marked
  "Retirée / Résolution 13 963-04-22" — 505 live entries across the whole MRC, not only the declared site.

## What could NOT be fetched

- **`terrebonne.ca` HTML pages — blocked, HTTP 403.** `vieux-terrebonne-patrimoine/`,
  `reglements-permis/reglement-sur-la-citation-des-biens-et-immeubles-patrimoniaux/` and
  `inventaire-du-patrimoine/` all returned a Cloudflare "Just a moment…" JavaScript interstitial with
  status 403, under both a research user-agent and a full desktop-browser user-agent, and through
  WebFetch as well as curl. The 403 bodies were deleted rather than kept as if they were sources.
  **The Internet Archive fallback was also unavailable** — `archive.org/wayback/available` returned
  "Internet Archive services are temporarily offline" at the time of the crawl.
  Consequence: Règlement 810's text, the Règlement d'urbanisme 1011 PIIA articles, and the Bergeron
  Gagnon inventory page are **carried from the Part 8 brief and not verified**, and are flagged as
  such in `place.yaml`, `sources.yaml` and `prose.md`. One municipal fact was recovered from the
  provincial side instead: the Citation statut on 28 associated RPCQ records is dated 2021-09-13,
  which corroborates the by-law's stated adoption date of 13 September 2021.
  The PDF at `terrebonne.ca/wp-content/…` downloaded without trouble — only the HTML pages are behind
  the challenge.
- The RPCQ fiche's own six photographs were not downloaded: the page marks them
  `data-flagtousdroitsreserves="true"` and the site footer asserts © Gouvernement du Québec.

## Notes on the RPCQ crawl

`lightBox.do` requires the servlet's **path-parameter** session id, not a cookie. Calling
`lightBox.do?type=immo&…` returns the RPCQ home page; calling
`lightBox.do;jsessionid=<SID>?type=immo&…` returns the list. Obtain `<SID>` by fetching the fiche
with a cookie jar and reading `JSESSIONID`. The list paginates through `d-12771-p=<n>`; passing
`nb=300` returns all 225 rows in a single response, which is what was used.

## Text-vs-brief verification

All 28 `characteristics_fr` clauses in `data/places/terrebonne/sectors.yaml` were checked
programmatically against `rpcq_231571.txt` after Unicode normalisation: **28/28 verbatim**, and the
fiche's four sector sentences are consumed with zero uncovered text. One difference from the brief's
transcription, recorded rather than silently resolved:

- **UP-1 has ten clauses in the fiche, not the nine the brief lists.** The brief omitted
  "ses bâtiments résidentiels dominant avec également des témoins bâtis d'activités commerciales et
  artisanales", having rendered it into English as the sector's `summary_en` instead. It is restored
  here in the fiche's own position (fifth), because §2.1.3 and the Part 8a acceptance criteria both
  ask for the *full* verbatim list. Noted in the sector's `note` field.

Two further discrepancies between the brief and the verified fiches, resolved in favour of the fiche:

- **Maison Roussil's builder.** The brief says "built by Noël-Théodore Roussil (mayor 1876–77)". RPCQ
  id 92502 says the house "a été construite par et pour Roussil" and describes him as
  "maître menuisier et capitaine de milice", giving his dates as *vers 1798-1890*. It says nothing
  about a mayoralty. The mayoralty claim is not encoded.
- **Maison Roussil's date.** The brief says "c. 1825–1830"; the RPCQ description says
  "construite vers 1830" and the associated-records list gives "1830 (Construction)". Encoded as
  c. 1830. (The neighbouring maison Alexandre et Joseph Roussil, id 110132, is the one whose RPCQ
  date field reads "vers 1825 – vers 1830".)
- **Maison Bélisle's alias.** The brief writes "Maison Perra"; the fiche names the builder
  **Jacques Perras** (1725–1786). Spelled Perras.

The McTavish discrepancy the brief flagged is confirmed exactly as described: `rpcq_231571.txt`
line 119 (valeur patrimoniale) prints "Simon McTavish (vers 1750-1844)" and line 142 (informations
historiques) prints "Simon McTavish (vers 1750-1804)". 1804 is used; the discrepancy is footnoted in
`prose.md`.

## Photographs — licence decisions

Every image was checked through the Commons API before download; raw metadata in
`photos/commons_licences.json`. Five published, one rejected.

| Published as | Commons file | Author | Licence | Match |
|---|---|---|---|---|
| place hero | `File:Ile-des-Moulins - 01.jpg` | Jeangagnon | CC BY-SA 4.0, own work | visual (UP-2) |
| `maison-vernaculaire-villageoise` | `File:Terrebonne, Quebec - 222-224 rue Sainte-Marie - 1.jpg` | Cantons-de-l'Est | CC BY-SA 4.0, own work | address — RPCQ 238773 |
| `maison-cossue-saint-louis` | `File:930, rue Saint-Louis, Terrebonne.jpg` | Jeangagnon | CC BY-SA 4.0, own work | address — RPCQ 232867 |
| `maison-tradition-francaise-pierre` | `File:Terrebonne, Quebec - 844, rue Saint-François-Xavier.jpg` | Cantons-de-l'Est | CC BY-SA 4.0, own work | address — RPCQ 92501, named in the uploader's description |
| `maison-neoclassique-quebecoise` | `File:Maison Roussil - 01.jpg` | Jeangagnon | CC BY-SA 4.0, own work | address — RPCQ 92502 |

All five downloaded through `Special:FilePath/…?width=1280`, so the stored files are Commons-rendered
1280 px derivatives of the originals. Author, licence and file URL are carried in each `credit` string.

**Rejected: `File:Rpcq bien 92501 240471.jpg`.** It is the obvious candidate for the maison Bélisle —
it is literally the RPCQ's own photograph of it — and it is tagged CC BY-SA 4.0 on Commons. But its
`Credit` field is the RPCQ fiche URL and its `Artist` is a Commons username, i.e. the uploader is
relicensing a Government of Québec photograph they do not own; the RPCQ marks its images
all-rights-reserved. Not used. A genuinely free photograph of the same building by an identifiable
photographer was found instead (844 rue Saint-François-Xavier, above), so nothing was lost.

## Not attempted

Part 8b items only: the Bergeron Gagnon 2015 inventory itself, the MCC presentation and written
submissions in the CPCQ dossier, and any plan de conservation for the new site (none published as of
this crawl).
