#!/usr/bin/env python3
"""Lint Vegapunk Brain JSONL graph files.

Usage:
    python "99-System/Vegapunk Brain/tools/graph_linter.py" \
      "99-System/Vegapunk Brain/graph/seed.graph.jsonl"

The linter intentionally avoids third-party dependencies so it can run in a
fresh clone with only Python 3.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ID_RE = re.compile(r"^(concept|repo|system):[a-z0-9][a-z0-9._:-]*$")
VALID_TYPES = {"concept", "repo", "system"}
VALID_CONFIDENCE = {"low", "medium", "high"}
VALID_FRESHNESS = {"current", "stale", "unknown"}
REQUIRED_FIELDS = {
    "id",
    "type",
    "name",
    "summary",
    "tags",
    "links",
    "provenance",
    "freshness",
}


def fail(errors: list[str], path: Path, line_no: int, message: str) -> None:
    errors.append(f"{path}:{line_no}: {message}")


def require_string(errors: list[str], path: Path, line_no: int, record: dict[str, Any], key: str) -> None:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(errors, path, line_no, f"{key!r} must be a non-empty string")


def lint_record(
    record: Any,
    *,
    path: Path,
    line_no: int,
    ids: set[str],
    link_targets: list[tuple[Path, int, str]],
    errors: list[str],
) -> None:
    if not isinstance(record, dict):
        fail(errors, path, line_no, "record must be a JSON object")
        return

    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        fail(errors, path, line_no, f"missing required fields: {', '.join(missing)}")

    extra = sorted(set(record) - REQUIRED_FIELDS)
    if extra:
        fail(errors, path, line_no, f"unknown fields: {', '.join(extra)}")

    record_id = record.get("id")
    if not isinstance(record_id, str) or not ID_RE.match(record_id):
        fail(errors, path, line_no, "'id' must match concept|repo|system namespaced format")
    elif record_id in ids:
        fail(errors, path, line_no, f"duplicate id: {record_id}")
    else:
        ids.add(record_id)

    record_type = record.get("type")
    if record_type not in VALID_TYPES:
        fail(errors, path, line_no, f"'type' must be one of: {', '.join(sorted(VALID_TYPES))}")

    if isinstance(record_id, str) and isinstance(record_type, str):
        prefix = record_id.split(":", 1)[0]
        if prefix != record_type:
            fail(errors, path, line_no, f"id prefix {prefix!r} must match type {record_type!r}")

    require_string(errors, path, line_no, record, "name")
    require_string(errors, path, line_no, record, "summary")

    tags = record.get("tags")
    if not isinstance(tags, list) or not tags:
        fail(errors, path, line_no, "'tags' must be a non-empty list")
    elif any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        fail(errors, path, line_no, "all tags must be non-empty strings")
    elif len(tags) != len(set(tags)):
        fail(errors, path, line_no, "tags must be unique")

    links = record.get("links")
    if not isinstance(links, list):
        fail(errors, path, line_no, "'links' must be a list")
    else:
        for index, link in enumerate(links):
            if not isinstance(link, dict):
                fail(errors, path, line_no, f"links[{index}] must be an object")
                continue
            for key in ("type", "target", "reason"):
                if not isinstance(link.get(key), str) or not link.get(key, "").strip():
                    fail(errors, path, line_no, f"links[{index}].{key} must be a non-empty string")
            target = link.get("target")
            if isinstance(target, str):
                if not ID_RE.match(target):
                    fail(errors, path, line_no, f"links[{index}].target has invalid id format: {target}")
                else:
                    link_targets.append((path, line_no, target))

    provenance = record.get("provenance")
    if not isinstance(provenance, dict):
        fail(errors, path, line_no, "'provenance' must be an object")
    else:
        if not isinstance(provenance.get("source"), str) or not provenance.get("source", "").strip():
            fail(errors, path, line_no, "provenance.source must be a non-empty string")
        if provenance.get("confidence") not in VALID_CONFIDENCE:
            fail(errors, path, line_no, "provenance.confidence must be low, medium, or high")

    freshness = record.get("freshness")
    if not isinstance(freshness, dict):
        fail(errors, path, line_no, "'freshness' must be an object")
    else:
        if freshness.get("status") not in VALID_FRESHNESS:
            fail(errors, path, line_no, "freshness.status must be current, stale, or unknown")
        updated = freshness.get("updated")
        if not isinstance(updated, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", updated):
            fail(errors, path, line_no, "freshness.updated must use YYYY-MM-DD")


def lint_path(path: Path, ids: set[str], link_targets: list[tuple[Path, int, str]], errors: list[str]) -> int:
    count = 0
    if not path.exists():
        errors.append(f"{path}: file does not exist")
        return count

    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(errors, path, line_no, f"invalid JSON: {exc}")
                continue
            lint_record(
                record,
                path=path,
                line_no=line_no,
                ids=ids,
                link_targets=link_targets,
                errors=errors,
            )
    return count


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: graph_linter.py <graph.jsonl> [more.graph.jsonl ...]", file=sys.stderr)
        return 2

    ids: set[str] = set()
    link_targets: list[tuple[Path, int, str]] = []
    errors: list[str] = []
    total = 0

    for arg in argv[1:]:
        total += lint_path(Path(arg), ids, link_targets, errors)

    for path, line_no, target in link_targets:
        if target not in ids:
            fail(errors, path, line_no, f"link target does not exist in loaded graph set: {target}")

    if errors:
        print("Vegapunk Brain graph lint failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Vegapunk Brain graph lint passed: {total} records, {len(ids)} ids")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
