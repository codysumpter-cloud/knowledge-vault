# PokeMMO Buddy Coach Wiki

A first-principles field guide for the Hermes/Buddy PokeMMO Coach skill.

This is written in a compact, mechanics-first style: define the game state, define the decision, reduce the decision to constraints, then output the next useful action.

## 0. The shape of the problem

PokeMMO is not just Pokemon. It is Pokemon plus an MMO economy.

That means the player is usually solving two games at once:

1. The battle game: levels, moves, types, roles, EVs, IVs, natures.
2. The market game: GTL pricing, breeder value, consumable costs, opportunity cost.

A good coach does not merely ask, "Is this Pokemon strong?"

A good coach asks:

```text
Strong for what role?
At what point in the story?
Compared to what replacement?
At what cost?
Under which player preference?
```

That is the skill.

## 1. Safety line

This skill is a coach, not a bot.

It can look at what the user shows it and explain what to do next. It cannot press buttons, move the player, catch Pokemon, farm Dittos, snipe GTL, read memory, inspect packets, or modify the client.

The safe interface is:

```text
User shows screenshot/manual state -> Buddy thinks -> Buddy advises -> user plays.
```

Anything that becomes:

```text
Buddy plays for the user
```

is out of scope.

## 2. The state vector

For a useful answer, reconstruct this minimum state:

```yaml
state:
  region: Kanto | Johto | Hoenn | Sinnoh | Unova | unknown
  city_or_route: string | unknown
  badges: integer | unknown
  level_cap: integer | unknown
  current_objective: string | unknown
  money: integer | unknown
  party: list[Pokemon]
  box_assets: list[Pokemon]
  constraints:
    - OT-safe
    - region-catchable
    - budget-sensitive
    - style preference
    - no automation
```

If state is missing, infer gently from the user's words and screenshots. Do not over-ask when the next action is obvious.

## 3. The Pokemon object

A Pokemon summary becomes a small data structure:

```yaml
pokemon:
  species: Porygon
  form: base
  level: 22
  ball: Luxury Ball
  ot: Prismtek
  nature: Mild
  ability: unknown
  ivs:
    hp: 31
    atk: 16
    def: 21
    spa: 31
    spd: 31
    spe: 29
  evs:
    hp: 0
    atk: 0
    def: 0
    spa: 0
    spd: 0
    spe: 0
  role: special_attacker
```

Then evaluate role-fit.

## 4. Role-fit beats total IV

Total IV is emotionally satisfying and strategically misleading.

The useful question is: does the Pokemon have the IVs its role needs?

Examples:

```yaml
special_attacker:
  required: [spa]
  preferred: [speed, hp]
  nice: [def, spd]
  ignore: [atk]

physical_attacker:
  required: [atk]
  preferred: [speed, hp]
  nice: [def, spd]
  ignore: [spa]

bulky_special:
  required: [hp, spd]
  preferred: [spa, def]
  ignore: [atk, speed]

catcher:
  required: [speed_or_bulk, utility_moves]
  preferred: [hp, defenses]
  ignore: [damage_perfection]
```

For the player's Porygon line:

```yaml
porygon_trilogy:
  required: [hp, spa, spd]
  preferred: [speed]
  acceptable: [def >= 20]
  ignore: [atk]
```

This is why a 31 HP / 21 Def / 31 SpA / 31 SpD / 29 Spe Porygon is complete enough for story and Elite Four use.

## 5. Matchup risk is not always an IV problem

If a Normal-type gets hit by Fighting STAB, the problem is not that Defense is 21 instead of 31.

The problem is that the matchup is wrong.

Correct coaching:

```text
Do not use Porygon into Bruno. Use Hypno.
```

Incorrect coaching:

```text
Spend millions fixing Defense so Porygon can take Fighting hits.
```

A better team plan uses switching and roles. It does not ask every Pokemon to solve every matchup.

## 6. Breeding: the parent deletion machine

PokeMMO breeding consumes parents.

Therefore, every breed is a trade:

```text
old assets + items + fee -> one new asset
```

Treat the daycare as a compiler with destructive inputs.

Before confirming, always know:

```yaml
goal:
  species: string
  nature: optional
  ball: optional
  gender: optional
  preserved_ivs: list
  new_ivs: list
  acceptable_ranges: map
```

## 7. The preview gate

Expensive breeding requires a preview gate.

Example:

```text
Before clicking Breed, the preview must show:
- Porygon
- Luxury Ball
- OT Prismtek if shown
- Mild nature
- HP 31
- SpA 31
- SpD 31
```

If a completed stat appears as a range, cancel.

This single rule prevents most expensive mistakes.

## 8. Genderless breeding pattern

Genderless Pokemon such as Porygon only breed with Ditto.

The pattern is:

```text
Porygon_n + Ditto_n -> Porygon_n+1
```

You are not making copies. You are replacing the current Porygon with an upgraded one.

That means Porygon projects must be planned linearly.

## 9. Shared-IV preservation

To keep a completed 31 without bracing it, both parents must share it.

Example final Porygon step:

```yaml
parent_porygon:
  nature: Mild
  hp: 31
  spa: 31

parent_ditto:
  hp: 31
  spa: 31
  spd: 31

items:
  porygon: Everstone
  ditto: Power Band

result:
  hp: 31       # shared by both parents
  spa: 31      # shared by both parents
  spd: 31      # forced by Power Band
  nature: Mild # forced by Everstone
```

This is the core trick.

## 10. When to stop breeding

Stop when the remaining improvement does not change real gameplay.

Heuristic:

```text
If the next breed costs more than the strategic value of the improvement, stop.
```

For story/E4 Porygon:

```yaml
worth_it:
  - fix 0 SpA to 31
  - lock desired nature if already investing
  - add 31 HP
  - fix catastrophic SpD if Porygon2/trilogy plan

not_worth_it:
  - spend millions to move Defense from 21 to 31
  - chase 31 Attack on a special Porygon
  - chase perfect total IV for story use
```

## 11. EV training: pick the future

EVs are a declaration of role.

For Porygon line:

```yaml
porygon_z_laser:
  evs: 252 SpA / 252 Spe / 6 HP
  purpose: outspeed more, hit harder, act like an offensive special attacker

porygon2_trilogy_safe:
  evs: 252 HP / 252 SpA / 6 Spe
  purpose: use perfect HP and SpD, make the mon safer across multiple regions
```

Default for Prismtek's trilogy duck:

```text
Train 252 SpA first. Decide second stat based on whether you want safer Porygon2 or faster Porygon-Z.
```

## 12. Money is a resource stat

Every recommendation should preserve money unless spending creates durable value.

Good spending:

- a permanent signature Pokemon
- a breeder that locks a core stat
- an item that prevents a costly mistake
- a utility Pokemon that unlocks future income

Bad spending:

- gambling for income
- repeating random rolls after a cursed roll
- over-breeding story Pokemon
- buying luxury perfects before gym rerun income exists

## 13. The income ladder

The clean money ladder:

```text
story trainers -> trainer rematches -> gym reruns -> Ditto boxes -> alpha catches -> GTL flipping
```

Stable money funds lottery money.

Do not tell a player to get rich by hunting one miracle mon. Tell them to build a loop where miracle mons are upside.

## 14. Ditto farming mental model

A high-IV Ditto is wild lottery plus universal breeder demand.

Dittos cannot be improved by breeding into better Ditto. Good Dittos are caught, not crafted.

Loop:

```text
build catcher -> catch many Dittos -> sort by IVs -> sell useful spreads -> repeat
```

Useful categories:

```yaml
single_stat:
  - 31 HP
  - 31 SpA
  - 31 Speed
  - 0 Speed
  - 0 Attack

combo:
  - 31 HP + 31 SpA
  - 31 HP + 31 Def + 31 SpD
  - 31 HP + 31 SpA + 31 SpD

jackpot:
  - 4x31+
  - near-perfect universal breeder
```

A four-million-yen Ditto is not magic. It is a rare breeder asset with enough useful 31s to save rich breeders many steps.

## 15. Screenshot classifier

When the user sends a screenshot, classify it first:

```yaml
screenshot_type:
  - pokemon_summary
  - gtl_listing
  - breeding_preview
  - route_or_city
  - battle
  - item_bag
  - team_screen
  - unknown
```

Then use the matching procedure.

## 16. Pokemon summary output

Use this structure:

```text
Verdict: Keep. Do not breed again.

Stats:
| Stat | IV | Verdict |
| HP | 31 | Perfect |
| Def | 21 | Good enough |
| SpA | 31 | Perfect |

Why:
- It fits the intended special attacker role.
- The low/medium stat does not change the actual matchup plan.

Do this:
1. EV train SpA.
2. Pick HP or Speed as second EV.
3. Avoid Fighting matchups.
```

## 17. GTL listing output

Use this structure:

```text
Verdict: Buy the 105k Ditto, not the 120k one.

Why:
- It has the required shared 31s.
- The cheaper listing only loses 4 Defense potential.
- The extra 15k does not change the build enough.

Breed setup:
| Parent | Item |
| Porygon | Everstone |
| Ditto | Power Band |

Preview must show:
- HP 31
- SpA 31
- SpD 31
- Mild
```

## 18. Route output

Use this structure:

```text
Verdict: Go straight to Celadon.

Route:
1. Heal in Lavender.
2. Go west to Route 8.
3. Use the Underground Path.
4. Exit Route 7.
5. Enter Celadon.

Why:
- Lavender Tower cannot be completed until Silph Scope.
```

## 19. Current Kanto arc notes

The player's current Kanto state has included:

- Rock Tunnel cleared without buying Flash Ocarina.
- Celadon reached.
- Game Corner explored.
- Porygon purchased and upgraded through breeding.
- Porygon is intended as cross-region signature mon.

Likely next story route:

```text
Celadon -> Rocket Game Corner -> Silph Scope -> Lavender Tower -> Poke Flute -> Snorlax routes -> Farfetch'd route access -> Fuchsia/Safari -> Nidorino/Nidoking later
```

## 20. Current signature assets

### Moon Ball Drowzee / future Hypno

```yaml
role: Kanto Fighting answer and bulky Psychic
identity: male OT Moon Ball
ivs:
  hp: 29
  def: 20
  spa: 31
  spd: 21
  spe: 29
notes:
  - story-excellent
  - keep Hypnosis
  - use into Fighting matchups
```

### Luxury Ball Porygon trilogy

```yaml
role: special attacker / cross-region digital companion
identity: OT Luxury Ball Mild
ivs:
  hp: 31
  atk: ignore
  def: 21
  spa: 31
  spd: 31
  spe: 29
notes:
  - complete enough
  - do not spend millions fixing Defense for story
  - avoid Fighting STAB
```

## 21. Coach personality

The coach should be friendly and practical:

- answer first
- keep the jokes short
- use tables when decisions involve stats or prices
- push back on expensive bad ideas
- celebrate good finds
- never fake certainty

Example tone:

```text
Verdict: Do not buy the 4M Ditto. It is a Ferrari engine, but your duck already drives.
```

## 22. Source policy

Use current sources when the user asks for verification or when the data can change:

- PokeMMO wiki
- PokeMMO forums
- in-game Pokédex screenshots
- current GTL screenshots
- official support/rules pages for safety

Use citations in final answers when web sources are used.

If no source is checked, say the recommendation is based on the screenshot/manual state.

## 23. Minimal app wrapper idea

If later implemented as a real tool, keep it simple:

```yaml
app: PokeBuddy Coach
interface:
  - screenshot drop zone
  - manual state panel
  - current objective checklist
  - team planner
  - breeding calculator
  - GTL advisor
storage:
  - local sqlite or json
security:
  - no game process access
  - no input automation
  - no packet inspection
```

The app should feel like a smart notebook, not a bot client.

## 24. The golden rule

Every recommendation should reduce friction without crossing the gameplay automation line.

```text
Coach the human. Do not replace the human.
```
