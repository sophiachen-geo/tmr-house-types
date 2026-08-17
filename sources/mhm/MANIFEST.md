# Source manifest — Mercier–Hochelaga-Maisonneuve

Fetched 2026-08-17 per the Part 10a brief §1.2, §1.4 and §2.3.4. New place; nothing existed before.

| file | bytes | url | sha-256 |
|---|---|---|---|
| `14_evaluation_patrimoine_mercier.pdf` | 7,922,808 | http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/14_evaluation_patrimoine_mercier.pdf | `ebb8753074e9ecbba4fbbd14a195557fe150e86d90d0661eec9a2b9dc111dba3` |
| `guide_patrimonial_mhm.pdf` | 8,915,878 | https://portail-m4s.s3.montreal.ca/pdf/26677_guide_patrimonial_vfinal.pdf | `16d6d53e992f40e8df3519c91e2d7f9eb6d613d99ff3962c7ff0e6ef437fba41` |
| `rpcq/rpcq_232824.html` | 64,887 | https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&id=232824&type=bien | `3011718acc4c59996db50879b759f10bf2034d42e1bc0c5e38cf3142e792c627` |
| `rpcq/rpcq_92740.html` | 66,919 | …&id=92740&type=bien — Château Dufresne | `deee9e965fcab2a58b37747920a71258538388cb055835794cefffc254116911` |
| `rpcq/rpcq_210645.html` | 34,896 | …&id=210645&type=bien — ancien hôtel de ville de Maisonneuve | `d25bd52d8da2e44373c556a8c14f32876256ae34e1b4266b0aab21f61ce92bbc` |
| `rpcq/rpcq_232894.html` | 46,288 | …&id=232894&type=bien — ancien marché public de Maisonneuve | `740beea0a0fe09c36da0d2e9367b3a5db7cbb3e2b2adceb6a69bec220f4ab5db` |
| `rpcq/rpcq_211389.html` | 41,942 | …&id=211389&type=bien — bain et gymnase publics (bain Morgan) | `730bae22449f9088a917a4ba03503f48088b85b8f83777c2f21e8b1f6a9a509c` |
| `rpcq/rpcq_96613.html` | 34,654 | …&id=96613&type=bien — ancienne caserne de pompiers / caserne Letourneux | `5ccb915de294be0ffe84f075ab0414e79d3105cd15825abbaed1581302f66ee5` |
| `rpcq/rpcq_232895.html` | 29,728 | …&id=232895&type=bien — avenue Morgan | `5771e87fbd69ae640d3bd15a0f4944ae94df6fb34536bb80dc15b81442899a89` |

`txt/` holds a `pdftotext -layout` extraction of each PDF and a tag-stripped text rendering of each RPCQ
page. The RPCQ site serves no plain-text or JSON view; the HTML is kept alongside so the stripping can be
re-checked.

## The arrondissement code — read from inside, as required

**The code is 27.** The Ville publishes this cahier as `14_evaluation_patrimoine_mercier.pdf`, and the
filename is worth nothing: every sector code printed inside the document begins with 27.

```
27.E.1–5   secteurs de valeur patrimoniale exceptionnelle
27.I.1–6   secteurs de valeur patrimoniale intéressante
27.U.1–5   ensembles urbains d'intérêt
27.N.1–2   ensembles industriels d'intérêt
27.AP.1–3  secteurs d'intérêt archéologique à fort potentiel
27.A.1–2   secteurs d'intérêt archéologique
```

Two things worth logging for the code map in `data/canon/`:

1. **A stray `14.AP.1` appears in the extraction, three times, and it is not an MHM sector.** It sits on
   the archaeological synthesis map (source p. 47), in the map margin next to `27.AP.1`, and it is a
   neighbouring borough's label bleeding across the sheet edge — arrondissement 14 is
   Villeray–Saint-Michel–Parc-Extension. A regex sweep of the extracted text for
   `\b[0-9]{1,2}\.(E|I|N|U|AP)\.[0-9]{1,2}\b` will pick it up; it must not be treated as evidence that
   this cahier is arrondissement 14.
2. **This cahier uses a sixth code letter the brief's grammar does not list: `A`.** Alongside
   `27.AP.n` for *secteurs d'intérêt archéologique à fort potentiel*, it carries `27.A.1` (« Fort et
   ancien village ») and `27.A.2` (« Zone côtière et chemin du Roy ») for plain *secteurs d'intérêt
   archéologique*, the lower of the two archaeological grades, and the map legend distinguishes them
   explicitly. The A sectors cross-refer to the AP texts (« Voir texte 27.AP.2 ») rather than carrying
   their own. If `AP` is being added to the schema enum, `A` should be added with it.

## What is in the cahier, and what is not

Front matter confirms the series data quoted in the brief §1.2, verbatim for this volume: produced by the
Division du patrimoine et de la toponymie under **Jean-François Gravel**, direction **Céline Topp**, work
carried out **janvier 2003 à mai 2004** for the Plan d'urbanisme adopted **23 novembre 2004**; team Julie
Boivin, Elizabeth Bonner, Anne-Marie Dufour, Guy Lafontaine, Christiane Lefebvre, Pierre-Paul Savignac
(architects) and Denise Caron (historian); archaeology by Claire Mousseau with Françoise Duguay, François
Bélanger, Anne-Marie Balac and Christian Roy; **27 cahiers**, one per arrondissement; ISBN 2-7647-0470-4,
dépôt légal 2005.

The document is **not a typology**. It characterises sectors, lists individually valued buildings by
address, and makes recommendations. Its entire description of Maisonneuve's housing is one clause —
« les habitations ouvrières de trois étages le long de rues bordées d'arbres » — glossed in § 3.1 as
« un patrimoine résidentiel composé de "plex" en pierre ou en brique le long de rues bordées d'arbres ».
Two-column extraction is clean for the E-sector fiches; only figure captions set inside the running text
had to be removed, and they are listed in the header of `sectors.yaml`.

## The « maison-modèle » question — answered: there is none

The brief flagged this and it checks out. Searching the full extraction for `modèle` returns exactly two
substantive uses, and neither is a model house of the cité:

- **27.E.2** — « Ce secteur regroupe les plus éloquents témoignages bâtis de **la cité-modèle de
  Maisonneuve** ». A model **city**, said of the municipality. This is almost certainly the phrase the
  memo garbled.
- **27.U.1** — « Ces ensembles ont été construits autour de 1950 sur **le modèle des maisons de la
  Wartime Housing Limited** ». A federal house type of the 1940s, adopted by private developers in Mercier
  around 1950 — thirty years after Maisonneuve ceased to exist, and at the other end of the borough.

Nothing in the RPCQ fiche for the classed site describes a house type either; its éléments
caractéristiques cover the four civic buildings, the avenue, the park and the two bronzes, and no
dwelling. No type record for a Maisonneuve model house has been created. The workers' housing is encoded
as three-storey plex and rangée, in `types/plex-ouvrier-trois-etages.yaml`, whose `profile_note` says all
of the above.

## Two corrections to the research memo

1. **Château Dufresne, reinforced concrete.** The memo says "first reinforced-concrete private residence
   in Montréal". RPCQ 92740 does not say that. It says « il s'agit de **l'une des premières** utilisations
   de ce matériau pour la construction résidentielle à Montréal, voire au Québec » and « **l'une des
   premières** résidences à structure en béton armé à Montréal ». One of the first. The superlative is not
   published on the site, and the correction is stated on the type card and in the place notes.
2. **Caserne Letourneux and Unity Temple.** The memo has the caserne "modelled on Frank Lloyd Wright's
   Unity Temple". RPCQ 96613 carries only: dates **1914–1915**, architect **Marius Dufresne**, other names
   *ancienne caserne Letourneux* and *ancienne caserne no 1 de pompiers*. The site fiche 232824 describes
   its architecture as « un vocabulaire plus moderne, caractérisé par un jeu de volumes, des toitures
   débordantes et une ornementation sobre » — a description consistent with the Wright attribution but not
   an assertion of it. No institutional source for the attribution was found, so it is not published.
   Part 10b: look for it in Linteau (1981) or in the MCC's classement dossier.

Two dates in the memo were confirmed as end-dates of RPCQ construction ranges rather than errors:
hôtel de ville 1912 (range 1910–1912), marché 1914 (range 1912–1914), bain et gymnase 1914–1916,
caserne 1915 (range 1914–1915). The encoded records use the RPCQ ranges.

## The by-laws

- **01-275** — Règlement d'urbanisme de l'arrondissement de Mercier/Hochelaga-Maisonneuve. Confirmed as
  the borough zoning by-law and, per the Guide patrimonial, the carrier of the *secteurs significatifs*
  and *immeubles significatifs* designations.
- **01-275-112** — **the memo's characterisation needs qualifying.** This amendment is not a general
  heritage-PIIA addition. It inserted a new Section VI after article 120.12 creating the PIIA for the
  *secteur Cité de la logistique* (Assomption-Sud–Longue-Pointe), an industrial-logistics control; public
  consultation was held 23 March 2017. The legacy Ville URL for the by-law PDF
  (`…/REGLEMENT_%2001-275-112_PIIA.PDF`) now 404s, so the content is attested through the search index and
  the borough's own consultation documents, and **the "in force 26 May 2017" date could not be verified
  from a municipal source and is therefore not encoded.** Part 10b: get the consolidated 01-275 and its
  amendment table.
- **RCA02-27006** — Règlement régissant la démolition d'immeubles. Confirmed on montreal.ca, with the
  wording « prévoit l'interdiction de démolir un immeuble sans avoir préalablement obtenu une
  autorisation », and the note that the CCU members sit as the demolition committee. The memo writes it
  "RCA02 27006"; the municipal form is hyphenated.
- Also named by the Guide patrimonial and encoded in the place notes: lotissement **RCA04-27003**,
  construction and transformation **11-018**, salubrité **03-096**, occupation et entretien **23-016**.
- The Guide lists **twelve** PIIA sectors by name; they are transcribed into `place.yaml`.

## Photographs — licences, and what was rejected

Every candidate's licence was read from the Wikimedia Commons API (`prop=imageinfo`,
`iiprop=url|extmetadata`) **before** any download, and each accepted image carries author, licence and
file URL in its `credit` field plus a `match_confidence` and a `match_note`.

Accepted, five files in `assets/places/mercier-hochelaga-maisonneuve/`:

| file | source | author | licence | confidence |
|---|---|---|---|---|
| `boulevard-morgan-1916.jpg` | `File:Boulevard Morgan Maisonneuve Montreal 1916.jpg` | Wm. Notman & Son (McCord Stewart Museum VIEW-16185) | public domain | place hero |
| `plex-rue-dezery.jpg` | `File:HochMais.JPG` | Atilin | CC BY-SA 3.0 | visual |
| `plex-rue-adam.jpg` | `File:Maisons du quartier Hochelaga.jpg` | Félix Mathieu-Bégin (User:Webfil) | CC BY-SA 4.0 | visual |
| `chateau-dufresne-facade-nord.jpg` | `File:Façade avant - Château Dufresne.JPG` | Thomas1313 | CC BY-SA 3.0 | address |
| `longue-pointe-rue-lepailleur.jpg` | `File:Mercier, rue Lepailleur.jpg` | Félix Mathieu-Bégin (User:Webfil) | CC BY-SA 4.0 | visual |
| `commerce-logement-4239-ontario-est.jpg` | `File:4239, Ontario Street East, Montreal.jpg` | Thomas1313 | CC BY-SA 4.0 | visual |

**The two categories the brief names were checked and produced nothing for this borough.**
`Category:Multiplexes (buildings)` holds 23 files, four of them Montréal (rue de la Montagne, rue du
Couvent, Saint-Léonard, Verdun) and none in MHM; the rest are American. `Category:External staircases`
holds well over a hundred files and is, in practice, a fire-escape category — Helsinki, Rotterdam, Madrid,
São Paulo, Bonn — with no Montréal content at all. Every image used here was found instead through
`Category:Mercier–Hochelaga-Maisonneuve` and `Category:Hochelaga-Maisonneuve`, which are untagged by
building type, which is why `match_confidence: visual` dominates exactly as the brief predicted.

**Rejected after downloading and looking at the image.** Three candidates had descriptions that did not
survive inspection, and this is the reason the workflow is "download, then look, then decide":

- `File:Montréal, Maison Typique du quartier Langue -.Pointe 01.jpg` (CC0, so licence was not the
  problem) — titled a *typical house* of Longue-Pointe, it is in fact a parking court between three-storey
  1950s–60s brick walk-up apartment blocks. No house in the frame.
- `File:Mercier, rue Curatteau.jpg` (CC BY-SA 4.0) — rue Curatteau is sector 27.U.4's street and the fiche
  describes « des maisons en brique à toit à deux versants qui s'apparentent au modèle développé par la
  Wartime Housing Limited », built 1953. The photograph shows yellow-brick plexes at the north end of the
  street near the tunnel ventilation tower. Wrong stretch, wrong type. The veterans' house record keeps a
  placeholder rather than take it.
- `File:Mercier-est neighbourhood.JPG` (CC BY 3.0) — a 2008 phone snapshot taken through a chain-link
  fence; no bungalow is legible. The bungalow record keeps a placeholder.

No commercial real-estate blog was consulted for anything, per brief §1.4.

**One access note for whoever fetches next.** `upload.wikimedia.org` returned HTTP 429 with the message
"Too many requests … instead use thumbnail images in sizes listed on https://w.wiki/GHai" for
original-size fetches from this environment's shared egress. Requesting a standard thumbnail width through
`Special:FilePath/<name>?width=N` succeeded at 500, 1280, 1600 and 1200 while failing at 640, 743 and 800.
The hero image is therefore served at 500 px wide; the Commons original is only 743 × 601, so little is lost.

## Sources found beyond the brief

- **The borough's own `Guide patrimonial`**, which the brief did not name and which turns out to be the
  only fabric-scale document MHM has. It is a conservation manual, not a typology, but its prescriptive
  tables for *secteur significatif*, *immeuble significatif*, *PIIA Village Champlain* and *Maison des
  vétérans* carry real material and dimensional content — brick formats, lintel and sill treatment, sash
  ratios (1/2–1/2, 2/5–3/5, 1/3–2/3), glazed-panel heights in both inches and centimetres, 36-inch guards,
  6-inch balcony boards, the prohibition of natural galvanised steel, and the rule that governs everything
  else: « lorsqu'une construction similaire adjacente comporte encore ses composantes d'origine, cet
  immeuble sert de référence pour les interventions ». Most of the articulation, openings and materials
  lines on this page's type cards come from it. Its own annexes (fiches-patrimoine, pp. 27–58 of its table
  of contents, including Village Champlain types I–VII and Maison des vétérans types I–III) are published
  separately and were **not** retrieved — Part 10b.
- **MEM / Mémoires des Montréalais** (Ville de Montréal), « Les maisons ouvrières de la rue
  Saint-Germain », 8 November 2017, Atelier d'histoire Mercier-Hochelaga-Maisonneuve with André Cousineau.
  The only institutional account of the 1881 V. Hudon mill housing, and the source of the claim that it is
  « le seul exemple encore existant d'habitations érigées au XIXe siècle par une compagnie à Montréal ».
  This is the record that lets the borough hold both a corporate company row and a bourgeois-municipal
  planned city, three streets apart, and it is the hinge of the Arvida / Témiscaming comparison.

## Deferred to Part 10b

1. The I, U, N, AP and A sector fiches of arrondissement 27 — twenty-one records, enumerated in the header
   of `sectors.yaml` but not encoded.
2. The consolidated text of by-law 01-275, the boundaries of its *secteurs significatifs* and *immeubles
   significatifs*, and the amendment table (to date 01-275-112 properly).
3. The Guide patrimonial's separately published *fiches-patrimoine* annexes, which would let the Village
   Champlain and Maison des vétérans lettered variants be encoded as `variants[]`.
4. A primary source for the caserne Letourneux / Unity Temple attribution, or a decision to drop it.
5. Whether the agglomeration's art. 120 pre-1940 inventory covers MHM, and with what effect.
6. A verified free photograph of the rue Saint-Germain row, and of a 27.U.4 or 27.U.2 street.
