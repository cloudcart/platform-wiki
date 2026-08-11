---
type: concept
nav_path: "Concept → JSON-API v2 → Pagination"
aliases: ["JSON-API v2 pagination", "page[number]", "page[size]", "JSON-API page meta", "JSON-API page links"]
tags: [api, json-api, pagination, integration, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, filtering & sorting, endpoints, status codes, webhooks, audit log, CORS & soft-delete, atomic operations).

# JSON-API v2 — Pagination

## Definition

Collection endpoints in JSON-API v2 are **always paginated** — there is no "fetch all in one call" option. Pagination is page-based (1-indexed) via `page[number]` and `page[size]` query parameters. Hard caps: `page[size]` between **1 and 100**; defaults `page[number] = 1` and `page[size] = 20`. Pagination metadata is returned under `meta.page`; pagination link blocks (`links.first`, `links.prev`, `links.next`, `links.last`) are emitted only when the request includes `X-Show-Links: 1`.

## Scope

- The `page[number]` + `page[size]` query parameters.
- Defaults and hard caps.
- The `meta.page` block in responses.
- The opt-in `links.*` blocks.
- The "always paginated" rule and its implication for exports.

Not covered:

- Filtering or sorting the paged collection — see [[json-api-filtering-sorting]].
- Sparse fieldsets / includes (which can change response size dramatically at large `page[size]`) — see [[json-api-filtering-sorting]].
- The CORS preflight quirk that affects browser-driven pagination loops — see [[json-api-cors-soft-delete]].
- Per-plan rate limits that throttle the export loop — see [[platform-rate-limits]].

## Contrasts

- **Page-based vs cursor-based** — JSON-API v2 uses page-based pagination only. There is no cursor-based scheme (`page[after]`, `page[before]`). Integrators paging through long-lived collections must accept that records may shift between page reads (a new product created mid-export would push subsequent pages one row).
- **Pagination is mandatory vs optional** — the API has **no** "give me everything" mode; pagination is always applied. To export an entire resource, integrators must loop until `meta.page.current-page == meta.page.last-page`.
- **Default `links.*` off vs `X-Show-Links: 1`** — the link blocks (`links.first`, `links.prev`, `links.next`, `links.last`) are off by default. Integrators that want JSON:API-compliant link traversal need the `X-Show-Links` header.

## How it works

### Query parameters

| Parameter | Default | Range | Notes |
|---|---|---|---|
| `page[number]` | `1` | `>= 1` | 1-indexed. Pages above `last-page` return an empty `data` array (200 OK, not 404). |
| `page[size]` | `20` | `1` to `100` | Outside the 1–100 range → **422 Unprocessable Entity** with a validation error pointing at `page[size]`. |

### Response meta

Every collection response includes a `meta.page` block:

```json
{
  "meta": {
    "page": {
      "current-page": 1,
      "per-page": 20,
      "from": 1,
      "to": 20,
      "total": 120,
      "last-page": 6
    }
  }
}
```

- `current-page` — the page that was actually returned.
- `per-page` — the `page[size]` used (clamped to 1–100).
- `from` / `to` — 1-indexed record positions in the FULL collection (useful for "showing records 41–60 of 120" UI hints).
- `total` — total record count across all pages.
- `last-page` — the highest valid `page[number]`. When `current-page == last-page`, the integrator has fetched the tail.

### Response links (opt-in)

When the request includes `X-Show-Links: 1`, the response also includes a top-level `links` block:

```json
{
  "links": {
    "first": "<host>/api/v2/products?page[number]=1&page[size]=20",
    "prev": "<host>/api/v2/products?page[number]=2&page[size]=20",
    "next": "<host>/api/v2/products?page[number]=4&page[size]=20",
    "last": "<host>/api/v2/products?page[number]=6&page[size]=20"
  }
}
```

`links.prev` is omitted on the first page; `links.next` is omitted on the last page. By default (without `X-Show-Links`), these are not in the response at all — see [[json-api-headers-envelope]] for the full header inventory.

### Exporting an entire collection

Because pagination is always applied, exporting a resource means iterating pages until the tail:

1. Request `page[number]=1`, read `meta.page.last-page`.
2. Request pages `2.. last-page` in sequence (or in parallel, respecting the per-plan rate limit on [[platform-rate-limits]]).
3. Concatenate the `data` arrays client-side.

For very large collections (hundreds of thousands of records), the page-based scheme has a known weakness: records added or removed mid-export shift subsequent pages. Integrators that need consistency should either (a) export during a low-traffic window, (b) sort by a stable monotonic field like `id ASC` and dedupe client-side, or (c) use the admin GraphQL endpoint where bulk operations exist (see [[json-api-v2]] for the contrast table).

### Pagination interaction with `filter[]`, `sort`, `include`, sparse fieldsets

- Filters and sorts are applied **before** pagination — `total` reflects the filtered count, not the resource's full row count.
- Includes are sideloaded **per page** — included resources are deduplicated within a single response, not across pages. The same `customer` could appear in `included` on page 1 AND page 2 if multiple orders on each page reference it.
- Sparse fieldsets do NOT change `page[size]` — they reduce payload per record, not the record count.

## Where it applies

- Every collection endpoint (`GET /api/v2/<resource>`) — without exception.
- The relationship endpoints `<resource>/{id}/<rel>` when `<rel>` is a `hasMany` — same pagination rules apply.
- The custom endpoint `GET /api/v2/order-status` is **NON-JSON:API** and does NOT paginate (see [[json-api-endpoints]]); it returns the full list of statuses in one shot.
- Bulk-generator custom endpoints (`POST /discount-codes/generate`, `POST /discount-codes-pro/generate`) do not paginate either — they return arrays of newly-generated codes in one response.

## Related

- [[json-api-v2]] — hub.
- [[platform-rate-limits]] — per-plan rate limits that throttle export loops.
- [[json-api-filtering-sorting]] — filters / sorts are applied before pagination.
- [[json-api-headers-envelope]] — `X-Show-Links` for `links.*` blocks.
- [[json-api-endpoints]] — the helper `order-status` endpoint that bypasses pagination.

## Open Questions

- **Cursor-based pagination** — not implemented. For very large collections with frequent inserts, cursors would avoid the shift-between-pages problem. Currently no platform plans to add this; integrators that need consistency rely on `id ASC` sort + client-side dedupe.
- **`page[size]` plan-tiered cap** — the cap is a flat 100 across all plans. A future enterprise tier might raise this; verify against the validator before assuming higher caps `(verify)`.
