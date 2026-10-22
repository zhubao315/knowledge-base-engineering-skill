#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detect whether the agent is running in a sandbox with a shared vault.

This script is read-only. It never creates, moves or deletes anything.

Usage:
    python3 detect_environment.py [--sandbox-root PATH] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_SANDBOX = os.environ.get("KBE_SANDBOX_ROOT") or "/app/.hermes/obsidian"


def detect(sandbox_root: str | Path = DEFAULT_SANDBOX) -> dict:
    p = Path(sandbox_root).expanduser().resolve()
    exists = p.exists()
    is_dir = p.is_dir()
    readable = bool(exists and is_dir and os.access(p, os.R_OK))
    reachable = bool(readable)
    environment = "sandbox" if reachable else "local"
    if environment == "sandbox":
        recommended_profile = "ulife"
        modes = ["mirror", "local"]
        guidance = (
            "检测到沙箱共享库可达。可先生成镜像/同步计划；"
            "实际双向同步必须交给外部同步工具并由人批准，本 Skill 不自动执行。"
        )
    else:
        recommended_profile = "para"
        modes = ["local"]
        guidance = (
            "未检测到沙箱共享库，按本地独立库处理。"
            "不要向用户展示 /app/.hermes/obsidian 作为默认路径；"
            "让用户指定一个本地可达目录，或提供可读的本地导入源。"
        )
    return {
        "sandbox_root": str(p),
        "exists": exists,
        "is_dir": is_dir,
        "readable": readable,
        "reachable": reachable,
        "environment": environment,
        "recommended_modes": modes,
        "recommended_profile": recommended_profile,
        "profiles": ["para", "minimal", "ulife"],
        "guidance": guidance,
        "mode": "read_only",
        "status": "PASS",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect sandbox shared-vault availability.")
    ap.add_argument("--sandbox-root", default=DEFAULT_SANDBOX)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    data = detect(args.sandbox_root)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"environment: {data['environment']}")
        if data['environment'] == 'sandbox':
            print(f"sandbox root: {data['sandbox_root']} (reachable=True)")
        else:
            print("sandbox root: unavailable; using the local branch")
        print(f"recommended profile: {data['recommended_profile']}")
        print(f"modes: {', '.join(data['recommended_modes'])}")
        print(data["guidance"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
