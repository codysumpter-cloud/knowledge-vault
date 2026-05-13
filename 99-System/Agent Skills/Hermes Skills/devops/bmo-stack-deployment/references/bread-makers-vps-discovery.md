# Bread-Makers Discovery on Hostinger VPS

## Location
The bread-makers project is located at: `/home/hermes/bread-makers/`

## Structure
```
/home/hermes/bread-makers/
├── .env                          # TradingAgents environment variables
├── REQUIRED_KEYS.md              # API key requirements guide
├── config/                       # Configuration directory
├── logs/                         # Log directory
├── money-printer-v2/             # Money Printer v2 component
│   ├── config.json               # Main config (includes email SMTP settings)
│   ├── config.example.json       # Template config
│   ├── src/                      # Source code
│   └── venv/                     # Python virtual environment
├── scouts/                       # Scouts directory
├── strategy.md                   # Strategy documentation
├── trading-agents/               # TradingAgents component
│   ├── .env                      # Environment variables (API keys)
│   ├── tradingagents/            # Trading agents source
│   ├── cli/                      # CLI interface
│   ├── venv/                     # Python virtual environment
│   └── docker-compose.yml        # Docker compose for services
└── venv/                         # Main virtual environment
```

## Key Configuration Files

### Money Printer v2 Email Settings
File: `/home/hermes/bread-makers/money-printer-v2/config.json`
```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "",
    "password": ""
  }
}
```

### TradingAgents Environment
File: `/home/hermes/bread-makers/trading-agents/.env`
Expected variables:
- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `ANTHROPIC_API_KEY`
- `ALPHA_VANTAGE_API_KEY`
- `OPENROUTER_API_KEY` (optional)

## Verification Notes
- The trading-agents directory shows local modifications: `M tradingagents/default_config.py`
- Money Printer v2 has a Gemini API key configured but email credentials are empty
- Both components have virtual environments set up
- Git repositories are present and appear to be synchronized with origin/main

## Relevance to BMO Stack
As noted in REQUIRED_KEYS.md: "BMO Note: Once these are set, we can launch the test runs! 🚀"
Indicating bread-makers is part of the broader BMO/BeMore ecosystem for testing and deployment validation.
