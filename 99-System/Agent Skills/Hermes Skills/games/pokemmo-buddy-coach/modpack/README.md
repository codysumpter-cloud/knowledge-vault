# PokeMMO Buddy Modpack Index

Status: source-index / installer-runbook, not bundled third-party mod binaries  
Owner: Prismtek / Buddy ecosystem  
Use with: `pokemmo-buddy-coach`

## Why this exists

This folder gives Buddy/Hermes a clean way to help Prismtek install and manage PokeMMO visual/audio/UI mods without digging through forum threads every time.

It intentionally does **not** vendor every third-party mod file into KnowledgeVault. Most PokeMMO mods are community-authored assets with their own permissions, update cadence, credits, and redistribution expectations. The safe pattern is:

```text
curated index + source links + install steps + local cache path + safety rules
```

not:

```text
copy every forum mod into this repo
```

## Load order

1. `README.md` — fast entrypoint.
2. `modpack.yaml` — machine-readable pack manifest.
3. `POKEMMO_MODPACK_INDEX.md` — human-readable curated index and policy.
4. `POKEMMO_MOD_INSTALL_RUNBOOK.md` — install/update/check workflow.
5. `MOD_ENTRY_SCHEMA.json` — schema for future mod entries.

## Hard boundary

Allowed:

- visual mods
- music/sound mods
- UI themes
- follower sprite mods
- documentation links
- local install checklists
- license/credit tracking

Forbidden:

- ROMs or ROM patches
- PokeMMO client patches
- automation, macros, bots, shiny scanners, GTL snipers, memory readers, packet inspection, or input controllers
- vendoring third-party mods without a clear redistribution license or explicit permission
- claiming a mod is safe/current without verification

## Local install philosophy

KnowledgeVault stores the map. Your local machine stores the downloaded mod files.

Suggested local cache:

```text
~/Games/PokeMMO/modpacks/prismtek-buddy/
  downloads/
  enabled/
  disabled/
  receipts/
```

Buddy can later read this index, check the user's local cache, and produce a simple install/update checklist.
