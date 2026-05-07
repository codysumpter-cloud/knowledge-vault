# DNS Guardrails

Last documented: 2026-05-07

## Prime rule

Do not touch, replace, suggest replacing, or casually route around working DNS for Prismtek or AutoMindLab properties.

DNS changes are protected release actions. They require explicit user authorization.

## Current protected domain state

### prismtek.dev

- Current intended hosting: Cloudflare Pages
- Current intended DNS posture: keep the free Cloudflare Pages DNS/routing intact
- Reason: prismtek.dev is a public brand site and benefits from free Cloudflare Pages hosting, CDN, TLS, rollback safety, and separation from VPS uptime/configuration risk.

Do not move prismtek.dev to the VPS unless the user explicitly asks for a cutover.

### automindlab.tech

- Current intended DNS posture: Hostinger DNS is working and should remain intact
- Reason: a working Hostinger DNS setup is an asset to protect, not an unfinished deployment step.

Do not replace or reroute automindlab.tech DNS unless the user explicitly asks for a DNS change.

## Safe future pattern

If a VPS-backed public route is needed later, prefer additive subdomains instead of destructive apex/root-domain cutovers.

Possible examples, only if explicitly requested:

- api.prismtek.dev -> VPS
- cloud.prismtek.dev -> VPS
- app.automindlab.tech -> VPS
- factory.automindlab.tech -> VPS

These are examples, not recommendations to execute.

## Correct operating model

- Direct VPS IP: safe for direct testing and staging checks
- Existing public domains: leave untouched by default
- DNS cutover: requires explicit instruction from the user
- DNS verification: read-only checks are okay only when needed and should not be framed as a reason to change anything

## Failure mode to avoid

Bad assumption:

```text
The VPS app is healthy by IP, therefore the public domain should point to the VPS.
```

Correct assumption:

```text
The VPS app is healthy by IP. Existing DNS remains authoritative and untouched unless the Release Conductor explicitly authorizes a change.
```
