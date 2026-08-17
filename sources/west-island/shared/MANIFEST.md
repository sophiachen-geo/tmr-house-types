# sources/west-island/shared — Part 11a, the five shared West Island type records

Independent source acquisition for `data/shared_types/*.yaml`. Everything here was retrieved by the
shared-types agent; the per-place source folders beside this one belong to the six place agents.

## Ville de Montréal, Évaluation du patrimoine urbain (2005)

The series of twenty-seven cahiers produced January 2003 – May 2004 for the Plan d'urbanisme adopted
2004-11-23, one per 2002–2006 arrondissement, and therefore the only document that covers all six
West Island places on one method. They characterise **sectors, not building types**: there is no
per-type table anywhere in the series. Five of the twenty-seven cover this territory.

| File | Arrondissement | URL slug | Notes |
|---|---|---|---|
| `03_baie-durfe_evaluation.pdf/.txt` | Beaconsfield–Baie-D'Urfé | `03_evaluation_patrimoine_bbu.pdf` | ISBN not transcribed; sectors 4.E.x / 4.I.x / 4.U.x cover both towns and do not always say which |
| `07_dorval_evaluation.pdf/.txt` | Dorval–L'Île-Dorval | `07_evaluation_patrimoine_dorval.pdf` | eight postwar Ensembles urbains d'intérêt, 7.U.1–7.U.8 — the richest bungalow evidence in the series for this territory |
| `09_lachine_evaluation.pdf/.txt` | Lachine | `09_evaluation_patrimoine_lac.pdf` | ISBN 2-7647-0462-3 |
| `13_ile-bizard-sainte-anne_evaluation.pdf/.txt` | L'Île-Bizard–Sainte-Geneviève–Sainte-Anne-de-Bellevue | `13_evaluation_patrimoine_lile.pdf` | the URL slug does not follow the pattern of the other four and was not findable by guessing; the address came from the Sainte-Anne place agent's `sources.yaml`. Prints its sector codes as **1.E.x**, not 13.x |
| `18_pierrefonds-senneville_evaluation.pdf/.txt` | Pierrefonds-Senneville | `18_evaluation_patrimoine_pier.pdf` | 2.E.4 Grandes propriétés de Senneville is the only sector-level description of the estate belt |

Base URL: `http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/`.
Converted with `pdftotext -layout`. The `.txt` files are two-column and read badly in places; quote
from them only after checking the PDF page.

## Statutory records

| File | Record |
|---|---|
| `rpcq_92796.html/.txt` | Maison Hyacinthe-Jamme-dit-Carrière, Pointe-Claire — classée 1964-08-12; address 152 avenue de Concord Crescent; built 1769–1791 |
| `rpcq_93440.html/.txt` | Maison Rangé-dit-Laviolette, Baie-D'Urfé — citée 2001; address 20122 chemin Lakeshore; built about 1700 |
| `parkscanada_nhs_1973_senneville.html/.txt` | Senneville Historic District NHS — see the discrepancy note below |

RPCQ 93274 (Le Ber-Le Moyne), 93473 (moulin de Pointe-Claire), 196303 (site patrimonial de la pointe
Claire), 92666 (maison Simon-Fraser) and 179473/179475 were already in the per-place folders and were
read from there rather than re-fetched.

**Parks Canada id 1973 gives two designation years, in two different fields of the same page.** The
metadata line reads `Designation Date: 2002-07-18`; the Heritage Value narrative reads "designated a
national historic site of Canada in 2001" and cites "Historic Sites and Monuments Board of Canada,
Minutes, 2001". Part 11's brief says the record "says 2001" and that 2002 is other people's claim. It
says both. Both are recorded in `domaine-arts-and-crafts.yaml`.

## Photographs

`commons_probe.py` — the helper used to query the Wikimedia Commons API for licence, author,
description and file URL before any download. Usage: `python3 commons_probe.py cat "<category>"` or
pipe file titles into `python3 commons_probe.py info`.

**The Flickr set Part 11 §1.3 flags for licence checking is free.** *Parcours riverain – Ville de
Montréal* (Flickr user `93016341@N07`) is mirrored on Wikimedia Commons under **CC BY 2.0**, with the
Commons `FlickreviewR 2` licence review recorded as **passed, review date 2024-04-30, reviewlicense
cc-by-2.0**. Author of record is "Parcours riverain - Ville de Montréal"; the photographer is named
per file in the description and is **not always Anne-Marie Dufour** — the Le Ber-Le Moyne photograph
used here is by **Denis Tremblay**. The set covers the six places thoroughly: 98 files tagged
(Lachine), 66 (Pointe-Claire), 63 (Sainte-Anne-de-Bellevue), 53 (Dorval), 32 (Senneville), 20
(Baie-D'Urfé).

Eight images were downloaded to `assets/shared_types/`, and **every one was opened and looked at
before publication**. One candidate was rejected on inspection: `File:Quatre-Vents, 12, avenue Dahlia
(Dorval)` was pulled because avenue Dahlia is the 1951 Dorval Model Homes street, and it turned out
to be a two-and-a-half-storey stuccoed house with tiled coping and an arcaded loggia, not a bungalow.
No freely licensed photograph of a postwar bungalow in any of the six places was found, so
`bungalow-apres-guerre.yaml` carries a placeholder crediting the cahiers' own photographs
(© Ville de Montréal, permission required).

## Not retrieved

- **Grand répertoire du patrimoine bâti de Montréal**, zone fiche 1225 (Sainte-Anne village core).
  The Ville's heritage databases are offline; its replacement page states access returns
  « dans le courant de l'année 2026 ». `grepertoire_zone_1225_sainte-anne.html/.txt` is that
  replacement page, kept as evidence of the outage.
- **Internet Archive**. `web.archive.org` and `archive.org/wayback/available` both refused the
  connection from this environment, so no snapshot of the above could be read.
