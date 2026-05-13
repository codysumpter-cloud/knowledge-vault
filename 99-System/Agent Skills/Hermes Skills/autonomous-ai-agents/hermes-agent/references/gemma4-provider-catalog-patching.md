# Gemma 4 provider catalog patch notes

Use this when adding `gemma-4-31b-it` (or another newly launched model) across Hermes model picker/provider resolution.

## Files that may need updates

Catalog visibility alone is not enough. For provider switching to work end-to-end, check all relevant layers:

- `hermes_cli/models.py` — static provider catalogs, validation fallbacks, model picker ordering.
- `agent/models_dev.py` — models.dev-derived provider/model metadata if the bundled snapshot is stale.
- `hermes_cli/model_normalize.py` — provider-specific model ID normalization.
- `hermes_cli/auth.py` — provider auth registry. Missing entries cause `Unknown provider '<name>'` during runtime credential resolution.
- `hermes_cli/providers.py` — provider overlays and aliases. Missing overlays can make provider detection/listing inconsistent.
- `hermes_cli/runtime_provider.py` — only if credentials/base URL routing needs provider-specific behavior.

## Provider-specific Gemma 4 IDs observed

- Gemini / Google AI Studio: `gemma-4-31b-it`
- OpenRouter: `google/gemma-4-31b-it` and free variant `google/gemma-4-31b-it:free`
- Hugging Face router: `google/gemma-4-31B-it` (case-sensitive repo spelling)
- NVIDIA NIM: `google/gemma-4-31b-it`
- OpenAI/custom/Ollama-style flat providers: preserve the bare or local configured ID unless that provider requires a namespace.

## Verification probes

```bash
python -m py_compile hermes_cli/models.py hermes_cli/model_normalize.py hermes_cli/auth.py hermes_cli/providers.py agent/models_dev.py

python - <<'PY'
from hermes_cli.model_normalize import normalize_model_for_provider
for p in ['gemini','openrouter','nvidia','huggingface','openai','ollama-cloud']:
    print(p, normalize_model_for_provider('gemma-4-31b-it', p))

from hermes_cli.model_switch import switch_model
for provider in ['huggingface','nvidia','gemini','openrouter']:
    r = switch_model('gemma-4-31b-it', 'gemini', 'old', explicit_provider=provider,
                     current_api_key='bad', current_base_url='https://generativelanguage.googleapis.com/v1beta')
    print(provider, r.success, r.target_provider, r.new_model, (r.error_message or r.warning_message or '')[:160])
PY
```

For Gemini API receipt:

```bash
curl -sS "https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent?key=[REDACTED]" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Reply exactly OK"}]}]}'
```

## Pitfalls observed

- `provider_model_ids()` showing a model does not prove `/model --provider <provider>` works. `switch_model()` also exercises auth registry, provider overlays, normalization, and validation.
- Copying a newer local `auth.py` or `providers.py` wholesale to an older VPS Hermes checkout can break imports if helper functions differ. Prefer targeted patches or mirror the whole compatible checkout.
- OpenRouter has both paid and `:free` IDs; for free-tier use, configure the `:free` variant explicitly.
