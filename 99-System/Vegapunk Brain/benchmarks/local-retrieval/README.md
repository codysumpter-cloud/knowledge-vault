---
type: integration
status: tested
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-07-27
risk_level: low
privacy: public
freshness: slow-changing
agent_load: task-specific
tags:
  - vegapunk-brain
  - local-retrieval
  - benchmark
  - litert
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

## Safety

- The default corpus is public-safe and excludes `00-Private`, `99-System/Security`, VCS metadata, virtual environments, and dependency directories.
- Reports contain paths, ranks, timing, model metadata, and numeric vectors only inside the adapter process. They do not store prompts, secrets, tokens, credentials, or private notes.
- Native acceleration flags are evidence claims. Keep them false until measured on the target device.

## Current implementation status

- Python corpus/chunk/rank/evaluation harness: tested locally.
- Python deterministic adapter: tested locally.
- Node/web-compatible JSONL adapter: tested locally.
- Swift adapter scaffold: source-complete, requires Apple hardware/toolchain verification.
- Android adapter scaffold: metadata/build boundary only; real embeddings remain blocked on selecting and testing the LiteRT model/runtime.
