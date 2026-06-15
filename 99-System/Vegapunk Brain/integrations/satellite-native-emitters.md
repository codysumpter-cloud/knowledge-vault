# Satellite Native Emitters Receiver Contract

## Status

This document defines the receiver expectations for Buddy ecosystem repos that want to emit native Knowledge Vault / Vegapunk Brain events.

Satellite emitters are **not complete** until each source repo has its own native code adapter or a reviewed adapter that produces sanitized, schema-valid event drafts. Specs alone define the contract; they do not prove that live emission exists.

BUAP remains the profile and routing layer. It can describe how agents route and behave, but it is not the runtime owner, receiver owner, or durable event source for these satellite records.

## Receiver source of truth

- Receiver repo: `codysumpter-cloud/knowledge-vault`
- Receiver system path: `99-System/Vegapunk Brain/`
- Event schema: `99-System/Vegapunk Brain/emitters/graph-event.schema.json`
- Intake inbox: `99-System/Vegapunk Brain/inbox/events/`
- Processed event path: `99-System/Vegapunk Brain/inbox/processed/`
- Compiled graph output: `99-System/Vegapunk Brain/outbox/graph-records/compiled.graph.jsonl`
- Search/index output: `99-System/Vegapunk Brain/outbox/indexes/`
- Health output: `99-System/Vegapunk Brain/outbox/health-report.json`

## Allowed satellite sources

The current `graph-event.schema.json` allows these `source` values:

- `buddy-agent`
- `buddy-brain`
- `omni-buddy`
- `prismtek-apps`
- `knowledge-vault`

This receiver contract covers the native satellite emitter specs for the Buddy ecosystem repos below.

| Source repo | Event source | Allowed event classes | Receiver notes |
| --- | --- | --- | --- |
| `codysumpter-cloud/buddy-agent` | `buddy-agent` | `task`, `system`, `decision`, `concept` | Guarded task/action/runtime receipts only. Public-alpha risk policy must be preserved. |
| `codysumpter-cloud/buddy-brain` | `buddy-brain` | `decision`, `system`, `task`, `concept` | Governance, policy, council, runbook, and cross-repo decisions. Durable governance decisions require human approval. |
| `codysumpter-cloud/omni-buddy` | `omni-buddy` | `system`, `task`, `repo`, `concept` | Local device/runtime/transport validation receipts. Live device state claims require actual receipts. |

## Required schema validation

Every satellite event draft must validate against:

```text
99-System/Vegapunk Brain/emitters/graph-event.schema.json
```

Minimum required fields:

- `event_id`
- `event_type`
- `source`
- `timestamp`
- `payload`

The source must match the schema's allowed source enum. The event type must match the schema's allowed `event_type` enum. Event-class labels such as `task`, `system`, `decision`, `repo`, and `concept` belong inside the event payload as public-safe metadata; they are not a replacement for the schema's `event_type` field.

## Public-safe summary requirement

Satellite emitters may emit **public-safe summaries only**.

Do not accept event drafts that include:

- secrets, credentials, tokens, private keys, cookies, OAuth material, or passwords;
- raw prompts, hidden reasoning, raw transcripts, browser sessions, or private document excerpts;
- private memory, sensitive operator context, account identifiers, or private local paths;
- private media data, camera/audio capture, local-network secrets, or unreviewed device identifiers;
- live account control details, money movement instructions, or denied high-risk action details beyond a sanitized denial receipt;
- unverifiable claims of runtime, repo, or device state without receipts.

Receiver-side review should prefer deletion/rejection over partial publication when sanitizer confidence is low.

## Intake path

Native satellite emission should follow this path:

```text
satellite repo
  → event draft
  → schema validation
  → 99-System/Vegapunk Brain/inbox/events/
  → event_ingestor
  → event_router
  → graph_compiler
  → graph_builder / compiled graph
  → indexes / search / health
```

Expanded operational flow:

1. The satellite repo creates a sanitized event draft from a reviewed receipt.
2. The satellite repo or reviewed adapter validates the draft against `graph-event.schema.json`.
3. The accepted draft is handed to Knowledge Vault intake, targeting `inbox/events/`.
4. `event_ingestor.py` validates and accepts events into `inbox/events/`.
5. `event_router.py` routes accepted events into `inbox/processed/<event_type>/`.
6. `graph_rebuilder.py` invokes `graph_compiler.py`, lints compiled event records, builds the compiled graph, and rebuilds indexes.
7. `graph_health.py` writes graph health output, and `graph_search.py` can query the compiled graph.

## Receiver invariants

Knowledge Vault must preserve these invariants:

- Event intake is append-safe and immutable; conflicting event IDs should be rejected rather than overwritten.
- Generated graph outputs are receiver-owned; satellite repos must not write directly to compiled graph output files.
- Event drafts must be sanitized before crossing repo boundaries.
- Receiver validation must reject schema-invalid events.
- Receiver docs must distinguish implementation specs from live adapters.
- Human-approved governance events must retain approval metadata in public-safe form.
- Device/runtime events must state whether receipts are verified, partially verified, simulated, stale, or unverified.

## Satellite readiness checklist

A satellite emitter is ready only when all of the following are true:

- The owning repo has a native emitter spec.
- The owning repo has native code or a reviewed adapter for event drafting.
- The adapter validates against `graph-event.schema.json`.
- The adapter has sanitizer tests for the source repo's sensitive data classes.
- The adapter writes to the approved intake path and never mutates compiled graph outputs directly.
- The receiver has validated at least one public-safe sample receipt from the source repo.
- The PR or release note clearly documents Summary, Validation, Risk, and Rollback.

## Current implementation boundary

As of this contract, the satellite emitter work is docs/spec-level unless a source repo separately lands native code or a reviewed adapter. Do not claim complete native Knowledge Vault emission for Buddy Agent, Buddy Brain, or Omni Buddy until implementation and validation receipts exist.
