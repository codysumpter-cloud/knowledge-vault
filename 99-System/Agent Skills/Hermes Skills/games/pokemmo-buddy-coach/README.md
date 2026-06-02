# PokeMMO Buddy Coach

Fast entrypoint for agents reading this folder.

## Load order

1. `SKILL.md` — shortest operating context and current Prismtek state.
2. `skill.yaml` — machine-readable manifest for registry/import tooling.
3. `POKEMMO_BUDDY_COACH_SKILL.md` — full skill contract and procedures.
4. `POKEMMO_BUDDY_COACH_WIKI.md` — compact first-principles coaching guide.
5. `POKEMMO_KARPATHY_SOURCEBOOK.md` — broad source map for the requested PokeMMO websites.

## Use rule

Use `SKILL.md` for fast runtime context. Use the sourcebook for source selection and durable schemas. Use current public sources or user screenshots for volatile facts such as encounter tables, GTL prices, events, and recently changed mechanics.

## Runtime shape

The skill turns user screenshots and manual game state into concise coaching decisions:

```text
state -> constraint -> option set -> cost -> recommendation -> next action
```

## File roles

| File | Role |
|---|---|
| `SKILL.md` | Agent-friendly quickstart and operating contract |
| `skill.yaml` | Manifest for machine loading |
| `POKEMMO_BUDDY_COACH_SKILL.md` | Detailed skill contract |
| `POKEMMO_BUDDY_COACH_WIKI.md` | First-principles coaching model |
| `POKEMMO_KARPATHY_SOURCEBOOK.md` | Source map and compressed knowledge architecture |

## Maintenance

When adding new facts, keep volatile data out of the durable docs unless it is marked with a verification date. Prefer source links, schemas, and decision rules over copied tables.
