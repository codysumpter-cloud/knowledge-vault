#!/usr/bin/env python3
"""Shared helpers for Vegapunk Brain event-sourced tooling."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

EVENT_TYPES = {
    "concept_created",
    "concept_updated",
    "task_created",
    "task_completed",
    "decision_made",
    "policy_updated",
    "council_update",
    "feature_added",
    "feature_removed",
    "repo_created",
    "repo_updated",
    "memory_created",
    "memory_updated",
    "relationship_created",
    "relationship_removed",
    "conversation_summarized",
    "device_registered",
    "model_changed",
    "local_memory_created",
    "app_created",
    "release_created",
    "agent_life_updated",
}

SOURCES = {"buddy-agent", "buddy-brain", "omni-buddy", "prismtek-apps", "knowledge-vault"}
EVENT_ID_RE = re.compile(r"^evt-[a-zA-Z0-9._:-]+$")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-") or "unnamed"


def load_json_events(path: Path) -> list[dict[str, Any]]:
    if path.is_dir():
        events: list[dict[str, Any]] = []
        for child in sorted(path.glob("*.json")):
            events.extend(load_json_events(child))
        for child in sorted(path.glob("*.jsonl")):
            events.extend(load_json_events(child))
        return events
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    return payload if isinstance(payload, list) else [payload]


def validate_event(event: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(event, dict):
        return ["event must be a JSON object"]
    required = {"event_id", "event_type", "source", "timestamp", "payload"}
    missing = sorted(required - set(event))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    extra = sorted(set(event) - required)
    if extra:
        errors.append(f"unknown fields: {', '.join(extra)}")
    if not isinstance(event.get("event_id"), str) or not EVENT_ID_RE.match(event.get("event_id", "")):
        errors.append("event_id must match evt-* format")
    if event.get("event_type") not in EVENT_TYPES:
        errors.append("event_type is not supported")
    if event.get("source") not in SOURCES:
        errors.append("source is not supported")
    if not isinstance(event.get("timestamp"), str) or not TS_RE.match(event.get("timestamp", "")):
        errors.append("timestamp must use YYYY-MM-DDTHH:MM:SSZ")
    if not isinstance(event.get("payload"), dict):
        errors.append("payload must be an object")
    return errors


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
