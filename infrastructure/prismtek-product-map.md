---
title: Prismtek Product Map
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [prismtek, product, architecture, map]
sources: [bmo-stack/README.md, omni-bmo/README.md, prismtek-apps/README.md]
confidence: medium
---

# Prismtek Product Map

This map defines the relationship between the different components of the Prismtek ecosystem.

## 1. The Brain (Omni-BMO)
The core intelligence and orchestration layer.
- **Role:** Manages agent logic, session continuity, and the high-level "Council" of personas.
- **Transport:** Uses the Omni-BMO Sync Protocol to communicate across networks.

## 2. The Operator Stack (BMO-Stack)
The toolkit and environment used to manage the brain.
- **Role:** Provides the `worldboxctl`-style CLI tools, the session management logic, and the project-specific context.
- **Relationship:** BMO-Stack is the "harness" that drives the Omni-BMO brain.

## 3. The Product Surface (Prismtek-Apps & Site)
The user-facing interface.
- **Prismtek-Apps:** The native iOS/macOS experience (e.g., BeMore Agent).
- **Prismtek-Site:** The web-based dashboard and public-facing identity.
- **Relationship:** These consume the results of the BMO-Stack/Omni-BMO operations via a unified API.

## 4. The Modding Wing (Everything is Crab / WorldBox)
The specialized application of the stack to third-party games.
- **Execution:** Uses the Buddy System to spawn "Game Buddies" that interact with the game via bridge mods.
- **Knowledge:** Powered by the Knowledge Vault.

[[buddy-system-architecture]]
[[omni-bmo-sync-protocol]]
