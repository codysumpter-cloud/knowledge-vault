#!/usr/bin/env python3
"""Public-safety checks for KnowledgeVault.

Hard-fails on tracked forbidden paths and unsafe automation staging. The check is
path-based on purpose: historical reference notes need separate human review.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_PREFIXES = (
    "00-Private/",
    "99-System/Security/",
    "99-System/Logs/",
    "99-System/Backups/",
    "99-System/Prompts/",
    "99-System/Templates/",
)
FORBIDDEN_NAME_PARTS = (
    ".env",
    "private-key",
    "private_key",
)
AUTOMATION_FILES = (
    ".github/workflows/vault-steward-daily.yml",
    "99-System/Automation/run-vault-maintenance.sh",
    "99-System/Automation/run-vault-steward-mac-safe.sh",
)


def run_git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout


def tracked_files() -> list[str]:
    return [line for line in run_git(["ls-files"]).splitlines() if line]


def check_tracked_paths(files: list[str]) -> list[str]:
    errors: list[str] = []
    for rel in files:
        if rel.startswith(FORBIDDEN_PREFIXES):
            errors.append(f"tracked forbidden path: {rel}")
        lowered = rel.lower()
        if any(part in lowered for part in FORBIDDEN_NAME_PARTS):
            errors.append(f"tracked sensitive-looking filename: {rel}")
    return errors


def check_automation() -> list[str]:
    errors: list[str] = []
    for rel in AUTOMATION_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"git\s+add\s+\.\b", text):
            errors.append(f"broad git add command in {rel}")
        for prefix in FORBIDDEN_PREFIXES:
            display = prefix.rstrip("/")
            if display in text:
                errors.append(f"automation references forbidden staged path {display} in {rel}")
    return errors


def main() -> int:
    os.chdir(ROOT)
    files = tracked_files()
    errors: list[str] = []
    errors.extend(check_tracked_paths(files))
    errors.extend(check_automation())

    if errors:
        print("Vault Doctor failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Vault Doctor passed: {len(files)} tracked files checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
