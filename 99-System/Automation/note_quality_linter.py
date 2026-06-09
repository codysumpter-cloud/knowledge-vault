#!/usr/bin/env python3
"""Lightweight KnowledgeVault note quality linter.

This checks public markdown notes for agent-readiness signals:
- title
- metadata front matter on important docs
- purpose/current/source/next-action style sections
- generated section markers when generated content appears

It is intentionally lightweight and dependency-free. It does not replace human review
or vault_doctor.py. Use --strict when you want warnings to fail CI.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]

EXCLUDED_PARTS = {
    ".git",
    ".obsidian",
    "00-Private",
    "99-System/Security",
    "99-System/Logs",
    "99-System/Backups",
    ".data",
}

CRITICAL_FILES = {
    "README.md",
    "AGENTS.md",
    "SYSTEMMAP.md",
    "RUNBOOK.md",
    "SECURITY.md",
    "BACKLOG.md",
    "AGENT_DATABASE_BLUEPRINT.md",
    "99-System/Standards/NOTE_FORMAT_STANDARD.md",
}

REQUIRED_METADATA = {
    "type",
    "status",
    "owner",
    "source_of_truth",
    "last_verified",
    "risk_level",
    "privacy",
}

SECTION_HINTS = {
    "purpose": re.compile(r"^##\s+Purpose\b", re.IGNORECASE | re.MULTILINE),
    "current": re.compile(r"^##\s+(Current state|Current known state|Status)\b", re.IGNORECASE | re.MULTILINE),
    "sources": re.compile(r"^##\s+(Source links|Links|Sources|References)\b", re.IGNORECASE | re.MULTILINE),
    "next": re.compile(r"^##\s+(Next action|Next actions|Tasks)\b", re.IGNORECASE | re.MULTILINE),
}


@dataclass
class Finding:
    path: str
    severity: str
    code: str
    message: str


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_excluded(path: Path) -> bool:
    relative = rel(path)
    parts = set(path.relative_to(ROOT).parts)
    if parts & EXCLUDED_PARTS:
        return True
    return any(relative.startswith(prefix + "/") for prefix in EXCLUDED_PARTS if "/" in prefix)


def iter_markdown_files() -> Iterable[Path]:
    for path in ROOT.rglob("*.md"):
        if not is_excluded(path):
            yield path


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end]
    metadata: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith("  ") or line.lstrip().startswith("-"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"')
    return metadata


def has_title(text: str) -> bool:
    return bool(re.search(r"^#\s+\S", text, re.MULTILINE))


def has_summary(text: str) -> bool:
    if re.search(r"^>\s+\S", text, re.MULTILINE):
        return True
    first_body_lines = [line.strip() for line in text.splitlines()[:12] if line.strip()]
    return any(line and not line.startswith(("#", "---", "type:", "status:", "owner:")) for line in first_body_lines)


def should_require_metadata(path: Path) -> bool:
    relative = rel(path)
    return (
        relative in CRITICAL_FILES
        or relative.startswith("30 - Projects/GitHub/")
        or relative.startswith("99-System/Agent Skills/")
        or relative.startswith("99-System/Agents/")
        or relative.startswith("99-System/Context Bundles/")
        or relative.startswith("99-System/Standards/")
    )


def lint_file(path: Path) -> list[Finding]:
    relative = rel(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: list[Finding] = []

    if not has_title(text):
        findings.append(Finding(relative, "error", "missing-title", "Missing top-level # title."))

    if not has_summary(text):
        findings.append(Finding(relative, "warning", "missing-summary", "Missing short opening summary or blockquote."))

    metadata = parse_front_matter(text)
    if should_require_metadata(path):
        missing = sorted(REQUIRED_METADATA - set(metadata))
        if missing:
            findings.append(
                Finding(
                    relative,
                    "warning",
                    "missing-metadata",
                    "Missing recommended front matter keys: " + ", ".join(missing),
                )
            )

    if relative.endswith(("Project.md", "Agent Context.md", "Decisions.md", "Tasks.md")):
        for key, pattern in SECTION_HINTS.items():
            if key in {"purpose", "next"} and not pattern.search(text):
                findings.append(Finding(relative, "warning", f"missing-{key}-section", f"Missing recommended {key} section."))

    if "generated" in text.lower() and "BEGIN GENERATED" not in text and "END GENERATED" not in text:
        findings.append(
            Finding(
                relative,
                "info",
                "generated-marker-check",
                "Generated content is mentioned; confirm generated sections use explicit markers where automation owns content.",
            )
        )

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint KnowledgeVault markdown notes for agent-readiness.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    parser.add_argument("paths", nargs="*", help="Optional specific paths to check.")
    args = parser.parse_args(argv)

    if args.paths:
        files = [ROOT / path for path in args.paths]
    else:
        files = list(iter_markdown_files())

    findings: list[Finding] = []
    for path in files:
        if path.exists() and path.suffix == ".md" and not is_excluded(path):
            findings.extend(lint_file(path))

    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2, ensure_ascii=False))
    else:
        if not findings:
            print("note_quality_linter: no findings")
        for item in findings:
            print(f"{item.severity.upper()} {item.path}: {item.code}: {item.message}")

    has_error = any(item.severity == "error" for item in findings)
    has_warning = any(item.severity == "warning" for item in findings)
    if has_error or (args.strict and has_warning):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
