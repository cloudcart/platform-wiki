---
type: concept
nav_path: "Concept → Merchant roles → API access (parallel mechanism)"
aliases: ["API access", "API Keys vs PAT Tokens", "Programmatic credentials", "Integration credentials", "API scope vs Moderator permission", "Courier integration API key", "Revoke API key"]
tags: [access, api, integrations, admin, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[merchant-roles]]. See the hub for the other aspects (owner, moderator, permissions tree, force sign-out + 2FA, notifications + audit, storefront contrast).

# Merchant roles — API access (parallel mechanism)

## Definition

**API access** is an access mechanism entirely separate from the Owner / Moderator staff model. Programmatic clients (ERP integrations, marketplaces, couriers, server-to-server callers, dev scripts) authenticate via:

- **API Keys** ([[settings-api-keys]]) — long-lived OAuth-style credentials assigned to integrations / apps. Each API Key has its own set of scopes (read products, write orders, etc.). Used by ERP integrations, marketplaces, and server-to-server callers.
- **Personal Access Tokens (PATs)** ([[settings-pat-tokens]]) — short-to-mid-lived tokens for development / scripts. Created with explicit scopes. Often used during integration testing.

Both mechanisms authenticate via HTTP headers (Bearer / API-Key), have their **own scope model** (NOT Moderator permissions), do **NOT appear on [[settings-staff]]**, and are **NOT subject to the `administrators` plan-feature cap**. They have no username, no 2FA, no avatar, no login screen — they're machine identities.

## Scope

What this page covers:

- The two programmatic-credential types (API Keys, PATs) and their typical uses.
- Why they're parallel to (not a subset of) the Moderator model.
- Scopes vs Moderator permissions.
- How revocation works and why Force sign out does NOT touch these.
- A worked courier-integration example.

Not covered here:

- The full screen UX of [[settings-api-keys]] and [[settings-pat-tokens]] — feature pages.
- The scope catalogues — they vary and are documented per-feature.
- The JSON-API v2 endpoint reference — see [[json-api-v2]].
- Webhook authentication (a different leg of the API surface) — see [[settings-hooks]].

## Contrasts

- **API Key vs Moderator** — Moderators are human admin accounts with username, email, login, 2FA, avatar — they appear on [[settings-staff]] and count toward the `administrators` cap. API Keys are programmatic credentials with their own scope model — they don't appear on Staff, don't count toward the cap, don't have 2FA.
- **API Key (long-lived) vs PAT Token (short-to-mid-lived)** — API Keys are issued for integrations that run indefinitely (ERP sync, courier label generation, marketplace inventory feed). PATs are typically used during development / scripting and are rotated more often. Both use the same HTTP-header authentication mechanism.
- **API scope vs Moderator permission** — scopes (e.g., Orders read, Fulfilments write) gate which API endpoints a credential can call. Moderator permissions (e.g., `settings.admins.all`) gate which admin-panel sections a staff user sees. The two systems reference similar resource families but are **not interchangeable** — granting a Moderator the "Orders" permission does NOT give an API Key the right to read orders, and vice versa.
- **Force sign out vs API-Key revocation** — Force sign out ([[merchant-roles-force-signout-2fa]]) kills human-facing browser sessions. It does **NOT** revoke API Keys or PAT Tokens. After a suspected credential leak, the merchant must visit [[settings-api-keys]] / [[settings-pat-tokens]] to revoke programmatic credentials individually.

## Where it applies

### API Keys — long-lived integration credentials

[[settings-api-keys]] is where the Owner (or a Moderator with the appropriate permission) creates, names, and revokes API Keys. Each key:

- Gets a name (e.g., "Courier Integration X") for the merchant to identify it.
- Carries a set of scopes chosen at creation time (e.g., Orders read + Fulfilments write).
- Authenticates via HTTP headers on every API request.
- Is revocable at any time from [[settings-api-keys]]; revocation is immediate (the next request from the integration is rejected).
- Does NOT consume an `administrators` plan-feature seat.

### PAT Tokens — short-to-mid-lived dev credentials

[[settings-pat-tokens]] is the parallel screen for Personal Access Tokens. Same authentication mechanism; typically used:

- During integration testing (a developer creates a PAT with the same scopes as the planned API Key to validate behaviour before promoting the integration to production).
- For one-off scripts / data exports.
- For ad-hoc admin operations performed via the JSON-API.

PATs have their own scope catalogue (similar to API-Key scopes but not identical — verify against each screen).

### Authentication mechanism

Both credential types authenticate via HTTP headers (typically `Authorization: Bearer <token>` or an equivalent API-Key header). The endpoint handler:

1. Reads the token from the header.
2. Looks up the credential record and its scopes.
3. Checks the requested operation against the credential's scopes.
4. Allows or rejects (HTTP 403 if scopes don't cover the operation).

No 2FA challenge, no session cookie — pure stateless credential check.

### Revocation surfaces — per-credential, not bulk

The merchant revokes individual credentials from their respective screens:

- **[[settings-api-keys]]** — Revoke button per row; the key is invalidated immediately.
- **[[settings-pat-tokens]]** — Revoke button per row; the token is invalidated immediately.

There is no "revoke all API credentials" bulk action analogous to Force sign out. If the merchant needs to invalidate every programmatic credential at once (e.g., after a major security incident), they must walk each list and revoke each row.

## Worked example — API integration with a courier system

The merchant integrates with a courier API to auto-generate shipping labels:

1. **Owner opens [[settings-api-keys]] → Create API Key.** Picks scopes: Orders (read), Fulfilments (write). Names the key "Courier Integration X".
2. **The platform issues a token.** Owner copies it into the courier's integration form.
3. **The courier service calls CloudCart APIs using the token.** The token's scopes are limited to Orders + Fulfilments — calls to (e.g.) Products write or Customers read would return HTTP 403.
4. **Owner can revoke the key at any time** from [[settings-api-keys]]. Revocation is immediate.
5. The integration does NOT appear on [[settings-staff]] and does NOT count toward the Moderator seat cap.

If the merchant later suspects the courier's system is compromised, they revoke just that one API Key — every other key (marketplaces, ERP, etc.) keeps working unchanged.

## Why this design — separation of human and machine

Mixing human staff accounts with machine credentials would create three problems:

- **Cap pressure.** A merchant who wires up 8 integrations would burn 8 Moderator seats on the `administrators` plan-feature.
- **Audit confusion.** Email lifecycle notifications (`new_admin_account`, etc.) firing for every integration would drown out actual staff changes.
- **Permission-tree mismatch.** Integrations need scopes like "Orders read + Fulfilments write" — narrower than the Moderator permission tree which is structured around admin-panel sections.

By keeping the two models parallel, each scales independently — unlimited integrations on one side, capped human staff on the other.

## Related

- [[merchant-roles]] — hub.
- [[merchant-roles-moderator]] — the parallel human-staff model.
- [[merchant-roles-force-signout-2fa]] — explicit note that Force sign out does NOT touch API Keys or PATs.
- [[settings-api-keys]] — long-lived API Keys screen.
- [[settings-pat-tokens]] — PAT Tokens screen.
- [[api-key]] — API-Key entity.
- [[pat-token]] — PAT-Token entity.
- [[json-api-v2]] — the API surface these credentials authenticate to.
- [[settings-hooks]] — webhook events (note: admin-account events don't have webhook coverage — only customer / order / product webhooks).

## Open Questions

None.
