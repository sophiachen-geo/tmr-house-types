#!/usr/bin/env python3
"""Parse the MRC de L'Île-d'Orléans / Patri-Arch inventory synthesis by page anchor.

Inputs : sources/ile-orleans/inventaire_synthese.pdf
         sources/ile-orleans/inventaire_synthese.txt
           (`pdftotext -layout inventaire_synthese.pdf inventaire_synthese.txt`)

The synthesis devotes a fixed pair of pages to each of eleven *courants architecturaux*:
a left-hand page of narrative that ends in a bulleted "Principaux éléments
caractéristiques" list, and a right-hand plate of captioned photographs carrying the
inventory's own example addresses. This script pulls both, plus the quantitative
diagnostic (composition de l'inventaire) on p. 47, so the encoding in
data/places/ile-orleans/ can be regenerated rather than retyped.

    python3 sources/ile-orleans/parse.py            # human-readable dump
    python3 sources/ile-orleans/parse.py --json     # machine-readable

Two things the naive reading gets wrong, and how this handles them:

* The photo plates are set in two columns. `pdftotext -layout` interleaves them on a
  single line, welding the left caption's street to the right caption's municipality
  ("1347 chemin Sainte-Famille. Royal, Saint-Jean"). Each plate is therefore
  re-extracted twice, cropped to the left and right half of the A4 page, so captions
  stay whole.
* Three courant headings are set with a word repeated on two lines ("Principaux
  éléments / éléments caractéristiques :"). The heading detector spans lines.

Note on page anchors: the PDF's page images and its printed folios agree throughout
this document, so "page 26" means both. Three of the anchors quoted in the Part 9
brief are off against the file downloaded 2026-08-17 — cottage vernaculaire américain
is on 36 (not 35), maison Boomtown on 40 (not 39) and régionalisme québécois on 44
(not 43). The anchors below are the observed ones.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PDF = HERE / "inventaire_synthese.pdf"
TXT = HERE / "inventaire_synthese.txt"
PAGE_W, PAGE_H = 595, 842          # A4, per pdfinfo

# slug -> (narrative + bullet list page, captioned photo plate page, printed heading)
COURANTS = [
    ("maison-inspiration-francaise",      26, 27, "La maison d'inspiration française"),
    ("maison-traditionnelle-quebecoise",  28, 29, "La maison traditionnelle québécoise d'influence néoclassique"),
    ("second-empire-maison-mansardee",    30, 31, "Le style Second Empire et la maison à mansarde"),
    ("cottage-regency",                   32, 33, "Le cottage Regency"),
    ("eclectisme-victorien",              34, 35, "L'éclectisme victorien"),
    ("cottage-vernaculaire-americain",    36, 37, "Le cottage vernaculaire américain"),
    ("maison-cubique",                    38, 39, "La maison cubique"),
    ("maison-boomtown",                   40, 41, "La maison Boomtown"),
    ("arts-and-crafts",                   42, 43, "L'architecture Arts & Crafts"),
    ("regionalisme-quebecois",            44, 45, "Le régionalisme québécois"),
    ("modernisme",                        46, None, "Le modernisme"),   # plate is inline on p.46
]

# the running head/foot Patri-Arch prints on every page
FOOTER = re.compile(r"(PATRI.ARCH|MISE À JOUR DE L'INVENTAIRE|Rapport de synthèse|^\s*\d{1,3}\s*$)")
HEAD_START = re.compile(r"^\s*Principaux\b", re.I)
HEAD_END = re.compile(r"caractéristiques\s*:", re.I)
# a divider page sets the courant name in caps above the real heading; skip it
DIVIDER = re.compile(r"^[A-ZÀ-Ü\s’'&-]{6,}$")
BULLET = re.compile(r"^\s*[••]\s*(.*)$")
# "sise au 3463, chemin Royal à Sainte-Famille." / "au 12, rue Gagnon à Sainte-Pétronille."
ADDRESS = re.compile(
    r"(\d+[A-Za-z]?(?:-\d+)*),\s+((?:chemin|rue|avenue|route|côte)\s+[^,]*?)\s+à\s+"
    r"(Sainte-[\w’'\-]+|Saint-[\w’'\-]+)", re.I)


def pages():
    if not TXT.exists():
        sys.exit(f"parse.py: {TXT} not found — run pdftotext -layout first")
    # pdftotext emits a form feed between pages; page N is index N-1
    return TXT.read_text(encoding="utf-8").split("\f")


def column_text(page_no, half):
    """Re-extract one page cropped to its left or right column."""
    if not shutil.which("pdftotext") or not PDF.exists():
        return ""
    x = 0 if half == "left" else PAGE_W // 2 - 5
    out = subprocess.run(
        ["pdftotext", "-layout", "-f", str(page_no), "-l", str(page_no),
         "-x", str(x), "-y", "0", "-W", str(PAGE_W // 2 + 5), "-H", str(PAGE_H),
         str(PDF), "-"],
        capture_output=True, text=True, check=True)
    return out.stdout


def clean(line):
    """Collapse the layout mode's runs of spaces; drop the running head/foot."""
    line = " ".join(line.split())
    return "" if not line or FOOTER.search(line) else line


def head_index(lines):
    """Index of the last line of the 'Principaux éléments caractéristiques' heading."""
    for i, l in enumerate(lines):
        if HEAD_START.search(l):
            # the heading wraps over at most two lines
            for j in (i, i + 1):
                if j < len(lines) and HEAD_END.search(lines[j]):
                    return j
            return i
    return None


def elements_caracteristiques(page):
    """The bulleted list that closes each courant block, one string per bullet.

    Bullets wrap over two or three physical lines, so a line that does not open
    with • continues the bullet above it. Captions printed below the list (p. 46)
    are not bulleted and are dropped with the trailing-continuation guard.
    """
    lines = page.splitlines()
    start = head_index(lines)
    if start is None:
        return []
    out, open_bullet = [], False
    for raw in lines[start + 1:]:
        line = clean(raw)
        if not line:
            # A blank line closes the current bullet. This is what separates the list
            # from the photo caption printed below it on p. 46; bullets themselves
            # always wrap onto contiguous lines.
            open_bullet = False
            continue
        m = BULLET.match(raw.strip())
        if m:
            out.append(" ".join(m.group(1).split()))
            open_bullet = True
        elif open_bullet:
            out[-1] += " " + line
    out = [re.sub(r"(\w)-\s+(\w)", r"\1-\2", b) for b in out]   # rejoin line-break hyphens
    return [re.sub(r"\s*;\s*$", "", b).strip() for b in out if b.strip()]


def narrative(page):
    """Heading and running text above the 'Principaux éléments' list."""
    lines = page.splitlines()
    stop = head_index(lines)
    body = [l for l in (clean(l) for l in lines[:stop if stop is not None else len(lines)]) if l]
    while body and DIVIDER.match(body[0]):       # p.44 opens with a caps divider
        body.pop(0)
    return (body[0] if body else ""), " ".join(body[1:])


def distribution(text):
    """The one sentence in each block that says how common the courant is here."""
    how = re.compile(r"(représenté|représentée|abondant|abondantes|bien présent|rare|"
                     r"peu d’exemples|quelques cas|quelques exemplaires|exemplaires|"
                     r"répertorié|comporte peu|peu représenté)", re.I)
    where = re.compile(r"(île d’Orléans|île d'Orléans|Île-d’Orléans|Île-d'Orléans|"
                       r"site patrimonial|municipalit|inventaire)", re.I)
    for sent in re.split(r"(?<=[.;])\s+", text):
        if how.search(sent) and where.search(sent):
            return sent.strip()
    return None


def example_addresses(page_no):
    """Addresses printed in the photo-plate captions, de-duplicated, in reading order.

    Read column by column so a caption is never welded to its neighbour's.
    """
    if page_no is None:
        return []
    seen, out = set(), []
    for half in ("left", "right"):
        flat = " ".join(column_text(page_no, half).split())
        flat = re.sub(r"-\s+", "-", flat)          # rejoin captions hyphenated at a line break
        for num, street, muni in ADDRESS.findall(flat):
            street = " ".join(street.split()).rstrip(".").strip()
            muni = muni.replace("’", "'")
            key = (num.lower(), street.lower(), muni)
            if key in seen:
                continue
            seen.add(key)
            out.append({"address": f"{num} {street}", "municipality": muni})
    return out


def diagnostic(all_pages):
    """Table 1 on p. 47: inventoried buildings by municipality and by cote A-E."""
    lines = [" ".join(l.split()) for l in all_pages[46].splitlines()]
    rows = {}
    for i, line in enumerate(lines):
        m = re.match(r"^(Sainte?-[\w’'\-]+)\s+((?:\d+\s*){6,})$", line)
        if not m:
            continue
        nums = [int(n) for n in m.group(2).split()]
        # Some rows wrap: the right-aligned total is echoed on the next line and the
        # "supprimé" figure printed beside it. Absorb a bare numeric continuation.
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if re.fullmatch(r"(?:\d+\s*){1,2}", nxt or "x"):
            nums += [int(n) for n in nxt.split()]
        a, b, c, d, e = nums[:5]
        total = a + b + c + d + e
        tail = [n for n in nums[5:] if n != total]   # drop the echoed total(s)
        rows[m.group(1).replace("’", "'")] = {
            "A": a, "B": b, "C": c, "D": d, "E": e,
            "total": total, "supprime": tail[-1] if tail else None}
    counts = {k: sum(v[k] for v in rows.values()) for k in "ABCDE"}
    counts["total"] = sum(counts[k] for k in "ABCDE")
    counts["supprime"] = sum(v["supprime"] or 0 for v in rows.values())
    return {"by_municipality": rows, "counts": counts}


def main():
    all_pages = pages()
    result = {"pdf_pages": len(all_pages) - 1, "courants": [],
              "diagnostic": diagnostic(all_pages)}
    for slug, p_text, p_photos, expect in COURANTS:
        page = all_pages[p_text - 1]
        title, body = narrative(page)
        norm = lambda s: s.replace("’", "'").lower()
        result["courants"].append({
            "slug": slug, "page": p_text, "photo_page": p_photos,
            "title_found": title, "title_expected": expect,
            "title_matches": norm(title) == norm(expect),
            "elements_caracteristiques": elements_caracteristiques(page),
            "distribution": distribution(body),
            "example_addresses": example_addresses(p_photos),
        })
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return
    bad = 0
    for c in result["courants"]:
        flag = "" if c["title_matches"] else f"   [!! expected {c['title_expected']!r}]"
        print(f"\n=== p.{c['page']:>2}  {c['slug']}{flag}")
        print(f"    {c['title_found']}")
        print(f"    distribution: {c['distribution'] or '(none found)'}")
        if not c["elements_caracteristiques"]:
            print("    !! NO 'Principaux éléments caractéristiques' LIST PARSED")
            bad += 1
        for b in c["elements_caracteristiques"]:
            print(f"      - {b}")
        for a in c["example_addresses"]:
            print(f"      @ {a['address']}, {a['municipality']}")
    d = result["diagnostic"]
    print("\n=== p.47 composition de l'inventaire")
    for muni, r in d["by_municipality"].items():
        print(f"    {muni:<20} A{r['A']:>4} B{r['B']:>4} C{r['C']:>4} D{r['D']:>4} "
              f"E{r['E']:>4}  total {r['total']:>4}  supprimé {r['supprime']}")
    t = d["counts"]
    print(f"    {'TOTAL':<20} A{t['A']:>4} B{t['B']:>4} C{t['C']:>4} D{t['D']:>4} "
          f"E{t['E']:>4}  total {t['total']:>4}  supprimé {t['supprime']}")
    print(f"\n{11 - bad}/11 courant blocks parsed with a characteristics list.")


if __name__ == "__main__":
    main()
