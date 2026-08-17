#!/usr/bin/env python3
"""Split the overloaded sector `value` field into `rank` and `kind` (Part 12 §1.3).

`value` carried two orthogonal things at once: how good a sector is, and what kind
of object it is. `exceptional` and `interesting` are ranks; `declared-site`,
`unite-de-paysage` and `parcel-system` are kinds. A field that answers two
questions cannot be filtered on either.

    rank: exceptional | interesting | none
    kind: declared-site | cited-site | evaluation-sector | unite-de-paysage |
          parcel-system | urban-ensemble | industrial | archaeological | review-jurisdiction

Also renames `code_eval2005` to `code_alt`, which absorbs Part 5's second Westmount
code and Part 11's second Montréal code under one name.

One judgement worth stating, because it is the only place the mapping is not
mechanical. The Ville de Montréal Évaluation grades sectors A (valeur
exceptionnelle) and B (valeur intéressante), and separately lists C, "ensembles
urbains d'intérêt". C uses the same word as B — d'intérêt — but it is a different
category in the source's own scheme, describing what a thing is rather than where
it sits on the A/B scale. §1.3 says never infer a rank, so urban-ensemble takes
`rank: none`. Nothing is lost: the interest is carried by the kind's own name.

Usage:
    python3 tools/migrate_sectors.py            # dry run
    python3 tools/migrate_sectors.py --write
"""
import collections
import glob
import sys

import yaml

# value -> (rank, kind)
SPLIT = {
    "exceptional":              ("exceptional",  "evaluation-sector"),
    "interesting":              ("interesting",  "evaluation-sector"),
    "urban-ensemble":           ("none",         "urban-ensemble"),
    "declared-site":            ("none",         "declared-site"),
    "cited-site":               ("none",         "cited-site"),
    "unite-de-paysage":         ("none",         "unite-de-paysage"),
    "parcel-system":            ("none",         "parcel-system"),
    "archaeological-potential": ("none",         "archaeological"),
    "review-jurisdiction":      ("none",         "review-jurisdiction"),
}

# The unified sector record, in render order.
ORDER = ["id", "code", "code_alt", "name_fr", "name_en", "rank", "kind", "summary_en",
         "summary_fr", "characteristics_fr", "streets", "source", "plan_de_conservation",
         "note", "promoted_to_place"]


def main():
    write = "--write" in sys.argv
    tally = collections.Counter()
    unknown = collections.defaultdict(list)
    touched = already = 0

    for path in sorted(glob.glob("data/places/*/sectors.yaml")):
        secs = yaml.safe_load(open(path, encoding="utf-8")) or []
        changed = False
        for s in secs:
            if "rank" in s and "kind" in s:
                already += 1
                continue
            val = s.pop("value", None)
            if val not in SPLIT:
                unknown[val].append(path)
                continue
            s["rank"], s["kind"] = SPLIT[val]
            if "code_eval2005" in s:
                s["code_alt"] = s.pop("code_eval2005")
            tally[val] += 1
            changed = True
        if not changed:
            continue
        touched += 1
        if write:
            ordered = [{k: s[k] for k in ORDER if k in s} | {k: v for k, v in s.items() if k not in ORDER}
                       for s in secs]
            with open(path, "w", encoding="utf-8") as fh:
                yaml.safe_dump(ordered, fh, allow_unicode=True, sort_keys=False, width=100)

    print(f"{'REWROTE' if write else 'WOULD REWRITE'} {touched} file(s); {already} sector(s) already split")
    print(f"\n  {'value':26s} {'rank':13s} {'kind':22s} count")
    for val, n in tally.most_common():
        r, k = SPLIT[val]
        print(f"  {val:26s} {r:13s} {k:22s} {n}")
    if unknown:
        print("\nUNKNOWN VALUES — migration refuses to guess:")
        for val, paths in unknown.items():
            print(f"  {val!r}: {len(paths)} file(s), e.g. {paths[0]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
