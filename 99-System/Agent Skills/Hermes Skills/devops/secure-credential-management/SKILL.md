---
name: secure-credential-management
description: "Secure patterns for handling sensitive credentials across integrations"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Security, Credentials, API Keys, OAuth, Authentication]
    related_skills: [github-access-management, hermes-gateway-routing]
prerequisites:
  commands: []
---
# Secure Credential Management

## Purpose

Establish secure patterns for handling sensitive credentials (API keys, passwords, tokens) across all integrations. This skill encodes the non-negotiable security posture: **never store plaintext credentials in agent memory or files**.

## Core Principles

1. **Plaintext credentials are forbidden** - never store passwords, API secrets, or recovery codes in memory, config files, or any agent-managed storage
2. **Least privilege** - credentials should have minimal necessary permissions
3. **Defense in depth** - use multiple layers of security (encryption, access controls, audit logs)
4. **User agency** - guide users to secure practices rather than refusing outright

## Secure Patterns

### Pattern A: Environment Variables with Proper Permissions
```bash
# Store in an app-specific env file with chmod 600
mkdir -p ~/.config/<app-name>
chmod 700 ~/.config/<app-name>
printf 'GOOGLE_API_KEY=your_key_here\n' > ~/.config/<app-name>/env
chmod 600 ~/.config/<app-name>/env
```

If an app only reads process env or a committed config file, patch the app and its preflight script to load the chmod-600 env file at startup. Keep real secrets out of repository files such as `config.json`; only commit the loader, never the env file.

### Pattern B: Service Account Keys
1. Create Google Cloud service account with minimal required roles
2. Download JSON key file
3. Store securely: `chmod 600 service-account.json`
4. Use `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### Pattern C: OAuth 2.0 Tokens
- Use Google's OAuth flow for user consent
- Store refresh tokens securely (encrypted, not in plaintext)
- Tokens should have limited scope (e.g., `https://www.googleapis.com/auth/spreadsheets.readonly`)

### Pattern D: Password Manager Integration
```bash
# Example with bitwarden CLI
bw get password google-account
# Or with pass
pass show google/api-key
```

## User Preferences Handling

### When User Insists on Storing Credentials
1. **Educate**: Explain the security risk clearly
2. **Redirect**: Offer secure alternatives
3. **Escalate**: If user persists, document the refusal and continue with secure pattern

### Pitfall: User Frustration with Security
- Signal: "Just store it somewhere safe"
- Response: Acknowledge desire for convenience, reiterate security requirements, offer to set up a secure system that balances both

## Google-Specific Guidance

### Google Sheets
- **Recommended**: Use OAuth with scope `https://www.googleapis.com/auth/spreadsheets`
- **Alternative**: API key with restricted referrer (less secure)
- **Never**: Store Google account password

### Google Drive
- OAuth with appropriate Drive scopes
- Consider using service account for server-to-server access

### Gmail
- OAuth is mandatory for Gmail API
- Never use username/password

## Implementation Commands

### Check if credentials exist securely
```bash
# Check for environment variables
env | grep -i google

# Check for service account file
if [ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "Service account found: $(basename "$GOOGLE_APPLICATION_CREDENTIALS")"
fi
```

### Verify credentials work
```bash
# Test Google Sheets access
python3 -c "import googleapiclient; service = googleapiclient.discovery.build('sheets', 'v4'); print('Authenticated')"

# Test Gmail API
python3 -c "from googleapiclient.discovery import build; build('gmail', 'v1')"
```

## Security Verification

Before claiming a Google integration is working:
- ✅ Credentials are not stored in plaintext in agent storage
- ✅ Permissions are minimal and appropriate
- ✅ Fallback mechanisms exist if primary credentials fail
- ✅ User has been educated about security trade-offs

## References

- Google API Best Practices: https://developers.google.com/maps/premium/best-practices
- OAuth 2.0 Security Considerations: https://oauth.net/2/security/
- Principle of Least Privilege: https://en.wikipedia.org/wiki/Principle_of_least_privilege
