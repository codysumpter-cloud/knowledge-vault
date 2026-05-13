# VPS SMTP Configuration for money-printer-v2

When configuring the VPS agent for the money-printer-v2 project, SMTP credentials need to be stored in the project's config.json file.

## Configuration Path
`/home/hermes/bread-makers/money-printer-v2/config.json`

## Required Fields
- `username`: Gmail email address (e.g., `Cody.sumpter@gmail.com`)
- `password`: App-specific password or account password

## Update Commands
```bash
# Set username
sed -i 's/"username":.*/"username": "Cody.sumpter@gmail.com",/' /home/hermes/bread-makers/money-printer-v2/config.json

# Set password
sed -i 's/"password":.*/"password": "Prismatic812!",/' /home/hermes/bread-makers/money-printer-v2/config.json
```

## Verification
```bash
grep -A 2 -B 2 '"username"\|"password"' /home/hermes/bread-makers/money-printer-v2/config.json
```

## Notes
- The VPS agent requires direct SMTP access for email notifications from the money-printer-v2 application
- Credentials are stored in plaintext in the config file - ensure appropriate file permissions
- After updating config, restart any dependent services if necessary
- For Gmail, consider using an App Password if 2FA is enabled
