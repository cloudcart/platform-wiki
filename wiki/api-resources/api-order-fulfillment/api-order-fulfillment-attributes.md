---
type: api-resource
resource_path: /api/v2/order-fulfillment
http_methods: [GET, POST, PATCH]
related_entity: order
related_features: [orders-shipping-waybill, orders-details]
aliases: ["Order fulfillment API attributes", "order-fulfillment fields", "shipping_tracking_url", "shipping_tracking_number", "shipping_date_delivery", "shipping_date_expedition", "order-fulfillment relationships", "order-fulfillment filtering", "order-fulfillment sorting"]
tags: [api, json-api-v2, orders, fulfillment, waybill]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Order Fulfillment API — attributes & querying

> Part of [[api-order-fulfillment]]. See the hub for the other aspects (side effects & failure modes, examples & testing).

## Purpose

This aspect documents the **shape** of the `order-fulfillment` resource — which attributes are writable on POST / PATCH, which are read-only, the single `order` relationship, and the filter / sort / pagination reference for reads. Integrators building a "mark this order shipped, then amend the tracking later" flow start here: the writable set is small (tracking URL / number + two dates), and the line-item list is computed automatically (no partial-fulfillment field).

## Endpoint

These attributes are written through `POST /api/v2/order-fulfillment` (create) and amended through `PATCH /api/v2/order-fulfillment/{id}`, and returned by `GET /api/v2/order-fulfillment` (collection) and `GET /api/v2/order-fulfillment/{id}` (single). The full method table + guard rules live on the hub [[api-order-fulfillment]]; the write cascade lives on [[api-order-fulfillment-side-effects]]. Base URL, auth, headers: see [[json-api-v2]].

## Attributes

**Writable on POST and PATCH:**

| Attribute | Type | Required on POST? | Validation | Notes |
|---|---|---|---|---|
| `shipping_tracking_url` | string (URL) | optional | `url` rule | External tracking-page URL the customer / merchant can open to track the package. |
| `shipping_tracking_number` | string | optional | — | Courier-provided tracking number. The admin-panel waybill flow normally pulls this from the courier API; via the API it's accepted as-is. |
| `shipping_date_delivery` | date (`Y-m-d`) | optional | `date_format:Y-m-d` | Promised / estimated delivery date. |
| `shipping_date_expedition` | date (`Y-m-d`) | optional | `date_format:Y-m-d` | Date the package was dispatched. Defaults to today if not provided. |
| `order` (relationship) | hasOne | required (POST) | `HasOne` rule | The parent order to fulfill. Use the standard JSON:API `relationships` payload: `{"data":{"type":"orders","id":"<order-id>"}}`. |

After creation, most attributes are effectively read-only — a PATCH is typically used only to amend `shipping_tracking_url` / `shipping_tracking_number` / `shipping_date_delivery` / `shipping_date_expedition` once the dispatch is confirmed.

**Read-only** (returned by GET, rejected on POST and PATCH):

- `order_id` — set via the `order` relationship, never written directly.
- `shipping_provider` — derived from the order's chosen [[api-order-shipping]] (the provider name snapshot, e.g. `Econt`).
- `date_fulfilled` — stamped automatically by the platform on create.

**Auto-computed line-item list — no partial fulfillment.** The Adapter automatically computes the `products_ids` list (all line items on the order at fulfillment time) — there is **no API field for selecting a subset of line items**. A POST fulfills the **whole order at once**. Stores that need partial / multi-package fulfillment cannot express it through this endpoint (currently all-or-nothing).

**Sparse-field append values:** none configured.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | hasOne (route) / belongsTo (data) | order | Parent order. Required on POST. The route is registered as `hasOne` (matching the framework's relationship form), but the underlying model is `belongsTo` order. |

**Allowed include paths:** `order`.

There are no other relationships — `order-fulfillment` is a thin record hanging off a single [[order]]. The order's own line items, payment, shipping, and addresses are reached through the parent [[api-orders]] resource and its sub-resources, not through the fulfillment record.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column, e.g. `filter[order_id]=123`). There are no comparison operators (no `>=` / `<=` on dates here, unlike the parent [[api-orders]] resource).

**Allowed sort parameters:** `id`, `order_id`, `date_fulfilled`, `shipping_date_delivery`, `shipping_date_expedition`. Prefix with `-` for descending (e.g. `sort=-date_fulfilled`).

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

Worked GET examples (collection, scoped-to-one-order, single) live on [[api-order-fulfillment-examples]].

## Side effects

Reads (GET) have no side effects. The write side effects of POST / PATCH / DELETE — the 14-step shipment cascade, payment auto-capture, and the DELETE teardown — are documented in full on [[api-order-fulfillment-side-effects]]. Note one attribute-level effect worth flagging here: `shipping_date_expedition` **defaults to today** when omitted on POST, so a fulfillment created without it stamps the current date as the dispatch date.

## Equivalent UI

- [[orders-shipping-waybill]] — the admin-panel waybill form holds the same fields (tracking URL / number, expedition / delivery dates); the provider is taken from the order's shipping selection rather than typed.
- [[orders-details]] — single-order detail view where the fulfillment record (with these attributes) is displayed.

## Related

- [[api-order-fulfillment]] — hub.
- [[api-order-fulfillment-side-effects]] — the POST / DELETE cascade driven by these writes.
- [[api-order-fulfillment-examples]] — worked GET / POST / PATCH requests + responses.
- [[json-api-v2]] — API hub (auth, headers, pagination conventions).
- [[api-orders]] — parent order resource.
- [[api-order-shipping]] — order's shipping provider selection (the source of `shipping_provider`).
- [[order]] — full order entity reference.

## Open questions

- Confirm whether `products_ids` is ever exposed as a read-only GET attribute or remains entirely internal. `(verify)`
- Document whether a PATCH that changes `shipping_date_expedition` after creation re-stamps anything downstream (e.g. the history entry) or is a silent field update. `(verify)`
