# Gateway Gemini 429 from stale session context

Use this when Hermes Gateway is running, `hermes chat --provider gemini ... -q` succeeds for a tiny prompt, but Telegram/Discord gateway turns return HTTP 429 from Gemini/Gemma.

## Symptom receipts

Gateway journal examples:

```text
Provider: gemini
Model: gemma-4-31b-it
Endpoint: https://generativelanguage.googleapis.com/v1beta/openai
HTTP 429 RESOURCE_EXHAUSTED
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_paid_tier_input_token_count
limit: 16000, model: gemma-4-31b
Context: 37-39 msgs, ~14,500 tokens
```

This is not necessarily a provider-selection bug. It can be a stale messaging-platform session carrying a huge transcript into each request and then retrying into the quota window.

## Diagnostic sequence

Run from a safe working directory on the VPS:

```bash
cd /opt/buddy-brain
sudo -u hermes env HOME=/home/hermes HERMES_HOME=/home/hermes/.hermes \
  PATH=/home/hermes/.hermes/hermes-agent/venv/bin:/usr/local/bin:/usr/bin:/bin \
  /home/hermes/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main chat \
  --provider gemini -m gemma-4-31b-it -Q -q "Reply exactly OK"
```

Interpretation:

- If this returns `OK`, Gemini credentials/model routing work for small requests.
- If gateway still gets 429, inspect the gateway session size instead of changing DNS or provider names.

Inspect active sessions:

```bash
sudo -u hermes python3 - <<'PY'
from pathlib import Path
import json
p = Path('/home/hermes/.hermes/sessions/sessions.json')
data = json.loads(p.read_text())
for k, v in data.items():
    print('KEY', k)
    print({kk: v.get(kk) for kk in ['session_id','platform','chat_type','display_name','updated_at','total_tokens','last_prompt_tokens','resume_pending','suspended']})
PY
```

## Minimal fix used successfully

Back up before editing:

```bash
TS=$(date -u +%Y%m%d-%H%M%S)
mkdir -p /home/hermes/.hermes/backup-gemini429/$TS
cp /home/hermes/.hermes/config.yaml /home/hermes/.hermes/backup-gemini429/$TS/config.yaml
cp /home/hermes/.hermes/sessions/sessions.json /home/hermes/.hermes/backup-gemini429/$TS/sessions__sessions.json
```

Mark the affected gateway session suspended so the next platform message creates a clean session:

```bash
sudo -u hermes python3 - <<'PY'
from pathlib import Path
from datetime import datetime
import json
p = Path('/home/hermes/.hermes/sessions/sessions.json')
data = json.loads(p.read_text())
key = 'agent:main:telegram:dm:<USER_ID>'
if key not in data:
    raise SystemExit(f'missing session key: {key}')
data[key]['suspended'] = True
data[key]['resume_pending'] = False
data[key]['last_prompt_tokens'] = 0
data[key]['total_tokens'] = 0
data[key]['updated_at'] = datetime.utcnow().replace(microsecond=0).isoformat()
p.write_text(json.dumps(data, indent=2))
print('suspended', key, data[key].get('session_id'))
PY
```

Keep `model.context_length` at least 64000; Hermes rejects smaller values at startup. To compress earlier without violating the minimum, set compression guardrails:

```yaml
model:
  provider: gemini
  default: gemma-4-31b-it
  max_tokens: 2048
  context_length: 64000
compression:
  enabled: true
  threshold: 0.12
  target_ratio: 0.18
  protect_last_n: 12
```

Restart via the installed user service, not a foreground SSH process:

```bash
UID=$(id -u hermes)
sudo -u hermes env XDG_RUNTIME_DIR=/run/user/$UID systemctl --user restart hermes-gateway.service
```

Verify with a restart timestamp so pre-restart errors do not pollute the result:

```bash
TS='YYYY-MM-DD HH:MM:SS'
sudo -u hermes env XDG_RUNTIME_DIR=/run/user/$(id -u hermes) \
  journalctl --user -u hermes-gateway.service --since "$TS" --no-pager \
  | grep -Ei 'error|exception|traceback|failed|429|401|permission|gemini|gemma' || true
```

## Pitfalls

- Do not conclude “both Google and Gemini are selected” solely from labels. `gemini` is the provider slug; Google/Gemini/`generativelanguage.googleapis.com` are the same family in logs/UI.
- A foreground `hermes gateway run --replace` over SSH may print the startup banner and exit cleanly; the durable process should be the systemd user service.
- Lowering `model.context_length` below 64000 causes Hermes Agent initialization failure. Use compression thresholds instead.
- Gemini 429 with `generate_content_paid_tier_input_token_count` and ~14k prompt tokens means quota window pressure; restarting alone will not fix it if the same stale platform session is reused.
