#!/usr/bin/env python3
"""Parse Patri-Arch, *Étude typomorphologique de l'arrondissement du Sud-Ouest*
(rapport de synthèse, mise à jour octobre 2013) into structured records.

Run from anywhere:

    python3 sources/sud-ouest/parse.py

Inputs (produced by `pdftotext -layout`, see MANIFEST.md):
    sources/sud-ouest/txt/sud-ouest_typomorphologie.txt
    sources/sud-ouest/txt/12_evaluation_patrimoine_sud.txt

Outputs:
    sources/sud-ouest/parsed/types.json        one record per architectural type
    sources/sud-ouest/parsed/unites.csv        the unités de paysage, with type counts
    sources/sud-ouest/parsed/figures.csv       every figure caption, with its SO id
    sources/sud-ouest/parsed/profile_fr.yaml   ready-to-paste profile_fr blocks

Why a parser and not hand transcription: the fiche structure is rigidly
identical across the nineteen type fiches (A identification; B contexte de
développement et lieux d'occurrence; C.1 implantation; C.2 volumétrie;
C.3 matériaux de revêtement; C.4 traitement des façades; C.5 ouvertures;
D variantes), and it maps one-to-one onto this site's five profile columns.
C.4 is the interesting one: Patri-Arch divides every façade into a
socle / corps / couronnement triad, which no other source on this site does,
so the parser keeps that triad as three separate blocks rather than flattening
it into one paragraph.

The PDF is a two-column layout flattened by `pdftotext -layout`, so figure
captions land inside the body text. They are recognised by their own grammar
(a leading "Fig. n.n.n :", or a trailing "SOnnnn." / "UPn.n_Street_number"
photo-file id) and lifted out into figures.csv rather than discarded, because
they carry the study's own anchor addresses.
"""
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "sources" / "sud-ouest"
TXT = SRC / "txt"
OUT = SRC / "parsed"

TYPO = TXT / "sud-ouest_typomorphologie.txt"
EVAL = TXT / "12_evaluation_patrimoine_sud.txt"

# ---------------------------------------------------------------- page furniture
FURNITURE = [
    re.compile(r"^\s*Patri-Arch\s*(\d{1,3})?\s*$"),
    re.compile(r"^\s*(\d{1,3})\s+Patri-Arch\s*$"),
    re.compile(r"^\s*2013\s*$"),
    re.compile(r"^\s*Rapport de synthèse\s*$"),
    re.compile(r"^\s*Étude typomorphologique de l[’']arrondissement du Sud-Ouest\s*$"),
    re.compile(r"^\s*\d{1,3}\s*$"),
]
# a caption is a paragraph carrying one of these
CAPTION = re.compile(r"(^\s*Fig\.\s*\d)|(\bSO\d{4}\b)|(\bUP\d+\.\d+_)")
SO_ID = re.compile(r"\bSO(\d{4})\b")
UP_PHOTO = re.compile(r"\bUP(\d+\.\d+)_([^\s.]+)")
# "Voir la carte 2.6 en annexe 3" — a cross-reference, not content
CROSSREF = re.compile(r"^\s*Voir la carte [\d.]+ en annexe", re.I)

# type fiche headings: "1.1 La maison villageoise", "4  L'immeuble à vocation mixte",
# "5. L'immeuble à vocation commerciale" — the trailing dot is inconsistent in the source
TYPE_HEAD = re.compile(r"^\s{0,4}(\d(?:\.\d)?)\.?\s+(L[ae’'][^\n]{4,70})\s*$")
# family headings ("1. La maison unifamiliale") are the same shape with a dot
FAMILY_HEAD = re.compile(r"^\s{0,6}(\d)\.\s+(L[ae’'][^\n]{4,70})\s*$")

SECTIONS = [
    ("identification", re.compile(r"^\s*A\.?\s+IDENTIFICATION\s*$")),
    ("contexte", re.compile(r"^\s*B\.?\s+CONTEXTE DE DÉVELOPPEMENT")),
    ("_caract", re.compile(r"^\s*C\.?\s+CARACTÉRISTIQUES\s*$")),
    ("implantation", re.compile(r"^\s*C\.1\s+Implantation\s*$")),
    ("volumetrie", re.compile(r"^\s*C\.2\s+Volumétrie\s*$")),
    ("materiaux", re.compile(r"^\s*C\.3\s+Matériaux de revêtement\s*$")),
    ("traitement", re.compile(r"^\s*C\.4\s+Traitement (?:de la façade|des façades)\s*$")),
    ("ouvertures", re.compile(r"^\s*C\.5\s+Ouvertures\s*$")),
    ("variantes", re.compile(r"^\s*D\.?\s+VARIANTES\s*$")),
]
VARIANT_HEAD = re.compile(r"^\s*Variante\s+(\d+)\s*:\s*(.+?)\s*$")
UP_LIST_HEAD = re.compile(r"Unités de paysage pour lesquelles .*?figure comme type architectural\s*$"
                          r"|Unités de paysage pour lesquelles .*?figure comme type architectural\s+"
                          r"(principal|secondaire)\s*:")
UP_ROLE = re.compile(r"\b(principal|secondaire)\s*:\s*$")
# unité entries inside a two-column list: "2.6   Parc Marguerite-Bourgeoys      4.10   Square …"
# The lookahead re-splits the flattened gutter without cutting names that hold
# their own wide gaps.
UP_ENTRY = re.compile(r"(\d{1,2}\.\d{1,2})\s{2,}(\S.*?)(?=\s{4,}\d{1,2}\.\d{1,2}\s{2,}|\s*$)")


def norm(s):
    """Collapse whitespace and normalise the PDF's typographic quirks."""
    s = unicodedata.normalize("NFC", s)
    s = s.replace(" ", " ").replace("ﬁ", "fi").replace("ﬂ", "fl")
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)      # de-hyphenate across the wrap
    return re.sub(r"\s+", " ", s).strip()


def is_furniture(line):
    return any(p.match(line) for p in FURNITURE)


def paragraphs(lines):
    """Group lines into paragraphs; return [(text, raw_lines)] with furniture dropped."""
    out, buf = [], []
    for ln in lines:
        if is_furniture(ln) or not ln.strip():
            if buf:
                out.append(buf)
                buf = []
            continue
        buf.append(ln)
    if buf:
        out.append(buf)
    return out


def split_columns(line):
    """Split a -layout line at runs of 3+ spaces — the two-column gutter."""
    return [c for c in re.split(r"\s{3,}", line.strip()) if c]


# ---------------------------------------------------------------- load and slice
def load_typo():
    lines = TYPO.read_text(encoding="utf-8").splitlines()
    # the type fiches run from the "1. La maison unifamiliale" that follows the
    # synthèse (not the two table-of-contents echoes) to "ANNEXE 1"
    starts = [i for i, ln in enumerate(lines) if FAMILY_HEAD.match(ln)
              and "unifamiliale" in ln]
    body_start = starts[-1]
    body_end = next(i for i, ln in enumerate(lines) if ln.startswith("ANNEXE 1")
                    and i > body_start)
    return lines, body_start, body_end


def find_type_blocks(lines, lo, hi):
    """Return [(code, name_fr, start, end)] for every type fiche in the body."""
    heads = []
    for i in range(lo, hi):
        m = TYPE_HEAD.match(lines[i])
        if not m:
            continue
        code, name = m.group(1), norm(m.group(2))
        # a fiche heading is followed within four lines by its A IDENTIFICATION
        if not any(SECTIONS[0][1].match(lines[j]) for j in range(i + 1, min(i + 6, hi))):
            continue
        heads.append((code, name, i))
    blocks = []
    for n, (code, name, i) in enumerate(heads):
        end = heads[n + 1][2] if n + 1 < len(heads) else hi
        blocks.append((code, name, i, end))
    return blocks


def split_sections(lines, lo, hi):
    """Slice one fiche into its A/B/C.1–C.5/D sections."""
    marks = []
    for i in range(lo, hi):
        for key, pat in SECTIONS:
            if pat.match(lines[i]):
                marks.append((key, i))
                break
    out = {}
    for n, (key, i) in enumerate(marks):
        end = marks[n + 1][1] if n + 1 < len(marks) else hi
        out[key] = lines[i + 1:end]
    return out


# ---------------------------------------------------------------- section readers
def read_prose(lines, figures, code, section):
    """Return (paragraph texts, captions lifted out) for one section."""
    texts = []
    for para in paragraphs(lines):
        joined = "\n".join(para)
        if CAPTION.search(joined):
            cap = norm(" ".join(split_columns(" ".join(para))))
            for piece in re.split(r"(?=Fig\.\s*\d)", cap):
                piece = piece.strip()
                if not piece:
                    continue
                so = SO_ID.search(piece)
                up = UP_PHOTO.search(piece)
                figures.append({"type_code": code, "section": section, "caption": piece,
                                "so_id": ("SO" + so.group(1)) if so else "",
                                "unite": up.group(1) if up else ""})
            continue
        if CROSSREF.match(para[0]):
            continue
        text = norm(" ".join(para))
        if len(text) < 3:
            continue
        texts.append(text)
    return texts


def read_bullets(lines, figures, code, section):
    """Like read_prose but keeps the source's own bullet grouping.

    Patri-Arch marks sub-points with a leading bullet glyph that pdftotext turns
    into a stray '' or ''; those start a new paragraph even without a blank line.
    """
    out = []
    for para in paragraphs(lines):
        joined = "\n".join(para)
        if CAPTION.search(joined):
            cap = norm(" ".join(split_columns(" ".join(para))))
            for piece in re.split(r"(?=Fig\.\s*\d)", cap):
                piece = piece.strip()
                if not piece:
                    continue
                so = SO_ID.search(piece)
                figures.append({"type_code": code, "section": section, "caption": piece,
                                "so_id": ("SO" + so.group(1)) if so else "", "unite": ""})
            continue
        if CROSSREF.match(para[0]):
            continue
        chunk, buf = [], []
        for ln in para:
            if re.match(r"^\s*[●•]\s", ln) and buf:
                chunk.append(buf)
                buf = []
            buf.append(re.sub(r"^\s*[●•]\s*", "", ln))
        if buf:
            chunk.append(buf)
        for c in chunk:
            text = norm(" ".join(c))
            if len(text) > 2:
                out.append(text)
    return out


# Patri-Arch defines the three horizontal divisions of the façade on p. 17:
#   « Le socle est la partie basse de la façade. Il se limite généralement à la
#     fondation du bâtiment mais peut également inclure le rez-de-chaussée en
#     tout ou en partie. »
#   « Le corps est la partie centrale de la façade. »
#   « Le couronnement est la partie haute de la façade. […] Lorsque la toiture
#     est visible, elle est incluse dans le couronnement. »
# Every C.4 section is written in that order, so the parser labels each
# paragraph by whichever division its own vocabulary names FIRST, then forces
# the sequence to be non-decreasing: a paragraph can continue a division or
# move up, never back down.
DIVISION_ORDER = ["socle", "corps", "couronnement"]
DIVISION_KEYS = {
    "socle": re.compile(r"\bsocles?\b|\bfondations?\b"),
    "corps": re.compile(r"\bcorps\b|\bcompositions?\b|\btravées?\b|\balignements?\b"),
    "couronnement": re.compile(r"\bcouronn\w+|\bcornich\w+|\bparapets?\b"
                               r"|\bfausses? mansardes?\b|\bsolin\b|\bamortissements?\b"),
}


# Where a fiche writes all three divisions inside one paragraph (1.5 does), the
# triad is still there — it just has no paragraph breaks. Split on the sentence
# that opens with an explicit division phrase.
DIVISION_OPENER = re.compile(
    r"^(?:(?:Pour le|La composition du)\s+)?(?:Le\s+)?"
    r"(socle|corps|couronnement)\b|^La partie supérieure\b", re.I)
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀÂÉÈÊÎÔÙÛÇ«])")


def presplit(block):
    """Split one C.4 paragraph at its explicit socle/corps/couronnement openers."""
    sents = SENTENCE.split(block)
    marked = [i for i, s in enumerate(sents) if DIVISION_OPENER.match(s)]
    if len(marked) < 2:
        return [block]
    groups, buf = [], []
    for i, s in enumerate(sents):
        if i in marked and buf:
            groups.append(" ".join(buf))
            buf = []
        buf.append(s)
    if buf:
        groups.append(" ".join(buf))
    return groups


def split_triad(blocks):
    """Split C.4 into Patri-Arch's socle / corps / couronnement triad.

    A paragraph is labelled by the explicit division phrase it opens with; if it
    opens with none, by whichever division's vocabulary it uses most (ties going
    to whichever appears first). The sequence is then forced non-decreasing,
    because the study always writes the façade bottom-up.

    Paragraphs that name no division at all continue the one in force, except
    after the couronnement, where an unmarked paragraph is general ornament
    rather than more roofline: those go to `ornementation`, which this site
    renders in the same Articulation row.
    """
    triad = {"socle": [], "corps": [], "couronnement": [], "ornementation": []}
    rank = -1
    for raw in blocks:
        for b in presplit(raw):
            opener = DIVISION_OPENER.match(b)
            if opener and opener.group(1):
                named = opener.group(1).lower()
            elif opener:                       # "La partie supérieure du bâtiment…"
                named = "couronnement"
            else:
                scores = []
                for k in DIVISION_ORDER:
                    hits = list(DIVISION_KEYS[k].finditer(b))
                    if hits:
                        scores.append((-len(hits), hits[0].start(), k))
                named = min(scores)[2] if scores else None
            if named:
                rank = max(rank, DIVISION_ORDER.index(named))
                triad[DIVISION_ORDER[rank]].append(b)
            elif rank in (0, 1):
                triad[DIVISION_ORDER[rank]].append(b)
            else:
                triad["ornementation"].append(b)
    return triad


LABELS_FR = {"socle": "Socle", "corps": "Corps", "couronnement": "Couronnement",
             "ornementation": "Ornementation"}


def triad_as_bullets(triad):
    """Render the triad as this site's `profile_fr.traitement_des_facades` list.

    build.py takes profile_fr values as flat lists of strings, so the division
    name is carried as a label on each entry rather than as a nested key. The
    text after the label is the source's own, unaltered.
    """
    out = []
    for k in DIVISION_ORDER + ["ornementation"]:
        for b in triad[k]:
            out.append(f"{LABELS_FR[k]} — {b}")
    return out


def read_unites(lines):
    """Read the two 'Unités de paysage pour lesquelles …' lists in section B."""
    role, out = None, {"principal": [], "secondaire": []}
    for ln in lines:
        if is_furniture(ln):
            continue
        if "Unités de paysage" in ln and "type architectural" in ln:
            m = UP_ROLE.search(ln)
            role = m.group(1) if m else "pending"
            continue
        if role == "pending":
            m = UP_ROLE.search(ln)
            if m:
                role = m.group(1)
                continue
        if role in ("principal", "secondaire"):
            hits = list(UP_ENTRY.finditer(ln))
            if not hits:
                if ln.strip() and not ln.strip().startswith("Voir la carte"):
                    role = None
                continue
            for h in hits:
                out[role].append((h.group(1), norm(h.group(2))))
    return out


def read_variants(lines, figures, code):
    """Section D: '<n> variantes' with 'Variante n : <title>' + description."""
    variants, current, buf, preamble = [], None, [], []
    for para in paragraphs(lines):
        joined = "\n".join(para)
        if CAPTION.search(joined):
            cap = norm(" ".join(split_columns(" ".join(para))))
            so = SO_ID.search(cap)
            figures.append({"type_code": code, "section": "variantes", "caption": cap,
                            "so_id": ("SO" + so.group(1)) if so else "", "unite": ""})
            continue
        m = VARIANT_HEAD.match(para[0])
        if m:
            if current:
                variants.append({"n": current[0], "title_fr": current[1],
                                 "description_fr": " ".join(buf)})
            current, buf = (int(m.group(1)), norm(m.group(2))), []
            rest = norm(" ".join(para[1:]))
            if rest:
                buf.append(rest)
            continue
        text = norm(" ".join(para))
        if not text:
            continue
        if current:
            buf.append(text)
        else:
            preamble.append(text)
    if current:
        variants.append({"n": current[0], "title_fr": current[1],
                         "description_fr": " ".join(buf)})
    return variants, preamble


# ---------------------------------------------------------------- the évaluation cahier
def read_arrondissement_code():
    """Read the arrondissement number from INSIDE the cahier, never the filename.

    The Évaluation series numbers its files and its arrondissements on two
    different sequences: the Sud-Ouest cahier is file 12 and arrondissement 22,
    while file 22 is Saint-Laurent.  Every sector code in the document carries
    the arrondissement number as its first field, so the code is whatever
    prefix the document itself uses.
    """
    text = EVAL.read_text(encoding="utf-8")
    codes = re.findall(r"\b(\d{1,2})\.(E|I|N|U|AP)\.(\d{1,2})\b", text)
    prefixes = {}
    for a, letter, n in codes:
        prefixes.setdefault(a, 0)
        prefixes[a] += 1
    families = {}
    for a, letter, n in codes:
        families.setdefault(letter, set()).add(int(n))
    return prefixes, {k: sorted(v) for k, v in families.items()}


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines, lo, hi = load_typo()
    figures = []
    records = []
    for code, name_fr, start, end in find_type_blocks(lines, lo, hi):
        sec = split_sections(lines, start, end)
        ident = read_prose(sec.get("identification", []), figures, code, "identification")
        contexte = read_prose(sec.get("contexte", []), figures, code, "contexte")
        # the unité lists are prose-looking but are data; drop them from contexte
        contexte = [p for p in contexte
                    if not p.startswith("Unités de paysage pour lesquelles")
                    and not UP_ENTRY.match(p)]
        traitement_blocks = read_bullets(sec.get("traitement", []), figures, code, "traitement")
        rec = {
            "code": code,
            "name_fr": name_fr,
            "identification_fr": ident,
            "contexte_fr": contexte,
            "unites": read_unites(sec.get("contexte", [])),
            "profile_fr": {
                "implantation": read_prose(sec.get("implantation", []), figures, code, "implantation"),
                "volumetrie": read_prose(sec.get("volumetrie", []), figures, code, "volumetrie"),
                "materiaux": read_prose(sec.get("materiaux", []), figures, code, "materiaux"),
                "traitement_des_facades": traitement_blocks,
                "ouvertures": read_prose(sec.get("ouvertures", []), figures, code, "ouvertures"),
            },
            "traitement_triad": split_triad(traitement_blocks),
        }
        rec["variants"], rec["variants_preamble"] = read_variants(
            sec.get("variantes", []), figures, code)
        records.append(rec)

    (OUT / "types.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    with (OUT / "figures.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, ["type_code", "section", "so_id", "unite", "caption"])
        w.writeheader()
        for f in figures:
            w.writerow(f)

    # --- unités de paysage, assembled from every fiche's lieux d'occurrence list
    unites = {}
    for r in records:
        for role in ("principal", "secondaire"):
            for num, nm in r["unites"][role]:
                u = unites.setdefault(num, {"unite": num, "name_fr": nm,
                                            "principal": [], "secondaire": []})
                # the two-column flattening can pair a number with the wrong
                # name; keep the name seen most often
                u.setdefault("_names", []).append(nm)
                u[role].append(r["code"])
    for u in unites.values():
        names = u.pop("_names")
        u["name_fr"] = max(set(names), key=names.count)
        u["name_variants"] = sorted(set(names) - {u["name_fr"]})
    # The study's aire de paysage is the unité number's first field.  The five
    # names are the ones the méthodologie gives (p. 11); the assignment of each
    # number to a name is read off the unité names themselves — 2.x are all in
    # Pointe-Saint-Charles, 3.x all in Côte-Saint-Paul, and so on — and the
    # study confirms 3 = Côte-Saint-Paul in as many words on pp. 50 and 70.
    AIRES = {"1": "La Petite-Bourgogne", "2": "Pointe-Saint-Charles",
             "3": "Côte-Saint-Paul", "4": "Saint-Henri", "5": "Griffintown"}
    # The synthesis names a unité only where some architectural type occurs in
    # it, so its lists are not the full set.  The set IS recoverable: the
    # numbering is dense within each aire, and the highest number seen in each
    # (1.5, 2.14, 3.20, 4.17, 5.9) sums to 65 — the count the PIIA by-law
    # states independently ("5 aires de paysage divisées en 65 unités de
    # paysage distinctes").  So fill the gaps rather than publish 59.
    highest = {}
    for num in unites:
        a, b = num.split(".")
        highest[a] = max(highest.get(a, 0), int(b))
    rows = []
    for aire in sorted(AIRES):
        for i in range(1, highest[aire] + 1):
            num = f"{aire}.{i}"
            u = unites.get(num)
            rows.append({
                "unite": num,
                "aire": aire,
                "aire_name_fr": AIRES[aire],
                "name_fr": u["name_fr"] if u else "",
                "name_variants_fr": "; ".join(u["name_variants"]) if u else "",
                "types_principaux": " ".join(sorted(set(u["principal"]))) if u else "",
                "types_secondaires": " ".join(sorted(set(u["secondaire"]))) if u else "",
                "n_types": len(set(u["principal"]) | set(u["secondaire"])) if u else 0,
                "named_in_synthese": "oui" if u else "non",
            })
    with (OUT / "unites.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, ["unite", "aire", "aire_name_fr", "name_fr",
                                "name_variants_fr", "types_principaux",
                                "types_secondaires", "n_types", "named_in_synthese"])
        w.writeheader()
        w.writerows(rows)

    # --- ready-to-paste profile_fr blocks, in this site's key order
    import yaml
    blob = {}
    for r in records:
        p = dict(r["profile_fr"])
        p["traitement_des_facades"] = triad_as_bullets(r["traitement_triad"])
        blob[r["code"]] = {"name_fr": r["name_fr"], "profile_fr": p,
                           "triad": {k: v for k, v in r["traitement_triad"].items() if v},
                           "variants": r["variants"]}
    (OUT / "profile_fr.yaml").write_text(
        yaml.safe_dump(blob, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8")

    prefixes, families = read_arrondissement_code()
    print(f"types parsed: {len(records)} -> {[r['code'] for r in records]}")
    # families 1–3 are the residential ones; 4–7 are recorded but get no card
    res = [r for r in records if "." in r["code"]]
    triad_ok = sum(1 for r in res
                   if all(r["traitement_triad"][k] for k in ("socle", "corps", "couronnement")))
    partial = [r["code"] for r in res
               if not all(r["traitement_triad"][k] for k in ("socle", "corps", "couronnement"))]
    print(f"socle/corps/couronnement triad complete in {triad_ok}/{len(res)} residential fiches; "
          f"partial in {partial} (the source itself does not divide those façades)")
    named = sum(1 for r in rows if r["named_in_synthese"] == "oui")
    print(f"unités de paysage: {len(rows)} rows "
          f"({named} named in the synthèse, {len(rows) - named} number-only)")
    for aire in sorted(AIRES):
        n = sum(1 for r in rows if r["aire"] == aire)
        print(f"  aire {aire} {AIRES[aire]}: {n} unités")
    print(f"figure captions: {len(figures)}")
    print(f"arrondissement code, read from inside the cahier: {prefixes}")
    for k in sorted(families):
        print(f"  {k}: {len(families[k])} sectors, {families[k][0]}–{families[k][-1]}")


if __name__ == "__main__":
    main()
