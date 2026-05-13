# Hermes + Buddy Native Skills v3

This pack normalizes all previously created Prismtek skills into official Hermes-style `SKILL.md` files and mirrors them for Buddy.

## Why this version exists

The Hermes skill authoring guide requires frontmatter at byte 0, a closing `---` before the body, `name` and `description`, a non-empty body, and peer-style metadata such as `version`, `author`, `license`, and `metadata.hermes`. This pack follows that shape for every skill.

## Included skills

- `content-growth-social-ops` → Hermes: `skills/social-media/content-growth-social-ops/SKILL.md`, risk: `external-action`
- `sportsbook-betting-advisor` → Hermes: `skills/research/sportsbook-betting-advisor/SKILL.md`, risk: `money`
- `polymarket-trading-advisor` → Hermes: `skills/research/polymarket-trading-advisor/SKILL.md`, risk: `money`
- `moneyprinter-content-factory` → Hermes: `skills/social-media/moneyprinter-content-factory/SKILL.md`, risk: `external-action`
- `bettingai-model-advisor` → Hermes: `skills/research/bettingai-model-advisor/SKILL.md`, risk: `money`
- `hermes-x-insights-analyst` → Hermes: `skills/social-media/hermes-x-insights-analyst/SKILL.md`, risk: `read-only`
- `hermes-bookmark-research-digest` → Hermes: `skills/research/hermes-bookmark-research-digest/SKILL.md`, risk: `external-action`
- `hermes-reflect-memory-analyst` → Hermes: `skills/productivity/hermes-reflect-memory-analyst/SKILL.md`, risk: `read-only`
- `hermes-precall-context-brief` → Hermes: `skills/productivity/hermes-precall-context-brief/SKILL.md`, risk: `read-only`

## Install into a Hermes repo

```bash
node tools/install-native-skills-v3.mjs   --hermes-repo /path/to/hermes-agent   --buddy /path/to/buddy-agent   --vault /path/to/KnowledgeVault   --dry-run
```

Then run without `--dry-run`.

## Install as user-local Hermes skills only

```bash
node tools/install-native-skills-v3.mjs   --hermes-home ~/.hermes   --dry-run
```

Then run without `--dry-run`.

After installing during a running Hermes session, use `/reload-skills` or start a fresh session.

## Validate

```bash
node tools/validate-hermes-skills.mjs hermes-agent/skills
node tools/validate-hermes-skills.mjs buddy-agent/skills/native
```

## Execution policy

All skills are `auto_executable: false` in Buddy metadata. They can analyze, draft, summarize, and prepare approval previews. They cannot post, message, trade, bet, move money, mutate repos, delete memory, or drive authenticated browser sessions without explicit Prismtek approval.
