---
type: handoff
status: draft
owner: Prismtek
source_of_truth: mixed
last_verified: 2026-08-06
risk_level: low
privacy: public
freshness: volatile
agent_load: reference-only
tags:
  - pixellab
  - research-receipt
  - provenance
  - youtube
---

# PixelLab AI Karpathy Wiki — Research Receipt

> Exact evidence, limitations, and continuation instructions for the 2026-08-06 PixelLab channel study.

## Task goal

Review the PixelLab AI YouTube account from newest to oldest, report durable lessons, create a Karpathy-style wiki, and store it in KnowledgeVault.

## Current state

### Completed

- Read the KnowledgeVault operating contract, system map, knowledge index, database blueprint, cold-start bundle, note standard, runbook, security policy, and existing Wikipedia Karpathy-wiki design.
- Verified that `codysumpter-cloud/knowledge-vault` is the canonical accessible repository and that it is public.
- Inspected current PixelLab documentation for image generation, style references, inpainting, skeleton animation, animation-to-animation, text animation, maps, tilesets, rotations, editor surfaces, API, and MCP usage.
- Recovered 24 original YouTube IDs from official pages, indexed metadata, and mirror pages that cite original URLs.
- Recovered six positions from a third-party collection labeled as 67 PixelLab videos.
- Produced a mental-model-first production wiki.
- Produced a provenance-first video inventory.

### Blocked

- A complete official newest-to-oldest channel feed was not available through the accessible YouTube page surface.
- Complete captions or transcripts were not available for every video.
- Therefore a claim that all videos were watched would be false.

## Files added

- `99-System/Agent Skills/Hermes Skills/reference/pixellab-ai-karpathy-wiki/README.md`
- `99-System/Agent Skills/Hermes Skills/reference/pixellab-ai-karpathy-wiki/VIDEO-INVENTORY.md`
- `99-System/Agent Skills/Hermes Skills/reference/pixellab-ai-karpathy-wiki/RESEARCH-RECEIPT.md`

## Vault files loaded before editing

- `README.md`
- `AGENTS.md`
- `SYSTEMMAP.md`
- `AGENT_KNOWLEDGE_INDEX.md`
- `AGENT_DATABASE_BLUEPRINT.md`
- `99-System/Context Bundles/cold-start/bundle.md`
- `99-System/Standards/NOTE_FORMAT_STANDARD.md`
- `99-System/Agent Skills/Hermes Skills/reference/wikipedia-karpathy-wiki/README.md`
- `RUNBOOK.md`
- `SECURITY.md`
- `99-System/Agent Skills/Skill Index.md`

## Primary external sources checked

- https://www.pixellab.ai/
- https://www.pixellab.ai/docs
- https://www.pixellab.ai/docs/ways-to-use-pixellab
- https://www.pixellab.ai/docs/tools/animate-with-skeleton
- https://www.pixellab.ai/docs/tools/animation-to-animation
- https://www.pixellab.ai/docs/tools/animate-with-text-new
- https://www.pixellab.ai/docs/options/inpainting
- https://www.pixellab.ai/docs/tools/inpaint
- https://www.pixellab.ai/docs/tools/consistent-style
- https://www.pixellab.ai/docs/tools/create-tileset
- https://www.pixellab.ai/docs/options/tileset
- https://www.pixellab.ai/docs/guides/map-tiles
- https://www.youtube.com/@PixelLab_AI

## Secondary discovery sources

Third-party mirror pages were used only to recover original video IDs, titles, and displayed collection positions. Mirror upload dates were not treated as original publication dates.

Examples:

- https://www.bilibili.com/video/BV1wzLs6mEox/
- https://www.bilibili.com/video/BV1LbLY64EAy/
- https://www.bilibili.com/video/BV1ZpLY68Emi/

## Core synthesis receipt

The source material supports these durable conclusions:

1. PixelLab is best operated as an iterative constrained editor rather than a one-shot generator.
2. Identity, style, projection, direction, state/outfit, pose, animation time, environment, and export topology should be controlled as separate axes.
3. Inpainting converts accepted pixels into frozen contextual supervision.
4. Corrected frames and skeletons become reusable guidance for future frames and characters.
5. Animation quality depends on key poses, alignment, and local repair more than blind frame generation.
6. Tilesets encode transition grammar and require adjacency testing.
7. Maps should be grown region by region with gameplay structure and surrounding context preserved.
8. MCP or API generation requires provenance, manifests, human review, and runtime validation to become dependable production infrastructure.

## Verification performed

### Verified

- Repository and branch creation succeeded through the GitHub connector.
- Each listed file was committed to the feature branch through GitHub's contents API.
- Source URLs are public and contain no private credentials or session state.
- Notes use public-safe KnowledgeVault metadata and explicit claim-status language.

### Unverified

- `vault_doctor.py` was not executed because this workflow used the remote GitHub connector without a local checkout.
- `note_quality_linter.py` was not executed for the same reason.
- The complete official channel count, order, and transcript coverage remain unverified.

## Remaining risks

- PixelLab tool names, access tiers, costs, dimensions, and limits are volatile.
- The mirror collection may omit, duplicate, or reorder official videos.
- The current wiki synthesizes confirmed documentation and recovered catalogue evidence, but it is not a replacement for future per-video viewing receipts.

## Continuation protocol

When official feed or transcript access becomes available:

1. Export the complete channel inventory with video ID, title, publication timestamp, duration, and availability.
2. Sort strictly by original YouTube publication timestamp descending.
3. For each video, record transcript/viewing status and 3-7 non-duplicative learnings.
4. Link each claim to its video ID and timestamp range where possible.
5. Reconcile duplicate or renamed tutorials.
6. Update `VIDEO-INVENTORY.md` rather than creating a parallel inventory.
7. Promote the research status only after every official video has a receipt.
8. Run `vault_doctor.py` and `note_quality_linter.py` before merging.

## Next action

- [ ] Obtain a complete official YouTube channel export or lawful transcript feed, then finish the newest-first per-video review.
