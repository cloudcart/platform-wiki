---
type: feature
nav_path: "Orders → Order details → Status → JSON-API v2"
route_name: api-orders.patch
route_path: /api/v2/orders/:id
aliases: ["Status PATCH API", "JSON-API v2 status change", "API order status update", "api2 history namespace"]
tags: [orders, status, api, json-api-v2]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders-status-change]]. See the hub for the other aspects (pill, transition rules, side effects, notification, fulfillment gate, bulk).

# Order status change — JSON-API v2

## Purpose

Order `status` can be PATCHed via **JSON-API v2** — integrators (custom apps, ERP connectors, automation tools) can drive status changes programmatically without touching the admin panel. The API runs the EXACT same pipeline as the admin breadcrumb pill ([[orders-status-change-pill]]): same hard transition gates, same full side-effect chain, same customer-notification gating. The only material difference is the source namespace recorded in the audit history (`api2`, rendered as "API" in [[orders-history]]).

This is the most-used JSON-API v2 write surface for order workflows — fulfilment integrations, ERP syncs, marketplace bridges, and custom store-management apps all rely on it.

## Where to find it

JSON-API v2 endpoint: `PATCH /api/v2/orders/:id` (see [[api-orders]] for the full resource shape, authentication, headers).

The request shape sets the `status` attribute on the orders resource:

```
PATCH /api/v2/orders/12345
{
  "data": {
    "type": "orders",
    "id": "12345",
    "attributes": {
      "status": "paid"
    }
  }
}
```

For authentication, pagination, error responses, and the JSON-API conventions, see [[json-api-v2]].

## What the merchant can do here

### PATCH `status` — same valid targets as the admin dropdown

The API exposes the SAME set of valid status targets as the admin dropdown (see [[orders-status-change-pill]]):

**Settable via API**:
- `pending`
- `paid`
- `authorized`
- `cancelled`
- `refunded`
- `completed`
- Custom statuses (merchant-defined in [[settings-statuses]] with type = `order`).

**NOT settable via API** (five gateway-driven statuses, owned by payment-provider integration):
- `chargebacked`
- `disputed`
- `timeouted`
- `failed`
- `voided`

The API returns a 422 validation error if the integrator attempts one of the five hidden statuses.

`abandoned` is likewise not settable — it is not a status at all, just a flag on the order, and a request for it is rejected as an invalid status.

### Every status PATCH sets the order's `manual` marker

A status change through JSON-API v2 permanently marks the order as manually managed. From then on the platform **stops recomputing the order's status from its payment rows** — gateway webhooks still update the payment, but no longer drag the order's status with them. Integrators driving status from an ERP get exactly that behaviour by design; integrators who expect the gateway to keep the order in sync afterwards will find it frozen. The status pill on the [[orders]] list does the same thing.

### PATCH `notify_customer` flag — control email gating per order

The `notify_customer` flag is PATCH-able via the same orders resource. Integrators can flip it OFF in a separate PATCH BEFORE the status PATCH to silence the customer email for that specific change, or flip it ON to ensure the email fires (subject to the status-change template's own active flag and the store-wide kill switch — see [[orders-status-change-notification]]).

### PATCH `note` — admin note

The admin `note` attribute is PATCH-able from the same endpoint. Editing the note does NOT trigger the status-change pipeline; it's a separate audit-log entry.

### Other order attributes are mostly READ-ONLY via API

Most order sub-resources are read-only via JSON-API v2. The integrator can PATCH `status` / `note` / `notify_customer` and create / edit `order-fulfillment` records (see [[api-order-fulfillment]]) — but rich admin-only actions (refund, capture, mark-paid via gateway, manual confirm, invoice / credit-note generation, address edit, line CRUD, discount add / delete, waybill generate / remove) are NOT exposed. See [[orders-details]] for the full set of admin-only flows.

## Settings & fields

The API consumes the SAME settings as the admin pill:

- [[settings-statuses]] — status taxonomy (rename / add custom).
- [[settings-cart]] — `order_status_for_quantity_decrease` (decrement timing, snapshotted per order at placement).
- [[marketing-omnichannel-mails-list]] — the status-change template's active flag + the store-wide `customer_email_notifications` kill switch.
- [[settings-hooks]] — `order.updated` webhook fires on every successful API PATCH.

## Business rules

### Same hard gates apply

The API runs the SAME validation as the admin pill (see [[orders-status-change-transition-rules]]):

- `Completed` requires `paid` **OR** `fulfilled` — either one is enough; only an order that is neither is refused.
- `Cancelled` requires NOT `paid` AND NOT `completed`.
- ANY status on an archived order is REJECTED.
- ANY status on a cancelled / refunded order carrying a return record or an issued credit number is REJECTED — the **reversal lock**. Only a `cancelled` ↔ `refunded` toggle is accepted.
- The authorised-amount check applies and runs FIRST: if the order's payment authorisation is smaller than the order total, **every** status change is refused, `cancelled` included.

Failed gates return JSON-API v2 422 responses with the same error messages the admin UI surfaces.

### Same side effects fire

The full side-effect chain runs identically (see [[orders-status-change-side-effects]]):

- Stock decrement / restore (per the order's snapshotted `order_status_for_quantity_decrease`).
- Invoice + receipt numbers issued.
- `order.updated` webhook per [[settings-hooks]], then the customer notification, then the two history rows.
- Discount-usage recount.
- Negative-status payment-authorization auto-release.
- Negative-status fulfillment auto-reset.
- Auto-created system return on `cancelled` / `refunded` of a committed sale — and the reversal lock that follows it.
- Paid + digital-products auto-fulfillment.
- Draft-flag strip on first non-Cancelled status.
- Auto-promotion to `completed` (if [[settings-cart]] `order_complete` is set and conditions are met) — applied before the event fires, so it is ONE webhook and ONE history row reading `completed`.

### History namespace = `api2` (rendered "API")

Audit-history entries written by API PATCH carry the `api2` source namespace. [[orders-history]] renders this as "API" — distinct from "Admin" (breadcrumb pill / bulk action) and "System" (automated triggers like banned-IP cancel). So the merchant can identify which status changes came from external integrations.

### No bulk endpoint — iterate one-by-one

There is NO JSON-API v2 bulk-status endpoint. Integrators must call `PATCH /api/v2/orders/:id` one order at a time. Each call is a separate transaction with its own side-effect chain — which means integrators get per-order error containment that the admin bulk action does NOT provide. See [[orders-status-change-bulk]].

For high-volume status updates, integrators should rate-limit per [[json-api-v2]] limits and batch their own retry / error-handling logic.

### Webhook idempotency required

`order.updated` fires on every successful API PATCH — receivers must be idempotent because retries are possible (network failures, gateway timeouts, integrator retry logic). The webhook payload includes the new status but does NOT include the previous status; receivers querying the order resource after webhook delivery may race against a follow-up status change.

### Plan-feature gating

The orders resource itself is gated by the same plan features as the admin orders pages (`orders_amount`, `orders_revenue`, `users_traffic`). API calls beyond the plan limits receive a 403. See [[plan-features]].

## Programmatic access

This page IS the programmatic-access surface. For the canonical resource documentation see [[api-orders]]; for the broader JSON-API v2 conventions (auth, pagination, error envelope, atomic operations) see [[json-api-v2]].

Related JSON-API v2 sub-resources for order management:

- [[api-order-fulfillment]] — fulfillment records (CREATE / PATCH allowed).
- [[api-order-payment]] — payment summary (READ-ONLY).
- [[api-order-shipping]] — shipping summary (READ-ONLY).
- [[api-order-products]] — line items (READ-ONLY).
- [[api-order-discount]] — order discounts (READ-ONLY).

## Related

- [[orders-status-change]] — hub.
- [[orders-status-change-pill]] — admin UI surface (same valid targets).
- [[orders-status-change-transition-rules]] — same hard gates apply.
- [[orders-status-change-side-effects]] — same side-effect chain.
- [[orders-status-change-notification]] — the same three notification switches.
- [[orders-status-change-fulfillment-gate]] — same fulfillment gating.
- [[orders-status-change-bulk]] — admin-only; API has no bulk endpoint.
- [[api-orders]] — canonical orders resource.
- [[json-api-v2]] — API overview.
- [[orders-history]] — `api2` source namespace surfaces here as "API".
- [[settings-hooks]] — `order.updated` webhook.
- [[plan-features]] — orders-resource plan-gate.

## Open questions

- Whether a future API release will support a partial-success bulk endpoint with per-order error containment `(verify — currently no bulk endpoint exists)`.
