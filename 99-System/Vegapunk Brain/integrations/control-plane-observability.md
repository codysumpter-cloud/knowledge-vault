# AgentRQ and Monocle Receiver Contract

Status: spec-only receiver contract  
Owner repo: `codysumpter-cloud/knowledge-vault`  
System path: `99-System/Vegapunk Brain/`  
Related satellite repos: `buddy-agent`, `buddy-brain`, `omni-buddy`  
Reference systems: AgentRQ, Monocle

## Purpose

Knowledge Vault / Vegapunk Brain is the durable memory and graph receiver for the Buddy ecosystem.

This document defines how events derived from AgentRQ task/control-plane state and Monocle observability traces may enter the Knowledge Vault safely.

The rule is simple:

> Raw control-plane data and raw observability traces stay private. Knowledge Vault receives sanitized receipts only.

## Source roles

| Source | External inspiration | What may be received |
| --- | --- | --- |
| `buddy-agent` | AgentRQ task lifecycle, Monocle execution traces | sanitized task/runtime receipts |
| `buddy-brain` | policy and approval governance | sanitized decision/system/concept receipts |
| `omni-buddy` | AgentRQ-style supervisor orchestration | sanitized cross-workspace coordination receipts |

## AgentRQ-derived receipts

AgentRQ-like task systems may produce useful memory events when a Buddy task:

- starts
- changes status
- becomes blocked
- requests approval
- receives approval
- receives denial
- completes
- is reassigned
- links to a public PR/issue/task reference

Knowledge Vault may receive only high-level facts such as:

```json
{
  "source": "buddy-agent",
  "event_class": "task",
  "title": "Completed AgentRQ-backed Buddy task",
  "summary": "Buddy Agent completed an operator-assigned task and recorded validation status.",
  "control_plane": {
    "provider": "agentrq",
    "workspace_alias": "buddy-agent-runtime",
    "task_status": "completed",
    "approval_outcome": "not_required"
  }
}
```

Knowledge Vault must reject or quarantine receipts containing:

- tokenized MCP URLs
- OAuth tokens
- bearer tokens
- raw task chat logs
- private workspace IDs unless intentionally public
- task attachments
- hidden operator notes
- unredacted user IDs, tenant IDs, or session IDs

## Monocle-derived receipts

Monocle-like tracing systems may produce useful memory events when an agent run:

- completes validation
- fails validation
- calls an expected tool
- avoids a forbidden tool
- hits an error class
- exceeds a duration or token budget
- produces a sanitized trace summary

Knowledge Vault may receive only summarized observability evidence:

```json
{
  "source": "buddy-agent",
  "event_class": "system",
  "title": "Monocle trace assertions passed",
  "summary": "A Buddy Agent workflow completed with trace-based validation and no durable private fields emitted.",
  "observability": {
    "provider": "monocle",
    "workflow": "repo-docs-integration",
    "raw_trace_exported": false,
    "assertions": [
      "expected_tool_categories_observed",
      "forbidden_tool_categories_absent",
      "no_secrets_emitted"
    ]
  }
}
```

Knowledge Vault must reject or quarantine receipts containing:

- raw OpenTelemetry spans
- prompts
- full model outputs
- tool arguments
- tool outputs
- local paths
- browser/session state
- stack traces with private paths
- credentials, headers, cookies, API keys
- raw vector search results that expose private data

## Intake policy

All AgentRQ/Monocle-derived events must pass the same intake path as native satellite events:

```text
satellite adapter
  → sanitized event draft
  → graph-event.schema.json validation
  → inbox/events
  → event_ingestor.py
  → event_router.py
  → graph_compiler.py
  → graph/index/search/health outputs
```

The receiver must treat every event as untrusted until validation and redaction checks pass.

## Required receipt fields

Every derived receipt should include:

- `source`
- `event_class`
- `title`
- `summary`
- `created_at` or equivalent event timestamp
- public-safe task/reference alias when available
- redaction status
- validation status
- raw trace/control-plane storage status

Recommended extensions:

```json
{
  "control_plane": {
    "provider": "agentrq",
    "workspace_alias": "public-safe-alias",
    "task_status": "completed",
    "approval_required": false,
    "approval_outcome": "not_required"
  },
  "observability": {
    "provider": "monocle",
    "workflow": "safe-workflow-name",
    "trace_ref": "private-or-redacted",
    "raw_trace_exported": false,
    "assertions": []
  },
  "redaction": {
    "tokens": "excluded",
    "raw_prompts": "excluded",
    "private_paths": "excluded",
    "raw_traces": "excluded"
  }
}
```

## Quarantine rules

Events should be quarantined instead of ingested when they contain:

- obvious secrets
- tokenized URLs
- raw prompts
- raw trace spans
- raw task chat transcripts
- private file paths
- browser session data
- credentialed request/response payloads
- attachment content
- unredacted user or tenant identifiers

Quarantine records should include only enough metadata to debug the failed intake safely.

## Durable memory stance

Knowledge Vault can remember:

- what happened
- who/which agent owned the task
- whether approval was required
- whether approval was granted or denied
- which validation class passed or failed
- which public PR/issue/task reference was involved
- which adapter class produced the receipt

Knowledge Vault must not remember:

- private runtime content
- raw control-plane messages
- raw traces
- secrets
- private local environment details
- private operator conversation content

## Implementation status

Current status: spec-only.

Knowledge Vault is not AgentRQ-native or Monocle-native until there is a reviewed adapter and receiver validation path that proves:

- schema compliance
- redaction compliance
- quarantine behavior
- no raw trace ingestion
- no raw prompt ingestion
- no secret ingestion
- safe rollback behavior
