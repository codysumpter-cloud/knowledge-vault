# Hermes Skill Mirrors

These are Hermes-facing mirrors that point back to the Buddy-compatible skill pack.

Do not fork logic into separate Hermes-only behavior unless necessary.

Recommended flow:

```txt
Hermes prompt
→ read Hermes mirror
→ load Buddy-compatible skill metadata
→ operate in draft-only / analysis-only mode
→ ask Buddy adapter for approved execution if needed
```

Hermes should treat Buddy as the future runtime authority.
