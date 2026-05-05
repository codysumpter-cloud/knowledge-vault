---
title: Advanced Context Management
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [memory, context, lcm, context-mode, optimization]
sources: [agentmemory, context-mode, hermes-lcm]
confidence: high
---

# Advanced Context Management

This page synthesizes the most powerful context optimization strategies from `agentmemory`, `context-mode`, and `hermes-lcm`. The goal is to achieve **Bounded Context, Unbounded Memory**.

## 1. The "Memory Gap" Problem
Traditional agents suffer from two failures:
- **Lossy Compaction:** When the context window fills, the agent replaces history with a summary, losing critical details.
- **Context Flooding:** Tool outputs (e.g., a 50KB file) consume 40% of the window in one turn, forcing premature compaction.

## 2. The Solution Suite

### Lossless Recall (Hermes-LCM)
Instead of flat summaries, `hermes-lcm` implements a **Hierarchical DAG Summary** system.
- **The DAG:** Messages are compacted into D0 leaf nodes $\rightarrow$ D1 nodes $\rightarrow$ D2 nodes.
- **Lossless Drill-down:** The agent has dedicated tools (`lcm_expand`, `lcm_grep`) to drill back into raw messages without needing a full session search.
- **Immutable Store:** All messages are stored in SQLite; summaries are purely for the active context window.

### Context Saving (Context-Mode)
To prevent flooding, `context-mode` introduces **Sandbox Routing**.
- **Out-of-Band Storage:** Large tool outputs are kept in a sandbox (SQLite) rather than dumped into the prompt.
- **T-S-T Paradigm (Think-Script-Tell):** Instead of reading 50 files to count functions, the agent writes a script to do the counting and only returns the final result.
- **Session Continuity:** Event-based tracking (file edits, decisions) ensures that when a conversation compacts, the agent doesn't "forget" what it was currently doing.

### Persistent Knowledge (AgentMemory)
While LCM handles the *session*, `agentmemory` handles the *identity*.
- **Hybrid Search:** Uses BM25 + Vector + Graph (RRF fusion) to retrieve memories across sessions.
- **Automatic Capture:** Uses hooks to silently capture preferences and project facts without manual `save` commands.
- **Confidence Scoring:** Memories are assigned confidence levels and managed via a lifecycle (decay/forget).

## 3. Implementation Strategy for BMO Stack
To reach "Phantom-Free" stability, the BMO stack should integrate these as follows:
1. **Bottom Layer (L1):** `agentmemory` for cross-session a-priori knowledge.
2. **Middle Layer (L2):** `hermes-lcm` for lossless current-session recall.
3. **Top Layer (L3):** `context-mode` to prevent tool-output flooding.

[[buddy-system-architecture]]
[[omni-bmo-sync-protocol]]
