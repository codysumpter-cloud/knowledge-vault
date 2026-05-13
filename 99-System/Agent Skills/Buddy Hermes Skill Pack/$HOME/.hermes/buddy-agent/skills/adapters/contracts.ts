export type RiskClass =
  | "read-only"
  | "draft-only"
  | "write"
  | "external-action"
  | "destructive"
  | "money";

export type PlatformClass =
  | "macos"
  | "ios"
  | "web"
  | "repo-only"
  | "youtube"
  | "x"
  | "twitch";

export interface ExplicitApproval {
  approvedBy: "Prismtek";
  approvedAt: string;
  actionSummary: string;
  riskClass: RiskClass;
  target: string;
}

export interface SkillRunLog {
  skillId: string;
  mode: "read-only" | "draft-only" | "analysis-only" | "confirmed-action";
  riskClass: RiskClass;
  adapterId?: string;
  inputsSummary: string;
  outputsSummary: string;
  actionTaken: boolean;
  requiresFollowup: boolean;
  timestamp: string;
}

export interface BuddySkillAdapter<Input, Output> {
  id: string;
  platform: PlatformClass;
  riskClass: RiskClass;
  dryRun(input: Input): Promise<Output>;
  execute(input: Input, approval: ExplicitApproval): Promise<Output>;
}
