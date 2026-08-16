# Source manifest — Témiscaming

Fetched 2026-08-16 per the Part 5 v2 brief §1.2, which asks for two captures for this place: the
MRC inventory published 8 April 2026, and the RPCQ page for the Gare de Témiscaming. **One
succeeded, one failed.**

| file | bytes | url | sha-256 |
|---|---|---|---|
| `rpcq_gare_temiscaming.html` | 58,082 | https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&id=92694&type=bien | `93c527873ac870dfaaf38155a3ecb382b5403b0043a44a6a1746d1fda9d14a1b` |
| `txt/rpcq_gare_temiscaming.txt` | 13,336 | (extraction) | `e60f6a69fdf161c51249fd693020b66497eda2e5eab2eb8993b02f6754d8a46c` |

The RPCQ capture confirms, from the page itself, every element of the `classement` instrument in
`place.yaml`: address *15, rue Humphrey*; *Date : 1927 (Construction)*; *Classement — Immeuble
patrimonial — Ministre de la Culture et des Communications — 2012-10-19*; *Statuts antérieurs :
Reconnaissance, 1979-06-28* (and an *avis d'intention de classement échu, 1978-03-16*); conservation
categories *1 – Extérieur exceptionnel* and *5 – Intérieur supérieur*, i.e. exterior and interior,
not the land. Some UI strings in the saved HTML contain the server's own mojibake (double-encoded
replacement characters); the substantive French is intact.

## Failed download — MRC de Témiscamingue inventory (8 April 2026)

**Not obtained.** Attempts made on 2026-08-16:

- `https://www.mrctemiscamingue.qc.ca/` — **HTTP 503** ("upstream connect error or disconnect/reset
  before headers"), both through the egress proxy and with the proxy bypassed; a TLS handshake to
  the host succeeds, so the certificate is fine and the site itself is down or refusing.
- `https://www.mrctemiscamingue.qc.ca/culture-et-patrimoine/` — **HTTP 503**.
- RPCQ inventory register: **no entry** for the MRC de Témiscamingue (`rechercheInventaire.do`
  returns 404; a site-scoped search returns inventories for other MRCs only, e.g. Témiscouata,
  Drummond, Antoine-Labelle, but none for Témiscamingue).
- Web search returns only the 2023 launch coverage (Radio-Canada, $50,000 provincial grant, pre-1940
  scope) and general coverage of the 1 April 2026 statutory deadline — nothing confirming the
  8 April 2026 publication, the 1,730-building screen or the three retained properties.

Consequence for the data: the inventory's content is recorded in `place.yaml`,
`data/places/temiscaming/sources.yaml` (`tm-mrc-inventaire-2026`) and the `## notes` prose **as
reported at ingest and explicitly unconfirmed against the document**, because no copy of it is held
here and none could be retrieved.

## Negative finding — the 2026 inventory retains no house in Témiscaming (v2)

The inventory screened **1,730 pre-1940 buildings** across the MRC and retained, for the Ville de
Témiscaming, **three properties, none residential**:

1. Gare de Témiscaming, 15 rue Humphrey (1927) — the one building already classée;
2. Poste de relais pour le flottage du bois d'Opémican, 5555 chemin Opémican (1883);
3. Ancien bassin de charge de la Gatineau Power, lot 3 658 710, between 78 and 126 avenue Thorne.

It carries **no materials field** — only addresses, dates, roles and "particularités/justifications"
— so even a retained house would not have filled this project's profile columns. The regional house
typologies it does document (maison de colonisation, maison de colonisation à trois pignons, grande
maison carrée, maison de colonisation avec galerie ceinturante, cottage carré, maison à pignon sur
rue avec galerie ceinturante) are in **Latulipe-et-Gaboury**, not Témiscaming, and are rural
colonisation types unrelated to company housing. Both type records carry this paragraph in their
`profile_note` and **stand unchanged**.

Still outstanding (Part 5b): the separate **51-page heritage analysis by Julien Rivard, Paul
Trépanier and Manon Sartou** behind the inventory (existence reported, no public copy located), and
**Témiscaming's 1992 architectural guide**, reported in the literature as written for the town's
company housing. Either would let the two records finally carry materials, roof forms and storey
counts.

## Photographs

Licences verified through the Wikimedia Commons API (`action=query&prop=imageinfo&iiprop=extmetadata`)
on 2026-08-16, for both files the brief names in `Category:Témiscaming` (28 files in the category):

| file | licence returned by the API | committed? |
|---|---|---|
| `File:Residential section, Temiskaming, Que. (BAnQ 3971732).jpg` | **Public domain** (`License: pd`, `Copyrighted: False`); BAnQ postcard, circa 1930s, author unknown | **yes** |
| `File:Témiscaming Quebec location diagram.png` | **CC BY-SA 3.0** (`cc-by-sa-3.0`), author Gordalmighty, own work | no — a locator diagram, not a house photograph; nothing on this page needs it |

The public-domain postcard downloaded successfully this time (the v1 pass recorded a refusal from
`upload.wikimedia.org`; the same URL returned HTTP 200 today) and is committed:

| file | bytes | url | sha-256 |
|---|---|---|---|
| `assets/places/temiscaming/residential-section-temiskaming-banq-commons.jpg` | 123,633 | https://upload.wikimedia.org/wikipedia/commons/e/ef/Residential_section%2C_Temiskaming%2C_Que._%28BAnQ_3971732%29.jpg | `56ebdd330d71195bbeb03987c30f41be06d95079e1048b4f712af45eeeecb08f` |

It is 1024 × 654 JPEG and now illustrates `types/lower-town-house.yaml`. Its credit records that it
is a general view of the residential section, **not** a documented Type 171C house.

**Not committed — CCA.** The Canadian Centre for Architecture's Gabor Szilasi photographs —
PH1995:0077 ("Houses Type 171C, Elm St., looking toward the Tembec factory, Témiscaming, 1995") and
PH1995:0053 — are © CCA and permission-only. They are cited in the records' `origin_en` and
`profile_note` text instead, never reproduced.

## Reference sources not downloadable

Cited in `data/places/temiscaming/sources.yaml`:

- Canadian Centre for Architecture, "Power and Planning: Industrial Towns in Québec, 1890–1950" (1996)
  — <https://www.cca.qc.ca/en/articles/issues/11/nature-reorganized/441/power-and-planning>
- Ville de Témiscaming, "History"; The Canadian Encyclopedia, "Témiscaming"
- RPCQ, Site patrimonial du Quartier-du-Moulin, Gatineau — used only to disambiguate: that site is in
  **Gatineau**, not Témiscaming.
