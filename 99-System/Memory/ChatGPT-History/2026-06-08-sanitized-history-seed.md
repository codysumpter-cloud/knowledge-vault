# 2026-06-08 ChatGPT History Digest

Status: generated summary
Visibility: public-safe seed
Source: available ChatGPT context and user-provided project direction

## Scope

This note seeds KnowledgeVault with a sanitized, durable summary of ChatGPT-derived project context for Prismtek, Buddy, BeMore, Hermes, and related workstreams.

It is **not** a raw transcript archive. It intentionally omits secrets, credentials, private operational details, local paths, and sensitive account information.

## Durable user preferences

- Preferred name: Prismtek.
- The user is a developer and builder focused on React/site migration, pixel games, creative tools, community features, AI-assisted workflows, and the Prismtek/Buddy/BeMore ecosystem.
- Preferred answers should be practical, concrete, friendly, and immediately useful.
- Clear and reliable beats clever and flashy.
- Maintainability, clean architecture, elegant UX, and shippable implementation matter.
- For simple tasks, concise answers are preferred.
- For complex tasks, include code, commands, diffs, steps, tradeoffs, verification, and blockers.
- Push back on unsafe, unreliable, or over-engineered approaches.

## Current project ecosystem

Core repos/projects repeatedly referenced in ChatGPT work:

- `buddy-agent` — guarded execution/runtime layer for Prismtek's agentic OS.
- `prismtek-apps` — iOS/macOS SwiftUI Buddy/BeMore companion app with Tamagotchi-style UX and TestFlight builds.
- `buddy-brain` — governance/operator/policy layer and BeMore stack continuity.
- `omni-buddy` — Raspberry Pi local multimodal prototype for voice, vision, local models, and TTS.
- `knowledge-vault` — durable project memory, context, runbooks, skill references, and agent-readable book layer.
- User fork of `hermes-agent` — active working agent base while Buddy-agent matures.

Current architecture direction:

- KnowledgeVault is the memory/book layer, not the runtime.
- Hermes-agent is the current active working agent system.
- Buddy-agent is intended to become the primary runtime.
- Buddy-brain remains continuity/governance until Buddy-agent fully owns that role.
- OpenClaw is retired for current work and should not be treated as active runtime, default toolchain, or product target.

## Agent operating model

The desired multi-agent flow:

1. Human gives intent to the Orchestrator.
2. Orchestrator, usually Buddy/Buddies, plans, preserves intent, and supervises.
3. Worker, usually Lil' Buddy/Lil' Buddies, executes steps autonomously.
4. Orchestrator reviews worker output.
5. If work is incomplete, Orchestrator reprompts the worker.
6. Dangerous or high-risk commands require human approval before proceeding.
7. The loop continues until done or blocked.

Minimum target: at least two agents per session — one orchestrator and one worker.

## Product direction

### Buddy / BeMore apps

Key desired app loop:

- create/customize Buddy
- train/care for Buddy
- chat/work with Buddy
- use Buddy as companion/operator for projects
- show memory, stats, skills, tasks, missions, receipts, and safe approvals

Important app priorities:

- local model support on-device
- cloud model selection
- tab customization
- rename/activation UX
- Buddy appearance customization
- ASCII/pixel/animation modes
- Pixel Studio integration
- Admin Mission Control
- ChatGPT/OpenAI account linking
- GitHub/Codex-style task UI with receipts

### Buddy appearance and sprite packs

The user wants Buddy asset packs, not just single generated images.

Preferred format:

- zipped sprite packs
- transparent backgrounds
- pixel art Tamagotchi/Pokemon-style look
- state frames
- animated GIF preview
- consistent high-quality treatment across states

States referenced:

- idle
- happy
- thinking
- working
- sleepy
- needs-attention
- level-up

## KnowledgeVault direction

KnowledgeVault should become the best possible human-and-agent-readable book for the Prismtek ecosystem.

High-value content types:

- source-of-truth dashboards
- repo maps
- project decisions
- handoff notes
- agent runbooks
- skill specs
- generated indexes
- public-safe context summaries
- reading paths

Current Wikipedia Knowledge Engine direction:

```txt
wikipedia-karpathy-wiki/
├── ingest/
│   ├── wikipedia_api_ingest.py
│   ├── dump_ingest.py
│   ├── concept_extractor.py
│   └── reading_path_generator.py
├── schemas/
├── generated/
├── indexes/
│   ├── concepts.json
│   ├── domains.json
│   └── redirects.json
└── prompts/
```

Expected deliverables:

- Wikipedia API ingestion
- dump ingestion
- concept-card generation
- domain-map generation
- redirects index
- reading path generation
- schema validation
- generated storage

## Known repo/PR workstreams

These items are included as public-safe operational memory, not as verified live GitHub status.

- `knowledge-vault` PR #5 was reported merged into main with merge commit beginning `1a8ba66`.
- `knowledge-vault` PR #6 was reported open and duplicate after PR #5 landed; intended cleanup was to close it as duplicate and build next phase from current main.
- `buddy-agent` PR #17 has been referenced as an active item needing checks/merge work.
- `prismtek-apps` PR #133 had a known blocker around `BuddyShortcutsProvider` declared twice.
- `prismtek-apps` PR #137 was also referenced as open.
- `knowledge-vault` daily maintenance / Vault Steward workflow has repeatedly failed on main and should be investigated with GitHub-visible receipts before making claims.
- `knowledge-vault` PR #8 review notes mention public-safety checks and a `00-Private/README.md` tracking/ignore issue.

## Game and creative-system workstreams

### PokeMMO / Pokemon-inspired systems

User has discussed:

- PokeMMO progression, Elite Four preparation, teams, breeding, EV/IV planning, GTL purchases, and region-specific teams.
- A Necesse/PokeMMO-style game idea where the battle engine matters most.
- Preference for real-time battles similar to Pokemon Legends Z-A direction, not only turn-based combat.
- Interest in public Pokemon-related projects and data sources, while avoiding unsafe/copyright-infringing asset or ROM handling.

Safety boundary:

- Do not store ROMs, copyrighted binaries, private client patches, cheats, bots, or automation payloads in KnowledgeVault.
- Store only public-safe design notes, legal data-source references, architecture notes, and original implementation plans.

### Pixel games / RG DS / ports

User is interested in:

- custom games for retro handhelds
- PortMaster-style deployment
- Linux/Android dual-boot handheld workflows
- simple game/app packaging that works directly from device storage

## Resume/job context

User has recently worked on a resume/cover letter for CPR Cell Phone Repair in Seymour, Indiana.

Relevant public-safe experience themes:

- building and upgrading PCs
- laptop/handheld disassembly and upgrades within safe tooling limits
- customer service
- B2B sales
- car wash membership sales
- electronics/e-cigarette retail management from 2014-2016
- business license and Indiana retail merchant permit
- Lenovo retailer setup without intent to compete with a repair employer

## Trading/finance safety note

The user has discussed paper trading, research loops, Alpaca paper trading, crypto monitoring, and trading-agent workflows.

Public-safe boundary:

- KnowledgeVault should not store credentials, account identifiers, API keys, live execution instructions, wallet details, or sensitive trading operational data.
- Public notes should frame trading material as research, simulation, education, or paper-trading architecture unless explicitly and safely scoped otherwise.

## Open loops for future agents

1. Build a real ChatGPT-history import pipeline:
   - accept exported ChatGPT data locally
   - parse conversations
   - classify by project/workstream
   - redact secrets and sensitive details
   - generate public-safe digests
   - optionally generate private local-only notes outside public Git

2. Add a vault-side schema for history digests:
   - date
   - source
   - visibility
   - confidence
   - projects touched
   - decisions
   - tasks
   - risks
   - links

3. Add a redaction scanner before committing generated ChatGPT digests.

4. Link relevant digest sections into project notes under `30 - Projects/GitHub/` only when the target note is public-safe.

5. Keep GitHub as source of truth for PR status, checks, merges, branches, and commit SHAs. Do not treat chat memory as authoritative for live repo state.

## Unsafe to assume

- Do not assume this digest contains the full ChatGPT history.
- Do not assume all remembered PR statuses are current.
- Do not assume private repo details are safe to publish.
- Do not assume a feature is implemented just because it was discussed.
- Do not store raw transcripts in this public repo.

## Next import steps

Recommended next implementation:

```txt
tools/chatgpt_history_importer/
├── README.md
├── import_chatgpt_export.py
├── redact.py
├── classify.py
├── render_digest.py
├── schemas/
│   └── chatgpt_history_digest.schema.json
└── tests/
    ├── test_redact.py
    ├── test_classify.py
    └── test_render_digest.py
```

The importer should produce candidate markdown files under this folder and require review before commit.
