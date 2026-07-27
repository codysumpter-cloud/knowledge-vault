#!/usr/bin/env python3
"""Public-safe local retrieval benchmark for Knowledge Vault adapters."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shlex
import subprocess
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Protocol

EXCLUDED_PARTS = {".git", "00-Private", "99-System/Security", "node_modules", ".venv", "venv"}


@dataclass(frozen=True)
class Chunk:
    id: str
    path: str
    heading: str
    text: str


@dataclass(frozen=True)
class QueryCase:
    query: str
    relevant: tuple[str, ...]


@dataclass(frozen=True)
class AdapterMetadata:
    name: str
    runtime: str
    model: str
    model_download_mb: float
    offline: bool
    native_acceleration: bool
    browser_fallback: bool
    dimension: int


class EmbeddingAdapter(Protocol):
    def metadata(self) -> AdapterMetadata: ...

    def embed(self, texts: list[str]) -> list[list[float]]: ...


class HashEmbeddingAdapter:
    """Deterministic dependency-free baseline; not a semantic model."""

    def __init__(self, dimension: int = 256) -> None:
        self.dimension = dimension

    def metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="hash-ngram-baseline",
            runtime="python",
            model="none",
            model_download_mb=0.0,
            offline=True,
            native_acceleration=False,
            browser_fallback=True,
            dimension=self.dimension,
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [hash_embedding(text, self.dimension) for text in texts]


class ExternalJsonlAdapter:
    """Adapter bridge for LiteRT.js, Core ML/MLX, Android LiteRT, or local services."""

    def __init__(self, command: str) -> None:
        self.command = shlex.split(command)
        if not self.command:
            raise ValueError("external adapter command is empty")

    def _request(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = subprocess.run(
            self.command,
            input=json.dumps(payload) + "\n",
            text=True,
            capture_output=True,
            check=False,
            timeout=300,
        )
        if result.returncode != 0:
            raise RuntimeError(f"adapter failed ({result.returncode}): {result.stderr.strip()}")
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError("adapter returned no JSONL response")
        return json.loads(lines[-1])

    def metadata(self) -> AdapterMetadata:
        return AdapterMetadata(**self._request({"op": "metadata"})["metadata"])

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self._request({"op": "embed", "texts": texts})
        return [[float(value) for value in row] for row in response["vectors"]]


def normalized_tokens(text: str) -> list[str]:
    token = []
    tokens = []
    for char in text.lower():
        if char.isalnum() or char in {"-", "_"}:
            token.append(char)
        elif token:
            tokens.append("".join(token))
            token = []
    if token:
        tokens.append("".join(token))
    return tokens


def hash_embedding(text: str, dimension: int) -> list[float]:
    vector = [0.0] * dimension
    tokens = normalized_tokens(text)
    features = tokens + [f"{tokens[index]}::{tokens[index + 1]}" for index in range(max(0, len(tokens) - 1))]
    for feature in features:
        digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=16).digest()
        index = int.from_bytes(digest[:8], "big") % dimension
        sign = 1.0 if digest[8] % 2 == 0 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError(f"embedding dimension mismatch: {len(left)} != {len(right)}")
    return sum(a * b for a, b in zip(left, right, strict=True))


def is_public_safe(path: Path) -> bool:
    return not any(part in EXCLUDED_PARTS for part in path.parts)


def chunk_markdown(path: Path, root: Path, max_chars: int = 1200) -> list[Chunk]:
    relative = path.relative_to(root).as_posix()
    source = path.read_text(encoding="utf-8", errors="replace")
    heading = path.stem
    paragraphs: list[str] = []
    chunks: list[Chunk] = []

    def flush() -> None:
        nonlocal paragraphs
        text = "\n\n".join(paragraphs).strip()
        paragraphs = []
        if not text:
            return
        while text:
            piece = text[:max_chars]
            if len(text) > max_chars:
                split = piece.rfind("\n\n")
                if split > max_chars // 2:
                    piece = piece[:split]
            text = text[len(piece):].lstrip()
            ordinal = len(chunks)
            chunks.append(Chunk(
                id=f"{relative}#{ordinal}",
                path=relative,
                heading=heading,
                text=f"{heading}\n{piece}",
            ))

    for line in source.splitlines():
        if line.startswith("#"):
            flush()
            heading = line.lstrip("#").strip() or path.stem
        elif line.strip() == "":
            if paragraphs and sum(len(item) for item in paragraphs) >= max_chars:
                flush()
            else:
                paragraphs.append("")
        else:
            paragraphs.append(line)
    flush()
    return chunks


def build_corpus(root: Path, include: list[str] | None = None) -> list[Chunk]:
    candidates: list[Path] = []
    selected = include or ["README.md", "AGENTS.md", "SYSTEMMAP.md", "AGENT_KNOWLEDGE_INDEX.md", "99-System/Vegapunk Brain"]
    for item in selected:
        path = root / item
        if path.is_file() and path.suffix.lower() == ".md" and is_public_safe(path.relative_to(root)):
            candidates.append(path)
        elif path.is_dir():
            candidates.extend(
                candidate
                for candidate in path.rglob("*.md")
                if candidate.is_file() and is_public_safe(candidate.relative_to(root))
            )
    chunks = []
    for path in sorted(set(candidates)):
        chunks.extend(chunk_markdown(path, root))
    return chunks


def load_queries(path: Path) -> list[QueryCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [QueryCase(str(item["query"]), tuple(str(value) for value in item["relevant"])) for item in payload]


def rank(query_vector: list[float], chunk_vectors: list[list[float]], chunks: list[Chunk], limit: int) -> list[tuple[Chunk, float]]:
    scored = [(chunk, cosine(query_vector, vector)) for chunk, vector in zip(chunks, chunk_vectors, strict=True)]
    return sorted(scored, key=lambda item: (-item[1], item[0].id))[:limit]


def evaluate(adapter: EmbeddingAdapter, chunks: list[Chunk], queries: list[QueryCase], top_k: int = 5) -> dict[str, Any]:
    if not chunks:
        raise ValueError("corpus has no chunks")
    metadata = adapter.metadata()
    tracemalloc.start()
    started = time.perf_counter()
    chunk_vectors = adapter.embed([chunk.text for chunk in chunks])
    cold_ms = (time.perf_counter() - started) * 1000.0
    warm_started = time.perf_counter()
    query_vectors = adapter.embed([case.query for case in queries])
    warm_ms_total = (time.perf_counter() - warm_started) * 1000.0
    _current, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    reciprocal_ranks = []
    recall_hits = 0
    details = []
    for case, query_vector in zip(queries, query_vectors, strict=True):
        results = rank(query_vector, chunk_vectors, chunks, top_k)
        relevant_rank = None
        for index, (chunk, _score) in enumerate(results, start=1):
            if any(chunk.path == target or chunk.path.startswith(target.rstrip("/") + "/") for target in case.relevant):
                relevant_rank = index
                break
        if relevant_rank is not None:
            recall_hits += 1
            reciprocal_ranks.append(1.0 / relevant_rank)
        else:
            reciprocal_ranks.append(0.0)
        details.append({
            "query": case.query,
            "relevant": list(case.relevant),
            "first_relevant_rank": relevant_rank,
            "results": [{"path": chunk.path, "chunk_id": chunk.id, "score": round(score, 6)} for chunk, score in results],
        })
    query_count = len(queries)
    return {
        "version": 1,
        "adapter": asdict(metadata),
        "corpus": {"chunks": len(chunks), "queries": query_count},
        "metrics": {
            "recall_at_k": round(recall_hits / query_count, 4) if query_count else 0.0,
            "mrr": round(sum(reciprocal_ranks) / query_count, 4) if query_count else 0.0,
            "top_k": top_k,
            "cold_embed_ms_total": round(cold_ms, 2),
            "warm_embed_ms_per_query": round(warm_ms_total / query_count, 2) if query_count else 0.0,
            "peak_python_memory_mb": round(peak_bytes / 1024 / 1024, 2),
        },
        "targets": {
            "model_download_under_150_mb": metadata.model_download_mb < 150,
            "warm_embedding_under_100_ms": (warm_ms_total / query_count if query_count else 0.0) < 100,
            "peak_memory_under_500_mb": peak_bytes / 1024 / 1024 < 500,
            "offline_required": metadata.offline,
            "browser_fallback_required": metadata.browser_fallback,
            "native_acceleration_preferred": metadata.native_acceleration,
        },
        "details": details,
    }


def compare_to_baseline(candidate: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    candidate_recall = float(candidate["metrics"]["recall_at_k"])
    baseline_recall = float(baseline["metrics"]["recall_at_k"])
    quality_delta = candidate_recall - baseline_recall
    return {
        "candidate": candidate["adapter"]["name"],
        "baseline": baseline["adapter"]["name"],
        "recall_delta": round(quality_delta, 4),
        "within_5_percent_of_baseline": candidate_recall >= baseline_recall - 0.05,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark local Knowledge Vault retrieval adapters.")
    parser.add_argument("--vault-root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--queries", type=Path, default=Path(__file__).with_name("queries.json"))
    parser.add_argument("--adapter", choices=("hash", "external"), default="hash")
    parser.add_argument("--adapter-command", help="JSONL adapter command when --adapter=external")
    parser.add_argument("--include", action="append", help="Relative file/directory to include; repeatable")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--baseline", type=Path, help="Optional prior benchmark JSON to compare against")
    args = parser.parse_args()
    if args.top_k < 1:
        raise SystemExit("--top-k must be positive")
    adapter: EmbeddingAdapter
    if args.adapter == "hash":
        adapter = HashEmbeddingAdapter()
    elif args.adapter_command:
        adapter = ExternalJsonlAdapter(args.adapter_command)
    else:
        raise SystemExit("--adapter-command is required for external adapters")
    chunks = build_corpus(args.vault_root.resolve(), args.include)
    report = evaluate(adapter, chunks, load_queries(args.queries), args.top_k)
    if args.baseline:
        baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        report["baseline_comparison"] = compare_to_baseline(report, baseline)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
