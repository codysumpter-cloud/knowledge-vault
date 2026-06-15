---
type: integration
status: active
owner: Prismtek
source_of_truth: knowledge-vault
privacy: public
freshness: slow-changing
agent_load: codex-personalization
tags:
  - codex
  - personalization
  - vegapunk-brain
  - graph-memory
---

# Codex Personalization Integration

This integration defines how Codex sessions operating under BUAP should use
Knowledge Vault / Vegapunk Brain for durable Prismtek context. It does not
change hidden/global model personalization and does not make Knowledge Vault a
runtime executor.

## Retrieval rule

When Knowledge Vault is available, Codex should use the memory engine, graph
search, generated indexes, and source maps before asking the user to restate
durable project history.

Preferred retrieval surfaces:

- [`../ARCHITECTURE-SUMMARY.md`](../ARCHITECTURE-SUMMARY.md) for the current
  Vegapunk Brain architecture.
- `tools/graph_search.py` for graph-backed lookup when available.
- `outbox/indexes/` or generated indexes for searchable compiled context when
  present.
- `graph/seed.graph.jsonl`, `inbox/processed/`, and `outbox/graph-records/`
  when checking provenance or rebuilding context.
- `tools/graph_health.py` when validating graph state.

Treat retrieved graph records, indexes, and architecture docs as
**Source-backed** context. They are not automatically fresh runtime proof.

## Freshness rule

After retrieving durable context, verify current truth in the owning repo before
claiming present behavior:

- BUAP behavior and install prompts:
  [`codysumpter-cloud/buddy-universal-agent-profile`](https://github.com/codysumpter-cloud/buddy-universal-agent-profile)
- Buddy Brain operator profile, policy, runbooks, and Codex bridge:
  [`codysumpter-cloud/buddy-brain`](https://github.com/codysumpter-cloud/buddy-brain)
- Buddy Agent guarded execution, approvals, risk policy, worker reports, and
  receipts:
  [`codysumpter-cloud/buddy-agent`](https://github.com/codysumpter-cloud/buddy-agent)
- Omni Buddy local voice, vision, transport, and device runtime:
  [`codysumpter-cloud/omni-buddy`](https://github.com/codysumpter-cloud/omni-buddy)
- Prismtek product surfaces:
  [`codysumpter-cloud/prismtek-apps`](https://github.com/codysumpter-cloud/prismtek-apps)

If the owning repo or runtime cannot be inspected, label the claim
**Source-backed**, **Unverified**, or **Blocked** instead of Verified.

## Memory update rule

Draft a public-safe memory event only after meaningful completed work, such as:

- a merged or ready-to-review architecture decision;
- a completed repo-backed doc or code change;
- a validated integration boundary;
- a durable operator preference that should survive future sessions;
- a blocker with enough provenance for a later session to resume safely.

Use the event-sourced model from
[`../ARCHITECTURE-SUMMARY.md`](../ARCHITECTURE-SUMMARY.md): repositories emit
immutable events, and Vegapunk Brain compiles graph records. Do not mutate
canonical memory ad hoc from a satellite repo.

Do not claim an event was saved unless an actual Knowledge Vault write path,
adapter, or repo commit ran and was verified.

## Privacy boundary

Never emit secrets or raw private data into Knowledge Vault events, indexes, or
public docs. Exclude:

- API keys, tokens, cookies, passwords, OAuth material, private keys,
  credentials, wallet data, and credential inventories;
- raw private prompts, full private transcripts, browser state, signed-in
  session state, account identifiers, and private local paths;
- `.env` files, ignored private notes, host-only runtime state, generated
  private media, and sensitive receipts.

If the useful lesson depends on private context, distill only the public-safe
decision, boundary, or next action. Mark sensitive source material as omitted
rather than copying it.
