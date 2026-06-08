# Wikipedia Karpathy Wiki

Status: Phase 2 implementation scaffold  
Owner: Prismtek / Buddy ecosystem  
Source: English Wikipedia  
Mode: source-guided learning wiki, not a verbatim mirror

## Purpose

This pack gives Hermes/Buddy a maintainable way to use Wikipedia as a broad world-knowledge backbone without committing a raw mirror into Git.

The goal is to create a Karpathy-style learning layer that turns source articles into compact, inspectable, agent-usable knowledge:

- mental models before trivia
- source pointers before copied text
- canonical questions before loose notes
- relationships before isolated facts
- freshness and uncertainty flags before confident claims
- citation and license discipline before ingestion

## Phase 2 engine

Phase 2 adds runnable Python tooling around the original source pack:

- API ingestion for selected articles
- dump streaming into local JSONL source records
- deterministic concept-card generation
- Obsidian note generation
- reading-path generation
- knowledge graph edge extraction
- redirect and alias resolution
- domain, concept, and category index updates
- Buddy runtime wrapper functions
- incremental update support through small JSON indexes

## Directory map

```text
wikipedia-karpathy-wiki/
├── ingest/
│   ├── wikipedia_api_ingest.py
│   ├── dump_ingest.py
│   ├── concept_extractor.py
│   ├── reading_path_generator.py
│   └── buddy_wikipedia_skill.py
├── schemas/
├── generated/
├── indexes/
│   ├── concepts.json
│   ├── domains.json
│   └── redirects.json
└── prompts/
```

## Quick start

```bash
cd "99-System/Agent Skills/Hermes Skills/reference/wikipedia-karpathy-wiki"
python3 ingest/wikipedia_api_ingest.py "Transformer (machine learning model)" --generate
python3 ingest/reading_path_generator.py "Transformer (machine learning model)"
```

Source JSON is cached under `.data/` by default so raw source does not get committed. Generated cards and indexes are small review artifacts.

## Agent usage

Use this pack when the user asks for broad knowledge, concept learning, research orientation, source-grounded explanation, concept dependencies, or reading paths.

Do not use it as the only source for current events, medical decisions, legal decisions, financial decisions, or anything where a stale answer could hurt someone.

## Safety and quality posture

Wikipedia is useful, but it is not a substitute for professional judgment. Treat it as a starting map and citation graph, not as final authority for high-stakes claims.

When in doubt:

1. Cite the source article and revision when text or facts are reused.
2. Prefer source-linked summaries over copied paragraphs.
3. Verify volatile facts with current primary or authoritative sources.
4. Preserve uncertainty.
5. Never imply this vault contains the full current state of Wikipedia.
