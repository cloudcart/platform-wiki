---
type: feature
nav_path: "Settings → Api keys"
route_name: api_keys.settings
route_path: /admin/settings/api_keys
aliases: ["API keys", "API Keys", "REST API keys", "API ключове", "API token", "Достъп до API"]
tags: [settings, api-keys, developer, integration]
plan_gates: ["api_requests"]
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---

# Api keys

## Purpose

The screen where the merchant manages credentials for CloudCart's public REST API. Each **API key** is a long server-generated token that an external integration (Zapier, custom ERP, internal scripts, third-party app, etc.) uses to authenticate as the store when calling JSON-API v2 endpoints. From this screen the merchant creates, names, activates / deactivates, copies, and deletes keys. The page also surfaces the **Site ID**, the **API Base URL** (`<store-host>/api/v2`), and the current per-minute rate limit — the three pieces of information a developer needs to start consuming the API.

Authentication is store-wide: every key authenticates as the store, paired with the Site ID (header `X-CloudCart-ApiKey` — verify). There is no per-key scope / endpoint restriction.

This concept is split into 6 aspect pages — drill into the aspect that matches the question rather than reading every page.

## Where to find it

Sidebar → Settings → **Api keys**. Route: `/admin/settings/api_keys`. Header icon: key.

## Sub-pages (in this cluster)

- [[settings-api-keys-overview]] — list view, page header (Site ID badge, Add button), rate-limit banner, keys table (Name / Api key / Created / Last updated / Active / Remove), copy-to-clipboard cell, Active toggle wiring.
- [[settings-api-keys-create-edit-modal]] — Add / Edit modal fields (Name, API key read-only, Description), Zod + server validation (`required`, `max:50`, `unique:api_keys,name`, Description `max:191`), the misleading-but-intentional "Generate" label in Edit mode.
- [[settings-api-keys-rate-limits]] — per-plan caps (Baby Pack: none / Starter: 50 / CC Pro: 100 / CC Master: 150 req/min), edge enforcement, `429` response shape with `Retry-After: 60` + `X-RateLimit-*` headers, a platform-internal address bypass, up to 800 req/min custom raise.
- [[settings-api-keys-feature-packs]] — Upgrade button branching (`<PlanFeature>` modal vs generic plan panel), fixed vs dynamic-pricing packs, `enable_feature_pack` gating, stacking, immediate effect on next request.
- [[settings-api-keys-delete-protection]] — single delete (`DELETE /admin/api/core/settings/api-keys/{id}`) + bulk delete (`POST /admin/api/core/settings/api-keys/delete`), database-level reference protection against webhook references, stop-on-first-failure NOT all-or-nothing.
- [[settings-api-keys-security]] — plaintext storage, model-layer immutability of `key` value, cosmetic 30-char truncation, no per-key scopes, Active=OFF takes effect on next request, permission gate `hasApiPermission:settings,settings.api_keys`.

## What the merchant can do here

The full task list lives in [[settings-api-keys-overview]]. At a glance:

- See **Site ID** + **API Base URL** + current rate limit.
- **+ Add Api key** — generate a new key ([[settings-api-keys-create-edit-modal]]).
- Click row's **Name** to edit (Name + Description only — key value is immutable).
- Click the truncated **Api key** value to copy the full string to clipboard.
- Toggle **Active** to revoke / restore without losing the value ([[settings-api-keys-security]]).
- Remove single rows or bulk-delete ([[settings-api-keys-delete-protection]]).
- Click **Upgrade** in the rate-limit banner to buy capacity ([[settings-api-keys-feature-packs]]).

## Settings & fields

The hub does not list individual fields — they live on the aspect pages:

- **Page header + keys table** (Site ID badge, +Add button, rate-limit banner, table columns Name / Api key / Created / Last updated / Active / Remove, default sort `id DESC`) — see [[settings-api-keys-overview]].
- **Add / Edit modal** (Name with `required` + `max:50` + `unique:api_keys,name`; Description capped `max:191`; read-only key value in Edit mode) — see [[settings-api-keys-create-edit-modal]].
- **Rate-limit banner** (plan name + N req/min + API Base URL `<host>/api/v2` + Upgrade button gated by `meta.api_requests_feature_exists`) — see [[settings-api-keys-rate-limits]] + [[settings-api-keys-feature-packs]].
- **Permission tree** (`hasApiPermission:settings,settings.api_keys`) — configured at [[settings-staff]], not here. See [[settings-api-keys-security]].

## Business rules

The hub captures only the four merchant-visible consequences that drive most support tickets; full mechanics are on the aspect pages:

- **More keys ≠ more capacity.** Rate limit is per-domain (`sha1(domain)`), shared across ALL keys of the store. Caps: Baby Pack none / Starter 50 / CC Pro 100 / CC Master 150 req/min, enforced at the platform edge. See [[settings-api-keys-rate-limits]].
- **Key value is permanent + plaintext.** No in-place rotation (model layer reverts changes); no `bcrypt`/encryption at rest; truncation in the table is cosmetic only. Rotate = delete + create. See [[settings-api-keys-security]].
- **Delete is reference-protected.** A webhook referencing the key blocks deletion at the database layer. Bulk delete is stop-on-first-failure, NOT transactional. See [[settings-api-keys-delete-protection]].
- **Active=OFF is the safe revoke.** Takes effect on the next request (no token cache); in-flight requests complete; value is preserved for restore. See [[settings-api-keys-security]].

The CRUD path itself is synchronous — no background jobs, admin notifications, or webhooks fire on create / edit / delete / status-toggle.

## Scope

What this cluster covers:

- The list view + page chrome (Site ID, rate-limit banner, table).
- The Add / Edit modal (Name + Description; immutable key value).
- The per-plan + per-pack rate-limit model and its enforcement at the edge.
- Single and bulk delete with FK protection.
- Storage + immutability + permission semantics.

What it does NOT cover:

- The JSON-API v2 endpoints themselves (per-resource shape, includes, side effects) — see [[json-api-v2]] + the `wiki/api-resources/` cluster.
- Webhook configuration that consumes these keys — see [[settings-hooks]].
- Personal Access Tokens, the user-bound CLI/admin equivalent — see [[settings-pat-tokens]].
- The Moderator permission tree where `settings.api_keys` is granted — see [[settings-staff]].
- The full platform-edge rate-limit catalogue (storefront, bot policy, timeouts) — see [[platform-rate-limits]].

## Programmatic access

**API keys cannot be managed via the API itself.** There is no JSON-API v2 resource for create / list / edit / delete of API keys — by design, the credential surface is admin-panel-only. An integration cannot bootstrap its own credentials; the merchant must generate the key on this screen and hand the value to the integration out-of-band. See [[settings-api-keys-security]] for the rationale.

## Related

- [[settings]] — parent hub.
- [[settings-hooks]] — Webhooks. Webhooks use API keys for authentication; deletion is blocked by FK protection ([[settings-api-keys-delete-protection]]).
- [[settings-pat-tokens]] — Personal Access Tokens, the CLI/admin equivalent (user-bound, not store-bound).
- [[settings-staff]] — `settings.api_keys` permission grants.
- [[api-key]] — entity page.
- [[webhook]] — entity page.
- [[plan]] — the `api_requests` feature governs the rate limit.
- [[plan-features]] / [[plan-vs-feature-pack]] — feature-pack stacking model.
- [[plan-gates]] — three plan-restriction shapes.
- [[json-api-v2]] — auth, pagination, side-effects principle.
- [[platform-rate-limits]] — full platform-edge rate-limit reference.

## Open questions

None — the previously-flagged items have been distributed to the aspect pages (header name verification, custom-raise ceiling) and remain marked `(verify)` there.
