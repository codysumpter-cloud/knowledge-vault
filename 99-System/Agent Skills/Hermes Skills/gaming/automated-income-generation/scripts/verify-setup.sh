#!/bin/bash
# MPV2 Setup Verification Script
# Run this to check if MoneyPrinterV2 is properly configured

set -euo pipefail

echo "=== MoneyPrinterV2 Setup Verification ==="
echo

# Check Python
echo "Checking Python..."
if command -v python3.12 &>/dev/null; then
    echo "✓ Python 3.12 available"
    python3.12 --version
else
    echo "⚠ No Python 3.12 found"
fi

# Check virtual environment
if [ -x "venv/bin/python" ]; then
    echo "✓ Virtual environment exists"
    venv/bin/python --version
else
    echo "⚠ No virtual environment found"
fi

# Check dependencies
echo
echo "Checking dependencies..."
deps=(ffmpeg geckodriver magick firefox)
for dep in "${deps[@]}"; do
    if command -v "$dep" &>/dev/null; then
        echo "✓ $dep available"
    else
        echo "⚠ $dep not found"
    fi
done

# Check Ollama
echo
echo "Checking Ollama..."
if command -v ollama &>/dev/null; then
    echo "✓ Ollama installed"
    ollama version
    if curl -sS http://127.0.0.1:11434/api/tags | grep -q '"models"'; then
        echo "✓ Ollama server reachable"
    else
        echo "⚠ Ollama server not reachable"
    fi
else
    echo "⚠ Ollama not installed"
fi

# Check Firefox profile
echo
echo "Checking Firefox profile..."
PROFILE_PATH="/Users/codysumpter/Library/Application Support/Firefox/Profiles/moneyprinter"
if [ -d "$PROFILE_PATH" ]; then
    echo "✓ Firefox profile exists"
else
    echo "⚠ Firefox profile not found"
    echo "  Create it with: firefox -CreateProfile \"moneyprinter $PROFILE_PATH\""
fi

# Check config
echo
echo "Checking config.json..."
if [ -f "config.json" ]; then
    echo "✓ config.json exists"
    python3 -c "
import json, os
with open('config.json') as f:
    cfg = json.load(f)
print('  Firefox profile:', cfg.get('firefox_profile', 'NOT SET'))
print('  Ollama model:', cfg.get('ollama_model', 'NOT SET'))
print('  Gemini API key:', 'SET' if cfg.get('nanobanana2_api_key') else 'NOT SET')
"
else
    echo "⚠ config.json not found"
fi

# Check environment file
echo
echo "Checking local env file..."
ENV_PATH="$HOME/.config/moneyprinterv2/env"
if [ -f "$ENV_PATH" ]; then
    echo "✓ Local env file exists"
    ls -l "$ENV_PATH"
else
    echo "⚠ Local env file not found"
fi

# Check preflight
echo
echo "Running preflight check..."
source venv/bin/activate 2>/dev/null || true
python3 scripts/preflight_local.py 2>&1 | grep -E "^(\\[OK\\]|\\[FAIL\\]|Preflight)"

echo
echo "=== Verification Complete ==="
