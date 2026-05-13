## MoneyPrinterV2 macOS Setup - Session Notes

### Environment
- **System**: macOS Sequoia 15.7.5
- **Hardware**: Intel MBP 15,2, 8GB RAM
- **User**: codysumpter

### Setup Steps Performed

#### 1. Python Setup
- Installed Python 3.12 via Homebrew: `brew install python@3.12`
- Created virtual environment: `python3.12 -m venv venv`
- Patched `setup_local.sh` to prefer Python 3.12 when available

#### 2. Dependencies
- FFmpeg: `brew install ffmpeg`
- GeckoDriver: `brew install geckodriver` (already installed)
- ImageMagick: `brew install imagemagick`
- Firefox: `brew install --cask firefox`

#### 3. Ollama Setup
- Installed via Homebrew: `brew install ollama`
- Pulled models: `gemma4:31b-cloud`, `tinyllama:latest`, `gemma4:e2b`
- Configured MPV2 to use local models to avoid cloud limits

#### 4. Firefox Profile
Created dedicated Firefox profile for MPV2:
```bash
mkdir -p /Users/codysumpter/Library/Application Support/Firefox/Profiles
/usr/local/bin/firefox -CreateProfile "moneyprinter /Users/codysumpter/Library/Application Support/Firefox/Profiles/moneyprinter"
```
Profile path: `/Users/codysumpter/Library/Application Support/Firefox/Profiles/moneyprinter`

#### 5. Configuration
- Updated `config.json` with:
  - Firefox profile path
  - ImageMagick path: `/usr/local/bin/magick`
  - Ollama model: `tinyllama:latest`
  - Gemini API key for image generation
- Added environment variable loading via `~/.config/moneyprinterv2/env`
- Patched `config.py` and `preflight_local.py` to load local env file

#### 6. Dependency Pinning (Critical Fixes)
Updated `requirements.txt` to avoid compatibility issues:
```diff
- selenium
+ selenium<4.11
- moviepy
+ moviepy<2
+ numpy<2
```

#### 7. Code Changes Committed
- `requirements.txt`: Pinned selenium, moviepy, numpy
- `scripts/setup_local.sh`: Python 3.12 preference
- `scripts/preflight_local.py`: Added env loading
- `src/config.py`: Added env loading

#### 8. API Key Management
- Stored Gemini API key in `~/.config/moneyprinterv2/env` with chmod 600
- Key: `AIzaSyB3xJs2n-rY512OkNHfQ_9J2s245puGRe8`

### Current Status
- MPV2 preflight passes
- App runs and shows menu
- YouTube account configured with profile path
- Image generation API key set
- Waiting for user to proceed with content creation

### Issues Encountered & Solutions
1. **Ollama weekly limit reached** → Switched to local models
2. **Selenium compatibility** → Pinned to <4.11
3. **MoviePy/NumPy compatibility** → Pinned both <2
4. **Invalid Firefox profile path** → Updated from config to correct path
5. **Hugging Face warnings** → Need to set HF_TOKEN for faster downloads

### Next Steps for User
1. Continue with YouTube Shorts automation
2. Consider setting up Hugging Face token for TTS
3. Set up cron jobs for automation
4. Configure Twitter bot
5. Integrate affiliate marketing
