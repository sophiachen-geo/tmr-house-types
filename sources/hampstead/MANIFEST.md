# Source manifest — Hampstead

Fetched 2026-08-16 per the Part 5 brief §1.2, and re-fetched 2026-08-16 for the v2 pass: both URLs
returned HTTP 200 and byte-identical files (same sizes, same SHA-256), so nothing was overwritten.
`txt/` holds `pdftotext -layout` extractions.

| file | bytes | url | sha-256 |
|---|---|---|---|
| `evaluation_patrimoine_csl_hampstead_mtl_ouest_2005.pdf` | 4,228,386 | https://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/05_evaluation_patrimoine_csl.pdf | `4f1b6d76845c3e271bd6ddd54102199acb080758f9782997d31a6284a96833ab` |
| `hampstead_775_PIIA.pdf` | 15,820,647 | https://www.hampstead.qc.ca/wp-content/uploads/2022/02/775_PIIA_UBPI-1.pdf | `f29ccbfe534d4065432f6dc8d189ba9f94d6973166a438497f226608254114d0` |
| `txt/evaluation_patrimoine_csl_hampstead_mtl_ouest_2005.txt` | 143,015 | (extraction) | `758f5abdc33ca37547e949fb3eeadc227102d40cf623ad95bafbe048b5546774` |
| `txt/hampstead_775_PIIA.txt` | 129,354 | (extraction) | `e5ff32a5b593295627d992b016a5224084baca6ff4ab80ee1934dacdbeca462a` |

Downloads attempted for Hampstead in §1.2: **2 of 2 succeeded.** No failures.

The 2005 evaluation covers Hampstead inside an arrondissement volume shared with Côte-Saint-Luc and
Montréal-Ouest; its three Hampstead sectors (18.E.3, 18.I.4, 18.U.1) are the whole of the published
characterisation. No per-type catalogue exists.

## Negative findings and unheld evidence (v2)

**The planner attribution is not in any file held here.** Part 5 v2 resolves the designer as
**Leonard E. Schlemm**, landscape architect, working during the 1920s, and records **Sir Herbert
Holt** separately as founder and first president of the Hampstead Land and Construction Company;
the **Frederick G. Todd attribution is explicitly rejected**. The Schlemm attribution rests on two
UQAM scholarly histories of Montréal's garden suburbs (« confié à Leonard E. Schlemm »; « dessinée
par Leonard E. Schlemm durant les années 1920 ») whose full bibliographic details are still
outstanding — completing them is the Part 5b task for this place. Neither history is held in this
folder and neither of the two PDFs above names a planner, so `place.yaml`'s `planner` block and the
`## notes` paragraph both mark the attribution as reported rather than footnoted.

**The demolition/rebuild statistic is confirmed not published.** The Town publishes no annual or
cumulative demolition or rebuild figure; `place.yaml` carries
`demolition_rebuild_statistics.published: false` with a note, and the field stays null. What exists
instead is individual council decisions and demolition notices — 5851 Ferncroft; 74 Stratford
(approved August 2024); 29 Lyncroft (approved February 2025, the replacement single-family house
considered separately); 54 Place Heath — plus a fee by-law that treats demolition permits one at a
time. Those four decisions are recorded in the data as **evidence of practice, not as a statistical
series**, and no count assembled from council records is published by this project. No copy of any
of the four decisions is held in this folder; they are reported at ingest.

## Photographs

None, and none are expected. No reliable open images of Hampstead's houses were located, so all
three type records keep `kind: placeholder` with the credit the brief specifies verbatim:

    pending: photograph on site — rue Thurlow, Vieux-Hampstead (sector 18.E.3)

The priority subject is the two-storey stone English-revival houses of rue Thurlow in
Vieux-Hampstead (sector 18.E.3), with École Hampstead (83 rue Thurlow) and Synagogue Beth Zion
(5740 av. Hudson) as the named landmarks. This is a shoot-it-yourself item.
