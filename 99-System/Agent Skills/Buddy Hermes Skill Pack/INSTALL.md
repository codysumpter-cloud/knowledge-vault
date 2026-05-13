# Install Guide

## 1. Copy files into Buddy and Hermes

Recommended:

```bash
node tools/install-skill-pack.mjs   --buddy ../buddy-agent   --hermes ../hermes-agent   --vault ../KnowledgeVault   --dry-run
```

Then run without `--dry-run` when the planned copies look right.

## 2. Point Buddy at KnowledgeVault

The installer writes this local override:

```txt
buddy-agent/skills/knowledge-vault-skill-sources.local.json
```

Buddy should read `knowledge-vault-skill-sources.json` first, then merge `.local.json` if present.

## 3. Runtime loading order

Buddy should load skills in this order:

1. canonical registry
2. KnowledgeVault source bridge
3. imported Hermes skills
4. reviewed Buddy-compatible skills
5. active adapter-bound skills

## 4. Approval behavior

Use `skills/risk-policy.json` as the runtime source of truth.

Required approvals:

- account write
- external posting
- trades
- bets
- deposits / withdrawals
- repo mutation
- deletion
- memory deletion
- location / messages
- auth / credentials

## 5. Promote skills gradually

Recommended lifecycle:

```txt
mirrored Hermes skill
→ reviewed Buddy-compatible skill
→ adapter-bound active skill
→ audited production skill
```

Do not promote a skill into auto-execution until it has:

- structured metadata
- risk class
- platform class
- required adapters
- dry-run mode
- confirmation copy
- failure handling
- log format
