# sources/west-island/senneville — acquisition manifest

Crawled 17 August 2026 for Part 11a (the West Island cores). All fetches with
`curl -sSL -A "Mozilla/5.0 (compatible; heritage-research/1.0)"` except the Commons downloads,
which went through the MediaWiki API with a project-identifying user agent. Checksums are sha-256
of the file as saved.

## What was fetched

| File | URL | sha-256 | bytes |
|---|---|---|---|
| `18_evaluation_patrimoine_pierrefonds-senneville.pdf` | `http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/18_evaluation_patrimoine_pier.pdf` | `f74215c0f294a35e97a085b0c9407bf3d39b64e97b85a9d9587b94b3636ab539` | 9 216 783 |
| `18_evaluation_patrimoine_pierrefonds-senneville.txt` | *(`pdftotext -layout` of the above)* | `916c2f6ad1da7de8f5f54d2d5087533dd49f409f3340e6acdbe67889b69868ff` | 199 251 |
| `enonce_bois-de-la-roche_2018.pdf` | `https://ville.montreal.qc.ca/pls/portal/docs/PAGE/PATRIMOINE_URBAIN_FR/MEDIA/DOCUMENTS/%C9NONC%C9%20BDLR%20FINAL.PDF` | `3227fc62111a199f0be04e9ec29a2c0980ac5bd790cde7dcecad0677185bfef1` | 4 158 805 |
| `enonce_bois-de-la-roche_2018.txt` | *(`pdftotext -layout` of the above)* | `7a521bc92e45e1a5da803110b773c821127fe0371c3f4bad8e544a9247bdce9c` | 89 253 |
| `piia_452-5_annexe4_guide_2019.pdf` | `https://www.senneville.ca/wp-content/uploads/2023/01/Reglement-452-5-Annexe-4-PIIA-2019-02-18.pdf` | `fc858d00676032200ecafab09d092d92804ae19a96767176611451c4a75ee024` | 11 632 313 |
| `piia_452-5_annexe4_guide_2019.txt` | *(`pdftotext -layout` of the above)* | `71215d4a02871dad5d558427a210765ee91b02d5b869be89b5ebee6ed9c70809` | 33 359 |
| `rpcq_93454.html` | `https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&id=93454&type=bien` | `d0b247efd7d3acf3ec9c12ef522e1a30128bbe397b72ac3f3e584ac2ef0ef949` | 46 565 |
| `rpcq_93454.txt` | *(text rendering of the above)* | `089ef07df0160a6d645a24351a07bedf77f89d0a4561dc9f09795fccf5401bd7` | 12 592 |
| `rpcq_99263.html` | `https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&id=99263&type=bien` | `bee7a8cef0e7bcd97fc1999cf7913ba795686f8db2b7d9dc04c8fe512718d84e` | 32 234 |
| `rpcq_99263.txt` | *(text rendering of the above)* | `ae528622feb6b602cd37b6d0a21ac3884b98487e290a10345e7c1292135ff536` | 3 565 |
| `rpcq_protval_search_senneville.html` | `https://www.patrimoine-culturel.gouv.qc.ca/rpcq/rechercheMotCle.do?methode=rechercher&motCle=Senneville&type=PROTVAL&reset=1` | `b77c5f37d2451c96ae91326bf277d306005c1b4b788d63a847689f871765d735` | 21 930 |
| `commons_licences.json` | Commons API `imageinfo` + `extmetadata` for the five photographs downloaded | `f1a128d44cf53519d435d9fca9cfbc8bf96c5a6f8a862db5f53e07906112af37` | 5 784 |

Note on the évaluation cahier's filename: the Ville de Montréal serves the Pierrefonds-Senneville
volume as `18_evaluation_patrimoine_pier.pdf`, and every sector code printed inside it begins **2**.
It is renamed here for legibility; the URL above is the one that was fetched.

## Photographs

Five files downloaded from Wikimedia Commons at 1600 px through the API's `iiurlwidth` parameter
(Wikimedia answered a first attempt on the originals with HTTP 429). Licence and authorship were
read from the API's `extmetadata` per file before download; all five are free licences.

| Saved as | Commons file | Author / licence |
|---|---|---|
| `180-chemin-de-senneville-todd-estate-commons.jpg` | *180 Senneville Road, Senneville 01.jpg* | Thomas1313, CC BY-SA 3.0, shot 2013-12-20 |
| `170-chemin-de-senneville-loge-du-gardien-commons.jpg` | *Loge du gardien - 170 chemin de Senneville - 01.JPG* | Jeangagnon, CC BY-SA 3.0, shot 2012-08-06 |
| `292-chemin-de-senneville-grange-etable-bois-de-la-roche-commons.jpg` | *Grange-étable du domaine du Bois-de-la-Roche, 292, chemin de Senneville (Senneville) (8531480761).jpg* | « Parcours riverain - Ville de Montréal » / *Photo : Anne-Marie Dufour*, CC BY 2.0, shot 2010-12-10 |
| `264-chemin-de-senneville-maison-morgan-commons.jpg` | *Maison Frederick-Cleveland-Morgan, 264, chemin de Senneville (Senneville) (8532651346).jpg* | same set, CC BY 2.0, shot 2010-12-10 |
| `chemin-de-senneville-commons.jpg` | *Chemin de Sennevile (Senneville) (9026228000).jpg* | same set, CC BY 2.0, shot 2013-05-31 |

The Part 11 brief asked for the licence of the Flickr set *Parcours riverain – Ville de Montréal*
(Anne-Marie Dufour) to be verified before use. It was, through the Commons API on 17 August 2026:
**CC BY 2.0**, `https://creativecommons.org/licenses/by/2.0`, with the photographer named in each
file's description. It is a free licence and the set is used, with attribution, on both this page
and Dorval's.

Every image was opened and looked at before publication. None of the five Senneville files was
rejected. The last one, `chemin-de-senneville-commons.jpg`, shows an empty two-lane road between a
hayfield and woods with no building in sight; it is published deliberately, because that is the
condition Parks Canada lists as a character-defining element of the district — *"the siting and
landscaping of most residences, which prevents a view to the buildings from chemin Senneville."*
Its Commons title carries the source's own typo, *"Sennevile"*.

## What could not be retrieved

- **Parks Canada (`pc.gc.ca`) and the Canadian Register of Historic Places
  (`historicplaces.ca` / `lieuxpatrimoniaux.ca`)** refuse every direct HTTP request from this
  environment: `curl: (35) Recv failure: Connection reset by peer`, over HTTP and HTTPS, HTTP/1.1
  and HTTP/2, with and without a browser user agent, and through `urllib` as well as `curl`. The
  designation record — id 1973 federally, id 4442 on the Register — was therefore read through the
  WebFetch tool in both English and French, and **no local copy of it exists under `sources/`**.
  Everything quoted from it on the Senneville page comes from those reads. This is the one
  primary source for Senneville that is not archived here, and it is the most important one.
- **The consolidated text of Village de Senneville by-law 452 (PIIA)** was not found: only
  Annexe 4, the *Guide des principes architecturaux*, is served from `senneville.ca`. The by-law's
  article numbers are therefore unverified, and the place record says so.
- **The Village de Senneville by-laws index page** (`/en/municipality/by-laws-and-policies/`)
  returned HTTP 404.
- The RPCQ's **advanced search by municipality** (`rechercheProtege.do`, field
  `municipaliteOfficielle`) accepts a query and returns *« Résultat de la recherche (0) »* for every
  form of the name tried — "Senneville", "Senneville (Village de)", "Dorval", "Dorval (Cité de)" —
  and its keyword-mode result rows are assembled client-side. The protected-heritage keyword search
  used instead (`rechercheMotCle.do?type=PROTVAL`) works and is what the two saved result pages
  record.

## Dating conflicts left unresolved in the sources

| Fact | RPCQ (statutory) | Ville de Montréal cahier (2005) | Village de Senneville site |
|---|---|---|---|
| Fort Senneville built | 1702–1703 | 1703 (archaeology section); **1692** (phase summary, same document) | 1703 |
| Mill | — | wooden 1686, burned 1691, stone under a 1700 contract; **1700** in the phase summary | stone windmill 1686, partly destroyed by fire 1691 |
| Fort destroyed | 1776 | — | 1777 |

The RPCQ classement fiche and the cahier's archaeology section agree; the cahier's own phase
summary does not agree with the rest of the cahier. The statutory record is what the place page
publishes.
