#!/usr/bin/env python3
"""Québec Residential Typologies — static site builder.

Loads YAML from data/, validates it loudly, derives cross-references, and
renders the site into docs/ for GitHub Pages. See docs/methods for what is
verbatim and what is interpretive, and for the schema-additions log.
"""
import csv
import html
import io
import json
import re
import shutil
import struct
import sys
from pathlib import Path

import yaml
import markdown as md_lib
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
TPL = ROOT / "templates"
DOCS = ROOT / "docs"

SECTIONS = {  # key -> (letter, display name, colour key)
    "planned": ("A", "Planned communities", "p1"),
    "historic-core": ("B", "Historic cores", "p2"),
    "borough-vernacular": ("C", "Borough vernaculars", "p3"),
}
ENUM = {
    "tenure_plan": {"single-family", "semi-detached", "row", "duplex", "triplex", "walk-up", "slab", "mixed"},
    "roof.form": {"flat", "gabled", "gabled-multi", "hipped", "mansard", "false-mansard", "bellcast", "pyramidal", "shed",
                  "flat-or-false-mansard",  # Part 2a: Plateau duplex-setback
                  "gabled-or-hipped", "hipped-or-pyramidal", "flat-or-low-slope",  # Part 3: Saint-Lambert fiches
                  None},                        # Part 4a: Arvida families whose roof form is undocumented
    "window_proportion": {"vertical-2to1", "vertical", "square", "horizontal", "horizontal-2to1", "horizontal-2.5to1", None},
    "garage": {"none", "detached", "detached-or-set-back", "attached-set-back", "integrated-facade", "underground",
               "integrated-or-carport", None},  # integrated-or-carport: Part 3
    "photo.kind": {"strip", "single", "placeholder"},
}
TRAIT_LABELS = [
    ("siting_landscape", "Siting & landscape"),
    ("massing", "Massing"),
    ("articulation", "Articulation"),
    ("openings", "Openings"),
    ("materials", "Materials"),
]
# profile_fr keys (verbatim source French) aligned to the English profile rows;
# sous_variantes has no English counterpart and renders as its own row.
FR_KEYS = {
    "siting_landscape": ["implantation"],
    "massing": ["volumetrie", "volumes", "saillies"],
    "articulation": ["traitement_des_facades", "ornementation"],
    "openings": ["ouvertures"],
    "materials": ["materiaux"],
}
NUM_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def fail(msg):
    sys.exit(f"build.py: ERROR: {msg}")


def load_yaml(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except yaml.YAMLError as e:
        fail(f"{path}: invalid YAML: {e}")


def require(rec, keys, ctx):
    for k in keys:
        if k not in rec:
            fail(f"{ctx}: missing key '{k}'")


def check_enum(value, enum_key, ctx):
    if value not in ENUM[enum_key]:
        fail(f"{ctx}: '{value}' not a valid {enum_key} (allowed: {sorted(str(v) for v in ENUM[enum_key])})")


def jpeg_size(path):
    data = Path(path).read_bytes()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    fail(f"{path}: cannot read JPEG dimensions")


def split_headed_md(path, head_re):
    """Split a markdown file on `## <head>` lines; return {head: body_str}."""
    out, current, buf = {}, None, []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(\S+)\s*$", line)
        if m and re.match(head_re, m.group(1)):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current, buf = m.group(1), []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def paragraphs(text):
    return [" ".join(p.split()) for p in re.split(r"\n\s*\n", text) if p.strip()]


def pct(a, lo, hi):
    return round((a - lo) / (hi - lo) * 100, 2)


# ---------------------------------------------------------------- load canon
canon_types = load_yaml(DATA / "canon" / "canonical_types.yaml") or []
canon_styles = load_yaml(DATA / "canon" / "styles.yaml") or []
glossary = load_yaml(DATA / "canon" / "glossary.yaml") or []
for c in canon_types:
    require(c, ["id", "name_en", "definition_en"], "canonical_types.yaml")
    c["members"] = []
for s in canon_styles:
    require(s, ["id", "name_en", "span"], "styles.yaml")
    s["members"] = []
    s["members_by_place"] = {}
for g in glossary:
    require(g, ["term", "definition_en"], "glossary.yaml")
    g.setdefault("term_fr", None)
CANON = {c["id"]: c for c in canon_types}
STYLE = {s["id"]: s for s in canon_styles}
if len(CANON) != len(canon_types):
    fail("canonical_types.yaml: duplicate ids")
if len(STYLE) != len(canon_styles):
    fail("styles.yaml: duplicate ids")

section_essays = split_headed_md(DATA / "canon" / "sections.md", r"^section:")

# ---------------------------------------------------------------- load places
places = []
for pdir in sorted((DATA / "places").iterdir()):
    if not (pdir / "place.yaml").exists():
        continue
    ctx = f"{pdir.name}/place.yaml"
    pl = load_yaml(pdir / "place.yaml")
    require(pl, ["id", "name_en", "name_fr", "sections", "region", "founded", "settlement_mode",
                 "governing_instruments", "typology_document", "map_layer", "summary_en"], ctx)
    if pl["id"] != pdir.name:
        fail(f"{ctx}: id '{pl['id']}' does not match directory name '{pdir.name}'")
    for sec in pl["sections"]:
        if sec not in SECTIONS:
            fail(f"{ctx}: unknown section '{sec}'")
    require(pl["typology_document"], ["title", "year", "format"], f"{ctx}: typology_document")
    per_type_table = pl["typology_document"]["format"] == "per-type-table"

    phases = load_yaml(pdir / "phases.yaml")
    for ph in phases:
        require(ph, ["id", "label", "start", "end", "title_en", "colour_key"], f"{pdir.name}/phases.yaml")
        ph["years"] = f"{ph['start']} – {ph['end']}"
        ph["types"] = []
        ph.setdefault("summary_en", "")
    PH = {p["id"]: p for p in phases}

    sources = load_yaml(pdir / "sources.yaml")
    for s in sources:
        require(s, ["id", "citation", "used_for"], f"{pdir.name}/sources.yaml")

    prose_raw = split_headed_md(pdir / "prose.md", r"^(intro|phase:.+|notes|footer)$")
    prose = {
        "intro": paragraphs(prose_raw.get("intro", "")),
        "notes": paragraphs(prose_raw.get("notes", "")),
        "footer": paragraphs(prose_raw.get("footer", "")),
    }
    for ph in phases:
        key = f"phase:{ph['id']}"
        ph["essay"] = " ".join(paragraphs(prose_raw.get(key, ""))) if prose_raw.get(key) else ""

    sec_file = pdir / "sectors.yaml"
    sectors = load_yaml(sec_file) if sec_file.exists() else None
    if sectors:
        for s in sectors:
            require(s, ["id", "code", "name_fr", "value", "summary_en", "streets"], f"{pdir.name}/sectors.yaml")
            if s["value"] not in ("exceptional", "interesting", "urban-ensemble"):
                fail(f"{pdir.name}/sectors.yaml: {s['code']}: value must be exceptional|interesting|urban-ensemble")
        codes = [s["code"] for s in sectors]
        if len(codes) != len(set(codes)):
            fail(f"{pdir.name}/sectors.yaml: duplicate sector codes")
    pl["sectors"] = sectors
    SECTOR = {s["code"]: s for s in (sectors or [])}
    grading = pl.get("grading")
    if grading:
        require(grading, ["system", "categories"], f"{ctx}: grading")
        for c in grading["categories"]:
            require(c, ["code", "label_fr", "count"], f"{ctx}: grading.categories")
    pl.setdefault("grading", None)

    types = []
    for tf in sorted((pdir / "types").glob("*.yaml")):
        tctx = f"{pdir.name}/types/{tf.name}"
        t = load_yaml(tf)
        require(t, ["id", "place", "phase", "name_en", "name_fr", "source_ref", "canonical", "styles",
                    "tenure_plan", "storeys", "roof", "window_proportion", "principal_cladding", "roofing",
                    "garage", "lot_width_m", "setback_front_m", "setback_side_m", "front_yard_green_pct",
                    "profile", "profile_note", "blurb_en", "origin_en", "photos"], tctx)
        slug = tf.stem
        if t["id"] != f"{pl['id']}.{slug}":
            fail(f"{tctx}: id '{t['id']}' should be '{pl['id']}.{slug}'")
        if t["place"] != pl["id"]:
            fail(f"{tctx}: place '{t['place']}' does not match '{pl['id']}'")
        if t["phase"] not in PH:
            fail(f"{tctx}: unknown phase '{t['phase']}'")
        for cid in t["canonical"]:
            if cid not in CANON:
                fail(f"{tctx}: unknown canonical id '{cid}'")
        for sid in t["styles"]:
            if sid not in STYLE:
                fail(f"{tctx}: unknown style id '{sid}'")
        require(t["roof"], ["form", "pitch_deg"], f"{tctx}: roof")
        check_enum(t["tenure_plan"], "tenure_plan", tctx)
        check_enum(t["roof"]["form"], "roof.form", tctx)
        check_enum(t["window_proportion"], "window_proportion", tctx)
        check_enum(t["garage"], "garage", tctx)
        for key, _label in TRAIT_LABELS:
            if key not in t["profile"] or not isinstance(t["profile"][key], list):
                fail(f"{tctx}: profile missing list '{key}'")
        if not per_type_table and not t.get("profile_note"):
            fail(f"{tctx}: profile_note is required when typology_document.format != per-type-table")
        if not t["photos"]:
            fail(f"{tctx}: needs at least one photo record")
        for p in t["photos"]:
            require(p, ["file", "credit", "kind"], f"{tctx}: photos")
            check_enum(p["kind"], "photo.kind", f"{tctx}: photos")
            if p["kind"] != "placeholder" and not (ROOT / p["file"]).exists():
                fail(f"{tctx}: photo file not found: {p['file']}")

        pfr = t.get("profile_fr")
        if pfr is not None and not isinstance(pfr, dict):
            fail(f"{tctx}: profile_fr must be a mapping of lists")
        for ck in ("conservation", "conservation_fr"):
            if t.get(ck) is not None and not isinstance(t[ck], list):
                fail(f"{tctx}: {ck} must be a list")
        t.setdefault("conservation", None)
        t.setdefault("conservation_fr", None)
        t.setdefault("models_observed", None)
        t.setdefault("sectors", None)
        if t["sectors"] is not None:
            if not isinstance(t["sectors"], list):
                fail(f"{tctx}: sectors must be a list of sector codes")
            for code in t["sectors"]:
                if code not in SECTOR:
                    fail(f"{tctx}: unknown sector code '{code}' (not in {pdir.name}/sectors.yaml)")
            t["sector_objs"] = [SECTOR[c] for c in t["sectors"]]
        else:
            t["sector_objs"] = []
        t.setdefault("display_order", None)
        if t.get("models_observed") is not None and not isinstance(t["models_observed"], list):
            fail(f"{tctx}: models_observed must be a list of model codes")
        pc = t.setdefault("phase_confidence", None)
        if pc not in (None, "verified", "provisional"):
            fail(f"{tctx}: phase_confidence must be 'verified' or 'provisional', got {pc!r}")
        csv_rel = t.setdefault("model_addresses_csv", None)
        if csv_rel and not (ROOT / csv_rel).exists():
            fail(f"{tctx}: model_addresses_csv not found: {csv_rel}")
        # derived display fields
        t["slug"] = slug
        t["place_name"] = pl["name_en"]
        t["phase_obj"] = PH[t["phase"]]
        t["doc_short"] = t["source_ref"].split(",")[0].strip()
        t.setdefault("source_generation", None)
        m = re.search(r"art\.\s*(\d+)", t["source_ref"])
        t["art_no"] = int(m.group(1)) if m else None
        # eyebrow: the by-law article where there is one, else a short ref (the
        # full source_ref always shows in the card's metaline)
        t["eyebrow_ref"] = (f"By-law art. {t['art_no']}" if (m and "y-law" in t["doc_short"])
                            else t["source_ref"] if len(t["source_ref"]) <= 60 else t["doc_short"])
        # ordering within the source document: by-law article, fiche x.y, or family n
        if t["art_no"] is not None:
            t["src_order"] = float(t["art_no"])
        elif (mf := re.search(r"fiche\s+(\d+)(?:\.(\d+))?", t["source_ref"])):
            t["src_order"] = int(mf.group(1)) + int(mf.group(2) or 0) / 100
        elif (mg := re.search(r"family\s+(\d+)", t["source_ref"])):
            t["src_order"] = float(mg.group(1))
        else:
            t["src_order"] = None
        t["profile_rows"] = [{"label": label, "bullets": t["profile"][key],
                              "fr": [v for fk in FR_KEYS[key] for v in (pfr or {}).get(fk, [])]}
                             for key, label in TRAIT_LABELS]
        if pfr and pfr.get("sous_variantes"):
            t["profile_rows"].append({"label": "Sous-variantes", "bullets": [], "fr": pfr["sous_variantes"]})
        t["canonical_objs"] = [CANON[c] for c in t["canonical"]]
        t["style_objs"] = [STYLE[s] for s in t["styles"]]
        t.setdefault("style_label", " / ".join(s["name_en"] for s in t["style_objs"]))
        t.setdefault("aliases", [])
        enriched = []
        for p in t["photos"]:
            if p["kind"] != "placeholder":
                w, h = jpeg_size(ROOT / p["file"])
            else:
                w, h = None, None
            n_photos = "Three photographs" if p["kind"] == "strip" else "Photograph"
            enriched.append(dict(p, w=w, h=h,
                alt=f"{n_photos} of {t['name_en']} houses in {pl['name_en']}, from {t['doc_short']}"))
        t["photos"] = enriched
        t["photo"] = enriched[0]
        types.append(t)

    # order types the way the source document orders them
    phase_order = {p["id"]: i for i, p in enumerate(phases)}
    # explicit display_order (Part 4a) wins; otherwise phase order then source-document order
    types.sort(key=lambda t: (
        0 if t["display_order"] is not None else 1,
        t["display_order"] or 0,
        phase_order[t["phase"]],
        t["src_order"] if t["src_order"] is not None else 10**6,
        t["name_en"],
    ))
    for t in types:
        PH[t["phase"]]["types"].append(t)

    # place-level timeline (header rail)
    p_min, p_max = phases[0]["start"], phases[-1]["end"]
    stops = []
    for ph in phases:
        a, b = pct(ph["start"], p_min, p_max), pct(ph["end"], p_min, p_max)
        stops.append(f"var(--{ph['colour_key']}) {a:g}% {b:g}%")
    pl["rail_gradient"] = "linear-gradient(90deg," + ",".join(stops) + ")"
    pl["rail_years"] = [ph["start"] for ph in phases] + [phases[-1]["end"]]
    n = len(phases)
    pl["rail_aria"] = f"Timeline {p_min} to {p_max} divided into {NUM_WORDS.get(n, n)} phases"
    pl["phase_span"] = f"{p_min}–{p_max}"
    fam_file = pdir / "model_families_summary.yaml"
    pl["model_families"] = load_yaml(fam_file) if fam_file.exists() else None
    if pl["model_families"]:
        pl["model_families_csv"] = f"data/{pl['id']}-models-addresses.csv"
    hero = pl.get("hero_photo")
    if hero:
        require(hero, ["file", "credit"], f"{ctx}: hero_photo")
        if not (ROOT / hero["file"]).exists():
            fail(f"{ctx}: hero_photo file not found: {hero['file']}")
        hero["w"], hero["h"] = jpeg_size(ROOT / hero["file"])
    pl.setdefault("hero_photo", None)
    pl["phases"] = phases
    pl["sources_list"] = sources
    pl["sources"] = sources
    pl["prose"] = prose
    pl["types"] = types
    places.append(pl)

PLACE = {p["id"]: p for p in places}
all_types = [t for p in places for t in p["types"]]
TYPE = {t["id"]: t for t in all_types}

# ------------------------------------------------------- derive cross-links
for t in all_types:
    for cid in t["canonical"]:
        CANON[cid]["members"].append(t)
    for sid in t["styles"]:
        STYLE[sid]["members"].append(t)
        STYLE[sid]["members_by_place"].setdefault(t["place"], []).append(t)


EN_PREPS = {"with", "without", "of", "in", "to", "at", "for"}
FR_ARTICLES = {"le", "la", "les", "l'", "un", "une", "des"}


def head_en(t):
    words = t["name_en"].split()
    for i, w in enumerate(words):
        if w.lower() in EN_PREPS:
            words = words[:i]
            break
    return re.sub(r"[^\w-]", "", words[-1]).lower()


def head_fr(t):
    words = [w for w in t["name_fr"].split() if w.lower() not in FR_ARTICLES]
    w0 = re.sub(r"^[LlDd]'", "", words[0]) if words else ""
    return re.sub(r"[^\w-]", "", w0).lower()


for t in all_types:
    heads = {head_en(t), head_fr(t)} | {a.lower() for a in t["aliases"]}
    same_word = [o for o in all_types if o["id"] != t["id"]
                 and heads & ({head_en(o), head_fr(o)} | {a.lower() for a in o["aliases"]})]
    same_form = [o for o in all_types if o["id"] != t["id"] and set(t["canonical"]) & set(o["canonical"])]
    tp = t["phase_obj"]
    same_period = [o for o in all_types if o["place"] != t["place"]
                   and o["phase_obj"]["start"] <= tp["end"] + 10 and o["phase_obj"]["end"] >= tp["start"] - 10]
    same_style = [o for o in all_types if o["id"] != t["id"] and set(t["styles"]) & set(o["styles"])]
    t["xlinks"] = [
        {"label": "Same word elsewhere", "entries": same_word},
        {"label": "Same form elsewhere", "entries": same_form},
        {"label": "Same period elsewhere", "entries": same_period},
        {"label": "Same style elsewhere", "entries": same_style},
    ]

# global timeline bounds (all places)
g_min = min(p["phases"][0]["start"] for p in places)
g_max = max(p["phases"][-1]["end"] for p in places)
ax_min = g_min - (g_min % 25)
ax_max = g_max + ((25 - g_max % 25) % 25)
tl_ticks = [{"year": y, "major": y % 50 == 0} for y in range(ax_min, ax_max + 1, 25)]
tl_intervals = len(tl_ticks) - 1
for p in places:
    for ph in p["phases"]:
        ph["tl_left"] = pct(ph["start"], ax_min, ax_max)
        ph["tl_width"] = round(pct(ph["end"], ax_min, ax_max) - pct(ph["start"], ax_min, ax_max), 2)

# sections
sections = []
for key, (letter, name, colour) in SECTIONS.items():
    essay_md = section_essays.get(f"section:{key}", "")
    sections.append({
        "key": key, "letter": letter, "name": name, "colour_key": colour,
        "essay_html": md_lib.markdown(essay_md) if essay_md else "<p>Essay to come.</p>",
        "teaser": paragraphs(essay_md)[0] if essay_md else "",
        "places": [p for p in places if key in p["sections"]],
    })

# style span-bar axis
s_min = min(s["span"][0] for s in canon_styles)
s_max = max(s["span"][1] for s in canon_styles)
for s in canon_styles:
    s["axis_min"], s["axis_max"] = s_min, s_max
    s["span_left"] = pct(s["span"][0], s_min, s_max)
    s["span_width"] = round(pct(s["span"][1], s_min, s_max) - pct(s["span"][0], s_min, s_max), 2)

# ---------------------------------------------------------------- render
env = Environment(loader=FileSystemLoader(TPL), undefined=StrictUndefined,
                  autoescape=False, trim_blocks=False, lstrip_blocks=False)
env.filters["esc"] = lambda s: html.escape(str(s), quote=False)
env.filters["dash"] = lambda v: "–" if v in (None, "", []) else v
env.filters["deg"] = lambda v: "–" if v is None else f"{v}°"
env.filters["num_m"] = lambda v: "–" if v is None else f"{v} m"
env.filters["pct"] = lambda v: "–" if v is None else f"{v} %"
env.filters["range_m"] = lambda v: "–" if not v else f"{v[0]}–{v[1]} m"
env.filters["joinlist"] = lambda v: "–" if not v else ", ".join(v)

if DOCS.exists():
    shutil.rmtree(DOCS)
DOCS.mkdir(parents=True)

SITE = "Québec Residential Typologies"
pages_written = 0


def render(template, out_rel, depth, **ctx):
    global pages_written
    out = DOCS / out_rel
    out.parent.mkdir(parents=True, exist_ok=True)
    ctx.setdefault("nav", "")
    ctx["R"] = "../" * depth
    out.write_text(env.get_template(template).render(**ctx), encoding="utf-8")
    pages_written += 1


render("home.html", "index.html", 0, title=SITE,
       description="Residential building types across Québec, place by place: local typologies from by-laws, inventories and studies, cross-referenced by form, style and period.",
       places=places, sections=sections, tl_ticks=tl_ticks, tl_intervals=tl_intervals)

for sec in sections:
    render("section.html", f"sections/{sec['key']}/index.html", 2,
           title=f"{sec['name']} — {SITE}", description=sec["teaser"] or sec["name"], sec=sec)

for p in places:
    render("place.html", f"places/{p['id']}/index.html", 2,
           title=f"Residential Architectural Styles of {p['name_en']}",
           description=p["summary_en"], pl=p)

for t in all_types:
    render("type.html", f"types/{t['id']}/index.html", 2,
           title=f"{t['name_en']} ({t['place_name']}) — {SITE}",
           description=t["blurb_en"][:220], t=t)

for c in canon_types:
    render("canonical.html", f"canonical/{c['id']}/index.html", 2,
           title=f"{c['name_en']} — {SITE}", description=c["definition_en"], c=c)

for s in canon_styles:
    render("style.html", f"styles/{s['id']}/index.html", 2,
           title=f"{s['name_en']} — {SITE}",
           description=f"{s['name_en']}, {s['span'][0]}–{s['span'][1]}: local residential types carrying the style.", s=s)

render("matrix.html", "matrix/index.html", 1, title=f"Style ↔ place matrix — {SITE}",
       description="Which places carry which styles, as a sortable matrix of local types.",
       styles=canon_styles, places=places, nav="matrix")
render("compare.html", "compare/index.html", 1, title=f"Compare types — {SITE}",
       description="Side-by-side comparison of two to four local residential types.", nav="compare")
render("glossary.html", "glossary/index.html", 1, title=f"Glossary — {SITE}",
       description="Terms used by the by-laws, inventories and studies this site draws on.",
       glossary=glossary, nav="glossary")
render("methods.html", "methods/index.html", 1, title=f"Methods — {SITE}",
       description="What is verbatim, what is interpretive, how nulls and photographs are handled, and the schema-additions log.",
       nav="methods")

# ------------------------------------------------------------- data exports
flat = []
for t in all_types:
    flat.append({
        "id": t["id"], "place": t["place"], "place_name": t["place_name"],
        "phase": t["phase"], "phase_label": t["phase_obj"]["label"],
        "phase_years": t["phase_obj"]["years"], "phase_title": t["phase_obj"]["title_en"],
        "name_en": t["name_en"], "name_fr": t["name_fr"], "source_ref": t["source_ref"],
        "canonical": t["canonical"], "canonical_names": [c["name_en"] for c in t["canonical_objs"]],
        "styles": t["styles"], "style_names": [s["name_en"] for s in t["style_objs"]],
        "style_label": t["style_label"], "tenure_plan": t["tenure_plan"], "storeys": t["storeys"],
        "roof": t["roof"], "window_proportion": t["window_proportion"],
        "principal_cladding": t["principal_cladding"], "roofing": t["roofing"], "garage": t["garage"],
        "lot_width_m": t["lot_width_m"], "setback_front_m": t["setback_front_m"],
        "setback_side_m": t["setback_side_m"], "front_yard_green_pct": t["front_yard_green_pct"],
        "profile": t["profile"], "profile_fr": t.get("profile_fr"), "profile_note": t["profile_note"],
        "conservation": t["conservation"], "conservation_fr": t["conservation_fr"],
        "models_observed": t["models_observed"], "phase_confidence": t["phase_confidence"],
        "sectors": t["sectors"],
        "source_generation": t["source_generation"],
        "blurb_en": t["blurb_en"], "origin_en": t["origin_en"],
        "photo": t["photo"], "url": f"types/{t['id']}/",
    })
(DOCS / "data.json").write_text(json.dumps({"site": SITE, "part": 1, "types": flat},
                                           ensure_ascii=False, indent=1), encoding="utf-8")

csv_buf = io.StringIO()
cw = csv.writer(csv_buf)
cw.writerow(["id", "place", "place_name", "phase", "phase_years", "phase_title", "name_en", "name_fr",
             "source_ref", "source_generation", "canonical", "styles", "style_label", "tenure_plan", "storeys", "roof_form",
             "roof_pitch_deg", "window_proportion", "principal_cladding", "roofing", "garage",
             "lot_width_min_m", "lot_width_max_m", "setback_front_m", "setback_side_m",
             "front_yard_green_pct", "siting_landscape", "massing", "articulation", "openings",
             "materials", "conservation", "models_observed", "phase_confidence", "sectors",
             "blurb_en", "origin_en", "photo_file", "photo_credit"])
for t in all_types:
    cw.writerow([
        t["id"], t["place"], t["place_name"], t["phase"], t["phase_obj"]["years"],
        t["phase_obj"]["title_en"], t["name_en"], t["name_fr"], t["source_ref"], t["source_generation"],
        "; ".join(t["canonical"]), "; ".join(t["styles"]), t["style_label"], t["tenure_plan"],
        t["storeys"], t["roof"]["form"], t["roof"]["pitch_deg"], t["window_proportion"],
        "; ".join(t["principal_cladding"]), t["roofing"], t["garage"],
        t["lot_width_m"][0] if t["lot_width_m"] else None,
        t["lot_width_m"][1] if t["lot_width_m"] else None,
        t["setback_front_m"], t["setback_side_m"], t["front_yard_green_pct"],
        " | ".join(t["profile"]["siting_landscape"]), " | ".join(t["profile"]["massing"]),
        " | ".join(t["profile"]["articulation"]), " | ".join(t["profile"]["openings"]),
        " | ".join(t["profile"]["materials"]), " | ".join(t["conservation"] or []),
        "; ".join(t["models_observed"] or []), t["phase_confidence"], "; ".join(t["sectors"] or []),
        t["blurb_en"], t["origin_en"],
        t["photo"]["file"], t["photo"]["credit"],
    ])
(DOCS / "data.csv").write_text(csv_buf.getvalue(), encoding="utf-8")

# ------------------------------------------------------------ static assets
shutil.copy(TPL / "base.css", DOCS / "base.css")
shutil.copy(TPL / "app.js", DOCS / "app.js")
shutil.copytree(ROOT / "assets", DOCS / "assets")
for p in places:                       # publish each place's address list beside the data exports
    if p.get("model_families"):
        (DOCS / "data").mkdir(exist_ok=True)
        shutil.copy(ROOT / p["types"][0]["model_addresses_csv"], DOCS / p["model_families_csv"])
(DOCS / ".nojekyll").touch()

print(f"build.py: OK — {len(places)} place(s), {len(all_types)} types, {len(canon_types)} canonical forms, "
      f"{len(canon_styles)} styles, {pages_written} pages -> docs/")
