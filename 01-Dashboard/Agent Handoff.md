---
type: dashboard
scope: agent-handoff
last_synced: 2026-08-06
tags:
  - dashboard
  - agent
  - handoff
---

# Agent Handoff

Read this before making changes in KnowledgeVault.

## Current operating direction

- OpenClaw is retired for current work.
- Hermes-agent is the current main working agent system.
- Buddy-agent is being prepared to become the primary runtime.
- KnowledgeVault is the book and memory layer.

## Required reading

1. `README.md`
2. `AGENTS.md`
3. `SYSTEMMAP.md`
4. `RUNBOOK.md`
5. `BACKLOG.md`
6. `SECURITY.md`
7. `01-Dashboard/Project Source of Truth.md`
8. `30 - Projects/GitHub/GitHub Projects Index.md`

## Current vault facts

- Public repos indexed: 83
- Registry owner: `codysumpter-cloud`
- Last generated: 2026-08-06

## Safe change pattern

1. Make additive changes.
2. Preserve human-authored sections unless directly asked to rewrite them.
3. Do not present reference notes as implemented runtime features.
4. Run `python3 "99-System/Automation/vault_doctor.py"`.
5. Open a PR with clear receipts.
