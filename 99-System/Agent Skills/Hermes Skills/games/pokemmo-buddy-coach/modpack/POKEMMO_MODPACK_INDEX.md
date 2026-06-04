# PokeMMO Modpack Source Index

This is a curated operating index for PokeMMO client customization. It is designed for Buddy/Hermes to quickly decide what kind of mod to recommend, where to fetch it, how to verify it, and how to avoid ban-risk tools.

## Core rule

```text
Package the knowledge and installer flow. Do not package unlicensed third-party mod binaries.
```

## Primary discovery sources

| Source | Role | URL |
|---|---|---|
| PokeMMO Forums Client Customization | Primary source for mods, themes, releases, updates, and author notes | `https://forums.pokemmo.com/index.php?/forum/33-client-customization/` |
| PokeMMO Support: Mods and Themes | Official install guidance | `https://support.pokemmo.com/knowledgebase/article/how-to-use-mods-and-themes` |

## What belongs in the Prismtek pack

### Tier 1: safe visual identity mods

These are the best first targets.

```yaml
safe_visual_identity:
  - follower sprite mods
  - battle sprite packs
  - clean UI themes
  - music or sound replacement packs
  - visual-only quality of life changes
```

Selection criteria:

- active or recently maintained thread
- clear screenshots/previews
- no executable installer required
- no account login required
- no automation claims
- author credit is clear
- download source is transparent
- install/uninstall instructions are simple

### Tier 2: optional style mods

```yaml
optional_style:
  - custom fonts if license allows redistribution
  - alternate battle backgrounds
  - nostalgia audio packs
  - icon replacements
```

Selection criteria:

- does not reduce readability
- easy to disable
- does not obscure important battle/menu info

### Tier 3: reject by default

```yaml
reject:
  - shiny scanners
  - encounter scanners
  - GTL snipers
  - memory readers
  - packet tools
  - macros
  - bot clients
  - input automation
  - account helpers
  - ROM bundles
  - client patches
```

If a thread or download uses these words, treat it as unsafe until proven otherwise:

```text
bot, macro, auto, automate, scanner, memory, packet, hook, inject, snipe, farm, clicker, controller, bypass, exploit
```

## Recommended Prismtek mod slots

| Slot | Category | Priority | What to look for |
|---|---|---:|---|
| Followers | follower sprites | High | Clean follower sprites that make the overworld feel alive |
| UI | theme | High | Dark/readable theme with good menu contrast |
| Battle visuals | sprites/backgrounds | Medium | Better visuals without visual clutter |
| Audio | music/sound | Low | Nostalgic or cleaner audio pack |
| Utility visuals | visual-only QoL | Medium | Better readability, no automation |

## Mod entry template

```yaml
id: example_mod_id
name: Example Mod
category: follower_sprites
source_url: https://forums.pokemmo.com/...
author: Unknown until verified
license_or_permission: unknown
retrieved_at: YYYY-MM-DD
redistribution:
  allowed: false
  evidence: none
install_type: mod_management_import
local_filename: example.mod
status: candidate
safety:
  executable: false
  automation: false
  memory_access: false
  packet_access: false
notes:
  - Verify latest thread comments before recommending.
```

## Candidate evaluation checklist

Before adding a mod to the recommended pack:

1. Open the source thread.
2. Confirm the mod is for current PokeMMO client customization.
3. Confirm it is visual/audio/theme only.
4. Confirm it does not require an executable helper.
5. Confirm the author and credits.
6. Confirm download URL and file type.
7. Record retrieval date.
8. Record install instructions.
9. Record uninstall instructions.
10. Mark redistribution status.

## Why not mirror the forum

PokeMMO mods are community assets. Mirroring them into a public repo can create problems:

- missing author permission
- stale files
- broken credits
- license ambiguity
- accidental redistribution of assets the author only intended to host in their own thread
- larger repo size
- increased risk of accidentally bundling unsafe tools

The better product is a **curated pack manager brain**: Buddy knows what to fetch, what to avoid, where to put it, and how to explain it.

## Future upgrade path

A later local tool can read `modpack.yaml` and entries using `MOD_ENTRY_SCHEMA.json`, then:

1. show candidate mods
2. open source pages for the user
3. download only after explicit confirmation
4. store files in a local cache
5. write receipts
6. copy/import selected mods into PokeMMO's Mod Management flow

The tool must still avoid automation against PokeMMO gameplay.
