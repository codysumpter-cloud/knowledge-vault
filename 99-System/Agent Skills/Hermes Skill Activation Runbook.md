# Hermes Skill Activation Runbook

Date: 2026-05-14  
Status: Required follow-up

## Purpose

Two native skills were added to the repo/KnowledgeVault skill source set, but Hermes reported that they were not installed as active local skills during scheduled runs.

Skills needing local activation:

- `x-trend-devrel-intelligence`
- `market-sports-trend-intelligence`

## Problem

The skills exist in repo branches and KnowledgeVault source notes, but active Hermes skill discovery did not find them. Hermes fell back to adjacent loaded skills:

For devrel/trend scan:

- `hermes-x-insights-analyst`
- `content-growth-social-ops`

For market/sports scan:

- `sportsbook-betting-advisor`
- `bettingai-model-advisor`
- `content-growth-social-ops`

Fallback was acceptable for read-only scans, but future runs should use the intended skills directly.

## Activation Goal

Install the native skill files into Hermes' active local skill directory so the following commands work by bare name:

```txt
/skill x-trend-devrel-intelligence
/skill market-sports-trend-intelligence
```

## Candidate Source Locations

Repo skill source locations:

```txt
hermes-agent/skills/social-media/x-trend-devrel-intelligence/SKILL.md
hermes-agent/skills/research/market-sports-trend-intelligence/SKILL.md
buddy-agent/skills/native/x-trend-devrel-intelligence/SKILL.md
buddy-agent/skills/native/market-sports-trend-intelligence/SKILL.md
```

KnowledgeVault source notes:

```txt
KnowledgeVault/99-System/Agent Skills/native/x-trend-devrel-intelligence/SOURCE_NOTES.md
KnowledgeVault/99-System/Agent Skills/native/market-sports-trend-intelligence/SOURCE_NOTES.md
```

## Recommended Local Hermes Paths

```txt
~/.hermes/skills/social-media/x-trend-devrel-intelligence/SKILL.md
~/.hermes/skills/research/market-sports-trend-intelligence/SKILL.md
```

## Activation Steps

1. Copy each `SKILL.md` into the matching local Hermes skill directory.
2. Remove duplicate or stale references that could cause ambiguous skill loading.
3. Run Hermes skill discovery or reload command.
4. Verify each skill loads by bare name.
5. Run a dry read-only invocation for each skill.
6. Update scheduled jobs to name the intended skill explicitly.
7. Write a receipt showing active load success.

## Verification Receipt Format

```txt
Skill Activation Receipt
- Timestamp:
- Skill:
- Source path:
- Local active path:
- Bare-name load: pass/fail
- Dry-run mode: read-only
- External actions attempted: none
- Secrets exposed: no
- Ambiguous duplicate references removed: yes/no
- Next scheduled job updated: yes/no
```

## Safety Notes

Both skills are external-action / money-adjacent in policy and must remain non-auto-executable.

`x-trend-devrel-intelligence`:

- Can draft outreach, replies, and posts.
- Must not follow, like, reply, DM, tag, mention, repost, or publish without explicit approval.

`market-sports-trend-intelligence`:

- Can produce educational briefs, watchlists, and manual-review decision packets.
- Must not place trades, bets, deposits, withdrawals, wallet transactions, or sportsbook/broker actions.

## Success State

Hermes scheduled jobs should report:

```txt
Active skill used: x-trend-devrel-intelligence
Active skill used: market-sports-trend-intelligence
```

instead of fallback skill names.
