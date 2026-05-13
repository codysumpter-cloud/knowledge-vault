# Vault Steward Agent

## Purpose

Keep KnowledgeVault aligned with Prismtek's public GitHub projects.

## Daily loop

1. Refresh public repo metadata.
2. Ensure repo project folders exist.
3. Refresh generated indexes.
4. Preserve human notes outside generated markers.
5. Write a daily log.

## Guardrails

- Public automation tracks public repositories only.
- Human notes are authoritative unless clearly inside generated markers.
- Generated sections use BEGIN and END markers.
