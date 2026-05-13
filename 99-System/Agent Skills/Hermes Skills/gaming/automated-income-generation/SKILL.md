---
name: Automated Income Generation
trigger: money_printer, income_automation, youtube_automation, affiliate_marketing, content_automation
summary: Setting up and running automated systems for generating online income through content creation, social media, and affiliate marketing.
description: This skill covers the setup, configuration, and operation of automated income generation systems, with a focus on the MoneyPrinterV2 (MPV2) framework. MPV2 automates content creation (YouTube Shorts), social media posting (Twitter), affiliate marketing, and outreach to generate online income.
tags: automation, youtube, twitter, affiliate, income
---
# Automated Income Generation

## Overview

This skill covers the setup, configuration, and operation of automated income generation systems, with a focus on the MoneyPrinterV2 (MPV2) framework. MPV2 automates content creation (YouTube Shorts), social media posting (Twitter), affiliate marketing, and outreach to generate online income.

Key components:
- YouTube automation: video generation, uploading, and monetization
- Twitter automation: content posting and engagement
- Affiliate marketing integration (Amazon Associates, etc.)
- Profit tracking and reinvestment
- Integration with stock trading platforms for profit allocation

## Prerequisites

### System Requirements
- Python 3.12+ (MPV2 requirement)
- Ollama (local LLM server for TTS and content generation)
- FFmpeg (video/audio processing)
- Firefox with geckodriver (browser automation)
- Sufficient disk space for media assets and cache

### Accounts Needed
- YouTube account (with channel)
- Twitter/X account
- Affiliate network accounts (Amazon Associates, etc.)
- Stock trading platform account (Alpaca, TD Ameritrade, etc. - optional)

## Setup Process

### 1. Clone and Install MPV2
```bash
git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git
cd MoneyPrinterV2
cp config.example.json config.json
python -m venv venv
source venv/bin/activate  # Linux/Mac
# Or: .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Install System Dependencies
```bash
# macOS (using Homebrew)
brew install ffmpeg geckodriver

# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg geckodriver
```

### 3. Set Up Ollama (Local LLM)
```bash
# macOS
brew install ollama

# Ubuntu/Debian
curl -fsSL https://ollama.com/install.sh | bash

# Pull a model (e.g., Llama 3.2)
ollama pull llama3.2:3b
# Or for better quality: llama3.2:8b
```

### 4. Configure MPV2
Edit `config.json` with your API keys and account details:
- YouTube API credentials
- Twitter API keys
- Affiliate network links
- Ollama model selection
- Firefox profile paths

### 5. Create Firefox Profiles
Create separate Firefox profiles for each account to avoid bans:
```bash
firefox -ProfileManager
```
Create profiles for YouTube, Twitter, etc., and note their paths in config.json.

## Running the System

### Interactive Mode
```bash
source venv/bin/activate
python src/main.py
```
Follow the menu to:
- Create/manage YouTube accounts
- Generate and upload videos
- Set up Twitter bots
- Manage affiliate products
- Configure CRON jobs for automation

### Automated Scripts
Use pre-built scripts for specific tasks:
```bash
bash scripts/upload_video.sh  # Direct upload flow
```

## CRON Automation

Set up automated posting schedules:

**YouTube Upload Schedule**
```bash
# Edit src/cron.py to set upload frequency
# Then set up cron job:
crontab -e
# Example: Upload once daily at 10 AM
0 10 * * * cd /path/to/MoneyPrinterV2 && source venv/bin/activate && python src/cron.py youtube <account_id> <model_name>
```

**Twitter Posting Schedule**
Similar setup in cron.py for Twitter accounts.

## Profit Tracking and Reinvestment

### Tracking Earnings
MPV2 does not directly track earnings from YouTube or affiliate networks. You need to:
1. Manually record earnings from each platform
2. Or integrate with platform APIs (YouTube Analytics, Amazon Associates API)
3. Store earnings data in a simple database or spreadsheet

### Stock Trading Integration
To reinvest profits into stock trading:
1. Choose a trading API (Alpaca, TD Ameritrade, etc.)
2. Add API credentials to config.json
3. Create a script that:
   - Checks earnings balance
   - Calculates reinvestment amount
   - Places trades based on predefined strategy
   - Logs transactions

Example integration points:
- Use `alpaca-trade-api` Python library
- Schedule daily/weekly profit allocation

## Common Pitfalls and Troubleshooting

### Shell/Subshell Issues
   - **Problem**: Pasting a block of commands into the terminal can leave you in a `bash` subshell instead of your usual `zsh` (or other) shell, leading to confusion and the warning about updating to zsh. This happened when attempting to run setup commands for MoneyPrinterV2.
   - **Solution**:
        - Type `exit` to leave the subshell and return to your parent shell.
        - To permanently use zsh (recommended on macOS), run `chsh -s /bin/zsh` and restart the terminal.
        - Always verify your shell with `echo $SHELL` before proceeding with setup.
        - **User preference**: When setting up development environments, prefer direct execution in the native shell (zsh on macOS) rather than pasting multi-command blocks that can create subshells.

### Dependency Installation Issues
- **Python on macOS**: MPV2 requires Python 3.12. If Homebrew `python3` is newer (e.g. 3.14), install and use `python3.12` explicitly:
  ```bash
  brew install python@3.12
  python3.12 -m venv venv
  ```
- **kittentts installation**: Download the wheel manually and install:
  ```bash
  wget https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl
  pip install kittentts-0.8.1-py3-none-any.whl
  ```
- **MoviePy compatibility**: MPV2 imports `moviepy.editor`, so pin `moviepy<2`. On Intel macOS, also pin `numpy<2` to avoid Torch/ctranslate2 NumPy 2 warnings.
- **Selenium compatibility**: `selenium_firefox` imports `selenium.webdriver.firefox.firefox_binary`, which is missing in newer Selenium. Pin `selenium<4.11`.
- **Ollama model not found**: Pull or configure a model first. On this user setup, `gemma4:31b-cloud` is available via Ollama cloud; local fallback models may be smaller.
- **FFmpeg not found**: Ensure it's installed and in PATH.
- **Songs download failure**: Upstream default song URLs may be empty/unavailable. Create `Songs/` and add at least one `.mp3`/`.wav` file; for a smoke-safe placeholder:
  ```bash
  mkdir -p Songs
  ffmpeg -y -f lavfi -i "sine=frequency=220:duration=90" -filter:a "volume=0.04" -ar 44100 -ac 2 Songs/default_background.wav
  ```

### Browser Automation Issues
- **Firefox profile errors**: Create dedicated profiles for each account
- **Gecko driver version mismatch**: Use webdriver-manager to auto-manage
- **Anti-bot detection**: Use residential proxies if needed (not built-in)

### Content Quality Issues\n- TTS voices may sound robotic; experiment with different models\n- Video generation may produce inconsistent results; adjust prompts and settings\n- YouTube may flag automated content; ensure compliance with community guidelines\n\n### YouTube Title Generation Infinite Loop\n- **Problem**: The `generate_metadata` function in `src/classes/YouTube.py` can enter an infinite recursion loop when the LLM generates a title longer than 100 characters, causing the application to hang.\n- **Solution**: \n  - Replace recursive logic with a retry loop (max 5 attempts)\n  - After 5 attempts, truncate the title to 100 characters\n  - This guarantees the automation doesn't hang indefinitely at the metadata stage\n- **Patch applied**: cf1c308 in the MoneyPrinterV2 repository\n\n### Account Bans\n- Using automation on YouTube/Twitter risks account termination\n- Mitigate by:\n  - Using aged accounts with history\n  - Limiting upload frequency\n  - Adding human oversight\n  - Using residential proxies for IP diversity

### Git/Fork Workflow Issues
- **Problem**: When trying to push changes to a repository you don't have write access to (e.g., the original MoneyPrinterV2 repo), you'll get "Permission denied" errors.
- **Solution**:
  - Fork the repository to your own GitHub account
  - Change the remote URL to point to your fork: `git remote set-url origin git@github.com:your-username/MoneyPrinterV2.git`
  - You can use the GitHub CLI to fork: `gh repo fork FujiwaraChoki/MoneyPrinterV2 --clone=false`
  - Then push to your fork: `git push -u origin main`
  - To keep your fork updated with the original: `git remote add upstream git@github.com:FujiwaraChoki/MoneyPrinterV2.git` and periodically `git fetch upstream && git merge upstream/main`

## Security Considerations

### API Key Management
- Never commit real API keys to version control
- Use environment variables or a secure secrets manager
- Encrypt sensitive config sections if storing locally

### Account Security
- Use unique, strong passwords for each platform
- Enable two-factor authentication where possible
- Regularly monitor account activity

### Legal Compliance
- Disclose affiliate relationships as required by FTC
- Follow YouTube's spam policies
- Respect copyright and intellectual property

## References\n\n- Session-proven macOS setup details: `references/moneyprinterv2-macos-setup.md`\n- Git fork workflow guide: `references/git-fork-workflow.md`\n- Advanced troubleshooting guide: `references/moneyprinterv2-advanced-troubleshooting.md`\n- Shell/subshell issue resolution: `references/shell-subshell-issue.md`\n- YouTube title generation infinite loop fix: `references/youtube-title-generation-fix.md`\n- MoneyPrinterV2 GitHub: https://github.com/FujiwaraChoki/MoneyPrinterV2\n- MoneyPrinterV2 Documentation: docs/\n- Ollama: https://ollama.com/\n- YouTube API: https://developers.google.com/youtube/v3\n- Twitter API: https://developer.twitter.com/\n- Affiliate Marketing: Amazon Associates, ShareASale, etc.\n\n## Next Steps

1. Install dependencies and set up MPV2
2. Configure accounts and API keys
3. Test video generation and upload
4. Set up Twitter automation
5. Integrate affiliate marketing
6. Implement profit tracking
7. Connect to stock trading API
8. Set up CRON jobs for full automation
```
