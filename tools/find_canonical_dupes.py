#!/usr/bin/env python3
"""Flag canonical forms that may be the same object recorded twice (Part 12 §2.1).

For every pair of canonical ids, compare the physical fingerprint of their member
records — roof.form, storeys, tenure_plan, principal_cladding — and print the pairs
agreeing on three of the four. This is a shortlist for a human to read, not a merge
tool: two genuinely distinct forms often share a fingerprint (a mansard duplex and a
mansard rowhouse agree on everything but attachment), so false positives are
expected and §2.1 says explicitly not to auto-merge.

Groups and aliases are skipped: a group is *meant* to resemble its children, and an
alias is already a declared duplicate.

Usage:
    python3 tools/find_canonical_dupes.py
"""
import collections
import glob
import itertools

import yaml

FIELDS = ["roof_form", "storeys", "tenure_plan", "principal_cladding"]


def hashable(v):
    """storeys and principal_cladding are lists on records whose source gives a
    range or several materials; make them comparable without losing the ordering."""
    return tuple(v) if isinstance(v, list) else v


def mode(values):
    """The most common non-null value, or None. Canonicals with mixed members get
    their dominant value, which is what makes the comparison meaningful at all."""
    vals = [hashable(v) for v in values if v not in (None, "", [])]
    return collections.Counter(vals).most_common(1)[0][0] if vals else None


def main():
    canon = yaml.safe_load(open("data/canon/canonical_types.yaml", encoding="utf-8"))
    meta = {c["id"]: c for c in canon}
    skip = {c["id"] for c in canon if c.get("is_group") or c.get("alias_of")}
    skip |= {ch for c in canon for ch in (c.get("children") or [])}

    members = collections.defaultdict(list)
    for path in sorted(glob.glob("data/places/*/types/*.yaml")) + sorted(glob.glob("data/shared_types/*.yaml")):
        t = yaml.safe_load(open(path, encoding="utf-8")) or {}
        fp = {"roof_form": (t.get("roof") or {}).get("form"),
              "storeys": t.get("storeys"),
              "tenure_plan": t.get("tenure_plan"),
              "principal_cladding": t.get("principal_cladding")}
        for cid in (t.get("canonical") or []):
            members[cid].append(fp)

    prints = {}
    for cid, fps in members.items():
        if cid in skip or len(fps) < 1:
            continue
        prints[cid] = {f: mode([fp[f] for fp in fps]) for f in FIELDS}

    hits = []
    for a, b in itertools.combinations(sorted(prints), 2):
        agree = [f for f in FIELDS if prints[a][f] is not None and prints[a][f] == prints[b][f]]
        if len(agree) >= 3:
            hits.append((len(agree), a, b, agree))

    print(f"{len(prints)} canonical forms fingerprinted "
          f"({len(skip)} groups/aliases/children skipped)\n")
    if not hits:
        print("No pair agrees on three of four. Nothing to review.")
        return
    print(f"{len(hits)} pair(s) agree on 3+ of {FIELDS} — REVIEW BY HAND, do not auto-merge:\n")
    for n, a, b, agree in sorted(hits, reverse=True):
        print(f"  [{n}/4] {a}  ({len(members[a])} members)")
        print(f"        {b}  ({len(members[b])} members)")
        print(f"        agree on: {', '.join(agree)}")
        print(f"        {meta[a]['name_en'][:74]}")
        print(f"        {meta[b]['name_en'][:74]}\n")


if __name__ == "__main__":
    main()
