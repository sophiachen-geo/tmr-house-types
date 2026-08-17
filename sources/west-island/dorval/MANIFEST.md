# sources/west-island/dorval — acquisition manifest

Crawled 17 August 2026 for Part 11a (the West Island cores). All fetches with
`curl -sSL -A "Mozilla/5.0 (compatible; heritage-research/1.0)"` except the Commons downloads,
which went through the MediaWiki API with a project-identifying user agent. Checksums are sha-256
of the file as saved.

## What was fetched

| File | URL | sha-256 | bytes |
|---|---|---|---|
| `07_evaluation_patrimoine_dorval.pdf` | `http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/07_evaluation_patrimoine_dorval.pdf` | `72f9300be8c8b5bb988718bca5186037ed7babe5ed35853754229b7405492e4f` | 8 838 059 |
| `07_evaluation_patrimoine_dorval.txt` | *(`pdftotext -layout` of the above)* | `647c0bc07cc6a1c557a79357023eb3f972a848324d1158a71bdb72ef27d1410f` | 162 363 |
| `piia_rcm-60i-2024.txt` | *(`pdftotext -layout` of the PIIA by-law; see note below)* | `230859d065b18a9fac3922636d730a1098ef16ada1a21d633c5888d9f9a5c5d2` | 966 027 |
| `demolition_rcm-97-2023.pdf` | `https://www.ville.dorval.qc.ca/storage/app/media/la-cite/administration-et-finances/reglements-municipaux/reglements-en-vigueur/reglement-rcm-97-2023-demolition-immeubles-final-fr.pdf` | `b44c9dca1c1722e0f6fafa636cda637ebbe1fbb04df34452e80a1a9f86cf1751` | 312 574 |
| `demolition_rcm-97-2023.txt` | *(`pdftotext -layout` of the above)* | `3f8a4638f7c85395da5eada16857dd4c0e5754156ee747830517d533e6a3b417` | 30 398 |
| `etude_12_dahlia.pdf` | `https://www.ville.dorval.qc.ca/storage/app/media/actualites/2025/20240815_lm_rpa_12_ave_dahlia_etude_patrimoniale_finale-fr.pdf` | `52add12b4347754054eee6962d8d62ea520fee5f0b1ab9b1e3b8485739ff2fd1` | 7 459 397 |
| `etude_12_dahlia.txt` | *(`pdftotext -layout` of the above)* | `8652933e3d3988e86d5139026956bfe3e04f6a639a16f26846a4eb66ae857c51` | 159 259 |
| `rpcq_216208.html` | `https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?id=216208&methode=consulter&type=bien` | `e8a7ac191f6e9e834ebcb997927ee562833b77ebf9e557333d69d73e7c5b1c9a` | 55 572 |
| `rpcq_216208.txt` | *(text rendering of the above)* | `9cd3bbe2fe93c616ae6afd44260cc491fcf814b770c57d069ee51787c28de79e` | 14 782 |
| `rpcq_protval_search_dorval.html` | `https://www.patrimoine-culturel.gouv.qc.ca/rpcq/rechercheMotCle.do?methode=rechercher&motCle=Dorval&type=PROTVAL&reset=1` | `c88271ab1f6c74ec0906b8c401e448ba1ccb1c1a7faf9d6c19d62379d8c4d08a` | 18 799 |
| `commons_licences.json` | Commons API `imageinfo` + `extmetadata` for the five photographs downloaded | `f157d2cfd2a6513b67337e9e0125ed362da5f8d839f6b01a200a03628268b689` | 5 431 |

### The one file not archived

`rcm-60i-2024-piia-cod-a-jour-au-2025-12-16-fr-reduit.pdf` — the Cité de Dorval's PIIA by-law
RCM-60I-2024, administrative codification to 16 December 2025 — was fetched successfully
(HTTP 200, **97 531 064 bytes**, sha-256
`b1fc050451de26b2bf1cef8322c21236e38462a51e7e36190b3fc7633fa99813`, 149 pages) but is not kept in
the repository: at 97 MB it is nearly twice the largest file otherwise held under `sources/`. Its
`pdftotext -layout` extraction is archived instead, and every quotation on the Dorval page comes
from that extraction. To refetch:

```bash
curl -sSL -o piia_rcm-60i-2024.pdf \
  "https://www.ville.dorval.qc.ca/storage/app/media/la-cite/administration-et-finances/reglements-municipaux/reglements-en-vigueur/rcm-60i-2024-piia-cod-a-jour-au-2025-12-16-fr-reduit.pdf"
pdftotext -layout piia_rcm-60i-2024.pdf piia_rcm-60i-2024.txt
```

The by-law's own footer reads, on every page, *« Cette codification administrative n'a aucune valeur
officielle »*; the official text is the individual by-laws held by the greffe.

## Photographs

Five files downloaded from Wikimedia Commons at 1600 px through the API's `iiurlwidth` parameter,
which is what Wikimedia asks bulk clients to use — a first attempt on the originals was answered
with HTTP 429. Every one is from the Flickr photostream **« Parcours riverain - Ville de Montréal »**
(`flickr.com/people/93016341@N07`), whose file descriptions all read *« Photo : Anne-Marie Dufour »*,
uploaded to Commons by user *Fabe56*, under **CC BY 2.0**. The Part 11 brief asked for this set's
licence to be checked before use: it is a free licence and the set is usable with attribution.
Per-file URLs, checksums, dimensions and licence fields are in `commons_licences.json`.

| Saved as | Commons file | Shot |
|---|---|---|
| `1850-chemin-bord-du-lac-musee-dorval-commons.jpg` | *Musée de Dorval, 1850, chemin du Bord-du-Lac (Dorval) (8535036734).jpg* | 2010-11-19 |
| `1800-chemin-bord-du-lac-forest-and-stream-club-commons.jpg` | *Forest and Stream Club, 1800, chemin du Bord-du-Lac (Dorval) (8533935523).jpg* | 2010-11-19 |
| `2120-chemin-bord-du-lac-aqua-vista-commons.jpg` | *Aqua Vista, 2120, chemin du Bord-du-Lac (Dorval) (8533904619).jpg* | 2010-11-19 |
| `noyau-villageois-dorval-commons.jpg` | *Noyau villageois de Dorval (8535023862).jpg* | 2010-11-19 |
| `365-chemin-bord-du-lac-magasin-joseph-decary-commons.jpg` | *Magasin Joseph-Décary, 365, chemin du Bord-du-Lac (Dorval) (8533922395).jpg* | 2010-11-19 |

### Downloaded, opened, and rejected

Every image was opened and looked at before publication. Two were downloaded under the same
CC BY 2.0 licence and then deleted rather than published:

- *L'Ermitage, 4, avenue Martin (Dorval) (8535020146).jpg* — a gambrel-roofed villégiature house
  with a wraparound veranda, exactly the form wanted, but photographed mid-recladding: most of the
  veranda wall is bare housewrap and framing. A half-stripped façade is misleading evidence in a
  typology catalogue, so it is not used.
- *Elmridge, 1335, chemin du Bord-du-Lac (Dorval) (8535047054).jpg* — the file name matches an
  address on the 2024 PIIA list, but what the photograph shows is a large stucco-and-half-timber
  institutional building behind three flagpoles and municipal parking signs, not a house, and no
  source consulted gives it a date or a builder. Rejected for want of a description that survives
  inspection.

## What could not be retrieved

- **`pc.gc.ca` and `historicplaces.ca`** refuse every direct HTTP request from this environment
  (`curl: (35) Recv failure: Connection reset by peer`), over both HTTP and HTTPS, HTTP/1.1 and
  HTTP/2, with and without a browser user agent, and through `urllib` as well as `curl`. Federal
  heritage records were therefore read through the WebFetch tool and no local copy exists. This
  affects Senneville rather than Dorval, which has no federal designation at all.
- **The Guide patrimonial de Dorval**, elaborated by the Société historique de Dorval and cited in
  article 56 of the 2024 PIIA as the register of the Cité's heritage elements, was not found
  online and is not held here.
