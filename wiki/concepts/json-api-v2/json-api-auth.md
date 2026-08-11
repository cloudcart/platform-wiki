---
type: concept
nav_path: "Concept → JSON-API v2 → Authentication"
aliases: ["JSON-API v2 authentication", "X-CloudCart-ApiKey", "API key auth", "JSON-API auth headers", "/api/v2 authentication", "Host header tenant resolution"]
tags: [api, json-api, authentication, integration, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[json-api-v2]]. See the hub for the other aspects (headers/envelope, pagination, filtering & sorting, endpoints, status codes, webhooks, audit log, CORS & soft-delete, atomic operations).

# JSON-API v2 — Authentication

## Definition

JSON-API v2 authenticates every request with **two HTTP headers**: `X-CloudCart-ApiKey` (the merchant-generated API key, 64-character uppercase) and the standard `Host` header (which resolves the tenant store). There is **no `X-Site-Id`** — site identity is derived from `Host` only. API keys have **no scopes**: a valid active key grants full access to every resource the API exposes.

API keys themselves cannot be created or deleted via JSON-API v2 (chicken-and-egg). Lifecycle management runs through the **admin GraphQL endpoint** at `<store-host>/api/gql`, authenticated with a Personal Access Token — see [[settings-pat-tokens]] for the PAT setup and [[settings-api-keys]] for the admin UI equivalent.

## Scope

- The two required headers and their validation order.
- The failure-response envelope on 401 / 404.
- API-key lifecycle through admin GraphQL: `createApiKey`, `deleteApiKey`, `updateApiKey`, `toggleApiKeyStatus`.
- The practical bootstrapping workflow (PAT → API key → integration).

Not covered here:

- The full request/response header inventory (rate-limit, CORS, diagnostics) — see [[json-api-headers-envelope]].
- The HTTP status codes returned on auth failure — see [[json-api-status-codes]].
- CORS preflight quirk where `OPTIONS` still runs through auth — see [[json-api-cors-soft-delete]].

## Contrasts

- **JSON-API v2 auth vs admin GraphQL auth** — JSON-API v2 uses `X-CloudCart-ApiKey` + `Host`. Admin GraphQL uses `Authorization: Bearer <PAT>` + `X-Site-Id`. The two are independent credential systems.
- **API key vs Personal Access Token (PAT)** — the API key is for production integrations calling JSON-API v2; the PAT is for bootstrapping (creating the API key itself) and for admin-GraphQL automation. See [[pat-token]] for the token model.
- **Per-key scope vs per-store unrestricted** — every active API key on a store can call every endpoint. The only limitation is rotation discipline (one key per integration, deactivate on suspicion).

## How it works

### Required headers

| Header | Required | Notes |
|---|---|---|
| `Host` | yes | Identifies the tenant store. The platform looks up the store by exact hostname match against the merchant's primary domain and aliases. **There is no `X-Site-Id` header** — site identity is derived from `Host` only. |
| `X-CloudCart-ApiKey` | yes | The 64-character uppercase random API key the merchant generated under [[settings-api-keys]]. Must be active (not deactivated). |

### Validation order

The platform runs three checks in sequence — failure at any step short-circuits:

1. **`X-CloudCart-ApiKey` header present?** If missing or empty → **401 Unauthorized**.
2. **`Host` matches a known store?** If no store found for the hostname → **404 Not Found**.
3. **API key matches an active key on the resolved store?** If the key is missing from the store's `api_keys` table OR has `active = 0` → **401 Unauthorized**.

**No additional permission scope** beyond authentication — once an integrator has a valid API key for a store, **they can perform every operation on every resource the API exposes**. There is no per-key permission / scope / restriction. An API key is effectively "full admin rights via JSON-API v2".

### Failure response body (401 / 404)

```json
{
  "errors": [
    {
      "status": "401",
      "title": "Unauthenticated"
    }
  ]
}
```

`Content-Type: application/vnd.api+json` on every error response. No `WWW-Authenticate` header is returned (the API does not advertise the auth scheme).

### Managing API keys programmatically (admin GraphQL)

API-key lifecycle management runs through the admin GraphQL endpoint at `<store-host>/api/gql`, with admin-session OR PAT authentication (NOT an API key) and the `X-Site-Id: <site-id>` header.

#### Create a new API key

```graphql
mutation CreateApiKey($input: CreateApiKeyInput!) {
  createApiKey(input: $input) {
    id
    name
    description
    key
    active
    createdAt
  }
}
```

Variables:

```json
{
  "input": {
    "name": "Zapier integration",
    "description": "Read-only sync for monthly reporting"
  }
}
```

Input contract:

- `name` — **required**, max 191 chars. The merchant-facing label visible on [[settings-api-keys]]; must be unique among the store's API keys.
- `description` — optional, max 500 chars. Internal note for the merchant; never sent to integrations.

Response: the full `ApiKey` object including the newly-generated 64-character uppercase `key` value. **This is the only moment the `key` field is returned in full** through normal admin flows — store it client-side immediately. Subsequent reads through the admin panel show only the truncated display (first 30 chars + `...`).

Side-effects on success:
- The new key is created with `active = true` by default.
- The merchant's `api_keys_count` plan-feature counter (if defined) consumes one slot.
- No webhook fires for API-key creation.

#### Delete an API key

```graphql
mutation DeleteApiKey($id: ID!) {
  deleteApiKey(id: $id)
}
```

Returns `Boolean!` — `true` on successful delete.

Side-effects on success:
- The key is **hard-deleted** from the `api_keys` table — there is no soft-delete / restore path.
- Any integration still calling `/api/v2/*` with that key starts returning **401 Unauthorized** on the next request.
- Webhooks created under this key (the `Hook → ApiKey` relationship) may be affected — verify on [[settings-hooks]] before deleting if the key has any active hook subscriptions.
- **In-flight requests at the moment of delete** complete normally (the auth check passes before the delete commits); only requests AFTER the delete fail.

#### Companion mutations (full lifecycle)

| Operation | Mutation signature |
|---|---|
| Update name / description | `updateApiKey(id: ID!, input: UpdateApiKeyInput!): ApiKey!` — both `name` and `description` are optional in `UpdateApiKeyInput`; max lengths same as Create. The `key` value itself is **immutable** — no GraphQL field accepts rewriting it. |
| Activate / deactivate | `toggleApiKeyStatus(id: ID!, active: Boolean!): ApiKey!` — flip without deleting; deactivated keys return 401 the same way as deleted keys but the row stays for future re-activation. |

#### Auth contract for the GraphQL endpoint

- **URL:** `<store-host>/api/gql`; **Method:** `POST` with `Content-Type: application/json`.
- **Required headers:** `Authorization: Bearer <PAT-token>` (see [[settings-pat-tokens]]) OR admin session cookie; PLUS `X-Site-Id: <site-id>` (different from JSON-API v2 which uses the Host header).
- **Auth failure** returns GraphQL error response: HTTP 200 with `{ "errors": [{ "message": "Unauthenticated", "extensions": {...} }] }`.

### Practical bootstrapping workflow

1. **Merchant generates a PAT** under [[settings-pat-tokens]] (one-time setup).
2. **Integrator uses the PAT** to call `createApiKey` mutation → receives the 64-char `key`.
3. **Integrator stores the key** securely on their side.
4. **Integrator switches to using the API key** (`X-CloudCart-ApiKey` header) for all subsequent JSON-API v2 calls.
5. **PAT can be revoked** without affecting the API key — the PAT is only the bootstrapping credential.
6. **API key rotation:** the merchant creates a NEW key, updates the integration to use it, then deletes the OLD key. There is no "rotate in place" — the `key` value is immutable per row.

## Where it applies

- Every JSON-API v2 request (the auth middleware runs at the routing layer before any controller).
- The CORS preflight `OPTIONS` request — which is itself a known quirk; see [[json-api-cors-soft-delete]].
- The `Hook → ApiKey` relationship — webhooks created via JSON-API v2 are associated with the calling key.
- The audit log for products / variants — API writes capture the calling key's id + name (variants only; products capture only the request IP). See [[json-api-audit-log]].

## Related

- [[json-api-v2]] — hub.
- [[settings-api-keys]] — admin UI where merchants create / deactivate keys.
- [[settings-pat-tokens]] — PAT setup, required for GraphQL-based key lifecycle management.
- [[pat-token]] — the token model.
- [[settings-hooks]] — webhooks subscriptions; some are bound to the creating API key.

## Open Questions

- **Per-key scopes** — every API key is unrestricted across all resources. A future per-key scope mechanism would let merchants issue narrower keys (e.g., read-only for analytics integrations). Currently the only blast-radius limiter is rotation discipline.
- **Key rotation tooling** — there is no "rotate in place" — the `key` value is immutable per row. A native rotate-and-grace-period mechanism would simplify integrator key rolls.
