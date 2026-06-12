#!/usr/bin/env python3
"""Produce a Vegapunk Brain graph health report."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from event_common import write_json


def load_graph(path: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            rid = record["id"]
            if rid in records:
                raise SystemExit(f"Duplicate id {rid} at {path}:{line_no}")
            records[rid] = record
    return records


def days_old(date_text: str) -> int | None:
    try:
        dt = datetime.strptime(date_text, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return (datetime.now(timezone.utc) - dt).days


def health(records: dict[str, dict[str, Any]], stale_days: int) -> dict[str, Any]:
    ids = set(records)
    inbound: dict[str, int] = defaultdict(int)
    report: dict[str, Any] = {
        "summary": {"record_count": len(records), "ok": True},
        "orphaned_nodes": [],
        "stale_records": [],
        "duplicate_concepts": [],
        "missing_provenance": [],
        "broken_relationships": [],
        "invalid_freshness": [],
    }

    concept_names: dict[str, list[str]] = defaultdict(list)
    for rid, record in records.items():
        if record.get("type") == "concept":
            concept_names[record.get("name", "").strip().lower()].append(rid)
        provenance = record.get("provenance", {})
        if not provenance.get("source") or not provenance.get("confidence"):
            report["missing_provenance"].append(rid)
        freshness = record.get("freshness", {})
        updated = freshness.get("updated")
        age = days_old(updated) if isinstance(updated, str) else None
        if age is None:
            report["invalid_freshness"].append(rid)
        elif age > stale_days:
            report["stale_records"].append({"id": rid, "updated": updated, "days_old": age})
        for link in record.get("links", []):
            target = link.get("target")
            if target not in ids:
                report["broken_relationships"].append({"source": rid, "target": target, "type": link.get("type")})
            else:
                inbound[target] += 1

    for rid, record in records.items():
        if not record.get("links") and inbound.get(rid, 0) == 0:
            report["orphaned_nodes"].append(rid)
    for name, matches in concept_names.items():
        if name and len(matches) > 1:
            report["duplicate_concepts"].append({"name": name, "ids": sorted(matches)})

    hard_fail_keys = ["missing_provenance", "broken_relationships", "invalid_freshness", "duplicate_concepts"]
    report["summary"]["ok"] = not any(report[key] for key in hard_fail_keys)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Vegapunk Brain graph health.")
    parser.add_argument("--graph", required=True, help="Graph JSONL file.")
    parser.add_argument("--out", required=True, help="health-report.json path.")
    parser.add_argument("--stale-days", type=int, default=120, help="Days before a current record is reported stale.")
    args = parser.parse_args()
    report = health(load_graph(Path(args.graph)), args.stale_days)
    write_json(Path(args.out), report)
    print(f"Graph health ok={report['summary']['ok']} records={report['summary']['record_count']}")
    return 0 if report["summary"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
