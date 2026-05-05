# Operator Runbook

## While user is driving

Do not ask the user to approve commands, inspect screens, or interact with the laptop while driving.

Allowed while user is driving:

- build/read knowledge base
- draft plans
- prepare commands for later
- inspect source docs
- create checklists

Not allowed while user is driving:

- ask for manual clicks
- request approval for shell scripts
- start game automation
- make irreversible filesystem/game changes

## No-mod mode command policy

Default safe loop:

```bash
worldboxctl focus
worldboxctl ready <step-label>
# inspect screenshot
# if clean, execute one action
worldboxctl ready <verify-label>
# inspect result
```

Avoid:

```bash
worldboxctl clear-ui 5
```

Use only modal-aware clearing:

```bash
worldboxctl safe-clear --esc 1 --label close-info-panel
```

If any modal appears:

```bash
worldboxctl modal-stop "Quit/settings/confirmation prompt visible"
```

Then stop and ask user to clear manually later.

## Command approval policy

Do not ask approval for one giant command that:

- unzips files
- installs packages
- links global CLIs
- edits config with Python
- starts services

Split it into phases:

1. inspect zip path
2. unzip to a clean directory
3. list files
4. run local help commands
5. link CLIs
6. run doctor/smoke tests
7. update config using CLI or manual JSON edit
8. start services

## Safer install commands

Prefer:

```bash
mkdir -p ~/worldbox-agent-bridge-v4
unzip -q /path/to/worldbox-agent-bridge-v4.zip -d ~/worldbox-agent-bridge-v4
find ~/worldbox-agent-bridge-v4 -maxdepth 3 -type f -name package.json -print
```

Then link without repeated `npm install` if no dependencies are required:

```bash
cd ~/worldbox-agent-bridge-v4/worldbox-agent-bridge-v4
npm link ./apps/worldboxctl
npm link ./apps/worldboxmod
npm link ./apps/agentcraft-worldbox
npm link ./apps/worldbox-ai-director
```

If `npm install` is necessary, get explicit approval and explain it may execute lifecycle scripts.

## Good first runtime test

```bash
worldboxctl doctor
worldboxctl help
worldboxmod help
agentcraft-worldbox start --port 4777
```

In a second shell:

```bash
worldboxctl emit mission_start --summary "WorldBox Hermes dry run" --risk low --print
```
