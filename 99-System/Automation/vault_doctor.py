#!/usr/bin/env python3
"""Public-safety checks for KnowledgeVault.

The doctor is intentionally conservative. It checks tracked files and automation
scripts for path-safety problems before a public vault update is published.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".sh",
    ".js",
    ".mjs",
    ".ts",
    ".tsx",
    ".html",
    ".css",
}
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
    "credential",
    "credentials",
)
SENSITIVE_CONTENT_HINTS = (
    re.compile(r"(?i)(secret|password|credential)\s*[:=]\s*\S{8,}"),
    re.compile(r"(?i)(access|refresh)[_-]?(key|value)\s*[:=]\s*\S{8,}"),
    re.compile(r"(?i)authorization\s*[:=]\s*\S+"),
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


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def check_tracked_paths(files: list[str]) -> list[str]:
    errors: list[str] = []
    for rel in files:
        if rel.startswith(FORBIDDEN_PREFIXES):
            errors.append(f"tracked forbidden path: {rel}")
        lowered = rel.lower()
        if any(part in lowered for part in FORBIDDEN_NAME_PARTS):
            errors.append(f"tracked sensitive-looking filename: {rel}")
    return errors


def check_text_content(files: list[str]) -> list[str]:
    errors: list[str] = []
    for rel in files:
        path = ROOT / rel
        if not path.exists() or not is_text_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            errors.append(f"could not read {rel}: {exc}")
            continue
        for pattern in SENSITIVE_CONTENT_HINTS:
            if pattern.search(text):
                errors.append(f"sensitive-looking content hint in {rel}")
                break
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
    errors: list[str] = []
    files = tracked_files()
    errors.extend(check_tracked_paths(files))
    errors.extend(check_text_content(files))
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
