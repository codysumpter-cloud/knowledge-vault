#!/usr/bin/env bash
set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p "$HOME/.config"
ENV_FILE="$HOME/.config/knowledge-vault.env"

if [[ ! -f "$ENV_FILE" ]]; then
  cat > "$ENV_FILE" <<'EOF'
VAULT_GITHUB_OWNER=codysumpter-cloud
VAULT_GITHUB_TOKEN=ghp_REPLACE_ME
# Keep false while codysumpter-cloud/knowledge-vault is public.
VAULT_TRACK_PRIVATE=false
EOF
  chmod 600 "$ENV_FILE"
  echo "Created $ENV_FILE. Edit it and add your GitHub token."
fi

PLIST="$HOME/Library/LaunchAgents/dev.prismtek.knowledge-vault-steward.plist"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>dev.prismtek.knowledge-vault-steward</string>
  <key>ProgramArguments</key>
  <array>
    <string>$VAULT_ROOT/99-System/Automation/run-vault-maintenance.sh</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$VAULT_ROOT</string>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>8</integer>
    <key>Minute</key><integer>30</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>$HOME/Library/Logs/knowledge-vault-steward.out.log</string>
  <key>StandardErrorPath</key>
  <string>$HOME/Library/Logs/knowledge-vault-steward.err.log</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST" >/dev/null 2>&1 || true
launchctl load "$PLIST"
echo "Installed daily Vault Steward launch agent: $PLIST"
echo "Next: edit $ENV_FILE and replace ghp_REPLACE_ME with a real token."
