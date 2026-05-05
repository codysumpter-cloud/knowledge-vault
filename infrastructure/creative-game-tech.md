---
title: Creative & Game Engine Tech
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [art, gamedev, bevy, aseprite, pixel-art]
sources: [bevy, libresprite, tamagoscii, aseprite-docker]
---

# Creative & Game Engine Tech

## Overview
Integration of high-performance game engines and pixel-art tooling to enable a professional asset pipeline for Prismtek projects.

## Components

### 1. Bevy Engine (Rust-based ECS)
- **Capability:** Data-driven, parallel game engine.
- **Strategic Value:** Provides a blueprint for "Entity Component System" (ECS) architecture. We can use Bevy's design patterns to optimize the `buddy-brain` state management (treating agents as entities and skills as components).

### 2. Aseprite / LibreSprite Pipeline
- **Capability:** Industry-standard pixel art and animation tools.
- **Strategic Value:** Enables high-fidelity asset creation for the "Everything is Crab" mod and other Prismtek apps.
- **Infrastructure:** Utilizes Dockerized build environments for Linux/Windows to ensure consistent asset export across platforms.

### 3. Tamagoscii
- **Capability:** Small-scale, constraint-based virtual pet simulation.
- **Strategic Value:** A reference for "Low-Fidelity/High-Engagement" interaction models, which can be applied to the Buddy UI.

## Integration State
- [x] PixelLab MCP integrated (Runtime access to pixel art tools).
- [ ] Bevy ECS patterns mapped to Buddy Brain state logic.
- [ ] Aseprite Docker pipeline verified for asset export.
