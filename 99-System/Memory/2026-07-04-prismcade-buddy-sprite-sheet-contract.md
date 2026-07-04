---
type: decision
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-07-04
risk_level: low
privacy: public
freshness: stable
agent_load: task-specific
tags: [prismcade, buddies, pixel-art, spritesheet, dex-entry, animation]
---

# Prismcade Buddy Sprite Sheet Production Contract

> Production sprite sheets and Dex entry sheets are separate deliverables. When Prismtek asks for a sprite sheet, default to the gameplay-ready contract below.

## Decision

Prismcade's original monster-companion creatures are called **Buddies**. They use a cohesive cute, expressive, isometric pixel-art style suitable for Prismcade games.

Current named Buddy starters:

- **Leaflet** — grass-type Buddy.
- **Axolitty** — water-type, axolotl-inspired Buddy.
- **Ignitten** — fire-type, cat-inspired Buddy.

These are original Prismcade creatures. “Pokemon-like” may be used only as shorthand for the monster-companion concept, not as the product identity or a request to copy protected characters.

## Gameplay sprite sheet contract

A normal request for a **sprite sheet** means a production-ready gameplay sheet with all of the following:

- Every frame uses an exact **64x64 pixel cell**.
- The creature may visually occupy roughly 16x16 through 64x64 inside the cell, depending on its body size, but the cell size never changes.
- Every frame keeps a consistent scale, anchor point, baseline, and framing.
- The creature design must match the approved reference exactly across all animations. Adding an animation must not redesign the Buddy.
- Pixel edges must remain crisp with no blur, smoothing, or inconsistent resampling.
- The background must be either:
  - one flat, single-color chroma green with no gradient, texture, checkerboard, or lighting variation, or
  - true RGBA transparency.
- Do not include words, labels, frame numbers, palettes, portraits, info boxes, decorative borders, or presentation graphics.
- Default animation groups are:
  - idle
  - walk
  - attack
- Each animation must support **8-direction gameplay**.
- It is acceptable to render five unique directional rows and derive the remaining three directions through safe horizontal mirroring, provided the result still supports all eight directions in-game.
- Directional attack coverage follows the same rule as movement: all eight gameplay directions must be supported, with mirroring allowed where the silhouette and effect remain correct.
- Sprite dimensions and placement must remain uniform throughout the sheet so Godot or Prismcade can slice it directly.

A sheet that merely looks like a grid but uses inconsistent frame sizes, offsets, scaling, or spacing is not considered usable.

## Dex entry sheet contract

A **Dex entry sheet** is a presentation asset, not a production sprite sheet.

Create this format only when Prismtek explicitly asks for a Dex entry sheet. It may include:

- animation previews
- attack previews
- labels and frame numbers
- palette swatches
- type and ability information
- description text
- a large character portrait
- decorative or themed backgrounds

Never substitute a Dex entry sheet when the request says “sprite sheet.”

## Delivery defaults

Use these defaults unless Prismtek overrides them:

- Gameplay sheet filename: `<buddy-name>_gameplay_64x64.png`
- Dex sheet filename: `<buddy-name>_dex_entry.png`
- Gameplay background: flat chroma green when transparency cannot be guaranteed; otherwise true transparency.
- No text or decorative content on gameplay sheets.

## Validation before claiming a gameplay sheet is ready

Check all of the following:

- Image width and height align cleanly to the intended 64x64 grid.
- Every cell is exactly 64x64.
- The Buddy uses a consistent scale and anchor across frames.
- Idle, walk, and attack are present.
- Eight-direction gameplay is supported directly or through documented mirroring.
- The background is uniformly chroma green or genuinely transparent.
- No labels, numbers, palettes, portraits, or info panels are present.
- The approved Buddy design was preserved exactly.

## Source links

- Source: Explicit Prismtek decisions made during the Buddy sprite-sheet design session on 2026-07-04.
- Related product repo: `codysumpter-cloud/prismtek-site`
- Durable memory home: `codysumpter-cloud/knowledge-vault`

## Known unknowns

- Exact frame count and playback FPS for idle, walk, and attack are not yet standardized.
- Exact row and column ordering is not yet standardized.
- The exact chroma-green color value is not yet standardized.
- Whether ground shadows are baked into gameplay frames is not yet standardized.
- A machine-readable animation manifest format has not yet been selected.

## Agent instructions

- Load this note whenever generating, editing, slicing, importing, or reviewing Prismcade Buddy art.
- Treat “sprite sheet” as the gameplay format by default.
- Treat “Dex entry sheet” as the presentation format only when explicitly requested.
- Do not change an approved Buddy's anatomy, palette, markings, face, proportions, or silhouette when adding new animations.
- Do not claim a gameplay sheet is production-ready without checking the 64x64 grid and frame consistency.
- Do not assume a visually attractive concept sheet is usable as a runtime sprite sheet.

## Next action

- [ ] Define a canonical row order, frame counts, FPS values, mirror rules, and JSON manifest schema for Buddy animation imports.
