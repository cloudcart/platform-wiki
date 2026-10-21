---
type: entity
nav_path: "Entity → Shipping Status"
aliases: ["Shipping Status", "Fulfillment status", "Delivery status", "Dispatch status", "Статус на доставка", "Статус на изпълнение"]
tags: [entity, orders, shipping, statuses]
created: 2026-05-21
updated: 2026-10-21
source_count: 0
---
# Shipping Status

## Identity

A **Shipping Status** is the value on every [[order|Order]] that tracks where the order is in the **fulfillment** lifecycle — has the order been dispatched (fulfilled) or not? It's a separate dimension from the [[order-status|Order Status]] (which tracks the order overall) and the [[payment-status|Payment Status]] (which tracks the money). Together, the three statuses answer three different questions: Order Status = "where is this order in the workflow?", Payment Status = "where is the money?", and Shipping Status = "where is the package?".

Each [[order|Order]] carries exactly one Shipping Status at a time (the `status_fulfillment` field on the order). The platform defines two values, **Not fulfilled** and **Fulfilled**. Transitions are driven by the merchant fulfilling or un-fulfilling the order from [[orders-details]], by a courier integration marking the order fulfilled when its waybill is created, and automatically by cancellation / refund (which resets a fulfilled order) and by payment of an order with only digital products (which fulfils it). Under [[settings-statuses]] (Shipping tab) the merchant can only rename the two values.

This entity is documented across a hub (this page) + 3 aspect sub-pages. The Assistant should drill into the aspect that matches the question rather than read the whole cluster.

## Aliases

- **Shipping Status** — the canonical merchant-facing term in the admin UI.
- **Fulfillment status** — used interchangeably; the underlying field is `status_fulfillment`. Internal documentation and webhook payloads often use this name.
- **Delivery status** / **Dispatch status** — informal merchant phrasing.
- **Статус на доставка** / **Статус на изпълнение** — Bulgarian terms used interchangeably.

## Sub-pages (in this cluster)

- [[shipping-status-values]] — the 2 values verbatim (`not_fulfilled`, `fulfilled`), what each means and when it's set; why there are no *shipped*, *delivered* or *returned* statuses; the per-status configuration from [[settings-statuses]] (a new name only — no custom sub-statuses, no notification toggle).
- [[shipping-status-lifecycle]] — the two-value flow (`not_fulfilled ⇄ fulfilled`); the transition-trigger table; the gates on each move; what courier integrations do after the waybill (they never set a further shipping status); manual stores vs courier-integrated stores; auto-fulfill on waybill issue.
- [[shipping-status-side-effects]] — what a Shipping Status change drives downstream: the links between the three statuses, the auto-completion rule (paid + fulfilled + **Automatic completion of the order**, on by default) and why it sends no separate "completed" email, the customer's shipment email, the `order.updated` webhook, the discount uses-counter (`fulfilled` is counted), returns as a separate record, cancellation, and digital-only orders.

## Key Attributes

The Shipping Status is an **enum** — its value is one of two fixed values. The merchant does NOT create new values and cannot add sub-statuses; the only option is to rename each value. The values are:

`not_fulfilled`, `fulfilled`.

The full per-value meaning table and the per-status configuration (the rename) live on [[shipping-status-values]]. The transition flows and triggers are on [[shipping-status-lifecycle]]. The downstream side-effects (auto-completion, notifications, webhook, discount-uses, return handling) are on [[shipping-status-side-effects]].

Each Order has exactly one Shipping Status (never null — defaults to `not_fulfilled` at creation). The three statuses are separate dimensions — the merchant cannot infer one from another — but the platform links them in a few places (auto-completion, the reset on cancel / refund, un-fulfilling re-opening the order). See [[shipping-status-side-effects]] for the examples and the auto-completion rule that ties Order, Payment, and Shipping status together.

## Where it appears

- [[order]] — every order carries a `status_fulfillment` value (the Shipping Status).
- [[settings-statuses]] — the Shipping tab, where the merchant renames the two values — see [[shipping-status-values]].
- [[order-status-workflow]] — concept page on how Order, Payment, and Shipping statuses interact.
- [[orders-shipping-waybill]] — waybill issuance often transitions `not_fulfilled` → `fulfilled` — see [[shipping-status-lifecycle]].
- [[orders-details]] — the per-order edit hub where the merchant changes the Shipping Status manually.
- [[shipping-provider-mechanism]] — courier integrations, whose waybill marks the order fulfilled.

## Related

### Related entities

- [[order]] — every Order has exactly one Shipping Status.
- [[order-status]] — the separate "Order Status" dimension (`pending`, `paid`, `completed`, `cancelled`, etc.).
- [[payment-status]] — the separate "Payment Status" dimension (the money lifecycle).
- [[shipping-provider]] — the courier whose waybill marks the order fulfilled in integrated stores.
- [[discount]] — counted-status rule for the discount uses-counter (default includes `fulfilled`).

### Cross-cutting concepts

- [[order-status-workflow]] — how Order Status, Payment Status, and Shipping Status interact (auto-completion rule, gating).
- [[notification-delivery]] — how a Shipping Status change becomes a customer email.
- [[shipping-provider-mechanism]] — courier integration; it marks the order fulfilled on waybill issue but does not push later tracking events into the Shipping Status.

### Settings & feature pages

- [[settings-statuses]] — renaming the two values.
- [[orders-shipping-waybill]] — waybill issuance and the link to fulfillment marking.
- [[settings-hooks]] — `order.updated` webhook fires on every Shipping Status change.

## Open Questions

No outstanding questions — all items resolved or distributed to the sub-pages.
