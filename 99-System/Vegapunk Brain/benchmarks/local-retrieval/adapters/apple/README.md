# Apple adapter

The Swift package implements the benchmark JSONL protocol with a deterministic baseline. Replace the `embedding` implementation with a Core ML, MLX, or Foundation Models adapter while preserving metadata and output shape.

```bash
swift run local-retrieval-apple
```

The baseline intentionally reports `native_acceleration: false`. Do not change that flag until the selected model path is measured on actual Apple hardware.
