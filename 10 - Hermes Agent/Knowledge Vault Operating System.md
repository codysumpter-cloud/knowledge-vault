# Knowledge Vault Operating System

Updated: 2026-05-11 14:22

## Purpose
Turn Obsidian from templates into BMO's operational brain: receipts, runbooks, source maps, ingestion queues, and release state.

## Folder roles
- `00 - Command Center`: dashboards and current operating picture.
- `10 - Hermes Agent`: Hermes config, skills, provider/tooling absorption.
- `20 - Operations`: release, VPS, trading, build, sync runbooks.
- `30 - Projects`: project-specific MOCs and status.
- `90 - Ingest`: raw imports waiting for absorption/rejection.

## Resource absorption workflow
1. Capture source under `90 - Ingest` or a project note.
2. Classify as skill / config / runbook / cron / note / reject.
3. Implement if operationally useful.
4. Add receipt: command, path, status, verification.
5. If repeated workflow emerges, promote to Hermes skill.

## Guardrails
- No raw secrets. Use `[REDACTED]` and pointers to secure locations.
- Prefer working runbooks over empty templates.
- Every dashboard item links to a receipt or next action.
