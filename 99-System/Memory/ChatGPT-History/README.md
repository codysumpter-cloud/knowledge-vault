# ChatGPT History

This folder is for **public-safe ChatGPT history digests**, not raw transcript dumps.

KnowledgeVault is public and agent-readable, so this area should only contain durable, reusable context that is safe to expose:

- project summaries
- durable decisions
- repo/source-of-truth notes
- architecture direction
- sanitized handoff context
- open loops and next actions
- import procedures and redaction checklists

Do **not** store:

- raw ChatGPT export archives
- secrets, tokens, API keys, cookies, passwords, certificates, or `.env` contents
- private repo names unless they are already public-safe and intentionally documented
- local machine paths that expose sensitive identity or workspace state
- signed-in browser/session details
- trading credentials, wallet details, account numbers, or execution instructions
- copyrighted binaries, ROMs, private client patches, or automation payloads

## Current files

- [`2026-06-08-sanitized-history-seed.md`](2026-06-08-sanitized-history-seed.md) — first public-safe seed digest created from available ChatGPT context.

## Import model

Use a two-layer model:

1. **Private raw archive** — kept outside this public repository, preferably local-only or in a private encrypted store.
2. **Public-safe digest** — committed here after redaction and summarization.

Agents may append new dated digests here when the content is useful for future project work and passes the public-safety checklist.

## Redaction checklist

Before committing any ChatGPT-derived note:

- Remove secrets and credentials.
- Remove raw/private transcripts.
- Remove private operational details.
- Replace exact local paths with generic descriptions.
- Replace account identifiers with role-based descriptions.
- Link only to public-safe sources.
- Mark uncertain/stale claims clearly.
- Prefer summaries over copied chat text.

## Recommended digest shape

```md
# YYYY-MM-DD ChatGPT History Digest

## Scope

## Durable preferences

## Project context

## Decisions

## Open loops

## Agent handoff notes

## Unsafe to assume

## Next import steps
```
