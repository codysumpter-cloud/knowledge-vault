---
type: integration
status: tested
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-07-29
risk_level: low
privacy: public
freshness: slow-changing
agent_load: task-specific
tags:
  - vegapunk-brain
  - local-retrieval
  - benchmark
  - litert
  - provenance
  - retrieval-drift
---

# Local Knowledge Vault retrieval benchmark

This harness measures a narrow, privacy-friendly first local workload:

```text
document chunk
  -> local embedding adapter
  -> cosine vector search
  -> ranked Knowledge Vault context
```

It does not implement a full local autonomous agent. The adapter boundary allows LiteRT.js, Android LiteRT, Core ML/MLX/Foundation Models, Transformers.js, or a local service to be compared without changing the corpus/evaluation logic.

## Targets

| Metric | Target |
|---|---:|
| Model download | Under 150 MB initially |
| Warm embedding latency | Under 100 ms per short query |
| Peak memory | Under 500 MB |
| Offline operation | Required |
| Browser fallback | Required for the web path |
| Native acceleration | Preferred and must be measured |
| Retrieval quality | Within 5 percentage points of the selected cloud baseline |

## Run the dependency-free baseline

From the vault root:

```bash
python3 "99-System/Vegapunk Brain/benchmarks/local-retrieval/benchmark.py" \
  --output /tmp/knowledge-vault-local-baseline.json
```

Run the web-compatible external adapter:

```bash
python3 "99-System/Vegapunk Brain/benchmarks/local-retrieval/benchmark.py" \
  --adapter external \
  --adapter-command 'node 99-System/Vegapunk\ Brain/benchmarks/local-retrieval/adapters/web/hash-adapter.mjs' \
  --output /tmp/knowledge-vault-web-baseline.json
```

The hash adapters are deterministic contract baselines, not semantic-quality targets. A real model adapter must use the same `metadata` and `embed` JSONL protocol, save its report, and compare against a named baseline.

## Adversarial 10k retrieval-drift proof

`drift_benchmark.py` directly exercises the failure mode that appears when a growing knowledge base contains near-duplicates, expired records, newer replacements, and unresolved contradictions.

The default corpus contains **10,240 records** split evenly between:

- current authoritative records;
- stale records deliberately written to be stronger similarity matches;
- unresolved contradictory records;
- near-miss records for similarly named entities.

It compares a dependency-free sparse hash-vector cosine baseline with provenance-aware temporal and graph reranking. The second pass uses stable IDs, content hashes, observation and expiry timestamps, trust tiers, confidence, `superseded_by` links, and contradiction edges.

```bash
python3 "99-System/Vegapunk Brain/benchmarks/local-retrieval/drift_benchmark.py" \
  --items 10240 \
  --queries 128 \
  --output /tmp/retrieval-drift-10k.json
```

The focused contract expects the adversarial similarity-only baseline to select stale records, then requires provenance/graph reranking to:

- return the current authoritative record at top-1;
- suppress stale and near-miss top-1 results;
- detect every planted contradiction;
- preserve source lineage for every record.

This is a synthetic adversarial proof, not a claim about production Mitosis, hosted-vector, or local-model quality. Those providers should run through the same corpus and metrics before comparative claims are made.

## Safety

- The default real-vault corpus is public-safe and excludes `00-Private`, `99-System/Security`, VCS metadata, virtual environments, and dependency directories.
- The adversarial 10k corpus is generated synthetic data and contains no user content.
- Reports contain paths, ranks, timing, model metadata, stable source IDs, and hashes. They do not store prompts, secrets, tokens, credentials, browser state, or private notes.
- Native acceleration flags are evidence claims. Keep them false until measured on the target device.

## Current implementation status

- Python corpus/chunk/rank/evaluation harness: tested locally and in CI.
- Python deterministic adapter: tested locally and in CI.
- Node/web-compatible JSONL adapter: tested locally and in CI.
- Adversarial 10,240-item drift benchmark: locally tested; CI required on the active PR head.
- Swift adapter scaffold: source-complete, requires Apple hardware/toolchain verification.
- Android adapter scaffold: metadata/build boundary only; real embeddings remain blocked on selecting and testing the LiteRT model/runtime.
