# Google Gemini/Gemma default-model fix (Updated for Fallback Configuration)

Session pattern: user wanted Hermes Agent to use the best Gemma 4 model with automatic fallback between cloud providers and local Ollama.

Observed failure:

- Config had `model.default: gemma4`, `model.provider: gemini`, `model.base_url: https://generativelanguage.googleapis.com/v1beta`.
- Gateway/Telegram logs showed Gemini HTTP 404:
  `models/gemma4 is not found for API version v1beta, or is not supported for generateContent`.

Better approach (current recommendation):

Instead of hard-coding a specific provider, use an empty provider field to enable model catalog lookup with automatic fallback:

```bash
hermes config set model.default google/gemma-4-31B-it
hermes config set model.provider ''  # Empty enables catalog lookup
hermes config set model.base_url http://localhost:11434/v1  # Still needed for local fallback
hermes config set model.api_key ollama  # Local Ollama auth
```

This configuration allows Hermes to:
1. Consult the model catalog to find providers offering `google/gemma-4-31B-it`
2. Use the first available provider (typically OpenRouter or Gemini based on catalog order)
3. Automatically fall back to local Ollama (`gemma4:e2b`) if cloud providers fail
4. Avoid hard-coding provider-specific URLs and auth

Important correction: do **not** label native Gemini `gemma-4-31b-it` as "free" or append an OpenRouter-style `:free` suffix unless the active provider is OpenRouter and the live OpenRouter catalog confirms that exact model ID. For native Google/Gemini, the canonical model ID is `gemma-4-31b-it`. Google's 429 text may mention `generate_content_paid_tier_input_token_count`; that is a Google quota metric name, not proof that Hermes selected a paid key.

Discovery technique:

- Read `~/.hermes/config.yaml` and `~/.hermes/.env`.
- Use the Google models list endpoint with `GOOGLE_API_KEY` from `.env` without printing the key:
  `https://generativelanguage.googleapis.com/v1beta/models?key=[REDACTED]
- Filter for models supporting `generateContent` and names containing `gemma`/`gemini`.

Models available in that session included:

- `gemma-4-26b-a4b-it`
- `gemma-4-31b-it`

Original fix applied (for reference):

```bash
hermes config set model.default gemma-4-31b-it
hermes config set model.provider gemini
hermes config set model.base_url https://generativelanguage.googleapis.com/v1beta
```

Verification (for both approaches):

```bash
# Verify which provider Hermes will use:
hermes model info google/gemma-4-31B-it

# Test with explicit provider (original approach):
hermes chat --provider gemini -m gemma-4-31b-it -Q -q 'Reply with exactly: OK'

# Test with default provider (new approach):
hermes chat -Q -q 'Reply with exactly: OK_DEFAULT'

# Gateway verification:
hermes gateway restart
hermes gateway status
```

Telegram/gateway verification:

- `hermes gateway restart` restarts the gateway service so Telegram picks up config changes.
- `hermes gateway status` should show the service loaded and running.
- Check logs after the restart timestamp, not the whole file, because pre-restart failures remain in logs:

```bash
python3 - <<'PY'
from pathlib import Path
log = Path('~/.hermes/logs/gateway.log').expanduser()
cut = 'YYYY-MM-DD HH:MM:SS'  # restart/connect timestamp
seen = False
bad = []
for line in log.read_text(errors='ignore').splitlines():
    if line.startswith(cut) or (len(line) >= 19 and line[:19] > cut and line[:4].isdigit()):
        seen = True
    if seen and 'gemma4' in line.lower():
        bad.append(line)
print('post_restart_gemma4_matches=', len(bad))
for line in bad[-10:]:
    print(line)
PY
```

Pitfalls:

- `gemma4` is not a valid Google model ID even if the user colloquially says Gemma 4.
- Native Gemini base URL in Hermes can be `https://generativelanguage.googleapis.com/v1beta`; do not automatically change to `/openai` unless using the OpenAI-compatible transport explicitly.
- Old gateway log entries can make it look like Telegram is still broken. Filter logs by timestamp after restart.
- If a gateway response is already in-flight during restart, old-model errors may be emitted during shutdown; verify with a fresh post-restart log window.
- **New pitfall with empty provider**: If no provider in the catalog offers the specified model, Hermes will fail to start. Always verify with `hermes model info <model>` first.
