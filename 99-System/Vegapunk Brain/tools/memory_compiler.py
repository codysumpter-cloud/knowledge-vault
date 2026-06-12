#!/usr/bin/env python3
"""Compile markdown/session memory into Vegapunk Brain graph JSONL records.

This is intentionally deterministic and dependency-free. It does not pretend to
be a full NER system; it extracts useful repo/system/concept/task/decision/person
signals from notes, summaries, decision logs, PR summaries, and docs.

Usage:
    python "99-System/Vegapunk Brain/tools/memory_compiler.py" \
      --source "docs/session.md" \
      --out "99-System/Vegapunk Brain/graph/generated.graph.jsonl"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

KNOWN_REPOS = {
    "knowledge-vault": "repo:knowledge-vault",
    "buddy-agent": "repo:buddy-agent",
    "buddy-brain": "repo:buddy-brain",
    "omni-buddy": "repo:omni-buddy",
    "prismtek-apps": "repo:prismtek-apps",
}

KNOWN_SYSTEMS = {
    "council": "system:council",
    "codex tasks": "system:codex-tasks",
    "codex-tasks": "system:codex-tasks",
    "agent browser": "system:agent-browser",
    "agent-browser": "system:agent-browser",
    "knowledge graph": "system:knowledge-graph",
    "shared memory bus": "system:shared-memory-bus",
    "memory compiler": "system:memory-compiler",
}

CONCEPT_HINTS = {
    "knowledge vault": "concept:knowledge-vault",
    "shared memory": "concept:shared-memory",
    "shared brain": "concept:shared-brain",
    "semantic graph": "concept:semantic-graph",
    "memory bus": "concept:memory-bus",
    "graph records": "concept:graph-records",
    "source of truth": "concept:source-of-truth",
    "future sessions": "concept:future-sessions",
}

RELATIONSHIP_HINTS = {
    "feeds": "feeds",
    "consume": "consumes",
    "consumes": "consumes",
    "depends on": "depends_on",
    "dependency": "depends_on",
    "owns": "owns",
    "owner": "owns",
    "implements": "implements",
    "implemented": "implements",
    "supersedes": "supersedes",
    "replaces": "supersedes",
    "related": "related_to",
    "uses": "uses",
    "integrates": "integrates_with",
    "sync": "syncs_with",
}

STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "that", "this", "your", "current", "state",
    "input", "output", "support", "define", "create", "build", "phase", "goal", "requirements",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("_", "-")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unnamed"


def titleize(value: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_\s]+", value.strip()) if part)


def now_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def stable_suffix(text: str, length: int = 10) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:length]


def record(record_id: str, record_type: str, name: str, summary: str, tags: list[str], source: str, confidence: str = "medium") -> dict[str, Any]:
    ts = now_ts()
    return {
        "id": record_id,
        "type": record_type,
        "name": name,
        "summary": summary,
        "tags": sorted(set(tags)),
        "links": [],
        "provenance": {"source": source, "confidence": confidence, "created": ts, "updated": ts},
        "freshness": {"status": "current", "updated": ts[:10]},
    }


def add_link(records: dict[str, dict[str, Any]], src: str, predicate: str, dst: str, reason: str) -> None:
    if src not in records or dst not in records or src == dst:
        return
    link = {"type": predicate, "target": dst, "reason": reason}
    if link not in records[src]["links"]:
        records[src]["links"].append(link)


def lines(text: str) -> Iterable[str]:
    for line in text.splitlines():
        clean = line.strip(" \t-*#>`")
        if clean:
            yield clean


def extract_known_entities(text: str, source: str, records: dict[str, dict[str, Any]]) -> None:
    lowered = text.lower()
    for key, entity_id in {**KNOWN_REPOS, **KNOWN_SYSTEMS, **CONCEPT_HINTS}.items():
        if key in lowered:
            entity_type = entity_id.split(":", 1)[0]
            records.setdefault(
                entity_id,
                record(
                    entity_id,
                    entity_type,
                    titleize(entity_id.split(":", 1)[1]),
                    f"Detected reference to {titleize(key)} in compiled memory.",
                    [entity_type, "compiled", "vegapunk-brain"],
                    source,
                    "high" if entity_id in KNOWN_REPOS.values() or entity_id in KNOWN_SYSTEMS.values() else "medium",
                ),
            )


def extract_tasks_and_decisions(text: str, source: str, records: dict[str, dict[str, Any]]) -> None:
    for line in lines(text):
        lower = line.lower()
        is_task = lower.startswith(("todo", "task", "next", "fix", "build", "create", "add", "implement")) or "must " in lower or "should " in lower
        is_decision = lower.startswith(("decision", "decided", "choose", "chosen")) or "source of truth" in lower or "do not" in lower
        if is_task:
            name = line[:96]
            rid = f"task:{slugify(name)[:64]}-{stable_suffix(line)}"
            records.setdefault(rid, record(rid, "task", name, f"Compiled task from source: {line[:180]}", ["task", "compiled"], source, "medium"))
        if is_decision:
            name = line[:96]
            rid = f"decision:{slugify(name)[:64]}-{stable_suffix(line)}"
            records.setdefault(rid, record(rid, "decision", name, f"Compiled decision from source: {line[:180]}", ["decision", "compiled"], source, "medium"))


def extract_people(text: str, source: str, records: dict[str, dict[str, Any]]) -> None:
    for match in re.finditer(r"\b(?:Prismtek|Cody|Buddy|Hermes|BMO|Finn|Jake|Marceline|Princess Bubblegum|Peppermint Butler|Prismo|NEPTR|Simon)\b", text):
        name = match.group(0)
        rid = f"person:{slugify(name)}"
        records.setdefault(rid, record(rid, "person", name, f"Person or named agent reference detected: {name}.", ["person", "agent-reference", "compiled"], source, "medium"))


def extract_candidate_concepts(text: str, source: str, records: dict[str, dict[str, Any]]) -> None:
    headings = re.findall(r"^#{1,4}\s+(.+)$", text, flags=re.MULTILINE)
    bullets = [line.strip(" -*") for line in text.splitlines() if line.strip().startswith(("-", "*"))]
    candidates = headings + bullets
    for raw in candidates:
        phrase = re.sub(r"[`*_\[\]()]", "", raw).strip()
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z0-9-]+", phrase) if w.lower() not in STOPWORDS]
        if not 1 <= len(words) <= 5:
            continue
        name = " ".join(words)[:80]
        if len(name) < 4:
            continue
        rid = f"concept:{slugify(name)}"
        records.setdefault(rid, record(rid, "concept", name, f"Compiled concept candidate from markdown heading or bullet: {name}.", ["concept", "compiled"], source, "low"))


def infer_relationships(text: str, records: dict[str, dict[str, Any]]) -> None:
    lowered = text.lower()
    ids = list(records)
    for src in ids:
        src_name = records[src]["name"].lower()
        for dst in ids:
            if src == dst:
                continue
            dst_name = records[dst]["name"].lower()
            window_patterns = [
                f"{src_name} feeds {dst_name}",
                f"{src_name} consumes {dst_name}",
                f"{src_name} uses {dst_name}",
                f"{src_name} implements {dst_name}",
                f"{src_name} depends on {dst_name}",
            ]
            for pattern in window_patterns:
                if pattern in lowered:
                    predicate = next((rel for hint, rel in RELATIONSHIP_HINTS.items() if hint in pattern), "related_to")
                    add_link(records, src, predicate, dst, f"Relationship inferred from source text phrase: {pattern}")
    if "concept:knowledge-vault" in records:
        for entity_id in ids:
            if entity_id != "concept:knowledge-vault" and entity_id.startswith(("repo:", "system:")):
                add_link(records, "concept:knowledge-vault", "related_to", entity_id, "Compiled source mentions this node near KnowledgeVault shared memory context.")


def compile_text(text: str, source: str) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    extract_known_entities(text, source, records)
    extract_tasks_and_decisions(text, source, records)
    extract_people(text, source, records)
    extract_candidate_concepts(text, source, records)
    infer_relationships(text, records)
    return [records[key] for key in sorted(records)]


def read_sources(paths: list[Path]) -> list[tuple[str, str]]:
    output = []
    for path in paths:
        if path.is_dir():
            for child in sorted(path.rglob("*.md")):
                output.append((str(child), child.read_text(encoding="utf-8")))
        else:
            output.append((str(path), path.read_text(encoding="utf-8")))
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile notes into Vegapunk Brain graph JSONL records.")
    parser.add_argument("--source", nargs="+", required=True, help="Markdown file or directory to compile.")
    parser.add_argument("--out", required=True, help="Output graph JSONL path.")
    parser.add_argument("--append", action="store_true", help="Append instead of replacing output.")
    args = parser.parse_args()

    compiled: dict[str, dict[str, Any]] = {}
    for source_name, text in read_sources([Path(item) for item in args.source]):
        for rec in compile_text(text, source_name):
            compiled.setdefault(rec["id"], rec)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if args.append else "w"
    with out.open(mode, encoding="utf-8") as handle:
        for rec in compiled.values():
            handle.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

    print(f"Compiled {len(compiled)} graph records into {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
