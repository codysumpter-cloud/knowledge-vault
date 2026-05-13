# Buddy Skill Adapters

Adapters are the only way Buddy may execute a skill action.

A skill can generate drafts and analysis internally, but account actions must go through an adapter.

## Required adapter interface

```ts
export interface BuddySkillAdapter<Input, Output> {
  id: string;
  platform: string;
  riskClass: "read-only" | "draft-only" | "write" | "external-action" | "destructive" | "money";
  dryRun(input: Input): Promise<Output>;
  execute(input: Input, approval: ExplicitApproval): Promise<Output>;
}
```

## Required approval payload

```ts
export interface ExplicitApproval {
  approvedBy: "Prismtek";
  approvedAt: string;
  actionSummary: string;
  riskClass: string;
  target: string;
}
```

## Adapter folders

```txt
adapters/
  genviral/    # social publishing backend adapter docs
  social/      # YouTube / X / Twitch generic adapter contracts
  market/      # sportsbook / prediction-market analysis contracts
  memory/      # KnowledgeVault and posted-content logs
```

## Default behavior

If no adapter exists, the skill may still run in `draft-only` or `analysis-only` mode.

It must not execute external actions.
