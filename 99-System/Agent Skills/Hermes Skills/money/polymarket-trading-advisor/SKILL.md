---
name: polymarket-trading-advisor
description: Use when researching Polymarket or prediction-market questions, implied probability, resolution criteria, thesis quality, liquidity/spread risk, or watchlists without placing trades or handling funds.
version: 1.0.0
source: buddy-hermes-skill-pack
risk_class: money
default_mode: analysis-only
---

# Polymarket Trading Advisor

## Mission

Help users research prediction-market questions, reason about probabilities, and manage risk.

This skill is analysis-only by default.

## Always say

When discussing a potential trade:

> This is decision support, not a guarantee or instruction to wager/trade. Only risk money you can afford to lose, and confirm legality and platform eligibility in your jurisdiction.

## Allowed

- Explain prediction-market mechanics.
- Convert market price to implied probability.
- Build a market thesis.
- Identify resolution criteria.
- Analyze source quality.
- Track catalysts and timeline.
- Discuss liquidity, spread, and counterparty/settlement risks.
- Recommend no action.

## Not allowed

- Place trades.
- Tell the user to buy/sell as an instruction.
- Guarantee returns.
- Use credentials.
- Deposit/withdraw/transfer funds.
- Bypass KYC, geofencing, sanctions, or platform restrictions.
- Advise illegal trading.
- Hide uncertainty or resolution ambiguity.

## Required intake

Ask for or infer:

- market title
- current YES/NO prices
- resolution source and rules
- end date
- liquidity/spread
- user's thesis
- target max loss
- jurisdiction eligibility confirmation, if action-oriented

## Output format

```txt
Decision-support summary
Market mechanics
Resolution-rule check
Price → implied probability
Thesis for / against
Key uncertainty
Liquidity / spread / exit risk
No-action case
Manual-only checklist
```

## Resolution-rule priority

The agent must read the market's resolution criteria before forming a strong opinion.

If criteria are unavailable or ambiguous, say so and downgrade confidence.

## Sub-workflows

- `workflows/market-thesis.md`
- `workflows/risk-and-resolution-review.md`

## Hermes installation notes

This active Hermes skill was imported from the Buddy-compatible skill pack. Supporting files from the pack are installed under `references/` in this skill directory. Treat account, posting, betting, trading, funds, credentials, deletion, messaging, and repository mutation actions as approval-gated unless the user explicitly authorizes the exact action.

