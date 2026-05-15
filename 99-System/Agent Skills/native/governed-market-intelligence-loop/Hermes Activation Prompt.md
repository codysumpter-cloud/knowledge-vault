# Hermes Activation Prompt — Governed Market Intelligence Loop

Use this prompt to activate and apply the native skill.

```txt
USE SKILL governed-market-intelligence-loop

Goal:
Improve the current Market Intelligence Loop so it is model/provider agnostic, proposal-only, auditable, and safe-by-default.

Current issue:
The current market loop is framed like a fully automated divergence hunter and may imply orders/fills or execution. That is too broad for a money-risk skill.

Upgrade it from:
Signal -> Analyze -> Report -> Execute

to:
Observe -> Validate -> Score -> Propose -> Require Approval -> Log

Requirements:

1. Keep it proposal-only.
Do not place trades.
Do not modify orders.
Do not resize exposure.
Do not change stops.
Do not deposit/withdraw.
Do not sign transactions.
Do not open broker/wallet/sportsbook pages for execution.

2. Make cron a heartbeat, not the decision-maker.
Replace 0 * * * * with market-calendar-aware jobs:

CRON_TZ=America/New_York
15 8 * * 1-5  hermes premarket-scan --proposal-only
25 9 * * 1-5  hermes open-risk-check --require-human-approval
7,22,37,52 9-15 * * 1-5 hermes market-loop --proposal-only
5 16 * * 1-5 hermes close-review --digest
30 17 * * 1-5 hermes slow-signal-scan --proposal-only
15 20 * * 1-5 hermes calibrate-thresholds --no-live-actions

Inside the app, use a market calendar:
- exit if not trading day
- exit if market not open for jobs requiring open market
- adjust for early close
- require approval near open/close risk windows

3. Load canonical state every run:
- watchlist
- holdings
- queued orders
- thesis per ticker
- risk policy
- previous run summary
- last alert per ticker
- prior divergence scores
- exposure limits

Fail closed if thesis/account/risk policy cannot be loaded.

4. Normalize all signals into schema:
- ticker
- source
- direction
- confidence
- severity
- freshness
- latency class
- evidence URL
- evidence hash
- summary
- limitations

5. Treat congressional disclosures as delayed context.
Track transaction_date, filing_date, detected_at.
They may increase scrutiny but cannot trigger execution.

6. Score divergence mathematically.
Use action thresholds:
- <0.35 silent
- 0.35-0.54 watch
- 0.55-0.74 proposal
- >=0.75 human_review

High confidence requires at least two verified independent sources and primary-source evidence.

7. Split loops:
Market Intelligence Loop: outside-world signals and thesis impact.
Account Risk Loop: holdings, queued orders, fills, exposure, drawdown, guardrails.

Account risk checks must be deterministic.

8. Use alert tiers:
P0 guardrail/order/exposure anomaly
P1 high-confidence thesis break
P2 material divergence/proposal
P3 digest note
P4 log only

Stable runs should log only unless digest is due.

9. Add idempotency/locking.
Each run should have a run key and avoid double alerts.
Store run ID, started/finished, tickers, signals, divergence scores, alerts, proposals, errors, agent version, config version.

10. Use least privilege.
web: read-only
market data: read-only
account info/positions/orders: read-only
trading: disabled
terminal: disabled unless whitelisted
file: read-only scoped paths
KnowledgeVault: read-only by default, write only receipts/proposals
X/social: read-only for sentiment

11. Produce proposal format when needed:
# Risk Proposal: {TICKER}
- alert tier
- current position
- trigger
- evidence
- signal classification
- thesis impact
- recommended action
- what Hermes is not doing
- approval required

12. Write outputs to KnowledgeVault:
KnowledgeVault/50 - Content/market-risk-proposals/
KnowledgeVault/50 - Content/market-sports-digests/
KnowledgeVault/50 - Content/market-watchlists/
KnowledgeVault/99-System/Cron Jobs/Runs/
KnowledgeVault/99-System/Cron Jobs/Learnings/
KnowledgeVault/99-System/Cron Jobs/Next Plans/
KnowledgeVault/99-System/Risk Policy/

13. Create content ideas only as educational/process content.
No financial advice claims.
No guaranteed-profit language.
No trade recommendations disguised as content.

Return:
- files patched
- cron schedule proposal
- active skill verification
- risk policy status
- execution disabled confirmation
- provider/model routing plan
- next safe test run command
```
