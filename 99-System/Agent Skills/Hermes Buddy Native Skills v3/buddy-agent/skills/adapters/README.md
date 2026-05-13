# Buddy Adapter Boundary

These native skills are instruction packages. Buddy should execute real-world actions only through adapters that enforce allowlists, risk class checks, dry-run previews, and explicit Prismtek approval.

Recommended adapters:

- `social-draft`: prepare drafts and previews only.
- `x-readonly`: read approved X API/export data only; no write scopes.
- `youtube-draft`: prepare metadata and upload checklists only.
- `twitch-draft`: prepare stream title, schedule, and promo copy only.
- `browser-readonly`: isolated browser profile for approved URLs only.
- `odds-readonly`: fetch odds/market data only.
- `prediction-market-readonly`: fetch Polymarket market data only.
- `knowledge-vault-readonly`: read canonical skill notes and memory; writes require approval.

Never let a skill directly handle credentials, cookies, wallets, sportsbook accounts, social posting, messaging, or repo mutation.
