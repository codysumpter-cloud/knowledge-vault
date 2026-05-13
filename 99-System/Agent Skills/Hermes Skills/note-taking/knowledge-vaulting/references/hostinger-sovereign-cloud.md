# Hostinger Sovereign Cloud Repair & Knowledge Vault Update (2026-05-07)

## Summary
- Created knowledge-vault page: `infrastructure/hostinger-sovereign-cloud.md`
- Pushed to https://github.com/codysumpter-cloud/knowledge-vault
- Updated buddy-brain and omni-buddy repos with TASK_STATE.md and memory/2026-05-07.md
- Verified VPS services (docker, nginx, automind-diagnostic.service, automind-app-factory.service, ollama.service, hermes-gateway.service)
- Fixed SSH key ownership for /opt/bmo-gateway/.deploy_key (changed to hermes:hermes)
- Switched Hermes gateway to use local Ollama model `gemma4:e2b` (via http://127.0.0.1:11434/v1/)
- Verified Telegram bot reachability via Bot API (send_ok True)

## Verification Receipts
- Direct health checks:
  - http://187.77.223.224/healthz → automindlab gateway ok
  - http://187.77.223.224/api/health → enterprise app factory ok
  - http://187.77.223.224/diagnostic/api/health → diagnostic consultation ok
- Hermes CLI smoke test from hermes user completed without API errors.
- Telegram outbound message test succeeded (message_id 68).

## Maintenance Notes
- All VPS repos now owned by hermes user to avoid permission issues.
- Consider setting up cron job to pull repos every 6 hours:
  ```
  0 */6 * * *  /usr/bin/git -C /opt/buddy-brain pull origin main >/dev/null 2>&1
  /usr/bin/git -C /opt/omni-buddy pull origin main >/dev/null 2>&1
  /usr/bin/git -C /opt/bmo-gateway pull origin main >/dev/null 2>&1
  ```
