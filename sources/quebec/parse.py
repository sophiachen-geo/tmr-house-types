#!/usr/bin/env python3
"""Parse the crawled Ville de Québec thésaurus pages into parsed.json.

Parsing spec: PART 7 §1.3, verified against tid 501 and checked against tid 303.

Page anatomy, in order:
    <h2>  = "{Courant} - {Type}", or the node's own name alone when it is a style node
    <img src=".../thesaurus/{tid}/{n}.jpg">   the commissioned illustration
    2-3 <p> of history and description
    <strong>Éléments caractéristiques :</strong><br> - … <br> - …
    <p>Illustration : Charles-Étienne Brochu, 2022.</p>
    <h3>Bâtiments liés à ce style</h3> + 3-4 fiche.aspx?fiche=N links
    "Retour aux styles architecturaux"

Three structural variants the CMS actually emits, all handled here:
  * tid 501 etc. — marker inside a <p>, bullets <br>-separated, credit in the next <p>;
  * tid 105     — marker as bare text outside any <p>, bullets written "-Composition …";
  * tid 801/606 — the bullet list runs across several <p> blocks carrying <strong> sub-heads
                  ("Bungalow à long pan (modèle populaire au Québec)"). Sub-heads are kept
                  verbatim as list entries: they name the variants and dropping them would
                  merge three variant groups into one.
So the bullet region is taken as everything between the marker and the "Illustration :"
credit (or the end of the summary), split on <br> and </p>, not paragraph by paragraph.

`courant` — the node's parent in the thesaurus — is resolved in this order:
  1. the "{Courant} - {Type}" prefix of the <h2>, where the page has one (§1.3);
  2. the STYLE-column parent in docs_tableau_styles.pdf, where the tableau lists this node
     as a déclinaison (this is what supplies Regency for tid 205/206, whose parent page
     tid 204 is a 404, and Prairie for tid 801);
  3. otherwise the influence family of the landing page that links it, in the City's words.

Output per tid: {tid, url, courant, courant_source, famille, name_fr, illustration, credit,
                 description[], elements_caracteristiques[], related_buildings[]}

Text normalisation — the only changes made to the source French, and the same three the
Gatineau records (Part 6a) declare:
  * hyphenation broken by a line wrap is rejoined ("d’amiante- ciment" -> "d’amiante-ciment");
  * runs of whitespace (the newlines the CMS emits mid-sentence) collapse to one space;
  * HTML entities are unescaped and NBSP becomes a normal space.
Apostrophes are left as the source's U+2019 throughout. Source typos are left alone
(tid 801 really does read "revêt-ment de membrane(s)").

Usage:  python3 parse.py            # writes parsed.json next to this file
        python3 parse.py 501 303    # prints those records only
"""
import html as html_mod
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HTML_DIR = HERE / "html"
OUT = HERE / "parsed.json"
BASE = "https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati"
MARKER = "Éléments caractéristiques"

TITLE_RE = re.compile(r'lblTitre">(.*?)</span>', re.S)
IMG_RE = re.compile(r'imgPhotoPrincipale"\s+src="([^"]+)"')
SUMMARY_RE = re.compile(r'lblSommaire">(.*?)</span>\s*</p>', re.S)
FICHE_RE = re.compile(r'href="/citoyens/patrimoine/bati/fiche\.aspx\?fiche=(\d+)">(.*?)</a>', re.S)
# The heading may carry a qualifier — "Éléments caractéristiques du Cottage Regency :" (tid 205),
# "… de la Villa Regency :" (tid 206) — which belongs to the heading, not to the first bullet.
# Only the heading that OPENS the block is stripped; a second one inside the list (tid 206 has
# one) is a sub-head and is kept verbatim, exactly like tid 801's variant sub-heads.
MARKER_RE = re.compile(r"(?:<strong>\s*)?" + MARKER + r"[^:<]{0,60}:?\s*(?:</strong>)?\s*", re.I)
CREDIT_RE = re.compile(r"Illustration\s*:", re.I)
LANDING_TID_RE = re.compile(r'href="thesaurus\.aspx\?tid=(\d+)"', re.S)
LANDING_H1_RE = re.compile(r"<section>\s*<h1>(.*?)</h1>", re.S)
LANDING_PERIOD_RE = re.compile(r'class="soustitre">(.*?)</p>', re.S)

# The nine landing pages, in the order the index presents them.
FAMILIES = ["influences-francaises", "influences-britanniques", "milieu-quebecois",
            "influences-styles-historiques", "influences-americaines", "influences-marginales",
            "influences-traditionnelles-modernes", "influences-modernes", "influences-contemporaines"]

# STYLE -> DÉCLINAISON, read off docs_tableau_styles.pdf ("Synthèse des styles architecturaux
# et de leurs déclinaisons"). Used only for nodes whose own <h2> does not name a parent.
TABLEAU_PARENT = {
    "Maison rurale d’inspiration française": "Colonial français",
    "Maison urbaine d’inspiration française": "Colonial français",
    "Maison londonienne": "Néoclassique",
    "Cottage Regency": "Regency",
    "Villa Regency": "Regency",
    "Maison de transition franco-québécoise": "Néoclassique québécois",
    "Maison néoclassique québécoise": "Néoclassique québécois",
    "Maison de faubourg": "Néoclassique québécois",
    "Maison mansardée": "Second Empire",
    "Maison de faubourg à toit plat": "Vernaculaire industriel",
    "Cottage vernaculaire industriel": "Vernaculaire industriel",
    "Maison cubique": "Vernaculaire industriel",
    "Boomtown": "Vernaculaire industriel",
    "Plex": "Vernaculaire industriel",
    "Immeubles à logements": "Vernaculaire industriel",
    "Wartime housing": "Cape Cod",
    "Bungalow": "Prairie",
}


def clean(s):
    """Unescape entities, drop tags, rejoin line-broken hyphens, collapse whitespace."""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html_mod.unescape(s).replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"(?<=\w)-\s+(?=\w)", "-", s)   # "d’amiante- ciment" -> "d’amiante-ciment"


def lines(block):
    """Split a run of CMS HTML into display lines: <br> and block ends are the breaks."""
    block = re.sub(r"(?i)<br\s*/?>", "\n", block)
    block = re.sub(r"(?i)</?(p|div|li|h[1-6])[^>]*>", "\n", block)
    return [x for x in (clean(l) for l in block.split("\n")) if x]


def read_families():
    """tid -> (landing-page family name, its period band), from the nine landing pages."""
    fam, period = {}, {}
    for slug in FAMILIES:
        path = HTML_DIR.parent / "html" / f"{slug}.html"
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        h1 = LANDING_H1_RE.search(raw)
        name = clean(h1.group(1)) if h1 else slug
        per = LANDING_PERIOD_RE.search(raw)
        band = clean(per.group(1)).strip("()") if per else None
        for tid in LANDING_TID_RE.findall(raw):
            fam[int(tid)] = name
            period[int(tid)] = band
    return fam, period


def parse_page(path, families, periods):
    raw = path.read_text(encoding="utf-8", errors="replace")
    tid = int(re.search(r"tid-(\d+)\.html$", path.name).group(1))

    m = TITLE_RE.search(raw)
    if not m:
        raise ValueError(f"tid {tid}: no lblTitre")
    title = clean(m.group(1))
    if " - " in title:
        courant, name_fr = (x.strip() for x in title.split(" - ", 1))
        courant_source = "h2"
    else:
        name_fr = title
        if title in TABLEAU_PARENT:
            courant, courant_source = TABLEAU_PARENT[title], "tableau"
        else:
            courant, courant_source = families.get(tid), "landing-page"

    img = IMG_RE.search(raw)
    ms = SUMMARY_RE.search(raw)
    if not ms:
        raise ValueError(f"tid {tid}: no lblSommaire")
    summary = ms.group(1)

    mk = MARKER_RE.search(summary)
    if not mk:
        raise ValueError(f"tid {tid}: no '{MARKER}' block")
    head, tail = summary[:mk.start()], summary[mk.end():]

    # the credit closes the bullet region
    credit = None
    mc = CREDIT_RE.search(tail)
    if mc:
        rest = clean(tail[mc.start():])
        credit = rest.split(".")[0].strip() + "." if "." in rest else rest
        tail = tail[:mc.start()]

    description = [l for l in lines(head) if l]
    elements = [re.sub(r"^[-–—•]\s*", "", l).strip() for l in lines(tail)]
    elements = [e for e in elements if e]

    related = []
    for fid, label in FICHE_RE.findall(raw):
        name = clean(label)
        if name and not any(r["fiche_id"] == int(fid) for r in related):
            related.append({"name": name, "fiche_id": int(fid),
                            "url": f"{BASE}/fiche.aspx?fiche={fid}"})

    return {
        "tid": tid,
        "url": f"{BASE}/thesaurus.aspx?tid={tid}",
        "name_fr": name_fr,
        "courant": courant,
        "courant_source": courant_source,
        "famille": families.get(tid),
        "periode_famille": periods.get(tid),
        "linked_from_landing_page": tid in families,
        "illustration": img.group(1) if img else None,
        "credit": credit,
        "description": description,
        "elements_caracteristiques": elements,
        "related_buildings": related,
    }


def main(argv):
    families, periods = read_families()
    recs = {}
    for path in sorted(HTML_DIR.glob("tid-*.html"),
                       key=lambda p: int(re.search(r"\d+", p.name).group())):
        r = parse_page(path, families, periods)
        recs[r["tid"]] = r
    if argv:
        for a in argv:
            print(json.dumps(recs[int(a)], ensure_ascii=False, indent=2))
        return 0
    OUT.write_text(json.dumps([recs[k] for k in sorted(recs)], ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    empty = [r["tid"] for r in recs.values() if not r["elements_caracteristiques"]]
    print(f"parsed {len(recs)} pages -> {OUT.name}")
    print(f"  with bullets: {sum(1 for r in recs.values() if r['elements_caracteristiques'])}")
    print(f"  with related buildings: {sum(1 for r in recs.values() if r['related_buildings'])}")
    if empty:
        print(f"  WARNING: {len(empty)} pages parsed with an empty bullet list: {empty}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
