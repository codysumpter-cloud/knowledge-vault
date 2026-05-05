# Modding Architecture

This page defines the target state for WorldBox control.

## The Control Pipeline
The current goal is to evolve the control surface to avoid the instability of screen-clicks.

1. **Stage 0: No-Mod Helper** (Current)
   - Focuses on `worldboxctl` for window management.
   - Uses screenshots and zone-clicks.
   - High vulnerability to camera drift and UI overlays.
2. **Stage 1: Read-Only Bridge**
   - Implementation of NML/BepInEx mod.
   - Provides `GET` endpoints for `/status`, `/observe`, and `/kingdoms`.
3. **Stage 2: Proposal Loop**
   - AI Director suggests actions based on bridge data.
   - User approves actions via AgentCraft HUD.
4. **Stage 3: Allowlisted Writes**
   - Safe API calls (pause/resume, speed, harmless spawns).
5. **Stage 4: Dangerous Writes**
   - High-impact powers (Plague, Nukes, Dragons).
   - Require explicit high-level approval.

## Tooling Recommendations
- **Primary:** NeoModLoader (NML). Replacement for NCMS.
- **Secondary:** BepInEx. Used for Harmony patching and ecosystem tools.
- **Legacy:** NCMS. Reference only.

[[bridge-security]]
[[operator-runbook]]
