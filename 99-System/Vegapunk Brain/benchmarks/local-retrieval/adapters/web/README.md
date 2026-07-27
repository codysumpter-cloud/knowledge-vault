# Web adapter

`hash-adapter.mjs` is a dependency-free browser-compatible fallback used to prove the JSONL contract. It is not the quality target.

A LiteRT.js or Transformers.js implementation should expose the same two operations:

```json
{"op":"metadata"}
{"op":"embed","texts":["..."]}
```

The adapter must report model download size, offline behavior, native acceleration, browser fallback support, and embedding dimension. The benchmark rejects dimension mismatches and compares retrieval quality to a saved baseline.
