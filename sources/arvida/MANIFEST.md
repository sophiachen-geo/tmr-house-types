# Source manifest — Arvida (Saguenay)

Fetched 2026-08-16 per the Part 4 brief §1; all five documents download
cleanly with `curl`. `txt/` holds `pdftotext -layout` extractions, and `txt/bbox.xhtml` the
`pdftotext -bbox-layout` word coordinates used to parse the address list.

| file | bytes | url | sha-256 |
|---|---|---|---|
| `PresentationSPArvida.pdf` | 2,467,995 | https://cpcq.gouv.qc.ca/app/uploads/2020/06/PresentationSPArvida.pdf | `e2cb58b558c4164641a95344720814034c09bfa0010792a42872327932817ac0` |
| `Rap_consultation_Arvida_2018.pdf` | 1,262,318 | https://cpcq.gouv.qc.ca/app/uploads/2020/06/Rap_consultation_15_01_18VF.pdf | `ed1c69adc8c433c650108849897d10860c9ac1c82a58b650bc53c444134cb956` |
| `la_ville_construite_en_135_jours.pdf` | 21,361,943 | https://arvida.saguenay.ca/files/documents/la_ville_construite_en_135_jours.pdf | `f2de8d18cdb4923644050dbc42a30577897d0e2a97f261d1eed5416b5cc8b34c` |
| `modeles_des_maisons_arvidiennes.pdf` | 238,869 | https://arvida.saguenay.ca/files/documents/modeles_des_maisons_arvidiennes.pdf | `0a892e8c331aa891091b8e44e376fe246807a26e0eb26efd509c115e2b8f2b32` |
| `saguenay_reglement_PIIA.pdf` | 2,173,994 | https://infopermis.saguenay.ca/medias/reglements/reglements_urbanisme/reglement_sur_les_PIIA.pdf | `1897e503a775c1aa6e0243adf62cd4021247ac841df549b92264418e5dff56dc` |

## Address list → CSV

`modeles_des_maisons_arvidiennes.pdf` is a two-column table (page 612×1008 pt, columns split at
x=306; the civic number sits at the column's left edge and the model code about 140 pt to its
right). A street block that fills the left column continues at the top of the right column, so
street context has to carry across the column break — treating each column as an independent
list strands 121 addresses with no street. Parsed from word coordinates rather than `-layout`
text, which interleaves the two columns onto single lines.

Result: **595 addresses** (492 carrying a model code, 103 blank in the source), **30 streets**,
**88 distinct model codes** — the same count as the 88 models in Morisset's album, although the
album's perimeter (the declared site) and this list's (the Sainte-Thérèse historic quarter) are
not stated anywhere to be identical. Written to `data/places/arvida/models_addresses.csv`, with
per-family totals in `data/places/arvida/model_families_summary.yaml`.

Codes printed without a model number (bare `N`, `Q`, `T`, `Y`, `Z`) and the single `M97` entry
(2912 rue Parks) are transcribed as the document gives them.

## Photographs — reuse terms

The photographs on **arvida.saguenay.ca are not reusable**. The site's legal notice
(`arvida.saguenay.ca/fr/avis-juridiques`) reserves all rights: the intellectual-property rights
belong to the Ville de Saguenay, and use by a third party "doit … faire l'objet d'autorisations,
licences, permissions ou concessions … de la part du titulaire des droits", with prior
authorisation required to reproduce, store or download material. Several of the images are also
credited to third parties (Rio Tinto, Société historique du Saguenay, Commission scolaire De La
Jonquière). Per the Part 4 brief §1.2, none of them are reproduced in this repository; the two
type records that would have carried them keep `kind: placeholder` with a credit line saying why.

The one image published here comes from Wikimedia Commons under a free licence:

| file | source | licence |
|---|---|---|
| `assets/places/arvida/arvida-company-houses-commons.jpg` | Commons, `File:Arvida (5786308087).jpg` | CC BY-SA 2.0 — © Sandra Cohen-Rose and Colin Rose |

It shows company houses on an Arvida street and is used as a place-level illustration
(`place.yaml: hero_photo`), explicitly not attributed to any model family. The Commons category
also holds a public-domain BAnQ postcard ("Davis Street, Arvida"), but it shows the commercial
street rather than housing, and the CC BY-SA view of the Saguenay Inn (1939) is a hotel.
