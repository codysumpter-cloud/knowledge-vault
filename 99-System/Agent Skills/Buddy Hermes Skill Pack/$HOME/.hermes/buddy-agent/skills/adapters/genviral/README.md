# Genviral Adapter

Use this adapter for social publishing workflows where Genviral is the backend.

## Allowed without approval

- list connected accounts
- list folders
- list files
- inspect draft metadata
- generate draft titles/descriptions
- analyze analytics
- prepare posting plan

## Requires Prismtek approval

- publish post
- schedule post
- update post
- delete post
- connect/disconnect account
- change account settings
- use paid features that may increase spend

## Recommended workflow

```txt
verify account
→ select content source
→ pick unused asset
→ generate metadata
→ dry-run preview
→ request approval
→ publish/schedule through adapter
→ log posted asset
→ send confirmation
```

## Required logs

- asset id / filename
- platform
- account id or alias
- title
- description
- hashtags
- scheduled/published time
- result URL if available
- adapter response summary
