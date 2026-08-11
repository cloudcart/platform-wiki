---
type: api-resource
resource_path: /api/v2/order-fulfillment
http_methods: [GET, POST, PATCH, DELETE]
related_entity: order
related_features: [orders-shipping-waybill, orders-details, orders-history]
aliases: ["Order fulfillment API", "Waybill API", "Mark fulfilled API", "JSON-API v2 order-fulfillment", "/order-fulfillment"]
tags: [api, json-api-v2, orders, fulfillment, waybill]
plan_gates: []
created: 2026-05-26
updated: 2026-06-10
source_count: 6
---
# Order Fulfillment (JSON-API v2)

## Purpose

The `order-fulfillment` resource is the **order's fulfillment record** — created when the merchant (or an external integration) ships the order, deleted when the merchant voids the shipment. This is the **only writable Order sub-resource** in JSON-API v2 and the API counterpart of the admin-panel **Save waybill** action on [[orders-shipping-waybill]].

External integrations use it to programmatically mark orders as fulfilled — typically a back-office ERP that books packages with the courier directly and then needs to tell CloudCart the order is shipped, with a tracking URL and dates. A successful POST runs the **same downstream cascade as the admin-panel waybill save**: invoice number generation, receipt number generation, inventory decrement, fulfillment-history entry, customer notification email, async webhooks, and (on gateways that support it) automatic payment-authorization capture. **Read [[api-order-fulfillment-side-effects]] carefully before integrating** — a single POST cascades through more than a dozen platform events, including real money movements.

## Sub-pages (in this cluster)

This resource is split into 3 aspect pages. Drill into the one that matches the question.

- [[api-order-fulfillment-attributes]] — the writable / read-only attribute tables, the single `order` relationship + allowed includes, the auto-computed line-item list (no partial fulfillment), and the filter / sort / pagination reference.
- [[api-order-fulfillment-side-effects]] — the 14-step POST shipment cascade (inventory, invoice / receipt, emails, webhooks, payment auto-capture), the DELETE teardown + courier-void note, and the full 422 / validation-guard catalogue.
- [[api-order-fulfillment-examples]] — worked curl requests + JSON responses for GET / POST / PATCH / DELETE, the integration testing checklist, and the integrator gotchas.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-fulfillment` | List every fulfillment row across every order on the store. |
| `GET` | `/api/v2/order-fulfillment/{id}` | Fetch a single fulfillment. |
| `POST` | `/api/v2/order-fulfillment` | Create a fulfillment on an order — marks the order as shipped and cascades side effects. |
| `PATCH` | `/api/v2/order-fulfillment/{id}` | Standard JSON:API update — accepted by the framework but most attributes are read-only after creation; typically used to amend `shipping_tracking_url` / `shipping_tracking_number` / `shipping_date_delivery` / `shipping_date_expedition`. |
| `DELETE` | `/api/v2/order-fulfillment/{id}` | Remove fulfillment — voids the courier dispatch (when a `bol_id` is present) and reverts the order to unfulfilled. |

No app install or plan feature gates this resource. The platform restricts POST: a validation hook checks `order.status_fulfillment == 'fulfilled'` and returns 422 *"This order is already fulfilled."* if so. Other [[order]] business rules — order archived, no shipping provider, no shippable (non-digital) products — block the underlying fulfillment-add call and surface as validation errors. Standard JSON-API v2 auth applies (see [[json-api-v2]]).

## Attributes

POST / PATCH write a small set — `shipping_tracking_url`, `shipping_tracking_number`, `shipping_date_delivery`, `shipping_date_expedition` — plus the required `order` relationship. `order_id`, `shipping_provider`, and `date_fulfilled` are read-only (returned by GET, set by the platform). The line-item list is **auto-computed** — there is no field to select a subset, so **partial fulfillment is not exposed**: a POST fulfills the whole order at once. Full tables: see [[api-order-fulfillment-attributes]].

## Relationships

One relationship: `order` (hasOne on the route, belongsTo on the model), required on POST. Allowed include path: `order`. Details on [[api-order-fulfillment-attributes]].

## Filtering & sorting

No resource-specific filters — only the framework's auto-merged exact-equality column filters (e.g. `filter[order_id]=123`). Sortable on `id`, `order_id`, `date_fulfilled`, `shipping_date_delivery`, `shipping_date_expedition` (prefix `-` for descending). Standard JSON:API pagination. Full reference: see [[api-order-fulfillment-attributes]].

## Side effects

A successful POST runs the **same fulfillment pipeline as the admin-panel Save waybill click** — order marked fulfilled, line items linked, inventory decremented, invoice + receipt numbers generated, audit entry written (`api2` → "API"), payment authorization auto-captured on supporting gateways (real money movement), then async webhooks + customer email. DELETE runs the inverse teardown and flips the order's status back to `paid` / `pending`. Unlike the admin flow, API POST does **NOT** call the courier — it records "already shipped" only. Full catalogue + DELETE teardown + 422 cases: see [[api-order-fulfillment-side-effects]] and [[order-processing-pipeline]].

## Equivalent UI

- [[orders-shipping-waybill]] — full admin-panel waybill flow (Generate / Save / Print / Remove / Update insurance / Change side). API POST corresponds specifically to the **Save** step; API DELETE corresponds to **Remove waybill**. Other admin actions (Print PDF, Update insurance, Change payer side) have **no API counterpart**.
- [[orders-details]] — single-order detail view where the fulfillment record appears.
- [[orders-history]] — audit-trail entries produced by POST / DELETE on this endpoint.

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (the custom `PATCH /orders/{id}/fulfill` route routes through this resource's validators).
- [[api-order-shipping]] — order's shipping provider selection (must be set before POST succeeds).
- [[api-order-shipping-address]] — recipient address (used implicitly by the admin-panel waybill flow, but not by API POST since it does not call the courier).
- [[api-shipping-providers]] — catalog shipping-provider definitions.
- [[order]] — full order entity reference.
- [[order-processing-pipeline]] — how fulfillment slots into the broader order lifecycle.
- [[inventory-tracking]] — stock-decrement side effect.
- [[background-queue-inventory]] — background-queue handling of the inventory side effect.
- [[orders-invoice]] — invoice number generation (one of the side effects).
- [[orders-notify-customer]] — customer email notification toggle.
- [[settings-hooks]] — webhook subscriptions fired post-commit.

## Open questions

None at the hub level — see each aspect's own Open questions.
