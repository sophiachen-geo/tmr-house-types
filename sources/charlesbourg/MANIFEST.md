# sources/charlesbourg — acquisition manifest

Acquired 17 August 2026 for Part 9a. All five documents named in the brief's §1.2 were fetched
successfully; four are PDFs and all four converted cleanly with `pdftotext -layout`.

## Files

| file | source URL | bytes | sha-256 | parse |
|---|---|---|---|---|
| `pc_charlesbourg_2016.pdf` | https://cpcq.gouv.qc.ca/app/uploads/2020/05/pc_charlesbourg.pdf | 8 781 442 | `8e9d7e953b017896df381d8174a238af3453df96dd62c7ab23f790b27cf996ba` | OK — 124 pages → `pc_charlesbourg_2016.txt`, 4 158 lines |
| `etude_caracterisation_2005.pdf` | https://cpcq.gouv.qc.ca/app/uploads/2020/05/charlesbourg.pdf | 7 694 767 | `2ed713589e1d709bc1f91c1d0ce976896fddc073083dd7750521afd514502380` | OK — 39 pages → `etude_caracterisation_2005.txt`, 1 443 lines |
| `rapport_consultation.pdf` | https://cpcq.gouv.qc.ca/app/uploads/2020/05/Rapport_de_consultation_Charlesbourg.pdf | 205 960 | `fbee36535b5bca336f0c953599371e2012cbfc6d11c969942cfd2a098a69824c` | OK — 20 pages → `rapport_consultation.txt`, 709 lines |
| `guide_rvq1324_charlesbourg.pdf` | https://reglements.ville.quebec.qc.ca/fr/ressource/rc/R.V.Q.1324_FR_008_0001.pdf | 1 771 971 | `0b36bb415176c78c778a3bf6d49e7f6c3c2f6d15aaf3075a9559720f093d3e3b` | OK — 57 pages → `guide_rvq1324_charlesbourg.txt`, 2 573 lines |
| `rpcq_93524.html` | https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&id=93524&type=bien | 74 942 | `05eb718863b34b240c95ff9f14e2482aadaac373c398c153816afa73d9ac6bb8` | OK — tag-stripped in memory, not written to disk |

**Nothing failed to download and nothing failed to parse.** `pdftotext` emitted repeated
`Syntax Warning: not an ICC profile, invalid signature` lines for embedded colour profiles in the
plan de conservation and the 2005 Étude; these affect image colour handling only and no text was
lost.

### Pagination

The plan de conservation's printed page numbers run 1–121 across 124 PDF pages, offset by exactly
one: **printed page = PDF page − 1**. Verified at four independent points (PDF 9 = `[8]`, PDF 16 =
`[15]`, PDF 42 = `[41]`, PDF 52 = `[51]`). All page references in the data records are the *printed*
numbers, which are the ones the brief cites.

## Target pages, and what was found

| brief target (printed) | PDF pages | content | result |
|---|---|---|---|
| 37–39 système parcellaire | 38–40 | réserve / commune / ceinture + "en bref" summary | found, complete |
| 41–46 cadre bâti statistics | 42–47 | date, type, cladding, roof, storeys | found, complete; the type-by-type discussion runs on to printed 47 |
| 48–51 five residential types | 49–52 | the five types, the three sub-variants, the mill and the secondary buildings | found, complete |
| 59 five unités de paysage | 60 | the five units are described on printed 57–59; printed 59 carries the "en bref" summary listing all five | found; the unit descriptions start two pages earlier than the brief's anchor |
| 68–78 orientations | 69–79 | conservation orientations | present, not parsed — Part 9b |

## Built-fabric figures: confirmed or corrected

Every figure the brief marked *verify on parse* was re-read against the plan de conservation.
**All of them are confirmed; none required correction.** Sources are printed pp. 41–47.

| figure | brief | source wording | verdict |
|---|---|---|---|
| residential share | 80 % | "L'architecture de type résidentiel représente 80 % du total des bâtiments" | confirmed |
| maisons rurales et urbaines | 82 | "se compose de 82 maisons rurales et urbaines" | confirmed |
| édifices à logements multiples | 28 | "ainsi que de 28 édifices à logements multiples" | confirmed |
| institutional / religious | 7 | "Ces sept bâtiments représentent 5 % du total" | confirmed |
| mixed residence + commerce | 14 | "On trouve 14 bâtiments de ce genre, soit environ 10 % du total" | confirmed |
| post-war commercial | 6 | "Six bâtiments de type commercial construits après la Seconde Guerre mondiale … environ 4 %" | confirmed |
| pre-industrial | 1 | "un exemple d'architecture préindustrielle, celui du moulin des Jésuites" | confirmed |
| built 1925–1975 | 65 / 48.5 % | "Plus de 65 bâtiments, soit près de 48,5 % des édifices" | confirmed |
| cladding: planches horizontales | 55 | "55 sont dotés d'un parement principal en planches horizontales … près de 40 %" | confirmed |
| cladding: brique | 35 | "35 bâtiments en brique (25 % du total)" | confirmed |
| cladding: pierre | 7 | "ils sont au nombre de sept" | confirmed |
| cladding: parement mixte | 23 | "soit 23 bâtiments" | confirmed |
| roof: deux versants | 56 | "Plus de 40 % … soit 56 bâtiments" | confirmed |
| roof: toit plat | 31 | "près de 22 % … soit 31 bâtiments" | confirmed |
| roof: mansardé | 27 | "27 bâtiments, soit environ 19 %" | confirmed |
| storeys ≤ 2 | 121 | "121 bâtiments, soit près de 88 %" | confirmed |

The figures also reconcile arithmetically against the 138 principal buildings, which is a useful
check that nothing was misread: cladding 55 + 35 + 7 + 23 + 18 = 138; storeys 121 + 17 = 138, and
within the 121, 26 + 31 + 64 = 121. Residential 82 + 28 = 110, which is 79.7 % — the plan's "80 %".

**Detail added beyond the brief's list**, all from the same pages and now carried in
`built_fabric_statistics`: 18 buildings of other claddings; within the 55 horizontal-plank buildings,
33 in wood and 22 in contemporary materials; within the 23 mixed claddings, 15 of brick and
artificial stone; within the 56 two-slope roofs, 26 with *larmiers retroussés*; the storey breakdown
26 / 31 / 64 / 17; roughly 30 buildings built 1850–1900 and about four after 1975.

## Corrections made to the brief on the strength of the parse

1. **The commune is 20 arpents, not 25.** The brief's §0 says the chemin du Trait-Carré "rings a
   *commune* of 25 arpents (~8.5 ha)". The plan is explicit that 25 arpents / 8.5 ha is the whole
   **central square**, réserve included: printed p. 26, "un carré central de 8,5 hectares (composé
   d'une réserve de 1,7 hectare entourée d'un pâturage commun délimité par le chemin du
   Trait-Carré)", and printed p. 38, the commune is "d'une superficie d'environ 7 hectares (20
   arpents)". So 25 = 5 (réserve) + 20 (commune). Encoded as three distinct areas, with the
   reconciliation written out in `prose.md ## notes`.
2. **The "quelque 200 bâtiments" figure is the consultation report's, not the plan's.** The string
   "200 bâtiments" does not occur anywhere in `pc_charlesbourg_2016.txt`. It occurs once, in
   `rapport_consultation.txt` line 96, in the CPCQ's summary of the plan's valeur architecturale.
   The place record and the notes attribute it accordingly.
3. **Petite-Auvergne and Bourg-Royal have different founders.** The brief presents all three radial
   villages as of a piece. The plan de conservation, printed p. 19, is more precise: the Jesuits
   reused their model at **Petite-Auvergne in 1666** but had room only for a half-square, and in the
   same year **Jean Talon expropriated part of the seigneurie and created Bourg-Royal**. The
   consultation report's sentence — the one the brief quotes — is reproduced verbatim in the notes,
   and the plan's finer account sits beside it.
4. **The unités de paysage begin on printed p. 57, not p. 59.** Printed p. 59 carries only the
   "en bref" recapitulation. All five are transcribed from pp. 57–59.
5. **Maison Pierre-Lefebvre's date is contested as well as its identifier.** The brief flags only
   the missing RPCQ id. The two principal sources also disagree on the year: the plan de conservation
   (printed p. 42) says **1846**, the 2005 Étude says **1825**. Both facts are recorded in the notes;
   no RPCQ id is published.
6. **The maison Éphraïm-Bédard date is better attested than the brief implies.** The brief describes
   1828/1830 as a tourism-source reading. In fact the plan de conservation itself says "la maison
   Éphraïm-Bédard a plutôt été érigée vers 1830", offering it explicitly as a correction of the
   building's misleading 18th-century appearance, and the 2005 Étude gives 1830 too. The brief's
   instruction is still followed — a **range** is published, not a year — but the notes record that
   both ministerial sources converge on c. 1830.

## Binding verifications from the brief's §0, re-checked here

- **Decree of 17 November 1965** — confirmed three times in the 2005 Étude (résumé; § 1.1, which
  names *arrêté en conseil no 2271* signed by the lieutenant-governor on the recommendation of the
  Commission des monuments historiques, meeting of 27 September 1965; and the annexe, which
  reproduces the arrêté) and once in the RPCQ statut block, "Déclaration / Site patrimonial /
  Gouvernement du Québec / 1965-11-17".
- **138 vs ~200 are two measures** — confirmed. 138 principal buildings, given identically by the
  RPCQ fiche and the plan de conservation printed p. 41. ~200 all buildings, from the consultation
  report. 149 associated RPCQ records, read off the fiche's "Patrimoine immobilier associé (149)".
- **Three radial villages** — confirmed verbatim, `rapport_consultation.txt` lines 71–78.
- **The plan is the Jesuits', not Talon's** — confirmed. Marcel Trudel, « Le village en étoile, une
  innovation des jésuites et non de Talon », *RHAF* vol. 44 no 3 (hiver 1991), p. 397–406, appears in
  the bibliography of **both** the plan de conservation (printed p. 109) and the 2005 Étude, and the
  Étude cites it in a footnote to the charge that Talon "aurait non seulement « emprunté » aux
  Jésuites l'espace nécessaire … mais s'en serait attribué l'idée originale". Noted for the record:
  the RPCQ fiche lists Jean Talon as the single "personne associée" to the site, which is exactly the
  misattribution the brief warns about.
- **Transfer of powers** — confirmed on the RPCQ fiche: "Transfert de responsabilité / Exercice de
  certains pouvoirs par la municipalité (Québec), 2016-12-09 / Prise d'effet : 2017-06-09".
- **Moulin des Jésuites, 1742 vs "vers 1740"** — 1742 appears three times in the plan de
  conservation; "vers 1740" appears in the 2005 Étude *and* in the Ville de Québec R.V.Q. 1324 guide.
  Two sources to one, but the plan is later and more specific. 1742 is used, the minority reading is
  flagged in the notes.

## Photographs — licence findings

**Rule applied:** nothing from the RPCQ, the MRC, Patri-Arch or the Ville de Québec goes into
`assets/`. All such images are recorded as `photos[]` entries with `file: null`, a `source_url` and
`licence: "permission required"`. Wikimedia Commons is the only render source, and **every candidate
licence was read individually through the Commons API** (`action=query&prop=imageinfo&iiprop=extmetadata`)
before any file was downloaded. No image was published whose terms had not been read.

### Published — verified, downloaded, rendered

| asset | Commons file | author | licence | assigned to | match |
|---|---|---|---|---|---|
| `rurale-inspiration-francaise.jpg` | House in Charlesbourg, Quebec City 03.jpg | Wilfredor | **CC0** | maison rurale d'inspiration française | visual |
| `neoclassique-galerie.jpg` | Old house in Charlesbourg.jpg | Wilfredor | **CC0** | maison québécoise d'inspiration néoclassique | visual |
| `neoclassique-boiseries.jpg` | Old house in Charlesbourg 005.jpg | Wilfredor | **CC0** | maison québécoise d'inspiration néoclassique | visual |
| `maison-mansardee.jpg` | House in Charlesbourg, Quebec City 01.jpg | Wilfredor | **CC0** | maison mansardée | visual |

All four are `match_confidence: visual` — matched on the plan's own diagnostic features, never on
address. The one legible civic number, 7960 on the mansard house, is recorded in the match note but
not used to assert a street.

### Verified and retrieved, but deliberately not published

| Commons file | author | licence | why not used |
|---|---|---|---|
| Old house in Charlesbourg 006.jpg | Wilfredor | CC0 | a shopfront, not a house type |
| House in Charlesbourg, Quebec City 02.jpg | Wilfredor | CC0 | a *bâtiment secondaire* — rectangular, one storey, straight two-slope roof, vertical planks, exactly as the plan describes them on printed p. 52. This site does not card non-residential buildings, and the schema attaches photographs only to type records, so it stays unpublished. A good candidate if a `secondary_buildings` block is ever added |
| House in Charlesbourg, Quebec City 04.jpg | Wilfredor | CC0 | a wide two-storey clapboard building under a hipped roof with three dormers; probably one of the 28 *édifices à logements multiples*, but the plan cards no such type and the identification is not certain enough to attach elsewhere |
| Arrondissement historique de Charlesbourg (4).JPG | Sylvainbrousseau | CC BY-SA 3.0 | despite the title, it shows a public sculpture ("PREMIÈRES FÊTES FORAINES 1975") in a park with a brick building behind. Not a house. The brief named this file as a candidate; it does not depict what the name suggests |

### Verified but not retrieved

| Commons file | author | licence | note |
|---|---|---|---|
| 1re avenue Charlesbourg.jpg | Judicieux | CC BY-SA 4.0 | a street view; licence read and clear, but Wikimedia rate-limited this session's egress before it could be fetched and its subject confirmed |
| Presbytère Saint-Charles-Borromée.jpg | Wilfredor | CC0 | the presbytery — institutional, Second Empire. Licence clear; recorded as a placeholder on the mansard record because it is not a *house* |
| Moulin des Jésuites-Québec-1.JPG | Gilbert Bochenek | CC BY-SA 3.0 | licence read and clear. The mill is not carded as a type, so nowhere to render it; a candidate if a place-level hero photo is ever wanted |

### Recorded as permission-required, never downloaded

All of the plan de conservation's own figures — fig. 28 (maison Éphraïm-Bédard), fig. 29 (8220 Le
Trait-Carré Ouest), fig. 30 (8290 Le Trait-Carré Est), fig. 31 (the three-photograph sub-variant
strip) and fig. 32 (8191 Le Trait-Carré Ouest) — are © Gouvernement du Québec, ministère de la
Culture et des Communications. Each is recorded on the matching type record as a `placeholder` photo
with `file: null` and `licence: "permission required"`, so the reader can see exactly which
illustration the source prints for each type without the image being reproduced here.

### Commons rate limiting

Wikimedia returned HTTP 429 repeatedly during this session ("Your request does not comply with our
robot policy"). Metadata queries through `api.php` succeeded with retries and generous spacing;
file downloads needed roughly 70 seconds between requests. Anyone re-running this acquisition should
pace it accordingly rather than assume a file is missing.

## Not done here — for Part 9b

- Printed pp. 68–79, the conservation orientations, are present in the parsed text but not encoded.
  They are the source of `conservation` on each type record and per sector, and every type record
  currently carries `conservation: []`.
- The RPCQ fiche for the église de Saint-Charles-Borromée (id 92700) was not retrieved. The classement
  year 1959 and the construction dates 1828–1830 used in this record come from the plan de
  conservation and the 2005 Étude instead, and `sources.yaml` says so.
- The Ville de Québec *Répertoire du patrimoine bâti* fiches for the Trait-Carré addresses were not
  obtained; the type records carry the plan's printed example addresses only.
