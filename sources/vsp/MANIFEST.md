# sources/vsp — acquisition manifest

Acquired 17 August 2026 for Part 10a, Villeray–Saint-Michel–Parc-Extension. Three documents were
retrieved and parsed; three more were sought and could not be reached. The failures are listed as
carefully as the successes, because two data records depend on knowing which is which.

## Files retrieved

| file | source URL | bytes | pages | sha-256 | parse |
|---|---|---|---|---|---|
| `pdf/vsp_01-283-124_fiches_typologies.pdf` | https://portail-m4s.s3.montreal.ca/pdf/Règlement%2001-283-124%20-%20Fiches%20typologies.pdf | 6 869 574 | 109 | `9ff4ea1e7b741c24436e0ff14f23018a821f91e42eb004326015e72225c1b676` | partial — see "The extraction problem" below → `txt/vsp_01-283-124_fiches_typologies.txt`, 3 238 lines |
| `pdf/26_evaluation_patrimoine_villeray.pdf` | https://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/26_evaluation_patrimoine_villeray.pdf | 3 961 471 | 46 | `e6e6ff5748506e6b14ad704068d232be3c8ee7f628b82ffab0d45c1ccbc2ca08` | OK → `txt/26_evaluation_patrimoine_villeray.txt`, 2 154 lines |
| `pdf/vsp_depliant_maisons_shoebox.pdf` | https://portail-m4s.s3.montreal.ca/pdf/depliant_maisons_shoebox_final_web.pdf | 590 541 | 2 | `2669e0a4b3ec22985871c5e2c4fdf78af0e4d9ebe8263cacc8f8da5707f8b4e7` | OK → `txt/vsp_depliant_maisons_shoebox.txt`, 100 lines |

## The arrondissement code — verified from inside the document

**VSP is arrondissement 14.** The Part 10 memo said so and the memo is right, but it was checked
rather than trusted, because §0 of the brief warns that the file-number and code-number sequences
collide. Method: extract every string matching `[0-9]{1,2}\.(E|I|N|U|AP)\.[0-9]{1,2}` from the
parsed cahier and tally it.

```
14.U.1  ×34    14.I.3  ×17    14.AP.1 ×13    14.E.1  ×9
14.I.4  ×8     14.I.2  ×8     14.U.3  ×7     14.U.2  ×7
14.I.5  ×7     14.I.1  ×7
```

**121 occurrences, every one of them prefixed 14, in a file published as
`26_evaluation_patrimoine_villeray.pdf`.** No other arrondissement number occurs anywhere in the
document. The filename is not evidence and was not used.

The document also prints a code letter the Part 10 schema does not carry: **`14.A.1`**, with a bare
A, under the heading « B. Les secteurs d'intérêt archéologique » — one rank below the
« secteur d'intérêt archéologique à fort potentiel » that carries `AP`. Six occurrences. The cahier
distinguishes them substantively: for AP it says protective measures are necessary, for plain A it
says further study is needed before the probability of remains can be estimated. Both are encoded as
`archaeological-potential` because that is the only archaeological value in the schema, and the
distinction is written into each sector's `note`. Adding a second value would be a change to shared
canon and was not made from a place record.

## The by-law's structure — and the truncation the brief flagged

The Part 10 brief lists fiches 1.1–1.7 and 2.1–2.2 and warns that the plex extraction may have been
truncated after 2.2. **It was, and by more than one fiche.** The page footers `P. x.y.z` were read
from all 109 pages, giving the complete structure:

| family | fiches | PDF pages |
|---|---|---|
| 1.0 Maisons unifamiliales | 1.1 – 1.7 | 2 – 57 |
| 2.0 Plex | 2.1, 2.2, **2.3** | 58 – 82 |
| **3.0 Immeubles d'appartements** | **3.1, 3.2, 3.3** | 84 – 108 |

So: **thirteen fiches, not nine.** Two findings the brief did not have —

1. **Fiche 2.3, « Plex de la seconde moitié du 20e siècle », exists** (PDF pp. 75–82), dated from the
   1960s and « aussi connue sous le nom "plex italien" en raison de l'origine de ses constructeurs ».
2. **An entire third family, 3.0 Immeubles d'appartements**, exists (PDF pp. 84–108), with three
   fiches — the conciergerie of 1900–1940, the post-1940 walk-up, and the 1960s high-density block.

Both were corroborated independently against the borough's own public guidance at
`montreal.ca/articles/les-plex-patrimoniaux-dans-vsp-100023`, which names all three plex typologies,
and `montreal.ca/articles/les-immeubles-dappartements-patrimoniaux-dans-vsp-100140`.

Each fiche runs to eight pages on a fixed plan (1.7 has seven): `.1` fiche d'accompagnement, `.2`
elevation of the typologie de base, `.3` description under Implantation / Volumétrie / Traitement
architectural, `.4`–`.5` lettered variants with elevations, `.6`–`.8` tables of permitted original
and replacement components. **The component tables were not transcribed** — they are three pages of
bulleted material lists per fiche, they are the worst-affected by the extraction problem below, and
nothing in the data model consumes them. They are the obvious target for a later pass.

## The extraction problem — and why every quotation was checked against an image

`pdftotext` **silently drops text** from this PDF. It is not a layout artefact; whole lines are
absent from the output with no marker. Diagnosis: the document embeds a font subset
(`OMOFGA+CoFoSansVF-Regular`, CID TrueType, Identity-H) whose glyphs poppler cannot map to Unicode,
and it emits nothing for those runs.

The failure is quiet and it lands mid-sentence. On PDF p. 13 (fiche 1.2.3) the text layer reads:

> Traitement architectural … sont disposées de part et d'autre de la porte d'entrée centrale.

while the page actually reads:

> **Traitement architectural — La composition de la façade de la maison est généralement symétrique :
> deux fenêtres** sont disposées de part et d'autre de la porte d'entrée centrale.

A parser trusting the text layer would have published a French quotation missing its subject.

**Method adopted:** `pdftohtml -xml` over the whole document to locate runs that emit only
whitespace, then `pdftoppm -r 100 -png -cropbox` to render every affected page, and every French
sentence quoted anywhere in this place record read off the rendered image. Pages rendered and read
visually:

`2, 5, 13, 19, 21, 27, 29, 31, 37, 38, 39, 43, 45, 47, 51, 53, 58, 61, 62, 63, 67, 75, 84, 85, 89,
93, 96, 97, 101, 103, 105`

36 pages carry blank-emitting runs in total, 396 runs. The great majority (pages `.6`–`.8` of each
fiche) are in the component tables, which are not transcribed. **No French sentence in this record
comes from the text layer alone.**

Two transcription decisions worth recording, both preserving source error rather than silently
correcting it: fiche 3.1 reads « … donne accès à tous les appartements. » preceded by a lower-case
« une porte d'entrée centrale » after a full stop, and fiche 1.7 omits the full stop after
« La toiture fait saillie au-dessus du perron ». Both are kept as printed.

## Documents sought and NOT retrieved

| document | route tried | result |
|---|---|---|
| **Étude d'évaluation patrimoniale et de mise en valeur des maisons de type « shoebox »**, 2018, Isabelle Bouchard | `ville.montreal.qc.ca/pls/portal/…/MAISONS SHOEBOX_ ÉTUDE_ÉVALUATION PATRIMONIALE_WEB.PDF` (https and http); `portail-m4s.s3.montreal.ca` | **404 / 302 to a dead portal page; S3 403.** The Ville's legacy `pls/portal` host no longer serves it. |
| **Parc-Extension : 100 ans d'histoire** (`rech_bilan_parc_extension.pdf`) | legacy host; S3 portal | **404 / 403** |
| **Portrait du quartier Parc-Extension** (`portrait_parc_extension.pdf`) | legacy host; S3 portal | **404 / 403** |

The Wayback Machine was unreachable through the agent proxy (502 on the availability API, connection
reset on `web.archive.org`), so no archived copy could be tried.

**Two data consequences, both written into the records rather than papered over:**

1. **« uniplex ».** The Part 10 brief asks for VSP's proposed alternative name for the shoebox. The
   claim traces to the 2018 study above, which was not retrieved. A search index returned an English
   paraphrase — that the houses could as well be called *uniplex*, being generally single-family
   dwellings though some have a basement flat — and that paraphrase matches the brief's own wording.
   It is therefore recorded in `prose.md` **in English, attributed, and labelled as unverified**.
   **No French quotation for « uniplex » is published anywhere in this record.** Retrieve the study
   and quote it directly before treating any wording as verbatim.
2. **The Parc-Extension wartime quadrilatère.** The brief asks for the quadrilateral bounded by
   Bloomfield, Jarry, Wiseman and de Liège to be encoded as a sector. It is **not** in the 2005
   cahier, which publishes ten coded sectors for this borough and codes no Parc-Extension wartime
   ensemble at all; the four street names occur in the cahier only in the list of immeubles de valeur
   exceptionnelle (7060 and 7290 avenue Bloomfield, 7941 avenue Wiseman). The documents that would
   confirm it are the two Parc-Extension PDFs above, both 404. It is encoded as `PE-WH-1` — a code
   deliberately outside the Évaluation's grammar so it can never be mistaken for one — with the
   doubt stated in its `note`.

## Corrections to the brief

1. **The plex list was truncated**, and family 3.0 was missing entirely. See above. Nine fiches
   expected, thirteen found.
2. **`01-283-124` is confirmed as VSP's by-law**, as the brief's own self-correction says. The
   document's running head reads « RÈGLEMENT DE ZONAGE DE L'ARRONDISSEMENT DE
   VILLERAY–SAINT-MICHEL–PARC-EXTENSION / ANNEXE F : TYPOLOGIES ARCHITECTURALES RÉSIDENTIELLES » on
   every fiche title page, and the PDF's own cover sheet is headed ANNEXE 4. Both facts are recorded.
3. **`depliant_maisons_shoebox_final_web.pdf` is a VSP publication, not a Rosemont one.** The brief
   cites this file under §2.3.2 Rosemont. Its own imprint reads « ARRONDISSEMENT DE
   VILLERAY–SAINT-MICHEL–PARC-EXTENSION / DIRECTION DU DÉVELOPPEMENT DU TERRITOIRE / 405, avenue
   Ogilvy » — the VSP borough hall — and « Année de publication : 2019 ». Its shoebox definition,
   which the brief quotes under Rosemont, is this borough's text. Flagged here only; Rosemont's
   record was not opened or edited.
4. **Parc-Extension lot dates conflict.** The brief dates the "Park Avenue Extension" lots to 1907
   and attributes them to Park Realty. The cahier says « Sur le territoire de Parc Extension, les
   lots sont à vendre **dès 1912** » (14.I.1) and names only the development project, not a company.
   The Ville's MEM encyclopedia gives « Depuis 1910 » for the quarter. All three are recorded in
   `prose.md`; only 1912 and 1910 are sourced.

## Photographs — every licence read before download

Rule applied: no file retrieved whose terms had not been read first. Author, licence, description and
file URL were read individually through the Commons API
(`action=query&prop=imageinfo&iiprop=url|extmetadata`) on 17 August 2026.

**Published — four files, all Creative Commons, all own work:**

| local file | Commons file | author | licence | match |
|---|---|---|---|---|
| `shoebox-debut-20e-parapet-fronton.jpg` | [Maison shoebox à Montréal 08](https://commons.wikimedia.org/wiki/File:Maison_shoebox_%C3%A0_Montr%C3%A9al_08.jpg) | Guerinf | CC BY-SA 4.0 | visual; uploader places it in Villeray |
| `shoebox-parement-leger-galerie.jpg` | [Maison de style shoebox à Montréal 09](https://commons.wikimedia.org/wiki/File:Maison_de_style_shoebox_%C3%A0_Montr%C3%A9al_09.jpg) | Guerinf | CC BY-SA 4.0 | visual; uploader places it in Parc Extension |
| `shoebox-milieu-20e-surelevee.jpg` | [Maison de style Shoebox à Montréal 03](https://commons.wikimedia.org/wiki/File:Maison_de_style_Shoebox_%C3%A0_Montr%C3%A9al_03.jpg) | Guerinf | CC BY-SA 4.0 | visual; uploader places it in Villeray |
| `plex-debut-20e-avenue-de-gaspe.jpg` | [Avenue Caspé Villeray Montreal](https://commons.wikimedia.org/wiki/File:Avenue_Casp%C3%A9_Villeray_Montreal.jpg) | Great11 | CC BY-SA 4.0 | visual; uploader's description reads "Avenue Gaspé Villeray Montreal" |

A fifth file, `Maison de style Shoebox à Montréal 01.jpg` (Guerinf, CC BY-SA 4.0), was verified and
downloaded but is not published; the parapet-à-fronton photograph carries the fiche's description
more completely. **Every match is on form, not on address, and every record carries
`match_confidence: visual`.**

**Categories checked:**

- `Category:Multiplexes (buildings)` — enumerated, 23 files. Its four Montréal entries are in
  Ville-Marie, the Sud-Ouest, Saint-Léonard and Verdun. **Nothing in this borough; nothing used.**
- `Category:External staircases` — named in the brief as the correct category (`Category:Staircases`
  being interior). **Never successfully enumerated**: every request returned the Commons API
  rate-limit error. Nothing in this record depends on it. Retry on a later pass.
- `Category:Villeray` — enumerated, ~150 files, and the source of the plex photograph. Mostly
  restaurants, parks, churches and civic buildings.
- `Category:Parc-Extension` and `Category:Villeray–Saint-Michel–Parc-Extension` — both returned empty
  or failed; the borough-level categories are not usefully populated, as the brief predicted.

**Types with no photograph.** Nine of the thirteen carry placeholders citing the by-law's own
elevation drawings, which are © Ville de Montréal and are **not reproduced**: boomtown, maison
d'après-guerre, jumelé d'après-guerre, bungalow, plex du milieu and de la seconde moitié du 20e
siècle, and all three immeubles d'appartements. No freely-licensed photograph identifiable as being
in this borough was found for any of them. **No commercial real-estate blog was consulted or cited**,
per §1.4 — several rank highly for "shoebox Montréal" and all were passed over.

## Not done, and why

- **Component tables** (`.6`–`.8` of each of the thirteen fiches, ~39 pages) not transcribed: no
  schema consumes them, and they are where the font problem is worst.
- **Zone-boundary geometry** for the ten zone codes the variants cite (H01-016, H01-131, H02-096,
  H03-032, H03-034, H03-049, H03-081, H03-085, H03-125, H03-128, H03-131, H03-132) not resolved; the
  codes are recorded on the variants verbatim, the polygons are not.
- **Guy Gaudreau, "Les premières maisons shoebox montréalaises de Rosemont et de Villeray"**
  (DOI 10.3138/uhr-2020-0004) is cited but paywalled and unread; no statement here rests on it.
- **`donnees.montreal.ca` `TYPOLOGIE_SPECIFIQUE`** join (brief §1.3) not attempted — it is a
  cross-borough deliverable, not a place record's work.
