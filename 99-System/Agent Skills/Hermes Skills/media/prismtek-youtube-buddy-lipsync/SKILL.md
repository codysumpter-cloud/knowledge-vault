---
name: prismtek-youtube-buddy-lipsync
description: Durable knowledge-vault reference for the Prismtek/Buddy talking-host lip-sync workflow.
version: 1.1.0
author: Prismtek
canonical_runtime: codysumpter-cloud/buddy-agent#18
operator_reference: codysumpter-cloud/buddy-brain#315
app_contract: codysumpter-cloud/prismtek-apps#138
local_device_reference: codysumpter-cloud/omni-buddy#11
---

# Prismtek YouTube Buddy Lip-Sync

This note stores the long-lived skill reference for the Buddy talking-host lip-sync workflow.

The canonical runnable implementation lives in `buddy-agent`. `knowledge-vault` keeps the memory/skill reference so Hermes, Buddy, and future agents can quickly understand the workflow, ownership boundaries, and verification path.

## What the Skill Does

- Starts with a clean Buddy avatar image.
- Generates small pixel-art mouth states.
- Analyzes narration energy frame-by-frame.
- Overlays Buddy onto a video using a deterministic renderer.
- Produces a proof clip and render receipt for review.

## Why This Exists

The earlier PR to `NousResearch/hermes-agent` was useful, but incomplete as a Prismtek ecosystem change. The completed split is:

| Repo | Purpose |
| --- | --- |
| `buddy-agent` | runnable runtime package |
| `buddy-brain` | operator skill reference |
| `omni-buddy` | embodied/local-device reference |
| `prismtek-apps` | app-facing UX contract |
| `knowledge-vault` | durable skill memory |
| `hermes-agent` fork/upstream | optional Hermes-compatible skill surface |

## Verification Memory

Canonical runtime validation:

```bash
python3 -m py_compile scripts/*.py
python3 -m pytest tests/test_prismtek_youtube_buddy_lipsync.py -q
```

Local validation before opening the runtime PR passed with 4 smoke tests.

## Visual Quality Rules

Accepted Buddy mouth style:

- one mouth only;
- small/cute pixel-art mouth;
- no darker patch around the mouth;
- no leftover original-smile marks;
- full Buddy crop remains intact;
- proof clip is reviewed before full render.

## Related PRs

- Runtime: `codysumpter-cloud/buddy-agent#18`
- Operator: `codysumpter-cloud/buddy-brain#315`
- Omni/local device: `codysumpter-cloud/omni-buddy#11`
- App contract: `codysumpter-cloud/prismtek-apps#138`
- Upstream context: `NousResearch/hermes-agent#26463`
