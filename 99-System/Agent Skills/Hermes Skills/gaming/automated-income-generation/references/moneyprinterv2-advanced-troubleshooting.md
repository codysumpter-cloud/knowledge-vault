# Advanced Troubleshooting for MoneyPrinterV2

## Issues Encountered During Setup on macOS

### 1. Python Version Compatibility
**Issue**: MPV2 requires Python 3.12, but Homebrew's default Python may be newer (3.14+).
**Solution**: Install Python 3.12 explicitly and create virtual environment with it.
```bash
brew install python@3.12
python3.12 -m venv venv
```

### 2. MoviePy and NumPy Compatibility
**Issue**: MPV2 uses older compiled modules that are incompatible with NumPy 2.x, causing crashes.
**Solution**: Pin moviepy and numpy versions in requirements.txt:
```txt
moviepy<2
numpy<2
```

### 3. Selenium Compatibility
**Issue**: Newer Selenium versions removed `firefox_binary` support, breaking Firefox automation.
**Solution**: Pin selenium version to <4.11:
```txt
selenium<4.11
```

### 4. Firefox Profile Path Issues
**Issue**: When creating a Firefox profile via `firefox -CreateProfile`, the directory name is randomized. Using the wrong path causes Selenium to fail.
**Solution**: Check `~/.config/firefox/profiles.ini` to find the actual profile path. Update `config.json` with the full path to the profile directory.

### 5. Ollama Cloud Model Limits
**Issue**: Cloud-hosted models like `gemma4:31b-cloud` have weekly usage limits that can be reached quickly.
**Solution**: Switch to local models:
- `tinyllama:latest` (1B parameters) - fastest, lower quality
- `gemma4:e2b` (5.1B parameters) - good balance of speed/quality
Update `config.json`:
```json
"ollama_model": "tinyllama:latest"
```

### 6. Hugging Face Warning in TTS
**Issue**: KittenTTS downloads models from Hugging Face without authentication, causing warnings and potential slowdowns.
**Solution**:
- Set HF_TOKEN environment variable with a Hugging Face token
- OR switch to a different TTS provider (AssemblyAI or local Whisper)
- OR disable TTS (not recommended)

### 7. Headless Mode Requirement
**Issue**: MPV2's Firefox automation requires headless mode to work reliably on macOS/Linux.
**Solution**: Set `headless: true` in `config.json`.

### 8. API Key Security
**Issue**: Storing API keys in plaintext in config.json is insecure.
**Solution**: Store keys in a secure location like `~/.config/moneyprinterv2/env` with proper permissions:
```bash
mkdir -p ~/.config/moneyprinterv2
chmod 700 ~/.config/moneyprinterv2
echo "GEMINI_API_KEY=your_key_here" > ~/.config/moneyprinterv2/env
chmod 600 ~/.config/moneyprinterv2/env
```
Then load them in `config.py` or `preflight_local.py`:
```python
env_path = os.path.expanduser(\"~/.config/moneyprinterv2/env\")
if os.path.exists(env_path):
    with open(env_path, \"r\", encoding=\"utf-8\") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith(\"#\") or \"=\" not in line:
                continue
            key, value = line.split(\"=\", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('\"').strip(\"'\"\))
```

### 9. Long Generation Times
**Issue**: Using larger local models (like gemma4:e2b) can take several minutes to generate content.
**Solution**:
- Use smaller models (tinyllama) for faster generation
- Optimize prompts to be more concise
- Consider using cloud models with sufficient usage limits

### 10. App Hanging After HF Warning
**Issue**: The app may hang after displaying the Hugging Face warning, possibly due to TTS model download issues.
**Solution**:
- Ensure stable internet connection
- Configure local TTS provider
- Check logs for errors
- Consider disabling TTS temporarily to test other components

## Summary of Key Fixes Applied
1. Updated `requirements.txt` to pin moviepy<2, numpy<2, selenium<4.11
2. Modified `setup_local.sh` to prefer python3.12
3. Updated `config.py` and `preflight_local.py` to load local env file
4. Created secure API key storage with proper permissions
5. Switched to local Ollama models to avoid usage limits
6. Set headless mode to true for Firefox automation
7. Created proper Firefox profile with correct path

## Verification Steps
1. Run preflight check: `python scripts/preflight_local.py`
2. Start the app: `python src/main.py`
3. Test each component individually before full automation
4. Monitor logs for any errors

## Additional Resources
- [MoneyPrinterV2 GitHub](https://github.com/FujiwaraChoki/MoneyPrinterV2)
- [Ollama Documentation](https://ollama.com/)
- [Firefox Profile Management](https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles)
