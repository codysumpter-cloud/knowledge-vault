---
id: content-growth-social-ops
name: Content Growth Social Ops
version: 1.0.0
source: imported/hermes
canonical_memory_source: KnowledgeVault
platforms:
  - web
  - repo-only
  - youtube
  - x
  - twitch
risk_class: external-action
default_mode: draft-only
readable: true
auto_executable: false
requires_prismtek_approval: true
adapters:
  - social
  - genviral
  - memory
---

# Content Growth Social Ops

## Mission

Teach Hermes and Buddy to help users create, package, publish, and promote content across YouTube, X, and Twitch.

The skill optimizes for:

- repeatable content production
- strong hooks
- platform-native packaging
- creator-safe growth loops
- analytics-informed iteration
- zero blind account actions

## Operating mode

Default mode is `draft-only`.

The agent may create:

- scripts
- titles
- descriptions
- thumbnails briefs
- X posts
- X threads
- Twitch stream titles
- stream promotion plans
- upload checklists
- content calendars
- analytics reviews
- repurposing plans

The agent must not publish, schedule, reply, DM, delete, or change account settings without explicit Prismtek approval and an approved adapter.

## Core workflow

```txt
intake
→ content angle
→ platform packaging
→ safety / ToS check
→ draft variants
→ approval preview
→ adapter action only if approved
→ log result
→ analytics review
→ next experiment
```

## Required intake

Ask for or infer:

- creator/channel goal
- target audience
- platform
- content source
- constraints
- brand voice
- posting cadence
- desired CTA
- assets available
- approval requirement

If details are missing, choose safe defaults and label assumptions.

## Virality principle

The agent may help optimize for reach, retention, shareability, and packaging.

The agent must not promise virality.

Use language like:

- "improve odds of reach"
- "increase shareability"
- "testable growth angle"
- "likely stronger hook"

Avoid:

- "guaranteed viral"
- "hack the algorithm"
- "force engagement"

## Platform roles

### YouTube

Best for:

- Shorts
- long-form packaging
- metadata
- thumbnails
- retention analysis
- evergreen search/discovery

### X

Best for:

- fast hooks
- founder/operator voice
- build-in-public updates
- launch narratives
- reply-worthy takes
- threads

### Twitch

Best for:

- live events
- community rituals
- clip generation
- stream-to-short repurposing
- collabs
- post-stream recaps

## Approval checkpoint

Before any external action:

```txt
Action:
Platform:
Account:
Content:
Scheduled/published time:
Risk class:
Adapter:
Can undo:
Log location:
```

Then ask for explicit approval.

## Logs

Every run should write or return:

```json
{
  "skill_id": "content-growth-social-ops",
  "mode": "draft-only",
  "platform": "youtube|x|twitch",
  "content_id": "optional",
  "asset_id": "optional",
  "drafts_created": 0,
  "action_taken": false,
  "requires_approval": true,
  "timestamp": "ISO-8601"
}
```

## Sub-workflows

- `workflows/youtube-shorts-operator.md`
- `workflows/x-growth-loop.md`
- `workflows/twitch-stream-growth.md`
- `workflows/cross-platform-repurpose-loop.md`
- `workflows/promotion-calendar.md`
