#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit frontmatter and H1 structure. Read-only.

Usage: python3 metadata_audit.py <root> [--json]
"""
from __future__ import annotations

import sys
from pathlib import Path

from common import h1_count, iter_markdown, parse_frontmatter, read_text, rel, dump_json

REQUIRED = ("title", "created", "tags")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    files = list(iter_markdown(root))
    missing_fm, missing_fields, h1_missing, h1_multi = [], {}, [], []
    for key in REQUIRED:
        missing_fields[key] = []
    for p in files:
        r = rel(root, p)
        text = read_text(p)
        fm = parse_frontmatter(text)
        if fm is None:
            missing_fm.append(r)
        else:
            for key in REQUIRED:
                val = fm.get(key)
                if val is None or (isinstance(val, str) and not val.strip()) or (isinstance(val, list) and not val):
                    missing_fields[key].append(r)
        n = h1_count(text)
        if n == 0:
            h1_missing.append(r)
        elif n > 1:
            h1_multi.append(r)
    fail = bool(missing_fm or any(missing_fields.values()) or h1_missing or h1_multi)
    data = {
        "root": str(root),
        "total_markdown": len(files),
        "missing_frontmatter": missing_fm,
        "missing_fields": missing_fields,
        "h1_missing": h1_missing,
        "h1_multiple": h1_multi,
        "status": "FAIL" if fail else "PASS",
        "mode": "read_only",
    }
    if "--json" in sys.argv:
        dump_json(data)
    else:
        print(f"markdown: {len(files)} · status: {data['status']}")
        print(f"missing frontmatter: {len(missing_fm)}")
        for k, v in missing_fields.items():
            print(f"missing {k}: {len(v)}")
        print(f"missing H1: {len(h1_missing)} · multiple H1: {len(h1_multi)}")
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
