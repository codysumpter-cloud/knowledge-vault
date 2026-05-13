# Buddy + Hermes Skill Pack

Generated: 2026-05-13

This pack adds a curated skill bridge for:

- YouTube / X / Twitch content generation and promotion
- cross-platform short-form repurposing
- safe sportsbook betting analysis
- safe Polymarket / prediction-market analysis
- KnowledgeVault skill-library compatibility
- Buddy runtime policy gates and adapter-first execution

## BMO verdict

Do **not** dump the entire KnowledgeVault/Hermes skill archive into Buddy as active code.

Use this layout:

```txt
buddy-agent/
  AGENTS.md
  skills/
    registry.json
    SKILL_IMPORT_POLICY.md
    knowledge-vault-skill-sources.json
    risk-policy.json
    adapters/
    imported/
      hermes/
        content-growth-social-ops/
        sportsbook-betting-advisor/
        polymarket-trading-advisor/
```

Hermes can use the same library for now, but Buddy should only execute skills after:

1. metadata/frontmatter is parsed
2. platform is checked
3. risk class is checked
4. confirmation policy is applied
5. an approved adapter handles the action

## One-command install

From the unpacked folder:

```bash
node tools/install-skill-pack.mjs \
  --buddy /path/to/buddy-agent \
  --hermes /path/to/hermes-agent \
  --vault /path/to/KnowledgeVault
```

Dry-run first:

```bash
node tools/install-skill-pack.mjs \
  --buddy /path/to/buddy-agent \
  --hermes /path/to/hermes-agent \
  --vault /path/to/KnowledgeVault \
  --dry-run
```

Validate the generated files:

```bash
node tools/validate-skills.mjs ./buddy-agent/skills
```

## Important safety defaults

These skills are **readable by default** but **not auto-executable** for account, money, trading, posting, repo, location, deletion, and messaging actions.

The pack intentionally blocks:

- auto-posting without approval
- mass engagement / spam / fake virality
- sportsbook wager placement
- Polymarket order placement
- deposits, withdrawals, transfers
- credentials handling
- repo mutation without explicit approval
- memory deletion without explicit approval

## What this does not do

This pack does not sign into accounts, hold credentials, place wagers, place trades, guarantee viral growth, or guarantee betting/trading profit.

It gives Buddy/Hermes a clean policy-and-workflow layer so the agents can advise, draft, plan, review, and prepare approved actions safely.
