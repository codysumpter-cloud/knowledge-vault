# Empty Provider Fallback Configuration

Session pattern: User wanted Hermes to use cloud providers (Gemini/OpenRouter) for google/gemma-4-31B-it with local Ollama as fallback, avoiding hard-coding a specific provider.

Configuration applied:
```yaml
model:
  default: google/gemma-4-31B-it
  provider: ''  # Empty enables model catalog lookup
  api_key: ollama  # Still needed for local fallback
  base_url: http://localhost:11434/v1
```

How it works:
1. With `provider: ''`, Hermes consults the model catalog
2. The catalog lists which providers offer which models
3. Hermes selects the first provider in the catalog that has `google/gemma-4-31B-it`
4. In this setup, OpenRouter and Gemini are checked before local Ollama
5. If cloud providers fail (quota/errors), falls back to local Ollama (`gemma4:e2b`)

Verification:
```bash
hermes model info google/gemma-4-31B-it
# Should show provider: openrouter (or gemini) based on catalog order

# To force a specific provider:
hermes config set model.provider openrouter
hermes config set model.default google/gemma-4-31B-it
```

Benefits:
- Automatic fallback when providers hit rate limits
- No need to modify config when adding/removing providers
- Local models remain available as last resort
- Works with all configured providers (Ollama, OpenRouter, Gemini, NVIDIA, etc.)

See also: `references/gemini-gemma4-default.md` for Gemini-specific verification steps.
