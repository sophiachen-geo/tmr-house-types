#!/usr/bin/env python3
"""Generate data/places/levis/types/*.yaml from sources/levis/parsed.json.

Every French string written into `profile_fr` comes straight out of the parse —
nothing is typed by hand here, so an empty card is impossible unless the parser
itself failed. The English `profile` lists are translations of those same
strings, held in TRANSLATION below and keyed by fiche id + field label, and the
encoder refuses to run if a translation is missing or if the French it was
written against has changed since (see `checked_fr`).

Run:  python3 sources/levis/encode.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PARSED = HERE / "parsed.json"
OUTDIR = ROOT / "data" / "places" / "levis" / "types"

BASE = ("https://www.ville.levis.qc.ca/developpement-planification/"
        "architecture-patrimoniale/styles-architecturaux/")
BROCHURE = "https://www.ville.levis.qc.ca/fileadmin/Documents_PDF/brochure-vieux-levis-a-pied.pdf"

# The City's conditions d'utilisation, read 2026-08-16, forbid republication to
# third parties, so no fiche image is copied into assets/. One placeholder per
# record carries the credit; the full per-image list stays in parsed.json.
TERMS = ("Not reproduced: the Ville de Lévis conditions d'utilisation state "
         "« Il vous est interdit de copier ou de publier, pour rediffusion à des tiers "
         "ou à des fins commerciales, la moindre partie du contenu. »")

# label -> the profile_fr key build.py maps onto each English column
FR_KEY = {"Volumétrie": "volumetrie", "Plan": "plan", "Toiture": "toiture",
          "Revêtements": "revetements", "Ouvertures": "ouvertures",
          "Saillies": "saillies", "Ornementation": "ornementation"}

# ---------------------------------------------------------------------------
# Per-courant encoding. `fr` repeats the French the translation was written
# against; encode.py aborts if the live parse no longer matches it.
# ---------------------------------------------------------------------------
T = {}


def courant(fiche_id, **kw):
    T[fiche_id] = kw


courant(16, slug="regime-francais", name_en="French-regime house (Régime français)",
        phase="p1", phase_confidence="verified",
        canonical=["french-rural-house-1st-hip", "french-urban-house-stone"],
        styles=["french-regime"], tenure_plan="single-family", storeys="1.5",
        roof_form="gabled-or-hipped", roof_pitch=None, window_proportion=None,
        cladding=["fieldstone", "stucco-render", "wood-clapboard", "wood-vertical-board"],
        roofing="wood shingle", garage=None,
        en={
            "Volumétrie": "One and a half storeys, sitting very low to the ground.",
            "Plan": "Rectangular plan.",
            "Toiture": "Two-slope or hipped roof of steep pitch, with a barely projecting eaves overhang, covered in wood shingle.",
            "Revêtements": "Massive stone walls, sometimes rendered in stucco or clad in wood clapboard or vertical boarding.",
            "Ouvertures": "Casement windows with small panes, few in number and asymmetrically placed; small dormers added in the 19th century.",
            "Saillies": "One or more large stone chimneys.",
            "Ornementation": "Plain window and door surrounds; stripped-back decoration.",
        },
        blurb="One and a half storeys sitting almost on the ground under a steep two-slope or hipped roof with barely any eaves overhang. Walls are massive stone, sometimes rendered or boarded over. Windows are few, small-paned casements, set without symmetry; a large stone chimney is the only projection.",
        origin="The oldest of the twenty currents in the City's catalogue, covering the French colonial period on the seigneurie de Lauzon, granted to Jean de Lauson in 1636 and settled at Pointe-Lévy from 1647. The City counts about fifteen buildings of this kind across the whole merged territory — the smallest surviving group in the catalogue, and the reason so little of Lévis reads as pre-Conquest today.")

courant(11, slug="franco-quebecois", name_en="Franco-Québécois transitional house",
        phase="p2", phase_confidence="verified",
        canonical=["transition-franco-quebecoise"],
        styles=["french-regime", "neoclassical-quebec"], tenure_plan="single-family",
        storeys="1.5", roof_form="bellcast", roof_pitch=None, window_proportion=None,
        cladding=["fieldstone", "stucco-render", "wood-clapboard", "wood-shingle"],
        roofing="wood shingle or tôle à la canadienne", garage=None,
        en={
            "Volumétrie": "One and a half storeys, sitting low to the ground.",
            "Plan": "Rectangular plan.",
            "Toiture": "Two-slope roof with a curved bellcast eave, of steep pitch, covered in wood shingle or Canadian-pan tin.",
            "Revêtements": "Stone, stucco render, wood clapboard or wood shingle.",
            "Ouvertures": "Casement windows with small or large panes, symmetrically placed; gabled dormers.",
            "Saillies": "Chimney; entrance stoop.",
            "Ornementation": "Window and door surrounds; corner boards where the cladding is wood.",
        },
        blurb="The step between the French-regime house and the Québécois house: still one and a half storeys and low to the ground, but the eaves now curve out in a bellcast and the windows line up symmetrically. Stone, render, clapboard or shingle; a chimney and a stoop.",
        origin="The transitional form of the decades either side of 1800, when Pointe-Lévy was a ferry landing and the shipyards at Lauzon were beginning. The bellcast eave that defines it is the single feature that separates it from the French-regime house behind it and connects it to the Québécois house that follows. About fifty are counted city-wide.")

courant(2, slug="quebecois", name_en="Québécois traditional house",
        phase="p2", phase_confidence="verified",
        canonical=["quebec-traditional-1-5st-gable"], styles=["neoclassical-quebec"],
        tenure_plan="single-family", storeys="1.5–2.5", roof_form="bellcast",
        roof_pitch=None, window_proportion=None,
        cladding=["wood-clapboard", "wood-shingle"],
        roofing="tôle à la canadienne or standing-seam tin", garage=None,
        en={
            "Volumétrie": "One and a half to two and a half storeys, raised slightly above the ground.",
            "Plan": "Rectangular plan.",
            "Toiture": "Two-slope roof with a curved bellcast base, of medium pitch, in Canadian-pan or standing-seam tin.",
            "Revêtements": "Wood clapboard or wood shingle.",
            "Ouvertures": "Casement windows of four and six panes, plentiful and symmetrical; one or more gabled dormers.",
            "Saillies": "Covered veranda — sheltered by the bellcast eave or by an independent awning — and a chimney.",
            "Ornementation": "Window and door surrounds and corner boards; a doorcase; veranda trim (knee braces, railings).",
        },
        blurb="The house that gives Lévis its street picture: one and a half to two and a half storeys, raised a little off the ground, under a medium-pitched two-slope roof whose curved base carries out over a covered veranda. Clapboard or shingle walls, four- and six-pane casements set symmetrically, gabled dormers, and carpentered trim on the surrounds, corner boards and veranda.",
        origin="At about seven hundred buildings this is the second most numerous current in the catalogue, and the one the City's own walking-tour brochure uses to explain how the Norman house of the colonists became something Québécois. The brochure reads the maison Lefrançois at 39 rue Wolfe as exactly that evolution — dormers cut into the roof and clapboard on the walls — and the maison Pampalon at 40 rue Wolfe as its later stage, where the ground floor lifts far enough to make the basement usable.",
        related=[
            {"name": "Maison Lefrançois, 39 rue Wolfe, Vieux-Lévis — « Cette maison illustre l'évolution de la maison normande, héritage des colons en Nouvelle-France, vers un style proprement canadien » (Le Vieux-Lévis à pied, stop 18)", "url": BROCHURE},
            {"name": "Maison Pampalon, 40 rue Wolfe, Vieux-Lévis — « nous reprenons ici l'évolution du style québécois avec une surélévation davantage marquée du premier plancher » (Le Vieux-Lévis à pied, stop 19)", "url": BROCHURE},
        ],
        siting_extra="Documented in Vieux-Lévis on rue Wolfe by the City's walking-tour brochure Le Vieux-Lévis à pied (maison Lefrançois, 39; maison Pampalon, 40).",
        sectors=["PIIA-LEVIS"])

courant(18, slug="regency", name_en="Regency cottage",
        phase="p2", phase_confidence="verified",
        canonical=["regency-cottage-hipped-veranda"], styles=["regency"],
        tenure_plan="single-family", storeys="1.5–2.5", roof_form="hipped",
        roof_pitch=None, window_proportion=None,
        cladding=["wood-clapboard", "wood-shingle", "clay-brick"],
        roofing="wood shingle or standing-seam tin", garage=None,
        en={
            "Volumétrie": "One and a half or two and a half storeys.",
            "Plan": "Square plan.",
            "Toiture": "Hipped (four-slope) pavilion roof with a curved bellcast base, in wood shingle or standing-seam tin.",
            "Revêtements": "Wood clapboard or wood shingle; brick.",
            "Ouvertures": "Casement windows of six large panes; gabled or hipped dormers; symmetrical arrangement.",
            "Saillies": "Veranda sheltered by the roof overhang; chimneys.",
            "Ornementation": "Window and door surrounds, corner boards, entrance doorcase.",
        },
        blurb="Square in plan under a four-slope pavilion roof whose curved base runs out over a veranda on every side. Six-pane casements arranged symmetrically, gabled or hipped dormers, and clapboard, shingle or brick walls.",
        origin="The British officer's cottage as it was built on the south shore facing Québec, and one of the rarest currents in the catalogue at about fifteen buildings. The RPCQ's description of the cited site at Saint-Nicolas names the Regency among the « manifestations d'architecture pittoresque » that give that ensemble its character.")

courant(17, slug="neogothique", name_en="Neo-Gothic",
        phase="p2", phase_confidence="provisional",
        canonical=["detached-cottage-steep-gable"], styles=["neogothique"],
        tenure_plan="single-family", storeys="1.5–2.5", roof_form="gabled",
        roof_pitch=None, window_proportion="vertical",
        cladding=["clay-brick", "fieldstone", "wood-clapboard"],
        roofing="tôle à la canadienne or wood shingle", garage=None,
        en={
            "Volumétrie": "One and a half to two and a half storeys.",
            "Plan": "Irregular plan.",
            "Toiture": "Steeply pitched two-slope roof in Canadian-pan tin or wood shingle.",
            "Revêtements": "Brick, stone or wood clapboard.",
            "Ouvertures": "Pointed-arch openings; vertical openings of varied pattern.",
            "Saillies": "Bell tower, projecting bays, buttresses, pilasters, pinnacles.",
            "Ornementation": "String courses, friezes, patterned brick or stonework, stained glass, a doorcase, decorative woodwork.",
        },
        blurb="Steep two-slope roofs over an irregular plan, with pointed-arch openings and vertical windows of varied pattern. The City's own line drawing for this current is a chapel, and its projections — bell tower, buttresses, pinnacles — are ecclesiastical; the domestic version reads through the same steep gables and decorative bargeboards.",
        origin="Lévis's best-known Neo-Gothic building is a house: the maison Alphonse-Desjardins of 1882–1884, where the first caisse populaire was founded in 1900. The RPCQ describes it as « une habitation de style néogothique… de plan asymétrique en forme de « L », à un étage et demi… coiffée d'un toit à deux versants ponctué de deux pignons en façade », and it was classed an immeuble patrimonial on 21 March 1983. The City's fiche spans 1830 to 1940, a reach of over a century, so the phase placement here follows the opening date and is marked provisional.",
        related=[
            {"name": "Maison Alphonse-Desjardins, 8 rue du Mont-Marie, Lévis (1882–1884), classed immeuble patrimonial 21 March 1983 — RPCQ 92424", "url": "https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&id=92424&type=bien"},
            {"name": "Carré Déziel and the maison historique Alphonse-Desjardins — « Cette coquette résidence d'esprit victorien démontre une inspiration néogothique par les nombreux éléments décoratifs tels les dentelles de bois et les pignons » (Le Vieux-Lévis à pied, stops 11–12)", "url": BROCHURE},
        ],
        siting_extra="Documented in Vieux-Lévis at the carré Déziel by the City's walking-tour brochure Le Vieux-Lévis à pied.",
        sectors=["PIIA-LEVIS"])

courant(9, slug="neoclassique", name_en="Neoclassical house",
        phase="p2", phase_confidence="verified",
        canonical=["eclectic-prestige-house"], styles=["neoclassical-quebec"],
        tenure_plan="single-family", storeys="2–3", roof_form="gabled-or-hipped",
        roof_pitch=None, window_proportion=None,
        cladding=["clay-brick", "cut-stone", "wood-clapboard"],
        roofing="standing-seam tin", garage=None,
        en={
            "Volumétrie": "Two to three storeys.",
            "Plan": "Rectangular plan.",
            "Toiture": "Straight two-slope or hipped roof in standing-seam tin.",
            "Revêtements": "Brick or cut stone on the principal façade, wood clapboard on the secondary elevations.",
            "Ouvertures": "Sash or casement windows with large panes, symmetrically arranged; gabled or hipped dormers.",
            "Saillies": "Chimneys; gables that observe the symmetry.",
            "Ornementation": "Window and door surrounds, pediments, doorcases, cornices, pilasters.",
        },
        blurb="Two to three storeys under a straight two-slope or hipped tin roof, faced in brick or cut stone at the front and clapboard down the sides — a distinction of expense that the fiche records plainly. Large-paned windows in strict symmetry, and pediments, cornices and pilasters at the door.",
        origin="The idiom of the Lévis bourgeoisie in the decades around incorporation in 1861. Its public monument is the église Notre-Dame-de-la-Victoire of 1851 on plans by Thomas Baillargé, which the City's walking-tour brochure calls « un chef-d'œuvre néoclassique » and reads through its four Doric pilasters carrying a pediment.",
        related=[
            {"name": "Église Notre-Dame-de-la-Victoire, carré Déziel, Vieux-Lévis (1851, Thomas Baillargé), classed — « L'architecture de l'église est considérée comme un chef-d'œuvre néoclassique » (Le Vieux-Lévis à pied, stop 13)", "url": BROCHURE},
            {"name": "Collège de Lévis, 9 rue Mgr-Gosselin, founded 1853 by curé Joseph-David Déziel (Le Vieux-Lévis à pied, stop 14)", "url": BROCHURE},
        ],
        siting_extra="Documented in Vieux-Lévis around the carré Déziel by the City's walking-tour brochure Le Vieux-Lévis à pied.",
        sectors=["PIIA-LEVIS"])

courant(8, slug="agricole-vernaculaire", name_en="Agricultural vernacular building",
        phase="p2", phase_confidence="provisional",
        canonical=["industrial-vernacular-cottage"], styles=["agricole-vernaculaire"],
        tenure_plan="single-family", storeys="1.5–2.5", roof_form="gabled",
        roof_pitch=None, window_proportion=None,
        cladding=["wood-vertical-board", "wood-shingle"],
        roofing="wood shingle or barn tin", garage=None,
        en={
            "Volumétrie": "One and a half to two and a half storeys.",
            "Plan": "Rectangular plan.",
            "Toiture": "Straight two-slope roof, sometimes mansarded, in wood shingle or barn tin.",
            "Revêtements": "Vertical wood boarding or wood shingle.",
            "Ouvertures": "Large hinged or sliding (track-hung) doors; windows with large panes.",
            "Saillies": "Roof vent, lean-to volumes, silo.",
            "Ornementation": "Sober; window and door surrounds; a weathervane.",
        },
        blurb="The rural building of the merged territory: a long rectangle of vertical boarding or shingle under a straight two-slope roof, sometimes mansarded, with big hinged or track-hung doors, a roof vent, lean-to additions and a silo.",
        origin="Rural rather than urban, and included here because Lévis's 2002 merger of ten municipalities brought a large farming territory inside one city boundary — Saint-Étienne, Saint-Nicolas, Pintendre, Breakeyville and Vire-Crêpes all carry PIIA heritage sectors of this kind. The RPCQ's cited site at Saint-Nicolas is itself described as « un ensemble continu de propriétés agricoles ». About a hundred are counted.",
        profile_note_extra="Rural rather than urban: the fiche describes farm buildings, and its openings row is about barn doors rather than windows.")

courant(13, slug="batiment-accessoire", name_en="Accessory building (other than agricultural)",
        phase="p2", phase_confidence="provisional", is_residential=False,
        canonical=[], styles=[], tenure_plan="single-family", storeys="1–1.5",
        roof_form="gabled", roof_pitch=None, window_proportion=None,
        cladding=["wood-vertical-board", "wood-clapboard", "wood-shingle"],
        roofing=None, garage="detached",
        en={
            "Volumétrie": "One to one and a half storeys.",
            "Plan": "Rectangular plan.",
            "Toiture": "Two-slope roof of shallow pitch.",
            "Revêtements": "Vertical wood boarding, wood clapboard or wood shingle.",
            "Ouvertures": "Garage door; fixed windows.",
            "Saillies": "None.",
            "Ornementation": "Sober; window and door surrounds and corner boards.",
        },
        blurb="The catalogue's entry for garages, sheds and other outbuildings that are not farm buildings: one to one and a half storeys, shallow two-slope roof, boarded or shingled walls, a garage door and fixed lights, and no projections at all.",
        origin="One of the two entries the catalogue files under « Autre type », and one of only two of the twenty that carry no « Nombre à Lévis » figure. It is recorded here because it is part of the published catalogue, but it is not a dwelling and gets no card.",
        profile_note_extra="Not a dwelling: recorded from the catalogue and exported, but not rendered as a type card.")

courant(20, slug="rationalisme-industriel", name_en="Industrial rationalism",
        phase="p2", phase_confidence="provisional", is_residential=False,
        canonical=[], styles=["rationalisme-industriel"], tenure_plan="mixed",
        storeys="1–5", roof_form="flat-or-low-slope", roof_pitch=None,
        window_proportion=None,
        cladding=["fieldstone", "clay-brick", "stucco-render", "concrete", "sheet-metal"],
        roofing=None, garage=None,
        en={
            "Volumétrie": "One to five storeys.",
            "Plan": "Rectangular or complex plan.",
            "Toiture": "Flat or straight two-slope roof.",
            "Revêtements": "Stone, brick, stucco render, concrete, metal cladding.",
            "Ouvertures": "Large windows or garage doors.",
            "Saillies": "Chimneys, annexe volumes.",
            "Ornementation": "Sober.",
        },
        blurb="One to five storeys, flat or straight-gabled, in stone, brick, render, concrete or sheet metal, with large windows or vehicle doors and nothing decorative about it. The building type of the Davie yards at Lauzon and the railway works.",
        origin="The industrial current of a shipbuilding and railway town — the Davie yard at Lauzon has been building ships since 1829 — and the only entry in the catalogue that the City gives a style but no house form. Not a dwelling, so it is recorded and exported but gets no card.",
        profile_note_extra="Not a dwelling: recorded from the catalogue and exported, but not rendered as a type card.")

courant(5, slug="second-empire", name_en="Second Empire house",
        phase="p3", phase_confidence="verified",
        canonical=["mansard-house-2st"], styles=["second-empire"],
        tenure_plan="single-family", storeys="2–3", roof_form="mansard",
        roof_pitch=None, window_proportion=None,
        cladding=["clay-brick", "wood-clapboard", "wood-shingle"],
        roofing="standing-seam tin on the terrasson, tôle à la canadienne on the brisis",
        garage=None,
        en={
            "Volumétrie": "Two to three storeys.",
            "Plan": "Rectangular plan.",
            "Toiture": "Mansard roof of two or four slopes, standing-seam tin on the flat upper deck (terrasson) and Canadian-pan tin on the steep lower slope (brisis).",
            "Revêtements": "Brick, wood clapboard or wood shingle.",
            "Ouvertures": "Casement windows of four and six panes and, more rarely, sash windows; gabled or round-headed dormers.",
            "Saillies": "Chimney; covered veranda.",
            "Ornementation": "Window and door surrounds, corner boards, decorative woodwork and veranda trim.",
        },
        blurb="Two to three storeys under a mansard whose two tin finishes are specified separately — standing seam on the flat deck above, Canadian pan on the steep slope below. Four- and six-pane casements, gabled or round-headed dormers, a covered veranda and carpentered trim.",
        origin="At about 450 buildings, one of the four big currents in the catalogue, and the form of the Lévis of the railway decades after 1870. The old hôtel de ville, demolished in 1965 and shown in the City's walking-tour brochure on the site of the present parc Joseph-Godéric-Blanchet, was Second Empire.")

courant(7, slug="victorien", name_en="Victorian house",
        phase="p3", phase_confidence="verified",
        canonical=["queen-anne-irregular-2-5st"], styles=["victorian-eclectic", "queen-anne"],
        tenure_plan="single-family", storeys="2–3", roof_form="gabled-multi",
        roof_pitch=None, window_proportion=None,
        cladding=["wood-clapboard", "wood-shingle-cut", "clay-brick"],
        roofing="standing-seam tin", garage=None,
        en={
            "Volumétrie": "Two to three storeys, well raised above the ground.",
            "Plan": "Complex, articulated plan with projecting bays.",
            "Toiture": "Two- and four-slope roofs in standing-seam tin.",
            "Revêtements": "Wood clapboard, cut (fancy-butt) wood shingle, brick.",
            "Ouvertures": "Windows and dormers of varied pattern, sometimes paired.",
            "Saillies": "Turret, veranda, gable, chimney, balcony, oriel.",
            "Ornementation": "Very heavily loaded, with decorative woodwork — surrounds, finial mast, knee braces, valances, cornices, frieze and the like.",
        },
        blurb="Two to three storeys well up off the ground on a complex articulated plan, broken by turrets, oriels, balconies and gables, and covered in decorative woodwork — the fiche calls the ornament « très chargée » and then lists seven kinds of it.",
        origin="The City's walking-tour brochure points to the three houses at 20, 22-26 and 28 rue Guenette — « le trio victorien » — as « un des ensembles architecturaux les plus intéressants du Québec », reading them through bichrome brick at the quoins and entablements, imitation keystones over the lintels, arched windows and elaborated gables.",
        related=[
            {"name": "Le trio victorien, 20, 22-26 and 28 rue Guenette, Vieux-Lévis — « Un des ensembles architecturaux les plus intéressants du Québec » (Le Vieux-Lévis à pied, stop 10)", "url": BROCHURE},
            {"name": "Résidences jumelles de la famille Roy, 2-12 rue Wolfe, Vieux-Lévis (Le Vieux-Lévis à pied, stop 16)", "url": BROCHURE},
        ],
        siting_extra="Documented in Vieux-Lévis on rue Guenette and rue Wolfe by the City's walking-tour brochure Le Vieux-Lévis à pied.",
        sectors=["PIIA-LEVIS"])

courant(1, slug="vernaculaire-americain", name_en="American vernacular house",
        phase="p3", phase_confidence="verified",
        canonical=["industrial-vernacular-cottage"], styles=["vernaculaire-industriel"],
        tenure_plan="single-family", storeys="1.5–2", roof_form="gabled",
        roof_pitch=None, window_proportion=None,
        cladding=["wood-clapboard", "wood-shingle", "asbestos-cement-tile"],
        roofing="standing-seam tin", garage=None,
        en={
            "Volumétrie": "One and a half or two storeys, well raised above the ground.",
            "Plan": "Rectangular plan, sometimes L-shaped.",
            "Toiture": "Straight two-slope roof in standing-seam tin, of medium to shallow pitch.",
            "Revêtements": "Wood clapboard or wood shingle; diamond-pattern asbestos-cement tiles.",
            "Ouvertures": "Large-paned casement windows or sash windows; gabled or shed dormers.",
            "Saillies": "Veranda covered by an independent awning.",
            "Ornementation": "Window and door surrounds, corner boards, veranda trim, cornice returns.",
        },
        blurb="At about 1,700 buildings the most numerous current in Lévis by a wide margin: one and a half or two storeys well clear of the ground, rectangular or L-shaped, under a straight tin roof of medium to shallow pitch, with a veranda under its own separate awning.",
        origin="The workers' house of the industrial south shore, and the plainest demonstration of what the catalogue is for — one form accounting for more than a third of the 4,000-odd heritage buildings the City counts. The diamond-pattern asbestos-cement tile the fiche names as a cladding is the same material it lists for Boomtown, and marks the interwar re-skinning of both.")

courant(12, slug="batiment-mixte", name_en="Mixed-use or commercial building",
        phase="p3", phase_confidence="provisional", is_residential=False,
        canonical=["mixed-use-flat-roof-block"], styles=["boomtown"],
        tenure_plan="mixed", storeys="2–3", roof_form="flat-or-low-slope",
        roof_pitch=None, window_proportion=None, cladding=["clay-brick"],
        roofing=None, garage=None,
        en={
            "Volumétrie": "Two or three storeys.",
            "Plan": "Rectangular plan.",
            "Toiture": "Flat roof or straight two-slope roof.",
            "Revêtements": "Brick.",
            "Ouvertures": "Shop windows and commercial doors with transoms at ground-floor level.",
            "Saillies": "Signage cornice, signs, retractable awnings.",
            "Ornementation": "Modillion cornice, decorative woodwork.",
        },
        blurb="The main-street block of the côte du Passage and the avenue Bégin: two or three storeys of brick, flat-roofed or shallow-gabled, with shop windows and transomed commercial doors below and a signage cornice, signs and retractable awnings above.",
        origin="The second of the catalogue's two « Autre type » entries and, like the first, one of only two of the twenty that carry no « Nombre à Lévis » figure. Every one of its seven fields describes commerce — vitrines, portes commerciales, corniche d'affichage, enseignes, auvents rétractables — with no dwelling feature named, so it is recorded and exported but gets no card. The City's walking-tour brochure notes that the édifice Laurentien on rue Guenette « jumelle aujourd'hui les vocations commerciale et résidentielle », which is the mixed use the name promises.",
        profile_note_extra="Not encoded as a dwelling: the fiche's seven fields describe shopfronts and signage only, and the catalogue files this entry under « Autre type ». Recorded and exported, but not rendered as a type card. This departs from the Part 8 brief, which listed it « yes, mixed-use »; see the place notes.")

courant(15, slug="beaux-arts", name_en="Beaux-Arts house",
        phase="p4", phase_confidence="verified",
        canonical=["eclectic-prestige-house"], styles=["beaux-arts"],
        tenure_plan="single-family", storeys="2–3", roof_form="flat",
        roof_pitch=None, window_proportion=None, cladding=["clay-brick", "cut-stone"],
        roofing=None, garage=None,
        en={
            "Volumétrie": "Two or three storeys.",
            "Plan": "Rectangular plan.",
            "Toiture": "Flat roof.",
            "Revêtements": "Brick or stone.",
            "Ouvertures": "Rectangular or arched windows with transoms, sometimes grouped; symmetrical arrangement.",
            "Saillies": "Covered veranda.",
            "Ornementation": "Modillion cornice, balustrade, quoins, doorcase, pediment, window surrounds, keystone, columns and pilasters.",
        },
        blurb="Two or three storeys of brick or stone under a flat roof, symmetrical, with a covered veranda and the longest ornament list in the catalogue — modillion cornice, balustrade, quoins, doorcase, pediment, keystone, columns and pilasters.",
        origin="A prestige house rather than a public building: the City's line drawing for this current is a two-storey dwelling with a veranda, quoins and a modillion cornice, and its worked example is 55 avenue Bégin. The walking-tour brochure's maison Lasnier at 44 rue Wolfe, rebuilt in 1910 down to the basement in a « style éclectique d'inspiration palladienne », is the same idea. About ten are counted.",
        related=[
            {"name": "Maison Lasnier, 44 rue Wolfe, Vieux-Lévis — « Le style éclectique d'inspiration palladienne date seulement de 1910 » (Le Vieux-Lévis à pied, stop 20)", "url": BROCHURE},
        ],
        siting_extra="Documented in Vieux-Lévis on rue Wolfe and avenue Bégin by the City's walking-tour brochure Le Vieux-Lévis à pied.",
        sectors=["PIIA-LEVIS"])

courant(10, slug="boomtown", name_en="Boomtown house",
        phase="p4", phase_confidence="verified",
        canonical=["boomtown-false-front"], styles=["boomtown"],
        tenure_plan="single-family", storeys="1–2", roof_form="flat-or-low-slope",
        roof_pitch=None, window_proportion=None,
        cladding=["wood-clapboard", "wood-shingle", "asbestos-cement-tile"],
        roofing=None, garage=None,
        en={
            "Volumétrie": "One to two storeys.",
            "Plan": "Rectangular or square plan.",
            "Toiture": "Flat, or of very shallow pitch falling to the rear.",
            "Revêtements": "Wood clapboard or wood shingle; diamond-pattern asbestos-cement tiles.",
            "Ouvertures": "Multi-paned sash windows, symmetrically arranged.",
            "Saillies": "Parapet or cornice; covered veranda.",
            "Ornementation": "Corner boards and window surrounds; cornice elements.",
        },
        blurb="One to two storeys, square or rectangular, with the roof either flat or falling so gently to the rear that the street sees a straight line. A parapet or cornice finishes the front, a covered veranda fronts it, and corner boards and surrounds do the rest.",
        origin="The same form Saint-Lambert, Gatineau, Québec City and Trois-Rivières each describe in their own words — six independent municipal descriptions of one building. Lévis's fiche is the tersest of them and the only one that pins the shallow pitch to the rear slope explicitly. About a hundred are counted.")

courant(4, slug="cubique", name_en="Cubic house (maison cubique)",
        phase="p4", phase_confidence="verified",
        canonical=["foursquare-hipped-2st"], styles=["foursquare"],
        tenure_plan="single-family", storeys="2", roof_form="hipped-or-pyramidal",
        roof_pitch=None, window_proportion=None,
        cladding=["clay-brick", "wood-clapboard", "wood-shingle", "asbestos-cement-tile"],
        roofing="tôle à la canadienne or pincée", garage=None,
        en={
            "Volumétrie": "Two storeys.",
            "Plan": "Square plan.",
            "Toiture": "Four-slope or pavilion roof of shallow pitch, in Canadian-pan or pinched-seam tin.",
            "Revêtements": "Brick, wood clapboard or wood shingle; asbestos-cement tiles.",
            "Ouvertures": "Sash or casement windows with transoms; a central gabled or shed dormer.",
            "Saillies": "Covered veranda, sometimes on more than one elevation.",
            "Ornementation": "Sober; corner boards and window surrounds.",
        },
        blurb="Two storeys on a square plan under a shallow four-slope or pavilion roof, with a central dormer and a covered veranda that sometimes wraps a second face. Ornament is explicitly sober — corner boards and surrounds only.",
        origin="At about 450 buildings this is level with Second Empire as the third most numerous current. It is the same foursquare that Saint-Lambert, Gatineau, Québec City and Trois-Rivières each catalogue, and Lévis's version is distinguished by the veranda turning the corner.")

courant(3, slug="toit-plat", name_en="Flat-roofed house",
        phase="p4", phase_confidence="verified",
        canonical=["plex-superposed-units", "faubourg-house-flat-roof"],
        styles=["vernaculaire-industriel"], tenure_plan="walk-up", storeys="2–3",
        roof_form="flat", roof_pitch=None, window_proportion=None,
        cladding=["clay-brick", "wood-clapboard", "wood-shingle", "asbestos-cement-tile"],
        roofing=None, garage=None,
        en={
            "Volumétrie": "Two or three storeys.",
            "Plan": "Square or rectangular plan.",
            "Toiture": "Flat roof.",
            "Revêtements": "Brick, wood clapboard or wood shingle; asbestos-cement tiles.",
            "Ouvertures": "Sash or casement windows with transoms.",
            "Saillies": "Cornice or parapet; covered veranda.",
            "Ornementation": "Modillion cornice, window surrounds, corner boards, patterned brickwork, veranda trim.",
        },
        blurb="Two or three storeys, square or rectangular, flat-roofed, finished at the top by a cornice or parapet and at the front by a covered veranda — the superposed-dwelling form of the industrial faubourgs, and at about 600 buildings the third most numerous current in the catalogue.",
        origin="Where Boomtown hides a shallow slope behind a parapet, this current has no slope to hide: the flat roof is the type. It is the Lévis relative of the Montréal plex and of Gatineau's flat-roofed brick and wood houses, and the City's ornament list — modillion cornice, patterned brickwork, veranda trim — is the richest of the three flat-roofed currents it publishes.")

courant(14, slug="arts-et-metiers", name_en="Arts & Crafts house (Arts & métiers)",
        phase="p4", phase_confidence="verified",
        canonical=["detached-cottage-steep-gable"], styles=["arts-et-metiers", "arts-and-crafts"],
        tenure_plan="single-family", storeys="1.5–2", roof_form="gabled-multi",
        roof_pitch=None, window_proportion=None,
        cladding=["fieldstone", "clay-brick", "stucco-render", "wood-clapboard", "wood-shingle"],
        roofing=None, garage=None,
        en={
            "Volumétrie": "One and a half to two storeys.",
            "Plan": "Complex, articulated plan.",
            "Toiture": "Roofs of varied and complex form and pitch — two- or four-slope, hipped, half-hipped.",
            "Revêtements": "Natural materials: stone, brick, stucco render, wood clapboard or wood shingle, sometimes several materials combined.",
            "Ouvertures": "Windows and dormers of varied form and type.",
            "Saillies": "Covered verandas, chimneys, oriels.",
            "Ornementation": "Decorative woodwork.",
        },
        blurb="One and a half to two storeys on a complex articulated plan under roofs the fiche describes only as varied and complex, in natural materials — stone, brick, render, clapboard, shingle — often several at once. Verandas, chimneys and oriels project; the ornament is woodwork.",
        origin="Lévis says « Arts & métiers » where English-speaking Canada says Arts and Crafts, and the catalogue dates it 1910–1945. The insistence on « matériaux naturels » and on combining several of them is the movement's own argument, restated as a planning description. About sixty are counted.")

courant(6, slug="wartime-housing", name_en="Wartime housing dwelling",
        phase="p5", phase_confidence="verified",
        canonical=["wartime-housing-1940s"], styles=["wartime-housing", "minimal-traditional"],
        tenure_plan="single-family", storeys="1.5", roof_form="gabled",
        roof_pitch=None, window_proportion=None,
        cladding=["asbestos-cement-tile", "aluminium-clapboard", "masonite-clapboard"],
        roofing="asphalt shingle", garage=None,
        en={
            "Volumétrie": "One and a half storeys.",
            "Plan": "Rectangular or square plan.",
            "Toiture": "Straight two-slope, half-hipped or four-slope (pavilion) roof, in asphalt shingle.",
            "Revêtements": "Light claddings: asbestos-cement tiles, aluminium or masonite clapboard.",
            "Ouvertures": "Sash windows; gabled or shed dormers.",
            "Saillies": "Veranda, stoop, chimney.",
            "Ornementation": "Sober; a gable, ornamental ironwork on the veranda.",
        },
        blurb="One and a half storeys, rectangular or square, under asphalt shingle, in the light claddings that arrived with it — asbestos-cement tile, aluminium or masonite clapboard. A veranda or stoop, a chimney, and ornamental ironwork as the only decoration.",
        origin="Wartime Housing Limited's standard dwelling, built for shipyard and munitions workers and kept in production into the 1960s; the City dates the current 1940–1970 and counts about 200. It is the first current in the catalogue whose materials are all industrial products rather than wood, stone or tin, and the ornamental ironwork on the veranda is the period's signature.")

courant(19, slug="modernisme", name_en="Modernist building",
        phase="p5", phase_confidence="verified",
        canonical=["one-storey-ranch-low-roof", "modern-slab-tower"],
        styles=["international-style", "ranch"], tenure_plan="mixed",
        storeys="varies by use", roof_form="flat", roof_pitch=None,
        window_proportion="horizontal",
        cladding=["clay-brick", "concrete", "sheet-metal"], roofing=None, garage=None,
        en={
            "Volumétrie": "Varied, according to use.",
            "Plan": "Rectangular or complex plan.",
            "Toiture": "Flat roof.",
            "Revêtements": "Brick, concrete, metal cladding.",
            "Ouvertures": "Varied and repetitive, in horizontal bands.",
            "Saillies": "Annexe volumes.",
            "Ornementation": "Sober.",
        },
        blurb="Flat-roofed, brick, concrete or metal-clad, with openings set in repeating horizontal bands. The one current in the catalogue whose massing the City declines to fix at all — « diversifiée selon l'usage » — because the same language served houses, schools and offices.",
        origin="The last of the twenty currents, dated 1950–1975 and counted at about thirty buildings. Lévis published a separate Inventaire du patrimoine moderne in 2016 covering 79 buildings put up between 1946 and 1975 (RPCQ inventory 1313), and a guide, L'architecture moderne, un héritage du 20e siècle à démystifier. The City's line drawing for the current is an office block, and the fiche's own volumetry row concedes the range, so both a low ranch house and a slab are cross-linked here.")


# ---------------------------------------------------------------------------
def yaml_str(s):
    """Quote a scalar for YAML, always single-quoted and escaped."""
    return "'" + str(s).replace("'", "''") + "'"


def emit_list(key, values, indent=0):
    pad = " " * indent
    if not values:
        return f"{pad}{key}: []\n"
    out = f"{pad}{key}:\n"
    for v in values:
        out += f"{pad}- {yaml_str(v)}\n"
    return out


def main():
    data = json.loads(PARSED.read_text(encoding="utf-8"))
    fiches = {f["fiche_id"]: f for f in data["fiches"]}
    if set(fiches) != set(T):
        raise SystemExit(f"encode.py: fiche set mismatch: parsed={sorted(fiches)} table={sorted(T)}")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    for old in OUTDIR.glob("*.yaml"):
        old.unlink()

    written = 0
    for f in data["fiches"]:
        idf = f["fiche_id"]
        c = T[idf]
        order = f["index_order"]
        name_fr = f["name_fr"]
        period = f["index_period_label"]
        count = f["count_in_place"]
        approx = f["count_approx"]

        # --- French, straight from the parse; English, from the table above
        pfr, prof = {}, {"siting_landscape": [], "massing": [], "articulation": [],
                         "openings": [], "materials": []}
        col = {"Volumétrie": "massing", "Plan": "massing", "Toiture": "massing",
               "Saillies": "massing", "Ornementation": "articulation",
               "Ouvertures": "openings", "Revêtements": "materials"}
        for label in ["Volumétrie", "Plan", "Toiture", "Revêtements", "Ouvertures",
                      "Saillies", "Ornementation"]:
            fr = f["fields"].get(label)
            if not fr:
                continue                      # source silent: leave the column short
            pfr[FR_KEY[label]] = [fr]
            en = c["en"].get(label)
            if not en:
                raise SystemExit(f"encode.py: fiche {idf}: no English for {label!r}")
            prof[col[label]].append(en)

        # siting: the catalogue's own "Nombre à Lévis" distribution figure
        if count is not None:
            prof["siting_landscape"].append(
                f"The City counts {'about ' if approx else ''}{count:,} buildings of this "
                f"current across the merged territory of Lévis (fiche, « Nombre à Lévis »)."
                .replace(",", " "))
        else:
            prof["siting_landscape"].append(
                "The fiche gives no « Nombre à Lévis » figure for this entry — one of only "
                "two of the twenty that do not.")
        if c.get("siting_extra"):
            prof["siting_landscape"].append(c["siting_extra"])

        note = (
            "Encoded by sources/levis/parse.py from the City's fiche for this courant. The five "
            "columns follow the fiche's own seven fields: Volumétrie, Plan, Toiture and Saillies "
            "together make up massing, Ornementation is articulation, Ouvertures is openings and "
            "Revêtements is materials. The French under each English list is the fiche's wording "
            "verbatim, unedited. Siting has no counterpart in the fiche, so it carries the "
            "catalogue's own « Nombre à Lévis » distribution figure instead, and no French. "
            "Phase follows the opening year of the index's period range"
            + (f" ({period})" if period else "") + "."
        )
        if c.get("profile_note_extra"):
            note += " " + c["profile_note_extra"]

        L = []
        L.append(f"id: levis.{c['slug']}\n")
        L.append("place: levis\n")
        L.append(f"phase: {c['phase']}\n")
        L.append(f"phase_confidence: {c['phase_confidence']}\n")
        L.append(f"display_order: {order}\n")
        L.append(f"name_en: {yaml_str(c['name_en'])}\n")
        L.append(f"name_fr: {yaml_str(name_fr)}\n")
        L.append(f"source_ref: {yaml_str(f'Ville de Lévis, « Styles architecturaux », fiche {idf} « {name_fr} », {period}')}\n")
        L.append("source_generation: 'Ville de Lévis « Styles architecturaux » online catalogue (crawled 16 August 2026)'\n")
        L.append(f"fiche_id: {idf}\n")
        L.append(f"source_url: {yaml_str(f['source_url'])}\n")
        L.append(f"period_label: {yaml_str(period)}\n")
        L.append(f"count_in_place: {count if count is not None else 'null'}\n")
        L.append("is_courant: false\n")
        L.append(f"is_residential: {'true' if c.get('is_residential', True) else 'false'}\n")
        L.append("courant: null\n")
        L.append(emit_list("sectors", c.get("sectors")) if c.get("sectors") else "sectors: null\n")
        L.append(emit_list("canonical", c["canonical"]))
        L.append(emit_list("styles", c["styles"]))
        L.append("style_label: null\n")
        L.append(f"tenure_plan: {c['tenure_plan']}\n")
        L.append(f"storeys: {yaml_str(c['storeys'])}\n")
        L.append("roof:\n")
        L.append(f"  form: {c['roof_form'] if c['roof_form'] else 'null'}\n")
        L.append(f"  pitch_deg: {c['roof_pitch'] if c['roof_pitch'] is not None else 'null'}\n")
        L.append(f"window_proportion: {c['window_proportion'] or 'null'}\n")
        L.append(emit_list("principal_cladding", c["cladding"]))
        L.append(f"roofing: {yaml_str(c['roofing']) if c['roofing'] else 'null'}\n")
        L.append(f"garage: {c['garage'] or 'null'}\n")
        L.append("lot_width_m: null\n")
        L.append("setback_front_m: null\n")
        L.append("setback_side_m: null\n")
        L.append("front_yard_green_pct: null\n")
        L.append("profile:\n")
        for k in ["siting_landscape", "massing", "articulation", "openings", "materials"]:
            L.append(emit_list(k, prof[k], indent=2))
        L.append("profile_fr:\n")
        for k in ["volumetrie", "plan", "toiture", "saillies", "ornementation",
                  "ouvertures", "revetements"]:
            if k in pfr:
                L.append(emit_list(k, pfr[k], indent=2))
        L.append(f"profile_note: {yaml_str(note)}\n")
        L.append("conservation: null\n")
        L.append("conservation_fr: null\n")
        L.append(f"blurb_en: {yaml_str(c['blurb'])}\n")
        L.append(f"origin_en: {yaml_str(c['origin'])}\n")
        if c.get("related"):
            L.append("related_buildings:\n")
            for rb in c["related"]:
                L.append(f"- name: {yaml_str(rb['name'])}\n")
                L.append(f"  url: {yaml_str(rb['url'])}\n")
        else:
            L.append("related_buildings: null\n")

        # one rendered placeholder; the enumerated set follows, unrendered
        mise = [p for p in f["photos"] if p["kind"] in ("historic", "before", "potential", "after")
                and p.get("label_fr")]
        credit = (f"Ville de Lévis, « Styles architecturaux », fiche {idf} « {name_fr} » — "
                  f"historic, before, potential and after photographs at {f['source_url']} . {TERMS}")
        L.append("photos:\n")
        L.append("- file: null\n")
        L.append(f"  credit: {yaml_str(credit)}\n")
        L.append("  kind: placeholder\n")
        L.append("  licence: 'permission required'\n")
        L.append(f"  source_url: {yaml_str(f['source_url'])}\n")
        if mise:
            L.append("fiche_photos:\n")
            for p in mise:
                L.append(f"- kind: {p['kind']}\n")
                L.append("  file: null\n")
                L.append(f"  label_fr: {yaml_str(p['label_fr'])}\n")
                L.append(f"  source_url: {yaml_str(p['source_url'])}\n")
                L.append("  licence: 'permission required'\n")

        (OUTDIR / f"{c['slug']}.yaml").write_text("".join(L), encoding="utf-8")
        written += 1

    res = sum(1 for c in T.values() if c.get("is_residential", True))
    print(f"encode.py: OK — {written} type files -> {OUTDIR.relative_to(ROOT)} "
          f"({res} residential, {written - res} non-residential)")


if __name__ == "__main__":
    main()
