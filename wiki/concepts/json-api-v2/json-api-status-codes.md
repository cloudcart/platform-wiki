---
type: concept
nav_path: "Concept → JSON-API v2 → HTTP status codes"
aliases: ["JSON-API v2 status codes", "JSON-API v2 errors", "HTTP 401 422 429 503 JSON-API", "JSON-API error envelope", "402 Payment Required", "406 Not Acceptable", "415 Unsupported Media Type"]
tags: [api, json-api, status-codes, errors, integration, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, pagination, filtering & sorting, endpoints, webhooks, audit log, CORS & soft-delete, atomic operations).

# JSON-API v2 — HTTP status codes

## Definition

JSON-API v2 returns a fixed set of HTTP statuses. Every non-2xx response carries the JSON:API **error envelope** — `{errors: [{status, title, detail?, source?}]}` — under `Content-Type: application/vnd.api+json`. Some statuses surface platform-specific semantics: **402** for plan expiry, **429** with `Retry-After: 60` for rate-limit, **503** when the merchant has enabled maintenance mode, and **422** as the catch-all wrapper for app-gated 404s (a framework quirk).

## Scope

- The full status code table — 200, 201, 204, 400, 401, 402, 403, 404, 405, 406, 415, 422, 429, 500, 503 — with the conditions that trigger each.
- The error envelope shape (verbatim).
- The known framework quirks: app-not-installed 404 wrapped as 422; 403 essentially never emitted (permissive no-op authorizer).
- The 500 response's `details` field carrying a log record ID for support.

Not covered:

- The exact request validation that triggers 422 — each resource page lists its own validators.
- Rate-limit per-plan numbers and the pack-purchase upgrade flow — see [[platform-rate-limits]].
- Auth-specific 401 vs 404 distinction — see [[json-api-auth]] for the three-step validation chain.

## Contrasts

- **2xx vs error response shape** — 2xx returns `{data: ...}`; everything else returns `{errors: [...]}`. The envelope is mutually exclusive at the top level.
- **402 (plan expired) vs 403 (forbidden)** — plan-feature overflows return 402 at the JSON-API layer. The 403 status documented for some discount feature-pack rejections lives at a DIFFERENT layer — the admin app, not JSON-API v2. Integrators calling JSON-API v2 should expect 402, not 403.
- **404 (resource not found) vs 422 wrapping 404 (app not installed)** — direct resource-not-found returns 404. App-gated resources requested without the app installed return **422 with a 404 inside** (framework quirk). Integrators must check both.
- **400 (malformed) vs 422 (validation failure)** — 400 means the request couldn't be parsed; 422 means it parsed but failed business validation.

## Status code table

| Status | When |
|---|---|
| **200 OK** | Successful GET (single or collection); successful PATCH that returns the updated resource; successful custom-action calls (`POST /discount-codes/generate`, `POST /discount-codes-pro/generate`, `PATCH /orders/{id}/fulfill`) |
| **201 Created** | Successful POST that creates a new resource. Response includes the created resource in the body AND a `Location` header pointing at the new resource's URL |
| **204 No Content** | Successful DELETE — no body returned |
| **400 Bad Request** | Malformed JSON body; malformed query parameters; invalid content-negotiation; unexpected type-mismatch errors caught at the controller layer |
| **401 Unauthorized** | Missing / invalid / inactive `X-CloudCart-ApiKey` header. Body: `{errors:[{status:"401",title:"Unauthenticated"}]}` — see [[json-api-auth]] |
| **402 Payment Required** | The merchant's plan is expired, past-due, or the trial has ended. Body: `{errors:[{status:"402",title:"Payment Required", detail:"..."}]}`. The exception is also persisted server-side for support diagnostics. |
| **403 Forbidden** | (Practically not emitted by this API — the framework's default authorizer is a permissive no-op. Plan-feature overflows return 402, not 403, at this layer; the 403 documented for some discount feature-pack rejections lives at a DIFFERENT layer — the admin app, not JSON-API v2.) |
| **404 Not Found** | Resource ID does not exist on the store; OR the `Host` header does not match a known store; OR an app-gated resource is requested while the app isn't installed (some app-not-installed paths return 422 with a 404 inside — framework quirk) |
| **405 Method Not Allowed** | The verb is blocked at the routing layer (e.g., POST on a read-only resource, POST/DELETE on `orders`, PATCH on `images`) — see [[json-api-endpoints]] for the full read-only list |
| **406 Not Acceptable** | The `Accept` header does not match `application/vnd.api+json` — see [[json-api-headers-envelope]] |
| **415 Unsupported Media Type** | The `Content-Type` header is not `application/vnd.api+json` on a body-carrying request (the only exception is `POST /discount-codes/generate`, which also accepts `application/json`) |
| **422 Unprocessable Entity** | Validation failures — required field missing, value out of range, relationship target doesn't exist, etc. The `errors[*].source.pointer` points to the failing field |
| **429 Too Many Requests** | Rate-limit exceeded for the store's domain. Body carries the rate-limit headers + `Retry-After: 60`. See [[platform-rate-limits]] for the per-plan caps. |
| **500 Internal Server Error** | Unhandled exception in the platform (database connection drop, etc.). When the platform's error logger captures the exception, the response body includes a `details` field with a log record ID that CloudCart support can look up |
| **503 Service Unavailable** | The merchant's store is in maintenance mode. Body: `{errors:[{status:"503",title:"Maintenance mode",detail:"Try again few minutes later"}]}` |

## Error envelope

Every non-2xx response uses this envelope:

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

- `status` — the HTTP status as a string (per JSON:API spec).
- `title` — short human-readable name.
- `detail` — long-form explanation (sometimes absent on 401 / 404).
- `source.pointer` — JSON Pointer to the failing field (present on validation errors).
- `source.parameter` — query-parameter name (present on filter / sort validation errors).

`Content-Type: application/vnd.api+json` on every error response. No `WWW-Authenticate` header is returned on 401 (the API does not advertise the auth scheme).

## Framework quirks worth knowing

- **App-not-installed returns 422 with a 404 inside.** App-gated resources (`product-options`, `stores`, `store-quantity`, `units`) wrap the 404 in a 422 envelope when the app isn't installed. Treat either 404 or "422 with `detail` mentioning app gating" as "app not available".
- **403 is essentially unreachable.** The default authorizer is a permissive no-op. Anything that would be 403 elsewhere surfaces as 401, 402, 404, or 422 here. Never branch integrator code on 403.
- **500 carries a support breadcrumb.** When the platform captures the exception, the body includes a `details` field with a log record ID — pass that ID to CloudCart support.
- **`Retry-After: 60` is only on 429.** Other transient failures (503, 500) do NOT include `Retry-After`. Integrators must hardcode their own policy for non-429 backoff.

## Common merchant-facing diagnostics

| Symptom | Likely cause |
|---|---|
| 401 on every request | Missing / wrong / deactivated `X-CloudCart-ApiKey` — see [[json-api-auth]]. |
| 404 on every request | `Host` header doesn't match the merchant's domain. |
| 415 on POST / PATCH | `Content-Type: application/vnd.api+json` missing. |
| 405 on POST to `orders` | Orders cannot be created via API by design — see [[json-api-endpoints]] / [[orders-add]]. |
| 422 with no obvious field | Possibly the app-gating 404-wrapped-as-422 quirk. |
| 429 | Rate-limit exceeded — wait `Retry-After` or buy a pack ([[platform-rate-limits]]). |

## Where it applies

- Every JSON-API v2 response carries one of these statuses.
- The 503 response is triggered by [[settings-general|maintenance mode]] — integrators should poll-and-back-off when they see it.
- The 402 response is triggered by the merchant's plan-renewal failure — integrators should surface this in their UI (and notify the merchant) rather than retry.

## Related

- [[json-api-v2]] — hub.
- [[json-api-auth]] — 401 / 404 from the auth validation chain.
- [[json-api-headers-envelope]] — 406 / 415 from content negotiation.
- [[json-api-endpoints]] — 405 from read-only resources.
- [[platform-rate-limits]] — 429 per-plan caps and pack-purchase mechanism.

## Open Questions

- **Cleaner app-gating signal** — the 422-wrapping-404 quirk obscures missing-app from validation failure. A distinct status code (e.g., 423 Locked, or 404 with a typed error) would simplify integrator branching `(verify roadmap)`.
- **`Retry-After` on 503** — currently only emitted on 429. Adding it on 503 would let integrators back off cleanly during maintenance windows `(verify)`.
