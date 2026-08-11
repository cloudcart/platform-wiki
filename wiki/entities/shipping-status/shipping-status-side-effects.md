---
type: entity
nav_path: "Entity → Shipping Status → Side-effects"
aliases: ["Shipping status side effects", "Fulfillment side effects", "Auto-completion rule", "Shipping status notifications", "Shipping status webhook", "Странични ефекти на статус на доставка"]
tags: [entity, orders, shipping, statuses]
created: 2026-06-10
updated: 2026-06-10
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

The three statuses move independently — the merchant cannot infer one from another. An order can be:

- `status = paid`, `status_fulfillment = not_fulfilled` (paid but not yet packed — typical post-checkout state for many minutes to hours).
- `status = paid`, `status_fulfillment = fulfilled` (paid and packed — ready for pickup).
- `status = completed`, `payment = refunded`, `fulfillment = returned` (the whole order has been reversed but the merchant marked it Complete first).

### Auto-completion rule

The platform auto-promotes the Order Status to `completed` when ALL of the following hold simultaneously on a save:

- `status = paid` (Order Status)
- `status_fulfillment = fulfilled` (Shipping Status)
- Store setting `order_complete = 1` (the merchant opted into auto-completion)

If the merchant didn't opt into auto-completion, the order stays at `paid` + `fulfilled` until the merchant manually marks it `completed`. See [[order-status-workflow]].

### Auto-completion fires TWO customer notifications

When the auto-completion rule fires (paid + fulfilled + `order_complete = 1`), the save writes BOTH the `fulfilled` change AND the `completed` change in the same save. The customer receives **TWO emails** (one for fulfilled, one for completed) IF both statuses have customer-notification ON in [[settings-statuses]]. To send only one email, the merchant turns OFF customer-notification for one of the two statuses.

### Customer notification is per-status, controllable per-status AND per-order

Each canonical Shipping Status has a customer-notification toggle in [[settings-statuses]] (see [[shipping-status-values]]). When ON, the platform sends an email via [[notification-delivery|notification dispatch]] when the order transitions to that status. The toggle can be turned OFF per status (e.g., the merchant might silence the `fulfilled` email if they prefer to email only on `shipped`).

Additionally, each order has a `notify_customer` flag — when OFF on the order, ALL automated customer emails (across all status types) are suppressed. The merchant uses this to silence a problematic order without changing global settings. See [[order]] business rules.

### Webhook on every change

Every Shipping Status change is a save on the order, which fires the platform-wide `order.updated` webhook to [[settings-hooks]] subscribers. The payload includes `status_fulfillment` (the new value) as a top-level field on the Order snapshot. There is **no separate "old value" field** — subscribers wanting to detect transitions must compare against their own prior snapshot. The platform does **not** emit a separate `shipping.status.changed` event.

### Discount uses-counter and fulfillment

The `discounts_used_statuses` setting (default: `paid`, `completed`, `fulfilled`) drives whether a [[discount|Discount]] applied to the order consumes a slot on the discount's `uses` counter. When the order's Shipping Status transitions to `fulfilled`, it satisfies this rule (if not already satisfied by `paid` or `completed`). Cancelled / refunded orders don't consume a slot. See [[marketing-discounts]] counted-status rule.

### Return handling does NOT auto-reverse payment

Setting `status_fulfillment = returned` marks the parcel as returned but does NOT automatically refund the payment. The merchant must separately issue a refund via [[orders-payment-refund]] (or whatever refund flow the payment provider supports). The two are distinct actions because the merchant may want to charge a restocking fee, partial refund, or extend store credit instead.

### Cancellation gating

The Cancel Order action (Order Status → `cancelled`) is gated by Order Status (`pending` only, with a stock-sufficient check) — the Shipping Status does NOT separately gate cancellation. However, in practice, the merchant typically should NOT cancel an order that's already `shipped` — the parcel is in transit and needs to be returned (set `returned`) and refunded, not cancelled.

### Digital-only stores still carry `not_fulfilled`

Even when every product has `shipping = no`, the Order still carries `status_fulfillment = not_fulfilled` by default. The merchant typically ignores the value entirely for digital Orders — completion is driven by payment + the auto-completion rule (when enabled). The merchant can manually mark digital Orders `fulfilled` to trigger the discount-uses counted-status rule.

## Where it appears

- [[orders-details]] — where a manual Shipping Status change triggers these side-effects.
- [[settings-statuses]] — the status taxonomy. The emails are gated by the order's Notify-customer flag, the mail template's own Active flag and the store-wide customer-email setting — not by a per-status toggle.
- [[settings-hooks]] — `order.updated` webhook subscribers that receive every change.
- [[orders-payment-refund]] — the separate refund action a `returned` status does NOT trigger automatically.
- [[marketing-discounts]] — the discount uses-counter that `fulfilled` can satisfy.

## Related

- [[shipping-status]] — hub.
- [[order]] — carries the `notify_customer` flag and the three independent statuses.
- [[order-status]] — auto-completion target (`completed`); cancellation gating reads Order Status.
- [[payment-status]] — independent; `returned` does NOT auto-reverse it.
- [[discount]] — uses-counter counted-status rule (default includes `fulfilled`).
- [[order-status-workflow]] — how the three statuses interact at status-change time.
- [[notification-delivery]] — how a status change becomes a customer email.
- [[settings-statuses]] — the status taxonomy (no per-status notification toggle).
- [[settings-hooks]] — `order.updated` webhook.
- [[marketing-discounts]] — counted-status rule.
- [[orders-payment-refund]] — the separate refund the merchant must issue after a return.

## Open Questions

No outstanding questions.
