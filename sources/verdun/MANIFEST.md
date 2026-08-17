# sources/verdun — acquisition manifest

Everything here was fetched on **17 August 2026**. Checksums are sha-256 of the file as it stands on
disk.

## 1. The document

| file | URL | bytes | sha-256 |
|---|---|---|---|
| `pdf/24_evaluation_patrimoine_ver.pdf` | `http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/24_evaluation_patrimoine_ver.pdf` | 8,294,333 | `3f89140caa4694ad93c13ffbc7b452c041046d1f9c7b8be71a54b210cf39b725` |

HTTP 200 on the first attempt. `pdftotext -layout` produced `txt/24_evaluation_patrimoine_ver.txt`
(2,343 lines). The PDF reports 7 pages because it is a scanned-and-rebuilt composite; the printed
folios run to p. 50 and are what the citations on the place page use.

Ville de Montréal, *Évaluation du patrimoine urbain : arrondissement de Verdun*, 2005,
ISBN **2-7647-0464-X**, dépôt légal BNQ and BNC 2005. Direction Céline Topp; analysis by the Division
du patrimoine et de la toponymie under **Jean-François Gravel**, January 2003 – May 2004, for the Plan
d'urbanisme adopted 23 November 2004. Team as printed: Julie Boivin, Elizabeth Bonner, Anne-Marie
Dufour, Guy Lafontaine, Christiane Lefebvre, Pierre-Paul Savignac (architects), Denise Caron
(historian); archaeology Claire Mousseau with Françoise Duguay, François Bélanger, Anne-Marie Balac
and Christian Roy. One of a series of **27 cahiers**.

## 2. The code — read from inside the PDF, as the brief requires

The file is published as `24_…_ver.pdf`. **Every code printed inside it begins `21`.** Extracted with
`grep -o '\b[0-9]\{1,2\}\.\(E\|I\|N\|U\|AP\)\.[0-9]\{1,2\}[A-Z]\?\b' | sort -u`, the complete set is:

```
21.AP.1  21.AP.2
21.E.1  21.E.1A  21.E.1B  21.E.1C  21.E.2  21.E.3  21.E.4  21.E.5  21.E.6  21.E.7
21.I.1  21.I.2  21.I.3  21.I.4  21.I.5  21.I.6  21.I.7  21.I.8  21.I.9  21.I.10
21.U.1
```

So **Verdun is code 21 in file 24** — the memo is right for this borough, and it is now verified
rather than assumed. `21.E.1` appears as a bare code on the synthesis map, where the three lettered
parts are drawn as one polygon; in the running text it is always 21.E.1A / 1B / 1C.

The synthesis map also carries sub-lettered sector variants that the running text does not use —
`21.I.2a`, `21.I.2b`, `21.I.2c`, `21.I.5a`, `21.I.5b`. They are recorded here and not encoded.

No `21.N.n` sector exists: Verdun has no *secteur industriel d'intérêt*, which fits a cahier that
calls the territory « presque exclusivement résidentielle ».

## 3. What was encoded

* `place.yaml`, `phases.yaml` (5), `sectors.yaml` (**9**), `sources.yaml`, `prose.md`,
  `types/` (**6**).
* Sectors: the seven **secteurs de valeur patrimoniale exceptionnelle** only, which make nine records
  because 21.E.1 is printed in three lettered parts. Every `summary_fr` is the source text verbatim
  with two-column hyphenation restored; every `summary_en` is a translation made here.
* Types, all six with a `profile_note` naming the fiches their columns came from, because the
  Évaluation is a sector characterisation and not a per-type table:

| slug | canonical | sectors | evidence |
|---|---|---|---|
| `plex-escalier-exterieur` | `triplex-exterior-stair` | null | 21.I.2, 21.I.5, 21.I.6 (+21.I.1) |
| `duplex-jumele-balcons` | `plex-family` | 21.E.2, 21.E.3 | +21.I.7 |
| `immeuble-commercial-balcon-alcove` | `mixed-use-flat-roof-block` | 21.E.1A, 1B, 1C | +21.I.5 |
| `maison-national-housing-act` | `veterans-house-nha` | 21.E.5 | +21.I.9, 21.I.10 |
| `tour-habitation-ile-des-soeurs` | `modern-slab-tower` | 21.E.6 | +§3.2.2 D, §3.1, ch. 2 |
| `duplex-en-rangee` | `plex-family` | null | 21.I.8 (+21.I.10) |

Two records carry `sectors: null` because their only evidence is in **I** sectors, which this part
does not publish. That is deliberate: pointing them at an E code they do not belong to would be worse
than leaving the field empty.

## 4. What was **not** encoded, and why

* **The ten `21.I` sectors, `21.U.1` and the two `21.AP`.** Part 10a captures E sectors only (brief
  §4). They are summarised in the place page's `## notes` so a reader knows what is missing, and
  four type records quote them. Enumerating them is Part 10b.
* **A "maison urbaine" type.** The cahier names four (703-707 rue Gordon; 3267, 3513 and 3523 rue
  Wellington), plus a *maison bourgeoise* at 5695 boulevard LaSalle and the *maison
  Nivard-de Saint-Dizier* at 7244 boulevard LaSalle, but gives no typological description of any of
  them. Listed in `## notes`; no type record invented.
* **`count_in_place` anywhere.** The cahier counts nothing except the ~30 buildings on the Douglas
  campus and the 18,000 dwellings of 1946, neither of which is a type count.
* **A `grading` block.** Verdun has no per-building value classes; the cahier's only grading is the
  E / I / U ranking of sectors, which `sectors.yaml` already carries.
* **`sector_map`.** The synthesis map is embedded in the PDF and no rasterisation was attempted.

## 5. Contradictions found, and how they were handled

Recorded in full in the place page's `## notes`; summarised here.

| item | source A | source B | encoded |
|---|---|---|---|
| village created | cahier ch. 2: **1874** | cahier archaeology ch.: **1876**; municipal record: **1 Jan 1875** | `founded: 1875`, all three printed in notes |
| renamed Verdun | cahier: **1878** | municipal record: **28 Dec 1876** | notes |
| *ville* status | cahier: **1909** | municipal record: **14 Mar 1907** (cité 21 Dec 1912) | 1907 in prose, cahier's 1909 quoted where it is the thing being quoted |
| dike begun | cahier ch. 2: **1895** | cahier archaeology ch.: **1896** | both printed |
| superficie | memo: **9.7 km²** | fr.wikipedia infobox: **983 ha** | both printed, neither averaged |
| architect's name | cahier body + building list: **Mies van der Rohe** | cahier captions + §3.1: **Mies van de Rohe** | correct form used, slip recorded |

The cahier is internally inconsistent about its own founding dates in two different chapters. That is
worth knowing about a document this project treats as a primary source for four other boroughs.

## 6. Instruments — what verified and what did not

Verified against Héritage Montréal's *Memento* by-law index and the Ville's own pages:

| instrument | number | status |
|---|---|---|
| zonage | **1700** | confirmed (memo agrees) |
| lotissement | **1751** | confirmed (memo agrees) |
| construction | **1750** | confirmed (not in the memo) |
| certificats d'autorisation et d'occupation | **RCA08 210004** | confirmed (memo agrees) |
| démolition | **RCA21 210020** | confirmed; CCU members sit as the comité de démolition |
| PIIA modernisation | **RCA22 210015P1** + zoning **RCA22 210014P** | confirmed, with the 10 January 2023 consultation |

**The memo's "987-series" demolition by-law could not be found.** No municipal source, no *Memento*
entry, no search result. The borough's demolition regime is RCA21 210020 and that is what is
encoded; the memo's claim is recorded as unconfirmed in the instrument title and in `## notes`, not
silently dropped and not repeated as fact.

**The 2020 fee schedule is attested but not retrieved.** *Règlement sur les tarifs (exercice
financier 2020)*, **RCA19 210007** (amended by RCA20 210002), carries a PIIA study fee reserved for
enlarging the roof volume of a **"wartime"-type house** to add habitable space — **$265** in the 2020
edition, $150 and $153 in neighbouring editions. This is the detail the brief flags as the only place
on this site where a fee schedule names a house type, and it survives verification. What did **not**
survive is the primary text:

* `ville.montreal.qc.ca/pls/portal/docs/PAGE/ARROND_VER_FR/MEDIA/DOCUMENTS/…` returns a 404 HTML
  shell for every path tried, including the two document URLs the search index still lists. The one
  legacy path that still serves files is `…/page/patrimoine_urbain_fr/media/documents/…`, which is
  how the cahier itself was obtained.
* `www1.ville.montreal.qc.ca/banque311/…` (the 311 information bank, which carries the fee table)
  now redirects in an infinite loop — curl gives up after 50 hops.
* `ville.montreal.qc.ca/sel/sypre-consultation/recherchereglement` returns HTTP 520.
* `web.archive.org` is not reachable from this environment.

**Consequence: the fee is stated in English on the site and no French is quoted for it.** Retrieving
the by-law and replacing the English paraphrase with the French line is a Part 10b task.

## 7. Photographs — every licence read before download

Checked through the MediaWiki API (`action=query&prop=imageinfo&iiprop=url|extmetadata`) on
17 August 2026, and for the postcard also through `action=parse&prop=wikitext` to read the licence
template itself. Author, licence and file URL are written into every `credit` string.

| file in `assets/places/verdun/` | Commons file | author | licence | used for | `match_confidence` |
|---|---|---|---|---|---|
| `plex-3857-boulevard-lasalle-commons.jpg` | Verdun (9155880752).jpg | Matias Garabedian | CC BY-SA 2.0 | plex with exterior stair | address |
| `boulevard-lasalle-hickson-commons.jpg` | BoulevardLasalleVerdun.jpg | Denis Tremblay (Parcours riverain – Ville de Montréal) | CC BY 2.0 | plex with exterior stair | address |
| `crawford-park-rue-leclair-commons.jpg` | Crawford Park Extension.jpg | A611662 | CC BY-SA 4.0 | NHA house | neighbourhood |
| `201-rue-corot-mies-commons.jpg` | 201Corot.jpg | Niroyb | CC BY-SA 3.0 | Mies tower | address |
| `100-rue-de-gaspe-mies-commons.jpg` | 100 rue De Gaspe - 01.jpg | Jeangagnon | CC BY-SA 4.0 | Mies tower | address |
| `avenue-desmarchais-banq-postcard.jpg` | Desmarchais Boulevard, Verdun.jpg | J. Sykes, Verdun, Que. | PD — BAnQ « Domaine public au Canada » / CC PDM 1.0; Commons `{{PD-old-70}}` | Desmarchais / Moffat duplex | address |

`Restrictions` was empty on all six.

**`match_confidence: neighbourhood` is a third value** beyond the `address` / `visual` this site has
used so far, introduced for the Crawford Park photograph. The cahier illustrates 21.E.5 with rue
Fayolle and rue Truman; the photograph is of rue LeClair, which Commons places in Crawford Park but
which the cahier does not name and whose position relative to the sector boundary was not verified.
`address` would have overstated it and `visual` would have understated it.

### The two Commons categories the brief named

* **`Category:Multiplexes (buildings)`** — 23 files worldwide, only two of them in Québec. One of
  those two, `Verdun (9155880752).jpg`, is in Verdun and is used. (The other is
  `Montréal - Saint-Léonard - Jarry 1.jpg`.)
* **`Category:External staircases`** — **not usable, and the brief's warning understates it.** It is a
  worldwide fire-escape category: its members are Helsinki, Leipzig, Madrid, São Paulo, Rotterdam,
  Bilbao. Its by-country subtree has five branches — Belgium, France, Greece, Japan, Portugal — and
  **no Canada**. `External staircases in Canada`, `…in Quebec`, `…in Montreal` and
  `Exterior staircases in Montreal` do not exist. The Montréal exterior stair, the single most
  photographed feature of the city's housing, has no type-tagged category on Commons at all.

### Checked and rejected

* **`Block near the Lachine Rapides (26575310271).jpg`** (CC BY 2.0, Robbie Sproule, categorised
  under `Verdun (Montreal)`). Downloaded and looked at before use: the "block" is a graffitied
  concrete block on the riverbank, not a city block of housing. A licence check alone would have let
  this through.
* **`Crawford Park Extension at Verdun.jpg`** — byte-for-byte identical (md5
  `39683736959be6c1c35533d700100b85`) to `Crawford Park Extension.jpg`. The same photograph uploaded
  twice by the same author. Only one copy is used, and the duplicate is recorded in the photo note so
  nobody later treats them as two pieces of evidence.
* **The Commons description of the Crawford Park photographs** attributes the subdivision to
  **Samuel Gitterman** at the NHA. That is an uploader's caption, not a municipal source; it appears
  in no document consulted here and is **not** asserted on the site. Noted in the type record's
  `profile_note` as an unverified claim.

### Rate limiting

`upload.wikimedia.org` returns its robot-policy block after the first file or two, on both the
`/thumb/` path and the original. `commons.wikimedia.org/wiki/Special:FilePath/<file>?width=N` works
where the direct route does not, but is itself throttled — the Desmarchais postcard failed through
every route for roughly twenty minutes across four separate retry loops before succeeding unchanged.
`api.php` was never throttled, which is why all licence checking went through it. Anyone re-running
this should use `Special:FilePath`, expect to retry, and leave real gaps between files.

### Nothing from the cahier is in `assets/`

The 2005 cahier's own photographs are © Ville de Montréal (credited in its front matter to Ville de
Montréal, Bibliothèque nationale du Québec, P. Fauteux and D. B Webster). They are recorded as
`photos[]` entries with `file: null`, `kind: placeholder`, `licence: "permission required"` and a
`source_url` pointing at the PDF, naming the page and the caption. None was downloaded.

### No commercial real-estate blog is cited

Per brief §1.4. `balconsverdun` in particular is named there as a source that disagrees with the
municipal record; it was not consulted and is not cited.

## 8. Reproducing

```bash
mkdir -p sources/verdun/{pdf,txt}
curl -sSL -o sources/verdun/pdf/24_evaluation_patrimoine_ver.pdf \
  "http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/24_evaluation_patrimoine_ver.pdf"
pdftotext -layout sources/verdun/pdf/24_evaluation_patrimoine_ver.pdf \
                  sources/verdun/txt/24_evaluation_patrimoine_ver.txt
# the code map, from the document and never from the filename
grep -o '\b[0-9]\{1,2\}\.\(E\|I\|N\|U\|AP\)\.[0-9]\{1,2\}[A-Z]\?\b' \
  sources/verdun/txt/24_evaluation_patrimoine_ver.txt | sort -u
python3 build.py
```

If `build.py` fails on another borough while Part 10a is in progress, copy the tree to a scratch
directory, drop the unfinished places, and build there; Verdun builds clean on its own.
