# PokeMMO Buddy Coach

Status: draft-first local assistant skill  
Runtime: Hermes/Buddy advisory skill  
Mode: screenshot/manual-state coach only

## What this skill does

PokeMMO Buddy Coach helps a Buddy/Hermes agent turn PokeMMO screenshots, user notes, and current public sources into fast gameplay decisions.

Use it when the user asks for help with:

- route/story navigation
- Elite Four prep
- region-locked team planning
- OT-safe Pokemon planning
- IV/nature/EV evaluation
- breeding path planning
- GTL listing evaluation
- money-making strategy
- encounter/location verification
- PokeMMO source lookup and synthesis

## Hard boundary

This skill is a coach, not a bot.

Allowed:

- analyze user-provided screenshots
- analyze manually entered game state
- recommend routes, teams, builds, EVs, breeding steps, and purchases
- summarize source pages and cite current sources when needed
- maintain checklists and local planning state

Forbidden:

- gameplay automation
- macros or input scripts
- client hooks or client patches
- process memory reading
- packet inspection
- auto-catching, auto-battling, auto-routing, auto-farming, or GTL sniping

## Immediate response contract

Prefer this shape:

```text
Verdict: <one-line decision>

Why:
- <short reason>
- <short reason>

Do this:
1. <next step>
2. <next step>
3. <next step>

Watch out:
- <only if important>
```

For screenshots, include a compact table when stats, prices, or listings matter.

For breeding, always include the item table and preview gate.

## Fast-load memory anchors

### Current Prismtek run

```yaml
user: Prismtek
game: PokeMMO
roms:
  kanto: FireRed
  johto: HeartGold
  hoenn: Emerald
  sinnoh: Platinum
  unova: Black
preferences:
  - practical advice first
  - OT-safe when practical
  - stylish balls matter
  - avoid wasted yen
  - favorites are allowed if team roles compensate
```

### Current Kanto plan

```yaml
kanto_team:
  - Hypno
  - Porygon
  - Omastar
  - Nidoking
  - Farfetch'd
  - Hitmonlee_or_Hitmonchan
notes:
  - Porygon replaced Magneton by preference.
  - Snorlax was dropped to avoid Normal-type overload.
  - Nidoking is planned later from higher-level Nidorino/Safari access.
```

### Signature Pokemon

```yaml
moon_ball_drowzee:
  future: Hypno
  role: bulky Psychic / Fighting answer
  ivs:
    hp: 29
    def: 20
    spa: 31
    spd: 21
    spe: 29

luxury_ball_porygon:
  future: Porygon2 / Porygon-Z trilogy
  nature: Mild
  role: special attacker / cross-region digital companion
  ivs:
    hp: 31
    atk: ignore
    def: 21
    spa: 31
    spd: 31
    spe: 29
```

## File map

Use these files in this order:

1. `SKILL.md` — fast-load entrypoint and operating rules.
2. `skill.yaml` — machine-readable manifest for registries/adapters.
3. `POKEMMO_BUDDY_COACH_SKILL.md` — full skill contract and procedures.
4. `POKEMMO_BUDDY_COACH_WIKI.md` — compact first-principles coaching field guide.
5. `POKEMMO_KARPATHY_SOURCEBOOK.md` — broad source map and compressed knowledge architecture for the requested PokeMMO sites.

## Source policy

Use sourcebook knowledge for orientation. Use current public sources or user screenshots for volatile facts such as exact encounter tables, GTL pricing, events, swarm/alpha state, or changed mechanics.

Do not mirror third-party sites verbatim. Compress them into schemas, source roles, decision procedures, and links.
