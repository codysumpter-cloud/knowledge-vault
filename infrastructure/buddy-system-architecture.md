---
title: Buddy System Architecture
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [buddy, architecture, runtime, agent]
sources: [buddy-brain/docs/BUDDY_SYSTEM.md, buddy-brain/contracts/buddy_runtime.md]
confidence: high
---

# Buddy System Architecture

The Buddy system is the core operational unit of the BeMore ecosystem. It separates the **definition** of an agent from its **execution**.

## 1. The Three-Layer Model
The system operates across three distinct layers of truth:
- **Canonical Truth (JSON/Schema):** Starter packs, progression rules, and creation constraints are stored in JSON. This is the machine-readable source of truth.
- **Runtime Execution (Buddy Runtime):** The engine that handles the `launch_task`, `submit_approval`, and session management. It is transport-neutral.
- **Continuity Layer (Markdown):** Human-readable summaries (`buddy.md`, `buddies.md`) that track the "soul" and progression of the agent.

## 2. The Buddy Lifecycle
- **Templates $\rightarrow$ Instances:** A "Buddy Template" is a sanitized, portable object. A "Buddy Instance" is a per-user, derived copy with unique memory and progression.
- **Execution Loop:**
  - **Launch:** `launch_task(goal, context, constraints)` $\rightarrow$ `session_id`.
  - **Interaction:** The runtime emits `tool_request` events.
  - **Supervision:** The Workbench (User/BMO) provides `submit_approval`.
  - **Completion:** `terminate_session` $\rightarrow$ `final_artifact`.

## 3. Governance and Safety
- **Approval Gating:** All risky or destructive actions must be gated by an approval event.
- **Safe Defaults:** If a request expires, the default decision for high-risk actions is `reject`.
- **State Ownership:** The Runtime owns the execution state; the Workbench owns the supervision state.

[[omni-buddy-sync-protocol]]
[[prismtek-product-map]]
