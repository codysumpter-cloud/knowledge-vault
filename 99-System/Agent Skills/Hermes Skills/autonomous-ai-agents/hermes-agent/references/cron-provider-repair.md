# Cron provider repair notes

Use when a Hermes cron job fails before doing work with an error like:

```text
RuntimeError: Unknown provider 'custom:local'. Check 'hermes model' for available providers, or run 'hermes doctor' to diagnose config issues.
```

## Repair pattern

1. List jobs and identify the failing job ID/name:
   ```bash
   hermes cron list --all
   ```
   Or use the `cronjob` tool with `action=list` from gateway sessions.
2. Compare the job's configured `provider`/`model` to known working jobs and current `hermes model` / provider config.
3. Update the job's model routing in place instead of deleting/recreating the schedule when the prompt and timing are correct.
   - Example known-good Mac routing from this session:
     - provider: `ollama-launch`
     - model: `gemma4:31b-cloud`
4. Trigger a manual run to verify the scheduler accepted the new routing:
   ```bash
   hermes cron run <job-id>
   ```
   Or `cronjob` tool `action=run`.
5. Check the next cron response or `hermes cron list --all` for status.

## Tool pattern

From a gateway/tool session:

```json
{"action":"update","job_id":"<id>","model":{"provider":"ollama-launch","model":"gemma4:31b-cloud"}}
```

Then:

```json
{"action":"run","job_id":"<id>"}
```

## Pitfalls

- Do not treat `custom:local` as a durable provider alias unless it appears in current provider config. Cron jobs can outlive provider aliases.
- Do not recreate the job when only routing is stale; update preserves schedule, delivery target, prompt, skills/toolsets, and history.
- For deterministic script-only tasks, prefer `no_agent=true` script jobs instead of prompt-shaped agent jobs; see `references/vps-cron-no-agent-script-jobs.md`.
