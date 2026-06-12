# Vegapunk Brain Scripts

## End-to-end local run

From the repository root:

```bash
bash "99-System/Vegapunk Brain/scripts/run-vegapunk-brain.sh"
```

The script compiles the example session, lints seed + generated records, builds the compiled graph, lints the compiled graph, generates indexes, and runs a sample search for `Knowledge Vault`.

Generated outputs are ignored by git by default:

- `graph/generated.graph.jsonl`
- `graph/compiled.graph.jsonl`
- `indexes/*.json`
