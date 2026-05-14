# Hermes Activation Runbook — No-API X Relationship Adapter

## Purpose

Activate the no-API X relationship adapter locally so Hermes can detect and process X relationship events without depending on paid X API credits.

## Source Location

KnowledgeVault source pack:

```txt
KnowledgeVault/99-System/Social Automation/No-API X Relationship Adapter/
```

## Local Install Target

Recommended local paths:

```txt
~/.hermes/scripts/prismtek_social_no_api_adapter.py
~/.hermes/bin/prismtek-social-no-api
```

## Install Commands

```bash
mkdir -p ~/.hermes/scripts ~/.hermes/bin
cp "KnowledgeVault/99-System/Social Automation/No-API X Relationship Adapter/scripts/prismtek_social_no_api_adapter.py" ~/.hermes/scripts/
chmod +x ~/.hermes/scripts/prismtek_social_no_api_adapter.py
ln -sf ~/.hermes/scripts/prismtek_social_no_api_adapter.py ~/.hermes/bin/prismtek-social-no-api
```

## Verify

```bash
~/.hermes/bin/prismtek-social-no-api status
```

Expected:

```json
{
  "ok": true,
  "adapter": "Prismtek No-API X Relationship Adapter",
  "safe_by_default": true,
  "x_api_required": false
}
```

## First Manual Seed for @legitgaran

Use the Prismtek source post URL that @legitgaran retweeted.

```bash
~/.hermes/bin/prismtek-social-no-api retweet-seed \
  --source-post-url "<PRISMTEK_SOURCE_POST_URL>" \
  --retweeter-handle legitgaran \
  --write-receipt
```

Then create a draft:

```bash
~/.hermes/bin/prismtek-social-no-api relationship-draft \
  --receipt-id "<RECEIPT_ID>" \
  --style compare_notes \
  --write-receipt
```

## Required Hermes Follow-Up

After install:

1. Verify script runs.
2. Create a relationship receipt for @legitgaran.
3. Create a reply draft.
4. Do not publish the reply until exact text/hash is approved.
5. Update the retweet relationship cron job to use no-API/manual-seed/browser routes before X API.
6. Update the Cron Job card and Next Plans.

## Local Browser Work Still Needed

The included Python script handles manual seed, receipts, and drafts. Hermes still needs to wire local Mac browser behavior for:

- notification scan through signed-in Safari;
- visible retweet/repost modal scan;
- screenshot/vision read;
- accessibility click/type for approved likes/replies.

Those routes should be implemented in the local Hermes runtime where Safari/screenshot tools are actually available.

## Safety Boundaries

Do not:

- store cookies/tokens/auth headers in KnowledgeVault;
- bypass CAPTCHA/MFA/locks;
- hammer failed routes;
- publish replies without approval;
- DM automatically;
- follow automatically;
- repeat identical CTA replies.

Public receipt wording should use:

```txt
signed-in Safari UI
signed-in local web-session fallback
manual seed fallback
screenshot/vision read
```

not raw cookie/token implementation names.
