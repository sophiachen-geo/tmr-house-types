#!/usr/bin/env python3
"""Write data/places/sud-ouest/types/*.yaml from the parser's output.

    python3 sources/sud-ouest/parse.py && python3 sources/sud-ouest/encode_types.py

The five-column French half of every card comes straight from
sources/sud-ouest/parsed/types.json — nothing here is retyped from the PDF, so
if a card's table is empty the parser is wrong and this file cannot hide it.
The English half (`profile`, `blurb_en`, `origin_en`), the canonical and style
attributions and the measured fields are ours, written against the same fiche.

On the socle / corps / couronnement triad. build.py takes `profile_fr` values as
flat lists of strings under a fixed set of keys, so the triad cannot be nested
sub-keys without changing the schema, which this pass is not allowed to do.
It is preserved instead as a label on each entry — "Socle — …", "Corps — …",
"Couronnement — …" — with the source's own sentence unaltered after the dash,
and in machine-readable form under `traitement_triad` in parsed/types.json.
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PARSED = ROOT / "sources" / "sud-ouest" / "parsed" / "types.json"
OUT = ROOT / "data" / "places" / "sud-ouest" / "types"

DOC = ("Patri-Arch, Étude typomorphologique de l'arrondissement du Sud-Ouest "
       "(2005, mise à jour octobre 2013)")
STUDY_URL = "https://ocpm.qc.ca/sites/default/files/pdf/P81/3.5_etude_typomorphologique_sud-ouest.pdf"

# Every fiche photograph in the study is © Patri-Arch, with usage rights ceded to
# the Ville de Montréal only; republication needs permission. So the study's own
# figures are recorded as placeholders and never reproduced.
def fig(code, caption):
    return [{"file": None, "kind": "placeholder", "licence": "permission required",
             "source_url": STUDY_URL,
             "credit": f"{DOC}, fiche {code} — {caption} © Patri-Arch; usage rights ceded to the "
                       f"Ville de Montréal. Not reproduced."}]


def commons(path, credit_body, confidence="visual"):
    return {"file": f"assets/places/sud-ouest/{path}", "kind": "single",
            "licence": "CC BY-SA (see credit)", "match_confidence": confidence,
            "credit": credit_body}


# --------------------------------------------------------------------------- per-type metadata
# keys: slug, name_en, phase, canonical, styles, and the measured columns; `profile` is the
# English five-column text; `photos` overrides the placeholder default.
META = {
"1.1": dict(
    slug="maison-villageoise", name_en="Village house", phase="p1", page=42,
    canonical=["bourg-vernacular-house-small"], styles=["faubourg-vernacular"],
    tenure_plan="single-family", storeys=1.5, roof={"form": "gabled", "pitch_deg": None},
    window_proportion="square", principal_cladding=["wood-clapboard", "clay-brick"],
    roofing="sheet metal, now often asphalt shingle", garage="none",
    lot_width_m=None, setback_front_m=1.5, setback_side_m=None, front_yard_green_pct=None,
    count_in_place=38,
    profile=dict(
        siting_landscape=[
            "Detached, semi-detached or contiguous — the only residential type in the borough that occurs all three ways.",
            "Front setback under 1.5 m, and usually filled by a galerie rather than a yard.",
            "A side passage giving on to the back yard is frequent.",
            "They rarely form regular alignments, because they were built one at a time rather than in series.",
        ],
        massing=[
            "A plain rectangular body with no projections, 1½ storeys.",
            "The ground floor sits almost on the ground — three risers at most.",
            "Two-slope pitched roof, normally with two dormers.",
            "A galerie running the full width of the building is common.",
        ],
        articulation=[
            "Symmetrical with the door at the centre and windows either side, or asymmetrical with the door at one end.",
            "All ground-floor windows line up horizontally, but there is generally no vertical alignment between them and the dormers: there is one dormer fewer than there are ground-floor openings, so the dormers sit between them.",
            "Window surrounds and corner boards are usually painted a contrasting colour.",
        ],
        openings=[
            "Almost all windows are replacements. The originals were probably six-pane casements; today they are mostly sash or paneless casements.",
            "Dormer windows are smaller, square or barely rectangular.",
            "Doors are plain, with no transom.",
            "The surround follows the cladding: a wood chambranle on clapboarded houses, a wood chambranle or a soldier-course brick lintel on brick ones.",
        ],
        materials=[
            "Stone foundation, sometimes rendered in cement roughcast.",
            "Brick and wood clapboard for the body of the building — the two claddings in use.",
            "Traditional sheet metal was probably the original roofing; asphalt shingle has often replaced it.",
        ]),
    example_addresses=[
        {"address": "110, rue Saint-Augustin", "note": "the maison Clermont, built about 1870, wood board and shingle façades under a sheet-metal roof — the study's own C.3 illustration, and listed in the Évaluation cahier among the borough's immeubles de valeur patrimoniale exceptionnelle"},
        {"address": "727, rue Lacasse", "note": "the study's typical example (unité 4.7), limited front setback with a side access to the back yard"},
        {"address": "747-751, rue du Couvent", "note": "the small series of four houses of variante 3, with a secondary front gable instead of dormers, in unité 4.6 Parc Saint-Henri"},
        {"address": "705-713, rue Bourassa", "note": "variante 4, the flat-roofed village house, in the village Turcot (unité 4.14) — the one unit where this type is the principal one"},
    ],
    photos=[commons("maison-villageoise-741-rue-du-couvent-commons.jpg",
        "741 rue du Couvent, Saint-Henri — a village house of variante 3, with a secondary gable "
        "on the façade in place of dormers, in the series of four the study names on this street. "
        "Photograph by Jeangagnon, 7 May 2016, Wikimedia Commons, CC BY-SA 3.0. "
        "https://commons.wikimedia.org/wiki/File:741_rue_du_Couvent.jpg — licence, author and file "
        "URL read through the Commons API before download. The estate agent's board in the frame "
        "is the photographer's, not a source.")],
    blurb_en=(
        "The oldest housing form still standing in the borough, and the rarest: thirty-eight of "
        "them, which the study says is what gives the type its value. One and a half storeys, a "
        "two-slope roof with two dormers, almost no front setback unless a galerie fills it, and a "
        "side passage to the back. They were built singly, in wood, in the first villages — "
        "Saint-Henri, Turcot, Saint-Augustin, Pointe-Saint-Charles — and burned or were pulled "
        "down for denser brick. Only the village Turcot, too far from the mills to be worth "
        "redeveloping, still has them as its principal type."),
    origin_en=(
        "The same small vernacular house that this site catalogues at Charlesbourg, on the Île "
        "d'Orléans and in the faubourgs of Québec City, arriving here as the pre-industrial layer "
        "under everything else. Note the name: the 2013 study calls it <em>maison villageoise</em>, "
        "but the PIIA by-law's own summary of the seven typologies calls the same thing "
        "<em>maison « de faubourg »</em>. Two arms of the same borough, two names for one form."),
),
"1.2": dict(
    slug="maison-urbaine", name_en="Urban house", phase="p3", page=49,
    canonical=["faubourg-house-flat-roof"], styles=["victorian-eclectic", "second-empire"],
    tenure_plan="single-family", storeys=2, roof={"form": "false-mansard", "pitch_deg": None},
    window_proportion="vertical-2to1", principal_cladding=["clay-brick", "cut-stone", "stone-rusticated"],
    roofing="slate or sheet metal on the false mansard", garage="none",
    lot_width_m=None, setback_front_m=3.0, setback_side_m=0, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Party-wall, as the name says. Front setback generally 2 to 4 m; sometimes under 2 m, but the façades are invariably in alignment.",
            "The front yard is often carefully kept and separated from the public realm by a low wrought-iron fence or a hedge.",
        ],
        massing=[
            "An elongated rectangular plan, two storeys.",
            "The upper storey sits under a low-pitched or flat roof fronted by a false mansard.",
            "The ground floor is raised five to ten risers above grade, and the stair up to it is outside.",
            "An oriel is possible on the ground floor or across both levels; the front door is sometimes in a projecting tambour, under a covered porch, or in a recess.",
        ],
        articulation=[
            "Two vertical alignments of openings: the first the door with a balcony or window over it, the second windows only. Where there is an oriel, it belongs to the second alignment, sometimes with a balcony above it.",
            "The raised ground floor is marked by a hard horizontal break at the socle, made with a change of cladding, with foundation stones set slightly proud, or with a band course between foundation and ground floor.",
            "Ornament is better than the borough average — this is the single-family house built where a location, a park or an owner's choice justified nobler materials.",
        ],
        openings=[
            "Sizes and proportions vary. On the ground floor either a single window of one width to half a height, or paired windows of varying proportion.",
            "Casements with transoms, or sash without, dominate.",
            "Upstairs the dormers bring smaller windows, square or slightly vertical.",
            "Doors single or double, generally with a transom.",
        ],
        materials=[
            "Rusticated stone at the socle.",
            "Brick and cut or rusticated stone for the body — the two dominant claddings.",
            "False mansards clad in slate shingle or sheet metal.",
        ]),
    example_addresses=[
        {"address": "rue Coursol", "note": "sector 22.E.5, the borough's finest run of the type — « le magnifique alignement de petites maisons victoriennes unifamiliales en série de deux étages au décor très élaboré de la rue Coursol suit la courbure de la rue et le rend d’autant plus pittoresque »"},
        {"address": "rue de Rushbrooke", "note": "the study's example of the semi-detached urban house with balcony and projecting window (SO0243); the sector 22.E.11 fiche calls the street's mix of types its defining character"},
        {"address": "rue Saint-Antoine Ouest, at rue Vinet", "note": "the belles séries of two- and three-storey stone buildings with false mansards, small exterior stairs and front yards that sector 22.E.5 records beside the rue Coursol houses"},
    ],
    profile_note=(
        "Two of the Évaluation cahier's fifteen exceptional sectors describe this type directly, and "
        "their words are the best short description of it anywhere in the municipal record. "
        "Sector 22.E.5 Coursol: « À proximité de l’église Sainte-Cunégonde, le magnifique alignement "
        "de petites maisons victoriennes unifamiliales en série de deux étages au décor très élaboré "
        "de la rue Coursol suit la courbure de la rue et le rend d’autant plus pittoresque. C’est le "
        "point fort de ce secteur résidentiel de la bourgeoisie industrielle de l’ancienne "
        "municipalité de Sainte-Cunégonde. » Sector 22.E.4 Place Richmond, for the three-storey "
        "relative of the same form: « La place regroupe un bel ensemble de maisons unifamiliales de "
        "trois étages en brique, au décor sobre et élégant et avec toits mansards, lucarnes et "
        "escaliers extérieurs. L’ensemble est d’une grande cohérence. » Note what the second one "
        "says: single-family, three storeys, and exterior stairs — the stair that this borough's "
        "own typology treats as the mark of the plex, on a house that holds one household."),
    blurb_en=(
        "The single-family house built where the borough could afford ornament. Two storeys over a "
        "ground floor raised five to ten risers, a false mansard across the front, an oriel often "
        "enough, rusticated stone at the base and brick or cut stone above. It is contemporary with "
        "the plexes and built to the same street rules — setback, alignment, low iron fence — but "
        "holds one household where its neighbours hold two or three."),
    origin_en=(
        "The Montréal faubourg house with a flat roof and a false mansard, which this site already "
        "carries at the Plateau and in Ville-Marie. In the Sud-Ouest it is the exception rather "
        "than the rule: the study introduces it by saying the borough is otherwise made of modest, "
        "often high-density residential buildings."),
),
"1.3": dict(
    slug="maison-boomtown", name_en="Boomtown house", phase="p3", page=50,
    canonical=["boomtown-false-front"], styles=["boomtown", "vernaculaire-industriel"],
    tenure_plan="single-family", storeys=1, roof={"form": "flat", "pitch_deg": None},
    window_proportion="vertical", principal_cladding=["clay-brick", "wood-clapboard", "metal-siding"],
    roofing=None, garage="integrated-or-carport",
    lot_width_m=None, setback_front_m=2.75, setback_side_m=0, front_yard_green_pct=None,
    count_in_place=352,
    profile=dict(
        siting_landscape=[
            "Exclusive to the aire de paysage Côte-Saint-Paul, where it is common; examples elsewhere in the borough are rare. It is not the principal type of any single landscape unit.",
            "Generally contiguous, front setback 1.5 to 4 m, and where a series occurs the façades form regular alignments.",
            "But there are detached examples set at the back of the lot, with a deep front yard in front of them — variante 1, and a relatively frequent one.",
            "The front yard is usually barely landscaped.",
        ],
        massing=[
            "A simple rectangular single-storey volume under a flat roof.",
            "A covered entrance porch, or even a full-width galerie, is frequent.",
            "The ground floor is lifted two to four risers above grade; the most recent examples sometimes have a real basement or a garage at the lower level.",
        ],
        articulation=[
            "The façade composition is often very simple: door in the centre, one window each side, with an awning, galerie or porch of varying size added.",
            "The top of the building is usually finished with a metal flashing; more complex crownings are made with a worked sheet-metal cornice, with amortissements — small piers at each end of the roof — or with a parapet at the centre.",
            "More decorated examples carry stone insertions on the façade: low reliefs in geometric patterns, or stone window surrounds.",
        ],
        openings=[
            "Rectangular windows, sometimes nearly square. Casements, or a fixed light paired with a slider.",
            "Doors plain and without a transom.",
            "Sometimes the openings have no particular surround; more often a straight stone lintel or a soldier course of brick sits over the windows.",
        ],
        materials=[
            "Concrete at the base of the house.",
            "Brick, wood clapboard, and contemporary light claddings such as vinyl for the façade.",
        ]),
    example_addresses=[
        {"address": "6305, rue Jogues", "note": "the study's own illustration of the type in the synthèse du développement (SO3535)"},
        {"address": "5975, rue Hamilton", "note": "described by the study as the typical boomtown house (unité 3.12 Terre Hudon)"},
        {"address": "6381, rue Hadley", "note": "the study's second representative example"},
        {"address": "rue Hurteau", "note": "an alignment of boomtown houses, contiguous with a small front yard (unité 3.16 Ville Émard Nord)"},
    ],
    blurb_en=(
        "One storey, flat roof, a door between two windows, and a flashing or a worked metal "
        "cornice for a crown. Three hundred and fifty-two of them, all but a handful inside one "
        "landscape area, Côte-Saint-Paul — and, tellingly, not the principal type of a single "
        "landscape unit anywhere. It is the cheap detached house of the borough's last frontier, "
        "built while the plex was filling everything closer in."),
    origin_en=(
        "Boomtown is the most widely distributed form on this site, and the Sud-Ouest is one of the "
        "places that extend its range. What is unusual here is the count and the confinement: the "
        "study puts a number on it — 352 — and puts it in one corner of one borough. Compare the "
        "Rosemont shoebox, a one-storey flat-roofed self-built house of the same decades that "
        "another Montréal borough treats as a protected type of its own."),
),
"1.4": dict(
    slug="maison-de-veterans", name_en="Veterans' house", phase="p5", page=55,
    canonical=["veterans-house-nha"], styles=["wartime-housing", "minimal-traditional"],
    tenure_plan="single-family", storeys=1, roof={"form": "gabled-or-hipped", "pitch_deg": None},
    window_proportion="horizontal", principal_cladding=["wood-clapboard", "clay-brick", "artificial-stone", "metal-siding"],
    roofing="asphalt shingle", garage="none",
    lot_width_m=None, setback_front_m=5.5, setback_side_m=None, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Detached. Front setback anywhere between 2.5 and 8.5 m; side margins have no typical dimension.",
            "Where the houses occur in concentrations the façades line up regularly — boulevard Monk in unité 3.10, and the rues Jolicoeur and Beaulieu.",
        ],
        massing=[
            "A simple rectangular or square plan, originally with no projection but a covered porch. One storey.",
            "Pitched two-slope, pavilion or hipped roof; the ridge is sometimes parallel to the street and sometimes at right angles to it. Where the pitch is steeper the attic is occupied.",
            "The ground floor is raised two to five risers above grade.",
        ],
        articulation=[
            "Façades are sober and carry very few ornamental details.",
            "The door is at the centre of the façade with windows either side, but the composition is slightly asymmetrical: very often one of the two windows is wider than the other.",
            "On houses clad in a light material there is sometimes a horizontal change of colour on the gable wall.",
            "Where the attic is occupied it is usually lit through windows cut in the gable walls, though dormers in the roof slope also occur.",
        ],
        openings=[
            "Rectangular windows, and in the study's period the sash and casement types have largely given way to replacements.",
            "Doors plain and without a transom.",
            "Openings are generally unframed, or framed only by the cladding itself.",
        ],
        materials=[
            "Concrete foundation.",
            "Wood clapboard originally; brick, artificial stone and contemporary light claddings on many, sometimes several on one façade.",
        ]),
    example_addresses=[
        {"address": "7034, rue Beaulieu", "note": "the study's typical example (unité 3.10 Terre De Sève Sud)"},
        {"address": "boulevard Monk, between rues Raudot and Allard", "note": "the study's illustration of the type in the synthèse (SO3556); the borough's largest concentration"},
        {"address": "6170, rue Angers", "note": "the study's example of a house carrying brick, sheet metal and artificial stone on one façade (unité 3.7 Rue Holy Cross)"},
    ],
    photos=[
        commons("maison-de-veterans-7056-rue-beaulieu-commons.jpg",
            "7056 rue Beaulieu, Côte-Saint-Paul — a veterans' house on the street the study names "
            "as one of the type's concentrations, four doors from its own example at 7034. "
            "Photograph by Jeangagnon, 11 April 2020, Wikimedia Commons, CC BY-SA 4.0. "
            "https://commons.wikimedia.org/wiki/File:7056_rue_Beaulieu.jpg — licence, author and "
            "file URL read through the Commons API before download."),
        commons("maisons-de-veterans-boulevard-monk-commons.jpg",
            "Boulevard Monk, Ville-Émard — the row of veterans' houses the study cites as the "
            "borough's clearest concentration of the type (unité 3.10). Photograph by Jeangagnon, "
            "19 May 2018, Wikimedia Commons, CC BY-SA 4.0, from Category:Maisons de vétérans. "
            "https://commons.wikimedia.org/wiki/File:Boulevard_Monk_-_003.jpg — licence, author and "
            "file URL read through the Commons API before download."),
    ],
    blurb_en=(
        "The one type in the borough that arrived from Ottawa rather than from a Montréal builder. "
        "Wartime Housing Limited, created by the federal government, drew economical, quickly built "
        "models for the workers in the munitions plants; they were meant to be dismantled after the "
        "war and instead spread through the outer quarters. One storey, low pitch, a door between "
        "two windows of unequal width, and — after seventy years — a façade that may carry brick, "
        "sheet metal and artificial stone at once."),
    origin_en=(
        "The same object as the wartime housing this site catalogues at Lévis, at Arvida and in "
        "Verdun's voisinage Crawford, and the reason the canonical id is shared. What the Sud-Ouest "
        "fiche adds is the ordinary end of the story: not a prize-winning NHA neighbourhood but a "
        "few streets in Côte-Saint-Paul where the standard plan was dropped into an existing grid."),
),
"1.5": dict(
    slug="maison-de-ville", name_en="Town house (post-1960 project housing)", phase="p5", page=60,
    canonical=[], styles=["minimal-traditional"],
    tenure_plan="row", storeys=2, roof={"form": "gabled-or-hipped", "pitch_deg": None},
    window_proportion=None, principal_cladding=["clay-brick", "wood-clapboard"],
    roofing="asphalt shingle", garage="integrated-facade",
    lot_width_m=None, setback_front_m=6.5, setback_side_m=None, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Semi-detached or contiguous. Side margins vary where they are paired; the front setback is generously large, 5 to 8 m.",
            "Front yards regularly carry real landscaping — hedges or trees — and a parking space.",
            "The result, the study says, is generally a break with traditional urban development; the sets are homogeneous by street segment or by block, according to how each project was planned.",
        ],
        massing=[
            "Rectangular plan, two storeys, pitched gable or hipped roof, ground floor raised two to five risers.",
            "Many carry projections on the façade, but their position varies from one to the next.",
            "An internal garage is frequent — either in a projecting volume at ground level or in the basement, which then commands a ramp down from the street.",
        ],
        articulation=[
            "The corps of the façade is asymmetrical: one vertical alignment of the front doors with a window above, a second of windows only.",
            "The composition is usually mirrored from one building to the next so that a pair reads as symmetrical.",
            "The socle is expressed by the exposed foundation, the crowning barely expressed at all.",
            "Façades are sober and carry very few ornamental details.",
        ],
        openings=[
            "Sizes and proportions vary, and different sizes are often used to express the different rooms behind — a wide picture window for the living room, smaller openings for the bedrooms.",
            "Doors plain and without a transom.",
            "Surrounds are rarely expressed, except by decorative shutters.",
        ],
        materials=[
            "Concrete foundation at the socle.",
            "Brick dominant on the façade, frequently with a change to a light cladding (wood or synthetic) on parts of the building.",
            "Asphalt shingle roofs.",
        ]),
    example_addresses=[
        {"address": "rue Fabien-Laberge, at avenue De Monts", "note": "the study's illustration of the type in the synthèse (SO3549)"},
        {"address": "rue Vinet, between avenue Lionel-Groulx and rue Saint-Antoine Ouest", "note": "the study's fiche example (SO0344), in the redeveloped Petite-Bourgogne"},
    ],
    blurb_en=(
        "The redevelopment house: two storeys under a pitched roof, an integral garage, a deep "
        "planted setback, built from the 1960s and mostly from the 1980s in the cleared parts of La "
        "Petite-Bourgogne and in the sectors reached by the Opération 20 000 logements. The study is "
        "blunt about what it is — « généralement en rupture avec les développements urbains "
        "traditionnels » — and equally clear that each project is internally consistent."),
    origin_en=(
        "No canonical form is claimed for this record. It is the one Sud-Ouest residential type that "
        "does not match anything else on this site: not the 19th-century terrace the English word "
        "<em>town house</em> normally names, not the plex it replaced, and not a suburban model "
        "catalogue. It belongs to the fifth phase and to the machinery of urban renewal, and it is "
        "recorded here because the borough's own typology records it."),
),
"2.1": dict(
    slug="duplex-escalier-interieur", name_en="Duplex with interior stair", phase="p3", page=65,
    canonical=["duplex-interior-stair", "plex-family"], styles=["faubourg-vernacular", "victorian-eclectic"],
    tenure_plan="duplex", storeys=2, roof={"form": "flat", "pitch_deg": None},
    window_proportion="vertical-2to1", principal_cladding=["clay-brick", "stone-rusticated", "wood-clapboard"],
    roofing=None, garage="none",
    lot_width_m=None, setback_front_m=0, setback_side_m=0, front_yard_green_pct=0,
    profile=dict(
        siting_landscape=[
            "Contiguous, and in most cases with no front setback at all — which is exactly why the stair to the second dwelling is inside the building.",
            "The façades form regular alignments.",
            "Present in every sector lotted at the end of the industrialisation period, 1825–1875.",
        ],
        massing=[
            "Rectangular plan with no projections, two storeys, flat roof.",
            "The ground floor is barely raised — two or three risers.",
            "A small balcony over the entrance doors is possible, mainly where the doors are paired.",
        ],
        articulation=[
            "Two modes of composition, and they are what tells the variants apart: doors separated, or doors paired.",
            "With separated doors, doors and windows alternate along the ground floor and the ground-floor openings frequently fail to line up with those above.",
            "With paired doors there are two vertical alignments, one of them holding the two doors with a balcony over them.",
            "The socle is one or two courses of rusticated stone; on altered buildings the stone is often replaced by exposed concrete.",
            "The crowning is a moulded cornice, more or less worked according to the case.",
        ],
        openings=[
            "Originally sash or casement with or without a transom; most of what survives is replacement, frequently sliders.",
            "The dominant proportion is one width to half a height, and segmental-arched openings are frequent.",
            "Doors plain, with or without a transom, the transom's height variable.",
        ],
        materials=[
            "Rusticated stone at the socle.",
            "Brick dominant on the body of the façade, with some buildings in rusticated stone or wood clapboard.",
            "Wood balconies with metal guards.",
        ]),
    related_buildings=[
        {"name": "Maisons d'ouvriers des ateliers du Grand Tronc, 422-436, 438-444, 456 and 458-460 rue de Sébastopol — built about 1855 to house a highly skilled workforce, « parmi les plus anciennes du quartier », and listed by the Évaluation cahier among the borough's immeubles de valeur patrimoniale exceptionnelle. Sector 22.E.13. Neither document assigns them to a type: the cahier calls them a série d'habitations and the typo-morphological study does not name the street. They are recorded on this card because they are contemporary with it, from the phase before the setback rule, and because they are the oldest surviving worker housing in the borough.",
         "url": "http://ville.montreal.qc.ca/pls/portal/docs/page/patrimoine_urbain_fr/media/documents/12_evaluation_patrimoine_sud.pdf"},
    ],
    blurb_en=(
        "The first multi-family building type built in the borough, and the one the exterior stair "
        "eventually killed. Two dwellings stacked under a flat roof, hard on the street line, both "
        "front doors at ground level and the upper dwelling reached by a stair inside. It loses "
        "ground after 1880 and is finally displaced by the triplex with exterior stair around 1900 "
        "— which is the whole argument of this borough in one sentence."),
    origin_en=(
        "The plex before the stair went outside. Reading this record against the triplex with "
        "exterior stair (2.6) gives the mechanism directly: no setback, so no room for a stair in "
        "the yard, so the stair eats interior floor area instead."),
),
"2.2": dict(
    slug="duplex-escalier-exterieur", name_en="Duplex with exterior stair", phase="p4", page=70,
    canonical=["duplex-exterior-stair", "plex-family"], styles=["faubourg-vernacular"],
    tenure_plan="duplex", storeys=2, roof={"form": "flat", "pitch_deg": None},
    window_proportion="vertical-2to1", principal_cladding=["clay-brick"],
    roofing=None, garage="none",
    lot_width_m=None, setback_front_m=3.25, setback_side_m=0, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Contiguous, with a front margin of 2 to 4.5 m; the front façades generally form regular alignments.",
            "Front yards stay sober, sometimes with a low metal fence between yard and public realm.",
            "Built at the same time as the triplex with exterior stair, from 1900 to 1945, in the sectors that needed less density — furthest from downtown. Commonest in the aire de paysage Côte-Saint-Paul.",
        ],
        massing=[
            "A simple rectangular plan, two storeys, flat roof.",
            "The ground floor is raised two to four risers above grade.",
            "A balcony at the upper level, and under it a covered entrance porch at ground level.",
            "An exterior stair reaches the upper dwelling; it is generally L-shaped, since the front margin is not deep enough for a straight run.",
        ],
        articulation=[
            "The socle is barely expressed and generally formed by the exposed foundation.",
            "The composition of the corps is symmetrical: the doors form the central vertical bay, the two flanking bays a vertical alignment of windows.",
            "The crowning varies — from a simple metal flashing to a moulded wood or metal cornice or a pedimented parapet, sometimes a light eave.",
        ],
        openings=[
            "Sash or casement, with or without a transom, in a proportion of one width to half a height.",
            "Doors plain with a transom.",
            "Lintels expressed as a cut-stone band or as a soldier course of brick, straight or in a segmental arch.",
        ],
        materials=[
            "Rusticated stone at the socle.",
            "Brick dominant, with some buildings in rusticated stone.",
            "Wood balconies and stair treads, metal guards.",
        ]),
    example_addresses=[
        {"address": "1903-1905, rue Springland", "note": "the study's fiche example (SO0266) and its illustration of the type in the synthèse"},
        {"address": "6959, rue Jogues", "note": "the study's example of variante 1, the asymmetrical duplex with exterior stair (SO0395)"},
    ],
    blurb_en=(
        "The triplex's smaller twin, built simultaneously and for the same reason, in the parts of "
        "the borough that did not need three dwellings on a lot. Two storeys, flat roof, a setback "
        "of two to four and a half metres, and an L-shaped stair climbing that setback because it "
        "is not deep enough for a straight one — a detail the study records and which explains the "
        "curved and dog-legged stairs of Montréal better than any folklore about snow."),
    origin_en=(
        "The study is explicit that this type and the triplex with exterior stair (2.6) are the "
        "same event: <em>« Le duplex avec escalier extérieur a été construit de façon simultanée au "
        "triplex avec escalier extérieur, soit à partir de 1900 jusqu’à 1945 »</em>. Density, not "
        "date, is what separates them."),
),
"2.3": dict(
    slug="duplex-sureleve", name_en="Raised duplex", phase="p4", page=73,
    canonical=["duplex-raised", "plex-family"], styles=["minimal-traditional"],
    tenure_plan="duplex", storeys=2, roof={"form": "flat", "pitch_deg": None},
    window_proportion="square", principal_cladding=["clay-brick", "cut-stone"],
    roofing=None, garage="underground",
    lot_width_m=None, setback_front_m=4.0, setback_side_m=0, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Contiguous, with a front margin of 3 to 5 m. Built in series, which gives a regular alignment of façades.",
            "Front yards are mostly lawn.",
            "It is the principal type of no landscape unit anywhere in the borough.",
        ],
        massing=[
            "A simple rectangular form, two storeys, flat roof.",
            "The ground floor is raised five to ten risers — the feature the type is named for.",
            "The basement sometimes holds interior parking, reached by a ramp down from the street.",
            "Projecting windows and balconies are rare.",
        ],
        articulation=[
            "The socle is the exposed concrete foundation; sometimes the ground-floor level is distinguished by using stone as its cladding.",
            "Two modes of composition for the corps. The first is symmetrical on three vertical bays, the central bay aligning the two front doors at ground level with a balcony above, the flanking bays windows.",
            "The second is the same but with a single door at the centre, the upper dwelling's door pushed to one side of the façade — and these duplexes are generally built as pairs, so the two side doors end up adjacent.",
            "The crowning is simple, generally a stone band course or a light eave.",
        ],
        openings=[
            "Sizes and proportions vary. Large glazed bays of nearly square proportion, made of several fixed, casement or sliding sashes.",
            "Other openings are generally one width to half a height.",
            "Doors plain and without a transom, sometimes paired.",
            "Surrounds mostly a stone lintel and sill.",
        ],
        materials=[
            "Concrete at the socle.",
            "Brick dominant on the body of the façade, with stone sometimes used to pick out parts of the building, especially the ground floor.",
        ]),
    blurb_en=(
        "What distinguishes it from the duplex with interior stair, the study says, is the front "
        "setback, the symmetrical façade and the use of square or rectangular windows. It is the "
        "hinge type between the pre-war plex and the post-war one: built at the end of the "
        "infrastructure period and the start of urban renewal, raised high enough to put parking "
        "under it, and — the study notes without comment — the principal type of nowhere."),
    origin_en=(
        "The raised duplex is the plex adjusting to the car and to the picture window. Its ground "
        "floor climbs from three risers to ten, the basement becomes a garage, and the ornamental "
        "programme collapses to a stone band. Compare the postwar plexes of Verdun and Villeray."),
),
"2.4": dict(
    slug="duplex-trois-etages", name_en="Three-storey duplex", phase="p3", page=75,
    canonical=["duplex-three-storey", "plex-family"], styles=["second-empire", "victorian-eclectic"],
    tenure_plan="duplex", storeys=3, roof={"form": "false-mansard", "pitch_deg": None},
    window_proportion="vertical-2to1", principal_cladding=["clay-brick", "stone-rusticated"],
    roofing="slate or sheet metal on the false mansard, often replaced by asphalt shingle", garage="none",
    lot_width_m=None, setback_front_m=0, setback_side_m=0, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Built almost everywhere in the borough except the aire de paysage Côte-Saint-Paul.",
            "Dominantly contiguous and with no front setback. Where there is one it exists to take an exterior stair up to the ground floor.",
            "In alignment, unless built independently of its neighbours; the shallow setback means no landscaping is characteristic of the type.",
        ],
        massing=[
            "A rectangular body of three storeys, generally with a false mansard.",
            "The ground floor is raised three risers, or up to eight where there is a front setback.",
            "Balconies, where present, are on the first floor above the entrance doors.",
            "Projecting windows on every level occur only on buildings with a setback.",
        ],
        articulation=[
            "The dominant composition is asymmetrical, on two vertical bays: the first aligning the paired ground-floor doors with the windows above, sometimes with a first-floor balcony; the second windows only, and it is there that the projecting windows sit.",
            "The socle is one to three courses of stone, and the top course is sometimes of a different texture so as to make a horizontal band between socle and corps; where the whole façade is stone, the texture or block size changes at the same line.",
            "The crowning is a false mansard over a moulded cornice on modillions or consoles, its dormers varied in shape and more or less ornamented.",
            "Buildings of the 1825–1875 period are soberer; those of the first third of 1875–1945 use stone more often, with more complex ornament and a marked raising of the ground floor.",
        ],
        openings=[
            "Sash or casement with a transom, one width to half a height.",
            "Doors generally plain or paired, with a transom.",
            "Surrounds are a straight stone lintel or a brick flat-arch in a segmental curve; rusticated-stone buildings get a complete cut-stone surround, and on the more ornamented buildings the lintel is absorbed into a horizontal band.",
        ],
        materials=[
            "Generally rusticated stone at the socle, sometimes cut stone.",
            "Brick dominant, with some three-storey duplexes clad in rusticated stone.",
            "False mansards originally slate or sheet metal, often replaced by asphalt shingle.",
            "Balconies and stairs generally wood with metal guards.",
        ]),
    example_addresses=[
        {"address": "rue d'Hibernia, between rues de Coleraine and de Rozel", "note": "the study's example of the type built with no front setback (SO0200)"},
        {"address": "2225-2247, rue Quesnel", "note": "the study's example of a three-storey duplex clad in stone (SO0690)"},
        {"address": "place Richmond", "note": "sector 22.E.4, three storeys, brick, mansard roofs, dormers and exterior stairs, « L’ensemble est d’une grande cohérence »"},
    ],
    profile_note=(
        "The Évaluation cahier's sector 22.E.4 Place Richmond describes what is visibly this type's "
        "gauge, and calls its dwellings single-family: « La place regroupe un bel ensemble de "
        "maisons unifamiliales de trois étages en brique, au décor sobre et élégant et avec toits "
        "mansards, lucarnes et escaliers extérieurs. L’ensemble est d’une grande cohérence. » The "
        "typo-morphological study has no single-family three-storey type; its three-storey forms "
        "are this duplex and the triplexes. Which document is right about the dwelling count on "
        "place Richmond is not settled here — both are recorded, because the disagreement is "
        "between two arms of the same borough eight years apart, and because the combination the "
        "cahier reports (one household, three storeys, an exterior stair) is precisely the case "
        "the typology has no box for."),
    blurb_en=(
        "Two dwellings over three occupied levels under a false mansard — the type that answers the "
        "question of what Montréal built before the exterior stair, and the one the study reaches "
        "for when it explains why the fabric of the 1875–1945 period is not homogeneous. Built with "
        "no setback in the earlier phase and with one in the later, which is when the projecting "
        "window and the raised ground floor arrive."),
    origin_en=(
        "It is the plex family's tallest pre-1900 member and its closest relative to the Second "
        "Empire terraces of Ville-Marie and the Plateau. The study notes a rare third dwelling "
        "squeezed in — variante 2, a triplex with a false-mansard roof — which is how the boundary "
        "between duplex and triplex actually behaves on the ground."),
),
"2.5": dict(
    slug="triplex-escalier-interieur", name_en="Triplex with interior stair", phase="p3", page=80,
    canonical=["triplex-interior-stair", "plex-family"], styles=["faubourg-vernacular", "victorian-eclectic"],
    tenure_plan="triplex", storeys=3, roof={"form": "flat", "pitch_deg": None},
    window_proportion="vertical-2to1", principal_cladding=["clay-brick", "stone-rusticated"],
    roofing=None, garage="none",
    lot_width_m=None, setback_front_m=0, setback_side_m=0, front_yard_green_pct=0,
    profile=dict(
        siting_landscape=[
            "Contiguous and with no front setback — but, unusually, its façade does not keep a regular alignment with its neighbours'.",
            "No landscaping at all.",
            "Mainly in the sectors lotted at the end of the industrialisation period and the start of the infrastructure period, when building behind a setback was not yet general.",
            "Frequently sited in a fabric with no ruelle, which is why the porte cochère appears (variante 3).",
        ],
        massing=[
            "A simple rectangular body under a flat roof, three storeys.",
            "The ground floor is raised less than three risers.",
            "Balconies possible at the upper levels; no projecting windows.",
        ],
        articulation=[
            "The composition of the corps varies, both in where the ground-floor doors sit and in how the openings line up vertically. On some buildings every door is paired, making a long run of doors along the ground floor; on others two paired doors sit at one end and a single door at the other.",
            "The socle is one to three courses of rusticated stone; exposed concrete foundations are generally the result of renovation.",
            "The crowning is a moulded wood cornice with modillions or consoles; brick cornices and false mansards also occur.",
        ],
        openings=[
            "Sash or casement with a transom, one width to half a height.",
            "Doors plain or paired, with a transom.",
            "Surrounds expressed by a straight brick or stone lintel, or a brick flat-arch in a segmental curve; rusticated-stone buildings get a complete cut-stone surround.",
        ],
        materials=[
            "Rusticated stone at the socle.",
            "Brick dominant; some triplexes with interior stair are clad in rusticated stone.",
            "Wood balconies with metal guards; the steps up to the ground floor are generally masonry.",
        ]),
    example_addresses=[
        {"address": "north side of rue Delisle, between avenue Atwater and rue Vinet", "note": "the study's illustration of the type in the synthèse du développement (SO0237)"},
        {"address": "rue Murray, between rues Ottawa and William", "note": "the study's fiche example — two semi-detached triplexes with interior stair and doors assembled at the centre (SO0085)"},
        {"address": "rue Sainte-Émilie, between rues Turgeon and Delinelle", "note": "the study's example of variante 3, the triplex with interior stair and porte cochère (SO0120)"},
    ],
    blurb_en=(
        "Three dwellings, three storeys, flat roof, no setback and no stair in the yard — the "
        "densest thing the borough built before 1900, and a denser variant of the duplex with "
        "interior stair rather than an ancestor of the triplex with exterior stair. Most dwellings "
        "have their own stair, but it is frequent for the two upper dwellings to share one. Where "
        "the block has no ruelle, a porte cochère cuts through to the back yard."),
    origin_en=(
        "The interior-stair triplex is the form the exterior-stair triplex displaced. Both are "
        "carried on this site, and their canonical ids are siblings under <em>plex-family</em> "
        "precisely so that the swap can be read as one event rather than two unrelated types."),
),
"2.6": dict(
    slug="triplex-escalier-exterieur", name_en="Triplex with exterior stair", phase="p4", page=84,
    canonical=["triplex-exterior-stair", "plex-family"], styles=["faubourg-vernacular"],
    tenure_plan="triplex", storeys=3, roof={"form": "flat", "pitch_deg": None},
    window_proportion="vertical-2to1", principal_cladding=["clay-brick", "stone-rusticated"],
    roofing=None, garage="none",
    lot_width_m=None, setback_front_m=3.75, setback_side_m=0, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "The commonest variant of the triplex in the borough, and the base type of the urban fabric of four-built-sided blocks with an « H » ruelle that is so typical of several Montréal quarters.",
            "Contiguous, front margin between 2.5 and 5 m. The alignment of façades is not regular.",
            "The front yard is often characterised by a low metal fence.",
            "Principal type in eleven of the sixty-five landscape units. Only the two interior-stair plexes it displaced are named principal in more of them — the duplex with interior stair in thirteen, the triplex with interior stair in twelve — which is what a type that arrives in 1900 looks like measured against types with a fifty-year head start.",
        ],
        massing=[
            "A rectangular body, sometimes with projecting windows on every level.",
            "Generally a rear extension, whose position is reversed from one building to the next so as to make shared yards.",
            "Flat roof, three storeys, ground floor raised two to three risers.",
            "An exterior access stair climbs to the first floor. Balconies are possible.",
        ],
        articulation=[
            "Two principal modes of composition. The first is asymmetrical on two vertical bays: the first aligns the exterior stair, the first-floor entrance doors and a window and balcony at the second; the second is windows only and may project from the plane of the wall. In this mode the ground-floor dwelling's door is frequently set apart from both alignments — at the centre of the façade, or just behind the stair.",
            "The second is symmetrical on three vertical bays: a central bay of doors and balconies, flanking bays of windows. At the first floor the two doors to the upper dwellings can sit at the centre, and the exterior stair is then slightly curved; or the stair runs straight to doors placed in one of the side bays.",
            "The first-floor entrance porch is frequently recessed behind the plane of the façade.",
            "The socle is one or two courses of rusticated stone.",
            "The crowning stands out as a moulded wood cornice, a stone cornice, or a pedimented parapet.",
        ],
        openings=[
            "Mainly sash or casement, with or without a transom. Proportion generally one width to half a height, though windows may be paired into a nearly square opening.",
            "Doors plain and with a transom; at the first floor the two doors to the upper dwellings are sometimes paired.",
            "Lintels expressed as a cut-stone band or as soldier-course brick, straight or in a segmental arch.",
        ],
        materials=[
            "Rusticated stone at the socle.",
            "Brick the dominant cladding, though some buildings are clad in rusticated stone.",
            "Balconies and stair treads in wood; guards in metal.",
        ]),
    example_addresses=[
        {"address": "872-880, rue Agnès", "note": "the study's fiche example of the type (SO0003)"},
        {"address": "avenue Greene, between rues Saint-Antoine Ouest and Saint-Jacques", "note": "the study's example of the asymmetrical triplex (SO0110)"},
        {"address": "rue York, at rue De Roberval", "note": "the study's example of the symmetrical triplex with the slightly curved exterior stair (SO0405)"},
        {"address": "avenue Egan, between boulevard De La Vérendrye and rue Laurendeau", "note": "the study's illustration of the type in the synthèse du développement (SO0254)"},
    ],
    blurb_en=(
        "The archetypal Montréal house, and this is the document that says how it happened. It "
        "appears from 1900. Its parent is the block with an « H » ruelle and four built "
        "sides. Its defining feature is not the stair as an object but the stair as a consequence: "
        "the front-setback requirement gave the stair somewhere to go, and putting it there kept "
        "the interior floor area and saved heating a shared hall. Eleven of the borough's "
        "sixty-five landscape units name it as their principal type."),
    origin_en=(
        "The mechanism, verbatim from the study's synthèse: <em>« l’obligation de l’implantation "
        "avec une marge de recul avant amènera la translation de l’escalier d’accès aux logements "
        "des étages supérieurs vers l’extérieur, ce qui donnera la caractéristique si typique des "
        "bâtiments des quartiers montréalais de cette époque »</em>. The sequence is dated: lotting "
        "without a ruelle and building with no setback <em>« ne sera abandonnée que vers la fin des "
        "années 1880 »</em>; this type <em>« fait son apparition principalement à partir de "
        "1900 »</em>; the duplex with exterior stair and the multiplex follow shortly after."),
),
"2.7": dict(
    slug="multiplex", name_en="Multiplex", phase="p4", page=88,
    canonical=["multiplex-4-6", "plex-family"], styles=["faubourg-vernacular"],
    tenure_plan="walk-up", storeys=3, roof={"form": "flat", "pitch_deg": None},
    window_proportion="vertical-2to1", principal_cladding=["clay-brick", "stone-rusticated"],
    roofing=None, garage="none",
    lot_width_m=None, setback_front_m=3.25, setback_side_m=0, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Contiguous, front margin 2 to 4.5 m; the alignment of façades is regular where the multiplexes are built in series.",
            "A low metal — sometimes wood — fence characterises the outdoor treatment.",
            "Generally built in a fabric with a ruelle, like the triplex, but on wider lots. Mostly from the First World War to the end of the 1875–1945 period.",
        ],
        massing=[
            "A simple rectangular body with no projections, generally with a rear extension whose position reverses from one building to the next so as to maximise sunlight in the yards.",
            "Three storeys, ground floor raised two to three risers, flat roof.",
            "Two dwellings per floor, and a shared access for the two dwellings on the top floor.",
        ],
        articulation=[
            "The socle is one or two courses of stone, or an exposed concrete foundation.",
            "The crowning is underlined by a moulded metal cornice, a stone cornice or a parapet.",
        ],
        openings=[
            "Sash or casement, generally one width to half a height.",
            "Doors plain with a transom; the doors to the upper dwellings are often paired.",
            "Lintels expressed as a cut-stone band or soldier-course brick.",
        ],
        materials=[
            "Concrete or rusticated stone at the socle.",
            "Brick dominant.",
            "Balconies and stair treads in wood; guards in metal.",
        ]),
    example_addresses=[
        {"address": "rue Delinelle, between rues Notre-Dame Ouest and Depocas", "note": "the study's fiche example of the type (SO0138)"},
        {"address": "rue Soulanges, between rues Butler and Charlevoix", "note": "the study's example of a multiplex with a recessed first-floor porch (SO0204)"},
        {"address": "6114-6116, rue Hamilton", "note": "the study's illustration of the type in the synthèse du développement (SO3584)"},
    ],
    photos=[
        commons("multiplex-805-815-rue-du-couvent-commons.jpg",
            "805-815 rue du Couvent, Saint-Henri — the multiplex in its symmetrical three-bay mode: "
            "a central bay of doors and balconies, flanking bays of windows, and one slightly "
            "curved exterior stair serving the pair of doors on the first floor. Photograph by "
            "Jeangagnon, 24 January 2015, Wikimedia Commons, CC BY-SA 3.0, from "
            "Category:Multiplexes (buildings). "
            "https://commons.wikimedia.org/wiki/File:805-815,_rue_du_Couvent.jpg — licence, author "
            "and file URL read through the Commons API before download."),
        commons("multiplex-375-399-rue-de-la-montagne-commons.jpg",
            "375-399 rue de la Montagne at rue Barré, Griffintown — four six-plex built about 1920, "
            "per the Ville de Montréal description quoted on the file page: « Cet ensemble de "
            "bâtiment est formé de 4 six-plex ». Three storeys, brick, flat roof, but built to the "
            "street line rather than behind the setback the study calls general for the type. "
            "Photograph by Jeangagnon, 6 October 2015, Wikimedia Commons, CC BY-SA 3.0, from "
            "Category:Multiplexes (buildings). "
            "https://commons.wikimedia.org/wiki/File:375-399,_rue_de_la_Montagne.jpg — licence, "
            "author and file URL read through the Commons API before download."),
    ],
    blurb_en=(
        "The top of the plex family: three storeys, two dwellings per floor, and — the detail that "
        "matters — one shared access for the two dwellings on the top floor. The study calls it a "
        "derivation of the triplex with exterior stair, « la transformation typologique du "
        "triplex afin de répondre au processus de densification du tissu urbain », built on "
        "wider lots from the First World War on."),
    origin_en=(
        "This is where the plex family ends and the apartment building begins. The multiplex still "
        "gives most dwellings their own front door but concedes a shared one at the top; the maison "
        "d'appartements (3.1) concedes the whole stair; the immeuble d'appartements (3.3) concedes "
        "a common hall serving six to twelve. Read the four records in order and the boundary the "
        "canonical layer draws between <em>plex-family</em> and "
        "<em>apartment-house-common-hall</em> is the study's own."),
),
"3.1": dict(
    slug="maison-appartements", name_en="Apartment house", phase="p4", page=92,
    canonical=["apartment-house-common-hall"], styles=["stripped-classicism", "minimal-traditional"],
    tenure_plan="walk-up", storeys=2, roof={"form": "flat", "pitch_deg": None},
    window_proportion="square", principal_cladding=["clay-brick", "cut-stone"],
    roofing="asphalt shingle where a false roof is present", garage="none",
    lot_width_m=None, setback_front_m=3.5, setback_side_m=1.25, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Detached, semi-detached or contiguous. Front setback 2.5 to 4.5 m; where a side margin exists it is 1 to 1.5 m.",
            "Façades align where the buildings are built in series.",
            "Appears from the 1930s, straddling the end of the infrastructure period and the beginning of urban renewal.",
        ],
        massing=[
            "A simple rectangular plan, two storeys, ground floor raised five to six risers and reached by an interior or an exterior stair.",
            "The entrance porch — and sometimes the stair cage — projects.",
            "Balconies are often aligned on each side of the façade.",
            "Generally four or six dwellings, all reached from one central interior stair.",
        ],
        articulation=[
            "A symmetrical composition with the main entrance door at the centre, often with a tall opening above it to light the stair cage, and a vertical alignment of balconies or windows on each side of the central bay; the number of windows in each side alignment varies.",
            "The exposed concrete foundation makes the socle, which may also take in the ground floor — clad then in stone, so as to make a horizontal division with the brick above.",
            "The crowning is simple, usually a metal flashing; a shallow eave or a false roof also occurs, and where the stair volume projects it may be crowned with a gable.",
        ],
        openings=[
            "Windows of varied types and proportions — casement or sash at one width to half a height, and square or slightly horizontal openings, usually made of fixed and opening parts together.",
            "The ground-floor entrance door is single or double, without a transom but sometimes with sidelights, and often under a marquise or a shallow eave.",
        ],
        materials=[
            "Concrete at the socle.",
            "Brick the dominant cladding, with stone possible at the ground floor.",
            "False roofs, where present, in asphalt shingle.",
        ]),
    example_addresses=[
        {"address": "6661-6667, rue Hurteau", "note": "the study's fiche example of the type (SO0321), and the same building it uses to illustrate the type in the synthèse du développement"},
        {"address": "west side of rue Beaulieu, near rue Allard", "note": "the study's example of an apartment house whose projecting stair volume is crowned with a gable (SO0244)"},
    ],
    blurb_en=(
        "The point at which the plex stops. Two storeys, four or six dwellings, and a single "
        "central interior stair reaching all of them — « Cet immeuble à logements se "
        "différencie du plex par la présence d’un escalier commun intérieur pour accéder aux "
        "logements ». It arrives in the 1930s, and it is the only Sud-Ouest type whose "
        "definition is drawn by negation from another type on the same page."),
    origin_en=(
        "First of the three members of the study's family 3, <em>L'immeuble d'appartements</em>, "
        "which the PIIA by-law summarises in one sentence that this site takes as the definition of "
        "the canonical form: <em>« L’immeuble d’appartements, aussi nommé édifice de rapport, est "
        "construit entre les deux guerres le long de boulevards ou d’avenues prestigieuses. Ce "
        "bâtiment possède un hall d’entrée commun qui dessert de six à douze logements. »</em>"),
),
"3.2": dict(
    slug="conciergerie", name_en="Conciergerie (walk-up apartment block)", phase="p5", page=95,
    canonical=["apartment-house-common-hall"], styles=["international-style", "minimal-traditional"],
    tenure_plan="walk-up", storeys=3.5, roof={"form": "flat", "pitch_deg": None},
    window_proportion=None, principal_cladding=["clay-brick"],
    roofing=None, garage="none",
    lot_width_m=None, setback_front_m=None, setback_side_m=None, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Generally detached, with front and side margins of variable size; contiguous ones built as sets share a uniform front margin.",
            "Landscaping dominated by lawn.",
            "Mostly built during the 1945-onward period of urban renewal — substitution buildings replacing older structures. The exception is the group on boulevard des Trinitaires, where the layout was planned around this building type from the start.",
        ],
        massing=[
            "A simple rectangular plan, the long side generally parallel to the street.",
            "Three or four storeys, flat roof.",
            "The only projections on the façades are the vertical alignments of balconies running through every level.",
        ],
        articulation=[
            "The socle is the exposed foundation.",
            "The corps of the façade is composed of an irregular number of vertical alignments of openings.",
            "The crowning is barely expressed — generally a plain metal flashing; sometimes a band of brick in a colour contrasting with the body of the façade makes one, or a projecting roof.",
        ],
        openings=[
            "Window and door types and proportions are varied on this type.",
            "Lintels and surrounds are barely expressed or not at all.",
        ],
        materials=[
            "Concrete at the socle.",
            "The body of the façade generally clad in brick, in varying tones.",
        ]),
    example_addresses=[
        {"address": "boulevard des Trinitaires", "note": "the one part of the borough the study says was laid out for this building type rather than redeveloped into it"},
        {"address": "1960-1970, rue Le Ber", "note": "the study's fiche example (SO1071)"},
    ],
    blurb_en=(
        "Three or four storeys, one shared entrance, an irregular number of window bays and a "
        "flashing for a cornice. Almost all of them are replacements — the study calls them "
        "« bâtiments de substitution » standing where something older was pulled down — "
        "and their gauges vary enormously with the number of dwellings in each project. Only the "
        "group on boulevard des Trinitaires was planned for."),
    origin_en=(
        "The second of the study's three apartment types, and the one that carries the postwar "
        "history of the borough on its face: expropriation, demolition, and rebuilding at a scale "
        "unrelated to the lot pattern around it. The same canonical form as the maison "
        "d'appartements and the immeuble d'appartements — the common hall — at a different height."),
),
"3.3": dict(
    slug="immeuble-appartements", name_en="Apartment building (lift-served)", phase="p5", page=98,
    canonical=["apartment-house-common-hall"], styles=["international-style"],
    tenure_plan="slab", storeys=5, roof={"form": "flat", "pitch_deg": None},
    window_proportion=None, principal_cladding=["clay-brick"],
    roofing=None, garage="underground",
    lot_width_m=None, setback_front_m=None, setback_side_m=None, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Generally detached, front and side margins of variable size, façades not in regular alignment.",
            "Landscaping dominated by lawn.",
            "Found throughout the borough. Mostly built during the 1945-onward period of urban renewal, as substitution buildings.",
        ],
        massing=[
            "A simple rectangular plan, the long side generally parallel to the street.",
            "More than four storeys, and it may take the form of a residential tower.",
            "Flat roof; projecting balconies are frequent.",
            "Large enough to require large lots, because access to the upper dwellings is by lift.",
        ],
        articulation=[
            "The socle is the exposed foundation.",
            "The corps of the façade is composed of an irregular number of vertical alignments of openings.",
            "The crowning is barely expressed, generally a plain metal flashing.",
        ],
        openings=[
            "Window and door types and proportions are varied on this type.",
            "Lintels and surrounds are barely expressed or not at all.",
        ],
        materials=[
            "Concrete at the socle.",
            "The body of the façade generally clad in brick, in varying tones.",
        ]),
    example_addresses=[
        {"address": "rue Dick-Irvin", "note": "the study's fiche example (SO1084)"},
        {"address": "4450, rue Saint-Jacques", "note": "Habitation Charlebois, the study's second fiche example (SO3051)"},
    ],
    blurb_en=(
        "The top of the borough's residential scale and the end of the sequence that starts with "
        "the duplex: more than four storeys, a lift, and a shared hall. The PIIA by-law's own "
        "summary is the definition this site uses for the canonical form — an édifice de "
        "rapport with « un hall d’entrée commun qui dessert de six à douze logements »."),
    origin_en=(
        "Note what the study does not do here: it does not treat the lift-served apartment building "
        "as a different family from the two-storey maison d'appartements. All three share family 3, "
        "and the thing they share is the common entrance. On this site they share one canonical id "
        "for the same reason."),
),
# ------------------------------------------------------ families 4–7: recorded, not carded
"4": dict(
    slug="immeuble-vocation-mixte", name_en="Mixed-use building", phase="p3", page=101,
    canonical=["mixed-use-flat-roof-block"], styles=["victorian-eclectic", "second-empire"],
    tenure_plan="mixed", storeys=3, roof={"form": "flat-or-false-mansard", "pitch_deg": None},
    window_proportion="vertical-2to1", principal_cladding=["clay-brick", "stone-rusticated"],
    roofing=None, garage="none", is_residential=False,
    lot_width_m=None, setback_front_m=0, setback_side_m=0, front_yard_green_pct=0,
    profile=dict(
        siting_landscape=[
            "Mainly on the borough's big commercial arteries and at certain junctions of residential streets; generally built to the street line.",
            "Some were built as mixed-use; others are residential buildings converted to take a shop, and those carry more variants.",
        ],
        massing=[
            "A clear division between the ground floor and the storeys above, made with a change of cladding, a cornice and a different fenestration.",
        ],
        articulation=[
            "The socle takes in the whole ground floor, unlike every other type in the study; a large part of it is shop window, with wood panels in the unglazed parts.",
            "Where the shopfront does not fill the façade, wood or stone pilasters can divide the frontage, and on the masonry part the socle is a stone band course.",
            "The corps is composed of vertical and horizontal alignments of openings, in a number that varies from building to building; balconies where present are vertically aligned.",
            "The crowning is a moulded cornice or a false mansard, carried round both façades on a corner, where the corner is often marked by a turret.",
        ],
        openings=[
            "Ground-floor openings may not align with those above.",
            "Upper floors follow the residential types the building sits among.",
        ],
        materials=[
            "Brick and stone, with the shopfront in wood and glass.",
        ]),
    example_addresses=[
        {"address": "2463-2473, rue du Centre, between rues Ropery and Charlevoix", "note": "the édifice O.-Labelle (SO1706), also listed in the Évaluation cahier among the borough's immeubles de valeur patrimoniale exceptionnelle"},
        {"address": "1124-1130, rue Charlevoix and 2602-2612, rue de Châteauguay", "note": "the Coop du coin (SO1679)"},
        {"address": "7005, rue Jogues", "note": "the study's example of variante 1, a multiplex converted into a mixed-use building (SO3530)"},
    ],
    blurb_en=(
        "Recorded, not carded: the study's family 4 is a commercial ground floor under dwellings, "
        "and this site's type cards are residential. It earns its place in the record because its "
        "socle is the exception that proves the triad — the only type in the study whose socle "
        "takes in the whole ground floor."),
    origin_en=(
        "The PIIA's own summary: <em>« Les magasins, ouverts sur le trottoir par de grandes "
        "vitrines, sont clairement séparés des étages supérieurs par une frise continue. Les étages "
        "supérieurs sont généralement occupés par des logements. »</em>"),
),
"5": dict(
    slug="immeuble-vocation-commerciale", name_en="Commercial building", phase="p3", page=105,
    canonical=[], styles=["beaux-arts"],
    tenure_plan="mixed", storeys=None, roof={"form": None, "pitch_deg": None},
    window_proportion=None, principal_cladding=["clay-brick", "cut-stone"],
    roofing=None, garage="none", is_residential=False,
    lot_width_m=None, setback_front_m=None, setback_side_m=None, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=["On the borough's main arteries."],
        massing=["Not characterised: the study says the type is too differentiated to describe."],
        articulation=[
            "Generally designed by architects and possessing an architectural language of their own.",
            "On a corner the side façade keeps the same rules of composition as the principal one.",
        ],
        openings=["Not characterised in the study."],
        materials=["Not characterised in the study."]),
    example_addresses=[
        {"address": "boulevard Monk, at rue du Parc-Garneau", "note": "the édifice de la banque Laurentienne (SO3635)"},
    ],
    blurb_en=(
        "Recorded as the study records it, which is to say barely: « En raison de la grande "
        "différenciation des bâtiments de ce type, il n’a pas fait l’objet d’une attention "
        "particulière dans cette description typologique. » Non-residential, so no card."),
    origin_en="Family 5 of seven. Kept in the record so the type list is complete and honest about its gaps.",
),
"6": dict(
    slug="immeuble-vocation-industrielle", name_en="Industrial building", phase="p2", page=107,
    canonical=[], styles=["rationalisme-industriel"],
    tenure_plan="mixed", storeys=None, roof={"form": None, "pitch_deg": None},
    window_proportion=None, principal_cladding=["clay-brick"],
    roofing=None, garage="none", is_residential=False,
    lot_width_m=None, setback_front_m=None, setback_side_m=None, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Around the canal de Lachine and in every sector near the railways, which kept a coarse-grained urban fabric given over to industry.",
        ],
        massing=["Great architectural simplicity; siting and cladding are both variable."],
        articulation=[
            "Openings arranged in regular alignment, and the structural elements form the principal ornament.",
        ],
        openings=["Regular alignments; not otherwise characterised."],
        materials=["Variable; the study does not characterise them."]),
    example_addresses=[
        {"address": "225, rue Bridge", "note": "the Postes Canada building (SO1606)"},
    ],
    blurb_en=(
        "Recorded, not carded. The industrial fabric is the reason the borough exists, and the "
        "Évaluation cahier gives it a whole grade of its own — the two secteurs industriels "
        "d'intérêt 22.N.1 and 22.N.2 — but the typo-morphological study leaves it deliberately "
        "undescribed: « Ce type n’a pas fait l’objet d’une description complète dans cette "
        "description typologique. »"),
    origin_en="Family 6 of seven. Non-residential; the canal-side complexes are catalogued in sector 22.E.1 instead.",
),
"7": dict(
    slug="immeuble-vocation-institutionnelle", name_en="Institutional building", phase="p3", page=109,
    canonical=[], styles=["beaux-arts", "neogothique"],
    tenure_plan="mixed", storeys=None, roof={"form": None, "pitch_deg": None},
    window_proportion=None, principal_cladding=["clay-brick", "cut-stone"],
    roofing=None, garage="none", is_residential=False,
    lot_width_m=None, setback_front_m=None, setback_side_m=None, front_yard_green_pct=None,
    profile=dict(
        siting_landscape=[
            "Distributed across the whole borough. They can form complexes filling a whole block — the study's example is the école secondaire Saint-Henri, in the block bounded by rues Saint-Ferdinand, du Couvent, Saint-Jacques and Saint-Antoine Ouest — or be inserted inside the residential fabric.",
        ],
        massing=["Large buildings, singular monuments designed by architects."],
        articulation=["Not characterised: the study treats them as exceptions in the fabric rather than base elements."],
        openings=["Not characterised in the study."],
        materials=["Not characterised in the study."]),
    example_addresses=[
        {"address": "110-154, avenue Atwater", "note": "the marché Atwater (SO1526)"},
        {"address": "625, rue Fortune", "note": "Grace Church (SO1610)"},
    ],
    blurb_en=(
        "Recorded, not carded. Churches, schools, hospitals, public baths and libraries, which the "
        "study excludes on principle: « ils constituent des exceptions dans le tissu urbain "
        "plutôt que des éléments de base »."),
    origin_en="Family 7 of seven. Non-residential; the borough's institutional cores are carried in the sector records.",
),
}

FAMILY = {"1": "1. La maison unifamiliale", "2": "2. L'immeuble de type plex",
          "3": "3. L'immeuble d'appartements", "4": None, "5": None, "6": None, "7": None}

# Sector codes each type is cited in, from the Évaluation cahier's sector texts.
SECTORS = {
    "1.1": ["22.E.11", "AIRE-4"],
    "1.2": ["22.E.4", "22.E.5", "22.E.11", "AIRE-1"],
    "1.3": ["AIRE-3"],
    "1.4": ["AIRE-3"],
    "1.5": ["AIRE-1"],
    "2.1": ["AIRE-2", "AIRE-4"],
    "2.2": ["AIRE-3"],
    "2.3": ["AIRE-3"],
    "2.4": ["22.E.4", "AIRE-2", "AIRE-5"],
    "2.5": ["AIRE-1", "AIRE-2"],
    "2.6": ["22.E.6", "22.E.7", "AIRE-2", "AIRE-4"],
    "2.7": ["AIRE-4", "AIRE-5"],
    "3.1": ["AIRE-3"],
    "3.2": ["AIRE-1", "AIRE-3"],
    "3.3": ["AIRE-3", "AIRE-5"],
    "4": ["AIRE-2", "AIRE-3"],
    "5": ["AIRE-3"],
    "6": ["22.E.1", "22.AP.5"],
    "7": ["22.E.10", "22.E.15"],
}

LABEL = {"socle": "Socle", "corps": "Corps", "couronnement": "Couronnement",
         "ornementation": "Ornementation"}
ORDER = ["socle", "corps", "couronnement", "ornementation"]


class Dumper(yaml.SafeDumper):
    pass


def _str(dumper, data):
    style = ">" if len(data) > 95 and "\n" not in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


Dumper.add_representer(str, _str)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    recs = {r["code"]: r for r in json.loads(PARSED.read_text(encoding="utf-8"))}
    written = []
    for code, m in META.items():
        r = recs[code]
        triad = r["traitement_triad"]
        pfr = {
            "implantation": r["profile_fr"]["implantation"],
            "volumetrie": r["profile_fr"]["volumetrie"],
            "materiaux": r["profile_fr"]["materiaux"],
            "traitement_des_facades": [f"{LABEL[k]} — {b}" for k in ORDER for b in triad[k]],
            "ouvertures": r["profile_fr"]["ouvertures"],
            "description": r["identification_fr"],
            "contexte": [p for p in r["contexte_fr"] if not p[0].isdigit()],
        }
        pfr = {k: v for k, v in pfr.items() if v}
        variants = [f"Variante {v['n']} — {v['title_fr']} : {v['description_fr']}"
                    for v in r["variants"]] or None
        # `variants` is the structural home for section D, but the card template does not yet
        # render it, so the same text is also placed in profile_fr.sous_variantes, which does.
        if variants:
            pfr["sous_variantes"] = variants
        doc_ref = f"{DOC}, type {code} — {r['name_fr']}, printed p. {m['page']}"
        t = {
            "id": f"sud-ouest.{m['slug']}",
            "place": "sud-ouest",
            "page": m["page"],
            "phase": m["phase"],
            "phase_confidence": "verified",
            "name_en": m["name_en"],
            "name_fr": r["name_fr"],
            "courant": FAMILY[code.split(".")[0]],
            "source_ref": doc_ref,
            "source_url": STUDY_URL,
            "source_generation": (
                "Parsed from the study's own fiche by sources/sud-ouest/parse.py and written by "
                "sources/sud-ouest/encode_types.py. profile_fr is the source text verbatim, section "
                "by section; C.4 is split into Patri-Arch's socle / corps / couronnement triad and "
                "each entry is labelled with the division it belongs to. The English profile is ours."),
            "sectors": SECTORS[code],
            "canonical": m["canonical"],
            "styles": m["styles"],
            "style_label": None,
            "tenure_plan": m["tenure_plan"],
            "storeys": m["storeys"],
            "roof": m["roof"],
            "window_proportion": m["window_proportion"],
            "principal_cladding": m["principal_cladding"],
            "roofing": m["roofing"],
            "garage": m["garage"],
            "lot_width_m": m["lot_width_m"],
            "setback_front_m": m["setback_front_m"],
            "setback_side_m": m["setback_side_m"],
            "front_yard_green_pct": m["front_yard_green_pct"],
            "count_in_place": m.get("count_in_place"),
            "is_residential": m.get("is_residential", True),
            "profile": m["profile"],
            "profile_fr": pfr,
            "profile_note": m.get("profile_note"),
            "variants": variants,
            "example_addresses": m.get("example_addresses"),
            "related_buildings": m.get("related_buildings"),
            "conservation": [],
            "photos": m.get("photos") or fig(code, r["identification_fr"][0][:120] + "…"),
            "blurb_en": m["blurb_en"],
            "origin_en": m["origin_en"],
        }
        t = {k: v for k, v in t.items() if v is not None or k in
             ("storeys", "roofing", "lot_width_m", "setback_front_m", "setback_side_m",
              "front_yard_green_pct", "window_proportion", "garage", "profile_note")}
        path = OUT / f"{m['slug']}.yaml"
        path.write_text(
            "# Written by sources/sud-ouest/encode_types.py — edit that file, not this one.\n"
            "# profile_fr is verbatim Patri-Arch; the English profile, blurb and origin are ours.\n"
            + yaml.dump(t, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=98),
            encoding="utf-8")
        written.append(path.name)
    print(f"wrote {len(written)} type files to {OUT}")
    res = [c for c in META if META[c].get("is_residential", True)]
    print(f"  residential (carded): {len(res)} — {sorted(res)}")
    print(f"  non-residential (recorded only): {sorted(set(META) - set(res))}")


if __name__ == "__main__":
    main()
