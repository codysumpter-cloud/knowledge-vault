# Wikipedia Karpathy Sourcebook

This sourcebook defines how Hermes/Buddy should use English Wikipedia as a learning substrate.

It is not a page mirror. It is a source map, compression protocol, and reasoning scaffold.

## Article shape

Useful article structure:

```text
article title
lead summary
sections
infobox facts
internal links
categories
references
external links
revision history
```

For an agent, the useful graph is:

```text
concept -> related concepts -> source claims -> references -> uncertainty -> refresh rule
```

## First-principles transform

A Wikipedia page usually answers:

1. What is this thing?
2. Where does it fit?
3. What are its parts, history, or mechanisms?
4. What sources support the page?

A Karpathy-style note makes that structure explicit and compact.

## Concept card anatomy

```yaml
title: <concept name>
tiny_model: <one sentence intuition>
why_it_exists: <concept being explained>
primitives:
  - <irreducible building block>
mechanism:
  - <how it works>
relationships:
  - from: <concept>
    relation: <depends_on | contains | contrasts | causes | enables>
    to: <concept>
examples:
  - <original example>
common_confusions:
  - <misconception>
freshness: stable | medium | volatile
source:
  title: <Wikipedia title>
  url: <canonical URL>
  revision_id: <optional>
  retrieved_at: <YYYY-MM-DD>
```

## Compression levels

```yaml
level_0_flashcard:
  target: 50-100 words
  use_for: quick recall

level_1_concept_card:
  target: 250-500 words
  use_for: agent memory

level_2_learning_note:
  target: 800-1500 words
  use_for: teaching and onboarding

level_3_source_map:
  target: structured YAML or JSON plus links
  use_for: retrieval planning
```

## Explanation template

```text
Tiny model:
<one sentence>

Build from primitives:
1. <primitive>
2. <primitive>
3. <primitive>

Mechanism:
<how the concept behaves>

Example:
<original example>

Common trap:
<misconception>

Read next:
1. <prerequisite>
2. <sibling>
3. <deeper topic>

Source posture:
<source URL, freshness, verification rule>
```

## Retrieval procedure

1. Parse the target topic.
2. Decide whether the topic is stable, medium, or volatile.
3. Fetch the relevant article or source pointer.
4. Extract lead, section headings, categories, references, and links.
5. Build a concept card using original wording.
6. Attach source pointer and retrieval date.
7. Verify live when freshness matters.

## Structures that matter

- Lead section: broad compressed summary; do not copy wholesale.
- Infobox: structured facts; many values may change.
- Internal links: dependency graph and reading path seed.
- References: next-hop verification layer.
- Revision ID: reproducibility marker.

## Agent memory rules

A vault note should never pretend to be the source article.

```yaml
note_type: original_summary | source_map | citation_index | extracted_fact | generated_explanation
source_project: English Wikipedia
source_title: <title>
source_url: <url>
source_revision: <revision id if available>
retrieved_at: <date>
derived_by: Hermes/Buddy Wikipedia Karpathy Wiki skill
```

## Reading-path generation

A useful reading path orders topics by dependency, not popularity.

Example:

```yaml
machine_learning:
  first: [function, probability, linear_algebra, optimization]
  then: [supervised_learning, loss_function, gradient_descent, overfitting]
  then: [neural_network, backpropagation, transformer]
```

## Best path

```text
Vault layer:
- schemas
- source maps
- concept cards
- generated learning notes
- prompts
- runbooks

Runtime layer:
- fetch current article/source
- check revision/freshness
- generate answer
- cite sources
- update note when useful
```
