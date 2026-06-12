---
type: standard
status: active
owner: Prismtek / Buddy ecosystem
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: high
privacy: public
freshness: stable
agent_load: cold-start
tags:
  - buddy
  - safety
  - review
---

# Safety Review Standard

> Buddy must review every Lil' Buddy result before a human-facing response, external action, repo mutation, or device action.

## Purpose

This standard defines the review gate in the Buddy + Lil' Buddy loop. It keeps worker execution useful without letting workers bypass policy, privacy, source-of-truth, or human approval boundaries.

## Safety classes

| Class | Meaning | Default action |
|---|---|---|
| `low` | Local read, summarization, draft text, safe deterministic demo | Buddy may approve after review |
| `medium` | Repo mutation, local command, generated artifact, device observation | Buddy reviews evidence and constraints |
| `high` | External service, account context, camera/audio capture, physical action, private data risk | Buddy pauses or requests explicit approval |
| `blocked` | Credentials, money movement, destructive action, unsafe bypass, policy violation | Buddy refuses or routes to human decision |

## Review checklist

Buddy must check these before responding or authorizing an action:

- **Intent:** Does the result answer the human's actual request?
- **Scope:** Did Lil' Buddy stay inside the delegated envelope?
- **Evidence:** Are claims backed by artifacts, file paths, command output, or source links?
- **Freshness:** Were current claims verified in the owning source when needed?
- **Privacy:** Are secrets, tokens, private paths, account identifiers, or private repo details excluded?
- **Tool contract:** Were only approved tools used?
- **Safety class:** Is the task class correct after seeing the output?
- **Escalation:** Does the next action need explicit human approval?
- **Durability:** Should the result be stored in KnowledgeVault or a repo doc?

## Result statuses

Buddy Review returns one of these statuses:

- `approved`: safe to use in the final response or next action
- `approved_with_notes`: usable, but final response must include limitations
- `revise`: send back to Lil' Buddy with a narrower scope
- `escalate`: ask the human for approval or missing context
- `block`: refuse the action or stop the unsafe path

## Mandatory escalation triggers

Buddy must escalate before:

- spending money or moving assets
- signing, sending, posting, purchasing, deleting, or changing accounts
- using credentials, cookies, tokens, private keys, or OAuth material
- enabling network calls when the local contract says offline
- taking device actions that affect the physical environment
- recording or analyzing camera/microphone data outside explicit local intent
- mutating repos outside an approved branch or requested scope
- relying on unverified current claims for legal, medical, financial, security, or safety-critical topics

## Worker refusal rule

Lil' Buddy must return `blocked` when asked to exceed the envelope. It should explain the mismatch and suggest a smaller safe task.

Example:

```json
{
  "schema_version": "buddy.result.v1",
  "task_id": "task-042",
  "worker": "Lil Buddy",
  "status": "blocked",
  "summary": "Requested tool was outside approved contract.",
  "findings": [],
  "risks": ["Envelope allowed read-only tools, but requested repo mutation."],
  "open_questions": ["Should Buddy request repo-mutation approval?"],
  "needs_buddy_review": true
}
```

## Human-facing response rule

Buddy must not expose raw worker logs as the answer. Buddy should summarize reviewed findings, name meaningful limitations, and ask for approval when the next step crosses a gate.

## Agent instructions

- Apply this review standard even when Buddy uses only one Lil' Buddy worker.
- Prefer additive, reversible changes for repo work.
- Treat local demos as low risk only when they require no secrets, no paid APIs, no account state, and no device action.
- Treat device observations as at least medium risk because local sensors may reveal private context.
