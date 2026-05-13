# Local Gemma 4 / Ollama fallback for small VPS Hermes gateways

Use this reference when a Hermes gateway is alive on a VPS but all cloud providers fail with quota/auth errors and the user wants a local fallback instead of DNS/app changes.

## Session trigger pattern

Observed on a Hostinger Ubuntu VPS with ~8 GiB RAM, 2 vCPU, no GPU:

- Gateway could reply once or twice, then model calls failed.
- Gemini/Gemma provider: `HTTP 429` quota exceeded on `gemma-4-31b-it`.
- OpenRouter fallback: `HTTP 401 User not found`.
- OpenAI key probe: `HTTP 401 Unauthorized`.
- Direct app health remained OK, so DNS/app runtime was not the root cause.

## Guardrail

Do not pivot to DNS/nameserver changes just because a domain does not route as expected or a panel says records are managed elsewhere. If the symptom is gateway/API errors, inspect provider logs/config first. DNS changes are a separate release action and require explicit user approval.

## Minimal local fallback workflow

```bash
# On VPS as root
free -h

# Add swap before loading local models on an 8 GiB machine
if [ ! -f /swapfile ]; then
  fallocate -l 8G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  echo "/swapfile none swap sw 0 0" >> /etc/fstab
else
  swapon --show | grep -q /swapfile || swapon /swapfile || true
fi

# Install Ollama CPU runtime
curl -fsSL https://ollama.com/install.sh | sh
systemctl enable --now ollama

# Pull small Gemma 4, not 31B
ollama pull gemma4:e2b
ollama list
```

Hermes config shape:

```yaml
model:
  default: gemma4:e2b
  provider: custom
  base_url: http://127.0.0.1:11434/v1/
  max_tokens: 2048
  context_length: 64000
```

Also set auxiliary sections (`vision`, `compression`, `session_search`, `title_generation`) to the same custom model/base_url when cloud auxiliary providers are failing.

## Verification commands

```bash
# Gateway and app health
systemctl is-active ollama docker nginx
sudo -u hermes XDG_RUNTIME_DIR=/run/user/$(id -u hermes) systemctl --user is-active hermes-gateway.service
curl -fsS http://127.0.0.1:11434/api/tags

# Run Hermes from a directory the hermes user can read; do not run from /root.
cd /home/hermes
sudo -u hermes env HOME=/home/hermes XDG_RUNTIME_DIR=/run/user/$(id -u hermes) \
  /home/hermes/.local/bin/hermes chat -q "Reply with OK only." --yolo

# Post-restart provider-error grep
sudo -u hermes XDG_RUNTIME_DIR=/run/user/$(id -u hermes) \
  journalctl --user -u hermes-gateway.service --no-pager --since "5 minutes ago" \
  | grep -Ei "HTTP 429|HTTP 401|gemma-4-31b|openrouter|gemini|error|failed|traceback" || true
```

## Pitfalls

- Hermes may enforce a minimum advertised context length. If a local model config with `context_length: 4096` is rejected, set the advertised `context_length` to `64000`; this lets Hermes initialize but does not mean the VPS can practically process a huge real prompt.
- `gemma4:e2b` can be slow and swap-heavy on 2 vCPU / 8 GiB RAM. Expect latency.
- `gemma4:e2b` may behave like a reasoning/thinking model and spend tokens before final content; exact-output smoke tests may be imperfect even when the provider path is fixed.
- Stale pre-restart logs can look like current failure. Filter logs by restart time or `--since`.
- A direct Telegram bot API send only proves token/chat reachability. True gateway verification requires an inbound user DM and a model-generated reply.
