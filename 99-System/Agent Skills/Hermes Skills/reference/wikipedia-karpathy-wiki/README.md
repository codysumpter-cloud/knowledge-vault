# Wikipedia Karpathy Wiki

Status: draft source pack  
Owner: Prismtek / Buddy ecosystem  
Source: https://en.wikipedia.org  
Mode: source-guided learning wiki, not a verbatim mirror

## Purpose

This pack gives Hermes/Buddy a maintainable way to use English Wikipedia as a broad world-knowledge backbone.

It does not paste all of Wikipedia into `knowledge-vault`. Instead, it defines a Karpathy-style learning layer that turns Wikipedia into compact, inspectable, agent-usable knowledge:

- mental models before trivia
- source pointers before copied text
- relationships before isolated facts
- freshness and uncertainty flags before confident claims
- citation and license discipline before ingestion

## What belongs in this pack

This pack stores:

- source policies and ingestion rules
- schemas for article summaries and concept cards
- domain maps for major areas of knowledge
- Karpathy-style explanation templates
- prompts for producing concise learning notes
- retrieval and citation procedures
- maintenance rules for keeping derived notes fresh

This pack does **not** store:

- a full dump of Wikipedia text
- un-attributed article mirrors
- media files from Wikimedia Commons
- stale facts presented as current truth
- scraped content without license and attribution handling

## Directory map

```text
wikipedia-karpathy-wiki/
├── README.md
├── WIKIPEDIA_KARPATHY_WIKI_SKILL.md
├── WIKIPEDIA_KARPATHY_SOURCEBOOK.md
├── WIKIPEDIA_INGESTION_RUNBOOK.md
├── WIKIPEDIA_TOPIC_SCHEMA.md
└── skill.yaml
```

## Operating model

For any topic, the agent should produce this layered view:

```text
1. One-sentence intuition
2. First-principles explanation
3. Core entities and relationships
4. Why it matters
5. Key mechanisms
6. Historical or causal arc
7. Common confusions
8. Examples and counterexamples
9. Open questions / uncertainty
10. Source pointers and refresh rules
```

## Article-to-note transform

Every Wikipedia article should be treated as a source artifact, not as the final note.

```yaml
article:
  title: <Wikipedia title>
  url: <canonical page URL>
  revision_id: <when available>
  last_seen: <YYYY-MM-DD>
  license: source license and attribution requirements must be preserved

karpathy_note:
  why_it_exists: <problem or concept the article explains>
  core_model: <plain mental model>
  primitives:
    - <entity/mechanism>
  relationships:
    - from: <concept>
      relation: <causes/enables/contrasts/contains>
      to: <concept>
  examples:
    - <short original example>
  uncertainty:
    freshness: stable | medium | volatile
    should_verify_live: true | false
```

## Agent usage

Use this pack when the user asks for broad knowledge, concept learning, research orientation, or source-grounded explanation.

Do not use it as the only source for current events, professional decisions, active public roles, or any situation where stale information could mislead the user.

## Style target

Karpathy-style here means:

- start with the tiny model
- build from primitives
- explain mechanisms, not just names
- preserve source provenance
- compress hard but do not flatten uncertainty
- make the note useful to a future agent that has to reason, route, or teach

## Example invocation

```text
Use Wikipedia Karpathy Wiki. Teach me quantum field theory from first principles, with concept dependencies and what to read next.
```

```text
Use Wikipedia Karpathy Wiki. Build an agent-usable concept card for the Roman Republic. Include uncertainty and source refresh rules.
```

## Safety and quality posture

Wikipedia is extremely useful, but it is a starting map and citation graph, not final authority for high-stakes claims.

When in doubt:

1. Cite the Wikipedia article and revision when text or article-derived facts are reused.
2. Prefer source-linked summaries over copied paragraphs.
3. Verify volatile facts with current primary or authoritative sources.
4. Preserve uncertainty.
5. Never imply this vault contains the full current state of Wikipedia.
