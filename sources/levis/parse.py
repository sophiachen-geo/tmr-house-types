#!/usr/bin/env python3
"""Parse the Ville de Lévis « Styles architecturaux » catalogue into JSON.

Input  : sources/levis/html/index.html and sources/levis/html/fiche-<N>.html
         (fetched by the crawl documented in sources/levis/MANIFEST.md)
Output : sources/levis/parsed.json

The catalogue is a TYPO3 extension (tx_absrubriquearchitecturale) whose fiche
markup is stable across all twenty pages:

    <div class="unefiche"><h1>NAME</h1>
      <img class="croquisg" src="...">                     the line drawing
      <div class="blocjaune">  … Nombre à Lévis : [environ] <span class="nombre">100</span> bâtiments
      <div class="blocjaune dernier"> … Période de construction : <span class="nombre">1900-1930</span>
      <div class="fauxtable">
        <div class="ligne"><div class="gauche">LABEL</div><div class="droite">VALUE</div></div>  ×7
      <div class="blocbas">
        <h4>Quelques exemples significatifs d'hier...</h4> <div class="blocthumbs1">…</div>
        <h4>...et d'aujourd'hui</h4>                       <div class="blocthumbs1">…</div>
        <h4>Exemple de mise en valeur</h4>                 <div class="blocthumbs2">
          <div class="ombmise"> … <span class="desc">ANCIENNE<br/> photographie</span>
      <div class="barnavfiche"><a class="prev" …><a class="next" …>

Verified against idfiche=10 (Boomtown) and idfiche=1 (Vernaculaire américain);
see check_cases() at the foot of this file, which runs on every invocation and
raises if the two reference fiches ever stop matching the transcribed spec.
"""
from __future__ import annotations

import html as htmlmod
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
HTML = HERE / "html"
OUT = HERE / "parsed.json"

BASE = ("https://www.ville.levis.qc.ca/developpement-planification/"
        "architecture-patrimoniale/styles-architecturaux/")

# the seven « Caractéristiques » labels the catalogue uses, in fiche order
FIELDS = ["Volumétrie", "Plan", "Toiture", "Revêtements", "Ouvertures",
          "Saillies", "Ornementation"]

# "ANCIENNE photographie" etc. -> photos[].kind
PHOTO_KINDS = {"ANCIENNE": "historic", "AVANT": "before",
               "POTENTIEL": "potential", "APRÈS": "after"}


# ----------------------------------------------------------------- utilities
def text_of(fragment: str) -> str:
    """Strip tags from an HTML fragment and normalise whitespace/entities."""
    s = re.sub(r"<br\s*/?>", " ", fragment)
    s = re.sub(r"<[^>]+>", "", s)
    s = htmlmod.unescape(s)
    s = s.replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip()


def slugify(name: str) -> str:
    """« Autre type : Bâtiment mixte… » -> autre-type-batiment-mixte…"""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("’", "'").replace("&", " et ")
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s


def abs_url(src: str) -> str:
    if src.startswith("http"):
        return src
    return "https://www.ville.levis.qc.ca/" + src.lstrip("/")


# -------------------------------------------------------------------- index
def parse_index(raw: str) -> list[dict]:
    """Harvest (idfiche, name, period) from the index listing, in index order."""
    out = []
    pattern = re.compile(
        r'href="[^"]*\?idfiche=(\d+)"'          # the fiche link
        r'(?:(?!</a>).)*?'                      # …anything up to the caption…
        r'<span class="titre">(.*?)</span>'
        r'\s*<span class="date">(.*?)</span>',
        re.S)
    for m in pattern.finditer(raw):
        idf, name, period = int(m.group(1)), text_of(m.group(2)), text_of(m.group(3))
        out.append({"fiche_id": idf, "name_fr": name, "period_label": period,
                    "slug": slugify(name)})
    return out


# -------------------------------------------------------------------- fiche
def parse_fiche(raw: str, idf: int) -> dict:
    block = re.search(r'<div class="unefiche">(.*?)<a class="retourliste"', raw, re.S)
    if not block:
        raise ValueError(f"fiche {idf}: no <div class=\"unefiche\"> block")
    body = block.group(1)

    h1 = re.search(r"<h1>(.*?)</h1>", body, re.S)
    if not h1:
        raise ValueError(f"fiche {idf}: no <h1>")
    name_fr = text_of(h1.group(1))

    # --- Nombre à Lévis  ------------------------------------------------
    # <div class="blocjaune"> … [environ.png] <span class="nombre">100</span>
    #                            <p class="deux">bâtiments</p>
    count = count_approx = None
    count_unit = None
    nb = re.search(r'<div class="blocjaune">(.*?)</div>', body, re.S)
    if nb and "Nombre à Lévis" in nb.group(1):
        frag = nb.group(1)
        n = re.search(r'<span class="nombre">\s*([\d\s ]+)\s*</span>', frag)
        if n:
            count = int(re.sub(r"[^\d]", "", n.group(1)))
        count_approx = "environ.png" in frag       # the "±" glyph the City sets
        unit = re.search(r'<p class="deux">(.*?)</p>', frag, re.S)
        count_unit = text_of(unit.group(1)) if unit else None

    # --- Période de construction ---------------------------------------
    period = None
    pb = re.search(r'<div class="blocjaune dernier">(.*?)</div>', body, re.S)
    if pb and "Période" in pb.group(1):
        n = re.search(r'<span class="nombre">(.*?)</span>', pb.group(1), re.S)
        if n:
            period = text_of(n.group(1))

    # --- the seven-row « Caractéristiques » pseudo-table -----------------
    fields, field_links = {}, {}
    table = re.search(r'<div class="fauxtable">(.*?)<div class="blocbas">', body, re.S)
    scope = table.group(1) if table else body
    for m in re.finditer(r'<div class="ligne"><div class="gauche">(.*?)</div>'
                         r'\s*<div class="droite">(.*?)</div>', scope, re.S):
        label, value_html = text_of(m.group(1)), m.group(2)
        value = text_of(value_html)
        if value:
            fields[label] = value
        # the catalogue hyperlinks component terms into « Composantes et modèles »
        links = [{"term": text_of(a.group(2)), "url": abs_url(a.group(1))}
                 for a in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', value_html, re.S)]
        if links:
            field_links[label] = links

    # --- photographs -----------------------------------------------------
    photos = []
    croquis = re.search(r'<img[^>]*class="croquisg"[^>]*src="([^"]+)"', body)
    if croquis:
        photos.append({"kind": "drawing", "source_url": abs_url(croquis.group(1))})

    # the two "hier / aujourd'hui" example strips, labelled by their <h4>
    for h4, strip in re.findall(r'<h4>(.*?)</h4>\s*<div class="blocthumbs1">(.*?)</div>',
                                body, re.S):
        heading = text_of(h4)
        kind = "historic" if "hier" in heading.lower() else "example"
        for a in re.finditer(r'<a[^>]*class="colorbox unthumb1[^"]*"[^>]*href="([^"]+)"', strip):
            photos.append({"kind": kind, "source_url": abs_url(a.group(1)),
                           "heading_fr": heading})

    # the avant/après « Exemple de mise en valeur » set
    for m in re.finditer(r'<div class="ombmise[^"]*">(.*?)</div>', body, re.S):
        frag = m.group(1)
        href = re.search(r'href="([^"]+)"', frag)
        desc = re.search(r'<span class="desc">(.*?)</span>', frag, re.S)
        if not (href and desc):
            continue
        label = text_of(desc.group(1))
        kind = PHOTO_KINDS.get(label.split()[0].upper())
        photos.append({"kind": kind or "example", "source_url": abs_url(href.group(1)),
                       "label_fr": label})

    # --- previous / next in the catalogue's own sequence ------------------
    nav = {}
    for rel in ("prev", "next"):
        m = re.search(rf'<a class="{rel}" href="[^"]*\?idfiche=(\d+)">(.*?)<img', body, re.S)
        if m:
            nav[rel] = {"fiche_id": int(m.group(1)), "name_fr": text_of(m.group(2))}

    return {
        "fiche_id": idf,
        "name_fr": name_fr,
        "slug": slugify(name_fr),
        "source_url": f"{BASE}?idfiche={idf}",
        "count_in_place": count,
        "count_approx": count_approx,
        "count_unit_fr": count_unit,
        "period_label": period,
        "fields": fields,          # verbatim French, label -> value
        "field_links": field_links,
        "photos": photos,
        "nav": nav,
    }


# --------------------------------------------------------------- validation
def check_cases(records: dict[int, dict]) -> list[str]:
    """The brief's two transcribed reference fiches, asserted field by field.

    Any mismatch means the catalogue markup changed under us and the parse can
    no longer be trusted; the caller should stop rather than publish.
    """
    expected = {
        10: {
            "name_fr": "Boomtown",
            "count_in_place": 100,
            "period_label": "1900-1930",
            "fields": {
                "Volumétrie": "1 à 2 étages",
                "Plan": "rectangulaire ou carré",
                "Toiture": "plate ou à très faible pente vers l'arrière",
                "Revêtements": "clin ou bardeau de bois, tuiles d'amiante-ciment en losange",
                "Ouvertures": "fenêtres à guillotine à carreaux, disposées symétriquement",
                "Saillies": "parapet ou corniche, galerie couverte",
                "Ornementation": "planches cornières et chambranles, éléments de corniche",
            },
            "prev": "Beaux-arts", "next": "Cubique",
        },
        1: {
            "name_fr": "Vernaculaire américain",
            "period_label": "1880-1940",
            "fields": {
                "Volumétrie": "1 ½ ou 2 étages, bien dégagé du sol",
                "Plan": "rectangulaire, parfois en « L »",
                "Toiture": "à 2 versants droits, en tôle à baguettes, pente moyenne à faible",
                "Revêtements": "clin ou bardeau de bois, tuiles d'amiante-ciment en losange",
                "Ouvertures": "fenêtres à battants à grands carreaux ou fenêtres à guillotine, "
                              "lucarne à pignon ou en appentis",
                "Saillies": "galerie couverte d'un auvent indépendant",
                "Ornementation": "chambranles, planches cornières, garnitures de galerie, "
                                 "retour de corniche",
            },
            "prev": "Victorien",
            "next": "Autre type : Bâtiment mixte ou à vocation commerciale",
        },
    }
    problems = []
    for idf, exp in expected.items():
        got = records.get(idf)
        if not got:
            problems.append(f"idfiche={idf}: not parsed at all")
            continue
        for key in ("name_fr", "period_label", "count_in_place"):
            if key in exp and got.get(key) != exp[key]:
                problems.append(f"idfiche={idf}: {key}: expected {exp[key]!r}, got {got.get(key)!r}")
        for label, want in exp["fields"].items():
            have = got["fields"].get(label)
            # compare on straight quotes so the source's ’ vs ' does not trip it
            if (have or "").replace("’", "'") != want.replace("’", "'"):
                problems.append(f"idfiche={idf}: {label}: expected {want!r}, got {have!r}")
        for rel in ("prev", "next"):
            have = (got["nav"].get(rel) or {}).get("name_fr")
            if have != exp[rel]:
                problems.append(f"idfiche={idf}: nav.{rel}: expected {exp[rel]!r}, got {have!r}")
    return problems


# -------------------------------------------------------------------- main
def main() -> int:
    index = parse_index((HTML / "index.html").read_text(encoding="utf-8"))
    records = {}
    for entry in index:
        idf = entry["fiche_id"]
        path = HTML / f"fiche-{idf}.html"
        if not path.exists():
            raise SystemExit(f"parse.py: missing {path}")
        rec = parse_fiche(path.read_text(encoding="utf-8"), idf)
        # the index carries the authoritative period label and listing order
        rec["index_period_label"] = entry["period_label"]
        rec["index_name_fr"] = entry["name_fr"]
        rec["index_order"] = index.index(entry) + 1
        missing = [f for f in FIELDS if f not in rec["fields"]]
        rec["missing_fields"] = missing
        records[idf] = rec

    problems = check_cases(records)
    for p in problems:
        print(f"parse.py: CHECK FAILED: {p}", file=sys.stderr)
    if problems:
        return 2

    payload = {
        "source": BASE,
        "courant_count": len(index),
        "fiche_ids": [e["fiche_id"] for e in index],
        "index": index,
        "fiches": [records[e["fiche_id"]] for e in index],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"parse.py: OK — {len(index)} courants parsed, check cases (idfiche 10, 1) pass "
          f"-> {OUT.relative_to(HERE.parent.parent)}")
    for r in payload["fiches"]:
        if r["missing_fields"]:
            print(f"  note: idfiche={r['fiche_id']} ({r['name_fr']}) has no "
                  + ", ".join(r["missing_fields"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
