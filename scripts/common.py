#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for the Knowledge Base Engineering skill.

Stdlib only. These helpers are intentionally conservative: they never write
to the knowledge base and they never follow symlinks.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

EXCLUDE_DIRS = {
    ".git", ".obsidian", ".runtime", ".venv", "node_modules",
    "attachments", "archive", ".stfolder", "__pycache__",
}

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
H1_RE = re.compile(r"(?m)^#\s+(.+?)\s*$")
FENCED_RE = re.compile(r"(?ms)^\s*```.*?^\s*```\s*$")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
PLACEHOLDER_RE = re.compile(r"(待补充|待填写|TODO|FIXME|此处待|XX提示)")
EMPTY_HEADING_RE = re.compile(r"(?m)^#{1,6}\s*$")


def iter_markdown(root: Path) -> Iterable[Path]:
    """Yield .md files, pruning excluded dirs and skipping symlinks."""
    root = root.expanduser().resolve()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                p = Path(dirpath) / name
                if p.is_symlink():
                    continue
                yield p


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> Optional[Dict[str, object]]:
    """Parse a small, safe subset of YAML frontmatter.

    Supports scalar values and simple block lists. Returns None when there is
    no frontmatter. This is deliberately not a full YAML parser.
    """
    m = FM_RE.match(text)
    if not m:
        return None
    fm: Dict[str, object] = {}
    current: Optional[str] = None
    for raw in m.group(1).splitlines():
        line = raw.rstrip()
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("- ") and current:
            val = s[2:].strip().strip('"').strip("'")
            existing = fm.get(current)
            if isinstance(existing, list):
                existing.append(val)
            else:
                fm[current] = [val]
            continue
        if ":" in s:
            key, _, val = s.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            current = key
            if not val:
                fm[key] = []
            elif val.startswith("[") and val.endswith("]"):
                fm[key] = [x.strip().strip('"').strip("'") for x in val[1:-1].split(",") if x.strip()]
            else:
                fm[key] = val
    return fm


def body_without_fm(text: str) -> str:
    m = FM_RE.match(text)
    return text[m.end():] if m else text


def prose_without_code(text: str) -> str:
    text = FENCED_RE.sub("", text)
    return INLINE_CODE_RE.sub("", text)


def wikilinks(text: str) -> List[str]:
    """Return link targets from prose, excluding fenced and inline code."""
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(prose_without_code(text))]


def h1_count(text: str) -> int:
    return len(H1_RE.findall(prose_without_code(body_without_fm(text))))


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def target_names(root: Path) -> Dict[str, str]:
    """Build target name -> relative path. Includes stems and aliases."""
    names: Dict[str, str] = {}
    for p in iter_markdown(root):
        r = rel(root, p)
        stem = p.stem
        names[stem] = r
        names[r[:-3]] = r
        fm = parse_frontmatter(read_text(p))
        if fm:
            aliases = fm.get("aliases")
            if isinstance(aliases, list):
                for a in aliases:
                    if isinstance(a, str) and a.strip():
                        names[a.strip()] = r
    return names


def dump_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
