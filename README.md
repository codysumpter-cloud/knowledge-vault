# KnowledgeVault

KnowledgeVault is Prismtek's public **agent memory database**, human-readable operating book, and now the home of **Vegapunk Brain (Punk Records)** — an event-sourced shared-memory platform for the Buddy ecosystem.

It exists so a fresh human, Buddy, Hermes, or future agent can quickly answer:

- What is this ecosystem?
- Which repos matter?
- What decisions have already been made?
- What is safe to assume?
- What is still unknown, stale, or risky?
- Which source should be checked before acting?
- What context bundle should an agent load for this task?

GitHub remains the source of truth for code, issues, pull requests, CI state, and releases. KnowledgeVault is the source of truth for durable project memory: decisions, status, context, roadmaps, runbooks, handoffs, daily agent logs, graph records, and agent-facing operating rules.

## Vegapunk Brain (Punk Records)

Vegapunk Brain extends KnowledgeVault from a documentation repository into an event-sourced shared-memory platform.

```txt
Buddy Agent
Buddy Brain
Omni Buddy
Prismtek Apps
        ↓
   Event Emitters
        ↓
    Punk Records
        ↓
  Knowledge Graph
        ↓
Indexes / Search
        ↓
 Future Sessions
```

Core rule:

- Repositories emit immutable events.
- Vegapunk Brain validates and ingests events.
- Vegapunk Brain compiles graph records.
- Graph state can be rebuilt from event history.
- Knowledge survives beyond any individual agent.

### Start here for Vegapunk Brain

| Need | Go here |
|---|---|
| Architecture overview | `99-System/Vegapunk Brain/ARCHITECTURE-SUMMARY.md` |
| Current implementation status | `99-System/Vegapunk Brain/STATUS.md` |
| Shared Memory Bus contract | `99-System/Vegapunk Brain/shared-memory-bus.md` |
| Satellite architecture | `99-System/Vegapunk Brain/satellites.md` |
| Event emitter contracts | `99-System/Vegapunk Brain/emitters/README.md` |
| Event schema | `99-System/Vegapunk Brain/emitters/graph-event.schema.json` |
| Future vision | `99-System/Vegapunk Brain/future-state.md` |

### Operator commands

```bash
bash "99-System/Vegapunk Brain/scripts/doctor-vegapunk-brain.sh"
bash "99-System/Vegapunk Brain/scripts/validate-vegapunk-brain.sh"
bash "99-System/Vegapunk Brain/scripts/rebuild-vegapunk-brain.sh"
bash "99-System/Vegapunk Brain/scripts/index-vegapunk-brain.sh"
bash "99-System/Vegapunk Brain/scripts/run-vegapunk-brain.sh"
```

KnowledgeVault now serves two roles:

1. Human-readable knowledge base and operating manual.
2. Event-sourced durable memory layer for Buddy systems.

See the existing repository documentation below for navigation, standards, safety rules, and operating procedures.
