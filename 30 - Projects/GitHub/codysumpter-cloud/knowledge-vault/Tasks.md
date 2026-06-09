---
type: project
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-09
risk_level: medium
privacy: public
freshness: volatile
agent_load: task-specific
tags:
  - tasks
  - knowledge-vault
  - agent-memory
---

# Tasks — knowledge-vault

> Current vault-side tasks for making KnowledgeVault more useful to humans and agents.

## Done

- [x] Add root README.
- [x] Add system map.
- [x] Add runbook.
- [x] Add backlog.
- [x] Add public safety policy.
- [x] Add vault doctor.
- [x] Position KnowledgeVault as an agent memory database.
- [x] Add agent database blueprint.
- [x] Add agent knowledge index.
- [x] Add note format standard.
- [x] Add record examples.
- [x] Add metadata schemas.
- [x] Add context bundle guide.
- [x] Add cold-start context bundle.
- [x] Add note quality linter.
- [x] Upgrade this repo's `Agent Context.md` from scaffold to useful context.
- [x] Add durable decisions for the June 2026 agent database direction.
- [x] Add runnable `memory_engine` Python package.
- [x] Add CLI commands for indexing, search, show, bundle export, Obsidian index generation, note creation, and local read-only serving.
- [x] Add Memory Engine guide and Obsidian integration guide.
- [x] Add default Memory Engine workspace documentation.
- [x] Add basic Memory Engine tests.
- [x] Add generated-output ignore rules.

## Next useful tasks

- [ ] Run `python3 "99-System/Automation/note_quality_linter.py"` locally and triage warnings.
- [ ] Run `python3 -m memory_engine index` locally and inspect generated outputs.
- [ ] Add a `vault-steward` context bundle.
- [ ] Add a `buddy-agent-maintainer` context bundle.
- [ ] Add a `prismtek-apps-maintainer` context bundle.
- [ ] Add a `public-alpha-reviewer` context bundle.
- [ ] Add a bundle export script that emits `bundle.md`, `manifest.json`, and receipt files from a manifest.
- [ ] Add richer graph/index exports connecting repos, decisions, skills, runbooks, and source packs.
- [ ] Upgrade high-priority generated repo notes from placeholders into verified briefs.
- [ ] Add or validate front matter on critical root and project docs.
- [ ] Promote skill notes into a maintained registry with explicit runtime status.
- [ ] Consider a future Obsidian plugin that wraps the CLI rather than replacing it.

## Agent instructions

When picking up this task list:

1. Prefer improvements that make the vault easier to retrieve and trust.
2. Do not rewrite broad swaths of human-authored content unless asked.
3. Upgrade one high-value area at a time.
4. Verify current repo state live before claiming PR, CI, branch, or release status.
5. Record durable decisions in `Decisions.md`.
