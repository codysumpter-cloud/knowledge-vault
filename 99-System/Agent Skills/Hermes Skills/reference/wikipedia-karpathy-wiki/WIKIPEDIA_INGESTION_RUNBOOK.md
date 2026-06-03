# Wikipedia Ingestion Runbook

This runbook defines the safe path for turning English Wikipedia into a Karpathy-style source-guided wiki inside Knowledge Vault.

## Constraint

Do not commit a full Wikipedia mirror into this repository.

The vault should contain the system for ingesting and summarizing Wikipedia correctly, plus compact derived notes when they are useful. Raw source dumps should stay outside Git.

## Source options

### Live page fetch

Use when:

- the user asks about one topic
- freshness matters
- the topic is volatile
- the agent needs the current article revision

Capture:

- source URL
- page title
- revision ID if available
- retrieval date
- concept card
- citations

### Wikimedia dumps

Use when:

- building an offline index
- creating embeddings
- generating broad topic maps
- doing batch concept-card generation

Store dumps outside Git:

```text
.data/wikipedia/enwiki/latest/
```

Recommended ignore rules:

```gitignore
.data/
*.xml
*.xml.bz2
*.jsonl
*.sqlite
*.parquet
*.faiss
*.duckdb
```

### Wikipedia API

Use when:

- fetching specific pages
- fetching revision IDs
- resolving redirects
- getting links, categories, and sections

API behavior should be polite:

- identify the application clearly
- back off on server pressure
- cache results
- avoid repeated unnecessary requests

## Pipeline

```text
source acquisition
  -> article normalization
  -> section extraction
  -> metadata capture
  -> concept graph extraction
  -> Karpathy note generation
  -> quality gate
  -> vault write
  -> index update
```

## Article normalization

```yaml
article_id: <id>
title: <title>
canonical_url: <url>
revision_id: <revision>
retrieved_at: <YYYY-MM-DD>
namespace: main
redirect: true | false
disambiguation: true | false
categories: []
links: []
sections: []
references: []
license_note: <source license note>
```

Skip by default:

- talk pages
- user pages
- templates
- redirects unless needed for alias mapping
- pure disambiguation pages unless building a resolver
- list pages unless building an index

## Chunking model

Chunk by semantic section, not arbitrary token windows.

Prefer:

```text
article lead
article section
article subsection
infobox facts
reference list
category/link graph
```

Blind chunks lose the article's conceptual structure.

## Derived note generation

For each eligible article:

1. Read title, lead, section headings, categories, and key references.
2. Generate an original summary.
3. Build primitives and relationships.
4. Assign freshness.
5. Write source metadata.
6. Include source URL and revision.
7. Avoid long copied text.

## Quality gate

```yaml
checks:
  has_source_url: true
  has_retrieval_date: true
  has_freshness_label: true
  has_original_summary: true
  has_relationships: true
  has_no_large_verbatim_copy: true
  marks_volatile_claims: true
```

## File naming

```text
generated/concepts/<domain>/<slug>.md
```

Examples:

```text
generated/concepts/math/pythagorean-theorem.md
generated/concepts/computing/transformer-machine-learning-model.md
generated/concepts/history/roman-republic.md
```

## Concept note template

```markdown
# <Title>

Status: generated concept card  
Source: <Wikipedia URL>  
Revision: <revision id if known>  
Retrieved: <YYYY-MM-DD>  
Freshness: stable | medium | volatile

## Tiny model

<one-sentence original explanation>

## Build from primitives

- <primitive>: <meaning>

## Mechanism

<original explanation of how it works>

## Relationships

- <concept> -> <relationship> -> <concept>

## Read next

1. <topic>
2. <topic>
3. <topic>

## Source posture

This is an original compressed note derived from the source page. Verify live before using for volatile claims.
```

## Batch guardrails

```yaml
batch:
  max_articles_per_run: 100
  max_generated_notes_per_commit: 25
  require_review_before_merge: true
  skip_volatile_topics_by_default: true
  commit_raw_source: false
  commit_generated_notes: true
  commit_index: true
```

## Done criteria

The wiki system is ready when:

- the skill contract exists
- the sourcebook exists
- ingestion rules exist
- schema exists
- generated notes include source metadata
- volatile topics require live verification
- raw Wikipedia dumps are excluded from Git
- attribution and license rules are explicit
