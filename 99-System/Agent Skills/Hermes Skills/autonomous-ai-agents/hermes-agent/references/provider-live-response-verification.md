# Hermes provider live-response verification

Use this when a task asks whether Hermes providers/models are "working", "responding", or "fully updated" across machines.

## Core lesson

Do not equate catalog/config updates with provider readiness. A model can appear in `models.py`, normalization, or provider pickers but still fail at runtime due to missing keys, wrong env vars, stale argparse choices, provider routing constraints, or provider-side model availability.

## Verification ladder

1. **Inventory configured secrets without printing them**
   - Check presence and length only for each expected env var in `~/.hermes/.env`.
   - Common vars: `GOOGLE_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `HF_TOKEN`, `HUGGINGFACE_API_KEY`, `NVIDIA_API_KEY`, `OPENAI_API_KEY`, `OLLAMA_API_KEY`.

2. **Check CLI accepts the provider**
   - Run `hermes chat --provider <provider> ...` with a tiny prompt.
   - If argparse says invalid choice, patch provider choices or verify the installed CLI version; catalog entries alone do not expose providers to `--provider`.

3. **Run a tiny end-to-end response probe per provider**
   - Example: `hermes chat -Q --provider gemini -m gemma-4-31b-it -q 'Reply exactly OK_GEMINI'`.
   - Capture exit code and the exact returned token.
   - Use `-v` only when quiet output hides the provider error.

4. **If Hermes output is opaque, raw-call the provider API**
   - Use OpenAI-compatible `/v1/chat/completions` endpoints where applicable.
   - Keep body tiny (`max_tokens: 16`) and never print API keys.

5. **Report a PASS only when the provider returns the expected text**
   - `exit 0` plus exact `OK_*` response is a pass.
   - 401 = auth/key issue, not a model-catalog issue.
   - 404/model unavailable = provider routing/model availability issue, not proof the model is absent everywhere.

## Session-specific receipts from 2026-05-08

- Gemini / Google AI Studio with `gemma-4-31b-it`: PASS, returned `OK_GEMINI`.
- OpenRouter with `google/gemma-4-31b-it`: FAIL, 404 `No allowed providers are available for the selected model`; OpenRouter metadata listed available providers but requested provider was constrained to `google-ai-studio`.
- Hugging Face with `google/gemma-4-31B-it`: FAIL, 401 / no valid `HF_TOKEN` or `HUGGINGFACE_API_KEY` on VPS.
- NVIDIA NIM with `google/gemma-4-31b-it`: FAIL, 401 / no valid `NVIDIA_API_KEY` on VPS.
- Ollama Cloud with `gemma4:31b-it`: FAIL, catalog entry existed but runtime said `Unknown provider 'ollama-cloud'`; provider/auth adapter was not fully wired.
- Native OpenAI with `gemma-4-31b-it`: FAIL, configured `OPENAI_API_KEY` was rejected by OpenAI and appeared to be a Google-style key.

## Reporting style for this user

Use receipt-based wording: "catalog updated" and "live response verified" are separate states. If only one provider passed, say so directly; do not summarize as "all set" or "fully working" until every provider has a successful live response probe.
