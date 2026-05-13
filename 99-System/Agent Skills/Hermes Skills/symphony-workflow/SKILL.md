---
title: Symphony Workflow
description: Implement isolated, autonomous implementation runs with Proof of Work.
category: software-development
---

# Symphony Workflow

## Goal
Transform a request into a verified, autonomous implementation run.

## Steps
1. **Isolation**: Spawn a sub-agent (Buddy) for a specific, isolated task.
2. **Execution**: The Buddy performs the work (code, config, research).
3. **Proof of Work**: The Buddy must provide a durable link or verifiable result (e.g., a GitHub PR, a CI pass log, or a file path).
4. **Surgical Review**: The Lead Operator reviews the Proof of Work against the original spec.
5. **Acceptance**: Only after verification is the task marked as "Completed."

## Pitfalls
- Do not accept "I have finished the task" as a result.
- Demand the "Receipt" (the Proof of Work).
