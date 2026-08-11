---
type: entity
nav_path: "Entity → Shipping Status"
aliases: ["Shipping Status", "Fulfillment status", "Delivery status", "Dispatch status", "Статус на доставка", "Статус на изпълнение"]
tags: [entity, orders, shipping, statuses]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Shipping Status

## Identity

A **Shipping Status** is the value on every [[order|Order]] that tracks where the order is in the **fulfillment** lifecycle — has the merchant packed it? has the courier picked it up? has it been delivered? has it been returned? It's a separate dimension from the [[order-status|Order Status]] (which tracks the order overall) and the [[payment-status|Payment Status]] (which tracks the money). Together, the three statuses answer three different questions: Order Status = "where is this order in the workflow?", Payment Status = "where is the money?", and Shipping Status = "where is the package?".

Each [[order|Order]] carries exactly one Shipping Status at a time (the `status_fulfillment` field on the order). The platform defines a canonical set of values; transitions are driven by the merchant marking fulfillment from [[orders-details]], by the courier integration syncing back delivery confirmations, and by return / refund actions. The taxonomy is managed under [[settings-statuses]], where the merchant can rename labels, define customer-notification toggles per status, and layer custom shipping statuses on top of the canonical values.

This entity is documented across a hub (this page) + 3 aspect sub-pages. The Assistant should drill into the aspect that matches the question rather than read the whole cluster.

## Aliases

- **Shipping Status** — the canonical merchant-facing term in the admin UI.
- **Fulfillment status** — used interchangeably; the underlying field is `status_fulfillment`. Internal documentation and webhook payloads often use this name.
- **Delivery status** / **Dispatch status** — informal merchant phrasing.
- **Статус на доставка** / **Статус на изпълнение** — Bulgarian terms used interchangeably.

## Sub-pages (in this cluster)

- [[shipping-status-values]] — the 5 canonical enum values verbatim (`not_fulfilled`, `fulfilled`, `shipped`, `delivered`, `returned`), what each means and when it's set; the per-status configuration from [[settings-statuses]] (display label and custom sub-statuses that layer on the canonical value — a status carries no notification toggle); the manual-store subset.
- [[shipping-status-lifecycle]] — the positive flow (`not_fulfilled → fulfilled → shipped → delivered`) and the negative branch (`→ returned`); the transition-trigger table; why transitions are NOT strictly state-machine-enforced; manual stores vs courier-integrated stores; auto-fulfill on waybill issue; why `returned` is not terminal.
- [[shipping-status-side-effects]] — what a Shipping Status change drives downstream: the auto-completion rule (paid + fulfilled + `order_complete`), the two-email auto-completion case, customer notifications, the `order.updated` webhook, the discount uses-counter (`fulfilled` is counted), return-does-NOT-auto-refund, cancellation gating, and digital-only stores.

## Key Attributes

The Shipping Status is an **enum** — its value is one of a fixed set of canonical strings stored on the order's `status_fulfillment` field. The merchant does NOT create new canonical values, but can rename labels per-language and add custom sub-statuses that layer on top. The canonical values are:

`not_fulfilled`, `fulfilled`, `shipped`, `delivered`, `returned`.

The full per-value meaning table and the per-status configuration (labels, custom sub-statuses) live on [[shipping-status-values]]. The transition flows and triggers are on [[shipping-status-lifecycle]]. The downstream side-effects (auto-completion, notifications, webhook, discount-uses, return handling) are on [[shipping-status-side-effects]].

Each Order has exactly one Shipping Status (never null — defaults to `not_fulfilled` at creation). The three statuses move independently: the merchant cannot infer one from another. See [[shipping-status-side-effects]] for the independence examples and the auto-completion rule that ties Order, Payment, and Shipping status together.

## Where it appears

- [[order]] — every order carries a `status_fulfillment` value (the Shipping Status).
- [[settings-statuses]] — taxonomy management: labels per language, customer-notification toggles, custom sub-statuses — see [[shipping-status-values]].
- [[order-status-workflow]] — concept page on how Order, Payment, and Shipping statuses interact.
- [[orders-shipping-waybill]] — waybill issuance often transitions `not_fulfilled` → `fulfilled` — see [[shipping-status-lifecycle]].
- [[orders-details]] — the per-order edit hub where the merchant changes the Shipping Status manually.
- [[shipping-provider-mechanism]] — courier integration webhooks that auto-drive the Shipping Status through the lifecycle.

## Related

### Related entities

- [[order]] — every Order has exactly one Shipping Status.
- [[order-status]] — the separate "Order Status" dimension (`pending`, `paid`, `completed`, `cancelled`, etc.).
- [[payment-status]] — the separate "Payment Status" dimension (the money lifecycle).
- [[shipping-provider]] — the courier whose webhooks drive Shipping Status transitions for integrated stores.
- [[discount]] — counted-status rule for the discount uses-counter (default includes `fulfilled`).

### Cross-cutting concepts

- [[order-status-workflow]] — how Order Status, Payment Status, and Shipping Status interact (auto-completion rule, gating).
- [[notification-delivery]] — how a Shipping Status change becomes a customer email.
- [[shipping-provider-mechanism]] — courier integration that pushes Shipping Status updates from the courier's tracking system.

### Settings & feature pages

- [[settings-statuses]] — label management + customer-notification toggles.
- [[orders-shipping-waybill]] — waybill issuance and the link to fulfillment marking.
- [[settings-hooks]] — `order.updated` webhook fires on every Shipping Status change.

## Open Questions

No outstanding questions — all items resolved or distributed to the sub-pages.
