#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate a KBE JSON report's status and evidence fields. Read-only.

Usage: python3 report_validate.py <report.json>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

STATUSES = {"PASS", "FAIL", "NOT_RUN", "BLOCKED", "NEEDS_REVIEW"}
METRIC_REQUIRED = ("name", "status", "timestamp", "scope", "method")


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level must be an object"]
    for key in ("status", "timestamp", "scope", "metrics"):
        if key not in data:
            errors.append(f"missing top-level field: {key}")
    status = data.get("status")
    if status not in STATUSES:
        errors.append(f"invalid top-level status: {status!r}")
    metrics = data.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        errors.append("metrics must be a non-empty list")
        return errors
    for i, m in enumerate(metrics):
        if not isinstance(m, dict):
            errors.append(f"metric[{i}] must be an object")
            continue
        for key in METRIC_REQUIRED:
            if key not in m or m[key] in (None, ""):
                errors.append(f"metric[{i}] missing {key}")
        if m.get("status") not in STATUSES:
            errors.append(f"metric[{i}] invalid status: {m.get('status')!r}")
        if m.get("status") == "PASS" and not all(m.get(k) for k in ("timestamp", "scope", "method")):
            errors.append(f"metric[{i}] PASS without timestamp/scope/method")
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(json.dumps({"ok": False, "errors": [f"cannot parse JSON: {e}"]}, ensure_ascii=False, indent=2))
        return 1
    errors = validate(data)
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
