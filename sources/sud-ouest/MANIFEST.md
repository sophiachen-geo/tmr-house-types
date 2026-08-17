# Sources — Le Sud-Ouest (Montréal), arrondissement code 22

Acquired 17 August 2026 for Part 10a. Everything in `pdf/` was fetched with `curl -sSL`,
hashed, and extracted with `pdftotext -layout` into `txt/`. Nothing in `data/places/sud-ouest/`
was transcribed by hand from a PDF: the type records come out of `parse.py` and are written by
`encode_types.py`.

## Files

| File | Bytes | Pages | SHA-256 |
|---|---:|---:|---|
| `pdf/sud-ouest_typomorphologie.pdf` | 9 842 817 | 150 | `12c8b0b6631a14b07ba73bb8e5dfea2cad6a3e1b28a171f4ced828a1e5f02b96` |
| `pdf/12_evaluation_patrimoine_sud.pdf` | 11 087 534 | 100 | `e9c7902b9d1f29169abc9a86c7c2350bd74d5285dcc637daeaf6af1ec2f7c9a2` |
| `pdf/sud-ouest_piia_fascicules.pdf` | 84 907 | 16 | `cfea8ea019c9bb2b150beff86a1760f8988da193931013879e8883677bc3fca8` |

Retrieval URLs:

- Patri-Arch, *Étude typomorphologique de l'arrondissement du Sud-Ouest — rapport de synthèse*,
  2005, mise à jour octobre 2013 —
  <https://ocpm.qc.ca/sites/default/files/pdf/P81/3.5_etude_typomorphologique_sud-ouest.pdf>
  (OCPM dossier P81). HTTP 200.
- Ville de Montréal, *Évaluation du patrimoine urbain — arrondissement du Sud-Ouest*, 2005 —
  <http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/12_evaluation_patrimoine_sud.pdf>.
  HTTP 200.
- Arrondissement du Sud-Ouest, *Règlement RCA08 22014* modifying the PIIA by-law *RCA07 22019*,
  adopted 21 May 2008, with the fascicules d'intervention in its annexes —
  <https://ocpm.qc.ca/sites/default/files/pdf/P34/7c1.pdf> (OCPM dossier P34). HTTP 200.

The Ville URL for the *synthèse du développement* that the brief warned about was not needed:
the synthèse is § of the Patri-Arch report itself (printed pp. 25–38) and was read there.

## The arrondissement code — read from inside the document

The brief's warning is correct and this pass confirms it independently.

    $ grep -ho '\b[0-9]\{1,2\}\.\(E\|I\|N\|U\|AP\)\.[0-9]\{1,2\}\b' \
        txt/12_evaluation_patrimoine_sud.txt | cut -d. -f1 | sort | uniq -c
        540 22

**Sud-Ouest is arrondissement 22**, in the file named `12_evaluation_patrimoine_sud.pdf`. All 540
sector-code occurrences in the cahier carry the prefix 22; none carries 12. `parse.py` re-derives
this on every run and prints it, so the claim is reproducible rather than remembered.

Sector tallies read from the same extraction — five code letters, not four:

| Letter | Meaning | Count | Range |
|---|---|---:|---|
| `E` | secteur de valeur patrimoniale exceptionnelle | 15 | 22.E.1 – 22.E.15 |
| `I` | secteur de valeur patrimoniale intéressante | 25 | 22.I.1 – 22.I.25 |
| `N` | secteur industriel d'intérêt | 2 | 22.N.1 – 22.N.2 |
| `U` | secteur urbain d'intérêt | 1 | 22.U.1 |
| `AP` | secteur d'intérêt archéologique à fort potentiel | 14 | 22.AP.1 – 22.AP.14 |

Encoded in `sectors.yaml`: all 15 E sectors, the 5 aires de paysage, and 22.AP.5 as the
archaeological overlay. The I, N and U sectors are counted but not encoded (Part 10b).

## `parse.py` — what it does and what it found

    $ python3 sources/sud-ouest/parse.py
    types parsed: 19 -> ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5',
                         '2.6', '2.7', '3.1', '3.2', '3.3', '4', '5', '6', '7']
    socle/corps/couronnement triad complete in 12/15 residential fiches; partial in
      ['1.1', '1.3', '1.4'] (the source itself does not divide those façades)
    unités de paysage: 65 rows (59 named in the synthèse, 6 number-only)
    figure captions: 68
    arrondissement code, read from inside the cahier: {'22': 540}

Outputs land in `parsed/`: `types.json` (the structured fiches), `unites.csv` (the 65 landscape
units, copied to `data/places/sud-ouest/inventory.csv`), `figures.csv` (68 figure captions with
their `SOnnnn` photo ids, which are where the anchor addresses come from) and `profile_fr.yaml`
(the ready-to-paste French blocks).

The fiche template, printed p. 17, maps one-to-one onto this site's five profile columns:

| Patri-Arch | this site |
|---|---|
| A Identification | `profile_fr.description` |
| B Contexte de développement et lieux d'occurrence | `profile_fr.contexte` + the unit table |
| C.1 Implantation | `siting_landscape` |
| C.2 Volumétrie | `massing` |
| C.3 Matériaux de revêtement | `materials` |
| C.4 Traitement de la façade | `articulation` |
| C.5 Ouvertures | `openings` |
| D Variantes | `variants[]` and `profile_fr.sous_variantes` |

### The socle / corps / couronnement triad

Patri-Arch defines the three horizontal divisions of the façade on printed p. 17 and then writes
every C.4 in that order. Nothing else on this site does it.

> Le socle : Le socle est la partie basse de la façade. Il se limite généralement à la fondation du
> bâtiment mais peut également inclure le rez-de-chaussée en tout ou en partie.
> Le corps : Le corps est la partie centrale de la façade.
> Le couronnement : Le couronnement est la partie haute de la façade. Son traitement peut être plus
> ou moins exprimé architecturalement. Lorsque la toiture est visible, elle est incluse dans le
> couronnement.

`parse.py` labels each C.4 paragraph by the explicit division phrase it opens with, or failing that
by whichever division's vocabulary it uses most; it then forces the sequence non-decreasing, since
the study always writes the façade bottom-up. Where a fiche puts all three divisions in one
paragraph (type 1.5 does), the paragraph is pre-split at its division openers. The result is stored
machine-readable under `traitement_triad` in `parsed/types.json`.

**Result: the triad is complete — all three divisions present — in 12 of the 15 residential
fiches.** The three that are not (1.1 maison villageoise, 1.3 maison « boomtown », 1.4 maison de
vétérans) are not parse failures: the study writes their C.4 as plain composition prose and never
names a socle. That was checked against the source text by hand for all three.

**Schema constraint, recorded because it is a compromise.** `build.py` takes `profile_fr` values as
flat lists of strings under a fixed set of keys (`FR_KEYS` / `FR_STANDALONE`), so the triad cannot
be nested sub-keys without editing `build.py`, which this pass was not allowed to do. It is carried
instead as a label on each entry — `Socle — …`, `Corps — …`, `Couronnement — …` — with the source's
own sentence unaltered after the dash. If `socle` / `corps` / `couronnement` are ever added to
`FR_KEYS["articulation"]`, `encode_types.py` needs a three-line change and `types.json` already
holds the data in that shape.

### The 65 unités de paysage

The synthesis report names a landscape unit only where it appears in some type's *lieux
d'occurrence* list, so its pages yield 59 named units. The full set is still recoverable: the
numbering is dense inside each aire, and the highest number reached in each — 1.5, 2.14, 3.20,
4.17, 5.9 — sums to exactly 65, which is the figure the PIIA by-law's Encadré 1 states
independently (« L'arrondissement compte 5 aires de paysage divisées en 65 unités de paysage
distinctes »). Two documents, two methods, same answer. `inventory.csv` therefore carries all 65
rows, with 2.13, 3.18, 5.4, 5.5, 5.6 and 5.8 present as numbers with a blank name and
`named_in_synthese: non`.

Eight units carry a second spelling in `name_variants_fr`, because the study's own cross-reference
lists disagree with each other. Seven are typographic; unit **3.2** is substantive, appearing as
both « Avenue de l'Église Ouest » (fiches 2.2, 2.5) and « Rue De Roberval » (fiche 2.6). Not
resolved — the per-unit fiches would settle it and were not retrieved.

The aire names come from the study's own methodology page (printed p. 11). Their assignment to the
numbers 1–5 is read off the unit names themselves (all 2.x are in Pointe-Saint-Charles, all 3.x in
Côte-Saint-Paul, and so on) and is confirmed in words for aire 3, which the study twice calls
« l'aire de paysage Côte-Saint-Paul » (printed pp. 50, 70).

## Photographs — every licence read through the Commons API before download

Method: `action=query&prop=imageinfo&iiprop=url|size|extmetadata` on
`commons.wikimedia.org/w/api.php`, one call per candidate, read before any file was fetched; each
downloaded file was then opened and looked at before it was published. No image is published whose
terms were not read first.

**Published — six files, all CC BY-SA, all by Jeangagnon, attribution required:**

| Local file | Commons file | Licence | Date | Used on |
|---|---|---|---|---|
| `escalier-exterieur-711-719-rue-du-couvent-commons.jpg` | `File:711-719 rue du Couvent.jpg` | CC BY-SA 3.0 | 2016-06-04 | place hero |
| `maison-villageoise-741-rue-du-couvent-commons.jpg` | `File:741 rue du Couvent.jpg` | CC BY-SA 3.0 | 2016-05-07 | 1.1 maison villageoise |
| `maison-de-veterans-7056-rue-beaulieu-commons.jpg` | `File:7056 rue Beaulieu.jpg` | CC BY-SA 4.0 | 2020-04-11 | 1.4 maison de vétérans |
| `maisons-de-veterans-boulevard-monk-commons.jpg` | `File:Boulevard Monk - 003.jpg` | CC BY-SA 4.0 | 2018-05-19 | 1.4 maison de vétérans |
| `multiplex-805-815-rue-du-couvent-commons.jpg` | `File:805-815, rue du Couvent.jpg` | CC BY-SA 3.0 | 2015-01-24 | 2.7 multiplex |
| `multiplex-375-399-rue-de-la-montagne-commons.jpg` | `File:375-399, rue de la Montagne.jpg` | CC BY-SA 3.0 | 2015-10-06 | 2.7 multiplex |

All six are downsampled to 1100–1280 px from the uploader's originals. Author, licence and file URL
are in each photo's `credit` field on the record, as required by the licences. Every one carries
`match_confidence: visual`: they match on form and on street, not on the study's own addresses.

Two of the six come from the type-tagged category the brief named,
**`Category:Multiplexes (buildings)`**, and one of those carries the Ville de Montréal's own
description quoted on the file page — « Les bâtiments localisés au 375-399, rue de la Montagne et
au 1290 de la rue Barré ont été construits vers 1920. Cet ensemble de bâtiment est formé de
4 six-plex » — which is what fixes it as a multiplex rather than a triplex.

**Findings on the two categories the brief named:**

- `Category:Multiplexes (buildings)` — 22 files worldwide, of which three are on the island of
  Montréal and two in this borough. Both were used.
- `Category:External staircases` — **no Canadian material at all.** Its `by country` subtree runs
  Belgium, France, Greece, Japan and Portugal only; the loose files are overwhelmingly fire escapes
  on office and hospital buildings. `Category:External staircases in Canada` does not exist. The
  brief is right that `Category:Staircases` is interior and was not used, but the recommended
  alternative turns out to be empty for this purpose, so the Montréal exterior stair was found
  through street categories instead (`Category:Rue du Couvent`).

**Rejected, and why:**

- `File:Rue Galt - 2025-10-11 - 01/03.jpg`, `File:Rue Galt - 2025-10-18 - 02.jpg` (Jeangagnon,
  CC BY-SA 4.0) — the description reads « Rue Galt, **Verdun**, Montréal ». There is a rue Galt in
  Côte-Saint-Paul, which the Évaluation cahier discusses at 22.I.17, and a different rue Galt in
  Verdun. Wrong borough; not used.
- `File:Verdun (9155880752).jpg` (Matias Garabedian, CC BY-SA 2.0) — a multiplex, but at
  3857 boulevard LaSalle in Verdun. Another borough's record.
- `File:6200 rue Angers.jpg`, `File:6201 rue Angers.jpg`, `File:5611 rue Angers.jpg` — right
  borough, but night snow views and a church; nothing legible as a type.
- `File:751 rue du Couvent.jpg` / `- 01.jpg` (CC BY-SA 4.0) — the closest thing to an address match
  in the whole set, because the study's own fiche photo for the maison villageoise variante 3 is
  filed `UP4.6_Couvent_751-747`. Both are night photographs of a fragment of the porch. The daytime
  741 was published instead, from the same series of four houses.
- Every figure in the Patri-Arch study — © Patri-Arch, usage rights ceded to the Ville de Montréal
  only, republication requiring permission. Recorded as `kind: placeholder` on eleven type records
  with the figure caption and the copyright line, and not reproduced.
- No commercial real-estate site was consulted or cited for any fact on this record.

## Scripts

- `parse.py` — parses the typo-morphological study; also re-derives the arrondissement code and
  the sector tallies from the Évaluation cahier. Idempotent; writes only into `parsed/`.
- `encode_types.py` — writes the nineteen files in `data/places/sud-ouest/types/`. The French half
  of every card comes straight from `parsed/types.json`; the English half, the canonical and style
  attributions and the measured columns are hand-written in this file. Edit `encode_types.py`, not
  the YAML.

Run order:

    python3 sources/sud-ouest/parse.py
    python3 sources/sud-ouest/encode_types.py
    python3 build.py

## Open items for Part 10b

1. The 25 `22.I.n`, 2 `22.N.n` and 1 `22.U.1` sectors are counted but not encoded.
2. The other 13 AP sectors. Note that the cahier heads one text « 22.AP.5, 22.AP.6 ET 22.A.1 » and
   sends 22.AP.4 and 22.AP.6 to it — a fourth code letter series, `A`, appears there for
   archaeological *sites* as opposed to potential zones, and was not investigated.
3. The 65 per-unit fiches, which would supply limits, parcel dimensions and the immeubles d'intérêt
   patrimonial per unit, and would settle the name of unit 3.2.
4. The `TYPOLOGIE_SPECIFIQUE` field of the Ville's open data, which would give a building count for
   the thirteen types the study does not count.
5. A photograph of the triplex with exterior stair (2.6) that is confidently a *triplex* — the two
   exterior-stair buildings published here are a multiplex and an unverified count.
