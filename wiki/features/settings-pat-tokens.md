---
type: feature
nav_path: "Settings → PAT Tokens"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["PAT Tokens", "Personal Access Tokens", "CLI Tokens", "GraphQL tokens", "Личен достъп", "PAT", "CLI"]
tags: [settings, security, tokens, cli, graphql, developer, owner-only]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---

# PAT Tokens

## Purpose

A security screen where the **store owner** generates **Personal Access Tokens** (PATs) used to authenticate against the CloudCart CLI and the GraphQL Admin API. Unlike the store-level [[settings-api-keys]] (which authorise external integrations and are bound to the store as a whole, with no scope model), PAT tokens carry **per-resource scopes**, **optional expiration**, and an **optional IP allowlist** — so a token can be issued with the narrowest possible permissions for a specific CI pipeline, dev machine, or office subnet.

CloudCart's page-header summary: *"Manage Personal Access Tokens for CloudCart CLI or GraphQL authentication."*

**Owner-only.** Despite the per-user wording in the API path (`/account/cli-tokens`), only the store **owner** can list, create, view, edit, or revoke PAT tokens. Moderators and Administrators see no entry in the sidebar and get HTTP 403 on any direct API call — see [[settings-pat-tokens-permissions]] for the four-layer enforcement.

The full token value (`cc_pat_` + 64 random hex characters = 71 chars total) is revealed exactly **once** at creation. The platform stores only the SHA-256 hash, never the original value — see [[settings-pat-tokens-security]].

## Where to find it

Sidebar → Settings → **PAT Tokens** (under the Account section per the breadcrumb).

The page's breadcrumb reads "Settings → Account → PAT Tokens". The route is `/admin/settings/pat-tokens`. The header icon is the key icon.

## What the merchant can do here

- See the count of active tokens vs the per-store max — *"`<N>` of 10 tokens"* shown as a chip near the Create button.
- Click **Create Token** to open the create modal — disabled when at the cap (see [[settings-pat-tokens-create-flow]]).
- See the table of existing tokens with name, masked prefix, scopes, created / last-used / active toggle (see [[settings-pat-tokens-list-view]]).
- Click a row's name → open the **Edit** modal (preserves name / scopes / IPs / expiration; CANNOT mint a new value — to rotate, delete + recreate).
- Toggle a token's active status (POST `/{id}/toggle-status`).
- Delete a token (DELETE `/{id}`) — revokes it immediately.

If the merchant has no tokens yet, the empty state shows a Create button + the message *"Create your first token to start using the CloudCart CLI or GraphQL API"* — see [[settings-pat-tokens-list-view]].

## Sub-pages (in this cluster)

This screen is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[settings-pat-tokens-list-view]] — the list table (columns, masked prefix, status toggle, row delete, empty state, `meta.max_tokens` chip).
- [[settings-pat-tokens-create-flow]] — the right-side slide-out modal (`CliTokensCreateOrEdit`), section layout, one-shot success card, copy-to-clipboard behaviour, edit vs create differences.
- [[settings-pat-tokens-scopes]] — the `CliTokensScopeSelector` wizard (Read Only / Full Access / Custom Permissions), the full scope catalog, primary-vs-granular rules, resource → scope URL mapping at the gateway.
- [[settings-pat-tokens-restrictions]] — IP allowlist UX + validation (`CliTokensIpRestrictions`), CIDR / IPv6 support, the 20-IP-per-token cap, expiration date picker + "No expiration" toggle.
- [[settings-pat-tokens-security]] — token format (`cc_pat_<64-hex>`), SHA-256 hashing, masking (`cc_pat_<8-hex>` + 49 asterisks), one-shot revelation, brute-force resistance, `findByRawToken` validation path.
- [[settings-pat-tokens-permissions]] — owner-only enforcement at four layers (route middleware, controller method, Form Request `authorize`, service layer), 10-token-per-store cap, cascade delete with Moderator account removal.
- [[settings-pat-tokens-endpoints]] — REST endpoint catalogue, validation rules (Zod client-side + Form Request server-side), partial-update behaviour on PUT, `recordUsage` tracking semantics, toggle-status alias.

## Settings & fields (at-a-glance)

Most fields live in the create / edit modal — see [[settings-pat-tokens-create-flow]] for full UX and [[settings-pat-tokens-endpoints]] for validation rules.

| Field | Required | Where it lives | Aspect page |
|-------|----------|----------------|-------------|
| `name` | yes (1–100 chars) | Token Details | [[settings-pat-tokens-create-flow]] |
| `description` | no (≤ 500 chars) | Token Details | [[settings-pat-tokens-create-flow]] |
| `scopes` | yes (≥ 1) | Permissions tab | [[settings-pat-tokens-scopes]] |
| `allowed_ips` | no (≤ 20 entries, IPv4/IPv6/CIDR) | Advanced Settings | [[settings-pat-tokens-restrictions]] |
| `expires_at` | no (date `after:now`, or null) | Advanced Settings | [[settings-pat-tokens-restrictions]] |
| `active` | toggle | Row action | [[settings-pat-tokens-list-view]] |

Backend endpoints (full reference on [[settings-pat-tokens-endpoints]]):

- `GET /admin/api/core/account/cli-tokens` — list.
- `GET /admin/api/core/account/cli-tokens/scopes` — available scopes.
- `POST /admin/api/core/account/cli-tokens/` — create (returns full token value in `CliTokenCreateResponse` — ONCE).
- `PUT /admin/api/core/account/cli-tokens/{id}` — update (partial allowed).
- `DELETE /admin/api/core/account/cli-tokens/{id}` — revoke.
- `POST /admin/api/core/account/cli-tokens/{id}/toggle-status` — flip active flag.

## Business rules

The rules below are the headlines — each aspect page has the verified-against-backend detail.

- **Owner-only.** Only the store owner can list / create / edit / delete PAT tokens, enforced at four layers. Moderators see HTTP 403 with message *"Only store owners can manage CLI tokens"*. There is no permission row in [[settings-staff]] to delegate this. See [[settings-pat-tokens-permissions]].
- **One-shot revelation.** The full token value is shown exactly once, at creation. The platform stores only the SHA-256 hash — no decrypt path exists. Lost tokens are unrecoverable; merchants must delete + recreate. See [[settings-pat-tokens-security]].
- **10-token-per-store cap.** Hardcoded `meta.max_tokens = 10`. Since only the owner creates, the per-user cap is effectively a per-store cap. See [[settings-pat-tokens-permissions]].
- **Two scope tiers, mutually exclusive.** A token picks ONE of: a primary scope (`full-access` OR `read-only`), OR one-or-more granular scopes (`products`, `orders`, `customers`, `inventory`, `discounts`, `blog`, `settings`, `webhooks`, with `:read` variants for the first 6). Mixing primary + granular is rejected by the validator. See [[settings-pat-tokens-scopes]].
- **Token rejected when ANY of these is true:** revoked, inactive, expired, request IP not in `allowed_ips`, request requires a scope not held by the token. See [[settings-pat-tokens-restrictions]] + [[settings-pat-tokens-scopes]].
- **Active toggle is reversible; deletion is permanent.** Flipping `active=false` and back keeps the same token value working. Deleting removes the hash permanently — even recreating with the same name yields a different `cc_pat_` value.
- **No brute-force throttle at the PAT layer.** The only protection is (a) the API gateway's `60 req/min` default rate limit, and (b) 256 bits of token entropy. Leaked tokens have no auto-revocation; the merchant must manually delete. See [[settings-pat-tokens-security]].
- **Cascade on admin deletion.** When a Moderator account is deleted from [[settings-staff]], any PAT tokens they had created (legacy, before owner-only was enforced) are auto-removed. See [[settings-pat-tokens-permissions]].
- **`last_used_at` reflects only successful requests.** Failed auth (IP / scope mismatch) does NOT bump the timestamp — so the column is a reliable "is this token actively working" signal. See [[settings-pat-tokens-endpoints]].

## Related

- [[settings]] — parent hub.
- [[settings-api-keys]] — store-level API authentication; full-access tokens scoped to the store, no per-user, no scopes (different model — contrast with PAT tokens).
- [[settings-staff]] — admin / moderator permission tree. Note: there is NO permission row to delegate PAT creation; the gate is binary (owner vs everyone else).
- [[settings-hooks]] — webhooks use API keys (not PAT tokens) for outgoing authentication.
- [[settings-banned-ip]] — store-level IP blocklist; separate from per-token `allowed_ips`.
- [[api-key]] — entity page for store-level API keys.
- [[pat-token]] — entity page for Personal Access Tokens.
- [[staff-member]] — historically PAT tokens are owned by individual staff members; in practice only the owner can create.
- [[merchant-roles]] — permission scoping rules.

## Open questions

_None — all previously-flagged items resolved or distributed to sub-pages._
