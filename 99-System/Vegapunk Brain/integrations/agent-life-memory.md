# Agent Life memory integration

## Purpose

Store and explain bounded BUAP agent development without turning opaque model behavior into trusted memory.

BUAP emits `prismtek-agent-life-event-v1`. Knowledge Vault validates and adapts that event into the canonical Vegapunk event bus, then compiles it into a provenance-backed graph record.

```text
.buddy/life-profile.json
        ↓ immutable profile
@prismtek/buap-agent-life
        ↓ externally evidenced outcome
prismtek-agent-life-event-v1
        ↓ agent_life_ingest.py
agent_life_updated canonical event
        ↓ graph_compiler.py
concept:agent-life-<agent>-<subject>
```

## Ingestion

```bash
python "99-System/Vegapunk Brain/tools/agent_life_ingest.py" \
  --events path/to/life-events.jsonl \
  --out /tmp/canonical-agent-life-events.jsonl

python "99-System/Vegapunk Brain/tools/graph_compiler.py" \
  --events /tmp/canonical-agent-life-events.jsonl \
  --out /tmp/agent-life-graph.jsonl
```

The adapter accepts JSON, JSONL, directories, or multiple paths through the existing event loader.

## Admission requirements

Every event must include:

- the exact Agent Life schema;
- a persistent agent ID;
- an ISO-8601 timestamp with timezone;
- a subject type and ID;
- reward in `-1..1`;
- confidence in `0..1`;
- a human, host, or verifier authority;
- at least one evidence reference;
- before/after/profile hashes;
- the exact bounded state changes;
- the functional-affect claim boundary.

An agent cannot reinforce itself. Missing provenance, malformed evidence, and out-of-range signals are rejected before graph compilation.

## Graph representation

Each learned agent/subject relationship becomes a concept record such as:

```text
concept:agent-life-buddy-cody-tool-github-actions
```

The record links to:

- `agent:buddy-cody`;
- the scoped subject, such as `tool:github-actions`;
- `concept:knowledge-vault` as the compiling source.

Tags identify the record as `agent-life`, `functional-affect`, the event kind, and the subject type. Provenance points to the canonical event ID and carries the admitted confidence tier.

## Retrieval and explanation

Hosts can retrieve these records to answer questions such as:

- Why does this agent prefer this tool?
- Which receipts caused its caution around a deployment workflow?
- Is this preference recent, repeated, or stale?
- Did a user correction change a person-scoped relationship or a global tool preference?

The graph record is explanatory evidence, not mutable runtime authority. The host remains responsible for loading the compiled life profile, applying decay, and enforcing permissions.

## Privacy boundary

Life events must not contain private chain-of-thought, raw prompts, credentials, browser state, private files, or unrelated personal history. Only admitted evidence references and bounded state changes belong on this bus.
