---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → API path"
route_name: api2.order-fulfillment
route_path: /api/v2/order-fulfillments
aliases: ["API waybill", "Fulfillment API", "Programmatic waybill", "JSON-API waybill", "External integration fulfillment", "createShippingWaybill", "getShippingWaybillPdf", "GraphQL waybill", "Waybill PDF via API"]
tags: [orders, shipping, waybill, api, json-api-v2, fulfillment, integration]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (generate flow, courier specifics, payer side, print PDF, remove/void, generic modal).

# Waybill — programmatic API path

## Purpose

External integrations (ERP exports, WMS systems, custom scripts) create / read / remove order fulfillments via the JSON-API v2 — without opening the UI's waybill modal. **Creating an `order-fulfillment` runs the same order-side cascade as a fulfilment (stock, status, emails) but does not create a courier waybill.** A real courier waybill and its label PDF are made through Admin GraphQL (below).

Fulfillments are the **single writable order sub-resource** on JSON-API v2. The shipping resource itself ([[api-order-shipping]]) is read-only and exposes the order's current shipping provider, side, cost, tracking number, and service name.

## Where to find it

Programmatic only — not a UI screen. See [[api-order-fulfillment]] for the JSON-API v2 reference. Authentication via [[settings-api-keys]] per [[json-api-v2]].

## What the merchant can do here

(For programmatic / integration use — not a UI surface. External tooling acts on behalf of the merchant.)

- POST `/api/v2/order-fulfillments` — create a fulfillment (the API equivalent of Generate waybill / Save).
- GET `/api/v2/order-fulfillments/{id}` — read a fulfillment.
- DELETE `/api/v2/order-fulfillments/{id}` — remove a fulfillment (the API equivalent of Remove waybill).
- GET `/api/v2/order-shippings/{id}` — read the order's current shipping state (READ-ONLY).

## Settings & fields

See [[api-order-fulfillment]] for the full attribute and relationship schema. Key writable attributes mirror the UI form:

- `shipping_date_expedition` / `shipping_date_delivery`
- `shipping_tracking_number` / `shipping_tracking_url` (255-char cap enforced)
- `notify_customer` (mirrors the UI Email-notification toggle)
- `products_ids[]` — explicit list of product IDs to include in this fulfillment

## Business rules

### Creating an `order-fulfillment` triggers the full cascade

The same side-effects fire as via the UI Generate flow per [[waybill-generate-flow]]:

- Order's `status_fulfillment` flips to `fulfilled`.
- **Stock decrements** for the shipped products. See [[inventory-decrement-timing]].
- **Invoice / receipt numbers may be generated** — see [[orders-invoice]] / [[orders-receipt]].
- **Pre-authorized payments auto-captured** for gateways supporting `captureAutomaticAuthorization` — see [[orders-payment-capture]].
- Customer fulfillment-notification email queues if `notify_customer = yes`.
- `order.updated` webhook fires per [[settings-hooks]].
- Discount-usage sync queues with a 10-second delay. See [[marketing-discounts-codes]].
- All downstream app listeners trigger (ERP exports, accounting integrations, warehouse routing, analytics events).
- History row written with `api2` namespace — see [[orders-history]].

### Same validation gauntlet applies

Identical checks to the UI per [[waybill-generate-flow]]:

- Archived-order block.
- Shipping-provider-required check.
- Non-digital-products-only filter.
- Stock-tracking check.
- Already-fulfilled rejection.
- 255-char tracking URL cap.

All enforced identically through the API.

### Courier-specific waybill generation is NOT directly exposed

The JSON-API v2 POST creates the platform-side fulfillment record only; no courier is called and no label exists afterwards. Courier waybills are created automatically only by [[apps-pick-and-pack]] and Glovo, which dispatch on their own events.

### Admin GraphQL: create a courier waybill and get its PDF

[[admin-graphql-api]] drives the courier itself (permission: orders):

- `shippingWaybillSchema(key, orderId)` — describes the waybill inputs that courier takes (`key` is the app key, e.g. `econt`, `dpdbulgaria`).
- `createShippingWaybill(key, orderId, input, autoFulfill = false)` — runs the courier's own waybill save, the same checks as the order page (e.g. an already fulfilled order is refused), and calls the courier. Returns success, message, tracking number, waybill id, delivery date, PDF link. With `autoFulfill` false the waybill is kept but the order is not marked fulfilled. Orders in BGN are refused: convert them to EUR first.
- `shippingPdfFormats(key)` — the print formats the courier offers, for the `type` below.
- `getShippingWaybillPdf(key, orderId, type)` — the label of an existing waybill, from the courier (DPD returns the PDF itself, base64; Econt a link to its hosted PDF). No new shipment is created; without a waybill it answers *"No waybill found for this order — cannot generate a PDF until a waybill is created."*
- `cancelShippingWaybill` and `shippingWaybillsBulkPrint` cancel one and print several.

### Remove via API behaves like UI Remove

DELETE `/api/v2/order-fulfillments/{id}` runs the same cascade as [[waybill-remove-void]]: deletes returns first, calls the courier's `cancelBillOfLading` (with the same swallowed-error semantics), removes the local fulfillment, restocks per [[inventory-restock]], recalculates order `status` per the same paid/pending rule.

### History rows tagged `api2`

When the fulfillment is created or removed via the API, the [[orders-history]] entry's namespace is `api2` (not the admin user's name). This is the marker that distinguishes API-initiated fulfillments from UI-initiated ones for support investigations.

### Useful for warehouse / WMS integrations

The typical integration pattern: the merchant's WMS scans a packed box → calls POST `/api/v2/order-fulfillments` with the tracking number from the courier app → the platform decrements stock, invoices, captures payment, emails the customer, and fires `order.updated`. The courier waybill itself is made beforehand, on the order page or through Admin GraphQL.

Apps that use this pattern include [[apps-pick-and-pack]] and other warehouse integrations — see their pages for the exact handoff sequence.

## Related

- [[orders-shipping-waybill]] — hub.
- [[api-order-fulfillment]] — JSON-API v2 resource reference (full schema).
- [[api-order-shipping]] — read-only JSON-API v2 resource (shipping state).
- [[admin-graphql-api]] — the GraphQL waybill operations.
- [[waybill-print-pdf]] — the print buttons in the admin.
- [[json-api-v2]] — API overview, authentication, side-effects principle.
- [[settings-api-keys]] — API authentication.
- [[settings-hooks]] — webhook event payload format.
- [[apps-pick-and-pack]] — WMS integration using this API path.
- [[orders-history]] — `api2`-namespaced history rows mark API-initiated fulfillments.
- [[order-processing-pipeline]] — the full status-transition pipeline (same side-effects whether triggered via UI or API).

## Open questions

None.
