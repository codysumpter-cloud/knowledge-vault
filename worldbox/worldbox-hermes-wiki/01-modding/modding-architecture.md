# Modding Architecture

## Goal

Create a reliable WorldBox control and observation layer for AgentCraft/BMO.

The no-mod screen-control helper is useful now, but it cannot be the final control surface because it is vulnerable to:

- camera drift
- zoom changes
- UI overlays
- macOS focus problems
- synthetic click rejection
- modal dialogs
- tool coordinate drift

The target architecture is a bridge mod with a localhost API.

```text
WorldBox desktop game
  -> NML/BepInEx bridge mod
  -> localhost HTTP/WebSocket API
  -> worldboxctl CLI
  -> BMO policy runtime
  -> AgentCraft HUD
  -> AI Director proposal service
```

## Loader recommendation

### Preferred: NML / NeoModLoader

Use NML first because current community docs describe it as the replacement for NCMS and note that it can load both NML and NCMS mods.

### Secondary: BepInEx

Use BepInEx when:

- NML is unavailable or unstable for a target version
- Harmony patching is easier through BepInEx
- the mod needs BepInEx ecosystem tooling

### Avoid starting on NCMS

NCMS is legacy. Keep it as a compatibility reference only.

## Bridge stages

### Stage 0: no-mod helper

Already usable:

- focus WorldBox
- screenshot
- safe-click named zones
- emit AgentCraft events
- log actions

### Stage 1: read-only bridge

First mod milestone:

- `GET /ping`
- `GET /status`
- `GET /observe`
- `GET /selected`
- `GET /kingdoms`
- `GET /cities`

No write actions yet.

### Stage 2: proposal loop

- bridge observes world state
- AI Director proposes safe actions
- BMO/AgentCraft displays proposals
- user approves/rejects

### Stage 3: allowlisted writes

Only after read-only endpoints are stable:

- pause/resume
- set speed
- inspect entity
- spawn harmless creatures
- use safe powers
- move/select units if stable APIs exist

### Stage 4: dangerous writes

Require explicit approval:

- plague
- bombs/nukes
- demons/dragons
- war forcing
- city destruction
- mass terrain edits

## Bridge security rules

- Bind only to `127.0.0.1`.
- Use a random session token.
- No arbitrary C# eval.
- No shell execution from the mod.
- No arbitrary file operations.
- Allowlist every command.
- Rate-limit write commands.
- Emit receipts for all writes.
- Require approval metadata for high-risk commands.
- Include a kill switch.
