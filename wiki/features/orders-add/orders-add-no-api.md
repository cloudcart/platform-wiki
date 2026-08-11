---
type: feature
nav_path: "Orders → + Add order → No JSON-API endpoint"
route_name: admin.orders.add
route_path: /admin/orders/add
aliases: ["No order create API", "Why orders cannot be POSTed", "Manual order vs API", "JSON-API v2 order create rationale", "Push orders into CloudCart"]
tags: [orders, manual, api, integration, rationale]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[orders-add]]. See the hub for the other aspects (wizard, customer, delivery methods, address handling, validation, draft state).

# Add order — no JSON-API endpoint for creation

## Purpose

A common integration question is *"how do I POST an order from my ERP / WMS / CRM into CloudCart?"* The answer is: **you can't, not directly.** This page documents the deliberate absence of a `POST /orders` endpoint in JSON-API v2, the two canonical entry points the platform requires order creation to flow through, and how integrations push orders into CloudCart in practice.

## Where to find it

This rationale applies to JSON-API v2 globally — see [[json-api-v2]] for the full API model. The only order-creation surfaces are:

- **Storefront checkout flow** — the customer-facing cart-to-order transition, see [[cart-vs-order-lifecycle]].
- **Admin-panel manual-order flow** — the side panel this hub documents (see [[orders-add-wizard]]).

The JSON-API v2 endpoint table is on [[api-orders]] for the read / limited-PATCH surface.

## What the merchant can do here

The merchant has no direct option here — this page documents constraints rather than UI affordances. The decision tree for an integration developer is:

| Goal | Approach |
|---|---|
| Sync existing orders into ERP / CRM / accounting | Use the JSON-API v2 read endpoints (see [[api-orders]]) plus the `order.*` webhooks (see [[settings-hooks]]). |
| **Push a new order INTO CloudCart from an external system** | Simulate the storefront checkout flow (most common pattern), OR hand the merchant a checkout link via the existing checkout-resume mechanism, OR have a staff member create it manually via the [[orders-add]] flow. |
| Update an existing order's status / fulfilment / tracking | Use the limited-PATCH endpoints on [[api-orders]]. |

## Settings & fields

Not applicable — this page describes an absent endpoint, not configurable behaviour.

## Business rules

### Orders cannot be POSTed through JSON-API v2 (verified)

There is **no JSON-API v2 endpoint for creating orders**. The API exposes orders as **read-and-limited-PATCH** (see [[api-orders]]) — useful for syncing existing orders into ERP / CRM / accounting tools, but not for creating them.

### The two canonical order-creation entry points

Order creation happens through exactly two flows:

1. **Storefront checkout flow** — the customer-facing cart-to-order transition (see [[cart-vs-order-lifecycle]]).
2. **Admin-panel manual-order flow** — this hub's flow (see [[orders-add-wizard]]).

Both flows touch the same set of invariants: customer resolution, address validation, courier office lookup, tax matching, geolocation capture, stock checks, draft-mode flagging.

### The rationale (verified)

Order creation is a complex, side-effect-heavy operation. The platform requires it to flow through one of the two canonical entry points so all invariants hold consistently:

- **Customer resolution** — the right Customer record (and Customer Group) is attached; new customers can be inline-created but never as a side effect of an order POST.
- **Address validation** — country / city / postcode are real; saved addresses are cloned not referenced.
- **Courier office lookup** — pickup-point IDs are validated against the courier's live API (see [[orders-add-validation-save]]).
- **Tax matching** — VAT rate is resolved against the address's country and any geo-zone overrides.
- **Geolocation capture** — admin / customer IP and MaxMind GeoIP fields are captured for analytics and fraud signals.
- **Stock checks** — products exist, are active, are sellable; per-Variant stock is the unit of decision (see [[inventory-tracking]]).
- **Draft-mode flagging** — manual orders are flagged `is_draft = 1` + `is_admin = true` so they're excluded from default list views and surfaced under "Created by admin" — see [[orders-add-draft-state]].

A generic `POST /orders` endpoint would have to re-implement every one of these guardrails, or expose merchants to inconsistent order state.

### What integrations actually do

To programmatically push orders into CloudCart from an external system, the integration typically:

- **Simulates the storefront checkout flow** — the integration drives a cart through to checkout-complete on behalf of the customer. This is the dominant pattern.
- **Hands the merchant a checkout link via the existing checkout-resume mechanism** — the integration builds a cart, generates a resume link, and emails / SMSes it to the customer. The customer clicks it and lands in the storefront checkout in a near-complete state.
- **Has a staff member create the order manually** — via the slide-in panel documented at [[orders-add-wizard]]. Suitable for low-volume / B2B / phone-order cases.

### Limited-PATCH on existing orders

Once an order exists (created via either canonical entry point), JSON-API v2 lets integrations update a constrained set of fields on it — status, fulfilment, tracking number, etc. See [[api-orders]] for the exposed surface and [[settings-hooks]] for the corresponding `order.updated` webhook semantics.

### See [[json-api-v2]] for the broader principle

The order-create gap is part of the larger JSON-API v2 design principle: the API exposes resources where the read / update model is well-defined and side-effects are bounded. Resources with complex creation pipelines (orders, certain financial records) deliberately exclude POST. See [[json-api-v2]] for the full rationale of what the API exposes and what it deliberately does not.

## Related

- [[orders-add]] — hub.
- [[orders-add-wizard]] — the admin-panel manual-order flow (canonical entry point #2).
- [[cart-vs-order-lifecycle]] — the storefront checkout flow (canonical entry point #1).
- [[api-orders]] — JSON-API v2 read + limited-PATCH endpoints for orders.
- [[json-api-v2]] — broader rationale on what the API exposes and what it doesn't.
- [[settings-hooks]] — `order.*` webhooks for read-side integrations.
- [[inventory-tracking]] — stock-check invariants that any order-creation path must respect.
- [[orders-add-draft-state]] — invariants the admin-panel flow sets on the draft order.

## Open questions

None.
