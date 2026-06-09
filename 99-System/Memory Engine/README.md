# Memory Engine Workspace

Status: active
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

This folder is the default output workspace for the runnable KnowledgeVault Memory Engine.

Run the engine from the repo root:

```bash
python3 -m memory_engine index
```

Default generated outputs:

- `memory-index.json`
- `memory-graph.json`
- `Obsidian Memory Index.md`

## Human workflow

1. Open KnowledgeVault in Obsidian.
2. Run `python3 -m memory_engine index`.
3. Open `99-System/Memory Engine/Obsidian Memory Index.md`.
4. Use the generated note to browse vault records by title, type, status, and tags.

## Agent workflow

1. Run `python3 -m memory_engine index`.
2. Load `memory-index.json` or call the local server.
3. Search for task-specific notes.
4. Export a bundle when the task needs a curated context packet.
5. Verify volatile claims against live sources before acting.

## Local API

```bash
python3 -m memory_engine serve
```

Endpoints:

- `/health`
- `/search?q=agent`
- `/record?path=README.md`
- `/bundle?q=memory`

## Generated files

Generated JSON and ad hoc bundles are local outputs. They can be regenerated from markdown notes.

Do not hand-edit generated files as durable memory. Put durable knowledge in normal vault notes instead.
