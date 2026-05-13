# Cleaning Hermes .env File for VPS Deployments

## Problem
When running Hermes gateway on a VPS (particularly Hostinger VPS with Ubuntu 24.04), the `.hermes/.env` file can accumulate invalid characters that break environment variable loading when using `su - hermes -c` or similar context switches.

## Symptoms
- `bash: export: 'la...': not a valid identifier` when trying to start gateway
- Environment variables not being loaded despite being present in .env
- Gateway starts but quickly exits with authentication errors
- Works when manually sourcing but fails in automated contexts

## Root Cause
The .env file contained:
1. Trailing spaces after values
2. Newlines inserted in the middle of values (particularly in HF_TOKEN and HUGGINGFACE_API_KEY)
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
- `$` at end of each line (normal line ending)
- `^M` for Windows-style carriage returns (if present)
- Visible spaces and newlines within values

### 3. Create Clean Version
```bash
cat > ~/.hermes/.env <<'EOF'
GOOGLE_API_KEY=AIzaSyB3xJs2n-rY512OkNHfQ_9J2s245puGRe8
GEMINI_API_KEY=AIzaSyB3xJs2n-rY512OkNHfQ_9J2s245puGRe8
NVIDIA_API_KEY=REDACTED_NVAPI_KEY
HF_TOKEN=hf_EXvmkcRdzYFLFeFrCUzvaRpKB
HUGGINGFACE_API_KEY=hf_EXvmkcRdzYFLFeFrCUzvaRpKB
OLLAMA_API_KEY=64bcd6c8a2da4de890bfa2c535a9ca39.9w5jUgBOAreEPtUabA7uKYDb
OLLAMA_CLOUD_API_KEY=64bcd6c8a2da4de890bfa2c535a9ca39.9w5jUgBOAreEPtUabA7uKYDb
OPENROUTER_API_KEY=sk-[REDACTED]
GITHUB_TOKEN=ghp_[REDACTED]
TELEGRAM_BOT_TOKEN=8650547852:AAHPcMsoKhKKCCbusWVtZGCL9BbQptSCr10
GATEWAY_ALLOW_ALL_USERS=true
EOF
```

### 4. Verify Format
```bash
cat -A ~/.hermes/.env
# Should show clean lines ending with $, no internal special characters
```

### 5. Test Loading
```bash
su - hermes -c "cd /home/hermes && set -a && source .hermes/.env && set +a && echo \"GOOGLE_API_KEY loaded: ${GOOGLE_API_KEY:0:10}...\""
```

## Prevention
1. Always use `cat > file <<'EOF'` to recreate .env (avoids interactive editors inserting characters)
2. Never edit .env with GUI editors that might add formatting
3. When updating via script, use:
   ```bash
   # To set or update a single variable
   KEY="GOOGLE_API_KEY"
   VALUE="new_key_here"
   grep -q "^${KEY}=" ~/.hermes/.env && sed -i "s/^${KEY}=.*/${KEY}=${VALUE}/" ~/.hermes/.env || echo "${KEY}=${VALUE}" >> ~/.hermes/.env
   ```

## Verification
After cleaning, the gateway should start successfully with:
```bash
su - hermes -c "cd /home/hermes && set -a && source .hermes/.env && set +a && .hermes/hermes-agent/venv/bin/hermes gateway run --replace"
```

Or using the HOME workaround:
```bash
HOME=/home/hermes /home/hermes/.hermes/hermes-agent/venv/bin/hermes gateway run --replace
```
