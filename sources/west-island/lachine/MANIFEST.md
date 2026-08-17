# sources/west-island/lachine — acquisition manifest

Crawled 17 August 2026 for Part 11a (Lachine). Fetches with `curl -sSL`, a browser user-agent where a
server required one. `.txt` files are text renderings of the file above them — `pdftotext -layout`
for PDFs, a local HTML-to-text pass for the RPCQ and Parks Canada pages. Checksums are sha-256 of the
file as saved.

## What was fetched

| File | URL | sha-256 | bytes |
|---|---|---|---|
| `09_evaluation_patrimoine_lac.pdf` | `http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/09_evaluation_patrimoine_lac.pdf` | `ee6a9ac6f7e768c09eddbff8ef80f3af4dd5d92db8d0eb0e7849de81067a2f51` | 9 318 273 |
| `09_evaluation_patrimoine_lac.txt` | *(pdftotext -layout of the above; 66 pp.)* | `50cd4832027500e00d9357b1ff42c0860579e98c6e4f5259223960f0b5dec311` | 230 782 |
| `rpcq_93274.html` | `https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&type=bien&id=93274` | `1fb9cecb66699082f2c26fa09b46fbbdcbc05bf6583d0bd15cd6dcb9059c962c` | 71 426 |
| `rpcq_93274.txt` | *(text rendering of the above)* | `6db44baf539d45a760a88730cf89499ee3bc56fbe0696b56ef7da461f9284685` | 19 694 |
| `pc_nhs_627_fra.html` | `https://www.pc.gc.ca/apps/dfhd/page_nhs_fra.aspx?id=627` | `e8d3c92a9293c93f7fffd64adf28b559b91a626e9c6e08f72601030784a246cb` | 25 928 |
| `pc_nhs_627_eng.html` | `https://www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=627` | `a26cad43d1ef73e94c8ddf877f9f145c0426d392a841ec228bcde65b11ab9c9e` | 25 046 |
| `ca_lachine_odj_2025-10-01.pdf` | `https://ville.montreal.qc.ca/documents/Adi_Public/CA_Lac/CA_Lac_ODJ_LPP_ORDI_2025-10-01_19h00_FR.pdf` | `20b412def89a05c84cd5d65dff7a38c077d3bd864a3d6309bf7f53e6ca5c2185` | 1 440 061 |

Both language versions of the Parks Canada record were taken deliberately: they disagree with each
other, and with the plaque text they both carry. See `data/places/lachine/prose.md`, `## notes`.

The French Parks Canada URL refused three of five attempts with `Recv failure: Connection reset by
peer` before succeeding; retry, do not conclude the page is gone.

## Photographs

Every candidate's licence, author, description and file URL was read through the Commons API
(`action=query&prop=imageinfo&iiprop=url|extmetadata`) **before** any download, and every downloaded
file was opened and looked at before publication.

| Asset | Commons file | Licence | Author | Verdict |
|---|---|---|---|---|
| `le-ber-le-moyne-maison-commons.jpg` | `Site historique et archéologique Le Ber-Le Moyne, main structure.jpg` | CC BY-SA 4.0 | Simon Geissbuehler, 2018-09-09 | published — hero |
| `le-ber-le-moyne-dependance-commons.jpg` | `…, rear of complex.jpg` | CC BY-SA 4.0 | Simon Geissbuehler, 2018-09-09 | staged for the shared `maison-de-pierre-regime-francais` |
| `maison-quesnel-5010-boulevard-saint-joseph-commons.jpg` | `Maison Quesnel, 5010, boulevard Saint-Joseph (Lachine) (8552680962).jpg` | CC BY 2.0 | Denis Tremblay / Parcours riverain, 2012-10-17 | staged for the shared records |
| `maison-jean-gabriel-picard-5430-boulevard-saint-joseph-commons.jpg` | `Maison Jean-Gabriel-Picard, 5430, … (8552680088).jpg` | CC BY 2.0 | Anne-Marie Dufour / Parcours riverain, 2010-11-18 | staged for the shared records |
| `boulevard-saint-joseph-commons.jpg` | `Boulevard Saint-Joseph (Lachine) (8551449525).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-12 | published — plex type |
| `876-898-boulevard-saint-joseph-commons.jpg` | `876-898, boulevard Saint-Joseph (Lachine) (8552645628).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-12 | published — plex type |
| `26e-avenue-commons.jpg` | `26e Avenue (Lachine) (8552634536).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-18 | published — small brick house |
| `rue-mclaughlin-commons.jpg` | `Rue McLaughlin (Lachine) (8551544881).jpg` | CC BY 2.0 | Anne-Marie Dufour, 2010-11-12 | published — Victorian bourgeois house |

**Rejected on inspection.** `Maison Emma-Jane-Sandilands, 4650-4666, rue Richard-Hewton (Lachine)
(8774842726).jpg` (CC BY 2.0, Anne-Marie Dufour, 2013-05-17) is a genuine photograph of a real address
on the cahier's exceptional list — the Manoir Elmscroft / Bickerdike Mansion — but most of the frame
is a late-20th-century condominium extension in matching stone, and publishing it as a Victorian
villa would misrepresent what survives. Downloaded, looked at, deleted.

**Not found.** No free photograph of a Lachine postwar house was located for the maison « Gameroff ».
Commons categories `Lachine`, `Buildings in Lachine` (empty), `Houses in Lachine` (empty) and searches
on *Sir-George-Simpson*, *Victoria*, *40e Avenue* and *bungalow* returned nothing usable; the one file
titled for a street in that sector shows modern apartment blocks. The card carries a placeholder
crediting the cahier's own figure, © Ville de Montréal, permission required.

**Licence provenance.** The *Parcours riverain – Ville de Montréal* Flickr set named in Part 11 § 1.3
was checked directly at `flickr.com/photos/parcoursriverain/8552645628`: the page source carries
`"license":4`, `creativecommons.org/licenses/by/2.0/`, `title="CC BY 2.0"` and the visible text "Some
rights reserved". It is free for reuse with attribution. The brief attributes the whole set to
Anne-Marie Dufour; that is only partly right — the West Island photographs credit either Anne-Marie
Dufour or Denis Tremblay in their own descriptions, and Flickr licences are per-photo, so each was
checked individually. No file was taken from Flickr directly; all are Commons re-uploads.

## Not retrieved

- The Lachine borough by-laws themselves. Numbers 2710 (zonage) and 2561 (PIIA) and their replacements
  RCA25-19005 and RCA25-19006 are confirmed from the borough council agenda of 1 October 2025; the
  adopted texts were not fetched and no article number is asserted anywhere.
- Individual RPCQ fiches for the houses named on the cahier's exceptional list (maison Quesnel, maison
  Jean-Gabriel-Picard, maison Martin dit Ladouceur, maison Joseph-Picard, maison Dawes, maison
  Thomas-Amos-Dawes, Heney's Inn, presbytère St. Stephen). Nothing on the Lachine page rests on them.
