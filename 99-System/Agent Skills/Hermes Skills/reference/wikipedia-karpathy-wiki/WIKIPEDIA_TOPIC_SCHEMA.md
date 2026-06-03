# Wikipedia Topic Schema

This is the required shape for generated Wikipedia Karpathy Wiki notes.

## Required fields

```yaml
title: <article or concept title>
slug: <filesystem-safe slug>
note_type: concept_card | learning_note | source_map | reading_path | citation_index
domain: <knowledge domain>
source:
  project: English Wikipedia
  title: <source article title>
  url: <canonical article URL>
  revision_id: <revision id if available>
  retrieved_at: <YYYY-MM-DD>
  license_note: <license and attribution note>
freshness:
  class: stable | medium | volatile
  verify_live_before_answering: true | false
  why: <reason>
tiny_model: <one-sentence original intuition>
why_it_exists: <what problem/concept this explains>
primitives:
  - name: <primitive>
    meaning: <short explanation>
mechanism: <how it works>
relationships:
  - from: <concept>
    relation: depends_on | contains | contrasts_with | causes | enables | emerged_from | measures | explains | part_of | example_of
    to: <concept>
examples:
  - <original example>
common_confusions:
  - <misconception>
read_next:
  - title: <next topic>
    reason: <why next>
    url: <optional source URL>
quality:
  has_source_url: true
  has_retrieval_date: true
  has_freshness_label: true
  has_original_summary: true
  has_no_large_verbatim_copy: true
```

## Quality rules

Generated notes should be rejected if they lack source metadata, copied large article sections, omit freshness, or treat volatile facts as permanently true.

## Stable example domains

- mathematics
- basic physics
- grammar
- classical algorithms

## Medium example domains

- software history
- company history
- population/statistical overviews
- scientific consensus summaries

## Volatile example domains

- current events
- public offices
- active laws or policies
- market data
- living-person claims
