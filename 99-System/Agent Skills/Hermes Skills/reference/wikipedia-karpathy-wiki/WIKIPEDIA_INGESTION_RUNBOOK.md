# Wikipedia Ingestion Runbook

This runbook defines the safe path for turning English Wikipedia into a Karpathy-style source-guided wiki inside Knowledge Vault.

## Important constraint

Do not commit a full Wikipedia mirror into this repository.

A full mirror is the wrong artifact for `knowledge-vault` because it is huge, difficult to review, constantly changing, license-sensitive, attribution-heavy, and not especially useful to an agent without indexing, ranking, chunking, and freshness logic.

Commit the system that can ingest and summarize Wikipedia correctly.

Store compact derived notes only when they are useful.

## Source options

### 1. Live page fetch

Use when:

- the user asks about one topic
- freshness matters
- the topic is volatile
- the agent needs the current article revision

Preferred outputs:

- source URL
- page title
- revision ID if available
- retrieval date
- concept card
- citations

### 2. Wikimedia dumps

Use when:

- building an offline index
- creating embeddings
- generating broad topic maps
- doing batch concept-card generation

Store dumps outside Git when possible:

```text
.data/wikipedia/enwiki/latest/
```

Recommended `.gitignore` entries:

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

### 3. Wikipedia API

Use when:

- fetching specific pages
- fetching revision IDs
- resolving redirects
- getting links/categories/sections

API behavior must be polite:

- identify the application with a descriptive User-Agent
- obey rate limits and backoff
- use maxlag where supported
- cache results
- avoid unnecessary repeated requests

## Minimal local pipeline

```bash
mkdir -p .data/wikipedia/enwiki/latest
mkdir -p 99-System/Agent\ Skills/Hermes\ Skills/reference/wikipedia-karpathy-wiki/generated
```

Fetch or stream source data outside Git.

Then generate small notes into the vault only when useful.

## Recommended pipeline architecture

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

For each article, capture:

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

Avoid:

```text
every 800 tokens blindly
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

Reject notes that fail any check:

```yaml
checks:
  has_source_url: true
  has_retrieval_date: true
  has_freshness_label: true
  has_original_summary: true
  has_relationships: true
  has_no_large_verbatim_copy: true
  marks_volatile_claims: true
  high_stakes_claims_require_external_verification: true
```

## File naming

Use filesystem-safe slugs:

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
- <primitive>: <meaning>
- <primitive>: <meaning>

## Mechanism

<original explanation of how it works>

## Relationships

```yaml
relationships:
  - from: <concept>
    relation: <depends_on | contains | contrasts | causes | enables>
    to: <concept>
```

## Examples

- <original example>

## Common traps

- <misconception>

## Read next

1. <topic>
2. <topic>
3. <topic>

## Source posture

This is an original compressed note derived from the source page. Verify live before using for volatile or high-stakes claims.
```

## Batch ingestion guardrails

For a large batch:

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

## Suggested manifest fields

```yaml
manifest:
  source_project: English Wikipedia
  dump_date: <YYYY-MM-DD>
  dump_url: <source dump URL>
  article_count_processed: <number>
  notes_generated: <number>
  skipped_redirects: <number>
  skipped_disambiguation: <number>
  generated_at: <timestamp>
  generator_version: <version>
```

## Example Python skeleton

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

Freshness = Literal["stable", "medium", "volatile"]

@dataclass
class SourceArticle:
    title: str
    url: str
    revision_id: str | None
    text: str
    retrieved_at: str

@dataclass
class ConceptCard:
    title: str
    tiny_model: str
    primitives: list[str]
    relationships: list[dict[str, str]]
    examples: list[str]
    common_traps: list[str]
    read_next: list[str]
    freshness: Freshness
    source_url: str
    revision_id: str | None
    retrieved_at: str


def classify_freshness(title: str, categories: list[str]) -> Freshness:
    volatile_terms = ["living people", "politics", "elections", "law", "medicine", "current events"]
    haystack = " ".join([title, *categories]).lower()
    if any(term in haystack for term in volatile_terms):
        return "volatile"
    medium_terms = ["software", "company", "population", "statistics", "biology"]
    if any(term in haystack for term in medium_terms):
        return "medium"
    return "stable"


def write_concept_card(card: ConceptCard, out_dir: Path) -> Path:
    slug = card.title.lower().replace(" ", "-").replace("/", "-")
    path = out_dir / f"{slug}.md"
    relationships = "\n".join(
        f"  - from: {r['from']}\n    relation: {r['relation']}\n    to: {r['to']}"
        for r in card.relationships
    )
    content = f"""# {card.title}

Status: generated concept card  
Source: {card.source_url}  
Revision: {card.revision_id or "unknown"}  
Retrieved: {card.retrieved_at}  
Freshness: {card.freshness}

## Tiny model

{card.tiny_model}

## Build from primitives

"""
    content += "\n".join(f"- {p}" for p in card.primitives)
    content += f"""

## Relationships

```yaml
relationships:
{relationships}
```

## Examples

"""
    content += "\n".join(f"- {x}" for x in card.examples)
    content += "\n\n## Common traps\n\n"
    content += "\n".join(f"- {x}" for x in card.common_traps)
    content += "\n\n## Read next\n\n"
    content += "\n".join(f"{i + 1}. {x}" for i, x in enumerate(card.read_next))
    content += "\n\n## Source posture\n\nThis is an original compressed note derived from the source page. Verify live before using for volatile or high-stakes claims.\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
```

## Review workflow

1. Generate notes locally.
2. Inspect a small sample manually.
3. Confirm no large copied blocks.
4. Confirm source metadata exists.
5. Commit generated notes in small batches.
6. Keep raw dumps out of Git.

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
