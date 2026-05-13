---
name: polymarket-weather-trading-bot
description: Use when setting up, auditing, paper-testing, running, or supervising a Hermes-controlled Polymarket weather trading bot, especially workflows involving weatherbot, Visual Crossing, py-clob-client, Polygon wallets, Polymarket approvals, Kelly/EV sizing, cron monitoring, Telegram reports, or live/paper prediction-market trading.
---

# Polymarket Weather Trading Bot

## Overview

Use this for the Medium-style Hermes + Polymarket weatherbot workflow, but run it with strict safety rails: paper trading first, isolated wallet, redacted secrets, explicit approval before any live on-chain transaction or live order, and receipt-based verification.

This skill turns the article workflow into an operational playbook for Hermes. It is not financial advice; markets can lose the entire stake. Default to paper/simulation until the user explicitly authorizes funding, approvals, and live mode.

## Required supporting skill

Load `polymarket` when market discovery, prices, orderbooks, condition IDs, or Polymarket public APIs are needed.

## Hard safety rules

- Do not promise profits or repeat claims like "$100 → $5,000" as expected results.
- Never print a private key, seed phrase, API key, or full `.env` contents in chat/log summaries. Show only wallet address and redacted key presence.
- Never stage/commit `.env`, private keys, wallet files, transaction logs containing secrets, or generated credentials.
- Ask explicit confirmation before:
  - creating or overwriting a funded wallet,
  - sending on-chain approval transactions,
  - switching config from `paper` to `live`,
  - starting continuous live trading,
  - increasing `max_bet`, `min_ev` risk settings, or allowance scope.
- Start with separate bot wallet only. Never use the user's main wallet.
- Start with small capital. Article defaults: $10 minimum, $50 recommended, `max_bet: 2.0`; prefer smaller if uncertain.
- Prefer limited approvals when supported by the bot; if using max approvals, state the risk and get explicit consent.
- Verify every on-chain transaction by receipt, chain ID, spender, token, and status before claiming success.
- On Mac hardware, avoid heavy watchers. For 24/7 trading prefer VPS; for simple scans use scheduled jobs or foreground runs.

## Quick workflow

1. Clone/setup weatherbot in an isolated project directory.
2. Create venv and install: `py-clob-client python-dotenv requests web3`.
3. Create or import a separate Polygon wallet; save secrets to `.env` with `chmod 600`; do not display the private key.
4. User funds wallet manually with Polygon USDC.e and POL gas.
5. Verify balances: POL and USDC.e (`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`) on Polygon chain 137.
6. Configure weather API (`vc_key`) and conservative risk settings in `config.json`.
7. Run paper/test scan: `python3 bot_v3.py scan`; inspect candidate trades and any orders.
8. Only after user approval: approve required Polymarket contracts, switch to live, and start continuous mode.
9. Report via Telegram with receipts, PnL, exposure, open positions, and errors.
10. Record lessons in a project-local journal or skill updates only when reusable; do not save stale trade details to memory.

## Setup commands

```bash
# Use a VPS or isolated workspace, not a random home/vault directory.
git clone https://github.com/alteregoeth-ai/weatherbot.git
cd weatherbot
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install py-clob-client python-dotenv requests web3
```

If venv creation fails on Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y python3.12-venv python3-venv
```

## Wallet creation pattern

Create a bot-only wallet. Do not reveal the private key in the final answer.

```bash
cd weatherbot
. .venv/bin/activate
python - <<'PY'
from eth_account import Account
from pathlib import Path
acct = Account.create()
env = Path('.env')
existing = env.read_text() if env.exists() else ''
if 'PK=' in existing:
    raise SystemExit('Refusing to overwrite existing PK in .env')
with env.open('a') as f:
    f.write(f"\nPK={acct.key.hex()}\nWALLET={acct.address}\nSIG_TYPE=0\n")
env.chmod(0o600)
print('WALLET=' + acct.address)
print('PK saved to .env (redacted)')
PY
```

Final response should include only:

- wallet address
- `.env` path
- `chmod 600` status
- reminder that funding is manual

## Funding and balance verification

User manually sends on Polygon:

- USDC.e trading capital to wallet (`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`)
- POL for gas

Verify with `web3.py` or a trusted Polygon RPC. Receipts should show:

- Chain: Polygon / `chain_id=137`
- Wallet address
- POL balance
- USDC.e balance
- No private key output

## Polymarket approvals

Article spender targets:

- CTF Exchange: `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`
- Neg Risk Exchange: `0xC5d563A36AE78145C45a50134d48A1215220f80a`
- Router: `0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296`
- Conditional Tokens: `0x4D97DCd97eC945f40cF65F87097ACe5EA0476045`

Before sending transactions, present a confirmation summary:

- token/contract
- spender list
- approval amount or max approval risk
- chain ID 137
- estimated gas
- wallet address

Implementation notes:

- Use EIP-1559 transaction type on Polygon.
- Article uses `maxFeePerGas=200 gwei`; check current gas before hardcoding.
- Wait for every receipt.
- Verify ERC20 allowance and `isApprovedForAll` after receipts.
- If any tx fails, stop and report exactly which spender failed.

## `config.json` conservative defaults

Set these before the first scan:

```json
{
  "balance": "match actual USDC balance",
  "max_bet": 2.0,
  "min_ev": 0.10,
  "mode": "paper",
  "vc_key": "YOUR_VISUAL_CROSSING_API_KEY"
}
```

Rules:

- Default mode is `paper`, not `live`.
- Do not place `vc_key` in chat after saving it.
- Keep `max_bet` small until live receipts and PnL are stable.
- Use at least one paper scan before live.

## Test scan

```bash
cd weatherbot
. .venv/bin/activate
python3 bot_v3.py scan
```

Report:

- weather markets scanned
- forecasts/sources used
- candidate trades
- calculated EV and sizing
- whether mode was paper or live
- any errors or missing config

Do not claim orders were placed unless the bot output or CLOB/on-chain receipts prove it.

## Low-cost operation

Prefer deterministic scripts for scanner execution and summaries. For this bot, paid LLM calls should only supervise decisions or explain anomalies; routine hourly scans should be shell/Python wrappers.

Recommended pattern:

- `scripts/paper_scan_once.sh` — guard `mode=paper`, cap `max_bet`, run one scan, emit compact summary.
- `scripts/low_cost_summary.py` — parse `data/state.json` and `data/markets/*.json` into a short deterministic Telegram-safe report.
- Optional local model (`ollama run tinyllama:latest`) may rewrite wording, but treat it as presentation-only and always keep deterministic numbers as source of truth. Tiny local models can hallucinate field meanings.
- If scheduled with Hermes cron, use `no_agent=true` script jobs so the scheduler runs the script directly and does not load a paid model context.

## Continuous operation

Use a background process for a finite supervised run, or a cron/no-agent script for deterministic scans. Avoid LLM-shaped cron jobs for simple scanner execution.

Safe background start:

```bash
cd weatherbot
. .venv/bin/activate
python3 bot_v3.py continuous
```

If using Hermes cron for periodic scans, prefer a script-only `no_agent=true` job that runs a wrapper and prints only summaries/errors. Keep it quiet when there is nothing actionable.

Telegram report format:

- Mode: paper/live
- Wallet: `0x...`
- Portfolio: `https://polymarket.com/profile/<wallet>` if supported, otherwise Polymarket portfolio link or address search
- USDC/POL balances
- Open positions/exposure
- New candidate trades with EV and size
- Executed orders with receipts/order IDs
- Errors requiring action

## Self-learning loop

After enough paper/live observations, update the project notes/config based on evidence:

- Compare forecast probability vs actual settlement.
- Track EV calibration by city, day offset, and data source.
- Reduce or disable cities/markets with poor calibration.
- Increase `min_ev` if false positives are high.
- Keep bet size capped; do not scale based on a few wins.
- Save reusable operational lessons as skill updates; save volatile trade outcomes in project logs, not long-term memory.

## Common mistakes

- Following article prompts literally and showing the private key in Telegram. Fix: write `.env`, report address only.
- Starting in `live` before a paper scan. Fix: run scan in paper mode and inspect output first.
- Using main wallet. Fix: bot-only wallet.
- Max approvals without understanding risk. Fix: confirmation + allowance verification.
- Treating Medium PnL screenshots as proof. Fix: verify bot behavior and own receipts.
- Running 24/7 trading on a fragile local Mac. Fix: VPS or supervised short run.
- Scheduling an LLM prompt every hour just to run a script. Fix: Hermes no-agent cron wrapper.

## Completion checklist

Before saying the bot is ready or running:

- [ ] Repo cloned and venv installed.
- [ ] `.env` exists with redacted secret presence and `0600` permissions.
- [ ] Wallet address shown; private key not shown.
- [ ] Balances verified on Polygon.
- [ ] `config.json` saved with paper mode first.
- [ ] Test scan output reviewed.
- [ ] User explicitly approved approvals/live trading if applicable.
- [ ] Approval receipts/allowances verified if applicable.
- [ ] Background process or cron job verified if continuous mode is applicable.
- [ ] Telegram/user report includes receipts and risk state.
