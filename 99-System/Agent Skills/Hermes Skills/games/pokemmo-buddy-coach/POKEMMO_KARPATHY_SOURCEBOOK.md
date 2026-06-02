# PokeMMO Karpathy-Style Sourcebook

Status: original synthesis / source map  
Scope: PokeMMO coach knowledge architecture  
Use with: `pokemmo-buddy-coach` Hermes skill  
Last manual seed: 2026-06-02

## Copyright and source boundary

This sourcebook is not a mirror of PokeMMO Wiki, PokeMMO Fandom, PokeMMO Hub, PokeMMO Index, or the official PokeMMO website. It is an original, compressed, first-principles map of the knowledge a coach needs to use those sources well.

Do not copy entire pages, tables, database dumps, sprites, route lists, or tool outputs into KnowledgeVault. Instead:

1. Store source links and source roles.
2. Store schemas and mental models.
3. Store durable rules.
4. Fetch or verify volatile facts when needed.
5. Prefer user screenshots and in-game UI for current state.

The goal is a high-signal coach brain, not a scraped replacement for the public sites.

## Source map

### 1. Official PokeMMO site

URL: `https://pokemmo.com/en/`

Primary use:

- official game positioning
- account/download entrypoint
- official client links
- official news/changelog entrypoints when available
- baseline source for what the project is

Coach rule:

```text
Use the official site for official posture and install/account direction. Do not infer mechanics from the landing page when wiki/tool data is more specific.
```

### 2. ShoutWiki PokeMMO Wiki

URL: `https://pokemmo.shoutwiki.com/wiki/PokeMMO_Wiki:Main_page`

Primary use:

- broad community-maintained reference
- game topics: getting started, regions, Pokemon, items, breeding, trading, PvP, gift shop, add-ons
- mechanics: damage, critical hits, status, weather, level caps, friendship, breeding, catch rate, shinies
- regions: Kanto, Sevii, Johto, Hoenn, Sinnoh, Unova
- locations, NPCs, events, tools, and editing/community docs

Important source note:

- The main page states it is written and maintained by players.
- The main page lists page/file counts and broad topic categories.
- The page footer states the ShoutWiki text license as Creative Commons Attribution 4.0 unless otherwise noted.

Coach rule:

```text
Use ShoutWiki for canonical PokeMMO-specific mechanics and reference pages, but still verify current route/spawn/price facts when the player is about to spend money or time.
```

### 3. Fandom PokeMMO Wiki

URL: `https://pokemmo.fandom.com/wiki/PokeMMO_Wiki`

Primary use:

- alternative community reference
- navigation across basics, advanced mechanics, player mechanics, item mechanics, regions, cities, landmarks, routes, walkthrough-like pages
- cross-check source when ShoutWiki and user memory disagree

Coach rule:

```text
Use Fandom as a second opinion and navigation aid. When Fandom and ShoutWiki conflict, verify with in-game Dex, current forums, or player screenshot before giving an expensive recommendation.
```

### 4. PokeMMO Hub Pokédex

URL: `https://pokemmohub.com/tools/pokedex/`

Primary use:

- Pokédex lookup workflow
- species-level search and filtering
- likely useful for base stats, types, abilities, moves, and encounter-style planning depending current tool data

Coach rule:

```text
Use PokeMMO Hub as an interactive dex/tool source. Do not cache its entire database in KnowledgeVault. Query or verify the needed species when making a specific team or breeding decision.
```

### 5. PokeMMO Index

URL: `https://pokemmo.info/`

Primary use:

- practical tools and fast references
- EV/EXP training horde locations
- EV berry mapping
- Hidden Power / gems reference
- in-game time display
- useful locations by region
- region maps
- level caps
- natures
- roaming legendary/event surface info

Coach rule:

```text
Use PokeMMO Index for quick optimization facts: EV hordes, level caps, nature modifiers, useful locations, and region utility locations. Treat dynamic events and market-like data as volatile.
```

## The mental model

PokeMMO knowledge is a graph, not a book.

```text
Player goal
  -> region
  -> progression gate
  -> team constraint
  -> Pokemon role
  -> species availability
  -> build quality
  -> money/time cost
  -> next action
```

The coach should navigate the graph from the player's current decision, not dump encyclopedic facts.

## Top-level ontology

```yaml
pokemmo:
  game:
    - account
    - client
    - roms
    - regions
    - progression
    - level_caps
    - story_gates
  pokemon:
    - species
    - forms
    - types
    - abilities
    - base_stats
    - moves
    - evolution
    - encounters
    - hordes
    - swarms
    - phenomena
    - alphas
    - shinies
  builds:
    - role
    - nature
    - ivs
    - evs
    - moveset
    - item
    - ball
    - ot
  economy:
    - yen
    - gtl
    - breeding_costs
    - braces
    - everstones
    - vouchers
    - items
    - money_routes
  multiplayer:
    - trading
    - teams
    - pvp
    - events
  tools:
    - pokedex
    - map
    - ev_training
    - hidden_power
    - calculators
```

## The core loop

Every gameplay answer should reduce to this:

```text
state -> constraint -> option set -> cost -> recommendation -> next action
```

Example:

```text
State: Celadon, Kanto, Porygon project, low yen.
Constraint: Wants Luxury Ball OT signature Porygon, no wasted breeding.
Options: stop, fix SpD, chase Def.
Cost: SpD fix is one targeted Ditto; Def chase is luxury.
Recommendation: fix SpD if trilogy, then stop.
Next action: buy Ditto with 31 HP / 31 SpA / 31 SpD.
```

## Region model

PokeMMO is multi-region. Region knowledge should be stored as modules.

```yaml
region:
  name: Kanto
  rom_family: FireRed
  port_city: Vermilion City
  daycare:
    story_daycare: Route 5
    breeding_daycare: Four Island
  department_store: Celadon City
  magnetic_field: Power Plant
  mossy_rock: Viridian Forest
  icy_rock: Seafoam Islands
  level_caps:
    start: 20
    one_badge: 26
    two_badges: 32
    three_badges: 37
    four_badges: 46
    five_badges: 47
    six_badges: 50
    seven_badges: 55
    eight_badges: 62
    after_e4: 100
```

Use this pattern for every region.

## Five-region utility map

This is a high-level map for coaching. Verify specific details if the player is about to spend resources.

```yaml
kanto:
  port: Vermilion City
  daycare: Route 5 / Four Island
  bp_exchange: Trainer Tower
  tm_store: Celadon City
  mossy_rock: Viridian Forest
  icy_rock: Seafoam Islands
  magnetic_field: Power Plant

johto:
  port: Olivine City
  daycare: Route 34
  tm_store: Goldenrod City
  mossy_rock: Ilex Forest
  icy_rock: Ice Path
  magnetic_field: Team Rocket HQ
  red: Mt. Silver

hoenn:
  port: Slateport City
  daycare: Route 117
  bp_exchange: Battle Frontier
  tm_store: Lilycove City
  mossy_rock: Petalburg Woods
  icy_rock: Shoal Cave Ice Room
  magnetic_field: New Mauville

sinnoh:
  port: Pastoria City
  daycare: Solaceon Town
  tm_store: Veilstone City
  mossy_rock: Eterna Forest
  icy_rock: Route 217
  magnetic_field: Mt. Coronet

unova:
  port: Castelia City
  daycare: Route 3
  bp_exchange: Nimbasa City / Gear Station
  tm_store: Route 9
  mossy_rock: Pinwheel Forest
  icy_rock: Twist Mountain
  magnetic_field: Chargestone Cave
```

## Level cap model

Level caps decide whether training is useful or self-sabotage.

Use level caps as a hard planning constraint.

```yaml
level_caps:
  kanto:  [20, 26, 32, 37, 46, 47, 50, 55, 62, 100]
  johto:  [20, 24, 29, 32, 37, 39, 41, 46, 48, 55, 100]
  hoenn:  [20, 24, 28, 33, 35, 38, 44, 48, 58, 100]
  sinnoh: [20, 27, 29, 34, 37, 43, 46, 52, 60, 100]
  unova:  [20, 24, 27, 31, 35, 38, 43, 46, 56, 100]
```

Interpretation:

```text
Index meaning is progression-dependent. Always explain in player terms: current badge count -> current cap -> safe training target.
```

Johto has a special Ho-Oh step where the cap rises to 55 before the Elite Four.

## Nature model

Natures are a 10% stat trade. Coaching should translate the nature into role impact.

```yaml
attack_up:
  Lonely:  {up: Attack, down: Defense}
  Brave:   {up: Attack, down: Speed}
  Adamant: {up: Attack, down: Special Attack}
  Naughty: {up: Attack, down: Special Defense}

defense_up:
  Bold:    {up: Defense, down: Attack}
  Relaxed: {up: Defense, down: Speed}
  Impish:  {up: Defense, down: Special Attack}
  Lax:     {up: Defense, down: Special Defense}

speed_up:
  Timid: {up: Speed, down: Attack}
  Hasty: {up: Speed, down: Defense}
  Jolly: {up: Speed, down: Special Attack}
  Naive: {up: Speed, down: Special Defense}

special_attack_up:
  Modest: {up: Special Attack, down: Attack}
  Mild:   {up: Special Attack, down: Defense}
  Quiet:  {up: Special Attack, down: Speed}
  Rash:   {up: Special Attack, down: Special Defense}

special_defense_up:
  Calm:    {up: Special Defense, down: Attack}
  Gentle:  {up: Special Defense, down: Defense}
  Sassy:   {up: Special Defense, down: Speed}
  Careful: {up: Special Defense, down: Special Attack}
```

Neutral natures are not bad for story. Bad natures are only bad relative to role.

## IV model

IVs are a role filter, not a beauty contest.

```yaml
special_attacker:
  must: Special Attack
  wants: Speed, HP
  nice: Defense, Special Defense
  ignore: Attack

physical_attacker:
  must: Attack
  wants: Speed, HP
  nice: Defense, Special Defense
  ignore: Special Attack

bulky_special:
  must: HP, Special Defense
  wants: Special Attack, Defense
  ignore: Attack

bulky_physical:
  must: HP, Defense
  wants: Attack, Special Defense
  ignore: Special Attack

utility_catcher:
  must: move_access
  wants: Speed, bulk
  ignore: perfect_damage_stats
```

Coach phrasing:

```text
This is not perfect, but it is perfect enough for the job.
```

## EV model

EVs declare the final job.

Use two-max-stat defaults unless the user asks for PvP-style fine tuning.

```yaml
fast_special:
  evs: 252 SpA / 252 Spe / 6 HP

bulky_special_story:
  evs: 252 HP / 252 SpA / 6 Spe

physical_sweeper:
  evs: 252 Atk / 252 Spe / 6 HP

bulky_physical_story:
  evs: 252 HP / 252 Atk / 6 Def

catcher:
  evs: enough_speed_then_bulk
```

EV berry mapping:

```yaml
Pomeg: lowers HP EVs by 10
Kelpsy: lowers Attack EVs by 10
Qualot: lowers Defense EVs by 10
Hondew: lowers Special Attack EVs by 10
Grepa: lowers Special Defense EVs by 10
Tamato: lowers Speed EVs by 10
```

## EV horde map

Use horde spots as a practical optimization layer. Verify if route access or horde composition matters.

```yaml
kanto:
  hp: Route 14, 5x Nidorina
  attack: Route 15, 5x Nidorino
  defense: Cape Brink, 5x Slowbro
  special_attack: Cape Brink surf, 5x Golduck
  special_defense: Trainer Tower / Island 7 surf, 5x Tentacruel
  speed: Five Isle Meadow, 5x Pidgeotto
  exp: Cerulean Cave surf, 5x Golduck

johto:
  hp: Route 44, 5x Lickitung
  attack: Mt. Silver Cave, 5x Machoke
  defense: Route 45, 5x Gligar
  special_attack: Route 43, 5x Flaaffy/Girafarig
  special_defense: Route 41 surf, 5x Mantine
  speed: Blackthorn City surf, 5x Poliwhirl
  exp: Mt. Silver surf, 5x Poliwhirl

hoenn:
  hp: Victory Road, 5x Hariyama
  attack: Route 120, 5x Mightyena
  defense: Magma Hideout, 5x Torkoal
  special_attack: Route 119, 5x Gloom
  special_defense: Battle Frontier surf, 5x Tentacruel
  speed: Route 121, 5x Linoone
  exp: Battle Frontier surf, 5x Tentacruel

sinnoh:
  hp: Route 230 surf, 5x Sealeo
  attack: Route 211 East, 5x Machoke
  defense: Route 222 surf, 5x Pelipper
  special_attack: Resort Area surf, 5x Golduck
  special_defense: Pokemon League surf, 5x Tentacruel
  speed: Route 225, 5x Raticate/Fearow
  exp: Stark Mountain, 5x Camerupt

unova:
  hp: Route 10, 5x Amoonguss
  attack: Route 10, 5x Bouffalant
  defense: Undella Bay surf, 5x Pelipper
  special_attack: Route 11, 5x Golduck
  special_defense: Undella Town surf, 5x Mantine
  speed: Route 12, 5x Rapidash
  exp: Giant Chasm dark grass, 5x Piloswine
```

## Breeding model

PokeMMO breeding is not vanilla Pokemon breeding. It is deterministic enough to plan, expensive enough to punish mistakes, and destructive enough to demand preview gates.

### Power items

```yaml
Power Weight: HP
Power Bracer: Attack
Power Belt: Defense
Power Lens: Special Attack
Power Band: Special Defense
Power Anklet: Speed
Everstone: nature
```

### Genderless rule

```text
Genderless Pokemon breed only with Ditto.
```

For Porygon, every breed is a replacement, not a copy.

### Preservation rule

```text
A completed 31 can be safely preserved without bracing only when both parents share that 31.
```

## GTL model

The GTL is not a shop; it is a market.

Price is a function of:

```yaml
price:
  species_demand: high | medium | low
  gender: male | female | genderless
  egg_group_utility: high | low
  iv_spread: useful | pretty | bad
  nature: role_fit | neutral | bad
  ball: style_bonus
  hidden_ability_or_alpha: optional_bonus
  scarcity: current_supply
```

Good buys are not always cheap. Good buys are underpriced relative to use.

## Ditto model

Ditto is special because it is universal breeder infrastructure, especially for genderless projects.

A high-IV Ditto is valuable because it cannot be produced by breeding a better Ditto.

```yaml
valuable_ditto:
  single_useful_31:
    - HP
    - Defense
    - Special Attack
    - Special Defense
    - Speed
  niche_zero:
    - 0 Attack
    - 0 Speed
  expensive_combo:
    - HP + Special Attack
    - HP + Special Attack + Special Defense
    - HP + Defense + Special Defense
    - HP + Defense + Special Attack + Special Defense + Speed
```

Coach rule:

```text
Do not tell the player to buy a multi-million Ditto unless it unlocks repeated breeding value beyond one story Pokemon.
```

## Money model

Income has stability tiers.

```yaml
low_setup:
  - story progression
  - trainer battles
  - item pickup

stable_midgame:
  - trainer rematches
  - Amulet Coin route planning

stable_postgame:
  - gym reruns
  - E4 rematches when appropriate

lottery_plus_income:
  - Ditto boxes
  - alpha catching
  - valuable held-item farming

market_skill:
  - GTL flipping
  - breeder arbitrage
  - vanity/event speculation
```

The coach should recommend stable money first, then lottery upside.

## Encounter model

Wild Pokemon value has three separate questions:

```text
Can it appear here?
Can I access the area now?
Is this the right time to hunt it?
```

A good encounter answer includes:

- region
- location
- method
- time/weather/lure/special condition if relevant
- level range if known
- rarity if known
- whether the target is worth hunting now

## Lure model

A lure does not generally mean "any Pokemon can appear here." It modifies encounter flow and may enable location-specific lure pools.

Coach rule:

```text
Only recommend lure spending when the target is lure-exclusive, encounter rate matters enough, or the player's goal is worth the consumable.
```

## Ball model

Balls are not just catch rate; for this player, they are identity.

Use ball style when it matters and cost is reasonable.

Examples:

```yaml
Moon Ball:
  vibe: sleep, dreams, psychic, night, occult
  good_for: Drowzee, Hypno, Umbreon-like projects, ghost/psychic themes

Luxury Ball:
  vibe: premium, signature, main-character
  good_for: Porygon trilogy, friendship evolutions, long-term companions

Nest Ball:
  vibe: green, route-caught, early-life, cozy
  good_for: low-level catches or color matching
```

## Team planning model

A team is a set of jobs, not six favorites stapled together.

Each region team should have:

```yaml
team_jobs:
  - physical_damage
  - special_damage
  - bulky_switch
  - status_or_utility
  - coverage_for_elite_four
  - favorite_or_identity_slot
```

Favorites are allowed. The team must compensate around them.

## Prismtek five-region team plan

```yaml
kanto:
  team:
    - Hypno
    - Porygon
    - Omastar
    - Nidoking
    - Farfetch'd
    - Hitmonlee_or_Hitmonchan
  identity: weird Kanto custom squad with Moon Ball Hypno and Luxury Porygon

johto:
  team:
    - Ampharos
    - Crobat
    - Heracross
    - Mamoswine
    - Donphan
    - Togetic_or_Togekiss
  identity: chunky Johto utility and friendship arc

hoenn:
  team:
    - Gallade
    - Milotic
    - Absol
    - Castform
    - Kecleon
    - Smeargle
  identity: stylish oddball challenge team

sinnoh:
  team:
    - Garchomp
    - Floatzel
    - Roserade
    - Rapidash
    - Scizor
    - Magnezone
  identity: high-power Sinnoh clear team

unova:
  team:
    - Krookodile
    - Chandelure
    - Galvantula
    - Sigilyph
    - Haxorus
    - Sawk
  identity: clean power team
```

## Current Prismtek signature mons

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
  note: strong story mon; keep Hypnosis

luxury_ball_porygon:
  future: Porygon2/Porygon-Z trilogy
  nature: Mild
  role: special attacker / signature digital companion
  ivs:
    hp: 31
    atk: 16
    def: 21
    spa: 31
    spd: 31
    spe: 29
  note: complete; do not spend millions fixing Defense for story
```

## Website-specific usage strategy

### When answering species/location questions

Use:

1. In-game Dex screenshot if the user has it.
2. PokeMMO Hub / Index / ShoutWiki species page.
3. Fandom as cross-check.
4. Forums for edge cases and recent changes.

### When answering mechanics questions

Use:

1. ShoutWiki mechanics pages.
2. Fandom mechanics pages.
3. Official support/rules pages when safety/policy matters.

### When answering route/progression questions

Use:

1. User's current location screenshot.
2. Region route map pages.
3. Walkthrough pages only as scaffolding, not as source to copy.

### When answering money/market questions

Use:

1. Current user GTL screenshots.
2. Current GTL manual price checks by user.
3. Community guides only for method classes, not exact guaranteed income.

### When answering EV training questions

Use:

1. PokeMMO Index EV/EXP horde table.
2. PokeMMO wiki EV Training page as cross-check.
3. User's access/progression constraints.

## Data extraction plan for a future local app

Do not scrape and republish full third-party databases.

Instead, build adapters like:

```yaml
adapters:
  source_registry:
    stores: source name, URL, license note, volatility
  species_query:
    input: species name
    output: links to authoritative pages and current user-noted facts
  ev_spot_query:
    input: region, ev_stat
    output: recommended spot with source link and last_verified timestamp
  breeding_planner:
    input: parent summaries and goal
    output: deterministic item plan and preview gate
  gtl_advisor:
    input: screenshot/manual listing
    output: buy/skip/sell recommendation
```

## Volatility labels

```yaml
stable:
  - type chart
  - nature modifiers
  - broad region structure
  - breeding item stat mapping

slow_changing:
  - level caps
  - daycare locations
  - utility locations
  - move tutor/TM locations

volatile:
  - GTL prices
  - event schedules
  - alpha calls
  - swarms
  - roamer availability
  - exact encounter tables after patches
```

Use volatility to decide when to browse or ask for a screenshot.

## Response recipes

### Keep/breed/sell

```text
Verdict: Keep. Do not breed again.

Why:
- It has the role-critical IVs.
- The weak stat is not worth the next spend.
- The matchup problem is solved by another team member.

Do this:
1. EV train SpA.
2. Add HP or Speed depending final role.
3. Move on to the next team slot.
```

### Buy/skip GTL

```text
Verdict: Buy the cheaper one.

Why:
- It has the required locked stat.
- The expensive one only improves a non-critical stat.
- The saved yen matters more right now.

Before buying:
- Confirm species.
- Confirm IVs.
- Confirm price.
```

### Route next step

```text
Verdict: Go to Celadon now.

Route:
1. Heal.
2. Go west.
3. Use Underground Path.
4. Enter Celadon.

Why:
- Lavender Tower needs Silph Scope first.
```

### Money plan

```text
Verdict: Do not gamble for income.

Do this:
1. Finish story gates.
2. Unlock trainer/gym reruns.
3. Build a catcher.
4. Farm Dittos for upside.
```

## What this sourcebook should become

This document should eventually split into smaller pages:

```text
/wiki/sources.md
/wiki/regions.md
/wiki/builds.md
/wiki/breeding.md
/wiki/ev-training.md
/wiki/economy.md
/wiki/team-plans.md
/wiki/safety.md
```

For now, keep one sourcebook because the skill is young and the mental model matters more than perfect file granularity.

## Final principle

The player does not need an encyclopedia in the chat window.

The player needs the next correct move.

```text
Compress the internet into decisions.
```
