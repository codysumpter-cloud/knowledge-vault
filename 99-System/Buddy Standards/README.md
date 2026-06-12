# Buddy Standards

Status: active
Owner: Prismtek / Buddy ecosystem
Last verified: 2026-06-12

## What was added

This folder is the durable KnowledgeVault home for the Buddy + Lil' Buddy default agent standard.

Files:

- `buddy-little-buddy-standard.md` - canonical role contract and lifecycle
- `prompt-routing-standard.md` - default prompt route and reusable system prompt
- `safety-review-standard.md` - Buddy Review gates and escalation classes
- `symphony-openmythos-integration-standard.md` - compatible orchestration, tool, guardrail, persona, memory, and world-model concepts

## Default future prompt route

```text
Human -> Buddy Orchestrator -> Lil' Buddy Worker(s) -> Buddy Review -> Human-facing response
```

Use this route unless the human explicitly disables it for the current task.

## Runtime demo

The local demo lives in `buddy-agent`:

```bash
buddy-demo "Draft a safe project note"
```

Equivalent checkout command:

```bash
python -m buddy_agent.orchestration.demo "Draft a safe project note"
```

The demo needs no paid API and no secrets.

## Repository ownership

- `knowledge-vault`: durable knowledge and standards
- `buddy-brain`: governance, policy, council routing, review rules
- `buddy-agent`: executable runtime scaffolds, schemas, and local demo
- `omni-buddy`: local embodied/device routing for voice, vision, sensors, and actions
