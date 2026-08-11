---
type: feature
nav_path: "Settings → PAT Tokens → Endpoints and validation"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["PAT endpoints", "CLI tokens REST", "CliTokenRequest", "CliTokenCreateResponse", "toggle-status alias", "recordUsage", "findByRawToken"]
tags: [settings, security, tokens, api, endpoints, validation, zod]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-pat-tokens]]. See the hub for related aspects (list view, create flow, scopes, restrictions, security, permissions).

# PAT Tokens — REST endpoints and validation

## Purpose

The full catalogue of REST endpoints behind the PAT Tokens screen, with client-side (Zod) and server-side (Form Request) validation rules. Also documents the partial-update behaviour on PUT, the `toggle-status` alias, and the precise authentication chain that gates every API call elsewhere on the platform.

## Where to find it

These endpoints back the Vue page at `/admin/settings/pat-tokens` — the merchant never invokes them directly through the UI. The page uses them all behind the scenes (see [[settings-pat-tokens-list-view]] and [[settings-pat-tokens-create-flow]] for which buttons map to which endpoints).

## What the merchant can do here

The endpoints exist to back the merchant-facing actions:

- **List tokens** for the page table — `GET /admin/api/core/account/cli-tokens`.
- **Fetch available scopes** for the scope-selector wizard — `GET /admin/api/core/account/cli-tokens/scopes`.
- **Open a single token** for Edit mode — `GET /admin/api/core/account/cli-tokens/{id}`.
- **Create a token** — `POST /admin/api/core/account/cli-tokens/`.
- **Update a token** (partial allowed) — `PUT /admin/api/core/account/cli-tokens/{id}`.
- **Revoke a token** — `DELETE /admin/api/core/account/cli-tokens/{id}`.
- **Flip the active flag** — `POST /admin/api/core/account/cli-tokens/{id}/toggle-status`.

## Settings & fields

### Endpoint catalogue

| Method | Path | Purpose | Owner-only? |
|--------|------|---------|-------------|
| `GET` | `/admin/api/core/account/cli-tokens` | List this owner's tokens | yes |
| `GET` | `/admin/api/core/account/cli-tokens/scopes` | List available scopes (catalog) | yes |
| `GET` | `/admin/api/core/account/cli-tokens/{id}` | Get single token (masked) | yes |
| `POST` | `/admin/api/core/account/cli-tokens/` | Create; returns full token value once | yes |
| `PUT` | `/admin/api/core/account/cli-tokens/{id}` | Update (partial allowed) | yes |
| `DELETE` | `/admin/api/core/account/cli-tokens/{id}` | Revoke; sets `revoked_at`, removes hash | yes |
| `POST` | `/admin/api/core/account/cli-tokens/{id}/toggle-status` | Flip `active` flag (alias for PUT with `active`) | yes |

Every endpoint is gated by the `isOwner` middleware + controller-level re-check + Form Request `authorize` + service-layer guard. See [[settings-pat-tokens-permissions]] for the four-layer enforcement detail.

### Create-modal validation (Zod, client-side)

| Field | Rule |
|-------|------|
| `name` | string, min 1, max 100 |
| `description` | string, max 500, nullable, optional |
| `scopes` | array of strings, min 1 |
| `allowed_ips` | array of strings, nullable, optional |
| `expires_at` | string (date), nullable, optional |

### Update-modal validation (Zod, slightly looser)

Same fields, plus:

- All fields become optional (partial update allowed).
- `active` boolean field added (for the toggle endpoint shared semantics).

### Server-side Form Request rules

In addition to mirroring the Zod schema, the server enforces:

- `expires_at` → `date|after:now`. Cannot create or update with a past date. Can be set to null to remove expiration.
- `allowed_ips` → max **20** entries; each entry must match IPv4 / IPv4-CIDR / IPv6 / IPv6-CIDR. *"Maximum of 20 IP addresses allowed"* error string.
- `scopes` → cannot mix primary (`full-access` / `read-only`) with granular scopes. Cannot include both `full-access` and `read-only`. See [[settings-pat-tokens-scopes]].

The Form Request's `authorize` returns false unless the caller is the store owner, so validation rules don't even run for non-owners — they get a 403 first.

### Create response shape (`CliTokenCreateResponse`)

The POST response includes the **full token value** ONCE — this is the only chance to capture it:

- `data.token` — the literal `cc_pat_<64-hex>` string (71 chars).
- `data.id` — the new record's ID.
- `data.name`, `data.scopes`, `data.allowed_ips`, `data.expires_at` — what the merchant submitted, echoed back.
- `data.token_prefix` — the 8-hex-char identifier used for masking in future list responses.

After this response, no endpoint returns the original value again. Subsequent GETs return only the masked form.

## Business rules

### Partial-update behaviour on PUT

The Update endpoint accepts any subset of: `name`, `description`, `scopes`, `allowed_ips`, `expires_at`, `active`. So a merchant can toggle just `active`, rename without touching scopes, re-set scopes without resetting IPs, or set `expires_at` to null to remove expiration. When `expires_at` is included as a non-null date, it must still pass `after:now`.

### Toggle-status is an alias

`POST /{id}/toggle-status` calls the same service method as PUT — reads the current `active` flag, flips it, updates. Functionally equivalent to `PUT {id}` with `active=true/false`. The endpoint exists for convenience in the row's switch UI on [[settings-pat-tokens-list-view]].

### Authentication chain (for other CloudCart endpoints authenticated by a PAT)

When ANY non-PAT-screen CloudCart admin endpoint is hit with a PAT token, the middleware runs:

1. **Format check** — `isValidTokenFormat` checks `cc_pat_` prefix and exactly 71 chars total. Malformed → rejected without DB hit.
2. **Hash lookup** — `findByRawToken` hashes the input (SHA-256) and looks up by `token_hash` with the `valid` scope (active=1, not revoked, not expired). Single indexed query.
3. **IP allowlist** — if `allowed_ips` is non-empty, the request's IP must match. Failure → HTTP 403 `IP_NOT_ALLOWED`.
4. **Scope check** — URL path mapped to required scope via `config('cli_scopes.resource_mapping')`. Failure → HTTP 403 `INSUFFICIENT_SCOPE`.
5. **`recordUsage`** — runs only when ALL prior checks pass. Updates `last_used_at` + `last_used_ip`, timestamps disabled to avoid bumping `updated_at`, wrapped in `retry(5, ..., 500)`.

### `recordUsage` runs ONLY on successful requests

When a token is valid by hash but the IP isn't allowed (or scope check fails), the middleware returns 403 — `recordUsage` is **NOT reached**. So `last_used_at` reflects SUCCESSFUL requests only. Failed attempts due to scope / IP do NOT update the timestamp. This makes "last used" a reliable proxy for "actively in use and working", not just "someone trying it".

### Format check before DB query

`isValidTokenFormat` rejects malformed tokens (wrong prefix or wrong length) **without hitting the database**. Only well-formed `cc_pat_<64-hex>` strings consume a hash lookup. Small optimisation that matters at gateway scale.

### Scope mapping uses `str_contains`

The middleware checks each mapping entry with `str_contains($path, $prefix)`; first match in insertion order wins. Unmapped prefixes default to `null` (no scope required) — a security gotcha documented on [[settings-pat-tokens-scopes]].

### No side effects on CRUD

CRUD on tokens is **synchronous**. No queue / no notifications fired. The next API request validates against the latest token state immediately — revoking via DELETE, toggling `active=false`, or changing scopes is effective on the next request. This matters for incident response: a leaked token can be revoked instantly with no propagation window.

### Cache + scope of side effects

No webhooks fire on token CRUD. No admin notifications are sent. The list updates immediately via in-page cache invalidation.

## Related

- [[settings-pat-tokens]] — hub.
- [[settings-pat-tokens-create-flow]] — modal that invokes POST + PUT.
- [[settings-pat-tokens-list-view]] — table that invokes GET, DELETE, toggle-status.
- [[settings-pat-tokens-scopes]] — scope catalog and the `/scopes` GET endpoint.
- [[settings-pat-tokens-restrictions]] — IP allowlist and expiration validation rules.
- [[settings-pat-tokens-security]] — the hashing model behind `findByRawToken` + `recordUsage`.
- [[settings-pat-tokens-permissions]] — four-layer owner-only enforcement.
- [[json-api-v2]] — separate JSON-API v2 surface authenticated by [[settings-api-keys]] (not PAT tokens) — contrast.

## Open questions

- Are there any audit-log entries written on token CRUD (create / update / delete), separate from `revoked_at`? `(verify)`
- Does the platform publish any webhook event when a token is created, revoked, or used from a new IP? Current understanding: no. `(verify)`
