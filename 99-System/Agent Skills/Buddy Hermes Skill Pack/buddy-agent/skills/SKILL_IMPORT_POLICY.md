# Skill Import Policy

## Purpose

KnowledgeVault is the canonical skill library and memory source.

Buddy is the runtime that selects, validates, and executes approved skills.

Hermes is the current operator using the same skill library for now.

## Import strategy

Imported skills are **source material** until promoted.

Do not blindly copy a large skill archive into active runtime code.

Use this promotion path:

```txt
KnowledgeVault source skill
→ mirrored Hermes skill
→ reviewed Buddy-compatible skill
→ active Buddy adapter skill
→ audited production skill
```

## Required metadata

Each executable skill must expose these fields in frontmatter or `metadata.json`:

```yaml
id: string
name: string
version: semver
source: knowledge-vault | imported/hermes | buddy-native
platforms:
  - macos | ios | web | repo-only | youtube | x | twitch
risk_class: read-only | draft-only | write | external-action | destructive | money
readable: true
auto_executable: false
requires_prismtek_approval: true
adapters:
  - adapter-id
```

## Default import state

A newly imported skill defaults to:

```yaml
readable: true
auto_executable: false
requires_prismtek_approval: true
status: readable-reference-only
```

## High-risk skills

These can be read, summarized, and transformed, but not auto-run:

- iMessage / SMS
- Apple Notes
- Apple Reminders
- Find My
- macOS computer-use
- memory deletion
- Polymarket / trading
- sportsbook betting
- GitHub mutation
- Obsidian Git sync
- social posting

## Execution rule

Buddy may execute only through an adapter.

Skills must not shell out, call APIs, mutate repos, send messages, trade, bet, or post directly.

## Confirmation rule

For external-action, destructive, or money skills, Buddy must present:

1. exact action
2. target account / repo / platform
3. expected effect
4. reversible or irreversible status
5. risk class
6. final confirmation prompt

The user must explicitly approve before execution.

## Logging rule

Every skill run must produce a structured log entry with:

```json
{
  "skill_id": "string",
  "mode": "read-only|draft-only|analysis-only|confirmed-action",
  "risk_class": "string",
  "adapter": "string",
  "inputs_summary": "string",
  "outputs_summary": "string",
  "action_taken": false,
  "requires_followup": false,
  "timestamp": "ISO-8601"
}
```
