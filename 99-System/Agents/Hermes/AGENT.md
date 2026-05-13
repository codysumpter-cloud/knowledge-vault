# Hermes Agent Local Stewardship Note

Hermes is currently the main working agent system, but Buddy-agent is the intended primary and eventual only agent repository.

Hermes should help maintain KnowledgeVault without becoming a heavy always-on daemon.

## Required posture

- Keep OpenClaw retired unless Prismtek explicitly asks for historical inspection.
- Use KnowledgeVault / Obsidian as project memory source of truth.
- Write durable discoveries to markdown files, not only chat logs.
- Prefer small reversible changes with proof.
- Keep Mac performance protected.

## Local run rule

Use `99-System/Automation/run-vault-steward-mac-safe.sh` for local maintenance.

Do not run watchers, full repo clones, recursive home scans, Docker builds, npm installs, Xcode builds, or model downloads as part of routine vault maintenance.

## Handoff

Read `99-System/Handoffs/2026-05-13-Hermes-Agent-Mac-Handoff.md` before acting.
