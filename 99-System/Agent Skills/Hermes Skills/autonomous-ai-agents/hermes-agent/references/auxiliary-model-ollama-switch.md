# Switching Hermes Auxiliary Models to Ollama to Avoid Google API Timeouts

## Problem
Hermes uses auxiliary models for tasks like context compression, vision, etc. By default, these fall back to the `gemini` provider, which requires calling Google's API. This caused frequent errors:
- HTTP 429 (quota exceeded)
- HTTP 401 (unauthorized/invalid key)
- Timeout failures
These errors appeared as "memory compression failed" or similar auxiliary task failures.

## Solution
Reconfigure Hermes to use local Ollama for all auxiliary tasks instead of Google Gemini.

### Steps Applied
1. **Set compression to use Ollama:**
   ```bash
   hermes config set compression.provider ollama
   hermes config set compression.model gemma4:e2b   # or your preferred local model
   hermes config set compression.base_url http://localhost:11434/v1
   ```

2. **Set vision to use Ollama:**
   ```bash
   hermes config set vision.provider ollama
   # vision.model and vision.base_url inherit from compression unless overridden
   ```

3. **(Optional) Verify other auxiliary providers:**
   You can similarly set:
   - `hermes config set auxiliary.session_search.provider ollama`
   - `hermes config set auxiliary.title_generation.provider ollama`
   - etc.
   Or rely on the `auto` provider falling back to your default if you set `model.provider` to ollama.

4. **Restart Hermes** for changes to take effect:
   - In CLI: exit and relaunch `hermes`
   - In gateway: `hermes gateway restart` or send `/restart` to the bot

### Why This Works
- Ollama runs the model locally (e.g., `gemma4:e2b` via `ollama serve`)
- No external API calls are made for compression/vision/tasks
- Eliminates dependency on Google API key validity, quotas, and network latency
- Fully offline after model is pulled

### Verification
- Run a long conversation to trigger context compression (`/compress`) – should succeed without Google API errors
- Use vision tools (if configured) – should process images locally
- Check `hermes config` to confirm the auxiliary sections now show `provider: ollama`

### References
- This fix was derived from session where Google API timeouts kept breaking memory compression.
- See also: `references/dns-guardrails.md` for related protected-action policy.
