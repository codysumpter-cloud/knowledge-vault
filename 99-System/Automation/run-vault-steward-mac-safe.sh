#!/usr/bin/env bash
set -euo pipefail

# Mac-safe KnowledgeVault steward runner.
# Conservative by design: no watchers, no repo clones, no heavy indexing.

VAULT_ROOT="${VAULT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
LOCK_DIR="${TMPDIR:-/tmp}/knowledge-vault-steward.lock"
LOG_DIR="$VAULT_ROOT/99-System/Agents/Vault Steward/Logs"
TODAY="$(date +%F)"
LOG_FILE="$LOG_DIR/${TODAY}-mac-safe-run.log"

mkdir -p "$LOG_DIR"

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "Vault Steward already running; exiting." | tee -a "$LOG_FILE"
  exit 0
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT

cd "$VAULT_ROOT"

if [[ ! -f "AGENTS.md" || ! -d ".obsidian" ]]; then
  echo "Refusing to run: not at expected KnowledgeVault root: $VAULT_ROOT" | tee -a "$LOG_FILE"
  exit 1
fi

if command -v pmset >/dev/null 2>&1; then
  PMSET_OUT="$(pmset -g batt || true)"
  if echo "$PMSET_OUT" | grep -q "Battery Power"; then
    BATTERY_PCT="$(echo "$PMSET_OUT" | grep -Eo '[0-9]+%' | head -1 | tr -d '%' || echo 100)"
    if [[ "${BATTERY_PCT:-100}" -lt 35 ]]; then
      echo "Skipping: battery ${BATTERY_PCT}% on battery power." | tee -a "$LOG_FILE"
      exit 0
    fi
  fi
fi

if command -v pmset >/dev/null 2>&1; then
  THERMAL="$(pmset -g therm 2>/dev/null || true)"
  if echo "$THERMAL" | grep -Eqi 'thermal pressure.*(warning|critical|serious|high)'; then
    echo "Skipping: thermal pressure is elevated." | tee -a "$LOG_FILE"
    exit 0
  fi
fi

LOAD_1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}' || echo 0)"
set +e
python3 - <<'PYLOAD'
import os
load_value = float(os.environ.get('LOAD_1', '0') or '0')
raise SystemExit(0 if load_value <= 6.0 else 42)
PYLOAD
LOAD_OK=$?
set -e
if [[ "$LOAD_OK" -eq 42 ]]; then
  echo "Skipping: current load average is high: $LOAD_1" | tee -a "$LOG_FILE"
  exit 0
fi

{
  echo "[$(date -Is)] Starting Mac-safe vault maintenance."
  echo "Vault root: $VAULT_ROOT"
  echo "Git state:"
  git status --short --branch || true
} >> "$LOG_FILE"

if [[ -f "99-System/Automation/vault_maintainer.py" ]]; then
  nice -n 19 python3 "99-System/Automation/vault_maintainer.py" >> "$LOG_FILE" 2>&1 || {
    echo "Maintainer exited with failure; see $LOG_FILE" | tee -a "$LOG_FILE"
    exit 1
  }
else
  echo "No vault_maintainer.py found; inspection only." >> "$LOG_FILE"
fi

{
  echo "Git state after run:"
  git status --short --branch || true
  echo "[$(date -Is)] Finished Mac-safe vault maintenance."
} >> "$LOG_FILE"

echo "Mac-safe vault maintenance complete. Log: $LOG_FILE"
