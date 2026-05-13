# VPS Cron No-Agent Script Jobs Pattern

When running Hermes on a resource-constrained VPS (e.g., 8GB RAM Intel Mac or low-cost cloud VPS), frequent cron jobs that execute simple scripts should not spawn full LLM-agent prompts. Instead, use `no_agent=true` with executable script wrappers.

## Problem
- Cron jobs shaped as prompts (e.g., `Execute: python3 /path/to/script.py`) repeatedly load full Hermes context + LLM prompt
- This consumes CPU/RAM and can make Telegram/Discord feel sluggish or "stuck"
- Especially problematic for minute-by-minute jobs like `TradeNotifications`

## Solution Pattern
Convert prompt-shaped cron jobs to no-agent script jobs:

### 1. Create executable wrapper scripts
Store in `/home/hermes/.hermes/scripts/` (ensure `hermes:hermes` ownership):

```bash
# Example: /home/hermes/.hermes/scripts/run_market_scout.sh
#!/bin/bash
set -euo pipefail
cd /home/hermes/bread-makers/money-printer-v2
source /home/hermes/.hermes/.env >/dev/null 2>&1 || true
venv/bin/python src/classes/YouTube.py "$@"
```

Make executable:
```bash
chmod +x /home/hermes/.hermes/scripts/run_market_scout.sh
```

### 2. Configure cron job as no_agent
In Hermes cron configuration (via `hermes cron edit` or direct JSON):

```jsonc
{
  "command": "/home/hermes/.hermes/scripts/run_market_scout.sh",
  "args": ["--scan", "--quiet"],
  "no_agent": true,
  "schedule": "0 * * * *",  // hourly example
  "delivery": "silent"      // or specify chat_id for output
}
```

### 3. Key benefits
- Script runs directly as shell process (no LLM context load)
- Near-zero overhead compared to prompt-shaped jobs
- Preserves Telegram responsiveness
- Still gets proper logging and error handling via stdout/stderr

## Applied Examples (money-printer-v2 & trading bots)
As of 2026-05-09, converted to no_agent:
- MarketScout
- Technical Scout
- Political Scout
- General's Wealth Report
- TradeNotifications (every minute)

## Verification
Check cron mode:
```bash
su - hermes -c "hermes cron list" | grep no_agent
```

Check recent execution:
```bash
journalctl -u hermes-gateway.service --since "1 hour ago" | grep -i "no_agent\|script"
```
