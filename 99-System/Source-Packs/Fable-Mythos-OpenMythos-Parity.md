# Fable/Mythos Open Architecture Parity Source Pack

status: reference  
last-verified: 2026-06-15  
owners: KnowledgeVault / Vegapunk Brain / Buddy ecosystem

## Summary

This source pack records the current evidence for Claude Fable 5 / Claude Mythos 5 feature parity against OpenMythos, OpenFable, and Buddy runtime targets.

The core decision: **OpenMythos and OpenFable are useful architecture references, not proven replacements for Claude Fable 5 or Claude Mythos 5.** Buddy should build missing runtime features as safe adapters and should only upgrade claims after validation receipts exist.

## Sources

| Source | Type | Status | Notes |
|---|---|---|---|
| `https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5` | official docs | reference | Baseline for hosted feature claims. |
| `https://github.com/kyegomez/OpenMythos` | open repo | reference | Theoretical recurrent-depth transformer implementation. |
| `https://github.com/lovestaco/OpenFable` | open repo | reference | Theoretical Fable-branded reconstruction with OpenMythos-style naming overlap. |
| `https://github.com/anthropic-fable/claude-fable-5` | open repo | reference | Third-party desktop client, not model source. |

## Decision record

- `decision`: Treat OpenMythos/OpenFable as architecture references only.
- `reason`: The open repos do not provide trained frontier weights, Anthropic runtime behavior, full tool/memory/code/vision stack, or production serving proof.
- `impact`: Buddy may implement a Fable/Mythos-inspired runtime surface, but must not advertise open model equivalence.

## Parity ledger

| Capability | Current classification | Evidence note |
|---|---|---|
| Trained model weights | missing in open repos | No equivalent released checkpoint was found in OpenMythos/OpenFable. |
| Recurrent-depth architecture | partial | OpenMythos documents Prelude, recurrent block, Coda, loop depth, MLA/GQA, MoE, and halting concepts. |
| Large context / large output | claimed-not-verified | Anthropic documents this for hosted models; OpenMythos-style tables claim large variants, but Buddy has no local proof. |
| Adaptive compute / effort | partial | Open architecture can expose loop budgets; hosted API exposes higher-level effort behavior. |
| Memory tool | missing in open architecture | Should be implemented through Buddy/Vegapunk memory adapters. |
| Code execution | missing in open architecture | Should be implemented through guarded sandbox adapters. |
| Programmatic tools | missing in open architecture | Should be implemented through Buddy skills/provider protocols. |
| Context editing / clearing | missing | Needs Buddy context-manager design. |
| Compaction | missing or docs-only | Needs algorithm, tests, and receipts. |
| Vision | missing in OpenMythos/OpenFable | Omni Buddy and Prismtek Apps own device/product vision receipts. |
| Provider safety/fallback behavior | external-runtime-required | Normalize provider responses; do not fabricate vendor billing behavior. |

## Graph event guidance

When a repo changes parity status, emit a Vegapunk event with:

```json
{
  "type": "parity.status_changed",
  "subject": "fable-mythos-open-architecture",
  "repo": "codysumpter-cloud/<repo>",
  "capability_id": "<capability>",
  "old_status": "<status>",
  "new_status": "<status>",
  "evidence": ["<repo path>", "<validation command>", "<source URL>"]
}
```

## Retrieval tags

- Buddy
- Fable 5
- Mythos 5
- OpenMythos
- OpenFable
- model parity
- runtime parity
- Vegapunk Brain
- source pack

## Next actions

1. Link this note from the relevant project source-of-truth pages.
2. Add a graph event example for model-runtime parity status changes.
3. Let Buddy Agent consume its typed model-runtime parity registry and emit machine-readable status.
