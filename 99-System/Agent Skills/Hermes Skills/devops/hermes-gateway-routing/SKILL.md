---
name: hermes-gateway-routing
description: Configure, deploy, and troubleshoot Hermes Gateway provider priorities (Cloud vs Local).
---

# Hermes Gateway Model Routing & Provider Management

This skill governs the configuration, deployment, and troubleshooting of the Hermes Gateway, specifically focusing on the balance between cloud providers and local fallback models.

## Provider Priority Workflow
1. **Cloud Primary:** Always prioritize high-parameter models (e.g., 31B+) from free cloud providers (OpenRouter, Google AI Studio) to maximize intelligence and avoid local hardware bottlenecks.
2. **Local Fallback:** Use local Ollama models (e.g., 2B variants) exclusively for:
    - Auxiliary tasks (Vision, Compression, Session Search, Title Generation).
    - Emergency fallback when cloud API limits are reached or connectivity is lost.
3. **Configuration:** Define these priorities in `~/.hermes/config.yaml` by setting `model.provider` to the cloud service and `model.default` to the specific cloud model ID.

## Common Pitfalls & Fixes
- **The "Nemotron" Loop:** If the gateway defaults to `nvidia/nemotron` and throws 401s, it is usually because `model.default` is unset or mismatched. Fix by explicitly defining the cloud model ID in `config.yaml`.
- **OpenRouter Credit Block (402):** Even "free" models on OpenRouter can return `HTTP 402 Insufficient Credits` if the account has zero balance. Pivot immediately to Google AI Studio (Gemini/Gemma) as the primary provider if this occurs, as they have a more permissive free tier.
- **Hardware Thrashing:** NEVER set a 31B+ model as `provider: custom` on an 8GB RAM machine (VPS). This causes extreme swap-thrashing and system instability.
- **Sudo Problems:** Use `su - <user> -c "<command>"` or `sudo -u <user>` for gateway restarts on Linux to ensure correct environment variables and home directory resolution.

## Execution Steps
1. **Verify Keys:** Check `.env` for active `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`.
2. **Apply Config:** Use a heredoc to overwrite `config.yaml` with the precise provider/model mapping.
3. **Restart Gateway:** Terminate existing gateway processes and launch as the service user (e.g., `hermes`).
4. **Verification:** Send a test message to the integrated platform (Telegram) to confirm the model's intelligence/latency matches the expected tier.
