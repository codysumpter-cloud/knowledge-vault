---
name: agent-orchestration-design
description: "Design patterns for scaling human-agent collaboration from unit-control to swarm-simulation."
---

# Agent Orchestration Design

This skill governs the design and implementation of systems that manage multiple AI agents in parallel, focusing on raising the "human ceiling" by applying gaming mechanics to productivity.

## Core Philosophy: The Evolution of Control

The goal is to move the human role from a bottleneck (micro-managing units) to a "God Sim" (shaping the environment).

### 1. The RTS Era (Warcraft Style)
*   **Focus:** Direct unit control and visibility.
*   **Patterns:**
    *   **Physical Manifestation:** Agents visualized as units/icons rather than just text logs.
    *   **FileSystem Projection:** Mapping the codebase as a physical map (directories = regions, files = rooms).
    *   **Collision Detection:** Using heatmaps to visualize where agents are working to prevent merge conflicts.
    *   **Tactical Cycling:** Using hotkeys/muscle memory to quickly switch between agents requiring approval.

### 2. The God Sim Era (WorldBox Style)
*   **Focus:** Emergent behavior and environmental laws.
*   **Patterns:**
    *   **Quest-Based Agency:** Agents identify their own missions (e.g., "I found a bug in the auth flow") and present them as "Quests" for the human to trigger.
    *   **Campaigns:** High-level goals (e.g., "Implement Feature X") that the orchestrator decomposes into a swarm of autonomous tasks.
    *   **Review-Centric Workflow:** Shifting effort from *Planning* $\rightarrow$ *Execution* to *Execution* $\rightarrow$ *Review/Selection*. Generate multiple valid implementations and pick the best one.
    *   **Environmental Simulation:** Integrating the orchestration into a game world (e.g., WorldBox mod) where codebase health and agent progress are mirrored by the state of a simulated civilization.

## Implementation Guidelines

### Visualization
- **Avoid** long lists of status updates.
- **Prefer** spatial projections (maps, graphs, heatmaps) that allow the human to perceive state at a glance.

### Interaction
- **Minimize** the "babysitting" loop.
- **Implement** "Soft Collaboration" where agents notify humans and other agents of their intent to touch specific files before doing so.

### Safety & Boundaries
- **Observability First:** The HUD should be a "bridge" (observability), not the runtime authority.
- **Isolation:** Run autonomous campaigns in containers to prevent reckless agents from damaging the host environment.

## Pitfalls
- **The Orchestration Trap:** Adding more agents without adding a better orchestration UI just increases the human bottleneck.
- **Over-Planning:** Spending too much time on a perfect plan when the "WorldBox" approach suggests generating 5 variants and picking one.
