# Wikipedia Karpathy Sourcebook

This sourcebook defines the mental model for using English Wikipedia as a learning substrate for Hermes/Buddy.

It is intentionally not a page mirror. It is a source map, compression protocol, and reasoning scaffold.

## 0. The shape of Wikipedia

Wikipedia is a collaboratively maintained graph of articles.

The important unit is not only the article. The useful structure is:

```text
article title
├── lead summary
├── sections
├── infobox facts
├── internal links
├── categories
├── references
├── external links
├── revision history
└── discussion / quality signals
```

For an agent, Wikipedia is most valuable as a graph:

```text
concept -> related concepts -> source claims -> references -> uncertainty -> refresh rule
```

## 1. First-principles model

A Wikipedia page usually answers four hidden questions:

1. What is this thing?
2. Where does it fit in the world?
3. What are its parts, history, or mechanisms?
4. What sources support the current page text?

The Karpathy-style transform makes those hidden questions explicit.

## 2. Concept card anatomy

Every useful derived note should contain:

```yaml
title: <concept name>
tiny_model: <one sentence intuition>
why_it_exists: <problem, phenomenon, object, event, person, or idea being explained>
primitives:
  - <irreducible building block>
mechanism:
  - <how it works>
relationships:
  - from: <concept>
    relation: <causes | enables | contains | contrasts | depends_on | emerged_from>
    to: <concept>
examples:
  - <original example>
counterexamples:
  - <thing people confuse with it>
common_confusions:
  - <misconception>
freshness: stable | medium | volatile
source:
  title: <Wikipedia title>
  url: <canonical URL>
  revision_id: <optional>
  retrieved_at: <YYYY-MM-DD>
```

## 3. Knowledge domains

Use this high-level map to route article notes.

```yaml
domains:
  mathematics:
    freshness: stable
    useful_for: definitions, proofs, dependency graphs, examples
    verify_elsewhere_for: active research claims, unsolved status

  physics:
    freshness: stable_to_medium
    useful_for: mechanisms, laws, history, conceptual overview
    verify_elsewhere_for: current experiments, constants, frontier results

  chemistry:
    freshness: stable_to_medium
    useful_for: structures, reactions, periodic trends, safety orientation
    verify_elsewhere_for: handling instructions, toxicology, regulations

  biology:
    freshness: medium
    useful_for: taxonomy, anatomy, mechanisms, history
    verify_elsewhere_for: medical application, current consensus, living databases

  medicine:
    freshness: volatile
    useful_for: vocabulary and overview only
    verify_elsewhere_for: all diagnosis, treatment, dosage, emergency guidance

  computing:
    freshness: medium_to_volatile
    useful_for: history, concepts, algorithms, terminology
    verify_elsewhere_for: current APIs, versions, vulnerabilities, active projects

  history:
    freshness: stable_to_medium
    useful_for: timelines, causes, actors, source trails
    verify_elsewhere_for: contested claims, new scholarship, active conflicts

  geography:
    freshness: medium_to_volatile
    useful_for: place overview, physical geography, history
    verify_elsewhere_for: populations, political status, travel advisories

  politics:
    freshness: volatile
    useful_for: institutions and historical overview
    verify_elsewhere_for: current office holders, laws, elections, conflicts

  culture:
    freshness: medium_to_volatile
    useful_for: works, movements, genres, creator histories
    verify_elsewhere_for: release dates, living people, active franchises

  people:
    freshness: medium_to_volatile
    useful_for: biographical orientation
    verify_elsewhere_for: living person claims, current roles, allegations
```

## 4. Compression levels

Different tasks need different note sizes.

```yaml
level_0_flashcard:
  target: 50-100 words
  use_for: quick recall
  contains:
    - tiny model
    - 3 primitives
    - 1 confusion

level_1_concept_card:
  target: 250-500 words
  use_for: agent memory
  contains:
    - tiny model
    - mechanism
    - relationships
    - examples
    - source metadata

level_2_learning_note:
  target: 800-1500 words
  use_for: teaching and onboarding
  contains:
    - intuition
    - primitives
    - dependency path
    - mechanism
    - examples
    - history/context
    - common traps

level_3_source_map:
  target: structured YAML/JSON plus links
  use_for: retrieval planning
  contains:
    - source URLs
    - revision IDs
    - related article graph
    - references
    - freshness tags
```

## 5. Explanation template

Use this when teaching a topic.

```text
Tiny model:
<one sentence>

Build from primitives:
1. <primitive> — <why it matters>
2. <primitive> — <why it matters>
3. <primitive> — <why it matters>

Mechanism:
<how the concept behaves over time or under conditions>

Graph:
<concept> depends on <concept> and contrasts with <concept>.

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

## 6. Retrieval procedure

When the user asks a question:

1. Parse the target topic.
2. Decide whether the topic is stable, medium, or volatile.
3. Search or fetch the relevant article/source.
4. Extract lead, section headings, categories, and references.
5. Build a concept card from original wording.
6. Attach source pointer and retrieval date.
7. If volatile, verify through current authoritative sources before answering.

## 7. Wikipedia structures that matter

### Lead section

The lead usually gives the broadest compressed summary. It is a good starting point but should not be copied wholesale.

### Infobox

The infobox is useful for structured facts, but many infobox facts are volatile: offices, populations, leaders, dates, coordinates, classifications, and statuses.

### Section headings

Headings reveal the conceptual decomposition of the topic.

### Internal links

Internal links form the dependency graph. A good learning path follows those links in a deliberate order.

### Categories

Categories help route a note to a domain but can be noisy.

### References

References are the next-hop verification layer. For high-stakes claims, use the reference trail.

### Revision ID

Revision ID makes a note reproducible. Store it when available.

## 8. Agent memory rules

A vault note should never pretend to be the source article.

Use labels:

```yaml
note_type: original_summary | source_map | citation_index | extracted_fact | generated_explanation
```

Use attribution fields:

```yaml
source_project: English Wikipedia
source_title: <title>
source_url: <url>
source_revision: <revision id if available>
retrieved_at: <date>
derived_by: Hermes/Buddy Wikipedia Karpathy Wiki skill
```

## 9. Hallucination control

Before answering from a generated note, ask:

1. Is the note clearly sourced?
2. Is the topic volatile?
3. Does the user need current truth or conceptual understanding?
4. Are there living people, medical, legal, political, or financial stakes?
5. Would a stale answer mislead the user?

If yes, fetch current sources.

## 10. Reading-path generation

A useful reading path orders topics by dependency, not popularity.

For example:

```yaml
machine_learning:
  first:
    - function
    - probability
    - linear algebra
    - optimization
  then:
    - supervised learning
    - loss function
    - gradient descent
    - overfitting
  then:
    - neural network
    - backpropagation
    - transformer
```

For history:

```yaml
roman_republic:
  first:
    - Roman Kingdom
    - Senate
    - consul
    - patrician
    - plebeian
  then:
    - Conflict of the Orders
    - Punic Wars
    - Gracchi brothers
    - Roman civil wars
  then:
    - Julius Caesar
    - Augustus
    - Roman Empire
```

For biology:

```yaml
photosynthesis:
  first:
    - cell
    - chloroplast
    - light
    - electron
  then:
    - light-dependent reactions
    - Calvin cycle
    - glucose
  then:
    - carbon fixation
    - photorespiration
    - C3/C4/CAM pathways
```

## 11. What not to do

Do not:

- mirror all article text into GitHub
- summarize without source metadata
- let generated notes lose their source trail
- treat page content as current when a topic is volatile
- reuse media without checking media-specific license
- build a scraper that hammers Wikimedia services
- give high-stakes advice from Wikipedia alone

## 12. The best path

The best path is a two-layer system:

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

This keeps the repo professional, legal, and agent-usable without turning `knowledge-vault` into an unmaintainable data dump.
