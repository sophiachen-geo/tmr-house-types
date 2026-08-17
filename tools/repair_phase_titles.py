#!/usr/bin/env python3
"""Repair phase titles truncated by YAML flow-style parsing.

Every part's brief wrote phases.yaml in flow style:

    - {id: p5, label: 2002-2026, ..., title_en: Merger, demerger, and inventory, colour_key: p5}

In a YAML flow mapping the commas inside the title are separators, so this parses
as title_en: "Merger" plus two extra keys, "demerger" and "and inventory", each
with a null value. The title is silently truncated at its first comma and the
build never complains, because the keys it requires are all present.

This was live from Part 1 and hit 18 places. The repair is exact: YAML split the
title on ", ", so rejoining title_en with the null-valued keys that follow it, in
order, reconstructs the original string character for character.

Files are rewritten in block style with the title quoted, so it cannot recur.

Usage:
    python3 tools/repair_phase_titles.py            # dry run
    python3 tools/repair_phase_titles.py --write
"""
import glob
import sys

import yaml

# Keys the phase schema actually defines. Anything else carrying a null value is
# a fragment of the string that preceded it.
SCHEMA = {"id", "label", "start", "end", "title_en", "colour_key", "summary_en",
          "note", "confidence"}
ORDER = ["id", "label", "start", "end", "title_en", "summary_en", "colour_key", "note"]


def main():
    write = "--write" in sys.argv
    repaired = files = 0

    for path in sorted(glob.glob("data/places/*/phases.yaml")):
        phases = yaml.safe_load(open(path, encoding="utf-8")) or []
        touched = False
        for ph in phases:
            keys = list(ph)
            if "title_en" not in keys:
                continue
            # fragments are the null-valued non-schema keys following title_en
            after = keys[keys.index("title_en") + 1:]
            frags = [k for k in after if ph[k] is None and k not in SCHEMA]
            if not frags:
                continue
            print(f"{path}  {ph['id']}")
            print(f"    was: {ph['title_en']!r}")
            ph["title_en"] = ", ".join([ph["title_en"]] + frags)
            for k in frags:
                del ph[k]
            print(f"    now: {ph['title_en']!r}")
            repaired += 1
            touched = True
        if not touched:
            continue
        files += 1
        if write:
            ordered = [{k: ph[k] for k in ORDER if k in ph}
                       | {k: v for k, v in ph.items() if k not in ORDER}
                       for ph in phases]
            with open(path, "w", encoding="utf-8") as fh:
                yaml.safe_dump(ordered, fh, allow_unicode=True, sort_keys=False, width=100)

    print(f"\n{'REPAIRED' if write else 'WOULD REPAIR'} {repaired} phase title(s) in {files} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
