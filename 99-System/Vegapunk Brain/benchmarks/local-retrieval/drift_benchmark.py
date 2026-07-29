#!/usr/bin/env python3
"""Adversarial retrieval-drift benchmark for provenance-aware memory systems."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Record:
    record_id: str
    entity_id: str
    text: str
    observed_at: str
    valid_until: str | None
    trust_tier: str
    confidence: float
    superseded_by: str | None = None
    contradicts: tuple[str, ...] = ()
    is_current: bool = False
    kind: str = "other"
    content_hash: str = ""


def _tokens(text: str) -> list[str]:
    current: list[str] = []
    values: list[str] = []
    for char in text.lower():
        if char.isalnum() or char in {"-", "_"}:
            current.append(char)
        elif current:
            values.append("".join(current))
            current = []
    if current:
        values.append("".join(current))
    return values


def _sparse_vector(text: str, dimension: int = 4096) -> dict[int, float]:
    tokens = _tokens(text)
    features = tokens + [
        f"{tokens[index]}::{tokens[index + 1]}" for index in range(max(0, len(tokens) - 1))
    ]
    counts: Counter[int] = Counter()
    for feature in features:
        digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
        counts[int.from_bytes(digest, "big") % dimension] += 1.0
    norm = math.sqrt(sum(value * value for value in counts.values())) or 1.0
    return {feature: value / norm for feature, value in counts.items()}


def _record(**values: Any) -> Record:
    text = str(values["text"])
    values["content_hash"] = f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"
    return Record(**values)


def generate_corpus(item_count: int = 10_240, query_count: int = 128) -> tuple[list[Record], list[str]]:
    if item_count < 4:
        raise ValueError("item_count must be at least 4")
    groups = math.ceil(item_count / 4)
    records: list[Record] = []
    for index in range(groups):
        entity = f"asset-{index:05d}"
        current_id = f"{entity}:current"
        stale_id = f"{entity}:stale"
        conflict_id = f"{entity}:conflict"
        current_value = 1_000 + index
        old_value = 900 + index
        conflicting_value = 1_100 + index
        records.extend(
            [
                _record(
                    record_id=current_id,
                    entity_id=entity,
                    text=(
                        f"{entity} authoritative operating record. Operating limit {current_value}. "
                        f"Status current. Effective 2026-01-01. Supersedes {stale_id}."
                    ),
                    observed_at="2026-07-01T00:00:00Z",
                    valid_until="2027-01-01T00:00:00Z",
                    trust_tier="authoritative",
                    confidence=0.98,
                    contradicts=(conflict_id,),
                    is_current=True,
                    kind="current",
                ),
                _record(
                    record_id=stale_id,
                    entity_id=entity,
                    text=(
                        f"What is the current operating limit for {entity}? "
                        f"The current operating limit for {entity} is {old_value}. "
                        f"{entity} current operating limit {old_value}. Legacy operations handbook."
                    ),
                    observed_at="2024-01-01T00:00:00Z",
                    valid_until="2025-12-31T23:59:59Z",
                    trust_tier="verified",
                    confidence=0.95,
                    superseded_by=current_id,
                    kind="stale",
                ),
                _record(
                    record_id=conflict_id,
                    entity_id=entity,
                    text=(
                        f"{entity} current operating limit is {conflicting_value}. "
                        f"Unreviewed field note for {entity}."
                    ),
                    observed_at="2026-06-20T00:00:00Z",
                    valid_until=None,
                    trust_tier="untrusted",
                    confidence=0.40,
                    contradicts=(current_id,),
                    kind="conflict",
                ),
                _record(
                    record_id=f"{entity}:backup",
                    entity_id=f"{entity}-backup",
                    text=(
                        f"{entity}-backup current operating limit is {500 + index}. "
                        f"Backup asset record, not {entity}."
                    ),
                    observed_at="2026-07-01T00:00:00Z",
                    valid_until="2027-01-01T00:00:00Z",
                    trust_tier="supporting",
                    confidence=0.80,
                    kind="near_miss",
                ),
            ]
        )
    records = records[:item_count]
    tested = min(query_count, groups)
    return records, [f"asset-{index:05d}" for index in range(tested)]


def build_index(records: list[Record]) -> dict[int, list[tuple[int, float]]]:
    postings: dict[int, list[tuple[int, float]]] = defaultdict(list)
    for index, record in enumerate(records):
        for feature, weight in _sparse_vector(record.text).items():
            postings[feature].append((index, weight))
    return postings


def similarity_rank(
    query: str,
    records: list[Record],
    postings: dict[int, list[tuple[int, float]]],
    limit: int = 10,
) -> list[tuple[int, float]]:
    scores: dict[int, float] = defaultdict(float)
    for feature, query_weight in _sparse_vector(query).items():
        for record_index, record_weight in postings.get(feature, []):
            scores[record_index] += query_weight * record_weight
    return sorted(
        scores.items(),
        key=lambda item: (-item[1], records[item[0]].record_id),
    )[:limit]


def _parse(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def provenance_rerank(
    entity_id: str,
    ranked: list[tuple[int, float]],
    records: list[Record],
    record_ids: dict[str, int],
    *,
    as_of: str = "2026-07-29T00:00:00Z",
) -> tuple[list[tuple[int, float]], bool, int]:
    candidates = dict(ranked)
    expanded = 0
    for record_index in list(candidates):
        record = records[record_index]
        references = ([record.superseded_by] if record.superseded_by else []) + list(
            record.contradicts
        )
        for reference in references:
            linked_index = record_ids.get(reference)
            if linked_index is not None and linked_index not in candidates:
                candidates[linked_index] = 0.0
                expanded += 1

    now = _parse(as_of)
    assert now is not None
    conflict_detected = False
    rescored: list[tuple[int, float]] = []
    for record_index, similarity in candidates.items():
        record = records[record_index]
        score = similarity
        valid_until = _parse(record.valid_until)
        if valid_until and valid_until < now:
            score -= 2.0
        if record.superseded_by:
            score -= 1.25
        if record.trust_tier == "authoritative":
            score += 0.80
        elif record.trust_tier == "verified":
            score += 0.45
        elif record.trust_tier == "untrusted":
            score -= 0.80
        score += 0.50 * record.confidence
        if record.entity_id == entity_id:
            score += 0.35
        if record.is_current:
            score += 0.50
        if record.contradicts:
            conflict_detected = True
            if record.trust_tier == "untrusted":
                score -= 0.50
        rescored.append((record_index, score))
    return (
        sorted(rescored, key=lambda item: (-item[1], records[item[0]].record_id)),
        conflict_detected,
        expanded,
    )


def run_benchmark(item_count: int = 10_240, query_count: int = 128) -> dict[str, Any]:
    started = time.perf_counter()
    records, entities = generate_corpus(item_count, query_count)
    postings = build_index(records)
    record_ids = {record.record_id: index for index, record in enumerate(records)}
    baseline: Counter[str] = Counter()
    provenance: Counter[str] = Counter()
    conflicts_detected = 0
    graph_expansions = 0

    for entity in entities:
        query = f"What is the current operating limit for {entity}?"
        ranked = similarity_rank(query, records, postings)
        baseline[records[ranked[0][0]].kind] += 1
        reranked, conflict_detected, expanded = provenance_rerank(
            entity, ranked, records, record_ids
        )
        provenance[records[reranked[0][0]].kind] += 1
        conflicts_detected += int(conflict_detected)
        graph_expansions += expanded

    total = len(entities)
    return {
        "version": 1,
        "benchmark": "retrieval-drift-10k",
        "corpus": {
            "items": len(records),
            "queries": total,
            "record_kinds": dict(Counter(record.kind for record in records)),
        },
        "baseline_similarity_only": {
            "current_top1_rate": round(baseline["current"] / total, 4),
            "stale_top1_rate": round(baseline["stale"] / total, 4),
            "near_miss_top1_rate": round(baseline["near_miss"] / total, 4),
            "conflict_top1_rate": round(baseline["conflict"] / total, 4),
            "false_current_rate": round(1.0 - baseline["current"] / total, 4),
        },
        "provenance_graph_rerank": {
            "current_top1_rate": round(provenance["current"] / total, 4),
            "stale_top1_rate": round(provenance["stale"] / total, 4),
            "near_miss_top1_rate": round(provenance["near_miss"] / total, 4),
            "conflict_top1_rate": round(provenance["conflict"] / total, 4),
            "false_current_rate": round(1.0 - provenance["current"] / total, 4),
            "conflict_detection_recall": round(conflicts_detected / total, 4),
            "graph_expansions": graph_expansions,
            "lineage_coverage": round(
                sum(bool(record.content_hash and record.observed_at) for record in records)
                / len(records),
                4,
            ),
        },
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        "limitations": [
            "The corpus is synthetic and adversarial; it proves the evaluation contract, not production quality.",
            "The similarity-only baseline is a dependency-free sparse hash-vector cosine index, not a hosted embedding model.",
            "Real Mitosis, cloud-vector, and local-model adapters should run through the same corpus and metrics before comparative claims.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Measure stale and near-miss retrieval drift at 10k+ items."
    )
    parser.add_argument("--items", type=int, default=10_240)
    parser.add_argument("--queries", type=int, default=128)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_benchmark(args.items, args.queries)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
