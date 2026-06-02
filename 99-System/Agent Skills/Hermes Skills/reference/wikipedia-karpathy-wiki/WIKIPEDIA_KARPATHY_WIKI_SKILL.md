# Wikipedia Karpathy Wiki — Hermes Skill

Status: draft reference skill  
Owner: Prismtek / Buddy ecosystem  
Category: reference / world-knowledge / learning / research  
Risk posture: source-guided, citation-required for factual reuse

## Purpose

Wikipedia Karpathy Wiki is a Hermes/Buddy skill for turning Wikipedia into compact, explainable, agent-usable knowledge.

The skill does **not** claim to contain all of Wikipedia inside the repository. It provides a reproducible method for deriving concise knowledge notes from Wikipedia pages, dumps, and citations while preserving provenance, uncertainty, and refresh rules.

## Skill contract

```yaml
skill_id: wikipedia_karpathy_wiki
name: Wikipedia Karpathy Wiki
version: 0.1.0
status: draft
runtime: hermes-agent
mode: source_guided_reference
sources:
  primary:
    - https://en.wikipedia.org
    - https://dumps.wikimedia.org/enwiki/latest/
    - https://www.mediawiki.org/wiki/API:Main_page
    - https://www.mediawiki.org/wiki/API:Etiquette
    - https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use
inputs:
  - user_question
  - topic_optional
  - wikipedia_url_optional
  - article_title_optional
  - desired_depth_optional
  - freshness_requirement_optional
outputs:
  - answer
  - concept_card_optional
  - dependency_graph_optional
  - reading_path_optional
  - uncertainty_notes
  - citations_when_source_used
safety:
  allow_public_reference_use: true
  allow_wikipedia_api_use: true
  allow_dump_ingestion_planning: true
  allow_verbatim_large_copying: false
  require_license_awareness: true
  require_attribution_for_reused_text: true
  require_current_verification_for_volatile_topics: true
```

## Core behavior

When invoked, the skill should:

1. Identify the user's target concept or question.
2. Decide whether Wikipedia is suitable as a starting source.
3. Fetch or use the relevant article/source pointer when live access is available.
4. Convert the source into a compact mental model.
5. Separate stable structure from volatile facts.
6. Provide citations or source pointers.
7. Recommend primary/authoritative sources when stakes are high.

## Response shape

Prefer this shape for concept teaching:

```text
Tiny model: <one-sentence intuition>

Build it from primitives:
1. <primitive>
2. <primitive>
3. <primitive>

Mechanism:
<how the thing works>

Why it matters:
<relevance>

Common traps:
- <misconception>

Read next:
1. <dependency topic>
2. <deeper topic>

Source posture:
- Based on: <Wikipedia source pointer>
- Freshness: stable | medium | volatile
- Verify live before using for: <dates, office holders, prices, medical guidance, law, current events>
```

For research orientation:

```text
Map:
- root concept
  - subtopic
  - subtopic

Useful sequence:
1. <topic>
2. <topic>
3. <topic>

What to ignore at first:
- <details that distract beginners>

What to verify elsewhere:
- <claims needing primary sources>
```

For agent memory creation:

```yaml
concept_card:
  title: <concept>
  source_url: <url>
  source_revision: <revision_id_if_known>
  last_seen: <YYYY-MM-DD>
  summary: <original compact summary>
  primitives: []
  relationships: []
  examples: []
  counterexamples: []
  common_confusions: []
  freshness: stable | medium | volatile
  verify_live_before_answering: true | false
```

## Karpathy-style rules

A good note should feel like source code comments for reality:

- name the primitives
- explain the mechanism
- show the dependency graph
- reduce vocabulary load
- mark the unknowns
- preserve links to source
- make the next action obvious

Bad notes look like copied encyclopedic paragraphs.

Good notes look like reusable thinking tools.

## Source hierarchy

Use Wikipedia as:

- a first-pass map
- a terminology resolver
- a citation graph
- a dependency graph seed
- a stable overview for mature topics

Do not use Wikipedia alone as final authority for:

- current political offices or active conflicts
- medical diagnosis or treatment
- legal advice
- financial advice
- safety-critical engineering decisions
- biographical claims about living people without verification
- anything the user explicitly asks to verify

## Attribution discipline

If the answer reuses Wikipedia wording, requires attribution, or creates a derived note from an article, include:

```yaml
source_attribution:
  project: English Wikipedia
  article_title: <title>
  article_url: <url>
  revision_id: <id_if_available>
  license_note: Wikipedia text is generally reusable under CC BY-SA terms with attribution and share-alike requirements; verify page-specific notices and media licenses.
```

Prefer original summaries over copied text.

## Freshness model

```yaml
stable:
  examples:
    - geometry
    - classical mechanics basics
    - ancient history overview
    - grammar concepts
  behavior: derived note may be reused; cite source when needed

medium:
  examples:
    - company history
    - software versions
    - scientific consensus summaries
    - population statistics
  behavior: refresh before formal claims

volatile:
  examples:
    - current office holders
    - wars and disasters
    - election results
    - laws and regulations
    - medical guidance
    - prices and market data
  behavior: web/live verification required before answering
```

## Failure modes to avoid

- treating Wikipedia as a database of guaranteed truth
- losing article provenance during summarization
- copying large passages into the vault
- mixing article text and generated notes without labels
- ignoring page-specific media licenses
- giving high-stakes advice from Wikipedia alone
- letting stale generated notes outrank fresh source checks

## Suggested invocations

```text
Use Wikipedia Karpathy Wiki. Build a concept card for entropy.
```

```text
Use Wikipedia Karpathy Wiki. Teach the Industrial Revolution with dependencies, mechanisms, and what to read next.
```

```text
Use Wikipedia Karpathy Wiki. Explain reinforcement learning from first principles and separate stable concepts from active research questions.
```

```text
Use Wikipedia Karpathy Wiki. Given this Wikipedia article URL, turn it into an agent-usable note with citations and freshness flags.
```

## Done criteria for generated notes

A generated note is ready when it includes:

- source URL
- source title
- source revision or retrieval date
- original compact summary
- concept dependencies
- relationships
- uncertainty/freshness label
- reading path
- no large copied article blocks
- clear reminder to verify volatile facts live
