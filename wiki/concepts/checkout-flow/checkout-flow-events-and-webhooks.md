---
type: concept
nav_path: "Concept → Checkout flow → Events & webhooks"
aliases: ["OrderCreated event", "PostOrderCreated", "OrderStatusChange", "PostOrderStatusChange", "DiscountUsageSync", "order.created webhook", "order.updated webhook", "order.deleted webhook", "cart.created webhook", "cart.updated webhook", "order-events8 queue", "notify_customer", "Status change side-effects"]
tags: [orders, checkout, events, webhooks, queues, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[checkout-flow]]. See the hub for the other aspects (cart entity, abandoned detection, submit-to-order, guest vs registered, lifecycle overview, discounts & rules).

# Checkout flow — Events & webhooks

## Definition

This aspect documents the **event + webhook fan-out** during the checkout flow: the `OrderCreated` chain at submit, the `OrderStatusChange` / `PostOrderStatusChange` four-stage side-effect sequence on every status transition, the per-status customer-email gating via [[settings-statuses]] + `notify_customer`, and the three platform-wide order webhook events (`order.created` / `order.updated` / `order.deleted`) plus the cart-side pair (`cart.created` / `cart.updated`). All webhook delivery runs on the `order-events8` queue when triggered from web requests, with the platform's standard **6-attempt retry over 20 minutes** (final-attempt auto-disable + merchant email — see [[settings-hooks-retry]]).

## Scope

Covered:

- The `OrderCreated` event chain fired at submit (step 8 of [[checkout-flow-submit-order-creation]]).
- The 4-stage `OrderStatusChange` / `PostOrderStatusChange` side-effect sequence on every status transition.
- Per-status customer-email gating + `notify_customer` per-order suppression.
- The three order webhooks + cart webhooks + `order-events8` queue routing.
- Draft-gating of `order.created` (the `is_draft` early-return).

Not covered here:

- The submit pipeline itself — see [[checkout-flow-submit-order-creation]].
- The full post-creation order pipeline outside checkout-flow — see [[order-processing-pipeline]].
- The 13-value `payment.status` enum and the payment-side events — see [[payment-status]].
- The status-machine rules — see [[order-status-workflow]].
- Webhook subscription UI + retry profile details — see [[settings-hooks]] + [[notification-delivery]].

## Contrasts

- **`OrderCreated` (event) vs `order.created` (webhook)** — the event is internal the application framework-side fan-out (jobs + listeners); the webhook is one of the outbound HTTP deliveries that the event triggers. The event ALWAYS fires at submit; the webhook does NOT fire if the order is `is_draft = 1`.
- **Inline status-change side-effects vs delayed fallback** — discount-usage increment runs inline on `OrderStatusChange` AND via a delayed `DiscountUsageSync` job (10s delay) as a fallback. The dual-path guarantees the counter is reconciled even if the inline path deadlocked.
- **Customer-notification email vs webhook** — the email is gated by the per-status toggle on [[settings-statuses]] AND the per-order `notify_customer` flag. The webhook is gated only by the webhook subscription's status filter on [[settings-hooks]] — not by `notify_customer`.

## Where it applies

### `OrderCreated` event chain (at submit, step 8)

Fired at the moment the Order row is persisted (after draft confirmation if applicable). Fans out to:

- The **order-confirmation email** job (transactional email to the customer).
- The **per-order analytics** job (`analytics2` queue, 60-second delay).
- The merchant's `order.created` **webhook** deliveries ([[settings-hooks]]).
- Any **app-specific listeners** (e.g. shipping-courier app pre-flight checks, ERP sync).

See [[notification-delivery]] for the email + webhook delivery infrastructure.

### Status-change side-effect sequence (4 stages)

When the order's `status` changes (via `changeStatus` or directly), the platform fires:

1. The **`OrderStatusChange` event** → stock increment/decrement decision runs (`paid` / `pending` / `completed` = decrement, anything else = increment), payment authorisation is cancelled if the status moved to a negative state and there's an active auth hold, then the inline discount-uses increment runs.
2. The **`PostOrderStatusChange` event** → the `order.updated` webhook fires, the customer-notification email queues (if `notify_customer` is ON), an `OrderHistory` row is written, and an `OrderStatusHistory` row records the previous/new status pair.
3. A **`DiscountUsageSync`** job is queued with a **10-second delay** as a fallback — this guarantees the discount-uses counter is reconciled even if the inline path deadlocked.
4. The **`saving` hook** auto-promotes to `completed` if the new state matches `paid` + `fulfilled` + the store setting `order_complete = 1` — without firing a third status-change event explicitly (the auto-promotion writes to the same DB row in the same save). See [[checkout-flow-order-lifecycle-overview]].

### Customer email at each transition

Each canonical status (`pending`, `paid`, `completed`, etc.) has a customer-notification toggle on [[settings-statuses]]. When the order's status changes and the new status's toggle is ON, the platform queues a transactional email to the customer's email address. Custom statuses (merchant-defined sub-labels) also have their own toggles.

Per-order, the merchant can **suppress** future status-change emails via [[orders-notify-customer]] (sets `notify_customer = 0` on the order). Toggling does NOT re-send the current status's email — the merchant must re-apply the status to re-fire.

### Order webhooks

Three platform-wide order webhook events fire via [[settings-hooks]]:

| Event | When |
|-------|------|
| `order.created` | New order is persisted (after draft confirmation if applicable). |
| `order.updated` | Order is edited — status change, address edit, payment confirmation, line-item change, archive toggle. |
| `order.deleted` | Order is permanently deleted (NOT fired on archive). |

Webhooks deliver with 6 attempts over 20 minutes — see [[notification-delivery]] for the retry profile.

Cart-side webhook events also fire (`cart.created` / `cart.updated`) — but most merchants subscribe only to the order events.

### Draft gating — `is_draft` early-return

The `order.created` webhook is dispatched from the order's `hooks('created')` method, called inside the `PostOrderCreated` event listener. The method checks `meta_pluck->get('is_draft')` and **early-returns** if the order is in draft state — so the webhook never fires for in-progress draft orders. When the merchant flips a draft to live by clicking **Create order** in [[orders-add]], the same `hooks('created')` runs again and the webhook fires exactly once at that moment. (verify hook + meta-key names)

So for draft-to-live conversions, the `order.created` webhook DOES fire — not `order.updated`. The `is_draft` meta flag is removed at the same moment.

### `order-events8` queue

The `order.created` and `order.updated` webhooks are dispatched via the **`order-events8`** queue when triggered from a web request (not a console job). This is a dedicated queue per the platform's high-volume event handling — separate from the marketing / system queues, so cart-side traffic and abandoned-cart sweeps don't compete with order events for processing slots. (verify queue name)

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-submit-order-creation]] — where the `OrderCreated` event fires (step 8).
- [[checkout-flow-order-lifecycle-overview]] — the lifecycle the status-change events drive.
- [[checkout-flow-discounts-and-rules]] — the `DiscountUsageSync` fallback path.
- [[order-processing-pipeline]] — the full post-submit pipeline this fan-out feeds.
- [[order-status-workflow]] — per-status transition rules.
- [[notification-delivery]] — webhook + email delivery infrastructure + retry profile.
- [[settings-hooks]] — webhook subscriptions for `order.*` / `cart.*`.
- [[settings-statuses]] — order-status taxonomy + `discounts_used_statuses` (no per-status notification toggle exists).
- [[orders-notify-customer]] — per-order `notify_customer` suppression.
- [[orders-history]] — `OrderHistory` row written by stage 2.
- [[orders-add]] — draft-to-live conversion that re-fires `hooks('created')`.
- [[plan-gates]] — quota gates that consume webhook + email events.

## Open Questions

- Confirm the `order-events8` queue name against current the platform code (verify).
- Confirm `analytics2` is the queue + 60-second delay for the per-order analytics job (verify).
- Confirm `DiscountUsageSync` is the exact job class name + 10-second delay (verify).
