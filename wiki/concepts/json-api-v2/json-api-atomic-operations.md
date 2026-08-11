---
type: concept
nav_path: "Concept → JSON-API v2 → Atomic Operations (not supported)"
aliases: ["JSON-API v2 Atomic Operations", "Atomic Operations extension", "Bulk operations JSON-API", "productsBulkCreate", "JSON-API bulk write", "Multi-resource transaction API"]
tags: [api, json-api, atomic-operations, bulk, integration, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, pagination, filtering & sorting, endpoints, status codes, webhooks, audit log, CORS & soft-delete).

# JSON-API v2 — Atomic Operations (NOT supported)

## Definition

The JSON:API **Atomic Operations** extension (`application/vnd.api+json;ext="https://jsonapi.org/ext/atomic"`) is **NOT** implemented on CloudCart's JSON-API v2. The platform supports only the standard **one-resource-per-request** semantics. Bulk operations require multiple sequential calls (subject to the per-plan rate limit on [[platform-rate-limits]]).

This page exists to make the gap explicit — integrators discovering JSON:API for the first time often look for the Atomic Operations extension before falling back to alternatives.

**Each individual write IS wrapped in a database transaction** by the framework, so if a single POST fails part-way through (e.g., a relationship target doesn't exist), the parent resource is rolled back. But this transaction does **NOT span multiple HTTP requests**.

## Scope

- The non-support of `application/vnd.api+json;ext="https://jsonapi.org/ext/atomic"`.
- The single-request transactional guarantee that DOES exist.
- The three alternative paths for bulk / atomic semantics:
  - Sequential JSON-API v2 calls (the default).
  - Admin GraphQL `productsBulkCreate` mutation.
  - The [[apps-csv-import]] flow.

Not covered:

- The standard one-resource POST / PATCH / DELETE semantics — see [[json-api-endpoints]].
- Status codes when sequential calls partially fail — see [[json-api-status-codes]].
- Rate limits that throttle sequential bulk loops — see [[platform-rate-limits]].

## Contrasts

- **Atomic Operations extension vs sequential calls** — the extension would let an integrator send multiple resource mutations in one HTTP request with all-or-nothing semantics. CloudCart does not implement this; the closest equivalent is sequential calls (no all-or-nothing guarantee).
- **Single-request transaction vs multi-request transaction** — the framework wraps each individual write in a DB transaction. A single POST that creates a product and links it to several relationship targets is atomic. But ten sequential POSTs across ten products are NOT atomic — if the fifth one fails, the first four are committed.
- **JSON-API v2 bulk vs admin GraphQL bulk** — JSON-API v2 has NO bulk-write surface. The admin GraphQL endpoint has `productsBulkCreate` + `bulkOperation` query / cancel mutation; that's the canonical path for catalog-scale imports.

## What's explicitly not supported

- **`PATCH /api/v2/operations` or similar atomic-ops endpoint** — does not exist.
- **`Content-Type: application/vnd.api+json;ext="https://jsonapi.org/ext/atomic"`** — sending this header on a body that follows the atomic-ops schema returns either **415 Unsupported Media Type** (because the bare media type without the `ext` parameter is expected) or a parse failure surfaced as **400 Bad Request** `(verify exact response)`.
- **Multi-resource transactions** — there is no way to atomically create a product AND its variants AND its images in one request and roll all of them back if any one fails. The integrator must orchestrate this client-side, accepting partial-write risk.

## What IS supported within a single request

The framework wraps each individual write in a DB transaction:

- A `POST /products` that includes relationships to `categories`, `property-options`, `vendor`, etc. either commits the entire product (with all relationships) OR rolls back if any relationship target validation fails. The integrator gets one 201 (success) or one 422 (validation failure) — never a partially-created product.
- A `PATCH /orders/{id}` that updates multiple attributes commits the diff atomically.
- A `DELETE /products/{id}` either soft-deletes or fails — the row is never half-deleted.

## Alternative paths for bulk semantics

Three options when an integrator needs more than single-resource writes:

### 1. Sequential JSON-API v2 calls (the default)

The integrator loops, calling `POST /products` once per product. Each call is its own HTTP round-trip and its own DB transaction. If call N fails, calls 1..N-1 are committed; the integrator must implement client-side rollback if all-or-nothing semantics are required.

Constraints:
- Per-plan rate limit caps requests/minute — see [[platform-rate-limits]].
- No depth limit on relationship sideloading per call — see [[json-api-filtering-sorting]].
- 429 backoff with `Retry-After: 60` on rate-limit overflow — see [[json-api-status-codes]].

### 2. Admin GraphQL `productsBulkCreate` mutation

The platform exposes a separate `productsBulkCreate` mutation on the admin GraphQL endpoint (`<host>/api/gql`). This is the **canonical path** for large catalog imports beyond the [[apps-csv-import]] wizard.

- Authentication: `Authorization: Bearer <PAT>` + `X-Site-Id` (NOT an API key) — see [[json-api-auth]] for the contrast and [[settings-pat-tokens]] for the PAT setup.
- Companion mutations: `bulkOperationCancel`, `bulkOperation` (query) — read / cancel in-flight bulk operations.
- Trade-off: GraphQL, not JSON:API; the integrator must build a separate request shape and consume different error semantics.

### 3. The [[apps-csv-import]] flow

For catalog-scale imports the merchant uploads a CSV through the admin UI, and the platform's import pipeline processes the file asynchronously. This is the merchant-facing equivalent of the GraphQL bulk path.

- Best for one-off migrations / initial catalog seeds.
- Not API-driven — the integrator can't trigger it from a script (the merchant runs it from the admin).
- Per-line error reporting on the upload result.

## Where it applies

- Catalog migrations — the integrator must pick one of the three paths. For ~thousands of products, the GraphQL `productsBulkCreate` mutation is the practical choice. For tens of products, sequential JSON-API v2 calls are simpler.
- ERP / inventory sync — sequential JSON-API v2 calls are the standard pattern; the per-call DB transaction is enough for the common cases.
- Order-status batch updates — sequential `PATCH /orders/{id}` calls; no batch endpoint exists.

## Related

- [[json-api-v2]] — hub.
- [[json-api-endpoints]] — single-resource write semantics that DO exist.
- [[json-api-status-codes]] — 415 / 400 on atomic-ops media type; 429 backoff on sequential-call rate limit.
- [[platform-rate-limits]] — per-plan rate limits that throttle sequential bulk loops.
- [[settings-pat-tokens]] — PAT auth for the admin GraphQL `productsBulkCreate` path.
- [[apps-csv-import]] — admin-UI bulk import flow.

## Open Questions

- **Atomic Operations roadmap** — JSON:API Atomic Operations extension is not on the platform. Merchants needing transactional multi-resource writes use the admin GraphQL endpoint OR multiple sequential calls. If a future version adds Atomic Operations support, this page should document the URL extension and per-resource constraints `(verify roadmap)`.
- **`Content-Type` response on atomic-ops media type** — currently unverified whether the platform returns 415 or 400 when an integrator sends the atomic-ops `ext` parameter. Worth nailing down for integrator error handling `(verify)`.
- **JSON-API v2 bulk-write parity with admin GraphQL** — the GraphQL `productsBulkCreate` mutation has no JSON-API v2 equivalent. A future `POST /api/v2/products/bulk` endpoint would close this gap `(verify roadmap)`.
