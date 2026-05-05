# Events and Protocol

## AgentCraft event envelope

```ts
type AgentCraftEvent = {
  type:
    | "mission_start"
    | "mission_checkpoint"
    | "game_observation"
    | "game_action_proposed"
    | "game_action_executed"
    | "game_action_blocked"
    | "achievement_detected"
    | "risk_escalation"
    | "human_intervention_required"
    | "hero_idle";
  timestamp: string;
  sessionId: string;
  client: "worldboxctl" | "worldbox-bridge" | "worldbox-ai-director" | string;
  summary: string;
  risk?: "low" | "medium" | "high" | "critical";
  data?: Record<string, unknown>;
};
```

## Bridge command envelope

```ts
type BridgeCommand = {
  id: string;
  type:
    | "get_status"
    | "observe"
    | "pause"
    | "resume"
    | "set_speed"
    | "spawn"
    | "use_power"
    | "inspect"
    | "move_actor";
  approvalId?: string;
  args?: Record<string, unknown>;
};
```

## Bridge response envelope

```ts
type BridgeResponse =
  | { id: string; ok: true; result: unknown; receipt: Receipt }
  | { id: string; ok: false; error: string; code: string };

type Receipt = {
  commandId: string;
  executedAt: string;
  actor: string;
  risk: "low" | "medium" | "high" | "critical";
  affectedEntities?: string[];
};
```

## AI proposal schema

```ts
type AIProposal = {
  actor: string;
  intent: string;
  actions: ProposedAction[];
  risk: "low" | "medium" | "high" | "critical";
  requiresApproval: boolean;
  rationale: string;
};

type ProposedAction =
  | { type: "suggest_policy"; policy: string }
  | { type: "request_player_action"; action: string; reason: string }
  | { type: "bridge_command"; command: BridgeCommand };
```

## Risk classifier

Low:

- read-only observation
- screenshots
- HUD events
- inspect selected entity
- safe menu navigation

Medium:

- spawning harmless creatures
- blessing/healing
- pause/resume/speed
- small controlled arena actions

High:

- madness
- plague
- fire
- demons/dragons
- war forcing
- terrain destruction

Critical:

- nukes
- mass life eraser
- save edits
- arbitrary code
- arbitrary filesystem access
