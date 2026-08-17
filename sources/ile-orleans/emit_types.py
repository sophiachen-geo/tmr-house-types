#!/usr/bin/env python3
"""Emit data/places/ile-orleans/types/*.yaml from the parse plus hand-authored English.

Every French string in `profile_fr.elements_caracteristiques` is copied byte-for-byte
out of sources/ile-orleans/parsed.json, which parse.py produces from the PDF. Nothing
French is retyped, so the encoded records cannot drift from the source. The English
columns, blurb and origin are editorial and live in ENGLISH below; they are written
against the same bullets and add no facts the source does not carry.

    python3 sources/ile-orleans/emit_types.py           # write the eleven files
    python3 sources/ile-orleans/emit_types.py --check   # verify what is on disk
"""
import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "data" / "places" / "ile-orleans" / "types"
PARSED = HERE / "parsed.json"

SRC_GEN = ("Patri-Arch inventory synthesis (cover Août 2014, fieldwork 2013–14, "
           "reissued 2025 as …maj2025.pdf), \"Principaux éléments caractéristiques\"")
INV_URL = "https://mrc.iledorleans.com/stock/fra/rapport_synthese_io_050919_maj2025.pdf"
RPCQ = "https://www.patrimoine-culturel.gouv.qc.ca/rpcq/detail.do?methode=consulter&id={}&type=bien"

# The MRC inventory's own photographs are © Patri-Arch with rights ceded to the MRC and
# require the credit "© Patri-Arch". They are recorded, never copied into assets/.
def mrc_photo(page, what):
    return {"file": None, "kind": "placeholder",
            "credit": f"MRC de L'Île-d'Orléans / Patri-Arch, rapport de synthèse, p. {page} — "
                      f"{what}. © Patri-Arch; rights ceded to the MRC de L'Île-d'Orléans. "
                      f"Not reproduced here.",
            "source_url": INV_URL, "licence": "permission required",
            "match_confidence": "address"}


def commons(fn, subject, author, lic, lic_url, file_url, confidence):
    return {"file": f"assets/places/ile-orleans/{fn}", "kind": "single",
            "credit": f"{subject}. Photograph by {author}, {lic}. "
                      f"Licence: {lic_url}. File: {file_url}",
            "source_url": file_url, "licence": lic, "match_confidence": confidence}


ENGLISH = {
"maison-inspiration-francaise": dict(
  phase="p1", name_en="House of French inspiration", name_fr="La maison d'inspiration française",
  canonical=["french-rural-house-1st-hip", "french-urban-house-stone"], styles=["french-regime"],
  storeys="1–1.5", roof={"form": "gabled-or-hipped-steep", "pitch_deg": 45},
  window_proportion="vertical", principal_cladding=["fieldstone-rendered", "wood"],
  roofing="cedar shingle", sectors=["UP-1", "UP-2"],
  profile=dict(
    siting_landscape=["Present in every municipality on the island and relatively abundant — the surviving fabric of the Régime français.",
                      "The plan de conservation places the Régime-français houses near the river, reached from the chemin Royal by long montées."],
    massing=["Low rectangular main body with no or almost no foundation; the original volume has often been lengthened rather than replaced.",
             "Steep two-slope or hipped roof, over 45°, most often covered in cedar shingle."],
    articulation=["Ornament reduced to its simplest expression, limited to encadrements, linteaux, chambranles and épis."],
    openings=["Asymmetrical façade composition; few openings, to limit heat loss.",
              "Double-casement windows with small panes, fitted with functional shutters."],
    materials=["Stone carré carrying a slight batter (fruit), often rendered or clad in wood.",
               "Massive stone chimney at the centre of the house."]),
  blurb_en="The island's founding house and still its commonest old one: a low stone box with barely any foundation, its walls battered slightly inward, a single massive chimney at the centre, and a roof so steep and so short-eaved that it reads as almost all roof. Everything decorative is in the frames of the openings.",
  origin_en="The house of the Régime français, built from the first concessions of 1648 onward and repeatedly lengthened rather than replaced. The inventory describes it as an architecture \"sans architecte\", brought by colonists and tradesmen from rural France and adapted fast to local stone, local timber and a hard climate — more chimney stacks, fewer openings. Dormers appear only at the end of the regime. Most of the island's nineteen classed immeubles patrimoniaux belong to this courant.",
  related_buildings=[
    {"name": "Maison Morisset (\"La Brimbale\"), 4417 chemin Royal, Sainte-Famille — ancienne maison de ferme d'esprit français built before 1699 and enlarged before 1727; stone, 1½ storeys, steep two-slope roof upturned on one side; classée 7 June 1962 (RPCQ 92475)", "url": RPCQ.format(92475)},
    {"name": "Maison Gagnon (\"Maison L'Âtre\"), Sainte-Famille — stone farmhouse of rectangular plan, 1½ storeys, built in two stages après 1680 – avant 1760; classée 6 December 1961 (RPCQ 92667)", "url": RPCQ.format(92667)},
    {"name": "Maison Drouin, Sainte-Famille — \"résidence d'inspiration française érigée peu après 1729 et agrandie vers 1734\"; rendered stone, 1½ storeys, steep slightly upturned slopes, wide central stack, gable dormer; classée 11 February 2010 (RPCQ 102270)", "url": RPCQ.format(102270)},
    {"name": "Manoir Mauvide-Genest, Saint-Jean — \"ancienne résidence seigneuriale érigée en 1734, probablement surhaussée vers 1738 et agrandie de façon importante avant 1755\"; rendered stone, 2½ storeys, high hipped roof; classé 8 December 1971, national historic site 1993 (RPCQ 92670)", "url": RPCQ.format(92670)},
    {"name": "Maison Gendreau, Saint-Laurent — 18th-century rural house of French inspiration, stone, 1½ storeys, steep hipped roof; classée 12 August 1964 (RPCQ 92491)", "url": RPCQ.format(92491)},
    {"name": "Maison Louis-Pouliotte, Saint-Laurent — farmhouse of the late 17th century (RPCQ construction date \"avant 1759\"), stone, two straight steep slopes with no overhang, stone laiterie against the east gable; classée 28 November 1973 (RPCQ 92490)", "url": RPCQ.format(92490)}],
  photos=[
    commons("maison-morisset-commons.jpg",
            "Maison Morisset, 4417 chemin Royal, Sainte-Famille — a classed house of this courant",
            "Benoit Rochon", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0",
            "https://commons.wikimedia.org/wiki/File:Maison_Morisset,_Sainte-Famille,_%C3%AEle_d%27Orl%C3%A9ans,_Qu%C3%A9bec.JPG",
            "address"),
    commons("manoir-mauvide-genest-commons.jpg",
            "Manoir Mauvide-Genest, 1451 chemin Royal, Saint-Jean — the seigneurial, hipped-roof end of the courant",
            "Marc-Lautenbacher", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0",
            "https://commons.wikimedia.org/wiki/File:Lieu_historique_national_du_Canada_du_Manoir_Mauvide-Genest,_vue_du_chemin_du_Roy.jpg",
            "address"),
    mrc_photo(27, "six captioned examples, including the type example at 3463 chemin Royal and the hipped variant at 1347 chemin Royal")]),

"maison-traditionnelle-quebecoise": dict(
  phase="p2", name_en="Traditional Québec house of neoclassical influence",
  name_fr="La maison traditionnelle québécoise d'influence néoclassique",
  canonical=["quebec-traditional-1-5st-gable"], styles=["neoclassical-quebec"],
  storeys="1.5–2.5", roof={"form": "gabled", "pitch_deg": 45},
  window_proportion="vertical", principal_cladding=["wood", "brick", "fieldstone-rendered"],
  roofing="traditional tin or cedar shingle", sectors=["UP-1", "UP-2"],
  profile=dict(
    siting_landscape=["\"Très bien représentée à l'île d'Orléans\" — the commonest house of the 19th century here.",
                      "The plan de conservation credits it with shaping the identity of the village sectors, particularly Saint-Laurent and Saint-Jean."],
    massing=["Generally 1½ storeys, sometimes 2½, on a pièce-sur-pièce wood carré — occasionally brick or stone — raised slightly off the ground, which is what produces the gallery and its steps.",
             "Two-slope roof of about 45°, its larmiers incurvés carried well past the front and rear walls to shelter the gallery; where the slopes are straight, an independent lean-to roof (auvent, garde-soleil) does the same job.",
             "A cuisine d'été sometimes extends the house longitudinally or transversally, repeating the main volume at reduced scale."],
    articulation=["Ornament generally sober — chambranles and planches cornières.",
                  "Richer variants take on a more eclectic decor: aisseliers, corniches, balustrades, ornamental woodwork."],
    openings=["Symmetrical façade composition, with many openings.",
              "Double-casement windows with large panes; fronton or gable dormers lighting the attic."],
    materials=["Cladding usually wood — horizontal or vertical boards, or cedar shingle — but sometimes stone or brick masonry.",
               "Chimney stacks generally in line with the gable wall."]),
  blurb_en="The synthesis of French practice and English neoclassicism, and the island's most numerous 19th-century house: a low wooden carré lifted just enough off the ground to need a gallery and steps, under a roof whose eaves curve outward to cover them. The summer kitchen trailing off one end is part of the type, not an afterthought.",
  origin_en="The Conquest of 1760 changed the buildings slowly. Tradesmen stayed and French practice held for decades; English classical architecture arrived early in the 19th century with military engineers, British architects and pattern books, and the two produced what the inventory calls \"une synthèse originale connue sous le nom de maison traditionnelle québécoise\". Its variants run from a bare rural carré to an ornamented village house, according to site and to the owner's standing.",
  photos=[
    commons("7327-chemin-royal-cuisine-ete-commons.jpg",
            "Cuisine d'été at 7327 chemin Royal, Saint-Laurent-de-l'Île-d'Orléans — the summer kitchen the inventory names as part of this type",
            "Thomas1313", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0",
            "https://commons.wikimedia.org/wiki/File:7327,_Chemin_Royal,_Saint-Laurent-de-l%27%C3%8Ele-d%27Orl%C3%A9ans_01.jpg",
            "address"),
    mrc_photo(29, "six captioned examples, including an all-stone variant at 130 chemin Ferland and a 2½-storey stone variant at 1936 chemin Royal")]),

"second-empire-maison-mansardee": dict(
  phase="p3", name_en="Second Empire style and the mansard house",
  name_fr="Le style Second Empire et la maison à mansarde",
  canonical=["mansard-house-2st"], styles=["second-empire"],
  storeys="2", roof={"form": "mansard", "pitch_deg": None},
  window_proportion="vertical", principal_cladding=["wood", "brick", "cut-stone"],
  roofing="traditional tin", sectors=None,
  profile=dict(
    siting_landscape=["\"Ce courant est bien présent à l'île d'Orléans.\"",
                      "A late arrival: Second Empire reaches Québec in the last quarter of the 19th century and only afterwards becomes a village house."],
    massing=["Rectangular two-storey body raised slightly off the ground, on a wood frame.",
             "Broken roof à la Mansart, of two or four slopes, made of brisis and terrassons — the shape that empties the attic and turns it into a fully habitable second storey."],
    articulation=["Ornament generally sober: chambranles, planches cornières and a cornice under the brisis.",
                  "Richer variants take on a more eclectic decor. The inventory's showpiece is the ancien presbytère de Sainte-Famille, brick, \"avec un parement de brique et une ornementation très élaborée\"."],
    openings=["Symmetrical façade composition.",
              "Casement windows with large panes or sash windows, and dormers set in the brisis."],
    materials=["Wood-plank or brick cladding, sometimes cut stone.",
               "Gallery under an independent awning on one or more elevations."]),
  blurb_en="The bourgeois Paris roof, arriving in a Québec village as a way of getting a second full floor. What the inventory calls a \"version populaire et modeste\" of the monumental style keeps only the mansard itself — the shallow terrasson above, the near-vertical brisis below, dormers punched through it — and the silhouette that villagers evidently liked.",
  origin_en="Second Empire architecture takes its source from Paris under Napoléon III (1852–1870) and reaches Québec in the last quarter of the 19th century, at first for institutional buildings and bourgeois houses. The maison à mansarde is its domestic descendant: the roof survives, the avant-corps and the turret mostly do not. On this island it is common enough that the inventory calls the whole courant well represented.",
  photos=[mrc_photo(31, "six captioned examples, including the two-slope type example at 1404 chemin Royal, a four-slope brick house at 1778 chemin Royal and the ancien presbytère de Sainte-Famille")]),

"cottage-regency": dict(
  phase="p3", name_en="Regency cottage", name_fr="Le cottage Regency",
  canonical=["regency-cottage-hipped-veranda"], styles=["regency"],
  storeys="1–2", roof={"form": "hipped", "pitch_deg": None},
  window_proportion="vertical", principal_cladding=["brick", "stone", "wood"],
  roofing="cedar shingle or traditional tin", sectors=["UP-2", "UP-3"],
  profile=dict(
    siting_landscape=["\"Relativement rare dans le site patrimonial de l'Île-d'Orléans et particulièrement présent dans la municipalité de Sainte-Pétronille.\"",
                      "Meant for a large wooded lot: \"le cottage Régence arbore une architecture en communion avec son environnement\"."],
    massing=["Plan tending toward a square; one or two occupied levels.",
             "Low, wide four-slope roof whose eaves are sometimes upturned and are carried out far enough to roof a gallery running right round the house."],
    articulation=["Sober ornament drawn from the classical repertoire — entablements and frontons.",
                  "Trellis gallery supports are frequent."],
    openings=["Symmetrical composition of the openings.",
              "Casement windows with large panes, sometimes as French doors; rampantes, hipped or gable dormers."],
    materials=["Walls of brick, stone or wood.", "Central chimney."]),
  blurb_en="The villégiature house of the British in Québec, and on this island almost entirely a Sainte-Pétronille phenomenon: a squarish block under a low, wide, sometimes upturned hipped roof whose eaves keep going until they have covered a veranda all the way around. French doors open onto it.",
  origin_en="A Regency-period English form — \"apparu en Angleterre sous le règne du Prince de Galles au début du 19e siècle\" — introduced to Québec by the British and taken up by townspeople who wanted a summer house. It belongs to the romantic current, and it is the type most tightly bound to one of the island's five landscape units: the villégiature sector that grew at Sainte-Pétronille after the Québec ferry began running in 1855.",
  photos=[mrc_photo(33, "six captioned examples, all at Sainte-Pétronille except 1585 chemin Royal, Saint-Laurent — including the brick example at 12 chemin de l'Église and a two-storey variant at 12 rue Gagnon")]),

"eclectisme-victorien": dict(
  phase="p3", name_en="Victorian eclecticism", name_fr="L'éclectisme victorien",
  canonical=["queen-anne-irregular-2-5st"], styles=["victorian-eclectic"],
  storeys="2–2.5", roof={"form": "gabled-multi", "pitch_deg": None},
  window_proportion="vertical", principal_cladding=["brick", "stone", "wood"],
  roofing="varied", sectors=None,
  profile=dict(
    siting_landscape=["\"Le site patrimonial de l'Île-d'Orléans comporte peu d'exemples architecturaux issus de l'éclectisme victorien.\"",
                      "What survives is a handful of genuinely eclectic houses plus common types — maison cubique, maison traditionnelle québécoise — carrying a very elaborate Victorian decor."],
    massing=["Asymmetrical plan with no typical plan at all; a very articulated volume with many projections and advances.",
             "Irregular roofs made of gables or turrets, often pierced by dormers."],
    articulation=["Galleries and ornamented covered balconies, often continuing across more than one elevation.",
                  "Varied ornament: neoclassical fronton, ornamental woodwork, mâts, épis, consoles, encorbellements."],
    openings=["No typical opening; several kinds of opening on one building, including bay windows (bow, oriel)."],
    materials=["Several materials and colours combined on a single building — brick, stone, decorative or polychrome shingle."]),
  blurb_en="The one courant on the island defined by refusing a rule. Plan asymmetrical, volume broken into projections, roof irregular and full of gables and turrets, several materials and colours at once, and no typical window. The inventory admits there are very few real examples here — mostly it is ordinary house types wearing an extraordinary decor.",
  origin_en="Québec architecture arrives at eclecticism toward the end of the 19th century, \"un peu en réaction aux compositions rigides du classicisme\", fusing borrowed elements from different periods and countries rather than reproducing any of them. Mechanised construction around 1880 made ornament cheap and fast, which is why façades carry so much of it. The movement runs roughly 1880–1920 in Québec and is called Victorian for Victoria's reign (1837–1901); for this current, \"chaque œuvre est unique en soi\".",
  photos=[mrc_photo(35, "six captioned examples, including a cottage vernaculaire américain with very elaborate wood ornament at 45 chemin du Bout-de-l'Île and a maison cubique with a corner oriel at 20 avenue Orléans")]),

"cottage-vernaculaire-americain": dict(
  phase="p4", name_en="American vernacular cottage", name_fr="Le cottage vernaculaire américain",
  canonical=["industrial-vernacular-cottage"], styles=["vernaculaire-industriel"],
  storeys="1.5–2", roof={"form": "gabled", "pitch_deg": 45},
  window_proportion="vertical", principal_cladding=["wood", "asbestos-cement-shingle", "roughcast"],
  roofing="traditional tin", sectors=None,
  profile=dict(
    siting_landscape=["\"Ce courant est peu représenté dans le site patrimonial, mais il est présent dans la majorité des municipalités en quelques exemplaires.\"",
                      "Elsewhere in Québec it is \"le type le plus varié et le plus courant dans la première moitié du 20e siècle\" — the island is the exception."],
    massing=["Rectangular volume showing a simplification of form.",
             "A 1½-storey plank carré under a straight two-slope roof at 45° or with half-hips; the two-storey low-pitch model is also widespread.",
             "Sub-variants: the cottage with half-hipped roof and the cottage with a gable dormer, otherwise identical."],
    articulation=["Ornament drawn from the 19th-century repertoire but standardised and bought in: chambranles, planches cornières, aisseliers, frontons."],
    openings=["Machined doors and windows — casement with transom, or sash."],
    materials=["Light claddings: wood boards, asbestos-cement shingle, roughcast.",
               "Gallery under an independent awning, often present."]),
  blurb_en="The traditional Québec house rebuilt out of a catalogue. The inventory is precise about the difference: this one rises to 1½ or 2 storeys instead of one and a half, which gives it more verticality, and its two straight slopes at 45° have no curved larmier. The symmetry survives; the carpentry does not.",
  origin_en="American vernacular architecture, the inventory says, is not a style at all — \"elle reprend souvent les formes du siècle précédent en les simplifiant\". What is new is the supply chain: milled beams and boards, doors and windows standardised and sold by catalogue, and the balloon frame (charpente claire) that made building fast and let a standard plan be fitted to a client's means. On this island the courant is thin, but it appears in nearly every municipality.",
  photos=[mrc_photo(37, "six captioned examples, including a large gallery example and a gable-dormer variant, at Saint-Jean, Sainte-Pétronille, Sainte-Famille and Saint-Laurent")]),

"maison-cubique": dict(
  phase="p4", name_en="Cubic house (Four Square)", name_fr="La maison cubique",
  canonical=["foursquare-hipped-2st"], styles=["foursquare"],
  storeys="2", roof={"form": "hipped-or-pyramidal", "pitch_deg": None},
  window_proportion="vertical", principal_cladding=["brick", "wood", "cedar-shingle", "embossed-tin", "asbestos-cement-tile"],
  roofing="traditional tin, sometimes flat", sectors=None,
  profile=dict(
    siting_landscape=["\"La maison cubique est assez peu représentée dans le site patrimonial de l'Île-d'Orléans.\"",
                      "A rural echo of an urban phenomenon: standardisation drove growth in the towns first, \"ce phénomène se répercutera ensuite dans les milieux ruraux\"."],
    massing=["Cubic volume on a square plan of two full storeys, raised slightly off the ground.",
             "Low-pitch pavilion (four-slope) roof, sometimes flat; usually a dormer on the front slope."],
    articulation=["\"Ornementation variable selon le statut social du propriétaire\" — the one type whose decoration the inventory ties explicitly to the owner's standing.",
                  "Picturesque influences show up on some models: aisseliers, ornamental woodwork, cornices."],
    openings=["Regular distribution of openings.",
              "Casement windows with large panes, casement with transom, or sash; hipped, gable, triangular or lean-to dormers, sometimes replaced by gables."],
    materials=["Brick, or light cladding: wood boards, cedar shingle, embossed tin, asbestos-cement tile.",
               "Gallery under an independent awning across the front, sometimes with a balcony above."]),
  blurb_en="Two entire floors under a shallow pavilion roof, on a square plan — a shape whose whole point is interior volume. The inventory says as much: its interest \"réside dans les dimensions de son espace habitable\", giving an ordinary family the room of a bourgeois house. How much ornament it carries depended on who was paying.",
  origin_en="An American model, \"conçu par l'architecte Frank Kidder en 1891\" and commonly called the Four Square house, spread through catalogues and trade journals across North America. It reached Québec's towns on the back of cheap standardised materials and falling construction costs, then reached the countryside. On Île d'Orléans it stayed rare.",
  photos=[mrc_photo(39, "six captioned examples at Saint-Pierre, Saint-François, Saint-Jean and Sainte-Famille, including a brick example at 1634 chemin Royal")]),

"maison-boomtown": dict(
  phase="p4", name_en="Boomtown house", name_fr="La maison Boomtown",
  canonical=["boomtown-false-front"], styles=["boomtown"],
  storeys="2", roof={"form": "flat-or-low-slope", "pitch_deg": None},
  window_proportion="vertical", principal_cladding=["wood", "brick"],
  roofing="flat or low slope to the rear", sectors=None,
  profile=dict(
    siting_landscape=["\"Sur le territoire du site patrimonial de l'Île-d'Orléans, on retrouve quelques exemplaires de maisons Boomtown dans toutes les municipalités.\"",
                      "Both a domestic and a commercial current: \"il n'est pas rare de retrouver un commerce au rez-de-chaussée avec un logement à l'étage\"."],
    massing=["Cubic or rectangular two-storey volume, barely raised off the ground.",
             "Flat roof, or a slight slope draining to the rear."],
    articulation=["Ornament concentrated at the top of the façade: a modillon or console cornice, a stepped parapet, or brick patterning.",
                  "Other ornament stays discreet — chambranles, planches cornières, brick platebandes."],
    openings=["Regular distribution of openings, generally symmetrical.",
              "Casement windows with large panes, casement with transom, or sash."],
    materials=["Wood-plank or brick cladding.",
               "Few projections beyond a gallery under an awning, sometimes with a balcony above on the central third."]),
  blurb_en="A flat-topped two-storey box that spends all its ornament in one place — the top of the front wall, where a bracketed cornice or a stepped parapet makes the building look taller and squarer than it is. Everything below that is plain boards or brick and a gallery.",
  origin_en="The balloon frame, \"qualifiée d'American Boomtown\", arrived with the fast growth of American cities and spread especially after the economic crisis of 1870 as a cheap, quick way to build in boom towns. In Québec it coexists with the traditional and mansard houses before supplanting them at the turn of the 20th century. On this island it never supplanted anything, but there are examples in all six municipalities.",
  photos=[mrc_photo(41, "six captioned examples, including stepped-parapet houses at 504 and 1913 chemin Royal and a shop-house at 148 chemin du Bout-de-l'Île")]),

"arts-and-crafts": dict(
  phase="p4", name_en="Arts and Crafts architecture", name_fr="L'architecture Arts & Crafts",
  canonical=["arts-crafts-articulated-house"], styles=["arts-and-crafts", "arts-et-metiers"],
  storeys="1.5–2.5", roof={"form": "gabled-multi", "pitch_deg": None},
  window_proportion="vertical", principal_cladding=["stone", "brick", "stucco", "cedar-shingle", "wood"],
  roofing="varied", sectors=["UP-2", "UP-3"],
  profile=dict(
    siting_landscape=["\"Il existe peu d'exemples de ce style dans le site patrimonial de l'Île-d'Orléans et ils sont principalement situés à Sainte-Pétronille.\"",
                      "The inventory restricts the current to domestic and villégiature architecture only."],
    massing=["A more or less imposing volume on an articulated plan — simple volumes distributed freely.",
             "Roofs of varied form, with slopes or half-hips sometimes of unequal length, the larmier often projecting well past the façades."],
    articulation=["Ornament often limited to members of the frame: colombage, exposed rafters, gallery supports.",
                  "\"Chaque cas est unique et possède ses propres caractéristiques.\""],
    openings=["Numerous and varied openings, with paired windows and hipped, lean-to or triangular dormers."],
    materials=["Natural and traditional materials — stone, brick, stucco, cedar shingle, wood boards — sometimes combined.",
               "Sheltered outdoor spaces: perrons, galleries, terraces."]),
  blurb_en="A house that breaks into wings and sheltered outdoor rooms under big overhanging roofs, with the structure itself doing the decorating — half-timbering, rafter ends carried out beyond the eaves, worked gallery posts. The inventory declines to generalise further, and says so: every case is its own.",
  origin_en="The English Arts and Crafts movement, rooted in Morris and Ruskin, argued for handwork, traditional materials and local skill against mass production. Crossing to the United States it lost the argument and kept the look: \"en Amérique, le mouvement Arts and Crafts devient essentiellement un mouvement stylistique, sans portée sociale\" — false half-timbering and slate roofs belonging to no local tradition, distributed by catalogue. On this island it is a Sainte-Pétronille resort style, and its best examples are the house and studio of the painter Horatio Walker.",
  related_buildings=[
    {"name": "Maison d'Horatio-Walker, 11 chemin Horatio-Walker, Sainte-Pétronille — \"un bel exemple d'architecture Arts & Crafts\" (inventory caption, p. 43)", "url": None},
    {"name": "Studio d'Horatio-Walker, 13 chemin Horatio-Walker, Sainte-Pétronille — \"représente la version anglaise de l'architecture Arts & Crafts\" (inventory caption, p. 43)", "url": None}],
  photos=[mrc_photo(43, "six captioned examples, all at Sainte-Pétronille, led by the maison and studio d'Horatio-Walker at 11 and 13 chemin Horatio-Walker")]),

"regionalisme-quebecois": dict(
  phase="p5", name_en="Québec regionalism", name_fr="Le régionalisme québécois",
  canonical=["quebec-regionalist-revival-house"], styles=["regionalisme-quebecois"],
  storeys="1.5–2", roof={"form": "gabled", "pitch_deg": None},
  window_proportion="vertical", principal_cladding=["wood", "asbestos-cement", "stone", "stucco"],
  roofing="wood or asphalt shingle", sectors=["UP-2", "UP-3"], period_label="1910–1945",
  profile=dict(
    siting_landscape=["\"On ne retrouve que quelques cas de régionalisme québécois dans l'inventaire, surtout situé à Sainte-Pétronille, car cette architecture s'allie bien à celle de la villégiature.\"",
                      "The inventory warns that these houses are easy to misdate: \"ces maisons peuvent souvent se confondre avec des constructions plus anciennes vue l'intention de les imiter\"."],
    massing=["Rectangular volume, more or less imposing, with annexes.",
             "High pitched roof, its slopes generally straight or slightly upturned, covered in wood or asphalt shingle."],
    articulation=["Ornament often limited to the frames of the openings: chambranles, faux volets.",
                  "Sheltered outdoor spaces — perrons, galleries."],
    openings=["Sash or casement windows with small panes, and generously sized gable dormers."],
    materials=["Wood cladding — shingle or boards — or asbestos-cement.",
               "Chimneys of massive appearance."]),
  blurb_en="A 1930s house built to look like a 1730s one. Québec's own version of Arts and Crafts went back to the buildings of the French regime for its vocabulary — high shingled roof, fire-break gable walls, stone or stucco standing in for lime — and copied them as faithfully as it could. On this island the results sit among the resort houses at Sainte-Pétronille, and the inventory dates the individual examples: 1939, 1940, 1944, 1945.",
  origin_en="\"Le Québec possède une version du courant Arts and Crafts qui lui est propre, soit le régionalisme québécois\", running from 1910 to the end of the Second World War. It began in the research of the McGill architecture professors Percy Erskine Nobbs and Ramsay Traquair, who wanted an authentically regional style, and spread through their students. It fed on the identity politics of the 1920s onward, which glorified New France, and found fertile ground under Duplessis; Gérard Morisset, the abbé Jean-Thomas Nadeau and Marius Barbeau argued for the same rediscovery of tradition.",
  photos=[mrc_photo(45, "six captioned and dated examples — 1939, c. 1940, 1940, 1944 and 1945 — four of them at Sainte-Pétronille")]),

"modernisme": dict(
  phase="p5", name_en="Modernism", name_fr="Le modernisme",
  canonical=[], styles=["international-style"],
  storeys=None, roof={"form": "flat-or-low-slope", "pitch_deg": None},
  window_proportion="horizontal", principal_cladding=["concrete", "steel", "glass"],
  roofing="flat or sculptural", sectors=None, count_in_place=1,
  profile=dict(
    siting_landscape=["\"À l'île d'Orléans, nous n'avons répertorié qu'une résidence issue de l'architecture moderne.\" One house, out of 659.",
                      "The inventory names it: the maison Paul-Brunet, 37 chemin de l'Église, \"témoigne de l'architecture moderne. Son architecture s'inspire notamment d'un paquebot.\""],
    massing=["Simple volume, stripped of ornament.",
             "Free plans producing very varied forms.",
             "Flat roofs, or roofs of sculptural form."],
    articulation=["No applied ornament: \"l'expressivité des matériaux remplace les éléments d'ornementation\"."],
    openings=["Large glazed surfaces, including horizontal ribbon windows."],
    materials=["Modern materials — concrete and steel."]),
  profile_note="The one courant of the eleven with a known population of exactly one. The English columns above are translations of the five bullets on p. 46; there is no five-column table behind them beyond that, and no canonical form on this site fits a single streamline-moderne detached house, so `canonical` is deliberately empty rather than mapped to the postwar slab or tower.",
  blurb_en="The island's single modern house. The courant is a real one — free plan, flat or sculptural roof, concrete and steel, ribbon glazing, no ornament at all because the materials are the ornament — but on Île d'Orléans the inventory found exactly one example of it, and even that one is a ship: the maison Paul-Brunet at 37 chemin de l'Église, modelled on an ocean liner.",
  origin_en="Born of the European modern movement (Art nouveau, the Bauhaus) and American rationalism (the Chicago School), modernism breaks with inherited form more completely than any style before it — practical and functionalist, sober, refusing ornament, and putting aluminium, concrete, steel and large sheets of glass at the front of the design. It divides into several currents more or less faithful to the movement that produced them. Almost none of that reached this island.",
  related_buildings=[
    {"name": "Maison Paul-Brunet, 37 chemin de l'Église — the only modern house in the inventory; the caption on p. 46 gives no municipality, and none is inferred here", "url": None}],
  photos=[mrc_photo(46, "one captioned example, printed inline below the characteristics list: the maison Paul-Brunet at 37 chemin de l'Église")]),
}

STOREY_DEFAULT = "1–2"

# The photo captions print short parish names; place.yaml and the RPCQ use the legal ones.
# example_addresses keep the caption's own wording; the derived municipalities[] index is
# normalised so it joins to place.yaml. "Sainte-Jean" is a typo in the source caption on
# p. 39 for the maison cubique at 3492 chemin Royal — normalised here, flagged on the address.
OFFICIAL = {
    "Sainte-Famille": "Sainte-Famille",
    "Sainte-Pétronille": "Sainte-Pétronille",
    "Saint-Laurent": "Saint-Laurent-de-l'Île-d'Orléans",
    "Saint-Jean": "Saint-Jean-de-l'Île-d'Orléans",
    "Sainte-Jean": "Saint-Jean-de-l'Île-d'Orléans",
    "Saint-François": "Saint-François-de-l'Île-d'Orléans",
    "Saint-Pierre": "Saint-Pierre-de-l'Île-d'Orléans",
}
ADDRESS_NOTES = {
    ("3492 chemin Royal", "Sainte-Jean"): "the caption prints « Sainte-Jean »; the municipality is Saint-Jean-de-l'Île-d'Orléans",
}


def build(slug, parsed_by_slug):
    p = parsed_by_slug[slug]
    e = ENGLISH[slug]
    rec = {
        "id": f"ile-orleans.{slug}",
        "page": p["page"],
        "phase": e["phase"],
        "phase_confidence": "verified",
        "place": "ile-orleans",
        "name_en": e["name_en"], "name_fr": e["name_fr"],
        "source_ref": f"MRC de L'Île-d'Orléans / Patri-Arch, rapport de synthèse, p. {p['page']}",
        "source_generation": SRC_GEN,
        "source_url": INV_URL,
        "courant": "courant architectural (MRC de L'Île-d'Orléans inventory, 11 courants)",
        "sectors": e.get("sectors"),
        "municipalities": sorted({OFFICIAL[a["municipality"]] for a in p["example_addresses"]}) or None,
        "canonical": e["canonical"], "styles": e["styles"],
        "tenure_plan": "single-family",
        "storeys": e.get("storeys", STOREY_DEFAULT),
        "roof": e["roof"],
        "window_proportion": e["window_proportion"],
        "principal_cladding": e["principal_cladding"],
        "roofing": e["roofing"],
        "garage": None,
        "lot_width_m": None, "setback_front_m": None, "setback_side_m": None,
        "front_yard_green_pct": None,
        "count_in_place": e.get("count_in_place"),
        "period_label": e.get("period_label"),
        "profile": e["profile"],
        "profile_fr": {"elements_caracteristiques": p["elements_caracteristiques"]},
        "profile_note": e.get("profile_note"),
        "example_addresses": [dict(a, note=ADDRESS_NOTES.get((a["address"], a["municipality"])))
                              for a in p["example_addresses"]] or None,
        "related_buildings": e.get("related_buildings"),
        "conservation": None,
        "blurb_en": e["blurb_en"], "origin_en": e["origin_en"],
        "photos": e["photos"],
    }
    if p["distribution"]:
        rec["profile_fr"]["repartition"] = [p["distribution"]]
    return rec


HEADER = """# Generated by sources/ile-orleans/emit_types.py from sources/ile-orleans/parsed.json.
# profile_fr is verbatim from the PDF; the English columns are editorial. Re-run
#   python3 sources/ile-orleans/emit_types.py --check
# to confirm the French here still matches the parse.
"""


def main():
    parsed = json.loads(PARSED.read_text(encoding="utf-8"))
    by_slug = {c["slug"]: c for c in parsed["courants"]}
    check = "--check" in sys.argv
    problems = 0
    for slug in ENGLISH:
        rec = build(slug, by_slug)
        path = OUT / f"{slug}.yaml"
        if check:
            if not path.exists():
                print(f"MISSING {path}"); problems += 1; continue
            on_disk = yaml.safe_load(path.read_text(encoding="utf-8"))
            for key in ("elements_caracteristiques", "repartition"):
                want = rec["profile_fr"].get(key)
                got = (on_disk.get("profile_fr") or {}).get(key)
                if want != got:
                    print(f"DRIFT  {slug}.profile_fr.{key}"); problems += 1
            if on_disk.get("example_addresses") != rec["example_addresses"]:
                print(f"DRIFT  {slug}.example_addresses"); problems += 1
        else:
            OUT.mkdir(parents=True, exist_ok=True)
            body = yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, width=100,
                                  default_flow_style=False)
            path.write_text(HEADER + body, encoding="utf-8")
    if check:
        print(f"{'OK' if not problems else 'FAIL'} — {len(ENGLISH)} records, {problems} problem(s)")
        sys.exit(1 if problems else 0)
    print(f"wrote {len(ENGLISH)} type records to {OUT}")


if __name__ == "__main__":
    main()
