#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan placeholder / content-debt markers. Read-only.

This is a heuristic. It excludes fenced and inline code so examples in
templates are not counted as content debt.

Usage: python3 placeholder_audit.py <root> [--json]
"""
from __future__ import annotations

import sys
from pathlib import Path

from common import EMPTY_HEADING_RE, PLACEHOLDER_RE, body_without_fm, iter_markdown, prose_without_code, read_text, rel, dump_json


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    hits = []
    empty_headings = []
    for p in iter_markdown(root):
        r = rel(root, p)
        text = read_text(p)
        body = body_without_fm(text)
        prose = prose_without_code(body)
        for m in PLACEHOLDER_RE.finditer(prose):
            hits.append({"file": r, "marker": m.group(1), "offset": m.start()})
        for m in EMPTY_HEADING_RE.finditer(prose):
            empty_headings.append({"file": r, "offset": m.start()})
    data = {
        "root": str(root),
        "placeholder_hits": hits,
        "placeholder_count": len(hits),
        "empty_headings": empty_headings,
        "empty_heading_count": len(empty_headings),
        "status": "FAIL" if hits or empty_headings else "PASS",
        "mode": "read_only",
        "note": "human must split blocker vs content debt before acting.",
    }
    if "--json" in sys.argv:
        dump_json(data)
    else:
        print(f"placeholders: {len(hits)} · empty headings: {len(empty_headings)}")
        for h in hits:
            print(f"  {h['file']}: {h['marker']}")
    return 0 if not (hits or empty_headings) else 1


if __name__ == "__main__":
    sys.exit(main())
