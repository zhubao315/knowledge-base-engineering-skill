#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for the KBE skill.

Uses only the standard library. The fixture vault contains known anomalies:
- missing frontmatter
- missing title
- broken wikilink
- raw orphans
- placeholder / empty heading
- a prompt-injection note (must be treated as data, never executed)
- excluded archive/attachments

The tests also assert that no fixture file is created, deleted or modified.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VAULT = HERE / "fixtures" / "vault"
SCRIPTS = ROOT / "scripts"
REPORTS = HERE / "fixtures" / "reports"

passed = 0
failed = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global passed, failed
    if cond:
        passed += 1
        print(f"PASS  {name}")
    else:
        failed += 1
        print(f"FAIL  {name}  {detail}")


def run_json(script: str, root: Path) -> tuple[int, dict]:
    p = subprocess.run(
        [sys.executable, str(SCRIPTS / script), str(root), "--json"],
        capture_output=True, text=True,
    )
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError:
        data = {}
    return p.returncode, data


def snapshot() -> dict[str, str]:
    out = {}
    for p in sorted(VAULT.rglob("*")):
        if p.is_file():
            out[p.relative_to(VAULT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def main() -> int:
    before = snapshot()

    code, inv = run_json("inventory.py", VAULT)
    check("inventory exit", code in (0, 1), str(code))
    check("inventory total 9 (excludes archive/attachments)", inv.get("total_markdown") == 9, str(inv.get("total_markdown")))
    check("inventory is read-only", inv.get("mode") == "read_only")

    code, meta = run_json("metadata_audit.py", VAULT)
    check("metadata detects missing frontmatter", len(meta.get("missing_frontmatter", [])) == 1, str(meta.get("missing_frontmatter")))
    check("metadata detects missing title", len(meta.get("missing_fields", {}).get("title", [])) == 1)
    check("metadata status FAIL", meta.get("status") == "FAIL")

    code, links = run_json("link_audit.py", VAULT)
    broken = links.get("broken_links", [])
    check("link audit finds one broken target", len(broken) == 1 and broken[0].get("target") == "missing-target", str(broken))
    check("link audit finds orphan-note", "orphan-note.md" in links.get("orphans", []))
    check("link audit is read-only", links.get("mode") == "read_only")

    code, ph = run_json("placeholder_audit.py", VAULT)
    check("placeholder audit finds 待补充", ph.get("placeholder_count") == 1, str(ph.get("placeholder_count")))
    check("placeholder audit finds empty heading", ph.get("empty_heading_count") == 1, str(ph.get("empty_heading_count")))

    v = subprocess.run([sys.executable, str(SCRIPTS / "report_validate.py"), str(REPORTS / "valid.json")], capture_output=True, text=True)
    check("valid report passes", v.returncode == 0, v.stdout + v.stderr)
    iv = subprocess.run([sys.executable, str(SCRIPTS / "report_validate.py"), str(REPORTS / "invalid.json")], capture_output=True, text=True)
    check("invalid report fails", iv.returncode == 1, iv.stdout + iv.stderr)

    policy = (ROOT / "config" / "policy.yaml").read_text(encoding="utf-8")
    check("policy forbids physical delete", "physical_delete: false" in policy)
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    check("skill states no physical delete", "物理删除" in skill and "永远" in skill)
    check("skill has five statuses", all(s in skill for s in ("PASS", "FAIL", "NOT_RUN", "BLOCKED", "NEEDS_REVIEW")))

    with tempfile.TemporaryDirectory() as td:
        # Environment detection: local (default) vs sandbox (explicit readable dir)
        local = subprocess.run(
            [sys.executable, str(SCRIPTS / "detect_environment.py"),
             "--sandbox-root", str(Path(td) / "missing"), "--json"],
            capture_output=True, text=True,
        )
        ld = json.loads(local.stdout)
        check("detect local environment", local.returncode == 0 and ld.get("environment") == "local" and ld.get("recommended_profile") == "para")

        shared = Path(td) / "shared"
        shared.mkdir()
        sandbox = subprocess.run(
            [sys.executable, str(SCRIPTS / "detect_environment.py"),
             "--sandbox-root", str(shared), "--json"],
            capture_output=True, text=True,
        )
        sd = json.loads(sandbox.stdout)
        check("detect sandbox environment", sandbox.returncode == 0 and sd.get("environment") == "sandbox" and sd.get("recommended_profile") == "ulife")

        local_target = Path(td) / "local-auto"
        p = subprocess.run(
            [sys.executable, str(SCRIPTS / "scaffold_obsidian.py"),
             "--target", str(local_target), "--sandbox-root", str(Path(td) / "missing"),
             "--execute", "--json"],
            capture_output=True, text=True,
        )
        check("auto local chooses PARA", p.returncode == 0 and (local_target / "01-Projects").is_dir() and (local_target / "04-Archives").is_dir(), p.stdout + p.stderr)

        sandbox_target = Path(td) / "sandbox-auto"
        p = subprocess.run(
            [sys.executable, str(SCRIPTS / "scaffold_obsidian.py"),
             "--target", str(sandbox_target), "--sandbox-root", str(shared),
             "--execute", "--json"],
            capture_output=True, text=True,
        )
        check("auto sandbox chooses uLife", p.returncode == 0 and (sandbox_target / "01-BRAIN" / "11-概念").is_dir(), p.stdout + p.stderr)

    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / "dry-vault"
        p = subprocess.run([sys.executable, str(SCRIPTS / "scaffold_obsidian.py"), "--target", str(target), "--profile", "minimal", "--json"], capture_output=True, text=True)
        check("scaffold dry-run makes no directory", p.returncode == 0 and not target.exists(), p.stdout + p.stderr)

        target2 = Path(td) / "new-vault"
        p = subprocess.run([sys.executable, str(SCRIPTS / "scaffold_obsidian.py"), "--target", str(target2), "--profile", "minimal", "--execute", "--json"], capture_output=True, text=True)
        check("scaffold execute creates starter vault", p.returncode == 0 and (target2 / "00-META" / "Home.md").is_file() and (target2 / "00-META" / "scaffold-manifest.json").is_file(), p.stdout + p.stderr)

        nonempty = Path(td) / "nonempty"
        nonempty.mkdir()
        (nonempty / "keep.md").write_text("keep", encoding="utf-8")
        p = subprocess.run([sys.executable, str(SCRIPTS / "scaffold_obsidian.py"), "--target", str(nonempty), "--execute", "--json"], capture_output=True, text=True)
        check("scaffold refuses non-empty target", p.returncode == 2 and (nonempty / "keep.md").read_text(encoding="utf-8") == "keep" and not (nonempty / "00-META").exists(), p.stdout + p.stderr)

        target3 = Path(td) / "ulife-vault"
        p = subprocess.run([sys.executable, str(SCRIPTS / "scaffold_obsidian.py"), "--target", str(target3), "--profile", "ulife", "--execute", "--json"], capture_output=True, text=True)
        check("scaffold ulife profile creates 01-BRAIN layers", p.returncode == 0 and (target3 / "01-BRAIN" / "11-概念").is_dir() and (target3 / "02-BUILD" / "22-uSkill").is_dir(), p.stdout + p.stderr)

    after = snapshot()
    check("no fixture file changed (read-only)", before == after)

    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
