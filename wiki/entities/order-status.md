---
type: entity
nav_path: "Entity → Order Status"
aliases: ["Order Status", "Order state", "Order workflow status", "Order lifecycle status", "Status", "Status na poruchka", "Статус на поръчка", "Състояние на поръчка", "Работен статус"]
tags: [entity, orders, statuses, lifecycle]
created: 2026-05-21
updated: 2026-08-06
source_count: 5
---

# Order Status

## Identity

An **Order Status** is the enum value on every [[order|Order]] that tracks **where the order is in the workflow** — placed, paid, shipped, completed, cancelled, refunded, etc. It is the merchant's primary "what's happening with this order?" signal. The platform defines **11 canonical statuses** (4 positive + 7 negative) that drive nearly every downstream rule — revenue reports, stock decrement, discount-uses counting, action-button availability, accounting-document issuance, customer notification, and webhook fan-out. The merchant can additionally **add custom statuses** via [[settings-statuses]] (Orders tab) and **rename built-in labels** for store-specific terminology, but the underlying 11 codes remain stable across all stores.

Order Status is **distinct from** [[payment-status]] (which tracks the money — 13 separate enum values) and from [[shipping-status]] (which tracks fulfillment — 2 values: `not_fulfilled` / `fulfilled`). Together, the three statuses answer three different questions: Order Status = "where is this order in the workflow?", Payment Status = "where is the money?", and Shipping Status = "where is the package?". They move independently — an order can be `status = completed` while its payment is `refunded` (refund issued after marking the order completed). See [[order-status-workflow]] for the full interaction model.

This page is the **hub** for the Order Status entity. The substantive content lives in 5 aspect pages — drill into the one that matches the question.

## Aliases

- **Order Status** — the canonical merchant-facing term in the admin UI.
- **Order state** / **Order workflow status** / **Order lifecycle status** — used interchangeably.
- **Status** — informal shorthand when context is clear.
- **Статус на поръчка** / **Състояние на поръчка** / **Работен статус** — Bulgarian equivalents.

The underlying field on the order is `status` (lowercase enum string). The shipping/fulfillment status is a separate field, `status_fulfillment` — sometimes informally called "Order status" by merchants who conflate them; the wiki keeps them strictly separate.

## Key Attributes

The 11 canonical values, draft sub-state, and pill colours live on [[order-status-entity-canonical-values]]. The detailed cross-cutting attributes split across the cluster:

### Sub-pages (in this cluster)

- [[order-status-entity-canonical-values]] — the 11 built-in values (4 positive + 7 negative), draft sub-state, status-pill colour coding, dropdown-vs-full-list distinction.
- [[order-status-entity-relationships]] — independence from [[payment-status]] / [[shipping-status]], action gates per status, what an Order Status drives downstream (history, notifications, stock, discounts, webhooks).
- [[order-status-entity-custom-statuses]] — merchant-added statuses layered on top, rename behaviour vs underlying code, `order-` slug rule, why customs DON'T trigger negative semantics.
- [[order-status-entity-side-effects]] — the firing order on every transition, auto-promotion to `completed`, hard gates that block transitions, bulk-operation semantics.
- [[order-status-entity-api-access]] — JSON-API v2 PATCH semantics, the 6 settable + 5 gateway-only split, webhook payload stability across renames, `order.created` / `order.updated` / `order.deleted` events.
- [[order-status-entity-edge-cases]] — negative-status shared rules (revenue exclusion, fulfillment auto-reset, payment auth release), the auto-created return and the reversal lock, `is_draft` meta clearing, stock-reversal skip for deleted products.

## Where it appears

- [[order]] — every order carries a `status` value (the Order Status).
- [[orders]] — the master list view; status filter + bulk "Mark as completed" action.
- [[orders-details]] — the per-order edit hub; the status pill in the breadcrumb lets the merchant change status. ~40 sub-actions check the current status.
- [[orders-status-change]] — the dedicated flow for single + bulk status changes.
- [[orders-history]] — per-order audit log; every status transition gets a row with prior + new values.
- [[settings-statuses]] — taxonomy management: rename built-ins, add / delete custom statuses. Notification settings do NOT live here — there is one status-change email template for all statuses, managed in [[marketing-omnichannel-mails-list]].
- [[order-status-workflow]] — concept page on how Order, Payment, and Shipping statuses interact (auto-completion rule, gating, side effects).
- [[orders-archive]] — archive / unarchive; archived orders are status-locked.
- [[orders-notify-customer]] — per-order toggle to suppress automated status-change emails.
- [[orders-credit]] — credit-note gate (status `cancelled` / `refunded` + invoice number).
- [[orders-invoice]] — invoice issuance surfaces the current status.
- [[settings-cart]] — `order_status_for_quantity_decrease` (stock-decrement trigger) and `order_complete` (auto-promotion toggle) settings.
- [[settings-banned-ip]] — auto-cancel rules acting on incoming orders' status.
- [[settings-admin-notifications]] — `order_status_change` / `order_payment_status_change` admin notifications.
- [[settings-hooks]] — `order.updated` webhook on every change.
- [[api-orders]] — JSON-API v2 endpoint for status PATCH.

## Related

### Related entities

- [[order]] — every Order has exactly one Order Status.
- [[payment-status]] — the separate enum tracking the money lifecycle (13 values, independent of Order Status).
- [[shipping-status]] — the separate enum tracking fulfillment (2+ values, independent).
- [[discount]] — counted-status rule (default `paid`, `completed`, `fulfilled`) for the discount uses-counter.
- [[invoice]] / [[credit-note]] — accounting documents whose issuance is gated by Order Status.

### Cross-cutting concepts

- [[order-status-workflow]] — how Order Status, Payment Status, and Shipping Status interact (auto-completion rule, gating, side effects, webhook fan-out).
- [[notification-delivery]] — how a status change becomes a customer email.
- [[checkout-flow]] — the storefront flow that produces the order's initial Order Status (`pending` for most providers, `authorized` for pre-auth).
- [[cart-vs-order-lifecycle]] — how a cart becomes an order in the first place.
- [[inventory-tracking]] — stock-decrement timing is driven by Order Status.
- [[marketing-discounts]] — discount uses-counter rules are status-driven.
- [[order-processing-pipeline]] — the full status-transition pipeline.
- [[json-api-v2]] — API overview.

## Open Questions

No outstanding questions — all items resolved or distributed to aspect pages.
