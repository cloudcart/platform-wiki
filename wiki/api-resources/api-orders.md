---
type: api-resource
resource_path: /api/v2/orders
http_methods: [GET, PATCH]
related_entity: order
related_features: [orders, orders-details, orders-status-change, orders-shipping-waybill, orders-archive, orders-add]
aliases: ["Orders API", "JSON-API v2 orders", "API поръчки", "/orders", "/api/v2/orders"]
tags: [api, json-api-v2, orders]
plan_gates: []
created: 2026-05-26
updated: 2026-06-10
source_count: 5
---
# Orders (JSON-API v2)

## Purpose

The `orders` resource is the public, programmatic view of every order on the merchant's store. External integrations — ERP systems, fulfillment back-offices, accounting platforms, custom dashboards — use it to **pull orders for processing**, **change status / write USN / set invoice metadata from an outside system**, and **read the full order envelope** (line items, payment, shipping, addresses) for downstream reconciliation. The endpoint is the JSON-API counterpart of the admin-panel orders list ([[orders]]) and order detail view ([[orders-details]]).

Two structural rules merchants and integrators must internalise: **orders cannot be CREATED via the API** (POST is blocked at the routing layer — orders are placed through storefront checkout or the admin-panel manual-order flow [[orders-add]]) and **orders cannot be DELETED via the API** (DELETE is blocked — cancellation goes through a status change; long-term cleanup goes through [[orders-archive]]). Everything else — listing, fetching, updating writable attributes, marking fulfilled, exporting through includes — is on the table.

## Sub-pages (in this cluster)

This resource is split into 3 aspect pages. Drill into the one that matches the question.

- [[api-orders-attributes]] — the full writable / read-only attribute tables, the `meta` sparse-field append, the relationship + allowed-include list, and the complete filtering / sorting / pagination reference.
- [[api-orders-side-effects]] — the status-transition cascade that fires on every PATCH (gates, auto-promotion, stock movement, emails, webhooks, audit log), the invoice / USN single-write semantics, the `/fulfill` custom action, the `/order-status` helper, and the full 422 / 405 failure catalogue.
- [[api-orders-examples]] — worked curl requests + JSON responses for GET / PATCH / fulfill / blocked verbs, and the end-to-end integration testing checklist.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/orders` | List orders with filter / sort / include / page. |
| `GET` | `/api/v2/orders/{id}` | Fetch a single order with all included relationships. |
| `PATCH` | `/api/v2/orders/{id}` | Update writable attributes (status, invoice_date, invoice_number, usn). |
| `PATCH` | `/api/v2/orders/{id}/fulfill` | Custom action — same validation pipeline as a regular PATCH but routed through the fulfillment hook. See [[api-orders-side-effects]] and [[api-order-fulfillment]]. |
| `GET` | `/api/v2/order-status` | Companion helper — flat list of all configured order statuses (built-ins + custom). NON-JSON:API shape: `{data: [{id, name, slug, status_type}, ...]}`. See [[api-orders-side-effects]]. |
| `POST` | `/api/v2/orders` | **Blocked — 405 Method Not Allowed.** Place orders via storefront checkout or [[orders-add]]. |
| `DELETE` | `/api/v2/orders/{id}` | **Blocked — 405 Method Not Allowed.** Use status change (cancel) or [[orders-archive]]. |

No app install or plan feature gates this resource — every store on every plan has the orders endpoint enabled by default. Standard JSON-API v2 auth applies (see [[json-api-v2]]).

For per-order sub-resources, see the dedicated pages: [[api-order-products]], [[api-order-products-options]], [[api-order-discount]], [[api-order-modification]], [[api-order-payment]], [[api-order-tax]], [[api-order-total]], [[api-order-shipping]], [[api-order-shipping-address]], [[api-order-billing-address]], [[api-order-fulfillment]].

## Attributes

PATCH writes only four attributes — `status`, `invoice_number`, `invoice_date`, `usn` — and POST is blocked entirely so no attribute is ever writable on create. Everything else (customer snapshot, currency, totals, fulfillment status, timestamps) is read-only on PATCH but returned by GET. The full writable / read-only tables, the GET-visible money + timestamp fields, and the `?append[orders]=meta` sparse-field rule live on [[api-orders-attributes]].

## Relationships

Nine relationships hang off an order: `products`, `discounts`, `modifications`, `totals`, `taxes` (hasMany) and `payment`, `shipping`, `shipping-address`, `billing-address` (hasOne). Allowed include paths and the nesting limit (`shipping.provider` is the deepest permitted) are documented on [[api-orders-attributes]]. Each relationship has its own sub-resource page (see *Endpoint* above).

## Filtering & sorting

Reads support the dedicated `filter[start_date]` / `filter[end_date]` date-range filters (rewritten to `date_added >= / <= ?`), `filter[geo_zone_id]` / `filter[geo_zone_name]`, and auto-merged exact-equality column filters. Sortable on `id`, `date_added`, `updated_at`, `date_archived`. Standard JSON:API pagination. Full reference + the no-comparison-operator rule: see [[api-orders-attributes]].

## Side effects

A PATCH that changes `status` runs the **same status-transition pipeline as the admin-panel status pill** — hard transition gates, auto-promotion to `completed`, payment-hold cancellation, stock movement, discount-usage recompute, customer emails, webhooks, and the `api2`-namespaced audit-log entry. Invoice number and USN are single-write (set once, then 422). Full catalogue: see [[api-orders-side-effects]] and [[order-processing-pipeline]].

## Equivalent UI

- [[orders]] — orders list (mirrors `GET /api/v2/orders` with merchant filters).
- [[orders-details]] — single-order detail view (mirrors `GET /api/v2/orders/{id}` with the standard set of includes).
- [[orders-status-change]] — status pill (mirrors `PATCH /api/v2/orders/{id}` with the `status` attribute).
- [[orders-add]] — manual order creation (admin-panel-only — the API cannot POST orders).
- [[orders-archive]] — archive flow (admin-panel-only — the API cannot DELETE orders).
- [[orders-shipping-waybill]] — waybill generation (the API surfaces the resulting fulfillment record via [[api-order-fulfillment]]).
- [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] — payment actions (no direct API counterpart; status-change side effects can drive some of these indirectly).

## Related

- [[json-api-v2]] — API hub (auth, headers, status codes, audit log conventions).
- [[order-processing-pipeline]] — the full side-effect catalogue for order writes.
- [[order-status-workflow]] — status transition rules and gates.
- [[cart-vs-order-lifecycle]] — when fields freeze (currency, customer snapshot).
- [[api-order-products]], [[api-order-products-options]], [[api-order-discount]], [[api-order-modification]], [[api-order-payment]], [[api-order-tax]], [[api-order-total]], [[api-order-shipping]], [[api-order-shipping-address]], [[api-order-billing-address]] — read-only sub-resources.
- [[api-order-fulfillment]] — the only writable order sub-resource.
- [[order]] — full order attribute entity reference.
- [[order-status]] — order-status entity (key set returned by `/api/v2/order-status`).
- [[orders-history]] — the merchant-visible audit log (records `api2` as the actor namespace for API writes).
- [[settings-hooks]] — webhook subscriptions fired by API writes.
- [[settings-api-keys]] — API-key management.
- [[platform-rate-limits]] — per-plan rate limits.

## Open questions

None at the hub level — see each aspect's own Open questions.
