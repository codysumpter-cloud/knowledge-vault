---
title: Lossless Recall
description: Use the LCM SQLite store to retrieve raw, uncompressed session history.
category: memory
---

# Lossless Recall

## Goal
Retrieve exact, raw data from past interactions to eliminate context drift.

## Workflow
1. Use `sqlite3 ~/.hermes/lcm.db "SELECT content FROM messages WHERE content LIKE '%search_term%'"` for raw keyword search.
2. Use the la-summarization logic to expand compressed nodes if a summary is too vague.
3. Cross-reference the raw record with the current state to verify accuracy.

## Pitfalls
- Do not rely on the chat history for absolute paths or precise version numbers; always query the LCM store.
