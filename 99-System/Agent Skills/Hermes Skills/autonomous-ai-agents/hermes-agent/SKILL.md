---
name: hermes-agent
description: "Configure, extend, or contribute to Hermes Agent."
version: 2.0.0
author: Hermes Agent + Teknium
license: MIT
metadata:
  hermes:
    tags: [hermes, setup, configuration, multi-agent, spawning, cli, gateway, development]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [claude-code, codex, opencode]
---

# Hermes Agent

Hermes Agent is an open-source AI agent framework by Nous Research that runs in your terminal, messaging platforms, and IDEs. It belongs to the same category as Claude Code (Anthropic), Codex (OpenAI), and OpenClaw — autonomous coding and task-execution agents that use tool calling to interact with your system. Hermes works with any LLM provider (OpenRouter, Anthropic, OpenAI, DeepSeek, local models, and 15+ others) and runs on Linux, macOS, and WSL.

What makes Hermes different:

- **Self-improving through skills** — Hermes learns from experience by saving reusable procedures as skills. When it solves a complex problem, discovers a workflow, or gets corrected, it can persist that knowledge as a skill document that loads into future sessions. Skills accumulate over time, making the agent better at your specific tasks and environment.
- **Persistent memory across sessions** — remembers who you are, your preferences, environment details, and lessons learned. Pluggable memory backends (built-in, Honcho, Mem0, and more) let you choose how memory works.
- **Multi-platform gateway** — the same agent runs on Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, and 10+ other platforms with full tool access, not just chat.
- **Provider-agnostic** — swap models and providers mid-workflow without changing anything else. Credential pools rotate across multiple API keys automatically.
- **Profiles** — run multiple independent Hermes instances with isolated configs, sessions, skills, and memory.
- **Extensible** — plugins, MCP servers, custom tools, webhook triggers, cron scheduling, and the full Python ecosystem.

People use Hermes for software development, research, system administration, data analysis, content creation, home automation, and anything else that benefits from an AI agent with persistent context and full system access.

**This skill helps you work with Hermes Agent effectively** — setting it up, configuring features, spawning additional agent instances, troubleshooting issues, finding the right commands and settings, and understanding how the system works when you need to extend or contribute to it.

**Docs:** https://hermes-agent.nousresearch.com/docs/

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Interactive chat (default)
hermes

# Single query
hermes chat -q "What is the capital of France?"

# Setup wizard
hermes setup

# Change model/provider
hermes model

# Check health
hermes doctor
```

---

## CLI Reference

### Global Flags

```
hermes [flags] [command]

  --version, -V             Show version
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --pass-session-id         Include session ID in system prompt
```

No subcommand defaults to `chat`.

### Chat

```
hermes chat [flags]
  -q, --query TEXT          Single query, non-interactive
  -m, --model MODEL         Model (e.g. anthropic/claude-sonnet-4)
  -t, --toolsets LIST       Comma-separated toolsets
  --provider PROVIDER       Force provider (openrouter, anthropic, nous, etc.)
  -v, --verbose             Verbose output
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --source TAG              Session source tag (default: cli)
```

### Configuration

```
hermes setup [section]      Interactive wizard (model|terminal|gateway|tools|agent)
hermes model                Interactive model/provider picker
hermes config               View current config
hermes config edit          Open config.yaml in $EDITOR
hermes config set KEY VAL   Set a config value
hermes config path          Print config.yaml path
hermes config env-path      Print .env path
hermes config check         Check for missing/outdated config
hermes config migrate       Update config with new options
hermes login [--provider P] OAuth login (nous, openai-codex)
hermes logout               Clear stored auth
hermes doctor [--fix]       Check dependencies and config
hermes status [--all]       Show component status
```

### Tools & Skills

```
hermes tools                Interactive tool enable/disable (curses UI)
hermes tools list           Show all tools and status
hermes tools enable NAME    Enable a toolset
hermes tools disable NAME   Disable a toolset

hermes skills list          List installed skills
hermes skills search QUERY  Search the skills hub
hermes skills install ID    Install a skill (ID can be a hub identifier OR a direct https://…/SKILL.md URL; pass --name to override when frontmatter has no name)
hermes skills inspect ID    Preview without installing
hermes skills config        Enable/disable skills per platform
hermes skills check         Check for updates
hermes skills update        Update outdated skills
hermes skills uninstall N   Remove a hub skill
hermes skills publish PATH  Publish to registry
hermes skills browse        Browse all available skills
hermes skills tap add REPO  Add a GitHub repo as skill source
```

### MCP Servers

```
hermes mcp serve            Run Hermes as an MCP server
hermes mcp add NAME         Add an MCP server (--url or --command)
hermes mcp remove NAME      Remove an MCP server
hermes mcp list             List configured servers
hermes mcp test NAME        Test connection
hermes mcp configure NAME   Toggle tool selection
```

### Gateway (Messaging Platforms)

```
hermes gateway run          Start gateway foreground
hermes gateway install      Install as background service
hermes gateway start/stop   Control the service
hermes gateway restart      Restart the service
hermes gateway status       Check status
hermes gateway setup        Configure platforms
```

Supported platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI connects via the API Server adapter.

Platform docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

### Sessions

```
hermes sessions list        List recent sessions
hermes sessions browse      Interactive picker
hermes sessions export OUT  Export to JSONL
hermes sessions rename ID T Rename a session
hermes sessions delete ID   Delete a session
hermes sessions prune       Clean up old sessions (--older-than N days)
hermes sessions stats       Session store statistics
```

### Cron Jobs

```
hermes cron list            List jobs (--all for disabled)
hermes cron create SCHED    Create: '30m', 'every 2h', '0 9 * * *'
hermes cron edit ID         Edit schedule, prompt, delivery
hermes cron pause/resume ID Control job state
hermes cron run ID          Trigger on next tick
hermes cron remove ID       Delete a job
hermes cron status          Scheduler status
```

**VPS script-only cron jobs:** if a job only runs a deterministic shell/Python script, make it a `no_agent` script job instead of a prompt like "Execute: python3 ...". Frequent prompt-shaped cron jobs can repeatedly load full LLM context and make Telegram/Discord feel stuck or stale. See `references/vps-cron-no-agent-script-jobs.md`.

### Webhooks

```
hermes webhook subscribe N  Create route at /webhooks/<name>
hermes webhook list         List subscriptions
hermes webhook remove NAME  Remove a subscription
hermes webhook test NAME    Send a test POST
```

### Profiles

```
hermes profile list         List all profiles
hermes profile create NAME  Create (--clone, --clone-all, --clone-from)
hermes profile use NAME     Set sticky default
hermes profile delete NAME  Delete a profile
hermes profile show NAME    Show details
hermes profile alias NAME   Manage wrapper scripts
hermes profile rename A B   Rename a profile
hermes profile export NAME  Export to tar.gz
hermes profile import FILE  Import from archive
```

### Credential Pools

```
hermes auth add             Interactive credential wizard
hermes auth list [PROVIDER] List pooled credentials
hermes auth remove P INDEX  Remove by provider + index
hermes auth reset PROVIDER  Clear exhaustion status
```

### Other

```
hermes insights [--days N]  Usage analytics
hermes update               Update to latest version
hermes pairing list/approve/revoke  DM authorization
hermes plugins list/install/remove  Plugin management
hermes honcho setup/status  Honcho memory integration (requires honcho plugin)
hermes memory setup/status/off  Memory provider config
hermes completion bash|zsh  Shell completions
hermes acp                  ACP server (IDE integration)
hermes claw migrate         Migrate from OpenClaw
hermes uninstall            Uninstall Hermes
```

---

## Slash Commands (In-Session)

Type these during an interactive chat session.

### Session Control
```
/new (/reset)        Fresh session
/clear               Clear screen + new session (CLI)
/retry               Resend last message
/undo                Remove last exchange
/title [name]        Name the session
/compress            Manually compress context
/stop                Kill background processes
/rollback [N]        Restore filesystem checkpoint
/background <prompt> Run prompt in background
/queue <prompt>      Queue for next turn
/resume [name]       Resume a named session
```

### Configuration
```
/config              Show config (CLI)
/model [name]        Show or change model
/personality [name]  Set personality
/reasoning [level]   Set reasoning (none|minimal|low|medium|high|xhigh|show|hide)
/verbose             Cycle: off → new → all → verbose
/voice [on|off|tts]  Voice mode
/yolo                Toggle approval bypass
/skin [name]         Change theme (CLI)
/statusbar           Toggle status bar (CLI)
```

### Tools & Skills
```
/tools               Manage tools (CLI)
/toolsets            List toolsets (CLI)
/skills              Search/install skills (CLI)
/skill <name>        Load a skill into session
/cron                Manage cron jobs (CLI)
/reload-mcp          Reload MCP servers
/plugins             List plugins (CLI)
```

### Gateway
```
/approve             Approve a pending command (gateway)
/deny                Deny a pending command (gateway)
/restart             Restart gateway (gateway)
/sethome             Set current chat as home channel (gateway)
/update              Update Hermes to latest (gateway)
/platforms (/gateway) Show platform connection status (gateway)
```

### Utility
```
/branch (/fork)      Branch the current session
/fast                Toggle priority/fast processing
/browser             Open CDP browser connection
/history             Show conversation history (CLI)
/save                Save conversation to file (CLI)
/paste               Attach clipboard image (CLI)
/image               Attach local image file (CLI)
```

### Info
```
/help                Show commands
/commands [page]     Browse all commands (gateway)
/usage               Token usage
/insights [days]     Usage analytics
/status              Session info (gateway)
/profile             Active profile info
```

### Exit
```
/quit (/exit, /q)    Exit CLI
```

---

## Key Paths & Config

```bash
~/.hermes/config.yaml       Main configuration
~/.hermes/.env              API keys and secrets
$HERMES_HOME/skills/        Installed skills
~/.hermes/sessions/         Session transcripts
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/hermes-agent/     Source code (if git-installed)
```

**Project-specific references**: See `references/vps-smtp-config-money-printer-v2.md` for VPS SMTP configuration details for the money-printer-v2 project.

Profiles use `~/.hermes/profiles/<name>/` with the same layout.

### Config Sections

Edit with `hermes config edit` or `hermes config set section.key value`.

| Section | Key options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |

### Provider Fallback Behavior**: Setting `provider: ''` (empty string) under the `model` section enables Hermes to consult the model catalog and automatically select the first available provider that offers the specified `model.default`. This allows for provider fallback behavior - if the preferred provider (e.g., Gemini/OpenRouter) is unavailable due to quotas or errors, Hermes will automatically try the next provider in the catalog that has the model. Local Ollama models can serve as a final fallback when configured in the catalog.

## VPS Gateway Troubleshooting**: When running Hermes gateway on a remote VPS (e.g., Sovereign Cloud, Hostinger VPS), common issues include:

### Cron Job Optimization (VPS Specific)
11. **Repeated LLM prompt loading from cron jobs** - Cron jobs that execute simple scripts (like scrapers or notification senders) should be configured as `no_agent=true` script jobs instead of prompt-shaped jobs. Repeatedly loading full Hermes/LLM context for trivial script execution can consume VPS resources and make Telegram feel unresponsive.

    **Fix**: Convert script-only cron jobs to use executable wrappers in `/home/hermes/.hermes/scripts/` with `no_agent=true` in their job configuration. See `references/vps-cron-no-agent-script-jobs.md` for the full conversion pattern used for money-printer-v2 and trading bots.

### User & Permission Issues
1. **Hermes user account locked** - Fix with: `usermod -U hermes && passwd hermes` (then set password)
2. **Incorrect file ownership** - Ensure hermes owns its home: `chown -R hermes:hermes /home/hermes/.hermes`
3. **Permission denied on gateway.lock** - Usually fixed by correcting ownership above
4. **Sudo/su failures** - Even when `id hermes` works, `sudo -u hermes` may fail if user is locked or in inconsistent state

### Environment & Startup Issues
5. **Invalid .env characters** - Newlines or special characters in .env break `export` - clean with:
   ```bash
   # Backup first
   cp .hermes/.env .hermes/.env.backup
   # Then recreate with proper format
   cat > .hermes/.env <<EOF
   GOOGLE_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   # ... other vars without trailing spaces or newlines in values
   EOF
   ```
6. **"bash: cd: /home/hermes: No such file or directory"** - Despite directory existing, can occur in su context. Workarounds:
   - Use `HOME=/home/hermes /path/to/hermes gateway run --replace` (avoid cd)
   - Explicitly source env: `cd /home/hermes && set -a && source .hermes/.env && set +a && /path/to/hermes/gateway run --replace`

### Provider & API Issues
7. **Gemini HTTP 500 errors** - Often indicates quota issues or invalid key. Verify with:
   ```bash
   curl https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent?key=[REDACTED] \
     -H 'Content-Type: application/json' \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
   ```
8. **Switch to OpenRouter as more reliable primary** - Edit config.yaml:
   ```yaml
   model:
     provider: openrouter
     default: google/gemma-4-31b-it
   providers:
     openrouter:
       api_key: sk-or-v1-...  # your key
       # ... rest of config
   ```

### Service Management
9. **Prefer a real systemd service instead of SSH-held foreground jobs**. For normal single-user installs, use the built-in installer:
   ```bash
   # As hermes user
   hermes gateway install  # installs systemd user service
   systemctl --user start hermes-gateway
   systemctl --user status hermes-gateway
   ```
   On headless VPS hosts where user-bus/systemd access is unreliable over SSH, a root-managed system service is acceptable:
   ```ini
   # /etc/systemd/system/hermes-gateway.service
   [Service]
   User=hermes
   Group=hermes
   WorkingDirectory=/home/hermes
   EnvironmentFile=/home/hermes/.hermes/.env
   ExecStart=/home/hermes/.hermes/hermes-agent/venv/bin/hermes gateway run --replace
   Restart=always
   RestartSec=5
   ```
   Use a separate `hermes-dashboard.service` if the Web UI should survive reboot. For internet exposure, prefer `hermes dashboard --host 127.0.0.1 --port 8080 --tui` behind nginx Basic Auth instead of binding the dashboard directly to `0.0.0.0 --insecure`; see `references/vps-dashboard-webui-access.md`. Verify with `systemctl is-active hermes-gateway hermes-dashboard nginx` and `ss -tlnp | egrep ':(80|8080)'`.
10. **Stale gateway state** - If gateway connects then quickly exits, check logs for:
    - Permission errors on lock/state files
    - API authentication failures
    - Context/compression issues

For detailed VPS-specific gateway troubleshooting, see `references/vps-gateway-troubleshooting.md`. For internet-exposed dashboard/web workspace setup with nginx Basic Auth, loopback binding, `--tui`, and external verification receipts, see `references/vps-dashboard-webui-access.md`.

**OpenRouter Free Model Usage**: To avoid hitting paid quotas on OpenRouter, use the free variant of models (e.g., `google/gemma-4-31b-it:free`). Configure this in `model.default` and ensure the OpenRouter provider lists the free model in its `models` array. Hermes will then route requests to the free tier, falling back to local Ollama only if the free tier is exhausted or returns an error.

**Avoiding Permission Denied Errors**: When running Hermes as a service or from cron, ensure the working directory is set to a user-owned path (e.g., your project directory) to prevent Hermes from scanning `/root` for git roots, which can cause a `PermissionError: [Errno 13] Permission denied: '/root/.git'`. Use the `--workdir` flag or set `terminal.cwd` in config.yaml to a safe directory.

Full config reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration

See `references/empty-provider-fallback-config.md` for details on configuring empty provider for automatic fallback behavior.
See `references/cron-provider-repair.md` for repairing scheduled jobs that fail with stale/unknown provider aliases like `custom:local` while preserving their prompt, schedule, and delivery settings.
See `references/openrouter-free-model-config.md` for OpenRouter free model configuration and fallback setup.
See `references/mac-dashboard-ios-and-windows-ollama.md` for MacBook dashboard access from iPhone and the guardrail for using the Obsidian-sourced Windows Ollama endpoint before changing Hermes model URLs.
See `references/ollama-provider-cleanup.md` for repairing bad `provider: custom` / `127.0.0.1:11435` Ollama configs while preserving the intended Ollama Launch and Windows Ollama providers.

### Providers

20+ providers supported. Set via `hermes model` or `hermes setup`.

| Provider | Auth | Key env var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` |
| Google Gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Z.AI / GLM | API key | `GLM_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| MiniMax CN | API key | `MINIMAX_CN_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| Alibaba / DashScope | API key | `DASHSCOPE_API_KEY` |
| Xiaomi MiMo | API key | `XIAOMI_API_KEY` |
| Kilo Code | API key | `KILOCODE_API_KEY` |
| AI Gateway (Vercel) | API key | `AI_GATEWAY_API_KEY` |
| OpenCode Zen | API key | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | API key | `OPENCODE_GO_API_KEY` |
| Qwen OAuth | OAuth | `hermes login --provider qwen-oauth` |
| Custom endpoint | Config | `model.base_url` + `model.api_key` in config.yaml |
| GitHub Copilot ACP | External | `COPILOT_CLI_PATH` or Copilot CLI |

Full provider docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

### Storing provider API keys on a VPS
When running Hermes on a remote VPS (e.g., Sovereign Cloud), store provider API keys in `~/.hermes/.env` using the standard environment variable names (e.g., `GOOGLE_API_KEY` for Gemini, `OPENROUTER_API_KEY` for OpenRouter). Then configure the provider in `config.yaml`:
```yaml
model:
  default: models/gemma-4-31b-it   # or your chosen model ID
  provider: gemini
  base_url: https://generativelanguage.googleapis.com/v1beta/openai   # for Gemini
```
Verify the setup with a live probe:
```bash
hermes -z 'OK_GEMINI' -m models/gemma-4-31b-it --provider gemini
```

**User preference**: When configuring providers, provide only essential information with verifiable receipts (command output, API responses) before claiming completion. Avoid optimistic claims. Never print raw API keys, tokens, passwords, or full credential-bearing config values in receipts; show key names/presence or redacted prefixes only.

**Provider Identification**: Distinguish between local-host and bridging providers (e.g., 'Windows Ollama' vs 'Ollama Launch'). Use `ollama launch <integration>` and the interactive picker for bridging provider fixes to ensure the correct model ID and provider alias are linked in `config.yaml`.

### Toolsets

Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.

| Toolset | What it provides |
|---------|-----------------|
| `web` | Web search and content extraction |
| `browser` | Browser automation (Browserbase, Camofox, or local Chromium) |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `vision` | Image analysis |
| `image_gen` | AI image generation |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `messaging` | Cross-platform message sending |
| `search` | Web search only (subset of `web`) |
| `todo` | In-session task planning and tracking |
| `rl` | Reinforcement learning tools (off by default) |
| `moa` | Mixture of Agents (off by default) |
| `homeassistant` | Smart home control (off by default) |

Tool changes take effect on `/reset` (new session). They do NOT apply mid-conversation to preserve prompt caching.

---

## Security & Privacy Toggles

Common "why is Hermes doing X to my output / tool calls / commands?" toggles — and the exact commands to change them. Most of these need a fresh session (`/reset` in chat, or start a new `hermes` invocation) because they're read once at startup.

### Secret redaction in tool output

Secret redaction is **off by default** — tool output (terminal stdout, `read_file`, web content, subagent summaries, etc.) passes through unmodified. If the user wants Hermes to auto-mask strings that look like API keys, tokens, and secrets before they enter the conversation context and logs:

```bash
hermes config set security.redact_secrets true       # enable globally
```

**Restart required.** `security.redact_secrets` is snapshotted at import time — toggling it mid-session (e.g. via `export HERMES_REDACT_SECRETS=true` from a tool call) will NOT take effect for the running process. Tell the user to run `hermes config set security.redact_secrets true` in a terminal, then start a new session. This is deliberate — it prevents an LLM from flipping the toggle on itself mid-task.

Disable again with:
```bash
hermes config set security.redact_secrets false
```

### PII redaction in gateway messages

Separate from secret redaction. When enabled, the gateway hashes user IDs and strips phone numbers from the session context before it reaches the model:

```bash
hermes config set privacy.redact_pii true    # enable
hermes config set privacy.redact_pii false   # disable (default)
```

### Command approval prompts

By default (`approvals.mode: manual`), Hermes prompts the user before running shell commands flagged as destructive (`rm -rf`, `git reset --hard`, etc.). The modes are:

- `manual` — always prompt (default)
- `smart` — use an auxiliary LLM to auto-approve low-risk commands, prompt on high-risk
- `off` — skip all approval prompts (equivalent to `--yolo`)

```bash
hermes config set approvals.mode smart       # recommended middle ground
hermes config set approvals.mode off         # bypass everything (not recommended)
```

Per-invocation bypass without changing config:
- `hermes --yolo …`
- `export HERMES_YOLO_MODE=1`

Note: YOLO / `approvals.mode: off` does NOT turn off secret redaction. They are independent.

### Shell hooks allowlist

Some shell-hook integrations require explicit allowlisting before they fire. Managed via `~/.hermes/shell-hooks-allowlist.json` — prompted interactively the first time a hook wants to run.

### Disabling the web/browser/image-gen tools

To keep the model away from network or media tools entirely, open `hermes tools` and toggle per-platform. Takes effect on next session (`/reset`). See the Tools & Skills section above.

---

## Voice & Transcription

### STT (Voice → Text)

Voice messages from messaging platforms are auto-transcribed.

Provider priority (auto-detected):
1. **Local faster-whisper** — free, no API key: `pip install faster-whisper`
2. **Groq Whisper** — free tier: set `GROQ_API_KEY`
3. **OpenAI Whisper** — paid: set `VOICE_TOOLS_OPENAI_KEY`
4. **Mistral Voxtral** — set `MISTRAL_API_KEY`

Config:
```yaml
stt:
  enabled: true
  provider: local        # local, groq, openai, mistral
  local:
    model: base          # tiny, base, small, medium, large-v3
```

### TTS (Text → Voice)

| Provider | Env var | Free? |
|----------|---------|-------|
| Edge TTS | None | Yes (default) |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid |
| MiniMax | `MINIMAX_API_KEY` | Paid |
| Mistral (Voxtral) | `MISTRAL_API_KEY` | Paid |
| NeuTTS (local) | None (`pip install neutts[all]` + `espeak-ng`) | Free |

Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.

---

## Spawning Additional Hermes Instances

Run additional Hermes processes as fully independent subprocesses — separate sessions, tools, and environments.

### When to Use This vs delegate_task

| | `delegate_task` | Spawning `hermes` process |
|-|-----------------|--------------------------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Tool access | Subset of parent's tools | Full tool access |
| Interactive | No | Yes (PTY mode) |
| Use case | Quick parallel subtasks | Long autonomous missions |

### One-Shot Mode

```
terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)

# Background for long tasks:
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)
```

### Interactive PTY Mode (via tmux)

Hermes uses prompt_toolkit, which requires a real terminal. Use tmux for interactive spawning:

```
# Start
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)

# Wait for startup, then send a message
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)

# Read output
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)

# Send follow-up
terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)

# Exit
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

### Multi-Agent Coordination

```
# Agent A: backend
terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)

# Agent B: frontend
terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)

# Check progress, relay context between them
terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)
terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)
```

### Session Resume

```
# Resume most recent session
terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)

# Resume specific session
terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)
```

### Tips

- **Prefer `delegate_task` for quick subtasks** — less overhead than spawning a full process
- **Use `-w` (worktree mode)** when spawning agents that edit code — prevents git conflicts
- **Set timeouts** for one-shot mode — complex tasks can take 5-10 minutes
- **Use `hermes chat -q` for fire-and-forget** — no PTY needed
- **Use tmux for interactive sessions** — raw PTY mode has `\r` vs `\n` issues with prompt_toolkit
- **For scheduled tasks**, use the `cronjob` tool instead of spawning — handles delivery and retry

---

## ⚙️ OPERATIONAL PLAYBOOK: CRITICAL TROUBLESHOOTING & BEST PRACTICES

This section documents patterns of failure and highly robust workflow sequences discovered during deployment, overriding general documentation. **Follow these steps in order if a standard action fails.**

### 🛑 Troubleshooting Guide: System Failures

#### 1. Gateway Connectivity & Profile Loss (HIGH PRIORITY)
If the gateway connects but frequently displays 'Gateway shutting down/restarting' or fails to process modern commands:
    - **Action 1 (Restart):** Run `hermes gateway restart` (CLI) or `systemctl --user restart hermes-gateway` (Systemd).
    - **Action 2 (Clean State):** If re-starting fails, check the logs for `PermissionError: [Errno 13] Permission denied: '/root/.git'`. This usually means a rogue background process is running as root. Use `sudo -u hermes` (instead of just `hermes`) for all commands to ensure correct user context.
    - **Action 3 (Platform Fix):** For persistent issues (e.g., Telegram model pickers falling back to text instructions), ensure the platform adapter is forcing the use of the latest message metadata (e.g., including `message_thread_id` and `topic` in system calls). *Reference: references/telegram-model-picker-vps.md*

#### 2. VPS Cron Job Optimization: The `no_agent` Mandate
**Rule:** Any scheduled job that performs a *non-LLM-intensive* task (e.g., fetching a weather API, scripting a file backup, checking a simple health endpoint) **MUST NOT** be shaped as a general `Execute: <script>` command.
**Fix:** Use a specialized, pre-wrapped script (e.g., `/home/hermes/.hermes/scripts/script_name.py`) and configure the cron job with `no_agent=true` capability. This bypasses the expensive LLM context loading and runs the payload deterministically, which is mandatory for stable, low-resource cron monitoring (like `bmo-system-health-check`). *Reference: references/vps-cron-no-agent-script-jobs.md*

#### 3. Data Model Conflict: Knowledge Vault Synchronization
The knowledge base is not a dump; it is a structured artifact flow.
- **Rule:** Never process the entire vault blindly. Always run the `knowledge-vault-sync` cron job first, as it determines the authoritative file/code memory pointers for the rest of the system.
- **Preferred Flow:** `Sync Vault` $\rightarrow$ `Update Code Memory` $\rightarrow$ `Execute Logic`.

### 🛠️ Core Best Practices Checklist
- **Initialization:** Always start with `hermes setup` or `/reset` (chat) after major config/toolset changes.
- **Security Confirmation:** Always verify API keys are loaded via `hermes config check` *before* attempting live connections.
- **Performance:** Utilize Worktree Mode (`--worktree` or `-w`) when running agents that frequently modify the codebase to guarantee isolation and rollback safety.

**Detailed Guides:** For detailed walkthroughs, consult the linked references, especially regarding API key sanitization (`references/cleaning-hermes-env-file.md`) and advanced provider catalog management (`references/gemma4-provider-catalog-patching.md`).
---

### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools
### Model/provider issues

1. `hermes doctor` — check config and dependencies
2. `hermes login` — re-authenticate OAuth providers
3. Check `.env` has the right API key
4. If the model name is colloquial or user-invented (e.g. `gemma4`), verify the exact provider model ID before setting it as default. For Google/Gemini Gemma 4, use the models list endpoint and prefer the largest available valid ID such as `gemma-4-31b-it`; see `references/gemini-gemma4-default.md` for the full verification/restart workflow. When adding a newly launched model across multiple providers, update and verify catalog, normalization, provider overlays, and auth registry together; see `references/gemma4-provider-catalog-patching.md`.
5. Before saying providers/models "all respond" or are "fully working," run live response probes for every claimed provider. Catalog/config entries are not enough: a provider can be listed but fail at runtime with stale CLI choices, missing keys, 401 auth, 404 routing, or an unwired adapter. See `references/provider-live-response-verification.md`.
6. When a gateway is alive but Gemini/Gemma returns `HTTP 429`, first distinguish provider failure from stale gateway context: run a tiny direct `hermes chat --provider gemini ... -q` probe, inspect the platform session prompt size, and use timestamp-filtered `journalctl`. If the direct probe succeeds but gateway logs show ~14k prompt tokens and `generate_content_paid_tier_input_token_count`, suspend/reset the stale platform session and add earlier compression guardrails; see `references/gateway-gemini-429-stale-session.md`.
    - **Config YAML Encoding**: If you encounter `expected '<document start>', but found '<block mapping start>'` or `HTTP 400 "No models provided"`, ensure `config.yaml` is saved as UTF-8 without BOM and has consistent 2-space indentation. Use `cat -e` to check for hidden characters.
    - **Remote Ollama Connectivity**: When configuring a remote Ollama instance:
        - Ensure `base_url` is set to the remote IP (e.g., `http://<IP>:11434`) and NOT the `/v1` endpoint.
        - **Windows Host Requirements**: The host must have `OLLAMA_HOST=0.0.0.0` set in System Environment Variables and TCP port `11434` open in the Windows Defender Firewall Inbound Rules.
        - **Verification**: Verify connectivity from the client using `curl http://<IP>:11434/api/tags` before updating config.
    - **Config YAML Encoding**: If you encounter `expected '<document start>', but found '<block mapping start>'` or `HTTP 400 "No models provided"`, ensure `config.yaml` is saved as UTF-8 without BOM and has consistent 2-space indentation. Use `cat -e` to check for hidden characters.
    - **Remote Ollama Connectivity**: When configuring a remote Ollama instance:
        - Ensure `base_url` is set to the remote IP (e.g., `http://<IP>:11434`) and NOT the `/v1` endpoint.
        - **Windows Host Requirements**: The host must have `OLLAMA_HOST=0.0.0.0` set in System Environment Variables and TCP port `11434` open in the Windows Defender Firewall Inbound Rules.
        - **Verification**: Verify connectivity from the client using `curl http://<IP>:11434/api/tags` before updating config.
8. **Gemini API key not found** — If you see `Error: Gemini HTTP 400 (INVALID_ARGUMENT): API Key not found` despite setting `GOOGLE_API_KEY` or `GEMINI_API_KEY` in the environment or config, verify that the Gemini provider plugin is reading the correct variable name. The plugin expects either `GOOGLE_API_KEY` or `GEMINI_API_KEY`. You can explicitly set the key via `hermes config set providers.gemini.api_key <key>` or ensure the `.env` file is being loaded (check with `hermes config env-path`). Also confirm that `model.provider` is set to `gemini` (or empty for catalog lookup) and that `model.default` matches a model offered by Gemini (e.g., `gemini-flash-latest`).

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart` or from shell: `hermes gateway restart`. In CLI: exit and relaunch.
- **Gateway model changes:** After changing `model.default`/`model.provider`, restart the gateway and verify post-restart logs only; stale pre-restart errors remain in `~/.hermes/logs/gateway.log` and can be misleading. See `references/gemini-gemma4-default.md` for an example timestamp-filtered check.
- **Code changes:** Restart the CLI or gateway process

### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `/skill name` or `hermes -s name`

### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Common gateway problems:
- **Telegram `/model` picker falls back to text instructions**: If `/model` asks the user to type full provider/model names instead of showing inline buttons, inspect gateway logs for `send_model_picker failed: Message thread not found`. On VPS gateways this can be stale Telegram topic/thread metadata. Patch/restart the Telegram adapter to retry `send_model_picker` without `message_thread_id`/topic metadata; see `references/telegram-model-picker-vps.md`.
- **Repeated `Gateway shutting down/restarting` messages in Telegram**: First distinguish real crash loops from planned `--replace` takeovers or service restarts. Check `journalctl -u hermes-gateway.service`, `~/.hermes/logs/gateway.log`, `NRestarts`, and kernel OOM logs. If the gateway is otherwise healthy, suppress user-facing lifecycle pings with `platforms.telegram.gateway_restart_notification: false`; see `references/vps-gateway-troubleshooting.md`.
- **Gateway appears stuck while cron jobs are active**: Inspect `hermes cron list` and recent `session_cron_...` files. Script-only jobs shaped as prompts (for example, `Execute: python3 ...`) should be converted to `no_agent=true` with executable wrappers so they do not repeatedly load full LLM prompt/context; see `references/vps-cron-no-agent-script-jobs.md`.
- **Do not misroute platform bugs into DNS work**: A broken Telegram model picker is a gateway/platform issue, not evidence that domain DNS should change. If a production domain already has working Hostinger/Cloudflare routing, only configure VPS/Nginx locally or prepare a subdomain after explicit DNS authorization. For web UI exposure, direct IP + nginx Basic Auth can be complete and verified before DNS; see `references/vps-dashboard-webui-access.md`.
Sovereign Cloud VPS: When restarting the gateway via `systemctl --user` over SSH, you MUST specify `XDG_RUNTIME_DIR=/run/user/<uid>` (e.g., 1001 for `hermes`) to connect to the user bus, otherwise you will get `Failed to connect to bus`.

### Provider Readiness Checklist
Do not equate catalog/config updates with provider readiness. A model can appear in `models.py` but fail at runtime due to missing keys, 401 auth, or 404 routing.
**Verification Standard**: A provider only "responds" if a live probe returns the expected token:
`hermes chat -Q --provider <p> -m <m> -q 'Reply OK_<P>'` $\rightarrow$ `exit 0` and output `OK_<P>`.
See `references/provider-live-response-verification.md` for a full verification ladder.
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`
- **Phantom Network Failures**: If gateway logs show `httpx.ConnectError` or `[Errno 8] nodename nor servname provided` but `curl -v https://api.telegram.org` works from the terminal, the gateway process may have a stale network state. Fix: `pkill -f hermes` followed by a fresh `hermes gateway run` or `hermes gateway restart`.
- **Do not misdiagnose provider errors as DNS**: If Telegram/Discord reached the bot and gateway logs show model API errors (`HTTP 429`, `HTTP 401`, provider names, quota/auth messages), fix provider/model config first. Nameserver or DNS-provider changes are release actions and need explicit user approval.

### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows HTTP 400 "No models provided"**: Config file encoding issue (BOM). Ensure `config.yaml` is saved as UTF-8 without BOM.
- **/steer command not responding**: If the `/steer` slash command appears to do nothing or returns no response in Telegram/Discord gateways:
    1. Verify the gateway service is running: `hermes gateway status`
    2. Check gateway logs for errors: `hermes logs --since 5m` or `journalctl --user -u hermes-gateway --since "5 minutes ago"`
    3. Ensure the agent is updated: `hermes update --yes`
    4. Confirm the steering tool is enabled: `hermes tools list` (look for `steering` or `agent-steering` in the toolsets)
    5. Restart the gateway: `hermes gateway restart`
    6. If using a VPS, verify `XDG_RUNTIME_DIR` is set correctly for systemd user services (see VPS gateway restart references)

### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider <your_provider>
hermes config set auxiliary.vision.model <model_name>
```

---

## Where to Find Things

| Looking for... | Location |
|----------------|----------|
| Config options | `hermes config edit` or [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Available tools | `hermes tools list` or [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) |
| Slash commands | `/help` in session or [Slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands) |
| Skills catalog | `hermes skills browse` or [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `hermes model` or [Providers guide](https://hermes-agent.nousresearch.com/docs/integrations/providers) |
| Platform setup | `hermes gateway setup` or [Messaging docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) |
| MCP servers | `hermes mcp list` or [MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) |
| Profiles | `hermes profile list` or [Profiles docs](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |
| Cron jobs | `hermes cron list` or [Cron docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) |
| Memory | `hermes memory status` or [Memory docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) |
| Env variables | `hermes config env-path` or [Env vars reference](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) |
| CLI commands | `hermes --help` or [CLI reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| Gateway logs | `~/.hermes/logs/gateway.log` |
| Session files | `~/.hermes/sessions/` or `hermes sessions browse` |
| Source code | `~/.hermes/hermes-agent/` |

---

## Contributor Quick Reference

For occasional contributors and PR authors. Full developer docs: https://hermes-agent.nousresearch.com/docs/developer-guide/

### Project Layout

```
hermes-agent/
├── run_agent.py          # AIAgent — core conversation loop
├── model_tools.py        # Tool discovery and dispatch
├── toolsets.py           # Toolset definitions
├── cli.py                # Interactive CLI (HermesCLI)
├── hermes_state.py       # SQLite session store
├── agent/                # Prompt builder, context compression, memory, model routing, credential pooling, skill dispatch
├── hermes_cli/           # CLI subcommands, config, setup, commands
│   ├── commands.py       # Slash command registry (CommandDef)
│   ├── config.py         # DEFAULT_CONFIG, env var definitions
│   └── main.py           # CLI entry point and argparse
├── tools/                # One file per tool
│   └── registry.py       # Central tool registry
├── gateway/              # Messaging gateway
│   └── platforms/        # Platform adapters (telegram, discord, etc.)
├── cron/                 # Job scheduler
├── tests/                # ~3000 pytest tests
└── website/              # Docusaurus docs site
```

Config: `~/.hermes/config.yaml` (settings), `~/.hermes/.env` (API keys).

### Adding a Tool (3 files)

**1. Create `tools/your_tool.py`:**
```python
import json, os
from tools.registry import registry

def check_requirements() -> bool:
    return bool(os.getenv("EXAMPLE_API_KEY"))

def example_tool(param: str, task_id: str = None) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="example_tool",
    toolset="example",
    schema={"name": "example_tool", "description": "...", "parameters": {...}},
    handler=lambda args, **kw: example_tool(
        param=args.get("param", ""), task_id=kw.get("task_id")),
    check_fn=check_requirements,
    requires_env=["EXAMPLE_API_KEY"],
)
```

**2. Add to `toolsets.py`** → `_HERMES_CORE_TOOLS` list.

Auto-discovery: any `tools/*.py` file with a top-level `registry.register()` call is imported automatically — no manual list needed.

All handlers must return JSON strings. Use `get_hermes_home()` for paths, never hardcode `~/.hermes`.

### Adding a Slash Command

1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Add handler in `cli.py` → `process_command()`
3. (Optional) Add gateway handler in `gateway/run.py`

All consumers (help text, autocomplete, Telegram menu, Slack mapping) derive from the central registry automatically.

### Agent Loop (High Level)

```
run_conversation():
  1. Build system prompt
  2. Loop while iterations < max:
     a. Call LLM (OpenAI-format messages + tool schemas)
     b. If tool_calls → dispatch each via handle_function_call() → append results → continue
     c. If text response → return
  3. Context compression triggers automatically near token limit
```

### Testing

```bash
python -m pytest tests/ -o 'addopts=' -q   # Full suite
python -m pytest tests/tools/ -q            # Specific area
```

- Tests auto-redirect `HERMES_HOME` to temp dirs — never touch real `~/.hermes/`
- Run full suite before pushing any change
- Use `-o 'addopts='` to clear any baked-in pytest flags

### Commit Conventions

```
type: concise subject line

Optional body.
```

Types: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`

### Key Rules

- **Never break prompt caching** — don't change context, tools, or system prompt mid-conversation
- **Message role alternation** — never two assistant or two user messages in a row
- Use `get_hermes_home()` from `hermes_constants` for all paths (profile-safe)
- Config values go in `config.yaml`, secrets go in `.env`
- New tools need a `check_fn` so they only appear when requirements are met

### User Preference: Concise, Receipt-Based Verification** - When configuring Hermes providers or discussing technical setup, avoid optimistic claims and verbose explanations. Provide only essential information with verifiable receipts (command output, API responses) before claiming completion. If the user asks a direct question, answer concisely first, then offer to provide details or verification steps if needed.
