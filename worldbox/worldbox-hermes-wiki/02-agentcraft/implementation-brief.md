# AgentCraft Implementation Brief

## Product thesis

WorldBox is the live chaos sandbox. AgentCraft is the command room. BMO is the safety/runtime authority.

The goal is not merely "AI clicks WorldBox." The goal is:

> A living god-game orchestration layer where kingdoms, species, advisors, rivals, and teammates are AI agents visible and steerable through AgentCraft.

## Roles

### BMO

- runtime authority
- policy checks
- approval gates
- receipts/logging
- memory and mission state
- refusal of risky or invalid actions

### AgentCraft HUD

- shows active agents/heroes
- shows missions and objectives
- shows current risk state
- shows action proposals
- shows observed world summaries
- lets user supervise without reading raw logs

### WorldBox agent

- observes game state
- proposes actions
- uses `worldboxctl` in no-mod mode
- later calls bridge endpoints
- never performs destructive actions without approval

### AI Director

- turns world state into proposals
- assigns role voices/personality to kingdoms/species
- keeps actions within a limited action schema
- does not directly execute game writes

## Event model

Minimum event stream:

```text
mission_start
mission_checkpoint
game_observation
game_action_proposed
game_action_executed
game_action_blocked
achievement_detected
risk_escalation
human_intervention_required
hero_idle
```

## First demo loop

1. Start AgentCraft HUD.
2. Start WorldBox.
3. Agent emits `mission_start` for unlock run.
4. Agent uses `worldboxctl ready` and screenshots.
5. Agent proposes one achievement action.
6. User approves or rejects.
7. Agent executes one step.
8. Agent emits result/receipt.
9. Repeat.

## Future gameplay loop

```text
World state changes
  -> bridge emits observation
  -> AI Director proposes kingdom/species action
  -> BMO validates risk and permissions
  -> AgentCraft displays proposal
  -> user approves/delegates
  -> bridge applies allowlisted action
  -> receipt appears in AgentCraft
```
