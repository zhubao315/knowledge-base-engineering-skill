#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventory a Markdown knowledge base without modifying it.

Usage: python3 inventory.py <root> [--json]
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from common import iter_markdown, rel, read_text, dump_json


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    files = list(iter_markdown(root))
    by_dir = Counter()
    for p in files:
        r = rel(root, p)
        by_dir[r.split("/")[0] if "/" in r else "."] += 1
    data = {
        "root": str(root),
        "total_markdown": len(files),
        "by_top_dir": dict(sorted(by_dir.items())),
        "files": [rel(root, p) for p in files],
        "mode": "read_only",
        "status": "PASS",
    }
    if "--json" in sys.argv:
        dump_json(data)
    else:
        print(f"root: {root}")
        print(f"markdown: {len(files)}")
        for k, v in sorted(by_dir.items()):
            print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
