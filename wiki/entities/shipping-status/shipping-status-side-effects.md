---
type: entity
nav_path: "Entity → Shipping Status → Side-effects"
aliases: ["Shipping status side effects", "Fulfillment side effects", "Auto-completion rule", "Shipping status notifications", "Shipping status webhook", "Странични ефекти на статус на доставка"]
tags: [entity, orders, shipping, statuses]
created: 2026-06-10
updated: 2026-10-21
source_count: 0
---

> Part of [[shipping-status]]. See the hub for the other aspects (values, lifecycle).

# Shipping Status — side-effects

## Identity

This page documents **what a Shipping Status change drives downstream** — how it interacts with [[order-status|Order Status]] and [[payment-status|Payment Status]], when it triggers a customer email, when it fires a webhook, when it consumes a discount-uses slot, and the rules around return handling, cancellation, and digital-only orders. For the meaning of each value see [[shipping-status-values]]; for the transition flows see [[shipping-status-lifecycle]].

## Aliases

- "Shipping status side effects" / "Fulfillment side effects" — the downstream consequences of a fulfillment change.
- "Auto-completion rule" — paid + fulfilled + `order_complete` → `completed`.
- Bulgarian: "Странични ефекти на статус на доставка".

## Key Attributes

### Independent of Order Status and Payment Status

The three statuses are separate, but the platform links them in four places: a `paid` order that becomes fulfilled is completed automatically (when automatic completion is on — below); moving an order to a negative status (cancelled, refunded …) resets a fulfilled order to `not_fulfilled`; un-fulfilling an order moves its Order Status back to `paid` (when its last payment is completed) or `pending`; and an order with only digital products is fulfilled automatically when it becomes `paid`. Typical combinations:

- Order Status `paid`, Shipping Status `not_fulfilled` (paid but not yet packed — typical post-checkout state for many minutes to hours).
- Order Status `paid`, Shipping Status `fulfilled` (paid and dispatched — with automatic completion on, fulfilling a paid order normally turns it `completed` in the same save).
- Order Status `cancelled` / `refunded`, Shipping Status `not_fulfilled` (cancelling or refunding resets the shipping status).

### Auto-completion rule

The platform auto-promotes the Order Status to `completed` when ALL of the following hold simultaneously on a save:

- `status = paid` (Order Status)
- `status_fulfillment = fulfilled` (Shipping Status)
- The store setting **Automatic completion of the order** ([[settings-cart]]) is on — it is ON by default.

If the merchant turned it off, the order stays at `paid` + `fulfilled` until the merchant manually marks it `completed`. See [[order-status-workflow]].

### Auto-completion sends no separate "completed" email

When fulfilling a `paid` order completes it, the order becomes `completed` inside the same save, without a status-change event. The customer receives only the shipment email (if the order's Notify-customer flag is on); no "completed" status email and no status-history entry are produced for this completion — see [[order-status-auto-transitions]].

### Customer notification — per order, not per status

There is no per-status notification toggle for shipping statuses. When an order is fulfilled (any route — **Fulfill products**, a courier waybill, the status menu), the platform sends the customer the shipment email via [[notification-delivery|notification dispatch]] if the order's Notify-customer flag is on. Un-fulfilling sends no email.

Additionally, each order has a `notify_customer` flag — when OFF on the order, ALL automated customer emails (across all status types) are suppressed. The merchant uses this to silence a problematic order without changing global settings. See [[order]] business rules.

### Webhook on every change

Every Shipping Status change is a save on the order, which fires the platform-wide `order.updated` webhook to [[settings-hooks]] subscribers. The payload includes `status_fulfillment` (the new value) as a top-level field on the Order snapshot. There is **no separate "old value" field** — subscribers wanting to detect transitions must compare against their own prior snapshot. The platform does **not** emit a separate `shipping.status.changed` event.

### Discount uses-counter and fulfillment

The `discounts_used_statuses` setting (default: `paid`, `completed`, `fulfilled`) drives whether a [[discount|Discount]] applied to the order consumes a slot on the discount's `uses` counter. When the order's Shipping Status transitions to `fulfilled`, it satisfies this rule (if not already satisfied by `paid` or `completed`). Cancelled / refunded orders don't consume a slot. See [[marketing-discounts]] counted-status rule.

### Returns are not a Shipping Status

There is no `returned` shipping status. Goods that come back are recorded as a return in the **Returns & exchanges** box ([[orders-details-returns]]), which handles the stock, the credit note and the refund method. A completed **full** return moves the order to `refunded`, which resets a fulfilled order to `not_fulfilled`; a **partial** return leaves the order's statuses unchanged.

### Cancellation gating

The Cancel Order action (Order Status → `cancelled`) is gated by Order Status (`pending` only, with a stock-sufficient check) — the Shipping Status does NOT separately gate cancellation. Cancelling (or refunding) a fulfilled order resets its Shipping Status to `not_fulfilled` automatically; goods that come back are recorded as a return in the **Returns & exchanges** box ([[orders-details-returns]]), not as a shipping status.

### Digital-only orders are fulfilled when paid

An order with only digital products starts as `not_fulfilled` like any other, but the platform marks it `fulfilled` automatically when it becomes `paid`. The merchant does not need to fulfil digital orders by hand.

## Where it appears

- [[orders-details]] — where a manual Shipping Status change triggers these side-effects.
- [[settings-statuses]] — the status taxonomy. The emails are gated by the order's Notify-customer flag, the mail template's own Active flag and the store-wide customer-email setting — not by a per-status toggle.
- [[settings-hooks]] — `order.updated` webhook subscribers that receive every change.
- [[orders-payment-refund]] — the separate refund action on the order's payment.
- [[marketing-discounts]] — the discount uses-counter that `fulfilled` can satisfy.

## Related

- [[shipping-status]] — hub.
- [[order]] — carries the `notify_customer` flag and the three independent statuses.
- [[order-status]] — auto-completion target (`completed`); cancellation gating reads Order Status.
- [[payment-status]] — a separate dimension (fulfilling an order can capture an authorised payment when the gateway supports automatic capture).
- [[discount]] — uses-counter counted-status rule (default includes `fulfilled`).
- [[order-status-workflow]] — how the three statuses interact at status-change time.
- [[notification-delivery]] — how a status change becomes a customer email.
- [[settings-statuses]] — the status taxonomy (no per-status notification toggle).
- [[settings-hooks]] — `order.updated` webhook.
- [[marketing-discounts]] — counted-status rule.
- [[orders-payment-refund]] — the separate refund the merchant must issue after a return.

## Open Questions

No outstanding questions.
