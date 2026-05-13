# Compliance Report

Generated: 2026-05-13

## Hermes skill format checks

Every included `SKILL.md` file follows the official Hermes authoring structure:

- starts at byte 0 with `---`;
- closes frontmatter with `---` before the Markdown body;
- includes `name`, `description`, `version`, `author`, `license`, and `metadata.hermes`;
- keeps `description` below 1024 characters and starts with `Use when`;
- includes `# Title`, `## Overview`, `## When to Use`, `## Common Pitfalls`, and `## Verification Checklist`;
- stays well under the 100,000-character file limit.

## Risk posture

- `read-only` skills still default to no automatic writes.
- `external-action` skills draft and preview only.
- `money` skills are analysis-only and block all bet/trade/wallet/money execution.

## Local validation command

```bash
node tools/validate-hermes-skills.mjs hermes-agent/skills
node tools/validate-hermes-skills.mjs buddy-agent/skills/native
```
