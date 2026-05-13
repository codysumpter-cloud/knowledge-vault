---
name: knowledge-vaulting
description: Design and maintain a centralized 'Knowledge Vault' for multi-project agent orchestration, moving from fragmented repos to a synthesized 'filing cabinet'.
---

# Knowledge Vaulting

Knowledge Vaulting is the process of transitioning from fragmented, raw information (individual wikis, repo READMEs, chat logs) to a centralized, synthesized knowledge base. This architecture transforms an agent from a 'file reader' into an 'architect' by providing a durable, cross-project source of truth.

## Trigger Conditions
- User has multiple related projects/repos with overlapping technical domains.
- Agent is experiencing 'context drift' or 'phantom' errors due to session compression.
- Large volumes of raw data (e.g., forked repos) need to be converted into actionable intelligence.
- The project requires 'Surgical' precision across multiple domains.

## The Workflow: Raw $\rightarrow$ Synthesis $\rightarrow$ Vault

### 1. Establish the Vault
Create a single, master repository (e.g., `knowledge-vault`) rather than separate wikis.
- **Structure:** Organize by 'Pillars' (e.g., `/infrastructure`, `/projects`, `/research`, `/entities`).
- **Philosophy:** The Vault is a 'Filing Cabinet', not a mirror of upstream docs.

### 2. The Ingestion Pipeline
Do not dump raw text. Follow the synthesis loop:
1. **Raw Ingest:** Capture the raw source (e.g., `curl` READMEs to `raw/` folder).
2. **Structural Audit:** Scan the raw data to identify 'Canonical Truths' vs. 'Temporal Logs'.
3. **Synthesis:** Create high-level 'Concept' or 'Entity' pages.
   - **Concept:** Theoretical frameworks, architecture, protocols (e.g., `[[omni-sync-protocol]]`).
   - **Entity:** Specific project targets, tools, or specifications (e.g., `[[eic-game-engine]]`).
4. **Linking:** Use wikilinks to create a knowledge graph. Link concepts across different pillars to enable cross-project synthesis.

### 3. State-Hardening (Combatting Session Compression)
Use the Vault as a 'Save Point' to prevent accuracy degradation during long sessions.
- **The Rule:** Any critical decision or architectural change must be committed to the Vault immediately.
- **The Ritual:** If session compression occurs, proactively reload the 'Product Map' or 'Architecture' pages to refresh the agent's active context with the lossless truth.
- **Memory Anchoring:** Use the `memory` tool for user-specific preferences (e.g., 'Surgical Operator' tone), and use the Vault for project-specific technical truth. This separates 'who the user is' from 'what the system is'.

## Pitfalls & Guardrails
- **The Wikipedia Trap:** Do NOT store general knowledge (e.g., 'what is a crab'). Store only the 'Secret Sauce'—project-specific, undocumented, or synthesized insights.
- **Identity Drift:** When rebranding projects or updating command syntax (e.g., moving from `BMO: /today` to `/today`), perform a vault-wide 'identity scrub' (regex replace) across all dashboards and runbooks to ensure documentation remains synchronized with the actual interface.
- **Shallow Wiki:** Avoid merely summarizing files. A perfect wiki provides a 'Tactical Recipe' or a 'Professional Playbook' that an agent can execute without further guidance.
- **Secret Leakage:** If credentials must be accessible from the vault, isolate them under a private folder such as `00-Private/Credentials/`, add explicit `.gitignore` rules, and verify with `git status --ignored` before any commit or push. For remote/VPS mirrors, sync operational docs separately and exclude private credential notes; deploy machine-readable secrets through dedicated files such as `~/.hermes/secrets/*.json` instead.
- **iCloud Path Assumptions:** On macOS, Obsidian+iCloud vaults can live under `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/`, not the generic `com~apple~CloudDocs` folder. For filesystem-first Obsidian work, use the `obsidian` skill and its iCloud reference.
- **Dirty Vault Handoffs:** If a handoff exists in GitHub but the local vault is dirty or behind, do not pull/checkout over user changes. Read the specific commit object and ingest from there; see `references/dirty-vault-handoff-ingestion.md`.

## Verification
- [ ] Is the information consolidated in a single vault?
- [ ] Is the data synthesized into concepts/entities rather than raw dumps?
- [ ] Does the vault provide a 'Product Map' that allows for cross-project reasoning?
- [ ] Can the agent recover its full state from the vault after a session reset?
