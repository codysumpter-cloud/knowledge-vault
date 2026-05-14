# Cleaning Hermes .env File for VPS Deployments

## Security Notice
This document previously contained real-looking credentials in the example `.env` block. Treat every exposed value as compromised. Revoke and rotate the provider-side credentials before redeploying.

Do not commit real `.env` values to this public repository. Use placeholders in documentation and store live secrets only in your VPS environment, a local untracked `.env`, or a secret manager.

## Problem
When running Hermes gateway on a VPS, particularly Hostinger VPS with Ubuntu 24.04, the `.hermes/.env` file can accumulate invalid characters that break environment variable loading when using `su - hermes -c` or similar context switches.

## Symptoms
- `bash: export: 'la...': not a valid identifier` when trying to start gateway
- Environment variables not being loaded despite being present in `.env`
- Gateway starts but quickly exits with authentication errors
- Works when manually sourcing but fails in automated contexts

## Root Cause
The `.env` file contained:
1. Trailing spaces after values
2. Newlines inserted in the middle of values, particularly in provider token fields
3. Inconsistent formatting that broke shell parsing

## Solution Procedure

### 1. Backup Current File
```bash
cp ~/.hermes/.env ~/.hermes/.env.backup.$(date +%s)
```

### 2. View Current Content with Special Characters
```bash
cat -A ~/.hermes/.env
```
This shows:
- `$` at end of each line, which is a normal line ending
- `^M` for Windows-style carriage returns, if present
- Visible spaces and newlines within values

### 3. Create Clean Version
Replace each placeholder with a freshly rotated secret from the corresponding provider. Keep exactly one `KEY=value` pair per line.

```bash
cat > ~/.hermes/.env <<'EOF'
GOOGLE_API_KEY=<set-on-server-only>
GEMINI_API_KEY=<set-on-server-only>
NVIDIA_API_KEY=REDACTED_NVAPI_KEY
HF_TOKEN=<set-on-server-only>
HUGGINGFACE_API_KEY=<set-on-server-only>
OLLAMA_API_KEY=<set-on-server-only>
OLLAMA_CLOUD_API_KEY=<set-on-server-only>
OPENROUTER_API_KEY=<set-on-server-only>
GITHUB_TOKEN=<set-on-server-only>
TELEGRAM_BOT_TOKEN=<set-on-server-only>
GATEWAY_ALLOW_ALL_USERS=true
EOF
```

Lock down the file after writing it:

```bash
chmod 600 ~/.hermes/.env
```

### 4. Verify Format
```bash
cat -A ~/.hermes/.env
# Should show clean lines ending with $, no internal special characters
```

Avoid printing full secrets during verification. Check only whether variables are present.

### 5. Test Loading
```bash
su - hermes -c 'cd /home/hermes && set -a && source .hermes/.env && set +a && test -n "$GOOGLE_API_KEY" && echo "GOOGLE_API_KEY loaded"'
```

## Prevention
1. Keep `.env` out of git with `.gitignore`.
2. Commit only `.env.example` files with placeholder values.
3. Always use `cat > file <<'EOF'` to recreate `.env`, which avoids interactive editors inserting characters.
4. Never edit `.env` with GUI editors that might add formatting.
5. When updating via script, use:
   ```bash
   # To set or update a single variable
   KEY="GOOGLE_API_KEY"
   VALUE="<set-on-server-only>"
   grep -q "^${KEY}=" ~/.hermes/.env && sed -i "s/^${KEY}=.*/${KEY}=${VALUE}/" ~/.hermes/.env || echo "${KEY}=${VALUE}" >> ~/.hermes/.env
   ```

## Verification
After cleaning, the gateway should start successfully with:
```bash
su - hermes -c 'cd /home/hermes && set -a && source .hermes/.env && set +a && .hermes/hermes-agent/venv/bin/hermes gateway run --replace'
```

Or using the `HOME` workaround:
```bash
HOME=/home/hermes /home/hermes/.hermes/hermes-agent/venv/bin/hermes gateway run --replace
```

## Required Secret Rotation Checklist
Rotate or revoke any real credentials that were previously committed, including provider API keys, access tokens, bot tokens, and repository tokens. After rotation, update the live VPS `.env` directly and do not paste the new values into this repository.
