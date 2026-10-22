#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safely scaffold a new Obsidian/Markdown vault.

This is provisioning, not governance. It is intentionally conservative:

- dry-run by default; writes only with --execute
- target must be absent or an empty directory
- never deletes, moves or overwrites anything
- only creates paths from a fixed allowlist profile
- writes a manifest for rollback/audit

Usage:
    python3 scaffold_obsidian.py --detect [--json]
    python3 scaffold_obsidian.py --target <new-or-empty-dir> [--profile auto|minimal|para|ulife]
    python3 scaffold_obsidian.py --target <dir> --execute
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from detect_environment import DEFAULT_SANDBOX, detect

PROFILES = {
    "minimal": {
        "dirs": [
            "00-META",
            "01-BRAIN",
            "02-BUILD",
            "07-SOURCES",
            "09-REFERENCE",
            "99-归档",
        ],
        "files": {
            "00-META/Home.md": "# Home\n\n新库入口。先跑一次只读体检，再决定第一周只做什么。\n",
            "01-BRAIN/∑ 知识索引.md": "# ∑ 知识索引\n\n只放已经能回答“它在哪一层、和谁有关”的笔记。\n",
        },
    },
    "para": {
        "dirs": [
            "00-Inbox",
            "01-Projects",
            "02-Areas",
            "03-Resources",
            "04-Archives",
        ],
        "files": {
            "00-Inbox/README.md": "# Inbox\n\n先收集，再在每周复盘时把内容放进 Projects / Areas / Resources / Archives。\n",
            "01-Projects/README.md": "# Projects\n\n有明确终点和交付物的项目。\n",
            "02-Areas/README.md": "# Areas\n\n需要长期维护的责任领域。\n",
            "03-Resources/README.md": "# Resources\n\n可复用的资料、主题与参考。\n",
            "04-Archives/README.md": "# Archives\n\n已完成或不再活跃的内容。\n",
        },
    },
    "ulife": {
        "dirs": [
            "00-META",
            "01-BRAIN",
            "01-BRAIN/11-概念",
            "01-BRAIN/12-模型",
            "01-BRAIN/13-框架",
            "01-BRAIN/14-原则",
            "01-BRAIN/15-洞察",
            "02-BUILD",
            "02-BUILD/22-uSkill",
            "02-BUILD/28-创作",
            "07-SOURCES",
            "07-SOURCES/74-影音",
            "09-REFERENCE",
            "09-REFERENCE/93-脚本",
            "99-归档",
        ],
        "files": {
            "00-META/Home.md": "# Home\n\nuLife 风格入口：先定义问题，再决定收什么。\n",
            "01-BRAIN/∑ 知识索引.md": "# ∑ 知识索引\n\n01-BRAIN 只收可复用的概念、模型、框架、原则与洞察。\n",
            "01-BRAIN/11-概念/∑ 概念索引.md": "# ∑ 概念索引\n\n概念层：说清“是什么、不是什么、与谁相邻”。\n",
            "02-BUILD/22-uSkill/∑ 技能索引.md": "# ∑ 技能索引\n\n技能层：触发、步骤、验收、回滚、升级五段。\n",
        },
    },
}


def planned_files(profile: str) -> dict[str, str]:
    return PROFILES[profile]["files"]


def main() -> int:
    ap = argparse.ArgumentParser(description="Safely scaffold a new Obsidian/Markdown vault.")
    ap.add_argument("--target", help="new or empty directory")
    ap.add_argument("--profile", choices=["auto"] + sorted(PROFILES), default="auto")
    ap.add_argument("--sandbox-root", default=DEFAULT_SANDBOX,
                    help="shared sandbox vault path to probe (default: /app/.hermes/obsidian)")
    ap.add_argument("--detect", action="store_true", help="only detect environment and exit")
    ap.add_argument("--execute", action="store_true", help="actually create; default is dry-run")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    detected = detect(args.sandbox_root)
    if args.detect or not args.target:
        if args.json:
            print(json.dumps(detected, ensure_ascii=False, indent=2))
        else:
            print(f"environment: {detected['environment']}")
            print(f"recommended profile: {detected['recommended_profile']}")
            print(f"modes: {', '.join(detected['recommended_modes'])}")
            print(detected['guidance'])
            if not args.target and not args.detect:
                print("\n缺少 --target。请指定一个本地目录；例如：")
                print("  python3 scripts/scaffold_obsidian.py --target ~/notes --profile para")
        return 0 if args.detect else 2

    target = Path(args.target).expanduser().resolve()
    profile = args.profile
    if profile == "auto":
        profile = detected["recommended_profile"]
    dirs = [target / d for d in PROFILES[profile]["dirs"]]
    files = {target / rel: content for rel, content in planned_files(profile).items()}

    # Preflight: target must be absent or empty; no existing path may be overwritten.
    blocked = []
    if target.exists():
        if not target.is_dir():
            blocked.append(f"target exists and is not a directory: {target}")
        else:
            try:
                if any(target.iterdir()):
                    blocked.append(f"target is not empty: {target}")
            except OSError as e:
                blocked.append(f"cannot read target: {e}")
    for p in dirs + list(files):
        if p.exists():
            blocked.append(f"path already exists: {p}")

    result = {
        "profile": profile,
        "environment": detected["environment"],
        "target": str(target),
        "mode": "execute" if args.execute else "dry_run",
        "dirs": [str(p) for p in dirs],
        "files": [str(p) for p in files],
        "created": [],
        "blocked": blocked,
        "policy": {
            "physical_delete": False,
            "overwrite": False,
            "move": False,
            "only_empty_target": True,
        },
        "status": "BLOCKED" if blocked else ("PASS" if args.execute else "NEEDS_REVIEW"),
    }

    if blocked:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("BLOCKED")
            for b in blocked:
                print(" -", b)
        return 2

    if not args.execute:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("DRY RUN — nothing will be written")
            print(f"environment: {detected['environment']} · profile: {profile}")
            print(f"target: {target}")
            print(f"dirs: {len(dirs)} · files: {len(files)}")
        return 0

    # Execute: only after preflight; no overwrite, no delete.
    created = []
    target.mkdir(parents=True, exist_ok=True)
    for p in dirs:
        p.mkdir(parents=True, exist_ok=True)
        created.append(str(p))
    for p, content in files.items():
        if p.exists():
            # Defensive: should have been blocked above.
            raise RuntimeError(f"refusing to overwrite: {p}")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        created.append(str(p))
    manifest = {
        "profile": profile,
        "target": str(target),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dirs": [str(p) for p in dirs],
        "files": [str(p) for p in files],
        "policy": result["policy"],
        "created": created,
    }
    manifest_dir = target / "00-META"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "scaffold-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    result["created"] = created
    result["manifest"] = str(manifest_dir / "scaffold-manifest.json")
    result["status"] = "PASS"
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PASS — created {len(dirs)} dirs + {len(files)} files")
        print(f"manifest: {result['manifest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
