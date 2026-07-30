#!/usr/bin/env python3
"""Compile Vegapunk Brain events into schema-compatible graph records."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any
from event_common import load_json_events, slugify, validate_event, write_jsonl

SOURCE_TO_REPO = {
    "buddy-agent": "repo:buddy-agent",
    "buddy-brain": "repo:buddy-brain",
    "omni-buddy": "repo:omni-buddy",
    "prismtek-apps": "repo:prismtek-apps",
    "knowledge-vault": "concept:knowledge-vault",
}

EVENT_TO_RECORD_TYPE = {
    "concept_created": "concept",
    "concept_updated": "concept",
    "task_created": "task",
    "task_completed": "task",
    "decision_made": "decision",
    "policy_updated": "decision",
    "council_update": "system",
    "feature_added": "system",
    "feature_removed": "system",
    "repo_created": "repo",
    "repo_updated": "repo",
    "memory_created": "concept",
    "memory_updated": "concept",
    "relationship_created": "concept",
    "relationship_removed": "concept",
    "conversation_summarized": "concept",
    "device_registered": "system",
    "model_changed": "system",
    "local_memory_created": "concept",
    "app_created": "repo",
    "release_created": "system",
    "agent_life_updated": "concept",
}


def graph_id(record_type: str, event: dict[str, Any]) -> str:
    payload = event.get("payload", {})
    explicit = payload.get("id")
    if isinstance(explicit, str) and explicit.startswith(f"{record_type}:"):
        return explicit
    if record_type == "repo" and payload.get("repo"):
        return f"repo:{slugify(str(payload['repo']))}"
    name = payload.get("name") or payload.get("title") or event["event_id"]
    return f"{record_type}:{slugify(str(name))}"


def record_from_event(event: dict[str, Any]) -> dict[str, Any]:
    errors = validate_event(event)
    if errors:
        raise ValueError(f"Invalid event {event.get('event_id')}: {errors}")
    payload = event.get("payload", {})
    event_type = event["event_type"]
    record_type = EVENT_TO_RECORD_TYPE[event_type]
    name = str(payload.get("name") or payload.get("title") or event_type.replace("_", " ").title())
    summary = str(payload.get("summary") or payload.get("body") or f"Compiled from {event_type} event {event['event_id']}.")
    tags = sorted(set([record_type, event_type, event["source"], "event-sourced"] + list(payload.get("tags", []))))
    links: list[dict[str, str]] = []

    producer = SOURCE_TO_REPO.get(event["source"])
    if producer:
        links.append({"type": "emitted_by", "target": producer, "reason": f"Compiled from {event['source']} event."})

    repo = payload.get("repo")
    if isinstance(repo, str):
        links.append({"type": "related_to", "target": f"repo:{slugify(repo)}", "reason": "Event payload identifies this repo."})

    target = payload.get("target")
    if isinstance(target, str) and ":" in target:
        links.append({"type": "related_to", "target": target, "reason": "Event payload identifies this graph target."})

    if event_type == "agent_life_updated":
        agent_id = payload.get("agent_id")
        if isinstance(agent_id, str) and agent_id:
            links.append({
                "type": "related_to",
                "target": f"agent:{slugify(agent_id)}",
                "reason": "The life event belongs to this persistent agent identity.",
            })
        subject_target = payload.get("subject_target")
        if isinstance(subject_target, str) and ":" in subject_target:
            links.append({
                "type": "related_to",
                "target": subject_target,
                "reason": "The learned preference or relationship is scoped to this subject.",
            })

    if event_type == "relationship_created":
        src = payload.get("source_record")
        dst = payload.get("target")
        rel = payload.get("relationship_type", "related_to")
        if isinstance(src, str) and isinstance(dst, str):
            # Relationship events become audit records; graph_builder/curation may promote the link later.
            links.append({"type": str(rel), "target": dst, "reason": f"Relationship requested by {event['event_id']} from {src}."})

    if event_type.endswith("_removed"):
        tags.append("removal-event")
    if event_type.endswith("_completed"):
        tags.append("completed")

    timestamp = event["timestamp"]
    return {
        "id": graph_id(record_type, event),
        "type": record_type,
        "name": name[:120],
        "summary": summary[:700],
        "tags": sorted(set(tags)),
        "links": links,
        "provenance": {
            "source": event["event_id"],
            "confidence": payload.get("confidence", "medium"),
            "created": timestamp,
            "updated": timestamp,
        },
        "freshness": {"status": "current", "updated": timestamp[:10]},
    }


def load_events(paths: list[Path]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for path in paths:
        events.extend(load_json_events(path))
    return sorted(events, key=lambda event: (event["timestamp"], event["event_id"]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile Vegapunk Brain events into graph JSONL records.")
    parser.add_argument("--events", nargs="+", required=True, help="Event JSON/JSONL files or directories.")
    parser.add_argument("--out", required=True, help="Output graph JSONL path.")
    args = parser.parse_args()

    records = [record_from_event(event) for event in load_events([Path(item) for item in args.events])]
    write_jsonl(Path(args.out), records)
    print(f"Compiled {len(records)} graph records into {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
