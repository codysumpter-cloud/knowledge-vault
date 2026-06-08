---
type: github-repo
repo: codysumpter-cloud/knowledge-vault
repo_name: knowledge-vault
owner: codysumpter-cloud
visibility: public
default_branch: main
github_url: https://github.com/codysumpter-cloud/knowledge-vault
clone_url: https://github.com/codysumpter-cloud/knowledge-vault.git
status: Active infrastructure
priority: Critical
source_of_truth: vault-project-memory
code_source: github
agent_owner: Vault Steward
last_synced: 2026-06-04
tags:
  - github/repo
  - project
  - visibility/public
  - prismtek/memory-layer
---

# knowledge-vault

> Public, agent-readable operating memory for Prismtek. GitHub is the source of truth for source code; this note is the source of truth for project context, decisions, status, and agent handoffs.

## Links

- GitHub: https://github.com/codysumpter-cloud/knowledge-vault
- Clone: `https://github.com/codysumpter-cloud/knowledge-vault.git`
- Default branch: `main`
- Visibility: `public`
- Root guide: `README.md`
- Agent contract: `AGENTS.md`
- System map: `SYSTEMMAP.md`
- Runbook: `RUNBOOK.md`
- Backlog: `BACKLOG.md`
- Security policy: `SECURITY.md`

## Current status

- Status: Active infrastructure
- Priority: Critical
- Owner: Prismtek
- Agent owner: Vault Steward
- Last verified: 2026-06-04

## Project intent

KnowledgeVault is the durable book and memory layer for the Prismtek, Buddy, and Hermes ecosystem. It exists so a human or agent can quickly understand:

- what projects exist
- which repo owns code vs memory
- what decisions have already been made
- what skills and runbooks are available
- what the current agent and runtime direction is
- what is safe to publish and what must remain local-only

It is not the execution runtime. Buddy-agent is the intended primary runtime. KnowledgeVault is the navigable reference and continuity layer.

## Source-of-truth rule

- GitHub repositories own code, issues, pull requests, CI state, and releases.
- KnowledgeVault owns project memory, durable decisions, runbooks, context, dashboards, and agent handoffs.
- Private operational memory must stay out of public tracked files.

## Current known state

- The vault is public.
- Public project memory lives under `30 - Projects/GitHub/codysumpter-cloud/`.
- Local-only memory is expected under `00-Private/` and ignored by Git.
- Vault Steward automation refreshes repo folders, indexes, registries, and logs.
- `vault_doctor.py` checks public-safety hazards before daily automation commits.
- Root docs provide a human and agent reading path.

## Agent context

Agents working on this repo should:

1. Read `README.md` first.
2. Read `AGENTS.md`, `SYSTEMMAP.md`, `RUNBOOK.md`, `BACKLOG.md`, and `SECURITY.md`.
3. Check GitHub issues and PRs before changing code or docs.
4. Preserve human-authored content unless explicitly asked to rewrite it.
5. Use additive updates where possible.
6. Run or account for `python3 "99-System/Automation/vault_doctor.py"` before publishing changes.
7. Avoid claiming runtime capabilities unless they are verified in the relevant runtime repo.

## Maintenance commands

```bash
python3 "99-System/Automation/vault_doctor.py"
"99-System/Automation/run-vault-maintenance.sh"
```

## Risks

- Public/private leakage if local-only notes are tracked.
- False capability claims if skill notes are confused with wired runtime features.
- Generated scaffolds becoming stale if not upgraded into real project briefs.
- Obsidian convenience files accidentally entering Git.

## Next actions

- [x] Add root README.
- [x] Add system map.
- [x] Add runbook.
- [x] Add backlog.
- [x] Add public safety policy.
- [x] Add vault doctor.
- [x] Remove forbidden security path from daily workflow staging.
- [ ] Add structured skill registry with status/risk metadata.
- [ ] Generate daily repo health dashboards.
- [ ] Upgrade high-priority repo notes from generated scaffolds to verified briefs.

## Decisions

### 2026-06-04 — Treat KnowledgeVault as active Prismtek infrastructure

**Decision:** KnowledgeVault is active critical infrastructure, not a triage placeholder.

**Why:** It is the durable operating memory and navigation layer for Prismtek/Buddy/Hermes work.

**Scope:** Root docs, project status, automation safety, and future agent ingestion.

**Owner:** Prismtek / Vault Steward

---

## 2026-05-13 agent direction update

OpenClaw is retired for current work. It should not be used as an active runtime, default toolchain, product target, or implementation path.

Hermes-agent is the current main working agent system.

Buddy-agent is being prepared to become the primary and eventually only agent repository.

KnowledgeVault / Obsidian remains the source of truth for project memory, decisions, daily notes, handoffs, and agent context.
