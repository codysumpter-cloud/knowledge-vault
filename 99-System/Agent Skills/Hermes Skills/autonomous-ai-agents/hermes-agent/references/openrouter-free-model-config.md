# OpenRouter Free Model Configuration for Hermes Agent

## Problem
When using OpenRouter with Hermes Agent, the non-free model ID `google/gemma-4-31b-it` was rejected after the first message, causing HTTP 500 errors. This occurred because:
1. The model ID was invalid for the free tier
2. OpenRouter returned 500 errors when quota/auth issues occurred
3. Hermes would retry 3 times before failing

## Solution
Use the free variant of the model ID and configure proper fallback behavior.

### Configuration Steps

1. Set the model to the free variant:
```yaml
model:
  default: google/gemma-4-31b-it:free   # Note the :free suffix
  provider: ''                          # Empty enables catalog-based fallback
```

2. Configure the OpenRouter provider to use the free model:
```yaml
providers:
  openrouter:
    api_key: your-openrouter-key-here
    api: https://openrouter.ai/api/v1
    default_model: google/gemma-4-31b-it:free
    models:
      - google/gemma-4-31b-it:free
    name: OpenRouter
```

3. Ensure local Ollama is configured as fallback:
```yaml
providers:
  ollama-launch:
    api: http://127.0.0.1:11434/v1
    default_model: gemma4:31b-cloud
    models:
      - gemma4:31b-cloud
    name: Ollama
```

### Verification
Run this command to see which provider Hermes will use:
```bash
hermes model info google/gemma-4-31b-it:free
```

Expected output should show Provider: openrouter (if credits available) or fall back to ollama-launch.

### Notes
- The free tier has rate limits - monitor usage at https://openrouter.ai/settings/usage
- If free tier is exhausted, Hermes will automatically fall back to the next provider in the catalog that can serve the model
- Local Ollama (`gemma4:e2b`) remains configured for auxiliary tasks (vision, compression, etc.) to avoid Google API timeouts
