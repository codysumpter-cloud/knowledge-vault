# VPS Gateway Troubleshooting Guide

## Common Issues and Solutions

### 1. Permission Denied Errors
**Symptom**: `/usr/local/bin/hermes: /usr/local/lib/hermes-agent/venv/bin/hermes: /usr/local/lib/hermes-agent/venv/bin/python3: bad interpreter: Permission denied`

**Solution**:
```bash
chmod +x /usr/local/lib/hermes-agent/venv/bin/python3 /usr/local/lib/hermes-agent/venv/bin/hermes
```

### 2. User Switching Issues
**Symptom**: `sudo: unknown user hermes` or `su: Sorry` when trying to run gateway as hermes user

**Primary Solution**: Use `runuser` instead of `su` or `sudo`:
```bash
runuser -l hermes -c '/home/hermes/.hermes/hermes-agent/venv/bin/hermes gateway run --replace'
```

**Alternative Solution**: Run as root but set HOME to hermes' home directory:
```bash
export HOME=/home/hermes
/home/hermes/.hermes/hermes-agent/venv/bin/hermes gateway run --replace
```

**Additional Notes**:
- If `runuser` is not available, try `su -s /bin/bash hermes -c '<command>'`
- Ensure the hermes user has a valid shell (`/bin/bash`) and home directory permissions are correct
- The hermes user must exist in `/etc/passwd` and have a UID/GID
- In our specific case on Hostinger VPS, the hermes user existed (uid=1001) but had switching issues with sudo/su that were resolved with the above methods
- When using the HOME workaround, ensure the hermes user has proper permissions to access the directory and files

### 3. API Quota Exhaustion (HTTP 429) and HTTP 500 Errors
**Symptom**:
- Gateway works for one message then stops with "HTTP 429: Gemini HTTP 429 (RESOURCE_EXHAUSTED)"
- Gateway starts but exits quickly with "HTTP 500: Gemini HTTP 500 (INTERNAL): Internal error encountered"

**Solution**:
1. Check API quota in Google AI Studio
2. Verify API key is correctly set in `~/.hermes/.env` (no extra characters/newlines)
3. Consider switching to a different provider or model temporarily
4. For immediate relief, use local Ollama fallback:
   ```yaml
   model:
     default: gemma4:31b-cloud
     provider: ollama
     base_url: http://localhost:11434/v1
   ```
5. **Specific fix for invalid .env characters**: Clean the .env file:
   ```bash
   # Backup first
   cp .hermes/.env .hermes/.env.backup
   # Then recreate with proper format (no trailing spaces or newlines in values)
   cat > .hermes/.env <<EOF
   GOOGLE_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   # ... other vars
   EOF
   ```

### 4. Service Management on VPS
**Best Practice**: Use systemd user service instead of foreground SSH sessions

**Setup**:
1. Ensure the hermes user exists and has proper permissions
2. Set XDG_RUNTIME_DIR for systemd user service:
   ```bash
   export XDG_RUNTIME_DIR=/run/user/$(id -u hermes)
   ```
3. Start service:
   ```bash
   systemctl --user start hermes-gateway
   ```
4. Check status:
   ```bash
   systemctl --user status hermes-gateway
   ```

### 5. Environment Variable Loading
**Symptom**: API key not being recognized despite being set

**Solution**:
1. Verify .env file location: `hermes config env-path`
2. Check if .env is being loaded: ensure it's in the correct location (~/.hermes/.env)
3. Format: `GOOGLE_API_KEY=your_key_here` (no quotes, no spaces around =)
4. **Specific fix for su environment issues**: When using `su - hermes -c`, explicitly set HOME and source environment:
   ```bash
   su - hermes -c "cd /home/hermes && set -a && source .hermes/.env && set +a && .hermes/hermes-agent/venv/bin/hermes gateway run --replace"
   ```

### 6. Gateway Process Management
**To check if gateway is running**:
```bash
ps aux | grep hermes
```

**To restart gateway**:
```bash
# Preferred method (if using systemd)
systemctl --user restart hermes-gateway

# Fallback method
pkill -f hermes
runuser -l hermes -c '/home/hermes/.hermes/hermes-agent/venv/bin/hermes gateway run --replace' &
```

**Specific fix for PID file issues**: Remove stale gateway lock/state files if gateway fails to start:
```bash
rm -f /home/hermes/.hermes/gateway.lock /home/hermes/.hermes/gateway_state.json
```

### 7. Log Checking
**Gateway logs**:
```bash
cat /tmp/hermes_gateway.log
journalctl --user -u hermes-gateway --since "1 hour ago"
```

**CLI logs** (if running interactively):
```bash
cat ~/.hermes/logs/gateway.log
```

### 8. "Gateway shutting down" Telegram noise during restarts
**Symptom**: The bot appears to be working but Telegram receives repeated messages like `Gateway shutting down`, `Gateway restarting`, or `Your current task will be interrupted` while services are being stabilized.

**Triage first** — do not assume a crash loop:
```bash
systemctl status hermes-gateway.service --no-pager -l | sed -n '1,35p'
journalctl -u hermes-gateway.service --since '20 minutes ago' --no-pager -o short-iso | tail -160
su - hermes -c 'tail -120 /home/hermes/.hermes/logs/gateway.log'
journalctl -k --since '30 minutes ago' --no-pager | egrep -i 'oom|killed process|out of memory' || true
systemctl show hermes-gateway.service -p NRestarts -p ActiveEnterTimestamp -p Result
```

**Interpretation**:
- `Received SIGTERM as a planned --replace takeover — exiting cleanly` means a newer `hermes gateway run --replace` intentionally took over. This is not a model/provider failure.
- `Main process exited, code=killed, status=9/KILL` after `TimeoutStopSec` usually means systemd killed a slow shutdown path; check whether shutdown notifications or adapter sends are blocking stop.
- Telegram `TimedOut` while registering commands can be transient network slowness; if the next lines show `Connected to Telegram` and `Gateway running`, treat it as warning-level unless it repeats.

**Suppress operator lifecycle noise in user-facing Telegram chats**:
```yaml
platforms:
  telegram:
    enabled: true
    gateway_restart_notification: false
```

Restart and verify the setting actually loaded:
```bash
systemctl restart hermes-gateway.service
su - hermes -c "cd /home/hermes && . .hermes/hermes-agent/venv/bin/activate && python - <<'PY'
from gateway.config import load_gateway_config, Platform
c = load_gateway_config()
pc = c.platforms.get(Platform.TELEGRAM)
print(pc.enabled, pc.gateway_restart_notification, pc.extra if pc else None)
PY"
```
Expected output includes `True False`.

Then verify receipts:
```bash
sleep 70
systemctl is-active hermes-gateway.service
systemctl show hermes-gateway.service -p NRestarts -p ActiveEnterTimestamp -p Result
journalctl -u hermes-gateway.service --since '70 seconds ago' --no-pager -o short-iso | egrep 'Received SIGTERM|Scheduled restart|Main process exited|Gateway running|Connected to Telegram' || true
```
Expected: active service, no new restarts, and no Telegram shutdown messages after the final intentional restart.

## Verification Steps
After making changes, verify with a live provider probe. Do not print raw API keys in receipts:
```bash
hermes chat -Q --provider gemini -m models/gemma-4-31b-it -q 'Reply exactly OK_GEMINI'
# or the current default provider/model:
hermes chat -Q -q 'Reply exactly OK_DEFAULT'
```

If this returns the expected token and gateway logs show `Gateway running`, the gateway should work consistently.
