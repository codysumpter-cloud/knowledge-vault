---
type: dashboard
scope: project-source-of-truth
last_synced: 2026-05-13
tags:
  - dashboard
  - projects
---

# Project Source of Truth

This dashboard is the front door for Prismtek project memory.

## Operating rule

- GitHub = source of truth for code.
- Obsidian = source of truth for project memory, decisions, agent context, and daily status.
- Private project memory stays in `00-Private/` while the vault repo is public.

## Public GitHub projects

```dataview
TABLE status, priority, default_branch, github_url, last_synced
FROM "30 - Projects/GitHub/codysumpter-cloud"
WHERE type = "github-repo"
SORT repo_name ASC
```

## Needs triage

```dataview
TASK
FROM "30 - Projects/GitHub/codysumpter-cloud"
WHERE !completed
GROUP BY file.link
```

## Agent operations

- [[99-System/Agents/Vault Steward/AGENT|Vault Steward Agent]]
- [[99-System/Automation/README|Vault Automation]]
- [[30 - Projects/GitHub/GitHub Projects Index|GitHub Projects Index]]

---

## 2026-05-13 agent direction update

OpenClaw is retired for current work. It should not be used as an active runtime, default toolchain, product target, or implementation path.

Hermes-agent is the current main working agent system.

Buddy-agent is being prepared to become the primary and eventually only agent repository.

KnowledgeVault / Obsidian remains the source of truth for project memory, decisions, daily notes, handoffs, and agent context.

