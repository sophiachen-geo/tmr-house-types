#!/usr/bin/env python3
"""Emit data/places/quebec/types/*.yaml from parsed.json plus the curated English.

Every French string in the output is lifted verbatim from parsed.json — which is itself lifted
from the crawled HTML in html/ — so no French is ever hand-typed here. What this file holds is
the part that is editorial and cannot be scraped: the English name, the five-column translation,
the blurb and origin paragraphs, and the cross-reference keys (phase, canonical form, styles,
sectors, quartiers) that tie a thesaurus node into the rest of the site.

Scope (PART 7 §0, §2.4). The thesaurus covers every building category. Three dispositions:
  * residential type          -> a card, with the full five-column table
  * is_courant: true          -> a parent node (courant): recorded and exported, no card
  * is_residential: false     -> a style the thesaurus applies to non-residential buildings:
                                 recorded and exported, no card

Which nodes are residential was decided as follows, and the decision for every one of the 53
crawled tids is recorded in MANIFEST.md:
  1. the 21 rows of §2.4's table are residential on the brief's authority;
  2. the five parents §2.4 names (202, 302, 401, 403, 506) are courants on the brief's
     authority, and 105 Colonial français joins them — the crawl found it outside the landing
     pages and it is the parent of 101/102, exactly the shape of 302 and 506;
  3. the ten candidates §2.4 says to "encode if the crawl confirms them as residential" were
     each tested against the fiche's own content and its linked exemplars. A node is residential
     when the Éléments caractéristiques describe the dwelling itself — a "niveaux d'occupation"
     bullet, the thesaurus's own marker for a habitable storey count — and at least half its
     exemplar buildings are dwellings. That admits 409, 407, 604 and 701 and rejects 406, 408,
     411, 602, 603 and 702, whose fiches describe an envelope applied to churches, banks and
     commercial blocks and carry no storey-count-for-habitation bullet;
  4. the same test decided the nodes §2.4 does not mention at all, admitting 201, 508 and 606.

Usage:  python3 encode.py        # writes the YAML files
        python3 encode.py --dry  # report only
"""
import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "data" / "places" / "quebec" / "types"
PARSED = HERE / "parsed.json"
CONSULTED = "2026-08-16"

SOURCE_GENERATION = ("Ville de Québec, Thésaurus du patrimoine bâti (fiches de styles "
                     f"architecturaux), consulté {CONSULTED}")
CREDIT = "Illustration : Charles-Étienne Brochu, 2022 — © Ville de Québec"
LANDING = "https://www.ville.quebec.qc.ca/citoyens/patrimoine/bati"

# The note every carded record carries: what was verbatim, what was translated, what is absent.
NOTE = (
    "Encoded from the City's thesaurus fiche for this node (tid={tid}), crawled {date}. "
    "The French beneath the table is the fiche's own text: « Description (source) » is its "
    "history-and-description paragraphs and « Éléments caractéristiques (source) » its bullet "
    "list, both verbatim. Three normalisations are applied to that French and are the only "
    "changes made to it: hyphenation broken by a line wrap is rejoined, the newlines the CMS "
    "emits mid-sentence are collapsed, and HTML entities are resolved; the source's own "
    "typography, including its U+2019 apostrophes, is left alone. The five English columns "
    "translate the bullet list, which the thesaurus orders composition → volumétrie → matériaux "
    "→ toit → ouvertures → saillies → ornements; the siting row is drawn from the fiche's "
    "prose, since the bullet list does not cover siting. Where the fiche is silent the field is "
    "null rather than inferred from the drawing. The thesaurus carries no conservation "
    "guidance of any kind, so `conservation` is empty here by fact and not by omission."
)
COURANT_NOTE = (
    "A parent node of the thesaurus (a *courant*), not a building type: recorded so the "
    "source's tree can be read whole, but given no card and no page of its own. Its French is "
    "verbatim from the fiche; no English five-column profile is written, because the node "
    "describes a family rather than a house. `tenure_plan` is set to `mixed` because the "
    "schema requires a value and the family spans several."
)
NONRES_NOTE = (
    "A style the thesaurus applies to non-residential buildings — the fiche carries no "
    "storey-count-for-habitation bullet and its linked exemplars are {ex}. Recorded so the "
    "source's list can be read whole, but out of this site's residential scope, so it gets no "
    "card and no page. Its French is verbatim from the fiche."
)

# --------------------------------------------------------------------------- residential types
# Keys per record: slug, name_en, phase, phase_confidence, canonical, styles, tenure_plan,
# storeys, roof, window_proportion, principal_cladding, roofing, sectors, quartiers,
# profile (the five English columns), blurb_en, origin_en.
T = {}

T[101] = dict(
    slug="maison-rurale-inspiration-francaise",
    name_en="One-storey rural house of French inspiration",
    phase="p1", phase_confidence="provisional",
    canonical=["french-rural-house-1st-hip"], styles=["colonial-francais", "french-regime"],
    tenure_plan="single-family", storeys="1", roof={"form": "hipped", "pitch_deg": 45},
    window_proportion="vertical",
    principal_cladding=["wood-piece-sur-piece", "wood-board-vertical", "stone", "roughcast"],
    roofing="cedar-shingle", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "The rural house of the French regime, built by the first settlers in a French frame of mind with such adaptations as the climate and the successive by-laws required.",
            "At Québec the plan leans Norman — more rectangular than square — and the base square or rectangle was often enlarged later in the same form to give an elongated model.",
        ],
        massing=[
            "Square plan, but generally rectangular; enlargement of the initial plan giving an elongated volume.",
            "One occupied level (one storey); no cellar.",
            "Hipped roof without eaves — the roof edge barely oversails the wall face.",
            "Projection: chimney at the centre, off-centre, or set within the gable wall.",
            "Steep roof pitch, above 45 degrees; the attic served to store grain and goods, hence the absence of dormers.",
        ],
        articulation=[
            "Decorative components are rare, limited to surrounds, lintels and chambranles.",
            "A plain composition on the classical ideal — a system of proportions and a search for harmony, but without symmetry.",
        ],
        openings=[
            "Few openings; no dormer.",
            "Openings distributed without any search for symmetry, and kept few to limit heat loss in winter and the weakening of the masonry walls.",
            "The usual window is the casement with small panes, fitted with working shutters.",
        ],
        materials=[
            "Walls of pièce-sur-pièce timber; vertical wood board cladding.",
            "Foundation barely raised above the ground.",
            "A squat square of stone rubble or pièce-sur-pièce timber, which may be covered in roughcast or vertical boards, with a slight batter in the walls.",
            "Roof slopes covered in cedar shingle.",
        ]),
    blurb_en=(
        "The oldest house in the thesaurus and the plainest: one storey, no cellar, a squat rectangle of "
        "rubble stone or stacked timber under a hipped roof pulled tight to the wall with no eaves at all. "
        "The attic held grain rather than people, which is why there are no dormers, and the windows are few "
        "because every one of them lost heat and weakened the wall."),
    origin_en=(
        "The colonial français idiom as the first settlers built it in Nouvelle-France: French models kept for "
        "their general proportions and their reserve, then adapted to the climate, the available materials and "
        "the intendants' by-laws. At Québec the plan tends to the Norman, more rectangular than square, and the "
        "original square could be extended along its length as the household grew."),
)

T[102] = dict(
    slug="maison-urbaine-inspiration-francaise",
    name_en="Urban stone house of French inspiration",
    phase="p1", phase_confidence="provisional",
    canonical=["french-urban-house-stone"], styles=["colonial-francais", "french-regime"],
    tenure_plan="row", storeys="1–2 plus attic", roof={"form": "gabled", "pitch_deg": None},
    window_proportion="vertical", principal_cladding=["stone", "roughcast"],
    roofing="sheet-metal-traditional", sectors=["SP-VQ"], quartiers=None,
    profile=dict(
        siting_landscape=[
            "The house of the walled town, rebuilt in stone after fire: few 17th-century examples survive, because most were of wood and burned.",
            "In the early 18th century the edicts and ordinances of the colony's intendants standardised how the house was to be built, and that series of regulations shaped the urban landscape of the town by reconsidering how it was to be lived in.",
        ],
        massing=[
            "One to three occupied levels (one to two and a half storeys); a vaulted cellar in the well-to-do house.",
            "Straight two-slope roof.",
            "Projections: party fire-break walls rising above the roof and containing the chimneys — built so to check the spread of flames.",
            "The more substantial houses are built over stone vaults.",
        ],
        articulation=[
            "Reduced ornament: bandeaux, quoins, corbels and tie-rods.",
            "Decorative components are rare, limited to surrounds, lintels and chambranles.",
        ],
        openings=[
            "Regular openings; cellar lights; hipped, gabled and cat-slide dormers.",
            "Openings distributed fairly regularly, but without any search for symmetry.",
            "The usual window is the casement with small panes, fitted with working shutters.",
        ],
        materials=[
            "Roof: slate, board-and-batten or lapped board, but generally traditional sheet metal.",
            "Foundation raised above the ground.",
            "A stone construction of one or two levels with an attic.",
        ]),
    blurb_en=(
        "Stone, one or two levels and an attic, with the party walls carried up past the roof as fire-breaks and "
        "the chimneys buried inside them — the shape the intendants' ordinances imposed on the walled town after "
        "wooden Québec kept burning down. The well-to-do version sits on a stone vault."),
    origin_en=(
        "Few urban houses of French inspiration built at Québec in the 17th century survive, and the wood most of "
        "them were made of is not unconnected with the fires that destroyed them. In the early 18th century the "
        "edicts and ordinances of the colony's intendants normalised how the house was to be built in order to "
        "remedy this, and that series of by-laws shaped the urban landscape of the town by reconsidering how it "
        "was to be lived in."),
)

T[201] = dict(
    slug="palladien",
    name_en="Palladian house (residential Palladian)",
    phase="p2", phase_confidence="verified",   # "de la fin du 18e siècle jusque vers 1830"
    canonical=["symmetric-brick-3-5-bay-2st"], styles=["palladien"],
    tenure_plan="single-family", storeys="2–2.5", roof={"form": "gabled-or-hipped", "pitch_deg": 38},
    window_proportion="vertical", principal_cladding=["cut-stone", "roughcast", "stucco"],
    roofing="sheet-metal-traditional", sectors=["SP-VQ", "SP-SIL"], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Introduced in England, then appearing in Lower Canada from the end of the 18th century until about 1830.",
            "A period marked by the new rulers' wish to signal their presence at Québec: buildings more representative of the British order were transformed or rebuilt, and well-to-do houses put up to match.",
        ],
        massing=[
            "Composition drawn from English classicism, itself drawn from Italian Renaissance architecture and reinterpreting the forms of Antiquity: a search for symmetry and a tripartite façade.",
            "Two to three occupied levels (two to two and a half storeys).",
            "Straight two- or four-slope roof; medium pitch, between 30° and 45°; traditional sheet-metal covering.",
            "Central projections: avant-corps and portal; central secondary body: porch.",
            "Projections: chimneys rising from the roof or set within the gable walls — distributed symmetrically, often one at each end.",
            "Handled with restraint, the residential architecture takes up only the broad principles of the Palladian style.",
        ],
        articulation=[
            "Classical ornament: columns, cornices, pediments and pilasters.",
            "A plain composition in the Palladian style.",
            "Projecting portals decorated with columns or pilasters carrying a cornice and a triangular pediment, and chambranles.",
        ],
        openings=[
            "Rectangular and round-arched openings; central door fitted with a portal.",
            "Casements with small or large panes, sash windows with small panes, Palladian (Serlian) windows and oculi.",
            "Cellar lights.",
            "The Serlian or Palladian window — three lights, the centre one crowned with a semicircular head — is another marked trait of the style.",
        ],
        materials=[
            "Walls of stone masonry, generally ashlar; roughcast or white stucco render.",
            "Stone foundation raised above the ground.",
            "The walls are of smooth-finished ashlar or covered in roughcast.",
        ]),
    blurb_en=(
        "English classicism arriving with the new rulers, and pulled back hard for domestic use: two to three levels, "
        "a rigorously symmetrical front with a central door, a projecting pedimented centre making the façade "
        "tripartite, and chimneys placed symmetrically at the ends. The Serlian window is the giveaway."),
    origin_en=(
        "The Palladian style belongs to English classicism, a movement current in England from the 17th century, drawing "
        "on Italian Renaissance architecture and on the writings and buildings of Andrea Palladio (1508–1580). "
        "Introduced first into England, it appeared in Lower Canada from the end of the 18th century until about 1830, "
        "in a period marked by the new rulers' wish to signal their presence at Québec — buildings more representative "
        "of the British order were transformed or rebuilt, and well-to-do houses erected. Residential architecture took "
        "up only the broad principles."),
)

T[203] = dict(
    slug="maison-londonienne",
    name_en="London-type terrace house",
    phase="p2", phase_confidence="verified",   # "principalement de 1815 à 1870"
    canonical=["london-terrace-house"], styles=["palladien", "neoclassical-quebec"],
    tenure_plan="row", storeys="2.5–3.5", roof={"form": "gabled", "pitch_deg": 38},
    window_proportion="vertical", principal_cladding=["cut-stone", "clay-brick", "roughcast"],
    roofing="sheet-metal-traditional", sectors=["SP-VQ"], quartiers=None,
    profile=dict(
        siting_landscape=[
            "It marks the urban fabric of 19th-century Québec, mainly from 1815 to 1870.",
            "It gives directly onto the street with no front setback, and may be pierced by a carriage passage giving access to a rear yard.",
            "The houses are often grouped in pairs or form part of a longer series called a row, which lets symmetries be played by alternating the plans from one house to the next.",
        ],
        massing=[
            "Composition: party-wall or row house with a front of two, three (the basic unit) or four bays and a door at one end; the well-to-do house has a five-bay front with a centred door monumentally treated.",
            "Rectangular plan, generally narrow and deep.",
            "Three to four occupied levels (two and a half to three and a half storeys); a hall serving the formal rooms on the ground floor and rooms progressively more modest and private from one storey to the next.",
            "Straight two-slope roof; medium pitch, between 30° and 45°.",
            "Projections: party fire-break walls rising above the roof and containing the chimneys.",
            "The roof edge oversails the wall little, and a few dormers light the attic.",
        ],
        articulation=[
            "The ornament is resolutely classical, with pediments, pilasters and cornices.",
            "Walls of ashlar or rubble stone, of brick, or covered in roughcast, showing a search for purity in the surfaces that suits this sober and rigorous architecture.",
        ],
        openings=[
            "Carriage door surmounted by a transom; top-floor windows treated as an attic storey; cellar lights; dormers present.",
            "Openings on the front are regularly disposed.",
            "Casements at first, the windows evolve continuously: small panes early in the 19th century, then large panes, then with transoms or sashes.",
            "The top-floor windows are treated as an attic — lower than those of the levels below — a particularity of the London-type house.",
        ],
        materials=[
            "Walls of rubble stone; brick cladding.",
            "Foundation raised above the ground.",
        ]),
    blurb_en=(
        "Narrow, deep and built in pairs or rows straight onto the pavement, with the door at one end of a three-bay "
        "front and a carriage passage to the yard behind. The rooms get smaller and more private as you climb, and the "
        "top-floor windows are squashed into an attic band — the detail that identifies the type."),
    origin_en=(
        "The London-type house belongs to the neoclassical style and recalls the residential models built in London in "
        "the 18th century. At Québec it marks the urban fabric of the 19th century, mainly from 1815 to 1870: an "
        "imposing volume of two or three levels with an attic, party fire-break walls carrying wide chimneys, and walls "
        "of ashlar or rubble stone, brick or roughcast showing a search for purity of surface suited to this sober and "
        "rigorous architecture."),
)

T[205] = dict(
    slug="cottage-regency",
    name_en="Regency cottage",
    phase="p3", phase_confidence="verified",   # "principalement entre 1820 et 1880"
    canonical=["regency-cottage-hipped-veranda", "detached-cottage-steep-gable"], styles=["regency"],
    tenure_plan="single-family", storeys="1–1.5", roof={"form": "hipped", "pitch_deg": 25},
    window_proportion="vertical", principal_cladding=["clay-brick", "stone", "wood"],
    roofing="sheet-metal-traditional", sectors=["SP-SIL", "SP-BEA"],
    quartiers=["Sillery", "Beauport", "Sainte-Foy", "Grande Allée", "chemin Saint-Louis"],
    profile=dict(
        siting_landscape=[
            "Layout: garden, quality of the landscaping, a wide expanse of ground and abundant vegetation.",
            "At Québec, villégiature spread to the suburbs — Sillery, Beauport and Sainte-Foy — over the 19th century; Regency buildings appear mainly between 1820 and 1880 along the old routes such as the Grande Allée and the chemins Saint-Louis and Sainte-Foy.",
            "Built on large properties still unoccupied or later subdivided, the building stands in communion with the setting it is placed in.",
        ],
        massing=[
            "Composition with a search for symmetry while integrating the forms into the natural environment.",
            "One to two occupied levels (one to one and a half storeys).",
            "Square plan.",
            "Four-slope roof; low pitch, under 30°; with curved eaves, though generally straight; traditional sheet-metal covering.",
            "Projections: wrap-around gallery sheltered by the eaves, and chimneys rising from the roof.",
            "A low, wide-spreading four-slope roof whose eaves are sometimes curved is what marks the type out above all.",
        ],
        articulation=[
            "Classical ornament: columns, cornices, pediments and pilasters.",
            "The ornaments are a more or less simplified recollection of those of Greek and Roman temples.",
        ],
        openings=[
            "Regular rectangular openings fitted with chambranles, surrounds and flat arches; central door with sidelight(s) and transom, and French windows.",
            "Casements with small or large panes; hipped or gabled dormers.",
            "Shed dormers.",
            "The most usual window is the casement with large panes, which sometimes becomes a French window.",
        ],
        materials=[
            "Walls: stone, brick or wood cladding.",
            "Stone foundation barely raised above the ground.",
        ]),
    blurb_en=(
        "A square one-storey cottage under a low four-slope roof whose eaves run out far enough to roof a veranda "
        "all the way round — the picturesque half of the Regency, built out along the Grande Allée and the chemins "
        "Saint-Louis and Sainte-Foy on grounds big enough to lay out a garden."),
    origin_en=(
        "The Regency draws on two aesthetics at once: the neoclassical, based on a rigorous reading of classical "
        "models, and the picturesque, which seeks to fit irregular forms into the natural setting. Those principles "
        "went mostly into residential architecture on the edge of the urban centres. Large houses called villas were "
        "followed by more modest ones taking the look of cottages; introduced by the British, both were adopted by the "
        "English elite who wanted a house in the country. At Québec villégiature reached the suburbs of Sillery, "
        "Beauport and Sainte-Foy over the 19th century, and Regency buildings appear mainly between 1820 and 1880."),
)

T[206] = dict(
    slug="villa-regency",
    name_en="Regency villa",
    phase="p3", phase_confidence="verified",   # "principalement entre 1820 et 1880"
    canonical=["picturesque-villa-estate"], styles=["regency"],
    tenure_plan="single-family", storeys="2–2.5", roof={"form": "hipped", "pitch_deg": 25},
    window_proportion="vertical", principal_cladding=["clay-brick", "stone", "wood"],
    roofing="sheet-metal-traditional", sectors=["SP-SIL", "SP-BEA"],
    quartiers=["Sillery", "Beauport", "Sainte-Foy", "Grande Allée", "chemin Saint-Louis"],
    profile=dict(
        siting_landscape=[
            "Layout: garden, quality of the landscaping, a wide expanse of ground and abundant vegetation.",
            "The building is set back from the road, on a cleared part of the ground, and the site is set off by landscaping, pavilions or fountains.",
            "At Québec, villégiature spread to the suburbs — Sillery, Beauport and Sainte-Foy — over the 19th century; Regency buildings appear mainly between 1820 and 1880 along the old routes such as the Grande Allée and the chemins Saint-Louis and Sainte-Foy.",
        ],
        massing=[
            "Composition drawn from the neoclassical aesthetic, with a search for symmetry and a rigorous reading of classical models, and from the picturesque, integrating the forms into the natural environment.",
            "Composition: a well-to-do house with a front of three or five bays.",
            "Square or rectangular plan; rectangular for the villa proper.",
            "Two to three occupied levels (two to two and a half storeys).",
            "Four-slope roof; low pitch, under 30°; traditional sheet-metal covering. Straight two-slope roof; medium pitch, between 30° and 45°.",
            "Projections: gallery; central projections: avant-corps; secondary body: veranda.",
            "A large gallery or a veranda across the front makes the link with the outdoors, while various annexes spread across the ground.",
        ],
        articulation=[
            "Classical ornament: columns, cornices, pediments and pilasters.",
            "Ornaments: quoins, finials, cut-out woodwork and rooftop terraces.",
            "The ornament is meant to be sober, using quoins, finials and chambranles.",
        ],
        openings=[
            "Regular rectangular openings fitted with chambranles, surrounds and flat arches; central door with sidelight(s) and transom, and French windows.",
            "Casements with small or large panes; hipped or gabled dormers.",
        ],
        materials=[
            "Walls: stone, brick or wood cladding.",
            "Stone foundation barely raised above the ground.",
        ]),
    blurb_en=(
        "The town house moved out to the country: a square or rectangular block of two to three levels, three or five "
        "bays wide, under a low four-slope roof, set back from the road on cleared ground with a gallery or veranda "
        "across the front and the site dressed with planting, pavilions and fountains."),
    origin_en=(
        "The Regency villa can be defined as a house transposed from the urban setting to the rural one. Its "
        "composition, from the classical repertoire, is turned toward rigour and symmetry, while the building still "
        "tries to establish a relation with its natural surroundings. The organisation of the property takes much the "
        "same shape from one villa to the next: the building stands back from the road on a cleared part of the ground, "
        "and the site is set off by landscaping, pavilions or fountains."),
)

T[301] = dict(
    slug="maison-neoclassique-quebecoise",
    name_en="Québécois neoclassical house",
    phase="p3", phase_confidence="verified",   # "Tout au long du 19e siècle"
    canonical=["quebec-traditional-1-5st-gable"], styles=["neoclassical-quebec"],
    tenure_plan="single-family", storeys="1.5", roof={"form": "gabled", "pitch_deg": 45},
    window_proportion="vertical", principal_cladding=["wood-clapboard", "wood-shingle", "clay-brick"],
    roofing="sheet-metal-traditional", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "All through the 19th century it was built at Québec in rural and semi-urban settings, and in the faubourgs.",
            "The house is raised well above ground level and frequently has, on its long axis, a summer kitchen reproducing the main body's characteristics at a smaller scale.",
        ],
        massing=[
            "Composition: a search for symmetry; the type is seen as the vernacular house of Québécois residential architecture, and takes in several variants including the artisan's house with a shop at basement level.",
            "Rectangular plan; variable volume.",
            "Two occupied levels (one and a half storeys).",
            "Two-slope roof with straight, but generally curved, eaves; medium pitch, about 45°; traditional sheet-metal covering.",
            "Projections sheltered by the curved eaves or by an awning: perron and gallery; secondary bodies: lean-to, larder and dairy, but generally a summer kitchen.",
            "The roof carries past the front and rear walls on curved bell-cast eaves that shelter a gallery laid out at the front; where the slopes are straight, a lean-to or awning often roofs the gallery instead.",
        ],
        articulation=[
            "Ornaments: brackets, lambrequins and corner boards.",
            "The ornament stays sober, with corner boards and chambranles; cut-out woodwork can give the house a picturesque touch.",
        ],
        openings=[
            "Openings fitted with chambranles; central door; gabled or pedimented dormers.",
            "The attic is inhabited, as the presence of dormers shows.",
        ],
        materials=[
            "Walls: brick cladding, but generally wood board or wood shingle.",
            "Foundation raised above the ground.",
            "Traditional sheet metal laid in battens, à la canadienne or pinched.",
        ]),
    blurb_en=(
        "The vernacular house of Québec, and the one the faubourg house is a stripped-down copy of: a storey and a "
        "half under a 45-degree roof whose bell-cast eaves sweep out to cover the front gallery, dormers in the "
        "attic, a summer kitchen trailing off the end, and corner boards for ornament."),
    origin_en=(
        "Descended from the French regime, this house evolved under the English regime in contact with the neoclassical "
        "style. It is a freer construction answering specifically to functional, economic and climatic constraints "
        "according to where it was built and the social standing of its occupants, and so takes several variants: from "
        "the small stripped-down body of lodging it can become a more developed and ornamented village dwelling. All "
        "through the 19th century it was built at Québec in rural and semi-urban settings, and in the faubourgs."),
)

T[303] = dict(
    slug="maison-de-faubourg",
    name_en="Rudimentary faubourg house",
    phase="p4", phase_confidence="verified",   # "jusqu'à la fin 19e siècle"
    canonical=["faubourg-house-1-1-5st"], styles=["neoclassical-quebec", "faubourg-vernacular"],
    tenure_plan="row", storeys="1–1.5", roof={"form": "gabled", "pitch_deg": 50},
    window_proportion="vertical",
    principal_cladding=["wood-board-vertical", "wood-clapboard", "clay-brick", "roughcast", "stucco"],
    roofing="sheet-metal-traditional", sectors=["SP-VQ"],
    quartiers=["Saint-Roch", "Saint-Sauveur", "Saint-Jean-Baptiste"],
    profile=dict(
        siting_landscape=[
            "Built outside the limits of the walled town, it spread widely at Québec through the faubourgs of Saint-Roch, Saint-Sauveur and Saint-Jean-Baptiste, which grew under demographic pressure from the middle of the 18th century.",
            "Often party-wall, or set off from its neighbours by a narrow alley.",
        ],
        massing=[
            "Composition: a simple, rudimentary house, with or without symmetry, party-wall or set off from its neighbours by a narrow alley; a type descended from the urban house of French inspiration and from the Québécois neoclassical house.",
            "One to two occupied levels (one to one and a half storeys); following densification or a fire, the house may be rebuilt, enlarged, raised by one or two storeys, given dormers, or capped with a mansard roof.",
            "Two-slope roof with shallow straight or curved eaves; steep pitch, over 45°; following the by-laws against fire, an eaveless roof.",
            "The basic model has a ground floor under a two-slope roof, straight or curved, with a shallow eave.",
        ],
        articulation=[
            "Ornaments: corner boards.",
            "The ornament stays limited to corner boards and chambranles.",
        ],
        openings=[
            "Few openings, fitted with chambranles: three at the front including the door at the end of the façade, and two at the rear; no dormer.",
            "The gable walls usually stay blind.",
        ],
        materials=[
            "Walls of pièce-sur-pièce timber; vertical or horizontal wood board cladding; following the by-laws against fire, walls clad in brick, roughcast or stucco.",
            "Foundation barely visible or raised above the ground.",
            "Roof covering of cedar shingle, board-and-batten or lapped board; following the by-laws against fire, traditional sheet metal.",
        ]),
    blurb_en=(
        "The plainest house in the city and the one the fires rewrote: a storey or a storey and a half of "
        "pièce-sur-pièce timber under a steep two-slope roof, three openings at the front with the door pushed to "
        "one end, two at the back, blind gables, and corner boards for the whole of its ornament. After the fires the "
        "by-laws took away the boards and the shingles and gave it brick or roughcast and eaveless tin instead."),
    origin_en=(
        "Set outside the limits of the walled town, this type descends from the urban house of French inspiration and "
        "can be read as a simplified version of the Québécois neoclassical house. It spread widely at Québec through "
        "faubourgs such as Saint-Roch, Saint-Sauveur and Saint-Jean-Baptiste, which grew under demographic pressure "
        "from the middle of the 18th century. It is a single-family dwelling, simple and rudimentary, built until the "
        "end of the 19th century by artisans, by workers, or by the owner himself. Following the great fires or the "
        "densification of the faubourgs, these houses were often rebuilt, enlarged, raised by one or two storeys, given "
        "dormers, or capped with a mansard roof that gave more space under the attic."),
)

T[304] = dict(
    slug="maison-transition-franco-quebecoise",
    name_en="Franco-Québécois transition house",
    phase="p2", phase_confidence="verified",   # "aux environs de 1770 à 1820"
    canonical=["transition-franco-quebecoise"], styles=["french-regime", "neoclassical-quebec"],
    tenure_plan="single-family", storeys="1.5", roof={"form": "gabled", "pitch_deg": 45},
    window_proportion="vertical",
    principal_cladding=["stone", "wood-piece-sur-piece", "wood-clapboard", "roughcast", "stucco"],
    roofing="cedar-shingle", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Built at Québec in rural and semi-urban settings, and in the faubourgs.",
            "The period from about 1770 to 1820 begins the adaptation of the French model to the Québécois context, under the influence of the neoclassical style.",
        ],
        massing=[
            "Composition: with or without symmetry; a type descended from the rural house of French inspiration.",
            "Rectangular plan; variable volume.",
            "Two occupied levels (one and a half storeys); no cellar.",
            "Two-slope roof with straight or curved eaves; medium pitch, about 45°.",
            "Projection: chimney at the centre, off-centre, or set within the gable wall.",
            "The type keeps a good footing on the ground, a steep roof and massive chimney stacks from the house of French inspiration; the roof pitch is often less pronounced than that house's, and the eave, straight or curved, oversails the wall face.",
        ],
        articulation=[
            "Classical ornaments such as pediments sometimes dress the dormers and the windows, which are surrounded by carved wood chambranles.",
        ],
        openings=[
            "Openings fitted with chambranles; gabled or pedimented dormers.",
            "The British influence is legible in the more regular disposition of the openings and the chimneys.",
            "The openings are more numerous than on the house of French inspiration and their panes are enlarged; dormers, the gabled model in ordinary use, become general.",
        ],
        materials=[
            "Walls of rubble stone or pièce-sur-pièce timber; wood board, roughcast or stucco cladding.",
            "Foundation barely raised above the ground.",
            "Cedar shingle roof covering.",
        ]),
    blurb_en=(
        "The house caught between two building traditions: French footing, steep roof and massive chimney stacks, "
        "with the British contribution visible only in how regularly the openings and the chimneys are now placed, "
        "how many more windows there are, and how much larger the panes have grown."),
    origin_en=(
        "The house changed little in the decades after the Conquest of 1759–1760, because the tradesmen and their French "
        "traditions remained. It met British influence only at the turn of the 19th century, with the English immigration "
        "that brought the newcomers' own ways of building. That period, from about 1770 to 1820, begins the adaptation of "
        "the French model to the Québécois context while under the influence of the neoclassical style, and produces the "
        "Franco-Québécois transition house, built at Québec in rural and semi-urban settings and in the faubourgs."),
)

T[402] = dict(
    slug="maison-mansardee",
    name_en="Mansard-roofed house",
    phase="p4", phase_confidence="verified",   # "entre 1860 et 1920"
    canonical=["mansard-house-2st"], styles=["second-empire"],
    tenure_plan="single-family", storeys="2–4", roof={"form": "mansard", "pitch_deg": 75},
    window_proportion="vertical",
    principal_cladding=["clay-brick", "wood-clapboard", "wood-shingle", "asbestos-cement-shingle"],
    roofing="sheet-metal-traditional", sectors=["SP-VQ"], quartiers=None,
    profile=dict(
        siting_landscape=[
            "It leaves its mark on the Québécois landscape between 1860 and 1920, in rural, semi-urban and urban settings alike.",
            "At Québec this type densifies the built fabric of the faubourgs in particular, since a two-slope roof was often replaced by a lit attic that became a full living space.",
            "In rural settings it is common to find a gallery laid out at the front and a summer kitchen at the side or rear of the main body.",
        ],
        massing=[
            "Composition: simple, modest decoration, with or without symmetry, and a silhouette giving off a certain elegance but without the monumental character; a type able to densify the urban fabric and seen as the vernacular house of the Second Empire style.",
            "Rectangular, square or L-shaped plan.",
            "Mansard (broken) roof with straight or curved terrasson and brisis: two-slope, two-slope with half-hips, or four-slope. False-mansard roof with straight or curved brisis; low pitch for the terrasson, under 30°, and very steep for the brisis, over 75°; traditional sheet-metal covering.",
            "Projections: gallery, wrapping or not, sheltered by the curved eave or by an awning, logettes, oriels, perron and fire-break walls; secondary bodies: summer kitchen and porch.",
            "Two to four occupied levels; the brisis is pierced by dormers.",
        ],
        articulation=[
            "Ornaments: brackets, corbels, cut-out woodwork, lambrequins and corner boards.",
            "The decorative repertoire, drawn from French classical eclecticism, stays simple and modest.",
            "The roof edge may be dressed with a cornice, corbels or consoles.",
        ],
        openings=[
            "Rectangular or arched openings picked out by chambranles.",
            "Sash or casement windows divided into four or six panes.",
            "The brisis is pierced by dormers, which light the attic storey.",
        ],
        materials=[
            "Walls: brick, wood board, wood shingle or asbestos shingle cladding.",
            "Roof covering of traditional sheet metal.",
        ]),
    blurb_en=(
        "The Second Empire without the monumentality: the same broken roof, the same dormers cut into a near-vertical "
        "brisis, but on a plain house, popularised through American plan catalogues. At Québec it is a densification "
        "device — swap a two-slope roof for a mansard and the attic becomes a whole extra floor."),
    origin_en=(
        "The mansard or broken-roofed house can be understood as the vernacular version of the Second Empire style. "
        "Though it has neither its monumentality nor its presence, its silhouette gives off a certain elegance. It was "
        "popularised in the United States through architectural catalogues, in which the variations of pitch and the "
        "flaring of the roofs became regional particularities. It leaves its mark on the Québécois landscape between "
        "1860 and 1920, in rural, semi-urban and urban settings, and at Québec it densifies the built fabric of the "
        "faubourgs in particular."),
)

T[404] = dict(
    slug="neo-queen-anne",
    name_en="Neo-Queen Anne house",
    phase="p5", phase_confidence="verified",   # "En vogue entre 1880 et 1915"
    canonical=["queen-anne-irregular-2-5st"], styles=["queen-anne", "victorian-eclectic"],
    tenure_plan="single-family", storeys="1.5–2.5", roof={"form": "gabled-multi", "pitch_deg": 45},
    window_proportion="vertical",
    principal_cladding=["clay-brick-red", "stone", "wood", "roughcast", "stucco"],
    roofing="slate", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "In vogue between 1880 and 1915 with the anglophone community of Québec, and used almost exclusively in residential architecture.",
            "The bourgeois houses, combining medieval picturesque with Georgian classicism, are associated with the rural and suburban parts of the city.",
        ],
        massing=[
            "Composition drawn from the revival of English vernacular architecture, itself drawn from old rustic cottages: a refined character, asymmetrical fronts, decoration at once simple and elaborate, and a contrasting treatment of materials and ornaments; a picturesque effect combining the medieval picturesque with Georgian classicism.",
            "Irregular plan; articulated volumes.",
            "Two to three occupied levels (one and a half to two and a half storeys).",
            "Straight two- or four-slope roof, truncated four-slope roof crowned with a rooftop terrace, multi-slope or asymmetrical; medium pitch, about 45°.",
            "Projections: avant-corps, balcony, chimneys, logettes, oriels and perron; projections capped with conical roofs: gallery, wrapping or not, towers and turrets; secondary body: side wing under a straight two-slope roof.",
        ],
        articulation=[
            "Ornaments: bandeaux, quoins, columns, consoles, cornices, finials, pediments, cut-out woodwork, gables, corner boards and cornice returns.",
            "The ornamental treatment of the materials, at once textured and coloured, contrasts with the principal cladding and picks out the different parts of the construction — the base, the asymmetrical fronts, the irregular steep roofs, the chimney stacks, the dormers and the articulated volumes.",
        ],
        openings=[
            "Rectangular openings fitted with chambranles, keystones, lintels and flat arches.",
            "Panelled door with or without glazing, surmounted by a transom.",
            "Casements with large panes, or sashes with or without glazing bars; dormers present.",
        ],
        materials=[
            "Walls: textured or plain stone, wood, roughcast or stucco cladding, but generally red brick.",
            "Stone foundation raised above the ground.",
            "Slate or traditional sheet-metal roof covering.",
        ]),
    blurb_en=(
        "The picturesque taken as far as it will go: an irregular plan, articulated volumes, asymmetrical fronts, "
        "turrets under conical roofs, oriels and a wrap-around gallery, all in red brick whose texture and colour are "
        "worked deliberately against the trim. Almost exclusively a house, and almost exclusively an anglophone one."),
    origin_en=(
        "The neo-Queen Anne style appeared in Britain about the middle of the 19th century, largely through the architect "
        "Richard Norman Shaw. Particularly prized by the middle class of the industrial period, it carried the revival of "
        "English vernacular architecture, drawing its vocabulary from old rustic cottages. Despite taking its name from "
        "Queen Anne Stuart it has little connection with the architecture built under her reign (1702–1714). In vogue "
        "between 1880 and 1915 with the anglophone community of Québec, it is used almost exclusively in residential "
        "architecture, where the search for the picturesque had become the established norm of the Victorian era."),
)

T[405] = dict(
    slug="maison-neogothique",
    name_en="Neo-Gothic house, villa or cottage",
    phase="p3", phase_confidence="verified",   # "jusque vers 1920 pour les bâtiments résidentiels"
    canonical=["detached-cottage-steep-gable"], styles=["neogothique"],
    tenure_plan="single-family", storeys="1.5–2.5", roof={"form": "gabled", "pitch_deg": 45},
    window_proportion="vertical", principal_cladding=["clay-brick", "wood-clapboard", "wood-shingle"],
    roofing="sheet-metal-traditional", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Present at Québec between 1830 and 1880 for the style at large, and observable until about 1920 for residential buildings.",
            "The residential examples are mostly villas or cottages set on the edge of the urban centre.",
        ],
        massing=[
            "Composition: a search for symmetry.",
            "Rectangular or L-shaped plan; irregular ground plan in the residential examples.",
            "Two to three occupied levels (one and a half to two and a half storeys).",
            "Straight two-slope roof; medium pitch, about 45°.",
            "Projection: gallery; central secondary body: porch.",
            "The aesthetic form is expressed through the medieval or picturesque silhouette of the building.",
        ],
        articulation=[
            "Ornaments: finials, cut-out woodwork and cornice returns.",
            "A new ornamental vocabulary: a central gable dormer on the front, pinnacles, cut-out wood motifs running along the cornice, and heavy roll or 'chapeau de gendarme' mouldings.",
            "Structural elements used to essentially decorative ends.",
        ],
        openings=[
            "Openings fitted with chambranles, roll mouldings and 'chapeau de gendarme' heads.",
            "Windows, with or without glazing bars forming diamonds, sashes with glazing bars or with iron bars.",
            "Central gable dormer.",
            "Pointed (ogee) arched openings.",
        ],
        materials=[
            "Walls: brick, wood board or wood shingle cladding.",
            "The walls and the chimney stacks are of brick, while the windows may carry diamond-shaped panes.",
        ]),
    blurb_en=(
        "The domestic half of a style that mostly built churches: a villa or cottage on the edge of town with a "
        "central gable dormer over the front door, pointed-arch windows, diamond panes and cut-out wood running "
        "along the cornice — structure turned into decoration, which is what neo-Gothic mostly was."),
    origin_en=(
        "Drawing on medieval architecture, the neo-Gothic style appeared in England about 1750, then spread through "
        "Europe before reaching North America; romantic spirits found in it an answer to the severity of neoclassical "
        "architecture. Present at Québec between 1830 and 1880, its popularity was short-lived: it quickly became the "
        "Protestant church's preferred choice, while Catholic communities moved away from it after the enthusiasm of the "
        "1850s and 1860s. Compared with religious architecture, the style is observable at Québec until about 1920 for "
        "residential buildings — mostly villas or cottages set on the edge of the urban centre."),
)

T[407] = dict(
    slug="neo-renaissance",
    name_en="Neo-Renaissance house and mixed-use block",
    phase="p5", phase_confidence="verified",   # "entre 1850 et 1920"
    canonical=["urban-house-stone-2-3st", "eclectic-prestige-house"], styles=["neo-renaissance"],
    tenure_plan="mixed", storeys="2.5–3.5", roof={"form": "hipped", "pitch_deg": 25},
    window_proportion="vertical", principal_cladding=["rusticated-stone", "clay-brick"],
    roofing="sheet-metal-traditional", sectors=["SP-VQ"], quartiers=None,
    profile=dict(
        siting_landscape=[
            "At Québec these buildings, though present in rural settings, are set above all in urban or semi-urban ones, between 1850 and 1920.",
            "They put the owner's material ease, or the importance of the construction — its standing in the setting — in the front rank.",
        ],
        massing=[
            "Composition drawn from Renaissance architecture: richness and refinement, the orders used in superposition and an overabundance of decoration; a picturesque effect in reaction to the rigour of the Palladian and neoclassical styles, or a more austere effect with a search for symmetry and an interior organisation tied to the form and the openings of the building.",
            "Simple or irregular plan.",
            "Three to four occupied levels (two and a half to three and a half storeys).",
            "Straight four-slope or truncated four-slope roof crowned with a lantern or a rooftop terrace; low pitch, under 30°; traditional sheet-metal covering. Flat roof (basin or internal drainage); membrane covering.",
            "Projection: perron, portal and square tower.",
        ],
        articulation=[
            "Classical ornaments: crowning balustrade, bas-reliefs, quoins, columns, consoles, cornices, entablatures, pediments, pilasters and cornice returns.",
            "The roof edge carries a crowning balustrade or a massive cornice on consoles or modillions.",
            "With the orders used in superposition, the separation of the storeys is legible in the treatment of the fronts.",
        ],
        openings=[
            "Rectangular or arched openings fitted with sills, arches, keystones, surrounds and lintels.",
            "Panelled door with or without glazing, surmounted by a transom and fitted with a portal.",
            "Casements with large panes, or sashes with small panes or glazing bars.",
            "A mixed-use building draws attention to its commercial ground floor with wide shopfronts, against the sober or distinctive look of the storeys above.",
        ],
        materials=[
            "Walls: cladding of variously rusticated stone, or of brick.",
            "Stone foundation raised above the ground.",
        ]),
    blurb_en=(
        "Italian palaces done over for the Victorian street: three or four levels of rusticated stone or brick, the "
        "orders stacked storey on storey, a massive bracketed cornice or a balustrade at the top, and — where the "
        "ground floor is a shop — wide plate-glass fronts under all that decoration."),
    origin_en=(
        "Renaissance architecture, which appeared in Italy in the 15th century, urged a return to antique forms and the "
        "restoration of harmony and balance of proportion through the orders. The neo-Renaissance style draws on the "
        "work of that period, more precisely the Italian palaces and villas of the 16th and 17th centuries, adapted to "
        "the Victorian and industrial era to create a picturesque effect in reaction to the rigour of the Palladian and "
        "neoclassical styles. These buildings generally have a commercial, industrial or residential function; at Québec "
        "they are set above all in urban or semi-urban settings between 1850 and 1920."),
)

T[409] = dict(
    slug="neo-tudor",
    name_en="Neo-Tudor house",
    phase="p5", phase_confidence="verified",   # "entre 1890 et 1920"
    canonical=["tudor-manor-stone-timber", "modest-tudor-cottage-brick-2st"], styles=["tudor-revival"],
    tenure_plan="single-family", storeys="1.5–2.5", roof={"form": "gabled-multi", "pitch_deg": 50},
    window_proportion="vertical",
    principal_cladding=["clay-brick-red", "stone", "wood", "roughcast", "half-timbering"],
    roofing="slate", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Present across the city's territory between 1890 and 1920, and principally associated with residential architecture.",
            "A picturesque effect, integrating the forms into the natural and built environment.",
        ],
        massing=[
            "Composition drawn from traditional English and Scottish architecture, itself drawn from the manors and farms of the 16th century: with or without symmetry.",
            "Simple or irregular plan, but flexible; the upper storeys project over the ground floor.",
            "Two to three occupied levels (one and a half to two and a half storeys); a functional arrangement of the rooms, and one private and comfortable for the house.",
            "Straight two- or four-slope roof, or truncated four-slope; medium pitch, between 30° and 45°, or steep, over 45°.",
            "Projections: chimneys, logettes, oriels, perron and square towers.",
            "The steep roof carries dormers and tall chimneys ornamented at their heads.",
        ],
        articulation=[
            "Ornaments: cornices, finials, false half-timbering, pediments and gables.",
            "The gables or parts of the fronts are cut up by false half-timbering set into surfaces of roughcast or white render.",
        ],
        openings=[
            "Rectangular openings, or Tudor-arched (a depressed pointed arch).",
            "Panelled door with or without glazing, surmounted by a transom.",
            "Stone mullioned and transomed windows, or casements with small or large panes, but generally sashes with or without glazing bars; dormers present.",
            "Tall narrow mullioned windows, and projections such as square towers and oriels, to increase the natural light indoors.",
        ],
        materials=[
            "Walls: stone or wood cladding, but generally red brick combined with roughcast or white stucco.",
            "Stone foundation raised above the ground.",
            "Slate, cedar shingle or traditional sheet-metal roof covering.",
        ]),
    blurb_en=(
        "The English manor scaled down for an anglophone bourgeoisie asserting itself: red brick below, white roughcast "
        "and false half-timbering above, upper storeys jettied out over the ground floor, steep gables, tall ornamented "
        "chimneys and stone-mullioned windows under depressed Tudor arches."),
    origin_en=(
        "The neo-Tudor style is a soberer reading of the Tudor vocabulary developed in England in the 16th century under "
        "Henry VIII (1491–1547) and Elizabeth I (1533–1603). Drawing on traditional English and Scottish architecture, it "
        "means to recall the manors and farms of that period. It was popularised at Québec at the end of the 19th century, "
        "among others by architects and by the bourgeois community of Anglo-Saxon stock wanting to assert its cultural "
        "identity — a return to the sources, in pursuit of an authentic English architecture. Present across the city's "
        "territory between 1890 and 1920, it is principally associated with residential architecture."),
)

T[410] = dict(
    slug="maison-neo-georgienne",
    name_en="Neo-Georgian house",
    phase="p6", phase_confidence="provisional",
    canonical=["eclectic-prestige-house", "symmetric-brick-3-5-bay-2st"], styles=["georgian-revival"],
    tenure_plan="single-family", storeys="2–2.5", roof={"form": "gabled", "pitch_deg": 38},
    window_proportion="vertical", principal_cladding=["clay-brick", "wood-clapboard"],
    roofing="asphalt-shingle-dark", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "A revival of the Georgian style at the beginning of the 20th century, after its popularity in Britain and through the thirteen English colonies of North America.",
        ],
        massing=[
            "Composition drawn from English vernacular architecture with the classical ideal applied to it: a system of proportions with the orders and a search for harmony, balance and symmetry; a house with a front of three or five bays with a centred door monumentally treated, and a precise colour scheme — white for the windows, projections and ornaments against the red of the brick and the black of the shutters and doors.",
            "Square or rectangular plan.",
            "Two to three occupied levels (two to two and a half storeys).",
            "Straight two-slope roof, or straight two-slope with half-hips; medium pitch, between 30° and 45°.",
            "Projections: a chimney at each of the gable walls; central projections: perron; central secondary body: porch.",
        ],
        articulation=[
            "Classical ornaments: columns, cornices, pediments, pilasters and cornice returns.",
            "The three or five bays of the front are regularly disposed and the entrance door, with its transom and sidelights, serves as the axis.",
        ],
        openings=[
            "Regular rectangular openings.",
            "Central door with sidelight(s) and transom, fitted with a portal.",
            "Sash windows with small panes fitted with louvred shutters.",
            "Gabled, pedimented or wall-gable dormers, present or not.",
        ],
        materials=[
            "Walls: wood board cladding, but generally brick.",
            "Concrete or stone foundation raised above the ground.",
            "Asphalt shingle or traditional sheet-metal roof covering.",
        ]),
    blurb_en=(
        "Georgian rules applied to a 20th-century house: a square or rectangular block of at least two levels, three or "
        "five bays regularly disposed about a centred door with transom and sidelights, a chimney at each gable end, and "
        "a colour scheme fixed as tightly as the proportions — white trim, red brick, black shutters and door."),
    origin_en=(
        "The Georgian style takes its name from the architecture built in Britain during the reigns of the first four "
        "monarchs of the House of Hanover (1714–1830). Palladian, Gothic, neoclassical and Regency, its sources are "
        "varied, but the Georgian refers more precisely to Renaissance architecture, urging a return to the system of "
        "proportions with the orders and the restoration of overall balance and harmony. After being popularised in "
        "Britain and then through the thirteen English colonies of North America that became the United States in 1776, "
        "it gained a fresh popularity at the beginning of the 20th century as the neo-Georgian."),
)

T[501] = dict(
    slug="maison-de-faubourg-toit-plat",
    name_en="Flat-roofed faubourg house",
    phase="p5", phase_confidence="verified",   # "au tournant du 20e siècle"
    canonical=["faubourg-house-flat-roof"], styles=["vernaculaire-industriel", "boomtown"],
    tenure_plan="mixed", storeys="2–3", roof={"form": "flat", "pitch_deg": 0},
    window_proportion="vertical", principal_cladding=["clay-brick"],
    roofing="membrane", sectors=["SP-VQ"],
    quartiers=["Saint-Roch", "Saint-Sauveur", "Saint-Jean-Baptiste"],
    profile=dict(
        siting_landscape=[
            "Aligned on the pavement; occupies the full width of the lot, hence party walls and a porte cochère.",
            "Transformed the built landscape of the faubourg quarters at the turn of the 20th century, favouring densification.",
        ],
        massing=[
            "Composition: multi-unit house, party-wall, adapted to the urban milieu and densifying the fabric.",
            "Two to three occupied levels.",
            "Flat roof (basin, internal drainage) with membrane covering; or low-pitch flat roof draining to the rear (external drainage), under 15°, in asphalt shingle, membrane, profiled or traditional sheet metal.",
            "Few projections apart from logettes and oriels at the upper floors.",
        ],
        articulation=[
            "Ornament concentrated at the crown: parapet, or a worked cornice in sheet metal or wood; bandeaux, decorative brick, consoles, corbels, planches cornières.",
            "The tinsmith-roofers of the period had to reinvent their decorative work, having lost much of their market to flat roofs covered in tar or membrane and gravel.",
        ],
        openings=[
            "Arched openings, usually segmental, with arches, chambranles and keystones.",
            "Single- or double-leaf door, and a single- or double-leaf porte cochère with or without a wicket, surmounted by a transom.",
            "Openings distributed fairly regularly from one level to the next; window models vary; frequently surmounted by transoms.",
        ],
        materials=[
            "Principal façade in brick.",
            "Side walls: wood board, asbestos-cement shingle or sheet tin.",
        ]),
    blurb_en=(
        "The house that replaced the faubourg's gables. Brick to the street, cheap sheet metal down the sides, filling "
        "its lot from party wall to party wall with a carriage arch punched through it, and all its display saved for "
        "the parapet — the last thing the tinsmiths had left to decorate."),
    origin_en=(
        "A turn-of-the-century densification type that gradually replaced the two-slope and broken-roof houses of "
        "Saint-Roch, Saint-Sauveur and Saint-Jean-Baptiste, and converted single-family ones into flats. Its "
        "architectural simplicity made it compatible with mixed commercial and residential use."),
)

T[502] = dict(
    slug="boomtown",
    name_en="Boomtown house and shop-house",
    phase="p5", phase_confidence="verified",   # "après la Grande Dépression (1873-1896)"
    canonical=["boomtown-false-front"], styles=["boomtown", "vernaculaire-industriel"],
    tenure_plan="mixed", storeys="1–2", roof={"form": "flat-or-low-slope", "pitch_deg": 0},
    window_proportion="vertical",
    principal_cladding=["wood-clapboard", "clay-brick", "wood-shingle", "asbestos-cement-shingle", "metal"],
    roofing="membrane", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Principally associated with urban residential architecture — housing workers' families, for instance — but also referring to commercial architecture.",
            "The balloon frame arrived from the United States and coincided with the rapid growth of the cities and their demographic surge; the type appeared after the Long Depression (1873–1896) and carried on into the first decades of the 20th century.",
        ],
        massing=[
            "Composition: a search for symmetry; single-family house, duplex.",
            "One to two occupied levels (one to two storeys); ground floor in commercial or residential use.",
            "Flat roof (basin or internal drainage); membrane covering. Low-pitch flat roof (external drainage); very low pitch, under 15°; straight two-slope roof; low pitch, under 30°; asphalt shingle, membrane, profiled or traditional sheet-metal covering.",
            "Projections sheltered by an awning: balcony, gallery and perron.",
            "The economy of means dictates a simple plan, a balloon frame, an inexpensive cladding and a stripped-down decoration.",
            "At first a low-pitch roof draining to the rear, reaching 15 degrees, then the flat roof drained internally and covered in tar or membrane and gravel.",
        ],
        articulation=[
            "Ornaments: finials, cornice, crowning, mast, parapet and corner boards.",
            "As the roof is no longer visible, its presence is marked by ornamental work such as the cornice or the parapet.",
            "For Boomtown shops, the cornice or parapet is used to give the volume of the construction some standing.",
        ],
        openings=[
            "Commercial shopfronts.",
            "The gallery often runs across the whole of the principal façade, with a balcony at the upper storey.",
        ],
        materials=[
            "Walls: wood board cladding; balloon frame. Side walls: wood shingle, asbestos shingle, sheet tin or brick paper cladding.",
            "Sometimes clad in brick, often built of wood.",
        ]),
    blurb_en=(
        "Cheap, fast and light: a balloon frame, a simple plan, boards on the front and whatever came to hand down the "
        "sides, under a roof that slopes gently back or lies flat. Because the roof cannot be seen, the whole "
        "architectural argument is moved to the cornice and the parapet at the top of the wall."),
    origin_en=(
        "Industrialisation brought new economical ways of building that sped the work up considerably. The balloon frame, "
        "which came from the United States and was then introduced into Canada, coincided with the rapid growth of the "
        "cities and their demographic surge. Called American Boomtown, the buildings using this lighter frame of sawn "
        "timber appeared above all in the architecture developed after the Long Depression (1873–1896) and carried on "
        "into the first decades of the 20th century. They are easy to build: the economy of means dictates a simple plan, "
        "a balloon frame, an inexpensive cladding and a stripped-down decoration."),
)

T[503] = dict(
    slug="plex",
    name_en="Plex — superposed dwellings",
    phase="p5", phase_confidence="verified",   # "supplante vers 1910 le bâtiment de type Boomtown"
    canonical=["plex-superposed-units", "duplex-flat-roof-brick"], styles=["vernaculaire-industriel"],
    tenure_plan="triplex", storeys="2–4", roof={"form": "flat", "pitch_deg": 0},
    window_proportion="vertical", principal_cladding=["clay-brick"],
    roofing="membrane", sectors=[],
    quartiers=["Montcalm", "Limoilou", "Vieux-Limoilou", "Lairet", "Maizerets"],
    profile=dict(
        siting_landscape=[
            "Common in the urban parts of Québec, notably in the Montcalm and Limoilou quarters — today Vieux-Limoilou, Lairet and Maizerets.",
            "Usually party-wall, which allows a greater urban density; built in numbers, plexes can form ensembles whose fronts are given rhythm by repeated elements.",
            "The small setback left in front of the buildings is what makes the projecting stairs, balconies and galleries possible.",
        ],
        massing=[
            "Composition: multi-unit house, detached, party-wall or in a row, taking in several types including the duplex, triplex and quadruplex, and comprising superposed dwelling units with independent entries reached by exterior or interior stairs.",
            "Two to four occupied levels (two to four storeys).",
            "Flat roof (basin or internal drainage); membrane covering. Low-pitch flat roof (external drainage); very low pitch, under 15°; asphalt shingle, membrane, profiled or traditional sheet-metal covering.",
            "Projections: avant-corps, straight, turning, spiral or recessed stairs, logettes and oriels; projections sheltered by an awning and superposed: balconies, galleries and perrons.",
            "It stands beside, then from about 1910 supplants, the Boomtown building, taking over several of its characteristics: brick cladding, flat roof, imposing cornice or crowning, and standardised components.",
        ],
        articulation=[
            "Ornaments: acroteria, finials, bandeaux, decorative brick, quoins, consoles, corbels, cornice in sheet metal or wood, and crowning.",
            "Ornamental wrought iron used for risers and posts, but generally for the balustrades of the projections.",
        ],
        openings=[
            "Arched openings, usually segmental, fitted with arches and keystones.",
            "Fully glazed door, with or without a transom above.",
            "Compound casements with transom, paired sashes or compound sashes.",
            "The rectangular windows are casements with transoms or sashes, dressed with lintels or flat arches.",
        ],
        materials=[
            "Brick cladding.",
            "The projecting stairs, balconies and galleries are of brick, wood or iron.",
        ]),
    blurb_en=(
        "Two, three or four dwellings stacked with their own front doors, reached — and this is where Québec parts "
        "company with Montréal — by stairs that may be inside as readily as out. Brick, flat-roofed, party-walled, "
        "built in numbers so the oriels, balconies and stairs set up a rhythm along the whole street."),
    origin_en=(
        "The plex is a multi-unit house comprising two (duplex), three (triplex) or four (quadruplex) superposed dwelling "
        "units whose independent entries are reached by exterior or interior stairs. It is common in the urban parts of "
        "Québec, notably in the Montcalm and Limoilou quarters. The promoters and property companies that built out the "
        "city's quarters at the beginning of the 20th century favoured this type, which allowed rapid and logical "
        "building in a compact residential fabric. It stands beside, then from about 1910 supplants, the Boomtown "
        "building, taking over its brick cladding, flat roof, imposing cornice and standardised components."),
)

T[504] = dict(
    slug="maison-cubique",
    name_en="Cubic house (Four Square)",
    phase="p5", phase_confidence="verified",   # "durant la première moitié du 20e siècle"
    canonical=["foursquare-hipped-2st"], styles=["foursquare"],
    tenure_plan="single-family", storeys="2–2.5", roof={"form": "hipped-or-pyramidal", "pitch_deg": 25},
    window_proportion="vertical",
    principal_cladding=["clay-brick", "wood-clapboard", "wood-shingle", "asbestos-cement-shingle"],
    roofing="sheet-metal-traditional", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Built above all during the first half of the 20th century, it is found in the quarters and suburbs of Québec and is strictly associated with residential architecture.",
            "Though a single-family house to begin with, more than one dwelling may be found in it.",
        ],
        massing=[
            "Composition: a search for symmetry; single-family house which may be converted into a multi-unit one.",
            "Generally square plan; imposing volume.",
            "Two to three occupied levels (two to two and a half storeys).",
            "Roof generally straight four-slope or truncated four-slope; low pitch, under 30°; low-pitch flat roof (external drainage); very low pitch, under 15°; asphalt shingle, membrane, profiled or traditional sheet-metal covering. Flat roof (basin or internal drainage); membrane covering.",
            "Projections sheltered by an awning: balcony, gallery wrapping or not, and perron; secondary bodies: annexe, summer kitchen, porch and veranda.",
            "Two variants: a first covered with a flat roof and another, commoner, capped with a low-pitched four-slope roof, occasionally surmounted by a rooftop terrace, with an inhabited attic lit by dormers.",
        ],
        articulation=[
            "Ornaments: brackets, finials, cornices, crowning, pediments, lambrequins and corner boards.",
            "The ornament varies with the taste and the means of the owner.",
        ],
        openings=[
            "Arched openings, usually segmental, fitted with arches, chambranles and keystones.",
            "Compound casements with transom, paired sashes or compound sashes; dormers present or not.",
            "The openings are regularly distributed and the windows are casements with large panes, casements with transoms, or sashes.",
            "Hipped, gabled, triangular or shed dormers.",
        ],
        materials=[
            "Walls: brick, wood board, wood shingle or asbestos shingle cladding.",
            "Traditional sheet metal on the four-slope roof.",
        ]),
    blurb_en=(
        "A square plan, square elevations and two or three levels — a lot of house for the footprint, which is exactly "
        "what the American catalogues sold it on. The common version has a low four-slope roof with dormers in an "
        "inhabited attic; the other is simply flat-topped."),
    origin_en=(
        "Devised in the United States by the architect Frank Kidder in 1891, the cubic house (Four Square House) was "
        "abundantly circulated in architectural catalogues, which made much of the size of its living space. The plan "
        "and elevations of square appearance, and the two or three occupied levels, do give this house an imposing "
        "volume. Built above all during the first half of the 20th century, it is found in the quarters and suburbs of "
        "Québec and is strictly associated with residential architecture. Though a single-family house to begin with, "
        "more than one dwelling may be found in it."),
)

T[505] = dict(
    slug="cottage-vernaculaire-industriel",
    name_en="Industrial-vernacular cottage",
    phase="p5", phase_confidence="verified",   # "la première moitié du 20e siècle"
    canonical=["industrial-vernacular-cottage"], styles=["vernaculaire-industriel"],
    tenure_plan="single-family", storeys="1.5–2.5", roof={"form": "gabled", "pitch_deg": 38},
    window_proportion="vertical",
    principal_cladding=["wood-clapboard", "wood-shingle", "asbestos-cement-shingle", "clay-brick",
                        "concrete-block", "artificial-stone"],
    roofing="asphalt-shingle-dark", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Associated with residential architecture in rural or urban settings; the commonest type in the first half of the 20th century at Québec.",
            "Popularised through pattern books, which supplied standard plans and architectural components alike.",
        ],
        massing=[
            "Composition drawn from the classical revival or from the historical influences: a search for symmetry; single-family house; a type taking in several variants including the colonisation house, the gable-fronted house, the central-dormer house and the storeyed house.",
            "Rectangular, L-shaped or T-shaped plan.",
            "One to three occupied levels (one and a half to two and a half storeys).",
            "Straight two-slope roof, or straight two-slope with half-hips; low pitch, under 30°, or medium, between 30° and 45°.",
            "Projections sheltered by an awning: balcony, gallery wrapping or not, and perron; secondary bodies: annexe, summer kitchen, porch and veranda.",
            "It is distinguished from the traditional Québécois house by a volume rising over one, two or three levels, giving the building more verticality, and by a straight two-slope roof without curved eaves.",
        ],
        articulation=[
            "Ornaments: brackets, cornices, pediments, cut-out woodwork, lambrequins, corner boards and cornice returns.",
        ],
        openings=[
            "Diamond windows in the gable walls; dormers present or not.",
        ],
        materials=[
            "Walls: brick paper, pressed tin, concrete block or artificial masonry cladding, but generally wood board, wood shingle or asbestos shingle.",
            "Asphalt shingle, cedar shingle, profiled or traditional sheet-metal roof covering.",
            "Wood frame.",
        ]),
    blurb_en=(
        "The workers' cottage of the industrial era, ordered out of a pattern book: a rectangle, an L or a T under a "
        "straight two-slope roof with no bell-cast to the eaves, taller and more vertical than the traditional "
        "Québécois house it replaced, and clad in whatever was cheapest that year."),
    origin_en=(
        "The vernacular cottage was popularised through pattern books, in which standard plans and architectural "
        "components were available. Arising out of the industrial period that began a little after the middle of the "
        "19th century in Québec, it is strongly marked by standardisation, and the building of this single-family house "
        "is at once quick, simple and inexpensive. The American vernacular cottage is the commonest type in the first "
        "half of the 20th century at Québec, drawing on various styles, particularly those of the classical revival or "
        "the historical influences."),
)

T[507] = dict(
    slug="immeubles-a-logements",
    name_en="Apartment block with a central stairwell",
    phase="p6", phase_confidence="verified",   # "entre 1920 et 1970 ... s'impose à partir de 1930"
    canonical=["apartment-block-central-stair"], styles=["rationalisme"],
    tenure_plan="walk-up", storeys="2–3", roof={"form": "flat", "pitch_deg": 0},
    window_proportion="vertical", principal_cladding=["artificial-stone", "clay-brick"],
    roofing="membrane", sectors=[], quartiers=["Montcalm", "Saint-Sacrement"],
    profile=dict(
        siting_landscape=[
            "Common in the urban parts of Québec, notably in the Montcalm and Saint-Sacrement quarters; its construction period runs between 1920 and 1970 but it takes hold from 1930.",
            "It is set on a newly developed lot, or on an old lot that has to be rebuilt after a fire.",
            "The promoters and property companies that built out the city's quarters favoured it after the plex, because it gives a greater density of residential fabric.",
        ],
        massing=[
            "Composition: a search for symmetry; a detached or party-wall building with a tripartite front and a centred door monumentally treated.",
            "Square plan; imposing volume.",
            "Two to three occupied levels (two to three storeys); a central stairwell giving access to four, six, eight or more dwellings.",
            "Flat roof (basin or internal drainage); membrane covering.",
            "Central projections: avant-corps and perron; projections sheltered by an awning and superposed: balconies.",
            "The stairwell, which may also be formed with an avant-corps, is lit by a vertical glass-block window and marked by a crowning.",
        ],
        articulation=[
            "Ornaments: bandeaux, decorative brick, cornice, crowning and parapet.",
            "Balconies set on either side of the symmetrical front give the whole composition its rhythm.",
        ],
        openings=[
            "Fully glazed single- or double-leaf door, with or without a transom above, fitted with a portal.",
            "Compound casements with transom, paired sashes, compound sashes, or fixed lights with or without glass blocks.",
            "The rectangular windows are sashes or casements with transoms, and sometimes paired; they are dressed with lintels or flat arches.",
        ],
        materials=[
            "Walls: artificial masonry cladding.",
            "Clad in brick or artificial masonry.",
        ]),
    blurb_en=(
        "What came after the plex when the promoters wanted more density still: a square block, a symmetrical "
        "tripartite front, and one monumental central door opening on a stairwell that serves four, six, eight or more "
        "flats — with a column of glass block up the front to light it."),
    origin_en=(
        "The apartment block is common in the urban parts of Québec, notably in the Montcalm and Saint-Sacrement "
        "quarters. Though its construction period runs between 1920 and 1970, it takes hold from 1930. The promoters and "
        "property companies that had built out the city's quarters at the beginning of the 20th century favoured this "
        "type after the plex, since it allows a greater density of residential fabric. It is a building set on a newly "
        "developed lot, or on an old lot that has to be rebuilt following a fire."),
)

T[508] = dict(
    slug="maison-neocoloniale-neerlandaise",
    name_en="Dutch Colonial Revival house",
    phase="p6", phase_confidence="verified",   # "apparaît durant les années 1920 ... apogée ... 1940"
    canonical=["eclectic-prestige-house"], styles=["colonial-revival"],
    tenure_plan="single-family", storeys="1.5–2.5", roof={"form": "mansard", "pitch_deg": 60},
    window_proportion="vertical",
    principal_cladding=["clay-brick", "wood-clapboard", "wood-shiplap", "wood-shingle",
                        "asbestos-cement-shingle", "stucco"],
    roofing="asphalt-shingle-dark", sectors=["SP-SIL"], quartiers=["Sillery"],
    profile=dict(
        siting_landscape=[
            "It spread through Québec between the wars thanks to the models available in the sales catalogues, and was one of the most popular models of that period, particularly in anglophone circles.",
            "At Québec it appears during the 1920s but reaches its height at the beginning of the 1940s; though rarer, houses of this style are found across practically the whole territory of the city, with a notable concentration in the Sillery quarter.",
        ],
        massing=[
            "Rectangular or L-shaped plan; simple volume.",
            "Two occupied levels (one and a half storeys, more rarely two and a half).",
            "Bell-shaped roof: an asymmetrical broken attic roof made of two pronounced slopes. Wide, elongated, oversailing eaves; asphalt shingle covering. The roof is generally pierced by a wide continuous shed dormer, which adds to its massive look.",
            "Projections: perron, porch or short covered gallery. Most often a portico surmounted by a triangular or semicircular pedimented awning tied to the main roof, carried on single or double columns without a balustrade; annexe, balcony, veranda, chimney at the end of the gable wall.",
            "It is distinguished from the mansard roof by the asymmetry of its slopes, with a very short terrasson and a very long flared brisis recalling the shape of a bell, giving it a massive and austere aspect.",
        ],
        articulation=[
            "Ornamentation: sober, with a more or less ornamented portal around the door, pediment, cornice returns, plain or decorated chambranles, surrounds, shutters or louvred shutters, columns, piers and flat arches.",
            "The bell-shaped roof is truly the centrepiece and the most emblematic attribute of houses belonging to this style.",
        ],
        openings=[
            "Doors: glazed-panel door, screen door with several joinered elements. Entrance placed centrally.",
            "Windows: rectangular, sashes with small panes, or more rarely casements with a fixed paned section. Often accompanied by shutters or louvred shutters. Fixed windows, oval or semicircular, present or not.",
            "Composition of the fronts regular and symmetrical, with an emphasis on the vertical lines.",
        ],
        materials=[
            "Cladding: brick, clapboard, shiplap board, wood shingle, asbestos shingle, render.",
            "Concrete foundation.",
        ]),
    blurb_en=(
        "Known by its roof and almost nothing else: a bell-shaped gambrel of two very unequal slopes — a stub of "
        "terrasson over a long flared brisis — with a wide continuous shed dormer cut into it and deep eaves "
        "oversailing. An interwar catalogue house, and at Québec a Sillery one."),
    origin_en=(
        "The Dutch Colonial Revival house has its origins at the beginning of the 18th century, when Dutch settlers "
        "brought their building traditions into the American colonies; the style became popular quickly in New York "
        "State and along the Hudson. They adapted their European technique to the harsher climate of North America, and "
        "the broken attic roof characteristic of the style was not only an aesthetic choice but a practical one, "
        "optimising the interior space while carrying heavy snowfall. At the beginning of the 20th century the Dutch "
        "colonial style was revived, leading to many houses reflecting the original in a schematised and more uniform "
        "way, through machined materials and standardised components distributed by catalogue. It spread through Québec "
        "between the wars, appearing during the 1920s and reaching its height at the beginning of the 1940s."),
)

T[604] = dict(
    slug="wartime-housing",
    name_en="Wartime Housing house (Cape Cod)",
    phase="p6", phase_confidence="verified",   # "Entre 1942-1945"
    canonical=["wartime-housing-prefab"], styles=["cape-cod", "wartime-housing"],
    tenure_plan="single-family", storeys="1–1.5", roof={"form": "gabled", "pitch_deg": 38},
    window_proportion="vertical", principal_cladding=["clay-brick", "asbestos-cement-shingle", "wood-clapboard"],
    roofing="asphalt-shingle-dark", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Concentration of houses marked by tight subdivision and a regular siting.",
            "Between 1942 and 1945 Wartime Housing Limited put up single-family houses across the country, notably in the quarters and suburbs of Québec.",
            "The sectors where Cape Cod dwellings are found are marked by tight subdivision and regular siting.",
        ],
        massing=[
            "Composition drawn from the English house of the colonial period in New England, and belonging to the line of industrial vernacular architecture: an affordable single-family house, built quickly and without symmetry; originally prefabricated and assembled on site without a footing.",
            "Over the years the house may be renovated, enlarged, raised by a storey, or given a dormer.",
            "Eaveless roof; medium pitch, between 30° and 45°.",
            "Projection: perron.",
            "The attic is sometimes habitable, though roof pitches vary considerably from one construction to another.",
        ],
        articulation=[
            "The Cape Cod house contains few ornamented details.",
        ],
        openings=[
            "Panelled door with glazing, or solid.",
            "Windows single, paired or grouped, sashes with or without glazing bars.",
            "Dormers present or not, including the central gabled or shed dormer.",
        ],
        materials=[
            "Walls: brick or asbestos shingle cladding; gables of the side walls: cladding the same as, or different from, that of the walls.",
            "Concrete foundation.",
            "Asphalt shingle or profiled sheet-metal roof covering.",
            "The materials used had to be non-essential to the war industry, light enough to handle on site, and among the cheapest available.",
        ]),
    blurb_en=(
        "A federal housing programme rendered as a house: a small eaveless gabled box, prefabricated and set down "
        "without a footing, built of whatever the war industry did not need, in tightly subdivided sectors laid out on "
        "a regular grid. Most have since been renovated, raised or given a dormer."),
    origin_en=(
        "When Wartime Housing Limited was created in 1942 by the Canadian federal government, the new company's mandate "
        "was to house the families of soldiers and the workers of the war industry quickly and economically. Between "
        "1942 and 1945 it put up single-family houses across the country, notably in the quarters and suburbs of Québec. "
        "Having become the Central Mortgage and Housing Corporation in 1946, it carried on after the second conflict, "
        "since the return of the combatants brought another campaign of affordable house-building. The Wartime Housing "
        "house draws on the English dwelling of the colonial period in New England — the Cape Cod style — and belongs to "
        "the line of 20th-century industrial vernacular architecture."),
)

T[606] = dict(
    slug="camp-et-chalet-de-villegiature",
    name_en="Camp and villégiature chalet",
    phase="p6", phase_confidence="provisional",
    canonical=["detached-cottage-steep-gable"], styles=["regionalisme-quebecois", "vernaculaire-industriel"],
    tenure_plan="single-family", storeys="1–1.5", roof={"form": "gabled", "pitch_deg": 25},
    window_proportion="horizontal", principal_cladding=["wood-shingle", "wood-shiplap", "wood", "stone"],
    roofing="asphalt-shingle-dark", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "A seasonal secondary dwelling set in a natural setting; the camp is found above all in forest country.",
            "The chalet's living spaces extend outdoors, opening onto a sun room, a screened veranda, a perron or a terrace.",
            "In its initial phase of occupation it rarely has hard foundations, and is neither insulated nor heated other than by a hearth or a stove; running water and sanitary fittings are often added late.",
        ],
        massing=[
            "Composition and structural type: for camp and chalet alike, belonging to vernacular architecture — techniques of stacked round logs, of traditional stone masonry (notably for the hearth), the use of a light frame and of the ordering typical of the North American house of the industrial period.",
            "Size: one storey, or never more than a storey and a half.",
            "Roof: low-pitched, often with an eave.",
            "The camp or 'cabane' is the simplest and most modest model of the villégiature dwelling: small, of a single room, built cheaply with a light frame and a low-pitched roof.",
            "Larger than the camp, the chalet is arranged to give basic comfort; there is no specific style attached to it, and the buildings are more or less elaborate according to the owner's means.",
        ],
        articulation=[
            "Characteristic components: gallery, veranda glazed or screened, chimneys and stone hearths; shutters allowing the building to be protected out of season against the weather and against intruders.",
            "The chalet attaches to the main architectural currents and neo-styles of the 20th century — industrial vernacular, arts and crafts, bungalow and so on.",
        ],
        openings=[
            "Openings of varied shapes: doors and windows with screens.",
            "The camp has few openings, generally of small dimensions.",
        ],
        materials=[
            "Walls: cladding in natural materials, generally wood, with a preference for shingle and shiplap board.",
            "Generally without foundations, built on wood or stone piles, though some bulkier chalets, or ones built on a slope, have foundations of locally quarried stone.",
            "Roof covering in modest materials: asphalt shingle, asphalt paper, shingle or sheet metal.",
            "In its rustic version, above all in forest country, the camp is built of 'bois rond' — stacked logs, a material taken on the spot.",
        ]),
    blurb_en=(
        "The cheap seasonal dwelling the 20th century added below the villa: a one-room camp of stacked logs, or a "
        "chalet a size up with a screened veranda and a stone hearth, on wood piles rather than foundations, shuttered "
        "against the weather and the intruders for the months nobody is there."),
    origin_en=(
        "While the villa and the country house count as villégiature residences, they differ little from urban houses in "
        "their size, their styles and the comfort they offer. In the 20th century more affordable secondary dwellings "
        "intended for seasonal use became popular: the camp and the chalet. The camp is the simplest and most modest "
        "model, built in its rustic version of stacked round logs taken on the spot, of a single room, serving above all "
        "to shelter the users of an outdoor way of life; in the 20th century the hotel industry took up the cabin model "
        "to create the 'cabine', a forerunner of the first motels. The chalet is larger and arranged for basic comfort, "
        "with no specific style attached to it."),
)

T[701] = dict(
    slug="arts-and-crafts",
    name_en="Arts and Crafts house",
    phase="p6", phase_confidence="verified",   # "Érigés durant la première moitié du 20e siècle"
    canonical=["english-revival-stone-2st", "modest-tudor-cottage-brick-2st"],
    styles=["arts-and-crafts", "arts-et-metiers"],
    tenure_plan="single-family", storeys="1.5–2.5", roof={"form": "gabled-or-hipped", "pitch_deg": 38},
    window_proportion="vertical",
    principal_cladding=["wood-shingle", "stone", "clay-brick", "roughcast", "stucco"],
    roofing="cedar-shingle", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "The Arts and Crafts house is conceived in complementarity with the setting it stands in, physical and natural alike.",
            "Built during the first half of the 20th century at Québec, and principally associated with residential architecture.",
        ],
        massing=[
            "Composition drawn from the architecture of the English countryside, itself drawn from the local way of building with regard to craft, materials and know-how: a picturesque effect, integrating the forms into the natural and built environment.",
            "Square or rectangular plan, but generally irregular; an informal plan.",
            "Two to three occupied levels (one and a half to two and a half storeys); the upper storeys project over the ground floor.",
            "Straight two- or four-slope roof, straight two-slope with half-hips, two-slope broken, multi-slope or asymmetrical; low pitch, under 30°, medium, between 30° and 45°, or steep, over 45°.",
            "Projections: chimneys, gallery sheltered by the straight eave or by the upper storeys, logettes, oriels and perron; secondary bodies: annexe and veranda.",
        ],
        articulation=[
            "Reduced ornament: rafters, false half-timbering, piers and corner boards.",
            "The decorative components stay simple: false half-timbering, exposed rafters at the ends of the roof, corner boards and chambranles.",
        ],
        openings=[
            "Rectangular openings fitted with chambranles.",
            "Panelled door with glazing, with or without a transom above.",
            "Windows single, paired or grouped, with or without glazing bars forming diamonds; casements with transom, compound casements with transom, sashes with or without glazing bars, sashes with small panes or compound sashes.",
            "Dormers present, including the central shed dormer.",
        ],
        materials=[
            "Walls: stone, wood — generally wood shingle — or brick cladding combined with roughcast or render.",
            "Concrete or stone foundation raised above the ground.",
            "Cedar shingle or traditional sheet-metal roof covering.",
        ]),
    blurb_en=(
        "The English cottage as an argument against the factory: an informal plan, wood shingle over stone or brick, "
        "upper storeys jettied out, a gallery tucked under the eaves, and ornament cut back to exposed rafters, corner "
        "boards and a little false half-timbering."),
    origin_en=(
        "In 19th-century England, society underwent major transformations because of industrialisation, and movements of "
        "thought appeared in reaction to the loss of the traditional social structure. The adherents of the Arts and "
        "Crafts movement proposed an architecture drawn from craft and from the dwelling of the English countryside, "
        "valuing a return to manual work, the use of traditional materials and recourse to local know-how as an obstacle "
        "to standardisation. The movement then reached the United States, where it was known through several styles — "
        "the Shingle Style on the east coast, the Prairie Style in the centre, and the Craftsman Style on the west. Its "
        "popularity was largely owed to the architectural catalogues and magazines distributed across North America from "
        "the beginning of the 20th century, although its ideology was poorly understood."),
)

T[801] = dict(
    slug="bungalow",
    name_en="Bungalow",
    phase="p6", phase_confidence="verified",   # "dans les années 1950 et 1960"
    canonical=["one-storey-ranch-low-roof", "split-level"], styles=["ranch", "minimal-traditional"],
    tenure_plan="single-family", storeys="1–1.5", roof={"form": "gabled", "pitch_deg": 25},
    window_proportion="horizontal", principal_cladding=["clay-brick", "stone", "artificial-stone",
                                                        "wood-clapboard", "metal-siding"],
    roofing="asphalt-shingle-dark", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Concentration of houses marked by a parallel siting, set back from the street.",
            "It became popular across the whole continent on the strength of the baby boom, the growth of the suburbs, easier access to ownership and the popularity of the car.",
            "So popular that it became a genuine consumer product manufactured in series — the queen of the suburb and the symbol of the American dream.",
        ],
        massing=[
            "Composition seeking to renew the form of residential architecture: a single-family house for the middle class, which dominates the development of the suburbs, draws on influences from the past, and takes in several types including the North American bungalow, the long-fronted bungalow and the split-level.",
            "Long-fronted bungalow (the popular model in Québec): rectangular plan, level with the ground.",
            "One occupied level (one storey); a vestibule separating the day rooms on one side from the night rooms on the other.",
            "Straight two-slope roof; low pitch, under 30°.",
            "Projections: awning and bay window.",
            "Other variants: square or L-shaped plan; two occupied levels (one and a half storeys); straight two-slope, straight four-slope or asymmetrical roof, medium pitch between 30° and 45°; or flat roof (basin or internal drainage).",
            "Secondary bodies: cellar entrance and garage.",
        ],
        articulation=[
            "Reduced ornament: rafters and corner boards.",
        ],
        openings=[
            "Numerous openings; panelled door with glazing, or solid.",
            "Windows single, paired or grouped, fitted with chambranles; casements with or without transom, compound casements with or without transom, sashes with small panes, sashes with or without glazing bars, or compound sashes.",
            "Dormers present, including the central hipped, gabled or shed dormer.",
        ],
        materials=[
            "Walls: brick, stone, artificial masonry, wood board, aluminium board, plastic board or wood-fibre board cladding.",
            "Concrete foundation.",
            "Asphalt shingle roof covering.",
            "Other variants: wood shingle or asbestos shingle cladding.",
        ]),
    blurb_en=(
        "One storey level with the ground, a long low rectangle with a vestibule dividing the day rooms from the night "
        "rooms, a shallow gable, a picture window and a garage. Descended from the Prairie house and the California "
        "ranch, and by the 1950s manufactured in series like any other consumer product."),
    origin_en=(
        "Descended from the Prairie style but also from certain Californian house models such as the ranch house, the "
        "postwar North American bungalow was popularised across the whole continent on the strength of the baby boom, "
        "the growth of the suburbs, easier access to home ownership and the popularity of the car. The bungalow, "
        "designed for the nuclear family wanting its own ground and a single-storey house with a garage, was a runaway "
        "success in the 1950s and 1960s — so much so that it became a genuine consumer product manufactured in series, "
        "the queen of the suburb and the symbol of the American dream. Given how popular it was, several residential "
        "quarters developed by working different variants of it."),
)

T[802] = dict(
    slug="style-international",
    name_en="International Style house (residential)",
    phase="p6", phase_confidence="verified",   # "dès 1935 ... à Québec"
    canonical=["modern-slab-tower", "modern-slab-flat-brick"], styles=["international-style"],
    tenure_plan="single-family", storeys="2–3", roof={"form": "flat", "pitch_deg": 0},
    window_proportion="horizontal", principal_cladding=["stucco", "clay-brick", "metal", "stone"],
    roofing="membrane", sectors=["SP-SIL"], quartiers=["Sillery"],
    profile=dict(
        siting_landscape=[
            "The building is put up in an isolated context — that is, without any real regard for the environment or the setting it is inserted into.",
            "The first manifestations of the International Style appear at Québec from 1935, notably with the building of white or brick houses of stripped-down form at Sillery, designed among others by the architects Robert Blatter and Charles A. Jean.",
        ],
        massing=[
            "Composition drawn from modernism, breaking totally with the forms of the past: a dominant horizontality, a stripped-down character, the volumes set off and brought forward, without symmetry, without regard for the natural and built environment, forms sometimes borrowed from the means of transport, fronts of smooth uniform surfaces, a palette of neutral sober colours, and an exterior that accounts for the interior organisation of the building.",
            "Assembly of volumes and play of solids and voids.",
            "Flat roof (basin or internal drainage) or flat roof laid out as a terrace; membrane covering.",
            "Projections: gallery, marquee, perron, pilotis, portal and portico.",
            "The distinct volumes, expressing the interior functions, are assembled and treated uniformly.",
        ],
        articulation=[
            "The smooth exterior surfaces carry no ornament and their colours stay neutral and sober; walls covered in stucco come in various shades of white, grey or light pastel.",
            "Regularity and stripping-down applied as a principle, using every possibility offered by concrete, steel and glass.",
        ],
        openings=[
            "Numerous openings; panelled door with glazing, solid, or fully glazed.",
            "Corner windows, ribbon windows, or fixed lights with glass blocks.",
        ],
        materials=[
            "Walls: stone, concrete, metal, metal-and-glass curtain wall, or render cladding; frame of wood, steel or reinforced concrete.",
            "Concrete foundation with or without pilotis.",
        ]),
    blurb_en=(
        "Smooth white walls, a flat roof, corner and ribbon windows, volumes assembled to show what is happening inside "
        "and no ornament anywhere — a house built as though the site had no history. At Québec that means Sillery from "
        "1935, and Robert Blatter."),
    origin_en=(
        "The principal characteristic of the International Style is building in total rupture with the traditions of the "
        "past. The architects of this school set off the volumes with smooth unornamented exterior surfaces, so that "
        "those volumes could be reproduced anywhere in the world with the least possible local cultural inflection. The "
        "style results from the marriage of European ideas out of the Bauhaus with the steel-and-glass building "
        "techniques of the United States; one of its foundations comes from Ludwig Mies van der Rohe — 'Less is more'. "
        "The first manifestations appear at Québec from 1935, notably with white or brick houses of stripped-down form "
        "at Sillery designed by Robert Blatter and Charles A. Jean."),
)

T[808] = dict(
    slug="prairie",
    name_en="Prairie house (Frank Lloyd Wright inspiration)",
    phase="p6", phase_confidence="provisional",
    canonical=["prairie-contemporary"], styles=["prairie", "arts-and-crafts"],
    tenure_plan="single-family", storeys="1–2", roof={"form": "hipped", "pitch_deg": 20},
    window_proportion="horizontal", principal_cladding=["clay-brick", "wood", "stucco"],
    roofing="asphalt-shingle-dark", sectors=[], quartiers=None,
    profile=dict(
        siting_landscape=[
            "Horizontality and regard for the natural environment.",
            "Wright designed for his wealthy clients several houses of very elongated, horizontal form fitting perfectly into the prairie landscapes of the American Midwest.",
            "At Québec, certain bungalows reflect this Prairie influence.",
        ],
        massing=[
            "Composition drawn from the architecture of the American Midwest, breaking with the forms of the past: horizontality and regard for the natural environment; a style seen as one of the variants of the Arts and Crafts movement, popularised in the United States.",
            "Simple volumes.",
            "Projections sheltered by an awning: perron and gallery.",
            "The model was taken up across North America by architects and builders for middle-class people wanting an individual house in the suburbs, worked through every form while keeping the horizontal treatment of its architecture.",
            "These houses may have a flat or low-pitched roof.",
        ],
        articulation=[
            "The horizontal treatment of the architecture is what is kept through every variant of the model.",
        ],
        openings=[],
        materials=[
            "Wood frame.",
            "The houses present various materials.",
        ]),
    blurb_en=(
        "Wright's long low horizontal house, worked down from wealthy clients to suburban builders across North "
        "America, keeping only the horizontality. The thesaurus's own fiche is brief; at Québec its clearest trace is "
        "in the bungalow, which the City files as its déclinaison."),
    origin_en=(
        "The architect Frank Lloyd Wright was among the first, at the beginning of the 20th century, to develop a "
        "typically American mode of dwelling. For his wealthy clients he designed several houses of very elongated and "
        "horizontal form that fitted perfectly into the prairie landscapes of the American Midwest. The model was then "
        "taken up across North America by architects and builders for middle-class people who wanted an individual, "
        "personalised house in the suburbs; they worked it through every form while keeping the horizontal treatment of "
        "its architecture, so that these houses may have a flat or low-pitched roof and present various materials. At "
        "Québec, certain bungalows reflect this Prairie influence."),
)

# --------------------------------------------------------------- parent nodes (courants)
# tid -> (slug, name_en, phase). §2.4 names 202, 302, 401, 403 and 506; 105 is the crawl's
# own find and is the parent of 101/102 in docs_tableau_styles.pdf.
COURANT_TIDS = {
    105: ("colonial-francais", "Colonial français (courant)", "p1"),
    202: ("neoclassique", "Néoclassique (courant)", "p2"),
    302: ("neoclassique-quebecois", "Néoclassique québécois (courant)", "p3"),
    401: ("second-empire", "Second Empire (courant)", "p4"),
    403: ("eclectisme", "Éclectisme (courant)", "p5"),
    506: ("vernaculaire-industriel", "Vernaculaire industriel (courant)", "p5"),
}

# -------------------------------------------------- the nine landing pages (top-level courants)
# These have no tid: they are .aspx pages, not thesaurus nodes. Their French description is the
# landing page's own intro, scraped by families.py-style extraction inside this script.
FAMILY_PAGES = [
    ("influences-francaises", "influences-francaises", "Influences françaises",
     "French influences", "p1"),
    ("influences-britanniques", "influences-britanniques", "Influences britanniques",
     "British influences", "p2"),
    ("milieu-quebecois", "milieu-quebecois", "Milieu québécois",
     "The Québécois milieu", "p3"),
    ("influence-styles-historiques", "influences-styles-historiques", "Influence des styles historiques",
     "The historical styles", "p4"),
    ("influences-americaines", "influences-americaines", "Influences américaines",
     "American influences", "p5"),
    ("influences-marginales", "influences-marginales", "Influences marginales",
     "Marginal influences", "p6"),
    ("influences-traditionnelles-modernes", "influences-traditionnelles-modernes",
     "Influences traditionnelles et modernes", "Traditional and modern influences", "p6"),
    ("influences-modernes", "influences-modernes", "Influences modernes",
     "Modern influences", "p6"),
    ("influences-contemporaines", "influences-contemporaines", "Influences contemporaines",
     "Contemporary influences", "p6"),
]

# ------------------------------------------------- non-residential nodes, recorded not rendered
# tid -> (slug, name_en, phase, what its linked exemplars actually are)
NONRES = {
    103: ("classicisme-francais", "Classicisme français", "p1", "churches and monasteries"),
    406: ("neo-roman", "Néo-roman", "p5", "four parish churches"),
    408: ("neo-baroque", "Néo-baroque", "p5", "a seminary chapel, a memorial building and a bank"),
    411: ("chateau", "Château", "p5", "hotels and institutional pavilions"),
    601: ("rationalisme", "Rationalisme", "p6", "churches and office buildings"),
    602: ("beaux-arts", "Beaux-arts", "p6", "commercial blocks on rue Saint-Jean"),
    603: ("art-deco", "Art déco", "p6", "commercial and office buildings"),
    702: ("regionalisme-quebecois", "Régionalisme québécois", "p6",
          "a church, an art centre, a youth centre and a school"),
    703: ("dom-bellot", "Dom Bellot", "p6", "four churches"),
    803: ("fonctionnalisme", "Fonctionnalisme", "p6", "a gallery, an office building and churches"),
    804: ("expressionnisme", "Expressionnisme", "p6", "a library, churches and a hotel"),
    805: ("modernisme", "Modernisme", "p6", "a restaurant, a community centre and churches"),
    806: ("brutalisme", "Brutalisme", "p6", "a church, a theatre and government towers"),
    809: ("paquebot", "Paquebot (Streamline Moderne)", "p6", "a medical centre and commercial blocks"),
    810: ("neo-regionalisme", "Néo-régionalisme", "p6",
          "houses and addresses, but the fiche is two bullets long and describes no dwelling"),
    901: ("postmodernisme", "Postmodernisme", "p6", "broadcast, bank and office buildings"),
    902: ("high-tech", "High-tech", "p6", "a convention centre and a library"),
    903: ("minimalisme", "Minimalisme", "p6", "community centres and institutional pavilions"),
    904: ("contemporaine", "Contemporaine", "p6", "theatres and a college"),
}

EMPTY_PROFILE = {k: [] for k in
                 ("siting_landscape", "massing", "articulation", "openings", "materials")}


def base(slug, name_en, name_fr, phase):
    """The keys build.py requires of every type record."""
    return {
        "id": f"quebec.{slug}", "place": "quebec", "phase": phase,
        "name_en": name_en, "name_fr": name_fr,
        "source_generation": SOURCE_GENERATION,
        "canonical": [], "styles": [], "style_label": None,
        "tenure_plan": "mixed", "storeys": None,
        "roof": {"form": None, "pitch_deg": None},
        "window_proportion": None, "principal_cladding": [], "roofing": None, "garage": None,
        "lot_width_m": None, "setback_front_m": None, "setback_side_m": None,
        "front_yard_green_pct": None,
        "sectors": [], "conservation": [], "conservation_fr": None,
    }


def photo(tid, illustration):
    """The thesaurus drawings are © Ville de Québec and may not be reproduced (see MANIFEST)."""
    return [{"file": None,
             "source_url": illustration or f"{LANDING}/thesaurus.aspx?tid={tid}",
             "credit": CREDIT, "licence": "permission required", "kind": "placeholder"}]


def emit(rec, slug):
    path = OUT / f"{slug}.yaml"
    path.write_text(yaml.dump(rec, allow_unicode=True, sort_keys=False, width=110,
                              default_flow_style=False), encoding="utf-8")
    return path


def main(argv):
    dry = "--dry" in argv
    parsed = {r["tid"]: r for r in json.loads(PARSED.read_text(encoding="utf-8"))}
    OUT.mkdir(parents=True, exist_ok=True)
    written = []

    # ---- residential types
    for tid, cur in sorted(T.items()):
        p = parsed[tid]
        if not p["elements_caracteristiques"]:
            sys.exit(f"encode.py: tid {tid} parsed with an empty bullet list — fix the parser")
        rec = base(cur["slug"], cur["name_en"], p["name_fr"], cur["phase"])
        rec.update({
            "tid": tid,
            "phase_confidence": cur["phase_confidence"],
            "courant": p["courant"],
            "source_ref": f"Ville de Québec, Thésaurus du patrimoine bâti, fiche tid={tid}",
            "source_url": p["url"],
            "sectors": cur["sectors"],
            "quartiers": cur["quartiers"],
            "canonical": cur["canonical"], "styles": cur["styles"],
            "tenure_plan": cur["tenure_plan"], "storeys": cur["storeys"], "roof": cur["roof"],
            "window_proportion": cur["window_proportion"],
            "principal_cladding": cur["principal_cladding"], "roofing": cur["roofing"],
            "profile": cur["profile"],
            "profile_fr": {"description": p["description"],
                           "elements_caracteristiques": p["elements_caracteristiques"]},
            "profile_note": NOTE.format(tid=tid, date=CONSULTED),
            "conservation": [],
            "blurb_en": cur["blurb_en"], "origin_en": cur["origin_en"],
            "related_buildings": p["related_buildings"] or None,
            "photos": photo(tid, p["illustration"]),
        })
        if not dry:
            emit(rec, cur["slug"])
        written.append((cur["slug"], "type"))

    # ---- parent nodes with a tid
    for tid, (slug, name_en, phase) in sorted(COURANT_TIDS.items()):
        p = parsed[tid]
        rec = base(slug, name_en, p["name_fr"], phase)
        rec.update({
            "tid": tid, "is_courant": True,
            "courant": p["famille"],
            "source_ref": f"Ville de Québec, Thésaurus du patrimoine bâti, fiche tid={tid}",
            "source_url": p["url"],
            "profile": dict(EMPTY_PROFILE),
            "profile_fr": {"description": p["description"],
                           "elements_caracteristiques": p["elements_caracteristiques"]},
            "profile_note": COURANT_NOTE,
            "blurb_en": f"A parent node of the thesaurus: the {p['name_fr']} current, "
                        f"under which the City files its named house types.",
            "origin_en": p["description"][0] if p["description"] else
                         f"The {p['name_fr']} current of the Ville de Québec thesaurus.",
            "related_buildings": p["related_buildings"] or None,
            "photos": photo(tid, p["illustration"]),
        })
        if not dry:
            emit(rec, slug)
        written.append((slug, "courant"))

    # ---- the nine landing pages
    fam_desc = landing_descriptions()
    for slug, page, name_fr, name_en, phase in FAMILY_PAGES:
        desc, period = fam_desc[page]
        rec = base(slug, f"{name_en} ({period})", name_fr, phase)
        rec.update({
            "is_courant": True,
            "courant": None,
            "source_ref": f"Ville de Québec, Thésaurus du patrimoine bâti, courant « {name_fr} »",
            "source_url": f"{LANDING}/{page}.aspx",
            "profile": dict(EMPTY_PROFILE),
            "profile_fr": {"description": desc},
            "profile_note": (
                "One of the nine top-level currents of the thesaurus — a landing page, not a "
                "thesaurus node, so it carries no tid and no Éléments caractéristiques list. "
                "Recorded so the nine-current tree can be read whole and checked against "
                "docs_tableau_styles.pdf; given no card and no page of its own. Its French is "
                f"the landing page's own introduction, verbatim. Period band: {period}."),
            "blurb_en": f"One of the thesaurus's nine top-level currents, {period}.",
            "origin_en": desc[0] if desc else f"The {name_fr} current, {period}.",
            "related_buildings": None,
            "photos": [{"file": None, "source_url": f"{LANDING}/{page}.aspx",
                        "credit": "© Ville de Québec", "licence": "permission required",
                        "kind": "placeholder"}],
        })
        if not dry:
            emit(rec, slug)
        written.append((slug, "courant"))

    # ---- non-residential nodes
    for tid, (slug, name_en, phase, ex) in sorted(NONRES.items()):
        p = parsed[tid]
        rec = base(slug, name_en, p["name_fr"], phase)
        rec.update({
            "tid": tid, "is_residential": False,
            "courant": p["famille"] or p["courant"],
            "source_ref": f"Ville de Québec, Thésaurus du patrimoine bâti, fiche tid={tid}",
            "source_url": p["url"],
            "profile": dict(EMPTY_PROFILE),
            "profile_fr": {"description": p["description"],
                           "elements_caracteristiques": p["elements_caracteristiques"]},
            "profile_note": NONRES_NOTE.format(ex=ex),
            "blurb_en": f"A thesaurus style outside this site's residential scope: its linked "
                        f"exemplars are {ex}.",
            "origin_en": p["description"][0] if p["description"] else name_en,
            "related_buildings": p["related_buildings"] or None,
            "photos": photo(tid, p["illustration"]),
        })
        if not dry:
            emit(rec, slug)
        written.append((slug, "non-residential"))

    kinds = {}
    for _, k in written:
        kinds[k] = kinds.get(k, 0) + 1
    print(f"{'would write' if dry else 'wrote'} {len(written)} records to {OUT}")
    for k, n in sorted(kinds.items()):
        print(f"  {k}: {n}")
    covered = set(T) | set(COURANT_TIDS) | set(NONRES)
    missing = set(parsed) - covered
    if missing:
        sys.exit(f"encode.py: crawled tids with no disposition: {sorted(missing)}")
    return 0


def landing_descriptions():
    """The nine landing pages' own intro paragraphs and period band, verbatim."""
    import re
    out = {}
    for _, page, _, _, _ in FAMILY_PAGES:
        raw = (HERE / "html" / f"{page}.html").read_text(encoding="utf-8", errors="replace")
        i = raw.find('<div id="texte"')
        j = raw.find("titrebande", i)
        seg = raw[i:j]
        per = re.search(r'class="soustitre">(.*?)</p>', seg, re.S)
        band = _clean(per.group(1)).strip("()").strip() if per else None
        paras = [_clean(p) for p in re.findall(r"<p>(.*?)</p>", seg, re.S)]
        out[page] = ([p for p in paras if p and p != band and not p.startswith("(")], band)
    return out


def _clean(s):
    import html as h
    import re
    s = re.sub(r"(?i)</?(sup|sub|strong|em|b|i|span|a)\b[^>]*>", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = h.unescape(s).replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"(?<=\w)-\s+(?=\w)", "-", s)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
