# Build 53 TestFlight Failure Receipt

Updated: 2026-05-11 14:22

## Root cause isolated
Swift compile failure in `BuddyTemplateSanitizer.swift`:
- `CouncilStarterBuddyTemplate.default(for:)` collided with Swift reserved word `default` in call syntax.
- `BuddyInstance` has no `template` member.
- `BuddyInstance` has no `ownerID` member; creator data lives under `instance.provenance.creatorId`.

## Local fix applied
File: `/Users/codysumpter/BMO-Builds/prismtek-apps/apps/bemore-ios-native/BeMoreAgentShell/BuddyTemplateSanitizer.swift`

Changes:
- Replaced invalid template access with `Self.defaultTemplate(for: instance.identity)`.
- Renamed fallback method from `default(for:)` to `defaultTemplate(for:)`.
- Replaced `instance.ownerID` with `instance.provenance.creatorId ?? "local-operator"`.

## Verification
Command run from `apps/bemore-ios-native`:
```bash
xcodebuild -project BeMoreAgent.xcodeproj -scheme BeMoreAgent -configuration Debug -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO build
```

Result: `** BUILD SUCCEEDED **`
Log: `/tmp/bemore-build53-fix2.log`

## Remaining release action
Commit/push the sanitizer fix, then re-run the TestFlight workflow/Xcode Cloud archive.


## 2026-05-11T15:07:51 — iOS upload receipt
- Commit: `b2900f3 fix: bundle MLC model resources for TestFlight`
- GitHub Actions run: `25690620076`
- Validate job: passed.
- TestFlight job: passed.
- Archive: passed.
- Bundled Gemma 4 MLC archive verification: passed.
- Export/upload: `Upload succeeded`, `Uploaded package is processing`, `** EXPORT SUCCEEDED **`.
- Current completion gate: not marked complete until Cody can see the build in TestFlight/App Store Connect; Apple processing can lag after upload.
- Annotation: imported provisioning profile name was `BMO`, expected `iOS Team Store Provisioning Profile: BeMoreAgent`; workflow used imported name successfully.
