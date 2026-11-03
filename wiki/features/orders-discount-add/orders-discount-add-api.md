---
type: feature
nav_path: "Orders → Order details → Discount → Programmatic access"
route_name: admin.orders.discount.add
route_path: /admin/orders/action/discount/:order_id/add
aliases: ["Order discount API", "Programmatic discount", "Order discount JSON-API", "Why order discount is admin-only", "api-order-discount read-only"]
tags: [orders, discount, api, json-api-v2]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[orders-discount-add]]. See the hub for the other aspects (form fields, existing-discount eligibility, manual discounts, delete, recalculation).

# Order-level discount — programmatic access

## Purpose

Why **adding and removing order-level discounts is admin-panel-only**, and what the JSON-API v2 surface DOES expose for order discounts (read-only).

## Where to find it

The discount add / delete actions live only on the admin paths under [[orders-details]] ([[orders-discount-add-form]], [[orders-discount-add-delete]]). The API read surface is the [[api-order-discount]] resource on [[json-api-v2]].

## What the merchant can do here

- **Read** the order-discount record(s) attached to an order via [[api-order-discount]] — type, value, code, label, target type, and timestamps.
- The merchant CANNOT add a manual discount, apply an existing discount, remove a discount, or remove discount-related modifications via the API — all of those are admin-panel-only.

## Settings & fields

Order-level discounts are exposed as the **read-only** [[api-order-discount]] resource on JSON-API v2. `POST` / `PATCH` / `DELETE` return **405 Method Not Allowed** — there is no API mutation path. Discount application happens at storefront checkout (customer enters a code) or via the admin-panel [[orders-discount-add]] flow; removal happens via the admin-panel per-discount remove action.

## Business rules

### All eligibility + validation logic lives in admin code only

The rich filtering and validation around order-level discounts is admin-only:

- Customer-group match, `order_over` threshold, target-type filtering, code-less-discount exclusion ([[orders-discount-add-existing-eligibility]]).
- One-order-level-discount-at-a-time gate, archived-order block ([[orders-discount-add]]).
- Flat-discount-less-than-subtotal and percent-no-negative validation ([[orders-discount-add-manual]]).

None of this is reachable from the API.

### Discount application is coupled to the recalculation cascade

Applying or removing a discount is tightly coupled to the totals / tax / shipping / line re-pricing cascade, all of which happen in one DB transaction with the discount add / delete (see [[orders-discount-add-recalculation]]). The platform requires this flow to go through the validated admin paths so the cascade always runs.

### Programmatic discount management belongs at the rule level

If the merchant needs programmatic discount management, the integration typically operates at the [[marketing-discounts]] level — creating / configuring discount RULES — rather than attaching them per-order via JSON-API v2. The read-vs-mutate principle is covered on [[json-api-v2]].

## Related

- [[orders-discount-add]] — hub.
- [[api-order-discount]] — the read-only JSON-API v2 resource.
- [[json-api-v2]] — API overview (read-vs-mutate principle).
- [[api-order-total]] — totals are likewise GET-only; discounts cascade into them.
- [[marketing-discounts]] — rule-level discount management (the programmatic alternative).
- [[orders-discount-add-recalculation]] — the transaction the API would have to replicate.
- [[order]] — entity page.

## Open questions

None.
