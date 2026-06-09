# KnowledgeVault

KnowledgeVault is Prismtek's public **agent memory database** and human-readable operating book.

It exists so a fresh human, Buddy, Hermes, or future agent can quickly answer:

- What is this ecosystem?
- Which repos matter?
- What decisions have already been made?
- What is safe to assume?
- What is still unknown, stale, or risky?
- Which source should be checked before acting?
- What context bundle should an agent load for this task?

GitHub remains the source of truth for code, issues, pull requests, CI state, and releases. KnowledgeVault is the source of truth for durable project memory: decisions, status, context, roadmaps, runbooks, handoffs, daily agent logs, and agent-facing operating rules.

## What this repo is

KnowledgeVault is not just notes. Treat it as a small, public-safe database for agents.

| Layer | Purpose |
|---|---|
| **Book** | Human-readable explanations, maps, and dashboards. |
| **Memory** | Durable decisions, project state, status, and handoffs. |
| **Index** | Repo maps, skill registries, source maps, and generated dashboards. |
| **Retrieval substrate** | Curated context that agents can load by task without swallowing the whole vault. |
| **Quality system** | Schemas, standards, examples, bundles, and lint checks that keep notes useful. |
| **Safety boundary** | Public/private rules, source-of-truth rules, and claim-status rules. |

The best version of this repo is a **trusted operating memory**: easy for humans to browse, strict enough for automation, and structured enough for agents to retrieve only the right context.

## Current role in the Prismtek stack

KnowledgeVault is the memory/book/database layer for the Buddy and Hermes ecosystem.

- **Buddy-agent** is being prepared to become the primary execution/runtime repository.
- **Hermes-agent** is the current main working agent system.
- **Buddy-brain** remains continuity and memory context until Buddy-agent fully owns that role.
- **KnowledgeVault** remains the durable project-memory and agent-reference layer.
- **OpenClaw is retired** for current work and should not be used as the active runtime, default toolchain, or product target.

## Start here

| Need | Go here |
|---|---|
| Agent operating contract | [`AGENTS.md`](AGENTS.md) |
| Agent knowledge index | [`AGENT_KNOWLEDGE_INDEX.md`](AGENT_KNOWLEDGE_INDEX.md) |
| Human/agent navigation map | [`SYSTEMMAP.md`](SYSTEMMAP.md) |
| Agent database north-star design | [`AGENT_DATABASE_BLUEPRINT.md`](AGENT_DATABASE_BLUEPRINT.md) |
| Cold-start context bundle | [`99-System/Context Bundles/cold-start/bundle.md`](99-System/Context%20Bundles/cold-start/bundle.md) |
| Note format standard | [`99-System/Standards/NOTE_FORMAT_STANDARD.md`](99-System/Standards/NOTE_FORMAT_STANDARD.md) |
| Record examples | [`99-System/Standards/RECORD_EXAMPLES.md`](99-System/Standards/RECORD_EXAMPLES.md) |
| Metadata schemas | [`99-System/Schemas/`](99-System/Schemas/) |
| Note quality linter | [`99-System/Automation/NOTE_QUALITY_LINTER.md`](99-System/Automation/NOTE_QUALITY_LINTER.md) |
| Maintenance commands and workflows | [`RUNBOOK.md`](RUNBOOK.md) |
| Current improvement backlog | [`BACKLOG.md`](BACKLOG.md) |
| Public/private safety policy | [`SECURITY.md`](SECURITY.md) |
| Main project dashboard | [`01-Dashboard/Project Source of Truth.md`](01-Dashboard/Project%20Source%20of%20Truth.md) |
| GitHub repo index | [`30 - Projects/GitHub/GitHub Projects Index.md`](30%20-%20Projects/GitHub/GitHub%20Projects%20Index.md) |
| Vault Steward agent | [`99-System/Agents/Vault Steward/AGENT.md`](99-System/Agents/Vault%20Steward/AGENT.md) |
| Vault automation | [`99-System/Automation/README.md`](99-System/Automation/README.md) |
| Hermes/Buddy skill index | [`99-System/Agent Skills/Skill Index.md`](99-System/Agent%20Skills/Skill%20Index.md) |
| Wikipedia knowledge pack | [`99-System/Agent Skills/Hermes Skills/reference/wikipedia-karpathy-wiki/README.md`](99-System/Agent%20Skills/Hermes%20Skills/reference/wikipedia-karpathy-wiki/README.md) |

## Repository map

```txt
.
├── README.md                         # Public repo front door
├── AGENTS.md                         # Agent operating contract
├── AGENT_KNOWLEDGE_INDEX.md          # Agent task-routing index
├── AGENT_DATABASE_BLUEPRINT.md       # North-star design for agent-grade memory
├── SYSTEMMAP.md                      # Human + agent navigation map
├── RUNBOOK.md                        # Safe operations guide
├── BACKLOG.md                        # Ranked improvement backlog
├── SECURITY.md                       # Public/private safety policy
├── 01-Dashboard/                     # Human-readable dashboards
├── 30 - Projects/GitHub/             # Project memory for GitHub repos
├── 99-System/Agents/                 # Agent specs, logs, and operating docs
├── 99-System/Automation/             # Vault Steward scripts and quality checks
├── 99-System/Context Bundles/        # Curated context bundles for agents
├── 99-System/Standards/              # Formatting and record standards
├── 99-System/Schemas/                # Machine-readable schemas
├── 99-System/Agent Skills/           # Mirrored Hermes/Buddy skill material
├── 99-System/Repositories/           # Generated public repo registries
└── 00-Private/                       # Local-only/private material; ignored by Git
```

## What makes this useful for AI agents

An agent database should not be a pile of markdown. It should be predictable, scoped, source-linked, and safe to query.

KnowledgeVault should optimize for these properties:

1. **Cold-start orientation** — a new agent can read a short path and understand the system.
2. **Source-of-truth clarity** — every note says whether GitHub, the vault, a runtime repo, or an external source is authoritative.
3. **Provenance** — claims point to repos, PRs, files, source articles, generated manifests, or explicit human decisions.
4. **Freshness** — volatile or high-stakes claims carry last-verified dates and refresh expectations.
5. **Claim status** — references, drafts, wired features, tested features, and disabled features are not blurred together.
6. **Task routing** — agents know which folder or file to inspect for each class of request.
7. **Retrieval discipline** — agents should load curated bundles, not blindly ingest the full vault.
8. **Formatting discipline** — notes follow predictable metadata and section patterns.
9. **Public safety** — private operational details stay out of tracked public files.

## Agent database model

KnowledgeVault stores four kinds of records.

| Record type | Examples | Agent use |
|---|---|---|
| **Project records** | `Project.md`, `Agent Context.md`, `Decisions.md`, `Tasks.md` | Repo status, verification commands, known risks, next action. |
| **Operating records** | `AGENTS.md`, `RUNBOOK.md`, `SECURITY.md`, agent specs | Safe behavior, maintenance, boundaries, escalation rules. |
| **Index records** | repo registry, skill registry, dashboards, system map, knowledge index | Fast routing, search, summarization, task planning. |
| **Knowledge records** | skill notes, source maps, Wikipedia concept cards, runbooks | Reusable background knowledge and learning paths. |

A good record should be:

- **Skimmable:** headings explain the shape before details.
- **Durable:** useful weeks later without chat context.
- **Grounded:** links to source repos, PRs, issues, files, or source articles when possible.
- **Actionable:** tells the next human or agent what to do next.
- **Scoped:** says what is known, unknown, stale, risky, and unsafe to assume.
- **Public-safe:** contains no private operational details.
- **Retrieval-friendly:** small and structured enough for task-specific loading.

## Minimum note contract

Prefer this shape for durable notes:

```yaml
---
type: project | decision | runbook | skill | source | dashboard | handoff | index | bundle
status: reference | draft | active | wired | tested | stale | disabled
owner: Prismtek
source_of_truth: github | knowledge-vault | runtime-repo | external-source | mixed
last_verified: YYYY-MM-DD
risk_level: low | medium | high
privacy: public
freshness: stable | slow-changing | volatile | high-stakes
agent_load: cold-start | task-specific | reference-only | never-auto-load
tags: []
---
```

Then include:

1. **Purpose** — why this note exists.
2. **Current state** — what is true now.
3. **Source links** — where claims came from.
4. **Known unknowns** — what must be checked before acting.
5. **Next action** — the smallest useful next step.
6. **Agent instructions** — how an agent should use or avoid the note.

See [`99-System/Standards/NOTE_FORMAT_STANDARD.md`](99-System/Standards/NOTE_FORMAT_STANDARD.md) and [`99-System/Standards/RECORD_EXAMPLES.md`](99-System/Standards/RECORD_EXAMPLES.md).

## Agent ingestion order

Agents should read these files before making claims about the vault or changing it:

1. [`README.md`](README.md)
2. [`AGENTS.md`](AGENTS.md)
3. [`SYSTEMMAP.md`](SYSTEMMAP.md)
4. [`AGENT_KNOWLEDGE_INDEX.md`](AGENT_KNOWLEDGE_INDEX.md)
5. [`AGENT_DATABASE_BLUEPRINT.md`](AGENT_DATABASE_BLUEPRINT.md)
6. [`99-System/Context Bundles/cold-start/bundle.md`](99-System/Context%20Bundles/cold-start/bundle.md)
7. [`99-System/Standards/NOTE_FORMAT_STANDARD.md`](99-System/Standards/NOTE_FORMAT_STANDARD.md)
8. [`RUNBOOK.md`](RUNBOOK.md)
9. [`BACKLOG.md`](BACKLOG.md)
10. [`SECURITY.md`](SECURITY.md)
11. [`01-Dashboard/Project Source of Truth.md`](01-Dashboard/Project%20Source%20of%20Truth.md)
12. [`30 - Projects/GitHub/GitHub Projects Index.md`](30%20-%20Projects/GitHub/GitHub%20Projects%20Index.md)
13. Relevant project notes under `30 - Projects/GitHub/codysumpter-cloud/`
14. Relevant skill notes under `99-System/Agent Skills/`
15. Task-specific context bundles under `99-System/Context Bundles/`.

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
- Retrieval-ready context packs
- Agent bootstrap instructions
- Concept cards and source-guided learning paths

Do **not** use KnowledgeVault for private credentials, private repo details while this repo is public, signed-in browser/session material, sensitive local workspace paths, raw vendored mirrors of large third-party datasets, copyrighted binaries, client patches, bots, cheats, automation payloads, or unverified claims that a skill is wired/tested/active in a runtime repo.

## Maintenance

Run the vault doctor first:

```bash
python3 "99-System/Automation/vault_doctor.py"
```

Run the note quality linter:

```bash
python3 "99-System/Automation/note_quality_linter.py"
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
- Credential-like filenames are ignored.
- Vault Steward should never use broad repository-wide staging.
- Private repo tracking must remain disabled unless the vault is made private.
- Any deeper operating memory should live in a private companion vault or in local-only ignored paths.

See [`SECURITY.md`](SECURITY.md) for the full policy.

## Roadmap to “best agent database”

The north star is not “more notes.” The north star is **trustworthy retrieval**.

Near-term upgrades:

1. Add front matter to critical notes.
2. Run quality linting and triage warnings.
3. Upgrade generated repo scaffolds into useful briefs.
4. Promote skill notes into a structured registry with explicit runtime status.
5. Generate task-specific bootstrap packs.
6. Export curated context bundles for Buddy-agent.
7. Keep public and private memory separated before storing deeper operational context.
8. Add receipts so agents can say which vault files or bundles influenced an answer.

See [`AGENT_DATABASE_BLUEPRINT.md`](AGENT_DATABASE_BLUEPRINT.md), [`AGENT_KNOWLEDGE_INDEX.md`](AGENT_KNOWLEDGE_INDEX.md), and [`BACKLOG.md`](BACKLOG.md) for the implementation path.

## Status

KnowledgeVault is active infrastructure for Prismtek. It is not a finished product runtime. Its job is to keep the broader Buddy/Hermes/Prismtek ecosystem understandable, recoverable, and easier for both humans and agents to operate.
