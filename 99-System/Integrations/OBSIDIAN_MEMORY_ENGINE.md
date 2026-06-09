# Obsidian Memory Engine Integration

Status: active
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

This note explains how to use the runnable KnowledgeVault Memory Engine with Obsidian.

No Obsidian plugin is required. The engine works with normal markdown files, YAML-style front matter, wikilinks, and generated index notes.

## Quick start

From the vault root:

```bash
python3 -m memory_engine index
python3 -m memory_engine obsidian
```

Then open this generated note in Obsidian:

```txt
99-System/Memory Engine/Obsidian Memory Index.md
```

## What Obsidian gets

The generated Obsidian index includes:

- vault stats
- note titles
- note types
- note status values
- tags
- wikilinks to indexed notes

The engine also emits `obsidian://open` links in JSON search results, which lets tools jump directly into Obsidian when supported by the host OS.

## Recommended workflow

1. Open this repo as an Obsidian vault.
2. Run `python3 -m memory_engine index` after meaningful note changes.
3. Use `Obsidian Memory Index.md` as a generated map.
4. Keep durable human-written knowledge in normal notes.
5. Treat generated outputs as disposable and rebuildable.

## Agent workflow with Obsidian

Agents can use the same vault without needing Obsidian running:

```bash
python3 -m memory_engine search "vault maintenance" --json
python3 -m memory_engine show --query "agent knowledge" --json --body
python3 -m memory_engine bundle --query "memory engine" --output "99-System/Context Bundles/memory-engine.bundle.md"
```

Humans can then open the generated bundle or related notes in Obsidian.

## Future plugin path

A future Obsidian plugin can use the Memory Engine outputs instead of replacing them.

Good plugin targets:

- button to rebuild index
- panel for search results
- command to export current-note context bundle
- command to start or stop the local read-only server
- view for graph records and backlinks

The current CLI is intentionally the stable base layer.
