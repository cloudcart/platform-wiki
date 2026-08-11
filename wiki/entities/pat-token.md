---
type: entity
aliases: ["Personal Access Token", "PAT", "PAT Token", "CLI Token", "GraphQL token", "Personal API token", "Личен достъп", "PAT токен"]
tags: [settings, security, tokens, cli, graphql, developer, entity]
created: 2026-05-21
updated: 2026-05-24
source_count: 0
---
# Personal Access Token

## Identity

A **Personal Access Token (PAT)** is a per-admin, scope-aware credential the merchant generates so the **CloudCart CLI** and the **GraphQL API** can authenticate as a specific admin user. It is bound to **one admin account**, carries **fine-grained scopes** (e.g., `orders:read`, `products`, `inventory`), supports an optional **expiration date** and **IP allowlist** (including CIDR ranges), and is **revealed exactly once** at creation — only a SHA-256 hash is stored, so the value is gone once the create modal closes. The merchant manages PATs from [[settings-pat-tokens]] (Sidebar → Settings → Account → PAT Tokens).

A PAT is intentionally **distinct from an [[api-key|API Key]]** — the screen contrasts the two so the merchant picks the right credential. API Keys are coarser (store-scoped, unscoped, plaintext-readable, used for webhook auth via the `X-CloudCart-ApiKey` header); PATs are finer (admin-scoped, scope-restricted, hash-stored, one-shot revealed). Reach for a PAT for least-privilege automation — a CI build that only reads orders gets `orders:read`.

## Aliases

- **Personal Access Token** / **PAT** / **PAT Token** — canonical terms in the sidebar and page header (*"Manage Personal Access Tokens for CloudCart CLI or GraphQL authentication."*).
- **CLI Token** — alternate label for the primary use case; backend endpoint `/admin/api/core/account/cli-tokens`.
- **GraphQL token** — used for PAT auth against `<store-host>/api/gql`.
- **Personal API token** — support-doc term distinguishing it from the store-level API Key.
- **Личен достъп** / **PAT токен** — Bulgarian terms in Settings → Account.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Token Name** (`name`) | Required free text, min 1, max 100 chars | Internal label, e.g., *"CI Pipeline"*. First list column. |
| **Description** (`description`) | Optional textarea, max 500 chars | Free-text note; documentation only. |
| **Token value** (`token`) | n/a — server-generated at create | A 71-character string of the form `cc_pat_` + 64 hex characters (256 bits of entropy). **Revealed exactly once** in the create modal's success state; only the SHA-256 hash is stored. |
| **Masked token prefix** | n/a — derived | Read-only badge: the `cc_pat_` prefix plus the first few hex characters — enough to identify, not reconstruct. |
| **Scopes** (`scopes`) | Required multi-select, ≥1 scope | Two **primary scopes** (`full-access` / `read-only`) are mutually exclusive global modes; **granular scopes** combine freely. See the scope catalog below. |
| **Active** | Toggle on each row | When OFF, the token is rejected at the API gateway. Reversible — flipping ON re-enables the same value. |
| **Expiration date** (`expires_at`) | Optional date in Advanced Settings | Token stops after this date. A **No expiration** toggle opts out. Recommended for CI / automation. |
| **IP restrictions** (`allowed_ips`) | Optional list of IPs / CIDR ranges in Advanced Settings | Only listed IPs are accepted; empty = no restriction. **CIDR supported** (e.g., `192.168.1.0/24`). |
| **Created at** | n/a — auto | Visible in the list. |
| **Last used at** (`last_used_at`) | n/a — auto, updated on every accepted request | Spots stale / dormant tokens. |
| **Last used IP** (`last_used_ip`) | n/a — auto, from the most recent successful auth | Supports IPv6; useful for forensics. |
| **Revoked at** | n/a — auto, set on delete | Distinguishes "never used" from "used and then revoked". |
| **Owning admin** (`admin_id`) | n/a — set to the creator | Tied to one admin account. When that admin is removed from [[settings-staff]], all their PATs are deleted. |

The per-admin maximum is **10 active tokens** (hardcoded, NOT plan-based). Since only the store **owner** can create PATs, this is effectively a **10-tokens-per-store** ceiling. Reaching the cap disables Create until a token is deleted.

### Scope catalog (NOT plan-dependent)

The scope list is fixed: 2 primary scopes (`full-access`, `read-only`) plus 14 granular scopes (`products`, `products:read`, `orders`, `orders:read`, `customers`, `customers:read`, `settings`, `settings:read`, `inventory`, `discounts`, `blog`, `blog:read`, `webhooks`, `webhooks:read`), fetched at `/admin/api/core/account/cli-tokens/scopes`. Every merchant sees every scope regardless of plan; the 10-token cap also does not vary by plan.

**Permission-tree downgrade does NOT auto-revoke tokens.** A token keeps working for its declared scopes after the issuing admin's permission tree is narrowed — scopes are validated against the static catalog at runtime, not the current permission tree. To revoke a downgraded admin's tokens, delete or deactivate them manually.

### Deactivate (Active OFF) vs delete

Deactivation flips the `active` flag and the token is immediately rejected — for request validation, identical to deletion. Differences: the audit row stays (re-enable later), and the slot still **counts against the 10-token cap**.

**Store-owner transfer deletes ALL PATs.** PATs are bound to the owner's admin record. If the owner is removed or owner-change moves to a new admin record, that admin's PATs are deleted — they do **NOT** migrate; the new owner must regenerate them.

### Rejection responses & related behavior

The validation endpoint returns `{valid: false, error: "<message>"}` with HTTP **200** (integrations check the JSON); the downstream gateway returns 401 / 403 to the caller. The two messages:

- *"Token is invalid or expired"* — not-found / expired / revoked / inactive.
- *"Access denied from this IP address"* — IP-allowlist mismatch.

`last_used_at` is written on **every** accepted request (no debouncing). No outgoing webhook fires on PAT create / revoke / toggle — [[settings-hooks]] lists no PAT events; these are admin-account-internal changes.

## Where it appears

- [[settings-pat-tokens]] — the master management screen (Sidebar → Settings → Account → PAT Tokens): create, edit, toggle Active, delete, bulk-delete. Shows the count chip *"`<N>` of `<max>` tokens"* and the scope / IP / expiration controls in the modal.
- [[settings-api-keys]] — the sibling credential screen; merchants compare API Key vs PAT here. The two screens mirror each other in layout.
- [[account-cc2fa]] — 2FA on the admin's account; recommended for any admin holding PATs, since a compromised password with no 2FA compromises every PAT they own.
- CloudCart CLI — uses the PAT as its bearer credential when calling the admin API.
- GraphQL endpoint at `<store-host>/api/gql` (POST or GET) — accepts the PAT via `Authorization: Bearer <token>` or `X-CloudCart-Token: <token>`. A playground UI at `<store-host>/api/gql/playground` is dev-only (`APP_DEBUG=true`).

## Related

### Related entities

- [[api-key]] — the store-level, plaintext, unscoped sibling credential. Use API Keys for webhooks and full-store integrations; use PATs for scoped per-admin CLI / GraphQL automation.
- [[webhook]] — outgoing webhooks authenticate with [[api-key|API Keys]] (NOT PATs) via the `X-CloudCart-ApiKey` header.
- [[staff-member]] — every PAT is owned by exactly one admin; PATs are deleted when the staff member is removed.
- [[admin-notification]] — PAT events (create / delete) may surface as admin notifications, depending on notification settings.

### Cross-cutting concepts

- [[merchant-roles]] — only the store **owner** can create PATs; Moderators and Administrators are rejected with *"Only store owners can create CLI tokens"*. Permission-tree grants restrict which scopes the owner can grant.
- [[plan-gates]] — the 10-token cap is hardcoded, not plan-based. The API gateway rate-limit is `60 req/min` per store.

### Settings & feature pages

- [[settings-staff]] — the staff / permission tree that determines who can create PATs (owner only) and which scopes are grantable.
- [[account-cc2fa-codes]] — backup codes for login when the authenticator is unavailable; recovering admin access also restores PAT management.

## Open Questions

No outstanding questions — all items resolved or removed.
