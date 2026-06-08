# KnowledgeVault

KnowledgeVault is the public, agent-readable operating memory for Prismtek.

It is designed to be useful in two ways:

1. **For agents:** a durable source of context, decisions, project state, runbooks, skill indexes, and handoff instructions.
2. **For humans:** a navigable Obsidian vault that explains what the Prismtek/Buddy ecosystem is, what matters now, and where to go next.

GitHub remains the source of truth for code, issues, pull requests, CI state, and releases. KnowledgeVault is the source of truth for project memory: decisions, status, context, roadmaps, runbooks, handoffs, daily agent logs, and agent-facing operating rules.

## Current role in the Prismtek stack

KnowledgeVault is the memory/book layer for the Buddy and Hermes ecosystem.

- **Buddy-agent** is being prepared to become the primary execution/runtime repository.
- **Hermes-agent** is the current main working agent system.
- **Buddy-brain** remains continuity and memory context until Buddy-agent fully owns that role.
- **KnowledgeVault** remains the durable project-memory and agent-reference layer.
- **OpenClaw is retired** for current work and should not be used as the active runtime, default toolchain, or product target.

## Start here

| Need | Go here |
|---|---|
| Agent operating contract | [`AGENTS.md`](AGENTS.md) |
| Human/agent navigation map | [`SYSTEMMAP.md`](SYSTEMMAP.md) |
| Maintenance commands and workflows | [`RUNBOOK.md`](RUNBOOK.md) |
| Current improvement backlog | [`BACKLOG.md`](BACKLOG.md) |
| Public/private safety policy | [`SECURITY.md`](SECURITY.md) |
| Main project dashboard | [`01-Dashboard/Project Source of Truth.md`](01-Dashboard/Project%20Source%20of%20Truth.md) |
| GitHub repo index | [`30 - Projects/GitHub/GitHub Projects Index.md`](30%20-%20Projects/GitHub/GitHub%20Projects%20Index.md) |
| Vault Steward agent | [`99-System/Agents/Vault Steward/AGENT.md`](99-System/Agents/Vault%20Steward/AGENT.md) |
| Vault automation | [`99-System/Automation/README.md`](99-System/Automation/README.md) |
| Hermes/Buddy skill index | [`99-System/Agent Skills/Skill Index.md`](99-System/Agent%20Skills/Skill%20Index.md) |

## Repository map

```txt
.
├── AGENTS.md                         # Agent operating contract
├── README.md                         # Public repo front door
├── SYSTEMMAP.md                      # Human + agent navigation map
├── RUNBOOK.md                        # Safe operations guide
├── BACKLOG.md                        # Ranked improvement backlog
├── SECURITY.md                       # Public/private safety policy
├── 01-Dashboard/                     # Human-readable dashboards
├── 30 - Projects/GitHub/             # Project memory for GitHub repos
├── 99-System/Agents/                 # Agent specs, logs, and operating docs
├── 99-System/Automation/             # Vault Steward scripts and wrappers
├── 99-System/Agent Skills/           # Mirrored Hermes/Buddy skill material
├── 99-System/Repositories/           # Generated public repo registries
└── 00-Private/                       # Local-only/private material; ignored by Git
```

## What belongs here

Use KnowledgeVault for durable, reusable context:

- Project intent and status
- Architecture decisions
- Agent handoffs
- Runbooks
- Safe skill documentation
- Repo maps and indexes
- Human-readable dashboards
- Public-safe source references
- Generated summaries that are clearly marked

Do **not** use KnowledgeVault for:

- Secrets, tokens, cookies, certs, keys, passwords, or `.env` contents
- Private repo names while this repo is public
- Signed-in browser session details
- Local machine paths that expose sensitive identity or workspace state
- Raw vendored mirrors of large third-party datasets
- ROMs, copyrighted binaries, client patches, bots, cheats, or automation payloads

## Agent ingestion order

Agents should read these files before making claims about the vault or changing it:

1. [`README.md`](README.md)
2. [`AGENTS.md`](AGENTS.md)
3. [`SYSTEMMAP.md`](SYSTEMMAP.md)
4. [`RUNBOOK.md`](RUNBOOK.md)
5. [`BACKLOG.md`](BACKLOG.md)
6. [`SECURITY.md`](SECURITY.md)
7. [`01-Dashboard/Project Source of Truth.md`](01-Dashboard/Project%20Source%20of%20Truth.md)
8. [`30 - Projects/GitHub/GitHub Projects Index.md`](30%20-%20Projects/GitHub/GitHub%20Projects%20Index.md)
9. Relevant project notes under `30 - Projects/GitHub/codysumpter-cloud/`
10. Relevant skill notes under `99-System/Agent Skills/`

## Maintenance

Run the vault doctor first:

```bash
python3 "99-System/Automation/vault_doctor.py"
```

Run the Vault Steward locally:

```bash
"99-System/Automation/run-vault-maintenance.sh"
```

The daily GitHub Actions workflow runs the Vault Steward, runs the doctor, and commits only approved safe paths.

## Public safety model

This repo is public. Private memory is local-only by default.

- `00-Private/**` is ignored.
- `99-System/Security/**` is ignored.
- Secrets and credential-like filenames are ignored.
- Vault Steward should never use `git add .`.
- Private repo tracking must remain disabled unless the vault is made private.

See [`SECURITY.md`](SECURITY.md) for the full policy.

## Status

KnowledgeVault is active infrastructure for Prismtek. It is not a finished product runtime. Its job is to keep the broader Buddy/Hermes/Prismtek ecosystem understandable, recoverable, and easier for both humans and agents to operate.
