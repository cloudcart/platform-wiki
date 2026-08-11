---
type: concept
nav_path: "Concept → JSON-API v2 → Headers and envelope"
aliases: ["JSON-API v2 headers", "JSON-API v2 envelope", "application/vnd.api+json", "X-Show-Links", "JSON-API request shape", "JSON-API response shape", "X-RateLimit headers"]
tags: [api, json-api, headers, envelope, integration, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, pagination, filtering & sorting, endpoints, status codes, webhooks, audit log, CORS & soft-delete, atomic operations).

# JSON-API v2 — Headers and envelope

## Definition

JSON-API v2 follows the **JSON:API 1.0 specification**. Every request body wraps its payload in a top-level `data` object; every response wraps its payload in `data` (success) or `errors` (failure). Content negotiation uses `application/vnd.api+json` (with `application/json` accepted only on `POST /discount-codes/generate`). Pagination metadata lives in `meta.page`; sideloaded resources live in `included`.

This page is the canonical inventory of every header an integrator should send or expect, plus the request/response envelope shapes.

## Scope

- Required and recommended request headers (full inventory).
- Response headers always returned (rate-limit, CORS, diagnostic).
- The standard JSON:API request shape for POST and PATCH.
- The standard JSON:API response shape for single resources and collections.
- The error envelope returned on every non-2xx status.
- The `X-Show-Links` opt-in for JSON:API `links.*` blocks.

Not covered:

- Authentication headers (`X-CloudCart-ApiKey`, `Host`) — see [[json-api-auth]].
- Concrete rate-limit values — see [[platform-rate-limits|Platform rate limits]]. This page covers header MEANING, not values.
- Status codes themselves — see [[json-api-status-codes]].
- CORS preflight quirk — see [[json-api-cors-soft-delete]].

## Contrasts

- **`Content-Type: application/vnd.api+json` vs `application/json`** — the API enforces the JSON:API media type on request bodies and returns **415 Unsupported Media Type** otherwise. The single documented exception is `POST /discount-codes/generate` which also accepts `application/json` (a deliberate relaxation for the bulk-generator).
- **Default off `links.*` vs `X-Show-Links: 1`** — to keep responses lean, JSON:API `links.self`, `links.related`, `links.first`, `links.next`, `links.prev`, `links.last` are omitted by default. Integrators that need link-driven traversal opt in via `X-Show-Links: 1`.
- **Single-resource response vs collection response** — single returns one object under `data`; collection returns an array under `data` plus `meta.page` pagination block.

## Required and recommended request headers (full inventory)

| Header | Required? | Value | When |
|---|---|---|---|
| `Host` | yes (HTTP-required anyway) | The store's primary domain or any alias | Always |
| `X-CloudCart-ApiKey` | yes | 64-char uppercase API key | Always — see [[json-api-auth]] |
| `Content-Type` | yes for POST / PATCH / DELETE with body | `application/vnd.api+json` | Bodies that contain a `data` envelope. Non-matching `Content-Type` returns **415 Unsupported Media Type**. The ONLY documented exception is `POST /discount-codes/generate` which also accepts `application/json`. |
| `Accept` | recommended | `application/vnd.api+json` | A mismatched `Accept` returns **406 Not Acceptable**. |
| `X-Show-Links` | optional | Any truthy value (e.g. `1`) | Enables JSON:API `links.self` / `links.related` blocks on every resource and relationship. Default OFF (omitted from the response) to keep payloads small. Turn ON when the integrator needs hyperlinks for crawling / discovery. |
| `Origin` | browser-side only | The calling browser's origin | Echoed into `Access-Control-Allow-Origin`. |

CloudCart does NOT enforce `User-Agent` restrictions, version-pinning headers, or any custom CSRF token for the API. There is no API-versioning header (the version is in the URL).

## Response headers (always returned)

| Header | Value / purpose |
|---|---|
| `Content-Type` | `application/vnd.api+json` |
| `x-powered-by` | `cloudcart.com` (platform diagnostic) |
| `x-cc-p` | Platform identifier (e.g. `google-cloud`, `hetzner-cloud`, `local`) — useful for support tickets |
| `x-cc-h` | Internal hostname of the responding server — useful for support tickets |
| `X-RateLimit-Limit` | The integrator's current per-minute cap (computed from plan + active feature packs). See [[platform-rate-limits]] for the cap values. |
| `X-RateLimit-Remaining` | Requests left in the current rate-limit window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |
| `X-RateLimit-Info` | Human-readable English message with the upgrade pointer (e.g., where to buy a pack) |
| `Retry-After` | `60` (seconds) — emitted ONLY on 429 responses |
| `Access-Control-Allow-Origin` | Echoes the request `Origin` header, or `*` if not provided |
| `Access-Control-Allow-Methods` | `GET, POST, PATCH, DELETE, OPTIONS` |
| `Access-Control-Allow-Headers` | `Content-Type, Accept, X-XSRF-TOKEN, Authorization, X-Requested-With, Application, X-CloudCart-ApiKey, Origin, Accept-Encoding, X-PINGOTHER` |

The API does NOT return: `ETag`, `Cache-Control`, `Last-Modified`, `X-Request-Id`, `X-Site-Id`, `X-Tenant`, or any other tracing / caching headers.

## Standard JSON:API request and response shapes

Bodies are always wrapped in a top-level `data` (success) or `errors` (failure) object.

**Request (POST to create a new resource):**

```json
{
  "data": {
    "type": "products",
    "attributes": {
      "name": "Test product",
      "price": 1999
    },
    "relationships": {
      "category": {
        "data": { "type": "categories", "id": "5" }
      },
      "property-options": {
        "data": [
          { "type": "property-options", "id": "1" },
          { "type": "property-options", "id": "2" }
        ]
      }
    }
  }
}
```

**Request (PATCH to update — `id` is REQUIRED in the payload AND in the URL):**

```json
{
  "data": {
    "type": "products",
    "id": "123",
    "attributes": { "price": 2499 }
  }
}
```

**Response — single resource (GET `/<resource>/{id}` or after successful POST/PATCH):**

```json
{
  "data": {
    "type": "orders",
    "id": "1001",
    "attributes": { "...": "..." },
    "relationships": {
      "products": {
        "data": [ { "type": "order-products", "id": "5001" } ]
      }
    }
  },
  "included": [ { "...included resources only when ?include= was sent..." } ],
  "jsonapi": { "version": "1.0" }
}
```

**Response — collection (GET `/<resource>`):**

```json
{
  "data": [ { "type": "...", "id": "1", "attributes": {} } ],
  "included": [],
  "meta": {
    "page": {
      "current-page": 1,
      "per-page": 20,
      "from": 1,
      "to": 20,
      "total": 120,
      "last-page": 6
    }
  },
  "jsonapi": { "version": "1.0" }
}
```

**Response — error (ALL non-2xx statuses):**

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "The name field is required",
      "source": { "pointer": "/data/attributes/name" }
    }
  ]
}
```

**Links blocks** (`links.first`, `links.next`, `links.prev`, `links.last`, `links.self`, `links.related`) are emitted **only when the request carries `X-Show-Links: 1`**. By default they are omitted to keep response sizes small. Integrators that need link-driven traversal should send the header.

## Base URL and URL pattern

- **Base URL:** `<store-host>/api/v2/`
- **Resource URL:** `<store-host>/api/v2/<resource>/` (collection) or `<store-host>/api/v2/<resource>/{id}` (single).
- **Relationship URLs:**
  - `<store-host>/api/v2/<resource>/{id}/<rel>` — full related resources.
  - `<store-host>/api/v2/<resource>/{id}/relationships/<rel>` — linkage only (`{data: [{type, id}, ...]}`).

The store host MUST be one of the merchant's registered domains (the primary domain OR any aliased domain in `sites_aliases`). The tenant store is identified solely by the `Host` HTTP header.

## Where it applies

- Every request and every response — these headers and envelope shapes are the contract surface for the entire API.
- Rate-limit headers (`X-RateLimit-*` and `Retry-After`) are particularly important for integrators throttling their own request rate — see [[platform-rate-limits]] for the actual per-plan numbers.
- The `Location` header on `201 Created` responses points at the new resource's URL — useful for crawlers and discovery agents.

## Related

- [[json-api-v2]] — hub.
- [[platform-rate-limits]] — per-plan rate-limit values and pack-purchase mechanism.
- [[settings-api-keys]] — where merchants generate the `X-CloudCart-ApiKey` value.

## Open Questions

- **Tracing headers** — the API does not return `X-Request-Id` or any correlation ID. For support tickets, the only diagnostic anchors are `x-cc-p` + `x-cc-h` (platform + host). A request-ID header would simplify correlation between integrator logs and platform logs.
