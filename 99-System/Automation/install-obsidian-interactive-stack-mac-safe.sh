#!/usr/bin/env bash
set -euo pipefail

# Mac-safe one-shot installer for the Obsidian interactive plugin stack.
# No watchers. No npm. No builds. No model downloads. No indexing.

VAULT_ROOT="$(pwd)"
LOCK="$VAULT_ROOT/.vault-steward-obsidian-install.lock"
LOCK_DIR="$VAULT_ROOT/.vault-steward-obsidian-install.lockdir"
LOG_DIR="$VAULT_ROOT/99-System/Logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/obsidian-interactive-stack-install.log"

stamp() { date '+%Y-%m-%dT%H:%M:%S%z'; }

# macOS does not ship flock by default. Prefer flock when present, otherwise
# use an atomic mkdir lock. This remains non-overlapping and one-shot.
if command -v flock >/dev/null 2>&1; then
  exec 9>"$LOCK"
  if ! flock -n 9 2>/dev/null; then
    echo "$(stamp) another installer run is active; exiting" | tee -a "$LOG"
    exit 0
  fi
else
  if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    echo "$(stamp) another installer run is active; exiting" | tee -a "$LOG"
    exit 0
  fi
  trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT
fi

echo "$(stamp) starting obsidian interactive stack install" | tee -a "$LOG"

# Skip on battery.
if command -v pmset >/dev/null 2>&1; then
  if pmset -g batt | grep -qi "Battery Power"; then
    echo "$(stamp) on battery power; skipping" | tee -a "$LOG"
    exit 0
  fi
fi

# Skip when system load is high. Conservative threshold for not annoying Prismtek.
LOAD="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}' | tr -d '{}')"
if [[ -n "${LOAD:-}" ]]; then
  if ! python3 - "$LOAD" <<'PY'
import sys
load = float(sys.argv[1])
if load > 4.0:
    raise SystemExit(1)
PY
  then
    echo "$(stamp) load too high ($LOAD); skipping" | tee -a "$LOG"
    exit 0
  fi
fi

# Skip under serious thermal pressure where available.
if command -v pmset >/dev/null 2>&1; then
  THERMAL="$(pmset -g therm 2>/dev/null || true)"
  if echo "$THERMAL" | grep -Eqi "CPU_Speed_Limit.*[5-9][0-9]|Scheduler_Limit.*[5-9][0-9]"; then
    echo "$(stamp) thermal pressure detected; skipping" | tee -a "$LOG"
    exit 0
  fi
fi

if [[ ! -f "99-System/Obsidian/obsidian-interactive-stack.manifest.json" ]]; then
  echo "$(stamp) missing stack manifest; run from KnowledgeVault root" | tee -a "$LOG"
  exit 1
fi

mkdir -p "99-System/Backups"
BACKUP="99-System/Backups/obsidian-config-before-interactive-stack-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP"
cp -R .obsidian "$BACKUP/.obsidian.backup"

# Low priority, one-shot download/install of release assets only.
nice -n 19 python3 "99-System/Automation/install_obsidian_plugins_from_manifest.py" 2>&1 | tee -a "$LOG"

echo "$(stamp) complete" | tee -a "$LOG"
