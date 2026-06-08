#!/usr/bin/env bash
set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$VAULT_ROOT"

ENV_FILE="$HOME/.config/knowledge-vault.env"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

export VAULT_GITHUB_OWNER="${VAULT_GITHUB_OWNER:-codysumpter-cloud}"
export VAULT_TRACK_PRIVATE="${VAULT_TRACK_PRIVATE:-false}"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git pull --rebase --autostash || true
fi

python3 "99-System/Automation/vault_maintainer.py"
python3 "99-System/Automation/generate_vault_dashboards.py"
python3 "99-System/Automation/vault_doctor.py"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git add \
    "AGENTS.md" \
    "README.md" \
    "SYSTEMMAP.md" \
    "RUNBOOK.md" \
    "BACKLOG.md" \
    "SECURITY.md" \
    ".github/workflows" \
    "01-Dashboard" \
    "30 - Projects/GitHub" \
    "99-System/Agents" \
    "99-System/Automation" \
    "99-System/Agent Skills" \
    "99-System/Repositories" \
    ".gitignore"

  if ! git diff --cached --quiet; then
    git commit -m "vault: daily steward maintenance"
    git push || true
  else
    echo "No tracked vault maintenance changes to commit."
  fi
fi
