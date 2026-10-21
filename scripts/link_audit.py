#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit wikilinks, broken targets and orphans. Read-only.

Orphan = no inbound links (the book's definition). It does not mean "no
outbound links". Composition/exemptions must be reported by a human.

Usage: python3 link_audit.py <root> [--json]
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from common import iter_markdown, read_text, rel, target_names, wikilinks, dump_json


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    names = target_names(root)
    files = list(iter_markdown(root))
    inbound = Counter()
    broken = []
    outbound = {}
    for p in files:
        r = rel(root, p)
        links = []
        for raw in wikilinks(read_text(p)):
            t = raw.strip()
            if t.endswith(".md"):
                t = t[:-3]
            links.append(t)
            if t in names:
                if names[t] != r:
                    inbound[names[t]] += 1
            else:
                broken.append({"file": r, "target": t})
        outbound[r] = len(links)
    orphans = []
    for p in files:
        r = rel(root, p)
        if inbound.get(r, 0) == 0:
            orphans.append(r)
    data = {
        "root": str(root),
        "total_markdown": len(files),
        "total_links": sum(outbound.values()),
        "broken_links": broken,
        "broken_count": len(broken),
        "orphans": sorted(orphans),
        "orphan_count": len(orphans),
        "inbound": dict(sorted(inbound.items())),
        "outbound": dict(sorted(outbound.items())),
        "status": "FAIL" if broken else "PASS",
        "mode": "read_only",
        "note": "orphans are raw; classify diary/archive/uWise/publishing/unknown before acting.",
    }
    if "--json" in sys.argv:
        dump_json(data)
    else:
        print(f"links: {data['total_links']} · broken: {data['broken_count']} · orphans: {data['orphan_count']}")
        for b in broken:
            print(f"  broken: {b['file']} -> {b['target']}")
    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
