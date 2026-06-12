---
type: standard
status: active
owner: Prismtek / Buddy ecosystem
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: stable
agent_load: cold-start
tags:
  - buddy
  - prompts
  - routing
---

# Prompt Routing Standard

> Default prompt routing rule for Buddy ecosystem work: Buddy owns intent, Lil' Buddy executes scoped work, Buddy reviews, then Buddy responds.

## Purpose

This note makes future prompts predictable across KnowledgeVault, Buddy Brain, Buddy Agent, and Omni Buddy.

Default route:

Human prompt or device event -> Buddy Orchestrator -> Lil' Buddy Worker(s) -> Buddy Review -> Human response or approved action

## Routing table

| Prompt or event type | Buddy responsibility | Lil' Buddy responsibility | Durable owner |
|---|---|---|---|
| Documentation update | Preserve intent, choose target docs, review wording | Draft scoped doc changes | KnowledgeVault or repo docs |
| Runtime implementation | Plan, define envelopes, review tests and safety | Implement focused code path | buddy-agent |
| Governance or policy | Apply existing Prismtek/Buddy rules | Summarize or draft constrained policy text | buddy-brain |
| Local voice/vision/device event | Classify intent and risk | Observe, transcribe, inspect, or prepare action | omni-buddy |
| Multi-agent narrative/world task | Maintain persona/world continuity | Produce scoped event, memory, or state update | KnowledgeVault + runtime memory |
| External or account action | Gate and request approval | Prepare draft or dry run only | Owning runtime after approval |

## Prompt handling sequence

1. **Classify:** Buddy identifies task type, risk, source-of-truth repo, and whether live verification is needed.
2. **Plan:** Buddy produces a short plan that names the worker task(s).
3. **Envelope:** Buddy sends each Lil' Buddy a task envelope with scope, constraints, tools, and expected output.
4. **Execute:** Lil' Buddy performs only the delegated work.
5. **Result:** Lil' Buddy returns a result envelope with artifacts, risks, and open questions.
6. **Review:** Buddy validates the result against the user intent and safety rules.
7. **Respond:** Buddy produces the final human-facing answer.
8. **Persist:** Buddy routes durable knowledge to KnowledgeVault and runtime contracts to the owning repo.

## Default prompt prefix

Use this reusable system prompt template when creating Buddy-compatible agents, tools, tasks, or docs:

```text
For every task, instantiate Buddy as orchestrator and at least one Lil' Buddy as worker.
Buddy must preserve the user's intent, create a short plan, delegate scoped work, review the result, apply safety/policy checks, and only then respond.
Lil' Buddy must execute only the delegated scope and return structured results.
Use knowledge-vault for durable knowledge, buddy-brain for governance, buddy-agent for runtime execution, and omni-buddy for local embodied/device integrations.
```

## Explicit disablement

The route can be disabled only for a specific task when the human explicitly says so. Examples:

- "Do this directly; do not delegate."
- "Skip Buddy/Lil' Buddy routing for this answer."
- "Use a single-agent answer for this prompt."

Disablement does not remove safety, privacy, or source-of-truth rules.

## Tool routing rules

- Knowledge reads go through KnowledgeVault paths or repo docs.
- Governance reads go through Buddy Brain policies, council docs, and prompt governance docs.
- Runtime execution goes through Buddy Agent contracts, CLI, schemas, and adapters.
- Local embodied actions go through Omni Buddy contracts and safety gates.
- Paid APIs, account actions, destructive changes, money movement, credentials, posting, or device control require explicit approval and a reviewed adapter.

## Agent instructions

- Apply this route by default for all future Buddy ecosystem prompts.
- If a prompt is tiny, Buddy may delegate a minimal synthetic Lil' Buddy check, but the review step still exists.
- Keep worker output structured enough to audit.
- Put user-facing prose only after Buddy Review.
