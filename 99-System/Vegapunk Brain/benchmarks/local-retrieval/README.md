---
type: integration
status: tested
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-08-03
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

## Evidence contract

A benchmark JSON alone is not enough to approve a local runtime for Buddy routing. Pair the report with a `buddy.local-retrieval-run.v1` manifest, then validate it:

```bash
python3 "99-System/Vegapunk Brain/benchmarks/local-retrieval/evidence_contract.py" \
  --report /tmp/knowledge-vault-local-baseline.json \
  --manifest /path/to/run-manifest.json \
  --output /tmp/knowledge-vault-local-evidence.json
```

The validator emits a compact `buddy.local-retrieval-evidence.v1` receipt. It hashes the exact report but excludes raw queries and ranked paths.

Two measurement classes are supported:

- `contract_baseline`: proves corpus, adapter protocol, ranking, and report generation. It must use a non-model adapter and is never qualified for routing.
- `hardware_measured`: may qualify for routing only when it identifies the real model and SHA-256, quantization, runtime and adapter versions, hardware, operating system, architecture, cold-start latency, warm latency, peak memory, energy observation, offline verification, fallback behavior, acceleration evidence, and durable evidence references.

The manifest model and runtime must match the benchmark report. Warm latency must also match the report within a small rounding tolerance. Missing hardware evidence is a validation failure, not an implied zero or assumed capability.

`--require-routing-qualified` turns a valid contract-only run into a non-zero exit so release or routing workflows cannot accidentally accept it.

CI uses the committed fixtures only as explicit contract baselines. CI does not claim M5, WebGPU, WASM, Android, native acceleration, battery, or real-model performance.

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
- Full benchmark reports contain public-safe paths, ranks, timing, model metadata, stable source IDs, and hashes. Evidence receipts omit raw queries and ranked paths.
- Reports and receipts do not store prompts, secrets, tokens, credentials, browser state, or private notes.
- Native acceleration, offline behavior, fallback behavior, energy, and routing qualification are evidence claims. Keep them unqualified until measured on the target device.

## Current implementation status

- Python corpus/chunk/rank/evaluation harness: tested locally and in CI.
- Python deterministic adapter: tested locally and in CI as a contract baseline.
- Node/web-compatible JSONL adapter: tested locally and in CI as a contract baseline.
- Evidence receipt and routing-qualification contract: implemented; hardware qualification still requires a real target run.
- Adversarial 10,240-item drift benchmark: locally tested; CI required on the active PR head.
- Swift adapter scaffold: source-complete, requires Apple hardware/toolchain verification.
- Android adapter scaffold: metadata/build boundary only; real embeddings remain blocked on selecting and testing the LiteRT model/runtime.
