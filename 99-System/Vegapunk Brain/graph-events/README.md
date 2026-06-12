# Graph Events

This folder documents the intended intake area for public-safe graph events emitted by Buddy-compatible repos.

Do not store private or sensitive runtime events here while KnowledgeVault is public.

Recommended event flow:

1. Producer repo emits public-safe event JSON or JSONL.
2. KnowledgeVault imports or summarizes the event.
3. `memory_compiler.py` compiles event summaries into graph records.
4. `graph_linter.py` validates graph records.
5. `graph_builder.py` merges records.
6. `concept_indexer.py` regenerates indexes.
