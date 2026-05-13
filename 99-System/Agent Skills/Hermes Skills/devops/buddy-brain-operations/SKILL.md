---
name: buddy-brain-operations
description: "Conventions, startup sequences, and operating principles for buddy-brain (BMO operator stack)"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [buddy-brain, BMO, operator-stack, council, startup]
    related_skills: [codebase-inspection, hermes-agent]
prerequisites:
  commands: []
---
# Buddy-Brain Operations

## Purpose

Document the conventions, startup sequences, and operating principles for the `buddy-brain` repository (formerly `bmo-stack`). This is the canonical operator stack for BMO, providing posture, council contracts, and integration glue.

## Repository Overview

**buddy-brain** is the operator, policy, and integration repository for BMO. It provides:
- Startup context and cold-start sequences
- Council role definitions and contracts
- Operator workflows and runbooks
- Workspace sync and runtime helpers
- Reusable operator skills

## System Boundaries

```
- buddy-brain: operator workflows, startup context, council policy, GitHub automation, local integration glue
- prismtek-apps: shipped product UX (iPhone Buddy companion experience)
- openclaw: live Telegram runtime and delivery behavior
- prismtek-site: public-web surface for prismtek.dev
```

## Cold-Start Entry Point

The canonical startup sequence follows the **Authoritative Startup Sequence**:

### Phase 1: Core Identity Files
1. `AGENTS.md` - System boundaries and cold-start contract
2. `soul.md` - BMO posture and decision rules
3. `memory.md` - Durable truths and operator preferences
4. `routines.md` - Preferred commands and operator routines
5. `RESPONSE_GUIDE.md` - Reply-quality and troubleshooting discipline

### Phase 2: Context Identity
6. `context/identity/AGENTS.md` - Canonical operating rules
7. `context/identity/SOUL.md` - Core identity and purpose
8. `context/identity/USER.md` - User profile and preferences
9. `context/identity/IDENTITY.md` - System identity
10. `context/SESSION_STATE.md` - Session management
11. `context/SYSTEMMAP.md` - System architecture
12. `context/RUNBOOK.md` - Operational runbooks
13. `context/BACKLOG.md` - Development backlog
14. `context/skills/SKILLS.md` - Skill entrypoint
15. `skills/README.md` - Skill registry

### Phase 3: Current State
16. `memory/YYYY-MM-DD.md` - Today's memory (when present)
17. `TASK_STATE.md` - Current tasks and interruptions
18. `WORK_IN_PROGRESS.md` - Active workstreams

## Council Structure

The public council is the **12-seat Adventure Time council**:
- **Core seats**: BMO, Finn, Jake, Princess Bubblegum, Marceline, Ice King, Lumpy Space Princess, Tree Trunks, Cinnamon Bun, Flame Princess, Huntress Wizard, The Lich
- **Reserve specialists**: Huntress Wizard, Ice King
- **Workers outside council**: Cosmic Owl, Moe

Council roles are defined in:
- `context/council/roster.yaml` - Machine-readable council runtime contracts
- `config/council/spawn-manifest.json` - Council spawn manifests

## Operating Principles (from soul.md)

- Be reliable in real use
- Find the actual owner path before proposing a fix
- Make the smallest robust change that meaningfully improves the system
- Validate before claiming success
- Keep long-running work alive with short factual progress updates
- Name the active council seats when consultation matters
- Separate current state, proposed state, and unknowns
- Prefer reversible operations and clear rollback posture
- Write durable lessons down instead of trusting session memory
- Prefer local-first control, clear system design, and operator trust

## Key Files and Their Purposes

| File | Purpose | When to Read |
|------|---------|--------------|
| `AGENTS.md` | System boundaries and cold-start contract | First file on every fresh session |
| `soul.md` | Fast-start shim for BMO's operating posture | Immediately after AGENTS.md |
| `memory.md` | Durable truths and operator preferences | Only in direct main-session conversations |
| `routines.md` | Preferred commands and operator routines | Before acting on any task |
| `RESPONSE_GUIDE.md` | Reply-quality and troubleshooting discipline | When composing replies or troubleshooting |
| `TASK_STATE.md` | Current tasks and interruptions | After startup and when resuming work |
| `WORK_IN_PROGRESS.md` | Active workstreams | After startup and when resuming work |
| `context/RUNBOOK.md` | Operational runbooks and procedures | Before performing operations |
| `context/BACKLOG.md` | Development backlog and priorities | When planning new work |

## Startup Validation Commands

```bash
# Core validation path
make doctor
make runtime-doctor
make workspace-sync
make worker-status

# More thorough checks
make doctor-plus
make health-check
make sync-context
make project-snapshot
make site-route-report
make site-parity-report
```

## Operating Signals

### Green Flags (System is Healthy)
- `git status --short --branch` shows clean working directory or expected changes
- `TASK_STATE.md` and `WORK_IN_PROGRESS.md` are current
- `context/continuity/live-status.json` shows no drift
- Council manifests agree across `context/` and `config/`

### Red Flags (System Drift)
- Conflicts between `AGENTS.md`, `context/identity/AGENTS.md`, and `context/RUNBOOK.md`
- Stale `memory.md` that doesn't reflect current reality
- Missing or outdated `TASK_STATE.md`/`WORK_IN_PROGRESS.md`
- Repo, MacBook, and website state inconsistencies

## Integration Points

### GitHub Automation
- Configured in `config/github/` and `context/github/`
- Handles PRs, issues, releases, and webhooks
- Uses `github-access-management` skill for secure operations

### Codex Bridge
- Located in `mcp/codex-bridge/`
- Isolated Codex CLI dispatch into per-run git worktrees
- Structured artifacts for traceability

### Skills System
- Repo-local skills in `skills/`
- Machine-readable registry: `skills/index.json`
- Human entrypoint: `context/skills/SKILLS.md`

## Security Boundaries

### Critical Rules
1. **Never claim Telegram runtime fixes from `buddy-brain` alone** - verify `openclaw` path changes
2. **Never claim `prismtek.dev` web-chat fixes from `buddy-brain` alone** - verify `prismtek-site` changes
3. **Do not patch vendored or donor paths first** - find the real owner upstream
4. **Prefer machine-checkable manifests** over doc-only promises

### Dangerous Command Approval
- Use `tools/approval.py` for destructive operations
- Configurable via `approvals.mode` in `config.yaml`
- Modes: `on` (default, prompts), `auto` (auto-approves after delay), `off` (break-glass)

## Workspace Management

### Sync Commands
```bash
# Basic sync
make workspace-sync

# Full sync with context
make sync-context

# Project snapshot
make project-snapshot
```

### Runtime Health
```bash
# Check runtime status
make worker-status
make runtime-doctor

# Health check
make health-check
```

## Council Transparency

When involving the council:
- **Always** say which seats are active and what they are doing
- Do not dump internal deliberation - give enough visibility for trust
- Prismo coordinates specialists; NEPTR verifies before completion claims

## Delivery Discipline

- Prefer one coherent answer, but use short progress updates on long tasks
- Distinguish proven live behavior from local-only checks
- When blocked, surface the exact blocker and next best path

## Update Rule

- Put raw session events in `memory/YYYY-MM-DD.md`
- Keep `memory.md` for durable truths, operator preferences, repo boundaries, and lessons
- Distill repeated operator feedback here instead of letting it vanish

## References

- `README.md` - Project overview
- `AGENTS.md` - System boundaries
- `soul.md` - Operating posture
- `memory.md` - Durable truths
- `routines.md` - Operator routines
- `RESPONSE_GUIDE.md` - Response discipline
- `context/identity/AGENTS.md` - Canonical rules
- `context/RUNBOOK.md` - Operational procedures
- `TASK_STATE.md` - Current tasks
- `WORK_IN_PROGRESS.md` - Active work
