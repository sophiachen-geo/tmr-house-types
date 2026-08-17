# sources/west-island/pointe-claire — acquisition manifest

Crawled 17 August 2026 for Part 11a (Pointe-Claire). Fetches with `curl -sSL`, a browser user-agent
where a server required one. `.txt` files are text renderings of the file above them —
`pdftotext -layout` for PDFs, a local HTML-to-text pass for the RPCQ pages. Checksums are sha-256 of
the file as saved.

## What was fetched

| File | URL | sha-256 | bytes |
|---|---|---|---|
| `rpcq_196303.html` | `https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&type=bien&id=196303` | `82d12efe26bb65a00e8d8525cf22e2404d4179e51604eb9690e9cb160af7324c` | 49 335 |
| `rpcq_93473.html` | `…&id=93473` — moulin à vent | `cbbe13588f04fb1b50b67caa3795cecfd044ea3971f6973a96f6eb559a0c5b89` | 62 378 |
| `rpcq_92796.html` | `…&id=92796` — maison Hyacinthe-Jamme-Dit-Carrière | `5d98a41a91947f21f136c40bbaf3a2f9dd7b55f25555e029eb75dbc7215e1077` | 54 969 |
| `rpcq_92413.html` | `…&id=92413` — maison Jean-Baptiste-Jamme-Dit-Carrière | `76532c5850d2d810955ba63787fa32f34d4684cbd03afb4525b65bf44cc38fe5` | 54 860 |
| `PC-2808_Site_patrimonial.pdf` | `https://www.pointe-claire.ca/assets/images/Documents/PC-2808_Site_patrimonial.pdf` | `c4416c5810950fb6a469a4ee539d0b1ca1d319198f8bd638ca30c64732c08a80` | 116 808 |
| `PC-2880_Code-Villageois.pdf` | `https://www.pointe-claire.ca/assets/images/Documents/PC-2880_Code-Villageois_2025-10-03-1.pdf` | `0260fd91e6166363c172903e8431f90e0b1922917c4b20114904dd0dda8a2f3c` | 29 742 604 |
| `PC-2787_PIIA.pdf` | `https://www.pointe-claire.ca/assets/images/Documents/pc-2787_piia_codif_2024-12-10.pdf` | `bdd41a7074820dbf4241a8fcf0491ea2558f3f10e2ab3ee18670a585e4397935` | 1 745 714 |
| `19_evaluation_patrimoine_pointe-claire.pdf` | `http://ville.montreal.qc.ca/pls/portal/docs/PAGE/PATRIMOINE_URBAIN_FR/MEDIA/DOCUMENTS/19_EVALUATION_PATRIMOINE_POINTE-CLAIRE.PDF` | `f528324af4e4db529b497acb532d74fcd5fb0c5f6e8dbc404a19e6216a6de7b7` | 8 373 870 |
| `zonage.html`, `reglement_pc2808_page.html`, `code_villageois_page.html` | the Ville de Pointe-Claire pages the three by-law PDFs were found from | — | — |

`rpcq_92413.html` is kept although it is **not** used: the maison Jean-Baptiste-Jamme-Dit-Carrière is
in **Kirkland**, not Pointe-Claire, which is only visible on the fiche itself. It is recorded so a
later pass does not repeat the check.

## The by-law number Part 11 § 4 listed as outstanding

**Found: PC-2808**, « Règlement sur la citation du noyau institutionnel de Pointe-Claire comme site
patrimonial ». Route: the city's *Zonage* page lists its urbanism by-laws by number and links each to
a page of its own; that page publishes the full PDF. The by-law itself gives resolution **2013-123**,
adoption at the ordinary sitting of **Tuesday 2 April 2013 at 19h30**, mover conseiller Geller,
seconder conseiller Smith, present conseillers Bissonnette, Geller, Iermieri, Trudeau, Smith and
Sztuka under maire suppléant J. Labbé, absent conseiller Grenier and maire Bill McMurchie; signed
Bill McMurchie, maire, and Jean-Denis Jacob, avocat, greffier. Cover line: « En vigueur le 12 décembre
2012 / Publication le 10 avril 2013 ».

## Photographs

Every candidate's licence, author, description and file URL was read through the Commons API
(`action=query&prop=imageinfo&iiprop=url|extmetadata`) **before** any download, and every downloaded
file was opened and looked at before publication.

| Asset | Commons file | Licence | Author | Verdict |
|---|---|---|---|---|
| `moulin-a-vent-commons.jpg` | `Moulin à vent de Pointe-Claire, 1, avenue Saint-Joachim … (8533745051).jpg` | CC BY 2.0 | Denis Tremblay / Parcours riverain, 2012-10-18 | published — hero |
| `avenue-cartier-commons.jpg` | `Avenue Cartier (Pointe-Claire) (8738646295).jpg` | CC BY 2.0 | Denis Tremblay, 2012-10-18 | published — Boomtown |
| `noyau-villageois-commons.jpg` | `Noyau villageois de Pointe-Claire (8533752297).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-25 | staged — shared `maison-de-tradition-quebecoise` |
| `chemin-du-bord-du-lac-commons.jpg` | `Chemin du Bord-du-Lac (Pointe-Claire).jpg` | CC BY 2.0 | Parcours riverain Montréal, 2010-11-25 | staged — shared `maison-de-tradition-quebecoise` |
| `avenue-demers-commons.jpg` | `Avenue Demers (Pointe-Claire) (8533752167).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2012-10-18 | staged — shared `maison-de-tradition-quebecoise` |
| `ancien-hotel-canada-322-324-bord-du-lac-commons.jpg` | `Ancien hôtel Canada, 322-324, chemin du Bord-du-Lac … (8534869366).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-25 | staged — village core, mansard |
| `ancien-hotel-pointe-claire-286-bord-du-lac-commons.jpg` | `Ancien hôtel Pointe-Claire, 286, chemin du Bord-du-Lac … (8533761731).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-25 | staged — village core, mansard |
| `secteur-avenue-du-golf-commons.jpg` | `Secteur de l'avenue du Golf (Pointe-Claire) (8533767567).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-25 | staged — shared `villa-anglaise-de-villegiature` |
| `secteur-bowling-green-commons.jpg` | `Secteur Bowling Green (Pointe-Claire) (8534877890).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-25 | staged — shared `villa-anglaise-de-villegiature` |
| `secteur-cedar-park-avenue-cedar-commons.jpg` | `Secteur de Cedar Park, avenue Cedar (Pointe-Claire) (8533764813).jpg` | CC BY 2.0 | Denis Tremblay, 2012-10-18 | staged — shared `villa-anglaise-de-villegiature` |
| `maison-hyacinthe-jamme-dit-carriere-commons.jpg` | `WTMTL T11 MG 7084.JPG` | CC BY-SA 3.0 | Claudie Gauthier, François Gauthier-Giroux (Wikipedia Takes Montreal), 2011-08-28 | staged — shared `maison-de-pierre-regime-francais` |

**Rejected on inspection.** `Avenue Maywood, Pointe-Claire.jpg` (CC BY-SA 3.0, Jeangagnon, 2014-05-23)
is titled for a street that carries two addresses on the PIIA heritage list, but the photograph shows
modern five-storey apartment blocks and a road, and neither heritage building is in it. Downloaded,
looked at, discarded.

**Not found.** No free photograph identifiable as a Pointe-Claire *Cubique* and none of a
Pointe-Claire veterans' house. Both cards carry placeholders; the Cubique's credits the Code
villageois's own figure, © Ville de Pointe-Claire, permission required.

## Not retrieved

- Individual RPCQ fiches for the église Saint-Joachim, the couvent, the presbytère, the croix des
  missions and the école Marguerite-Bourgeoys. Everything the page says about them comes from RPCQ
  196303 and from by-law PC-2808, both of which describe them.
- Any independent account of the village fire beyond the two municipal documents.
