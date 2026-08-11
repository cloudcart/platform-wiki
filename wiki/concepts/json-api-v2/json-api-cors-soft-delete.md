---
type: concept
nav_path: "Concept → JSON-API v2 → CORS and soft-delete"
aliases: ["JSON-API v2 CORS", "JSON-API v2 soft-delete", "CORS preflight quirk", "OPTIONS preflight 401", "Soft-delete returns 404", "Access-Control-Allow-Origin JSON-API"]
tags: [api, json-api, cors, soft-delete, browser, integration, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, pagination, filtering & sorting, endpoints, status codes, webhooks, audit log, atomic operations).

# JSON-API v2 — CORS and soft-delete behaviour

## Definition

Two cross-cutting behaviours that affect how integrators interact with the API:

1. **CORS is open by default.** The API is callable from any browser origin — the CORS middleware echoes the request's `Origin` header into `Access-Control-Allow-Origin` (or `*` when no Origin is provided). The allowed-headers list includes `X-CloudCart-ApiKey`, so browser-side integrations can authenticate directly. **Known preflight quirk:** `OPTIONS` requests still run through the authentication middleware, so a preflight without `X-CloudCart-ApiKey` returns 401.

2. **Soft-deletes return 404, not 410 Gone.** Resources using the platform's soft-delete trait (e.g., `products`) set `deleted_at` and are filtered out of future GET queries by a global scope. Subsequent reads return **404 Not Found** — there is no `410 Gone` semantic. Soft-deleted resources are **not restorable** through the public API.

## Scope

- The open CORS policy, allowed methods, allowed headers.
- The preflight `OPTIONS` quirk and the practical workarounds.
- The absence of `Access-Control-Allow-Credentials` (no cross-origin cookies).
- Soft-delete read semantics (404 after delete; no 410 Gone).
- Restoration path (CloudCart support, database-level).

Not covered:

- The `X-CloudCart-ApiKey` header itself — see [[json-api-auth]].
- The full request/response header inventory — see [[json-api-headers-envelope]].
- HTTP status code semantics — see [[json-api-status-codes]].

## Contrasts

- **Open CORS vs preflight blocked** — origins are unrestricted (echoes back any `Origin`), but the auth check still runs on preflight. Browser clients can either (a) avoid CORS preflight by using only simple requests, or (b) proxy through a server-side endpoint that injects the API key.
- **Soft-delete 404 vs hard-delete 404** — both return 404 to the API caller. The distinction is internal: soft-deleted rows can in principle be restored at the DB level by CloudCart support; hard-deleted rows are gone. (Orders use a status-flag approach instead of physical delete; discounts use soft-delete via the same trait.)
- **No 410 Gone vs 404 Not Found** — the API does not signal "this resource USED to exist". Integrators that need to distinguish "never existed" from "existed but deleted" cannot do so from the response.

## CORS — open by default, with a preflight quirk

The CORS middleware echoes the request's `Origin` header into `Access-Control-Allow-Origin` (or returns `*` when no `Origin` is provided). The allowed-headers list includes `X-CloudCart-ApiKey`, so browser-side integrations can authenticate with the API key directly.

### CORS response headers (always emitted)

| Header | Value |
|---|---|
| `Access-Control-Allow-Origin` | Echoes the request `Origin` header, or `*` if not provided |
| `Access-Control-Allow-Methods` | `GET, POST, PATCH, DELETE, OPTIONS` |
| `Access-Control-Allow-Headers` | `Content-Type, Accept, X-XSRF-TOKEN, Authorization, X-Requested-With, Application, X-CloudCart-ApiKey, Origin, Accept-Encoding, X-PINGOTHER` |

`Access-Control-Allow-Credentials` is **NOT** set — cookies cannot be passed cross-origin. Authentication is via the `X-CloudCart-ApiKey` header only.

### The preflight quirk

Preflight `OPTIONS` requests **still hit the authentication middleware**. If a browser-side client sends an `OPTIONS` preflight WITHOUT the `X-CloudCart-ApiKey` header (the default `fetch` behaviour — browsers don't attach custom request headers to preflight), the preflight will return **401 Unauthorized**.

Three workarounds for browser-side integrations:

1. **Use simple requests where possible** — a "simple" CORS request (GET / HEAD / POST with `Content-Type` set to `application/x-www-form-urlencoded`, `multipart/form-data`, or `text/plain`, and only "CORS-safelisted" headers) does NOT trigger preflight. Most JSON:API calls DO require preflight because of `Content-Type: application/vnd.api+json` and the `X-CloudCart-ApiKey` header.
2. **Proxy through a server-side endpoint** that injects the API key — the integrator's own backend forwards the call, so the browser never deals with preflight authentication directly. This is the canonical pattern for production browser apps.
3. **Cache the preflight result** — once the platform fixes the quirk OR the preflight succeeds, the browser caches it for the `Access-Control-Max-Age` window. The platform does not currently set `Access-Control-Max-Age` `(verify)`, so each preflight runs fresh.

The quirk most often surfaces during local-dev / Postman-style testing, when the developer forgets the auth header on the preflight. In production, the proxy-through-backend pattern sidesteps it entirely.

## Soft-deletes — return 404, not 410

Deleting a resource that uses the platform's soft-delete trait (e.g., `products`) sets the `deleted_at` timestamp; the row is filtered out of future GET queries by the global scope.

**Subsequent GETs return `404 Not Found`** — there is no `410 Gone` semantic. The API does not distinguish "never existed" from "existed but was deleted". Integrators that need this distinction must keep their own list of known-deleted IDs client-side.

**Soft-deleted resources are NOT restorable through the public API** — restoration requires CloudCart support to flip `deleted_at` back to `null` at the database layer. There is no `POST /products/{id}/restore` or similar mutation in JSON-API v2 (or, currently, in the admin GraphQL either) `(verify GraphQL parity)`.

### Hard-delete vs soft-delete behaviour

From the API's perspective, both look the same:

- **Soft-delete resources** (e.g., `products`, `discounts`): row stays in DB with `deleted_at` set; future GET → 404; restoration via support at DB level.
- **Hard-delete resources** (e.g., the `webhooks` resource): row removed from DB; future GET → 404; restoration impossible.
- **Orders** use a status-flag approach rather than physical delete — DELETE is blocked at the routing layer (see [[json-api-endpoints]]); cancellation goes through a status change on PATCH instead.

### Webhook firing on delete

Both soft and hard deletes fire the corresponding `<resource>.deleted` webhook — see [[json-api-webhooks-integration]]. Subscribers cannot tell from the event payload whether the row is soft-deleted-and-recoverable or hard-deleted-and-gone.

## Where it applies

- Every browser-side integration calling the API — the CORS policy + preflight quirk shape the architecture.
- Server-side integrations — CORS is irrelevant; the preflight quirk doesn't affect them.
- Catalog management — products are the most common soft-delete resource; merchants who soft-delete a SKU and then can't find it via API need to contact support for restoration.
- Webhook-subscriber design — `<resource>.deleted` fires the same regardless of soft vs hard delete.

## Related

- [[json-api-v2]] — hub.
- [[json-api-auth]] — the `X-CloudCart-ApiKey` header that the preflight quirk requires.
- [[json-api-headers-envelope]] — the full response-header inventory (the CORS headers are part of it).
- [[json-api-endpoints]] — DELETE blocked on `orders` (uses status change instead); PATCH blocked on `images`.
- [[json-api-status-codes]] — 404 returned both for "never existed" and "soft-deleted"; 401 returned by preflight without the auth header.
- [[json-api-webhooks-integration]] — `<resource>.deleted` event fires on both soft and hard delete.

## Open Questions

- **Preflight skip-auth** — letting `OPTIONS` requests bypass the auth check (per the CORS spec) would eliminate the quirk. Currently the workaround is server-side proxying or simple requests `(verify roadmap)`.
- **`Access-Control-Max-Age`** — not currently set; setting a reasonable cache window (e.g., 86400 seconds) would reduce preflight overhead for high-traffic browser apps `(verify)`.
- **410 Gone for soft-deleted** — distinguishing "never existed" from "soft-deleted" via 404 vs 410 would help integrator cleanup logic, but currently both return 404 `(verify)`.
- **Self-service restore** — restoring a soft-deleted row requires support intervention; a `POST /products/{id}/restore` would be useful for catalog merchants who soft-delete in error `(verify roadmap)`.
