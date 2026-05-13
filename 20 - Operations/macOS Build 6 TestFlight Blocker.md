---
type: release-receipt
status: blocked
updated: 2026-05-11T15:07:51
---
# macOS Build 6 TestFlight Blocker

## Receipt
- Workflow run: `25552738755`
- Job: `build`
- Failed step: `Archive BeMore Mac`
- Upload step: skipped because archive failed.

## Exact blocker
- Xcode error: `Choose a certificate to revoke. Your account has reached the maximum number of certificates.`
- Xcode error: `Signing certificate is invalid. Signing certificate "Apple Development: cody.sumpter@gmail.com (MLM49L8SMR)" ... is not valid for code signing. It may have been revoked or expired.`

## Current local Mac state
- Local keychain has a valid `Apple Development: Cody Sumpter (MLM49L8SMR)` certificate expiring May 7 2027.
- Attempted CI secret refresh by exporting the local identity; export is blocked by macOS Keychain/SecurityAgent approval prompt.

## Next action
Approve the keychain export prompt on the Mac, then rerun the export/secret update and macOS TestFlight workflow. If Apple still reports max certificates, revoke stale certificates in Apple Developer portal or create/provide a valid Mac App Distribution/Apple Distribution signing asset.
