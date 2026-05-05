# WorldBox Hermes Wiki

Purpose: a compact knowledge base for BMO/Hermes/AgentCraft agents working with WorldBox as a simulation testbed.

This wiki is designed for:

- WorldBox achievement/unlock coaching
- no-mod screen-control reliability
- NML/BepInEx bridge planning
- AgentCraft HUD/event design
- AI-driven species/kingdom mod architecture

## Operating principle

Do not treat screen clicks as authoritative. Use screen control only for supervised play. Prefer bridge/mod observation once available.

```text
WorldBox
  -> no-mod helper: worldboxctl focus/shot/zones
  -> mod bridge: NML/BepInEx localhost API
  -> BMO policy runtime
  -> AgentCraft HUD
  -> AI Director proposals
```

## Suggested read order

1. `00-sources/source-map.md`
2. `01-modding/modding-architecture.md`
3. `02-agentcraft/implementation-brief.md`
4. `03-runtime/operator-runbook.md`
5. `04-playbooks/achievement-atlas.md`
6. `05-schemas/events-and-protocol.md`

## Hard safety rules

- Do not automate while the user is driving.
- Do not run install/package commands that fetch or execute code unless the user approves and can supervise.
- Do not use repeated ESC/clear-ui in WorldBox. Modal prompts are hard-stop states.
- Do not batch game actions in no-mod mode.
- Do not give LLMs arbitrary C# eval, shell execution, or unrestricted file access from a game mod.
