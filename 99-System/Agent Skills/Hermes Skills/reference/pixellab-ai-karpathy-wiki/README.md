---
type: source
status: reference
owner: Prismtek
source_of_truth: mixed
last_verified: 2026-08-06
risk_level: low
privacy: public
freshness: volatile
agent_load: task-specific
tags:
  - pixellab
  - pixel-art
  - game-assets
  - animation
  - tilesets
  - inpainting
  - mcp
  - karpathy-wiki
---

# PixelLab AI — Karpathy-Style Production Wiki

> A mental-model-first guide to using PixelLab as a constraint-preserving production system for consistent, game-ready pixel art.

## Purpose

This source pack turns PixelLab's tutorials, current documentation, and indexed video catalogue into compact operating knowledge for Prismtek, Buddy, Hermes, and future agents.

It is intentionally not a transcript mirror. The goal is to preserve:

- the smallest useful mental models
- the dependency order between tools
- repeatable production loops
- failure modes and recovery paths
- source links and freshness warnings
- implications for directional characters, outfits, animation packs, maps, and AI-assisted game workflows

## Evidence status

**Source-backed:** The concepts in this wiki were checked against PixelLab's current documentation, current product pages, officially embedded tutorial links, indexed YouTube metadata, and a third-party mirror collection that identifies many PixelLab videos by original YouTube ID.

**Blocked:** YouTube did not expose a complete, newest-first channel feed or complete caption set to the available research tools on 2026-08-06. A mirror collection labels PixelLab material as a 67-video set, but that count and ordering are not an official channel export.

**Do not assume:** This note does not prove that every channel video was watched frame-by-frame. See [`VIDEO-INVENTORY.md`](VIDEO-INVENTORY.md) and [`RESEARCH-RECEIPT.md`](RESEARCH-RECEIPT.md) for exact coverage.

## The one big idea

PixelLab is most useful when treated as an **iterative constrained editor**, not a one-shot prompt box.

The production loop is:

```text
reference
  -> constrained generation
  -> select what works
  -> freeze stable pixels / frames
  -> repair only the failing region or motion
  -> reuse the corrected result as stronger guidance
  -> repeat until export-ready
```

A weak workflow asks the model to recreate the whole asset every time.

A strong workflow converts every accepted result into additional supervision for the next pass.

## The asset-state tensor

A game asset is not one undifferentiated image. Model it as a point in a set of mostly independent axes:

```text
asset = f(
  identity,
  visual_style,
  projection,
  direction,
  body_state,
  outfit,
  pose,
  animation_time,
  environment_context,
  export_topology
)
```

Examples:

- **Identity:** Ani Iso Human, Shiba Inu, Balinese Cat, Reptar-like dinosaur
- **Visual style:** outline weight, palette, detail density, shading language
- **Projection:** sidescroller, high top-down, low top-down, isometric, oblique
- **Direction:** north, northeast, east, southeast, south, southwest, west, northwest
- **Body state:** normal, damaged, sleeping, eating, carrying, transformed
- **Outfit:** bare, hoodie, armor, wizard robe
- **Pose:** idle key pose, stride contact, attack anticipation, recovery
- **Animation time:** frame index inside a loop or action
- **Environment context:** transparent sprite, floor contact, wall-mounted object, map tile
- **Export topology:** frame size, row order, frame count, anchors, sockets, manifest names

### Why this matters

Consistency becomes debuggable when only one axis changes at a time.

Bad experiment:

> Change the outfit, direction, action, frame count, palette, and camera angle in one generation.

Good experiment:

> Keep the canonical south-facing idle frame, change only the outfit, approve it, then propagate that approved outfit through directions and animations.

This is the central operating rule for scalable sprite customization.

## Four forms of consistency

### 1. Identity consistency

The character remains recognizably the same entity.

Anchor with:

- a canonical reference frame
- stable silhouette proportions
- recurring face and hair landmarks
- palette constraints
- fixed canvas and ground-contact point

### 2. Style consistency

Different assets look like they belong to the same game.

Anchor with:

- one or more style reference images
- explicit outline, shading, detail, and palette settings
- the same camera projection and pixel scale
- a reusable style brief rather than a fresh prose prompt every time

PixelLab's style-reference tools are designed to generate multiple variations that match reference imagery. They work best when the references are clean representatives of the target style, not a contradictory mood board.

### 3. State consistency

The identity survives changes such as clothing, equipment, damage, or emotion.

Treat an outfit or state as a reusable layer of constraints, not as a new character. Preserve body anchors, direction, pose, and timing while changing only the intended region.

### 4. Motion consistency

The character remains coherent across time.

Anchor with:

- key poses
- skeletons or copied skeleton animation
- frozen accepted frames
- fixed head or stable facial regions when appropriate
- repeatable frame counts and timing contracts

## Frozen context is supervision

PixelLab inpainting lets the user mark only the region that may change. The frozen remainder is not merely protected output; it is context that teaches the model what the edit must match.

Use inpainting for:

- replacing or repairing clothing
- adding held equipment
- correcting one arm, hand, leg, face, or effect
- keeping a character's identity while changing a local state
- extending or repairing part of a map
- fixing individual animation frames

### Practical rule

Describe the complete visible result, not only the masked patch.

The model sees the surrounding image. A prompt such as `red wizard sleeve holding a wooden staff, matching the existing short dark-haired isometric character` is stronger than `add sleeve`.

## Accepted frames become a training set

Animation quality improves when every accepted frame becomes guidance for neighboring frames.

PixelLab's skeleton workflow recommends:

1. derive or import a skeleton
2. align it to the reference character
3. generate from a stable frozen frame
4. make rough manual corrections
5. regenerate only the weak areas or frames
6. increase init-image strength as the result converges

This is a form of progressive self-conditioning:

```text
rough structure -> generated candidate -> human correction -> stronger conditioned candidate
```

The human does not need to hand-pixel the final result. Small structural corrections can steer the next generation much more efficiently than repeatedly rewriting prompts.

## Skeletons are portable motion programs

A skeleton animation is separable from the rendered character.

That means a useful skeleton can be:

- reused across multiple compatible characters
- copied from an existing animation
- rescaled to a new body
- corrected independently of the final pixels
- stored as a reusable motion asset

PixelLab supports template skeletons and animation-to-animation skeleton extraction. The estimated skeleton is a starting point, not ground truth; joints and proportions still require inspection.

### Fixed-head strategy

When an action does not require major head motion, keeping the head fixed can improve face consistency. Use this selectively. A permanently fixed head can look robotic during expressive or rotational motion.

## Key poses before interpolation

Interpolation works best between meaningful endpoints.

Before asking for in-between frames, verify:

- the first and final poses are anatomically and spatially compatible
- the character occupies a consistent scale and anchor position
- limbs do not teleport between impossible configurations
- carried props have a plausible path
- the silhouette reads clearly at both ends

The model cannot rescue fundamentally incompatible key poses without inventing motion.

## Animation methods and when to use them

| Method | Best use | Main constraint |
|---|---|---|
| Animate with text | Fast idle, walk, run, jump, attack, or object motion from one reference | Less direct control over exact pose arcs |
| Animate with skeleton | Character motion requiring deliberate posing and reusable structure | Skeleton setup and cleanup are required |
| Animation to animation | Transfer an existing motion pattern or maintain a coherent sequence | Source animation quality strongly affects output |
| Interpolate / animate between frames | Add controlled in-betweens between approved key poses | Endpoints must already be compatible |
| Edit animation | Repair selected frames while preserving the rest | Requires clear frame selection and masking discipline |
| Automatic directional animation | Rapid prototype of a character and common actions in several directions | Validate topology and identity before production use |
| Transfer outfit | Propagate clothing while preserving character and motion | Inspect occlusion, hem length, sleeves, and direction-specific details |

### Start simple

For early generations, prefer semantically simple actions:

- idle
- walk
- run
- jump
- breathe
- eat
- sleep

Complex actions should be decomposed into phases:

```text
anticipation -> contact / release -> follow-through -> recovery
```

For attacks with large visual effects, leave spatial room around the character rather than centering the body so tightly that the effect has nowhere to exist.

## Style references are a basis, not a spell

A style reference contributes signals such as:

- palette distribution
- outline behavior
- shape simplification
- material rendering
- shading density
- texture frequency

It does not automatically define:

- exact anatomy
- camera direction
- animation timing
- frame order
- game-engine anchors
- semantic state names

Those still require explicit constraints.

### Reference selection rules

Prefer references that:

- share the same projection
- use similar pixel dimensions
- have clean, readable silhouettes
- avoid mixed resolutions or filtering
- represent the target style rather than merely the target subject

## Rotations are a view graph

Directional sprites should be treated as related observations of one 3D-like identity, not eight unrelated drawings.

A robust rotation workflow:

1. approve one canonical direction
2. define the direction convention and row order
3. generate or rotate neighboring directions
4. compare shared landmarks across adjacent views
5. repair only mismatched regions
6. test the full compass ring in motion
7. lock the mapping with regression images or automated metadata tests

### Directional invariants

Check:

- height and ground contact
- head size
- shoulder and hip width
- handedness
- clothing hem
- equipment side
- light direction
- palette
- facial visibility

Mirroring can reduce production work, but only when handedness, asymmetrical clothing, weapons, text, and lighting permit it.

## Outfits are state transforms

For modular clothing, do not regenerate a fully independent character pack for every outfit.

Use this model:

```text
base identity + outfit specification + body anchors + occlusion rules
  -> outfit state
```

Then propagate the state through the existing direction and animation topology.

### Outfit QA

Inspect every frame for:

- torso hem ending at the intended body boundary
- sleeves following arms rather than merging into the torso
- hood or collar preserving the neck/head relationship
- pants and shoes maintaining ground contact
- front/back details changing correctly by direction
- no clothing pixels leaking into the groin, floor, or neighboring cells

This is exactly the class of defect that local inpainting and frame-by-frame regeneration should fix without destroying the already-correct motion.

## Tilesets are transition grammars

A tileset is not a collection of attractive square images. It is a grammar describing how terrain classes connect.

PixelLab's tileset tools explicitly distinguish concepts such as:

- inner terrain
- transition terrain
- outer terrain
- top tile versus center tile for sidescrollers
- tile size
- border jitter
- map strength
- tile strength
- AI border freedom

### Mental model

```text
terrain vocabulary + adjacency rules + edge freedom -> tile grammar
```

A useful tileset must cover:

- interior fill
- straight edges
- inside corners
- outside corners
- narrow passages
- isolated islands
- transitions between materials
- animated variants where needed

### Validation beats beauty

Always render a test map containing every adjacency combination. A beautiful tile that does not seam correctly is not a production tile.

For dual-grid, Wang, 3x3, or engine-specific exports, preserve the exact index convention in metadata and tests.

## Maps are iterative inpainting canvases

PixelLab's map workflow encourages generating selected regions with an init image and inpainting mask.

That implies a strong map-building loop:

1. block out composition and traversable structure
2. select one bounded region
3. describe the complete local scene
4. generate with surrounding map context frozen
5. repair seams and gameplay readability
6. extend into the next region

Do not ask the model to invent an entire production map before collision, path width, exits, doors, and gameplay landmarks have been planned.

## UI generation still needs a design system

Generated buttons, panels, health bars, and menu elements should inherit:

- a spacing scale
- corner language
- border thickness
- font and icon scale
- state set: default, hover, pressed, disabled, focused
- nine-slice or stretch rules
- contrast requirements

A pile of matching-looking UI images is not yet a usable component library.

## The full production dependency graph

```text
visual brief
  -> canonical style references
  -> canonical identity frame
  -> approved directional views
  -> approved states / outfits
  -> approved key poses
  -> animation families
  -> props and interaction assets
  -> terrain textures and tileset grammar
  -> maps and scenes
  -> UI system
  -> export manifests
  -> engine validation
```

Building in this order reduces expensive rework. Every downstream asset depends on assumptions established upstream.

## Generate, select, correct, reseed

A reliable session should look more like search plus editing than gambling:

1. **Generate:** create several candidates under controlled constraints.
2. **Select:** choose the candidate with the best global structure.
3. **Correct:** make small manual structural fixes or masks.
4. **Reseed:** use the corrected result as init/reference guidance.
5. **Converge:** increase guidance strength as the desired asset stabilizes.
6. **Validate:** test in the actual sprite sheet, map, UI, or engine context.

Keep seeds and settings when reproducibility matters.

## Change one variable per experiment

When a result fails, identify the failing axis before regenerating.

Examples:

- identity drift -> strengthen identity reference or freeze the face
- wrong direction -> correct camera/direction metadata, not the outfit prompt
- bad arm -> edit skeleton or inpaint the arm only
- inconsistent palette -> apply target palette, do not redesign the pose
- broken map seam -> adjust border/transition settings, not the entire scene description
- clothing leak -> mask the garment boundary, preserve the body and motion

This turns generation into a debuggable engineering process.

## Export contracts are part of the art

A sprite is not production-ready until its machine-readable contract is stable.

Record at minimum:

```yaml
character_id: ani_iso_human
state_id: hoodie_dark
projection: isometric
frame_width: 64
frame_height: 64
directions: [south, southwest, west, northwest, north, northeast, east, southeast]
animations:
  idle: 4
  walk: 8
  run: 8
  jump: 6
anchors:
  ground: [32, 52]
  hand_right: per-frame
mirroring_policy: explicit
```

The exact numbers above are illustrative. The important point is that filenames alone are not a sufficient runtime contract.

## Recommended Prismtek pipeline

### Character canon

1. Pick one canonical frame for each identity.
2. Record canvas, projection, direction, palette, ground anchor, and body proportions.
3. Store the original and approved corrected versions separately.

### Direction canon

1. Generate or import all required directions.
2. Verify row order visually with a compass-ring preview.
3. Lock direction mapping with tests.

### Outfit canon

1. Apply an outfit to the canonical frame only.
2. Repair garment boundaries with inpainting.
3. Approve the state before propagation.
4. Transfer through directions and animation families while preserving frame topology.

### Motion canon

1. Maintain a reusable skeleton/motion library.
2. Map semantic actions to frame counts and loop behavior.
3. Generate one direction first.
4. Validate timing and silhouette.
5. Expand to other directions.
6. Repair frames locally rather than restarting the whole sequence.

### Runtime canon

1. Export a manifest with semantic IDs.
2. Make reaction mapping consume semantic actions rather than arbitrary filenames.
3. Validate missing frames, frame counts, anchors, transparency, and direction order.
4. Preview every installed pack in the actual runtime before marking it compatible.

## AI-agent and MCP workflow

PixelLab currently documents web, Pixelorama, Aseprite, API, and MCP-based workflows. The MCP path lets an agent request characters, animations, tilesets, and isometric assets from an IDE or coding environment.

The important architectural lesson is not merely that an agent can call generation tools. A dependable agent workflow must also:

- preserve asset IDs and provenance
- save prompts, seeds, settings, references, and generation receipts
- avoid overwriting approved source art
- inspect generated outputs before integration
- run topology and engine-level validation
- require human approval before expensive or destructive batch generation

Generation without receipts creates an unrepeatable art pile.

## Quality gates

### Pixel gate

- nearest-neighbor presentation
- no unintended anti-aliasing or blur
- intended palette and alpha
- no stray pixels outside cell bounds

### Identity gate

- same silhouette and proportions
- stable face/hair/markings
- directionally correct asymmetry

### Motion gate

- readable anticipation and contact
- stable ground point
- no limb teleportation
- loop closes cleanly
- frame count and timing match the runtime contract

### Outfit gate

- correct occlusion
- no body leaks
- consistent garment boundaries
- direction-specific front/back logic

### Tileset gate

- all adjacency cases render
- no seams or index mismatches
- collisions and traversal remain readable
- animated tiles preserve edge compatibility

### Export gate

- deterministic file names and manifest IDs
- exact dimensions
- exact frame counts
- correct direction order
- anchors and sockets present
- runtime preview passes

## Common failure modes

### One-shot prompting

**Symptom:** Every retry changes the whole character.

**Recovery:** Freeze accepted regions, mask only the defect, and reuse corrected output as init guidance.

### Too many changing axes

**Symptom:** It is impossible to tell whether the prompt, direction, outfit, or animation caused the failure.

**Recovery:** Return to the canonical reference and vary one axis.

### Vague style references

**Symptom:** Assets share a mood but not a production style.

**Recovery:** Use cleaner references with matching projection, resolution, outline, and shading language.

### Treating interpolation as animation design

**Symptom:** Smooth but weightless or anatomically impossible motion.

**Recovery:** Improve key poses and motion arcs before generating in-betweens.

### Generating every direction before validating one

**Symptom:** The same structural defect multiplies across the entire pack.

**Recovery:** Approve one direction and action topology first.

### No machine-readable export contract

**Symptom:** Runtime mapping depends on ad hoc filenames and hidden row assumptions.

**Recovery:** Export manifests, semantic IDs, direction conventions, frame counts, and anchors.

### No engine validation

**Symptom:** Art looks good in the editor but drifts, clips, flickers, or maps incorrectly in game.

**Recovery:** Preview in the actual runtime with automated structural checks and human visual QA.

## Canonical questions

Before generating:

1. Which axis is changing?
2. Which pixels, frames, directions, or metadata must remain invariant?
3. What is the canonical reference?
4. What topology must the runtime receive?
5. What is the cheapest validation that can fail fast?

Before accepting:

1. Does the asset still match the identity and style canon?
2. Did the model alter anything outside the intended axis?
3. Are frame order, dimensions, anchors, and transparency correct?
4. Does it work in a full compass, loop, map, or UI-state preview?
5. Can the generation be reproduced or repaired later?

## Sources

Primary current sources:

- PixelLab documentation: https://www.pixellab.ai/docs
- Ways to use PixelLab: https://www.pixellab.ai/docs/ways-to-use-pixellab
- Animate with skeleton: https://www.pixellab.ai/docs/tools/animate-with-skeleton
- Animation to animation: https://www.pixellab.ai/docs/tools/animation-to-animation
- Animate with text: https://www.pixellab.ai/docs/tools/animate-with-text-new
- Inpainting: https://www.pixellab.ai/docs/options/inpainting
- Inpaint tool: https://www.pixellab.ai/docs/tools/inpaint
- Style-reference generation: https://www.pixellab.ai/docs/tools/consistent-style
- Create tileset: https://www.pixellab.ai/docs/tools/create-tileset
- Tileset options: https://www.pixellab.ai/docs/options/tileset
- Map guide: https://www.pixellab.ai/docs/guides/map-tiles
- PixelLab product page: https://www.pixellab.ai/
- PixelLab YouTube channel: https://www.youtube.com/@PixelLab_AI

## Known unknowns

- The official total number of channel videos and their exact newest-first order were not available through the accessible YouTube surface.
- Complete transcripts were not available for every indexed video.
- Some tools and tier limits are volatile and must be checked against current documentation before spending generations or building automation around them.
- The mirror collection's `67` count is useful evidence, but it is not an official channel export.

## Agent instructions

- Load this note for PixelLab asset planning, sprite consistency, animation repair, outfit propagation, tileset generation, map production, or MCP integration.
- Treat conceptual production guidance as durable, but verify current tool names, limits, pricing, and access tiers live.
- Do not claim every PixelLab video was reviewed unless a future receipt includes a complete official feed and transcript or viewing log.
- Prefer this note's constraint/dependency model over loose prompt recipes.

## Next action

- [ ] When channel feed or transcript access becomes available, reconcile every official video newest-first, add per-video receipts, and promote the coverage status from partial to complete.
