---
type: concept
nav_path: "Concept → Merchant roles → API access (parallel mechanism)"
aliases: ["API access", "API Keys vs PAT Tokens", "Programmatic credentials", "Integration credentials", "API scope vs Moderator permission", "Courier integration API key", "Revoke API key"]
tags: [access, api, integrations, admin, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 2
---

> Part of [[merchant-roles]]. See the hub for the other aspects (owner, moderator, permissions tree, force sign-out + 2FA, notifications + audit, storefront contrast).

# Merchant roles — API access (parallel mechanism)

## Definition

**API access** is an access mechanism entirely separate from the Owner / Moderator staff model. Programmatic clients (ERP integrations, marketplaces, couriers, server-to-server callers, dev scripts) authenticate via:

- **API Keys** ([[settings-api-keys]]) — long-lived keys for JSON-API v2 ([[json-api-v2]]), sent in the `X-CloudCart-ApiKey` header. A key has **no scopes**: every active key reaches every resource the API exposes ([[json-api-auth]]). Used by ERP integrations, marketplaces and server-to-server callers.
- **Personal Access Tokens (PATs)** ([[settings-pat-tokens]]) — the owner's tokens for the CLI and the [[admin-graphql-api]], sent as `Authorization: Bearer`. Each has an access level: Read Only, Full Access or Custom Permissions ([[settings-pat-tokens-scopes]]). They do not work on JSON-API v2.

Neither uses Moderator permissions; both **do NOT appear on [[settings-staff]]**, and are **NOT subject to the `administrators` plan-feature cap**. They have no username, no 2FA, no avatar, no login screen — they're machine identities.

An **AI agent** connected to the store signs in with one of these or with an admin's own browser sign-in: see [[ai-agent-access]].

On the [[admin-graphql-api]], a token always acts as the store owner. A browser sign-in acts as the admin who signed in, with that admin's role permissions, because staff permissions apply there.

## Scope

What this page covers:

- The two programmatic-credential types (API Keys, PATs) and their typical uses.
- Why they're parallel to (not a subset of) the Moderator model.
- PAT scopes vs Moderator permissions.
- How revocation works and why Force sign out does NOT touch these.
- A worked courier-integration example.

Not covered here:

- The full screen UX of [[settings-api-keys]] and [[settings-pat-tokens]] — feature pages.
- The PAT scope catalogue — see [[settings-pat-tokens-scopes]].
- The JSON-API v2 endpoint reference — see [[json-api-v2]].
- Webhook authentication (a different leg of the API surface) — see [[settings-hooks]].

## Contrasts

- **API Key vs Moderator** — Moderators are human admin accounts with username, email, login, 2FA, avatar — they appear on [[settings-staff]] and count toward the `administrators` cap. API Keys are programmatic credentials — they don't appear on Staff, don't count toward the cap, don't have 2FA.
- **API Key vs PAT Token** — an API Key serves JSON-API v2 integrations that run indefinitely (ERP sync, courier labels, marketplace feeds), with full access. A PAT signs in the CLI, scripts and AI agents on Admin GraphQL as the owner, limited by its access level, optionally with an end date and an IP list.
- **PAT scope vs Moderator permission** — a PAT's scopes (e.g. `orders:read`) gate what the token may do. Moderator permissions gate which admin sections a staff user sees. They are **not interchangeable**: ticking "Orders" for a Moderator gives no token anything.
- **Force sign out vs API-Key revocation** — Force sign out ([[merchant-roles-force-signout-2fa]]) kills human-facing browser sessions. It does **NOT** revoke API Keys or PAT Tokens. After a suspected credential leak, the merchant must visit [[settings-api-keys]] / [[settings-pat-tokens]] to revoke programmatic credentials individually.

## Where it applies

### API Keys — long-lived integration credentials

[[settings-api-keys]] is where the Owner (or a Moderator with the appropriate permission) creates, names, and revokes API Keys. Each key:

- Gets a name (e.g., "Courier Integration X") for the merchant to identify it.
- Reaches every JSON-API v2 resource; there is nothing to narrow.
- Is switched off or deleted at any time from [[settings-api-keys]]; the next request is rejected.
- Does NOT consume an `administrators` plan-feature seat.

### PAT Tokens — short-to-mid-lived dev credentials

[[settings-pat-tokens]] is the parallel screen for Personal Access Tokens. Same authentication mechanism; typically used:

- For the CloudCart CLI and AI agents ([[ai-agent-access]]).
- For one-off scripts and exports through Admin GraphQL.

Only the owner creates them, and changes made with one are recorded as the owner's.

### Authentication mechanism

- **API Key:** JSON-API v2 checks only that the key exists and is active (HTTP 401 otherwise).
- **PAT:** the token is checked (owner, active, dates, IP list), then its scopes against the operation; a missing scope is refused with `ACCESS_DENIED` naming it ([[admin-graphql-api]]).

No 2FA challenge, no session cookie — pure stateless credential check.

### Revocation surfaces — per-credential, not bulk

The merchant revokes individual credentials from their respective screens:

- **[[settings-api-keys]]** — the **Active** switch or **Remove** per row, or a bulk delete; effective from the next request.
- **[[settings-pat-tokens]]** — the **Active** switch or delete per row; effective from the next request.

Nothing revokes every credential of both kinds at once, as Force sign out does for sessions; after a security incident the merchant clears each list.

## Worked example — API integration with a courier system

The merchant integrates with a courier API to auto-generate shipping labels:

1. **Owner opens [[settings-api-keys]] → Create API Key** and names it "Courier Integration X".
2. **The platform issues a token.** Owner copies it into the courier's integration form.
3. **The courier service calls JSON-API v2 with the key.** The key reaches every resource, not only orders, so it is given only to a trusted integration, one key per integration.
4. **Owner can revoke the key at any time** from [[settings-api-keys]]. Revocation is immediate.
5. The integration does NOT appear on [[settings-staff]] and does NOT count toward the Moderator seat cap.

## Why this design — separation of human and machine

Mixing human staff accounts with machine credentials would create three problems:

- **Cap pressure.** A merchant who wires up 8 integrations would burn 8 Moderator seats on the `administrators` plan-feature.
- **Audit confusion.** Email lifecycle notifications (`new_admin_account`, etc.) firing for every integration would drown out actual staff changes.
- **Permission-tree mismatch.** The Moderator tree follows admin-panel sections; a token needs resource-level access (e.g. `orders:read`).

## Related

- [[merchant-roles]] — hub.
- [[merchant-roles-moderator]] — the parallel human-staff model.
- [[merchant-roles-force-signout-2fa]] — explicit note that Force sign out does NOT touch API Keys or PATs.
- [[settings-api-keys]] — long-lived API Keys screen.
- [[settings-pat-tokens]] — PAT Tokens screen.
- [[api-key]] — API-Key entity.
- [[pat-token]] — PAT-Token entity.
- [[admin-graphql-api]] — sign-in and permissions on Admin GraphQL.
- [[json-api-v2]] — the API surface these credentials authenticate to.
- [[settings-hooks]] — webhook events (note: admin-account events don't have webhook coverage — only customer / order / product webhooks).

## Open Questions

None.
