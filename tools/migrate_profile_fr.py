#!/usr/bin/env python3
"""Collapse the many `profile_fr` shapes into the Part 12 §1.2 two-field shape.

Eleven parts each mirrored the sub-headings of their own source document, which was
right per part and wrong overall: 32 distinct shapes across 17 sub-keys are in the
tree. This rewrites every one of them to

    profile_fr:
      source_headings: [Volumétrie, Ouvertures, ...]     # verbatim, in source order
      blocks:
        - {heading: Volumétrie, bullets: [...], maps_to: massing}

Two deliberate departures from the brief's sketch, both in its own spirit:

  * blocks carry `bullets` (a list) rather than `text` (a string). Every source in
    this project itemises: the Gatineau fiches, the Lévis catalogue and the RPCQ
    éléments caractéristiques are all bullet lists, and they render as <li>.
    Flattening them into one string would erase the source's own itemisation,
    which is the kind of evidence §1.2 says must not be normalised away.
  * `heading` is reconstructed with the source's own accented word — Revêtement for
    Gatineau, Revêtements for Lévis, Volumes for Saint-Lambert, Volumétrie for the
    rest. The keys were slugified on the way in; the headings are the evidence.

Usage:
    python3 tools/migrate_profile_fr.py            # dry run: report only, writes nothing
    python3 tools/migrate_profile_fr.py --write    # rewrite the files
"""
import collections
import glob
import sys

import yaml

# The source's own heading for each slugified key. Singular/plural and
# volumes/volumétrie differences are real differences between documents.
HEADINGS = {
    "implantation": "Implantation",
    "repartition": "Répartition géographique",
    "volumetrie": "Volumétrie",
    "volumes": "Volumes",
    "saillies": "Saillies",
    "plan": "Plan",
    "toiture": "Toiture",
    "traitement_des_facades": "Traitement des façades",
    "ornementation": "Ornementation",
    "ouvertures": "Ouvertures",
    "materiaux": "Matériaux",
    "revetement": "Revêtement",
    "revetements": "Revêtements",
    "description": "Description",
    "contexte": "Contexte",
    "elements_caracteristiques": "Éléments caractéristiques",
    "sous_variantes": "Sous-variantes",
}

# Which of the five profile columns each heading answers to. None means the source
# heading has no column equivalent and renders as its own row.
MAPS_TO = {
    "implantation": "siting_landscape",
    "repartition": "siting_landscape",
    "volumetrie": "massing",
    "volumes": "massing",
    "saillies": "massing",
    "plan": "massing",
    "toiture": "massing",
    "traitement_des_facades": "articulation",
    "ornementation": "articulation",
    "ouvertures": "openings",
    "materiaux": "materials",
    "revetement": "materials",
    "revetements": "materials",
    "description": None,
    "contexte": None,
    "elements_caracteristiques": None,
    "sous_variantes": None,
}


def files():
    return sorted(glob.glob("data/places/*/types/*.yaml")) + sorted(glob.glob("data/shared_types/*.yaml"))


def main():
    write = "--write" in sys.argv
    seen = collections.Counter()
    unknown = collections.defaultdict(list)
    already = touched = 0

    for path in files():
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        doc = yaml.safe_load(raw) or {}
        pfr = doc.get("profile_fr")
        if not pfr:
            continue
        if isinstance(pfr, dict) and "blocks" in pfr:
            already += 1
            continue

        blocks = []
        # yaml.safe_load preserves mapping order, so this is the source's own order.
        for key, val in pfr.items():
            if key not in HEADINGS:
                unknown[key].append(path)
                continue
            seen[key] += 1
            bullets = val if isinstance(val, list) else [val]
            blocks.append({"heading": HEADINGS[key],
                           "bullets": [str(b) for b in bullets],
                           "maps_to": MAPS_TO[key]})
        if not blocks:
            continue
        doc["profile_fr"] = {"source_headings": [b["heading"] for b in blocks],
                             "blocks": blocks}
        touched += 1
        if write:
            with open(path, "w", encoding="utf-8") as fh:
                yaml.safe_dump(doc, fh, allow_unicode=True, sort_keys=False, width=100)

    print(f"{'REWROTE' if write else 'WOULD REWRITE'} {touched} record(s); "
          f"{already} already migrated")
    print("\nHEADING TABLE — eyeball this vocabulary before committing:")
    print(f"  {'key':26s} {'heading':26s} {'maps_to':18s} count")
    for key, n in sorted(seen.items(), key=lambda kv: -kv[1]):
        print(f"  {key:26s} {HEADINGS[key]:26s} {str(MAPS_TO[key]):18s} {n}")
    if unknown:
        print("\nUNKNOWN KEYS — migration refuses to guess at these:")
        for key, paths in sorted(unknown.items()):
            print(f"  {key}: {len(paths)} file(s), e.g. {paths[0]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
