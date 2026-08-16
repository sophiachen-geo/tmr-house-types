# Source manifest — Gatineau

Fetched 2026-08-16 per the Part 6a brief §1.2. The City publishes fourteen fiches, one per dominant
residential type, produced in 2023 by Enclume with Passerelles Coopérative en patrimoine and financial
support from the government of Québec. Each fiche is a four-page PDF with a credited banner photograph
served as a separate JPEG. `txt/` holds `pdftotext -layout` extractions of the fourteen fiches; those
extractions are what the type records were encoded from.

## Fiches (`fiches/`)

Base URL: `https://www.gatineau.ca/docs/guichet_municipal/patrimoine/patrimoine_bati/types_architecturaux/`
Index page: <https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal/patrimoine/patrimoine_bati/types_architecturaux>

| file | bytes | sha-256 |
|---|---|---|
| `bungalow_nord_americain.pdf` | 1,098,841 | `419f515bc268e55e350da1aa3326ad73dcbb08bafcf3d638e6af930afda21f70` |
| `duplex_mur_pignon_lateral.pdf` | 747,685 | `a7914f1e8a71480a1ed974bf0d6d6c570781c0a9dd83933a017a4a030e26e5db` |
| `edifice_mixte_toit_plat.pdf` | 950,353 | `b3d3e3bfc2ec14fb19e7478f8b46f2c0ecfd50580452daee22f095d36a7ae70a` |
| `maison_allumette_bois_1_etage.pdf` | 1,052,995 | `55f22df438374f7aa09687c110b308cb26e656888c97809c148f00028530b702` |
| `maison_allumette_bois_2_etages.pdf` | 1,043,139 | `600ba7123c2704cb51f2850f77b183ad8c9214bc14e16e33ab92c9fabc58b0c6` |
| `maison_allumette_brique_2_etages.pdf` | 1,012,306 | `e5e6c714dc70f70cdc2f131d02ae7357f8ac2df932f3b9b568747412326fa915` |
| `maison_bois_toit_plat.pdf` | 1,084,030 | `9d3b796d9b06e062c045593aa39649127b7b8f902ff38b8485fcbc757ea8ac61` |
| `maison_brique_toit_plat.pdf` | 1,020,277 | `2971d1e8c398818f2bcd56e4a2d41c6d54f2ad31c780c5ed1cb3fba998a0b1fa` |
| `maison_cadre_cip.pdf` | 1,107,929 | `6398fd333f89b1520b3c3d166ab93728612d7f57b7093eadfdae7fb5ca5b35d8` |
| `maison_cubique.pdf` | 1,136,490 | `1cdea8dcedcb6a766a1d1dfdebf9c936f824a638067402a537d5462bb00ed3e0` |
| `maison_pignon_central.pdf` | 1,059,802 | `30325cc1dbd86f2370434e4488abf2c3ca6c709c8818042705091e52f9031576` |
| `maison_plan_l_toit_deux_versants.pdf` | 991,870 | `a82cebc5ddde0192c9a94963ed9b9f9ea0612515837e8c5afccac91332de29e6` |
| `maison_toit_complexe_pignon.pdf` | 1,097,407 | `6a5b3673176da602fecf3ac74ed0a747db19d927921b57ec6712b9b277d63ce5` |
| `maison_toit_mansarde_mur_pignon_facade.pdf` | 1,161,852 | `d5b575ec460f4d8582b75ef4fb1dafc86f54ef7ca450736654cb9bffc2387c45` |

`photos/` holds the fourteen banner JPEGs served with the fiches, one per type, at the same base URL.

## Licence — why none of these images is republished

The City's conditions of use (<https://www.gatineau.ca/portail/default.aspx?p=conditions_utilisation>,
checked 2026-08-16) state, under *Droits d'auteur*:

> Vous devez tenir pour acquis que tout élément que vous visualisez ou lisez dans le présent site Web
> est, sauf mention contraire, protégé par droits d'auteur et ne peut être utilisé sans l'autorisation
> écrite de la Ville de Gatineau, sauf par vous à des fins non commerciales, pourvu que vous n'en
> modifiiez pas le contenu et que vous ne retiriez de celui-ci aucun avis relatif aux droits d'auteur
> ou autres droits de propriété intellectuelle. **Il vous est interdit de copier ou de publier, pour
> rediffusion à des tiers ou à des fins commerciales, la moindre partie du contenu.**

Republication to third parties is therefore prohibited, and the fiche photographs are additionally
credited to third parties of their own — Association du patrimoine d'Aylmer, Passerelles, Enclume,
Google Street View, and named individual photographers. Nothing in `sources/gatineau/` is copied into
`assets/`, and no fiche photograph appears on the site. The credit line printed on each fiche is
carried into the type record's photo placeholder so a reader can find the original.

The **text** of the fiches is quoted, in the same way every other place's typology document is quoted
on this site: the profile rows carry the source's own wording in `profile_fr`, the conservation lists
carry its "interventions à privilégier / à éviter" sentences, and both are attributed on the page. The
fiches themselves are the document this place is built from and are cited as such.

## Photographs that *are* published

Four freely-licensed images from Wikimedia Commons stand in for the fiche photographs:

| file | source | licence |
|---|---|---|
| `assets/places/gatineau/maison-allumette-commons.jpg` | Commons, `File:Maison allumette.jpg` | CC BY-SA 4.0 — © JeanPaulGRingault |
| `assets/places/gatineau/124-rue-poplar-commons.jpg` | Commons, `File:124, rue Poplar, Gatineau.jpg` | CC BY-SA 4.0 — © Cantons-de-l'Est |
| `assets/places/gatineau/quartier-du-moulin-rue-poplar-commons.jpg` | Commons, `File:Site patrimonial du Quartier-du-Moulin - 2.jpg` | CC BY-SA 4.0 — © Cantons-de-l'Est |
| `assets/places/gatineau/243-245-rue-champlain-commons.jpg` | Commons, `File:243-245, rue Champlain.jpg` | CC BY-SA 4.0 — © Jeangagnon |

Two were checked against the fiche descriptions before being attached: `Maison allumette.jpg` shows a
narrow two-storey gable-front house clad in boards with the gable end to the street, which is the
*maison allumette en bois de deux étages*; `124, rue Poplar` shows the shingle-clad, steep-gabled house
with small-paned shuttered windows over a low ground floor that the RPCQ's Quartier-du-Moulin entry
describes, which is the *maison de cadre de la CIP*. `485, chemin d'Aylmer.jpg` (CC BY-SA 4.0,
Cantons-de-l'Est) matches the RPCQ description of the L-plan house cited in the brief but is derelict
and carries legible graffiti, and is not used.

## Not encoded

*Inventaire du patrimoine bâti moderne* (EVOQ Stratégies, 10 November 2023, 164 buildings 1937–1980).
It classifies by *familles typologiques* — function of origin × morphology — and grades on five levels
(4 supérieure, 65 forte, 93 moyenne). Those families do not map onto the fourteen fiche types without
inventing correspondences, so the inventory is cited in `sources.yaml` and named on the place page's
notes, and nothing from it is encoded.
