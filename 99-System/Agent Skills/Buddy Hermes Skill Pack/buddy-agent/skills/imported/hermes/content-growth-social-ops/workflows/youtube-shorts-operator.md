# YouTube Shorts Operator Workflow

## Purpose

Run a safe, repeatable YouTube Shorts workflow for Hermes/Buddy.

## Required inputs

- YouTube account alias
- content folder/source
- asset inventory
- metadata rules
- cadence
- approval mode
- posted-content log location

## Workflow

```txt
1. Verify account visibility through adapter.
2. Read content inventory.
3. Exclude already-posted assets.
4. Select next eligible asset.
5. Generate title variants.
6. Generate description and hashtags.
7. Check copyright/source restrictions.
8. Build preview.
9. Ask for approval if posting or scheduling.
10. Publish/schedule only through adapter.
11. Log result.
12. Send confirmation summary.
```

## Metadata template

```txt
Title:
- 35-70 characters when possible
- concrete outcome
- no clickbait lie

Description:
- 1 sentence context
- 2-4 bullets
- CTA
- 3-5 hashtags

Thumbnail/title image:
- one visual claim
- 3-5 words
- high contrast
```

## Cadence default

Start with 1 short per day.

Scale only after the workflow has:

- no duplicate posts
- clean metadata
- stable confirmations
- no account errors
- acceptable performance trend

## Internal log schema

```json
{
  "asset_id": "clip_042.mp4",
  "platform": "youtube",
  "account_alias": "main",
  "title": "string",
  "description_hash": "string",
  "status": "drafted|approved|published|failed",
  "published_url": "optional",
  "published_at": "ISO-8601",
  "notes": "string"
}
```

## Failure handling

If upload fails:

1. Do not retry endlessly.
2. Mark status as `failed`.
3. Capture adapter error.
4. Notify Prismtek.
5. Suggest one fix.
